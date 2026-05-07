"""
main.py
-------
Point d'entrée principal de l'application SGP (Système de Gestion de Projets).
Gère l'affichage de la fenêtre de connexion et de la fenêtre principale avec sidebar.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QPushButton, QStackedWidget, QFrame, QStatusBar
)
from PyQt6.QtCore import Qt
import qtawesome as qta
import ctypes
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon

from login_window import LoginWindow
from views.dashboard_view import DashboardView
from views.projects_view import ProjectsView
from views.tasks_view import TasksView
from views.team_view import TeamView
from views.reports_view import ReportsView
from views.profile_view import ProfileView
from views.planning_view import PlanningView
from views.documents_view import DocumentsView
from logger_config import app_logger

# Configuration de la base de données
db_config = {
    'dbname': 'sgp_db',
    'user': 'sgp_user',
    'password': 'sgp_password',
    'host': 'localhost',
    'port': '5432'
}

# Libellés des rôles (RBAC)
ROLE_LABELS = {
    1: "Administrateur",
    2: "Chef de Projet",
    3: "Membre Équipe",
    4: "Client",
    5: "Direction"
}


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application SGP avec sidebar de navigation."""

    def __init__(self, user_info: dict, login_window_ref):
        """
        Initialise la fenêtre principale.

        Args:
            user_info: Dictionnaire contenant les informations de l'utilisateur connecté.
            login_window_ref: Référence à la fenêtre de login pour la déconnexion.
        """
        super().__init__()
        self.user_info = user_info
        self.login_window = login_window_ref
        self.setWindowTitle("SGP – Système de Gestion de Projets")
        self.resize(1200, 750)
        app_logger.info(f"Connexion utilisateur: {user_info.get('nom_utilisateur')} (rôle: {user_info.get('id_role')})")
        
        # Set Window Icon using the app logo
        logo_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_icon_path):
            self.setWindowIcon(QIcon(logo_icon_path))
        else:
            self.setWindowIcon(qta.icon('fa5s.layer-group', color='#3182CE'))
        
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur principale."""
        # Charge la feuille de style globale
        style_path = os.path.join(os.path.dirname(__file__), 'style.qss')
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- SIDEBAR ----
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(210)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # En-tête sidebar : logo + titre
        brand_widget = QWidget()
        brand_widget.setStyleSheet("background-color: #111827; padding: 10px 0 10px 0;")
        brand_layout = QVBoxLayout(brand_widget)
        brand_layout.setContentsMargins(10, 10, 10, 10)
        brand_layout.setSpacing(5)

        logo_lbl = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_lbl.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setPixmap(qta.icon('fa5s.layer-group', color='#63B3ED').pixmap(32, 32))
        
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_layout.addWidget(logo_lbl)

        title_brand = QLabel("SGP - Gestion de Projets")
        title_brand.setObjectName("SidebarSubtitle") # Using subtitle style for better fit
        title_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_layout.addWidget(title_brand)

        sidebar_layout.addWidget(brand_widget)

        # Séparateur
        divider = QFrame()
        divider.setObjectName("SidebarDivider")
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #2D3748; margin: 0 0;")
        sidebar_layout.addWidget(divider)

        sidebar_layout.addSpacing(10)

        # Boutons de navigation
        self.btn_dashboard = self._make_nav_btn("  Tableau de Bord", 'fa5s.tachometer-alt', lambda: self.switch_view(0))
        self.btn_projects = self._make_nav_btn("  Projets", 'fa5s.folder', lambda: self.switch_view(1))
        self.btn_tasks = self._make_nav_btn("  Tâches", 'fa5s.tasks', lambda: self.switch_view(2))
        self.btn_planning = self._make_nav_btn("  Planning", 'fa5s.stream', lambda: self.switch_view(3))
        self.btn_documents = self._make_nav_btn("  Documents", 'fa5s.file-alt', lambda: self.switch_view(4))
        self.btn_team = self._make_nav_btn("  Équipe", 'fa5s.users', lambda: self.switch_view(5))
        self.btn_reports = self._make_nav_btn("  Rapports", 'fa5s.chart-bar', lambda: self.switch_view(6))
        self.btn_profile = self._make_nav_btn("  Profil", 'fa5s.user', lambda: self.switch_view(7))

        # Marquer le premier comme actif
        self.btn_dashboard.setChecked(True)

        self.nav_buttons = [
            self.btn_dashboard, self.btn_projects, self.btn_tasks, 
            self.btn_planning, self.btn_documents, self.btn_team, 
            self.btn_reports, self.btn_profile
        ]

        # RBAC: Dynamic Sidebar filtering
        role_id = self.user_info.get("id_role", 0)
        
        # Hide Team for Member (3) and Client (4)
        if role_id in [3, 4]:
            self.btn_team.setVisible(False)
            
        # Hide Reports for Member (3) and Client (4)
        if role_id in [3, 4]:
            self.btn_reports.setVisible(False)

        # Hide Planning for Client (4)
        if role_id == 4:
            self.btn_planning.setVisible(False)
            
        # Client specific: Change Dashboard title
        if role_id == 4:
            self.btn_dashboard.setText("  Aperçu")
        
        for btn in self.nav_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Divider bas
        div_bottom = QFrame()
        div_bottom.setFixedHeight(1)
        div_bottom.setStyleSheet("background-color: #2D3748; margin: 0;")
        sidebar_layout.addWidget(div_bottom)

        # Info utilisateur connecté
        user_widget = QWidget()
        user_widget.setStyleSheet("background-color: #111827; padding: 10px 16px;")
        user_layout = QVBoxLayout(user_widget)
        user_layout.setContentsMargins(0, 8, 0, 8)
        user_layout.setSpacing(2)

        role_id = self.user_info.get("id_role", 0)
        role_lbl_text = ROLE_LABELS.get(role_id, "Utilisateur")

        user_name_lbl = QLabel(self.user_info.get("nom_utilisateur", "Utilisateur"))
        user_name_lbl.setStyleSheet("color: #E2E8F0; font-weight: bold; font-size: 13px;")
        user_role_lbl = QLabel(role_lbl_text)
        user_role_lbl.setStyleSheet("color: #718096; font-size: 11px;")
        user_layout.addWidget(user_name_lbl)
        user_layout.addWidget(user_role_lbl)
        sidebar_layout.addWidget(user_widget)

        # Bouton de déconnexion
        self.btn_logout = QPushButton("  Déconnexion")
        self.btn_logout.setIcon(qta.icon('fa5s.sign-out-alt', color='#FC8181'))
        self.btn_logout.setStyleSheet(
            "background-color: #111827; color: #FC8181; font-weight: bold; "
            "text-align: left; padding: 14px 20px; border: none; font-size: 13px;"
        )
        self.btn_logout.clicked.connect(self.logout)
        sidebar_layout.addWidget(self.btn_logout)

        # Done above in a cleaner way

        # ---- ZONE DE CONTENU ----
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget()

        self.dashboard_view = DashboardView(db_config, self.user_info)
        self.projects_view = ProjectsView(db_config, self.user_info)
        self.tasks_view = TasksView(db_config, self.user_info)
        self.planning_view = PlanningView(db_config, self.user_info)
        self.documents_view = DocumentsView(db_config, self.user_info)
        self.team_view = TeamView(db_config, self.user_info)
        self.reports_view = ReportsView(db_config, self.user_info)
        self.profile_view = ProfileView(db_config, self.user_info)

        self.stacked_widget.addWidget(self.dashboard_view)   # Index 0
        self.stacked_widget.addWidget(self.projects_view)    # Index 1
        self.stacked_widget.addWidget(self.tasks_view)       # Index 2
        self.stacked_widget.addWidget(self.planning_view)    # Index 3
        self.stacked_widget.addWidget(self.documents_view)   # Index 4
        self.stacked_widget.addWidget(self.team_view)        # Index 5
        self.stacked_widget.addWidget(self.reports_view)     # Index 6
        self.stacked_widget.addWidget(self.profile_view)     # Index 7

        content_layout.addWidget(self.stacked_widget)

        # Assemblage final
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

        # ---- BARRE DE STATUT ----
        status_bar = QStatusBar()
        status_bar.setObjectName("MainStatusBar")
        self.setStatusBar(status_bar)
        status_bar.showMessage(
            f"  Connecté en tant que  {self.user_info.get('nom_utilisateur', '')}  |  "
            f"Rôle : {role_lbl_text}  |  Base de données : sgp_db"
        )

    def _make_nav_btn(self, text: str, icon_name: str, callback) -> QPushButton:
        """
        Crée un bouton de navigation pour la sidebar.

        Args:
            text: Texte du bouton.
            icon_name: Nom de l'icône qtawesome.
            callback: Fonction appelée au clic.

        Returns:
            QPushButton configuré.
        """
        btn = QPushButton(text)
        btn.setIcon(qta.icon(icon_name, color='#A0AEC0'))
        btn.setCheckable(True)
        btn.clicked.connect(callback)
        return btn

    def switch_view(self, index: int):
        """
        Bascule vers la vue correspondante à l'index.

        Args:
            index: Index de la vue dans le QStackedWidget.
        """
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        self.stacked_widget.setCurrentIndex(index)

        # Recharge automatique des données lors du changement de vue
        current_widget = self.stacked_widget.currentWidget()
        for method_name in ['load_data', 'load_metadata', 'load_roles', 'load_table', 'load_projects']:
            if hasattr(current_widget, method_name):
                try:
                    getattr(current_widget, method_name)()
                except Exception as e:
                    app_logger.warning(f"Erreur lors du rechargement de {method_name}: {e}")

    def logout(self):
        """Déconnecte l'utilisateur et affiche à nouveau la fenêtre de login."""
        app_logger.info(f"Déconnexion de l'utilisateur: {self.user_info.get('nom_utilisateur')}")
        if self.login_window:
            self.login_window.email_input.clear()
            self.login_window.password_input.clear()
            self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ---- Fix for Windows Taskbar Icon ----
    if sys.platform == 'win32':
        myappid = 'telnet.sgp.projectmanagement.v1' # Unique ID
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Set global application icon using the app logo
    _app_logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
    if os.path.exists(_app_logo_path):
        app.setWindowIcon(QIcon(_app_logo_path))
    else:
        app.setWindowIcon(qta.icon('fa5s.layer-group', color='#3182CE'))

    # ---- Forcer le thème Fusion (clair) pour neutraliser le dark mode Windows ----
    app.setStyle("Fusion")
    light_palette = QPalette()
    light_palette.setColor(QPalette.ColorRole.Window,          QColor("#F0F4F8"))
    light_palette.setColor(QPalette.ColorRole.WindowText,      QColor("#1A202C"))
    light_palette.setColor(QPalette.ColorRole.Base,            QColor("#FFFFFF"))
    light_palette.setColor(QPalette.ColorRole.AlternateBase,   QColor("#F7FAFC"))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase,     QColor("#1A202C"))
    light_palette.setColor(QPalette.ColorRole.ToolTipText,     QColor("#FFFFFF"))
    light_palette.setColor(QPalette.ColorRole.Text,            QColor("#2D3748"))
    light_palette.setColor(QPalette.ColorRole.Button,          QColor("#EDF2F7"))
    light_palette.setColor(QPalette.ColorRole.ButtonText,      QColor("#2D3748"))
    light_palette.setColor(QPalette.ColorRole.BrightText,      QColor("#FFFFFF"))
    light_palette.setColor(QPalette.ColorRole.Link,            QColor("#3182CE"))
    light_palette.setColor(QPalette.ColorRole.Highlight,       QColor("#3182CE"))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
    light_palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#A0AEC0"))
    app.setPalette(light_palette)

    # Charge la feuille de style globale (après palette pour que QSS ait priorité)
    style_path = os.path.join(os.path.dirname(__file__), 'style.qss')
    if os.path.exists(style_path):
        with open(style_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

    app_logger.info("Démarrage de l'application SGP")

    login_window = LoginWindow(db_config)
    main_window = None

    def show_main_window(user_info: dict):
        global main_window
        main_window = MainWindow(user_info, login_window)
        main_window.show()

    login_window.login_successful.connect(show_main_window)
    login_window.show()

    sys.exit(app.exec())
