import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QSpacerItem, QSizePolicy, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPixmap
import qtawesome as qta
from db_connection import DbConnection
from auth_utils import check_password

# Libellés rôles pour le quick-login
_ROLE_LABELS = {1: "Admin", 2: "Chef", 3: "Membre", 4: "Client", 5: "Direction"}

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)

    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.setObjectName("LoginWindow")
        self.setWindowTitle("SGP - Connexion")
        self.resize(800, 600)
        # Force le rendu du fond même en dark mode Windows
        self.setAutoFillBackground(True)
        self.setStyleSheet("QWidget#LoginWindow { background-color: #EDF2F7; }")
        
        # Set Window Icon using the app logo
        logo_icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
        if os.path.exists(logo_icon_path):
            self.setWindowIcon(QIcon(logo_icon_path))
        else:
            self.setWindowIcon(qta.icon('fa5s.layer-group', color='#3182CE'))
            
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Main Card container
        self.card = QFrame()
        self.card.setObjectName("LoginCard")
        self.card.setFixedWidth(450)
        self.card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        
        # Shadow effect (optional, relies on QSS or QGraphicsDropShadowEffect)
        # Using QSS for simpler border structure
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(15)
        
        # Logo and Title Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(0)
        
        telnet_logo_label = QLabel()
        telnet_logo_label.setObjectName("LoginLogo")
        telnet_logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'telnet_logo.png')
        if os.path.exists(telnet_logo_path):
            pixmap_telnet = QPixmap(telnet_logo_path)
            telnet_logo_label.setPixmap(pixmap_telnet.scaled(280, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_icon = qta.icon('fa5s.layer-group', color='#3182CE')
            telnet_logo_label.setPixmap(logo_icon.pixmap(80, 80))
        telnet_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(telnet_logo_label)
        
        card_layout.addLayout(header_layout)
        
        # Spacer
        card_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # User Label
        user_lbl_layout = QHBoxLayout()
        user_icon_lbl = QLabel()
        user_icon_lbl.setPixmap(qta.icon('fa5s.user', color='#4A5568').pixmap(16, 16))
        user_lbl_txt = QLabel("Nom d'utilisateur")
        user_lbl_txt.setStyleSheet("color: #2D3748; font-weight: 500; font-size: 14px;")
        user_lbl_layout.addWidget(user_icon_lbl)
        user_lbl_layout.addWidget(user_lbl_txt)
        user_lbl_layout.addStretch()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Nom d'utilisateur ou Email")
        
        card_layout.addLayout(user_lbl_layout)
        card_layout.addWidget(self.email_input)
        
        # Password Label
        pass_lbl_layout = QHBoxLayout()
        pass_icon_lbl = QLabel()
        pass_icon_lbl.setPixmap(qta.icon('fa5s.lock', color='#4A5568').pixmap(16, 16))
        pass_lbl_txt = QLabel("Mot de passe")
        pass_lbl_txt.setStyleSheet("color: #2D3748; font-weight: 500; font-size: 14px;")
        pass_lbl_layout.addWidget(pass_icon_lbl)
        pass_lbl_layout.addWidget(pass_lbl_txt)
        pass_lbl_layout.addStretch()
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("••••••••")
        
        card_layout.addLayout(pass_lbl_layout)
        card_layout.addWidget(self.password_input)
        
        # Forgot password link
        forgot_pw = QLabel("<a href='#' style='color:#3182CE; text-decoration:none;'>Mot de passe oublié ?</a>")
        forgot_pw.setObjectName("ForgotPassLink")
        forgot_pw.setOpenExternalLinks(False)
        forgot_pw.linkActivated.connect(self.handle_forgot_password)
        card_layout.addWidget(forgot_pw)
        
        card_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Login Button
        self.login_button = QPushButton("Connexion")
        self.login_button.setObjectName("PrimaryLoginBtn")
        self.login_button.setProperty("class", "PrimaryButton")
        self.login_button.clicked.connect(self.attempt_login)
        card_layout.addWidget(self.login_button)

        # ---- Section Quick Login (Dev / Test) ----
        card_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        divider_dev = QFrame()
        divider_dev.setFrameShape(QFrame.Shape.HLine)
        divider_dev.setStyleSheet("background-color: #E2E8F0;")
        card_layout.addWidget(divider_dev)

        card_layout.addSpacerItem(QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        quick_title = QLabel("⚡ Connexion rapide (Test)")
        quick_title.setStyleSheet("color: #718096; font-size: 12px; font-weight: 600;")
        card_layout.addWidget(quick_title)

        quick_row = QHBoxLayout()
        quick_row.setSpacing(6)

        self.quick_combo = QComboBox()
        self.quick_combo.setPlaceholderText("Sélectionner un utilisateur...")
        self.quick_combo.setStyleSheet(
            "QComboBox { padding: 8px; font-size: 12px; border: 1px solid #CBD5E0; border-radius: 6px; }"
        )
        quick_row.addWidget(self.quick_combo, stretch=1)

        self.btn_quick_login = QPushButton("➜")
        self.btn_quick_login.setFixedSize(40, 36)
        self.btn_quick_login.setStyleSheet(
            "QPushButton { background-color: #48BB78; color: white; font-size: 16px; "
            "font-weight: bold; border-radius: 6px; border: none; }"
            "QPushButton:hover { background-color: #38A169; }"
        )
        self.btn_quick_login.setToolTip("Connexion directe sans mot de passe")
        self.btn_quick_login.clicked.connect(self.quick_login)
        quick_row.addWidget(self.btn_quick_login)

        card_layout.addLayout(quick_row)

        card_layout.addStretch()
        
        main_layout.addWidget(self.card)

        # Charger les utilisateurs pour le quick-login
        self._load_quick_users()

    def _load_quick_users(self):
        """Charge la liste des utilisateurs pour le quick-login."""
        db = DbConnection(**self.db_config)
        conn = db.connect()
        if not conn:
            return
        try:
            users = db.fetch_data(
                "SELECT id_utilisateur, nom_utilisateur, email, id_role, "
                "COALESCE(actif, TRUE) FROM Utilisateurs ORDER BY id_role, nom_utilisateur;"
            )
            self.quick_combo.clear()
            self._quick_users = {}
            for uid, nom, email, role_id, actif in (users or []):
                role_lbl = _ROLE_LABELS.get(role_id, "?")
                status = " [INACTIF]" if not actif else ""
                display = f"[{role_lbl}] {nom}{status}"
                self.quick_combo.addItem(display, email)
                self._quick_users[email] = {
                    "id_utilisateur": uid,
                    "nom_utilisateur": nom,
                    "email": email,
                    "id_role": role_id,
                    "actif": actif
                }
        except Exception as e:
            pass
        finally:
            db.close()

    def quick_login(self):
        """Connexion directe sans mot de passe (pour les tests)."""
        email = self.quick_combo.currentData()
        if not email or email not in self._quick_users:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur.")
            return

        user_basic = self._quick_users[email]

        # Bloquer les comptes désactivés même en quick-login
        if not user_basic.get("actif", True):
            QMessageBox.warning(
                self, "Compte Désactivé",
                "Ce compte est désactivé. Utilisez la vue Équipe pour le réactiver."
            )
            return

        # Charger les données complètes
        db = DbConnection(**self.db_config)
        conn = db.connect()
        if not conn:
            return
        try:
            user_data = db.fetch_single_data(
                "SELECT id_utilisateur, nom_utilisateur, email, mot_de_passe, id_role, "
                "peut_reviser, photo_profil, COALESCE(actif, TRUE) "
                "FROM Utilisateurs WHERE email = %s;",
                (email,)
            )
            if user_data:
                user_dict = {
                    "id_utilisateur": user_data[0],
                    "nom_utilisateur": user_data[1],
                    "email": user_data[2],
                    "mot_de_passe_hashed": user_data[3],
                    "id_role": user_data[4],
                    "peut_reviser": user_data[5],
                    "photo_profil": user_data[6],
                    "actif": user_data[7]
                }
                self.login_successful.emit(user_dict)
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de connexion rapide : {e}")
        finally:
            db.close()

    def handle_forgot_password(self, link):
        """Affiche une boîte de dialogue d'aide en cas de mot de passe oublié."""
        msg = QMessageBox(self)
        msg.setWindowTitle("Réinitialisation du mot de passe")
        msg.setText("<b>Mot de passe oublié ?</b>")
        msg.setInformativeText(
            "Pour des raisons de sécurité, veuillez contacter votre administrateur SGP "
            "ou l'équipe IT de Telnet Holding pour réinitialiser votre accès.<br><br>"
            "📞 <b>Support :</b> +216 XX XXX XXX<br>"
            "📧 <b>Email :</b> support@telnet.com"
        )
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet("QLabel{min-width: 350px; font-size: 13px;}")
        msg.exec()

    def attempt_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        db = DbConnection(**self.db_config)
        conn = db.connect()
        if conn:
            try:
                user_data = db.fetch_single_data(
                    "SELECT id_utilisateur, nom_utilisateur, email, mot_de_passe, id_role, "
                    "peut_reviser, photo_profil, COALESCE(actif, TRUE) "
                    "FROM Utilisateurs WHERE email = %s OR nom_utilisateur = %s;",
                    (email, email)
                )

                if user_data:
                    user_dict = {
                        "id_utilisateur": user_data[0],
                        "nom_utilisateur": user_data[1],
                        "email": user_data[2],
                        "mot_de_passe_hashed": user_data[3],
                        "id_role": user_data[4],
                        "peut_reviser": user_data[5],
                        "photo_profil": user_data[6],
                        "actif": user_data[7]
                    }

                    if check_password(password, user_dict["mot_de_passe_hashed"]):
                        # Bloquer les comptes désactivés
                        if not user_dict["actif"]:
                            QMessageBox.warning(
                                self, "Compte Désactivé",
                                "Votre compte a été désactivé par un administrateur.\n\n"
                                "Veuillez contacter l'équipe IT de Telnet Holding pour "
                                "rétablir votre accès."
                            )
                            return
                        self.login_successful.emit(user_dict)
                        self.close()
                    else:
                        QMessageBox.warning(self, "Erreur", "Email ou mot de passe incorrect.")
                else:
                    QMessageBox.warning(self, "Erreur", "Email ou mot de passe incorrect.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")
            finally:
                db.close()
        else:
            QMessageBox.critical(self, "Erreur DB", "Impossible de se connecter à la base de données. Assurez-vous d'avoir exécuté init_db.py")

if __name__ == "__main__":
    db_config_test = {
        'dbname': 'sgp_db',
        'user': 'sgp_user',
        'password': 'sgp_password',
        'host': 'localhost',
        'port': '5432'
    }
    app = QApplication([])
    
    # Load stylesheet for testing
    style_path = os.path.join(os.path.dirname(__file__), 'style.qss')
    if os.path.exists(style_path):
        with open(style_path, 'r') as f:
            app.setStyleSheet(f.read())
            
    window = LoginWindow(db_config_test)
    window.show()
    app.exec()
