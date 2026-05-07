"""
seed_test_data.py
-----------------
Injecte des données de test réalistes dans la base de données SGP.
Crée des utilisateurs pour chaque rôle, des projets, des tâches avec
différents statuts/priorités, des commentaires/preuves, et des rapports.

Tous les mots de passe sont : test123

Usage:
    python seed_test_data.py
"""

import sys
import os
from datetime import date, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_connection import DbConnection
from auth_utils import hash_password

# ======================================================================
# Configuration
# ======================================================================

db_config = {
    'dbname': 'sgp_db',
    'user': 'sgp_user',
    'password': 'sgp_password',
    'host': 'localhost',
    'port': '5432'
}

# Mot de passe commun pour tous les utilisateurs de test
PASSWORD = hash_password("test123")

# ======================================================================
# Données de test réalistes
# ======================================================================

USERS = [
    # (nom, email, id_role, peut_reviser, actif)
    # --- Administrateurs ---
    ("Sami Ben Ali",       "sami.benali@telnet.tn",      1, True,  True),
    # --- Chefs de Projet ---
    ("Amira Trabelsi",     "amira.trabelsi@telnet.tn",   2, True,  True),
    ("Youssef Hammami",    "youssef.hammami@telnet.tn",  2, True,  True),
    ("Nadia Mansouri",     "nadia.mansouri@telnet.tn",   2, False, True),
    # --- Membres Équipe ---
    ("Khalil Bouazizi",    "khalil.bouazizi@telnet.tn",  3, False, True),
    ("Ines Chaabane",      "ines.chaabane@telnet.tn",    3, False, True),
    ("Mohamed Jaziri",     "mohamed.jaziri@telnet.tn",   3, True,  True),
    ("Rania Sfar",         "rania.sfar@telnet.tn",       3, False, True),
    ("Tarek Bouzid",       "tarek.bouzid@telnet.tn",     3, False, True),
    ("Salma Khelifi",      "salma.khelifi@telnet.tn",    3, False, False),  # Inactif !
    # --- Clients ---
    ("Groupe Poulina",     "contact@poulina.tn",         4, False, True),
    ("Banque BH",          "projets@bh.tn",              4, False, True),
    # --- Direction ---
    ("Moncef Sellami",     "moncef.sellami@telnet.tn",   5, False, True),
]

PROJECTS = [
    # (nom, description, statut, chef_email, client_email_or_None, est_modele, jours_debut, jours_duree)
    (
        "Plateforme E-Commerce Poulina",
        "Développement d'une plateforme de vente en ligne B2C pour le Groupe Poulina avec paiement intégré, gestion de stock et tableau de bord analytics.",
        "En Cours",
        "amira.trabelsi@telnet.tn",
        "contact@poulina.tn",
        False, -30, 90
    ),
    (
        "Application Mobile BH Bank",
        "Conception et développement d'une application mobile bancaire (iOS/Android) avec authentification biométrique et virements instantanés.",
        "En Cours",
        "youssef.hammami@telnet.tn",
        "projets@bh.tn",
        False, -15, 120
    ),
    (
        "Migration Cloud Infrastructure",
        "Migration de l'infrastructure on-premise vers AWS : serveurs, bases de données, CI/CD pipelines et monitoring.",
        "En Attente",
        "amira.trabelsi@telnet.tn",
        None,
        False, 10, 60
    ),
    (
        "Système de Gestion RH",
        "Outil interne de gestion des ressources humaines : fiches employés, congés, évaluations et paie.",
        "Terminé",
        "youssef.hammami@telnet.tn",
        None,
        False, -90, 75
    ),
    (
        "Audit Sécurité SI",
        "Audit complet de la sécurité des systèmes d'information : pentesting, analyse des vulnérabilités, conformité ISO 27001.",
        "Annulé",
        "amira.trabelsi@telnet.tn",
        None,
        False, -20, 30
    ),
    (
        "Template Projet Standard",
        "Blueprint standard pour les nouveaux projets IT avec phases pré-définies.",
        "En Attente",
        "amira.trabelsi@telnet.tn",
        None,
        True, -5, 60
    ),
]

# Tâches par projet (index dans PROJECTS)
TASKS = {
    0: [  # Plateforme E-Commerce Poulina
        ("Analyse des besoins client",         "Recueil et formalisation des exigences fonctionnelles du client Poulina.",    "Terminé",    "Haute",   "khalil.bouazizi@telnet.tn",  100, -28, 7),
        ("Maquettes UI/UX",                    "Design des interfaces utilisateur avec Figma (desktop + mobile).",           "Terminé",    "Haute",   "ines.chaabane@telnet.tn",    100, -21, 10),
        ("Architecture technique",             "Définition de l'architecture microservices et choix des technologies.",       "Terminé",    "Moyenne", "mohamed.jaziri@telnet.tn",   100, -20, 5),
        ("Développement API Backend",          "Développement des endpoints REST (catalogue, panier, commandes, paiement).", "En Cours",   "Haute",   "khalil.bouazizi@telnet.tn",   65, -14, 21),
        ("Intégration passerelle de paiement", "Intégration de la passerelle Stripe/Flouci pour les transactions en ligne.", "En Cours",   "Haute",   "mohamed.jaziri@telnet.tn",    40, -7, 14),
        ("Développement Frontend React",       "Développement des pages (catalogue, fiche produit, checkout, dashboard).",   "En Cours",   "Moyenne", "ines.chaabane@telnet.tn",     30, -10, 25),
        ("Tests d'intégration",                "Tests E2E et intégration continue avec Jenkins pipeline.",                   "À Faire",    "Moyenne", "rania.sfar@telnet.tn",         0,  14, 10),
        ("Déploiement staging",                "Mise en production sur l'environnement de pré-production.",                  "À Faire",    "Basse",   "tarek.bouzid@telnet.tn",       0,  24, 5),
        ("Formation utilisateurs",             "Formation du personnel Poulina à l'utilisation de la plateforme.",           "À Faire",    "Basse",   None,                           0,  30, 5),
    ],
    1: [  # Application Mobile BH Bank
        ("Cahier des charges fonctionnel",  "Rédaction du cahier des charges avec les équipes métier de BH Bank.",            "Terminé",  "Haute",   "rania.sfar@telnet.tn",       100, -14, 7),
        ("Design System Mobile",            "Création du Design System (composants, tokens, typographie) sur Figma.",         "En Cours", "Haute",   "ines.chaabane@telnet.tn",     70, -10, 14),
        ("Backend API bancaire",            "Développement des services (authentification, consultation solde, virements).",  "En Cours", "Haute",   "khalil.bouazizi@telnet.tn",   45, -7, 28),
        ("Module biométrique",              "Intégration Face ID / Touch ID / empreinte digitale pour l'authentification.",   "En Cours", "Haute",   "mohamed.jaziri@telnet.tn",    25, -3, 14),
        ("Ecrans de consultation",          "Développement des écrans Flutter (historique, RIB, relevés PDF).",               "À Faire",  "Moyenne", "tarek.bouzid@telnet.tn",       0,  7, 21),
        ("Notifications Push",              "Système de notifications push (alertes de transaction, promotions).",            "À Faire",  "Basse",   "rania.sfar@telnet.tn",         0,  14, 10),
        ("Audit sécurité applicative",      "Pentesting et validation OWASP Mobile Top 10.",                                 "À Faire",  "Haute",   None,                           0,  35, 7),
    ],
    2: [  # Migration Cloud Infrastructure
        ("Inventaire des serveurs",        "Cartographie de l'infra existante : VMs, stockage, réseau.",            "À Faire", "Haute",   "tarek.bouzid@telnet.tn",     0, 10, 5),
        ("PoC migration AWS",             "Proof of concept : migration d'un serveur de test vers EC2.",            "À Faire", "Haute",   "mohamed.jaziri@telnet.tn",   0, 15, 10),
        ("Plan de migration détaillé",    "Planning détaillé avec phases, risques et rollback.",                    "À Faire", "Moyenne", "khalil.bouazizi@telnet.tn",   0, 20, 7),
        ("Migration base de données",     "Migration PostgreSQL vers RDS avec replica et tests de performance.",    "À Faire", "Haute",   "tarek.bouzid@telnet.tn",     0, 30, 14),
        ("Configuration CI/CD AWS",       "Pipeline CodePipeline + CodeDeploy + monitoring CloudWatch.",            "À Faire", "Moyenne", None,                         0, 40, 10),
    ],
    3: [  # Système de Gestion RH (Terminé)
        ("Analyse des processus RH",       "Étude des processus existants et identification des besoins.",          "Terminé", "Haute",   "rania.sfar@telnet.tn",      100, -88, 7),
        ("Développement module congés",    "CRUD congés, workflow de validation, calendrier.",                     "Terminé", "Haute",   "khalil.bouazizi@telnet.tn", 100, -80, 15),
        ("Module fiches employés",         "Gestion des profils, contrats et documents administratifs.",            "Terminé", "Moyenne", "ines.chaabane@telnet.tn",   100, -65, 14),
        ("Module évaluations",             "Système d'évaluation annuelle avec grilles et objectifs.",              "Terminé", "Moyenne", "mohamed.jaziri@telnet.tn",  100, -50, 14),
        ("Tests et recette",               "Tests fonctionnels et validation avec les RH.",                        "Terminé", "Haute",   "tarek.bouzid@telnet.tn",    100, -35, 10),
        ("Mise en production",             "Déploiement final et migration des données employés.",                  "Terminé", "Haute",   "tarek.bouzid@telnet.tn",    100, -25, 5),
    ],
    4: [  # Audit Sécurité SI (Annulé)
        ("Cadrage de l'audit",             "Définition du périmètre et des objectifs de l'audit.",                 "Annulé", "Haute",   "mohamed.jaziri@telnet.tn",   0, -20, 3),
        ("Scan de vulnérabilités",         "Scan automatisé avec Nessus et OpenVAS.",                              "Annulé", "Haute",   "tarek.bouzid@telnet.tn",     0, -17, 7),
    ],
    5: [  # Template Projet Standard (Blueprint)
        ("Phase 1 : Cadrage",             "Analyse des besoins, faisabilité et planification.",                    "À Faire", "Haute",   None, 0, 0, 10),
        ("Phase 2 : Conception",          "Architecture technique et design fonctionnel.",                          "À Faire", "Haute",   None, 0, 10, 15),
        ("Phase 3 : Développement",       "Développement itératif avec sprints de 2 semaines.",                    "À Faire", "Moyenne", None, 0, 25, 30),
        ("Phase 4 : Tests",              "Tests unitaires, intégration, performance et sécurité.",                  "À Faire", "Haute",   None, 0, 55, 10),
        ("Phase 5 : Déploiement",        "Mise en production et formation des utilisateurs.",                      "À Faire", "Moyenne", None, 0, 65, 7),
    ],
}

COMMENTS = [
    # (project_idx, task_name, user_email, texte)
    (0, "Analyse des besoins client",         "khalil.bouazizi@telnet.tn", "Document BRD finalisé et validé par le client. Toutes les exigences sont couvertes."),
    (0, "Analyse des besoins client",         "amira.trabelsi@telnet.tn",  "Excellent travail Khalil ! Approuvé pour passer à la phase design."),
    (0, "Maquettes UI/UX",                    "ines.chaabane@telnet.tn",   "Les maquettes desktop sont finalisées. Les maquettes mobile sont en cours de validation."),
    (0, "Maquettes UI/UX",                    "contact@poulina.tn",        "Les maquettes correspondent bien à notre charte graphique. Validé."),
    (0, "Développement API Backend",          "khalil.bouazizi@telnet.tn", "API catalogue et panier terminées. En cours sur le module commandes."),
    (0, "Intégration passerelle de paiement", "mohamed.jaziri@telnet.tn",  "Environnement sandbox Flouci configuré. Tests de transaction en cours."),
    (1, "Cahier des charges fonctionnel",     "rania.sfar@telnet.tn",      "CDC livré et approuvé par le comité de pilotage BH Bank."),
    (1, "Design System Mobile",               "ines.chaabane@telnet.tn",   "Composants de base exportés. En attente de la review Chef de Projet."),
    (1, "Backend API bancaire",               "khalil.bouazizi@telnet.tn", "Module authentification JWT terminé. Module consultation solde à 80%."),
    (3, "Tests et recette",                    "tarek.bouzid@telnet.tn",    "Tous les tests fonctionnels passent. 0 bugs critiques restants."),
    (3, "Mise en production",                  "tarek.bouzid@telnet.tn",    "Déploiement réussi. 450 fiches employés migrées avec succès."),
    (3, "Mise en production",                  "youssef.hammami@telnet.tn", "📝 Modifications automatiques :\n• Statut changé : « En Cours » → « Terminé »"),
]


def seed():
    """Insère toutes les données de test dans la base de données."""
    db = DbConnection(**db_config)
    conn = db.connect()
    if not conn:
        print("❌ Impossible de se connecter à la base de données. Vérifiez PostgreSQL.")
        return

    print("🌱 Insertion des données de test...")

    # ---- Vérifier que les rôles existent ----
    roles = db.fetch_data("SELECT id_role, nom_role FROM Roles ORDER BY id_role;")
    if not roles or len(roles) < 5:
        print("❌ Les rôles ne sont pas configurés. Exécutez d'abord les migrations.")
        db.close()
        return
    print(f"  ✅ {len(roles)} rôles trouvés")

    # ---- Insérer les utilisateurs ----
    user_ids = {}  # email -> id
    inserted_users = 0
    for name, email, role_id, peut_rev, actif in USERS:
        try:
            # Vérifier si l'utilisateur existe déjà
            existing = db.fetch_single_data(
                "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s;", (email,)
            )
            if existing:
                user_ids[email] = existing[0]
                print(f"  ⏭  Utilisateur existant : {name} ({email})")
                continue
                
            db.execute_query(
                "INSERT INTO Utilisateurs (nom_utilisateur, email, mot_de_passe, id_role, peut_reviser, actif) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (name, email, PASSWORD, role_id, peut_rev, actif)
            )
            uid = db.fetch_single_data(
                "SELECT id_utilisateur FROM Utilisateurs WHERE email = %s;", (email,)
            )
            user_ids[email] = uid[0]
            inserted_users += 1
            status = "🔴 INACTIF" if not actif else ""
            print(f"  ✅ Utilisateur : {name} ({email}) — Rôle {role_id} {status}")
        except Exception as e:
            print(f"  ❌ Erreur utilisateur {name}: {e}")

    # Récupérer les IDs de tous les utilisateurs (y compris ceux qui existaient déjà)
    all_users = db.fetch_data("SELECT id_utilisateur, email FROM Utilisateurs;")
    for uid, uemail in all_users:
        user_ids[uemail] = uid

    print(f"  📊 {inserted_users} nouveaux utilisateurs insérés, {len(user_ids)} total")

    # ---- Insérer les projets ----
    project_ids = {}  # index -> id
    today = date.today()
    inserted_projects = 0
    
    for idx, (nom, desc, statut, chef_email, client_email, est_modele, jours_debut, jours_duree) in enumerate(PROJECTS):
        try:
            # Vérifier si le projet existe déjà
            existing = db.fetch_single_data(
                "SELECT id_projet FROM Projets WHERE nom_projet = %s;", (nom,)
            )
            if existing:
                project_ids[idx] = existing[0]
                print(f"  ⏭  Projet existant : {nom}")
                continue

            chef_id = user_ids.get(chef_email)
            client_id = user_ids.get(client_email) if client_email else None
            d_debut = today + timedelta(days=jours_debut)
            d_fin = d_debut + timedelta(days=jours_duree)
            
            db.execute_query(
                "INSERT INTO Projets (nom_projet, description, date_debut, date_fin_prevue, statut, "
                "chef_projet_id, client_id, est_modele) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (nom, desc, d_debut, d_fin, statut, chef_id, client_id, est_modele)
            )
            pid = db.fetch_single_data(
                "SELECT id_projet FROM Projets WHERE nom_projet = %s;", (nom,)
            )
            project_ids[idx] = pid[0]
            inserted_projects += 1
            print(f"  ✅ Projet : {nom} ({statut})")
        except Exception as e:
            print(f"  ❌ Erreur projet {nom}: {e}")

    print(f"  📊 {inserted_projects} nouveaux projets insérés")

    # ---- Insérer les tâches ----
    task_ids = {}  # (project_idx, task_name) -> id
    inserted_tasks = 0
    
    for proj_idx, tasks in TASKS.items():
        pid = project_ids.get(proj_idx)
        if not pid:
            continue
            
        proj_debut_offset = PROJECTS[proj_idx][6]  # jours_debut du projet
        
        for (t_nom, t_desc, t_statut, t_prio, t_user_email, t_prog, t_offset_start, t_duration) in tasks:
            try:
                # Vérifier si la tâche existe déjà
                existing = db.fetch_single_data(
                    "SELECT id_tache FROM Taches WHERE nom_tache = %s AND id_projet = %s;",
                    (t_nom, pid)
                )
                if existing:
                    task_ids[(proj_idx, t_nom)] = existing[0]
                    continue

                t_user_id = user_ids.get(t_user_email) if t_user_email else None
                t_debut = today + timedelta(days=t_offset_start)
                t_fin = t_debut + timedelta(days=t_duration)
                
                db.execute_query(
                    "INSERT INTO Taches (nom_tache, description, date_debut, date_fin_prevue, "
                    "statut, priorite, id_projet, assigne_a_id, progression) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                    (t_nom, t_desc, t_debut, t_fin, t_statut, t_prio, pid, t_user_id, t_prog)
                )
                tid = db.fetch_single_data(
                    "SELECT id_tache FROM Taches WHERE nom_tache = %s AND id_projet = %s;",
                    (t_nom, pid)
                )
                task_ids[(proj_idx, t_nom)] = tid[0]
                inserted_tasks += 1
            except Exception as e:
                print(f"  ❌ Erreur tâche {t_nom}: {e}")

    print(f"  ✅ {inserted_tasks} tâches insérées")

    # ---- Insérer les commentaires ----
    inserted_comments = 0
    for proj_idx, task_name, user_email, texte in COMMENTS:
        try:
            tid = task_ids.get((proj_idx, task_name))
            uid = user_ids.get(user_email)
            if not tid or not uid:
                continue
                
            db.execute_query(
                "INSERT INTO Commentaires_Tache (id_tache, id_utilisateur, texte_commentaire) "
                "VALUES (%s, %s, %s);",
                (tid, uid, texte)
            )
            inserted_comments += 1
        except Exception as e:
            print(f"  ❌ Erreur commentaire: {e}")

    print(f"  ✅ {inserted_comments} commentaires insérés")

    # ---- Ajouter des dépendances de tâches ----
    deps_added = 0
    # Projet 0 : certaines tâches dépendent les unes des autres
    dependency_pairs = [
        (0, "Maquettes UI/UX",                    0, "Analyse des besoins client"),
        (0, "Architecture technique",              0, "Analyse des besoins client"),
        (0, "Développement API Backend",           0, "Architecture technique"),
        (0, "Développement Frontend React",        0, "Maquettes UI/UX"),
        (0, "Intégration passerelle de paiement",  0, "Développement API Backend"),
        (0, "Tests d'intégration",                 0, "Développement API Backend"),
        (0, "Déploiement staging",                 0, "Tests d'intégration"),
        (1, "Design System Mobile",                1, "Cahier des charges fonctionnel"),
        (1, "Backend API bancaire",                1, "Cahier des charges fonctionnel"),
        (1, "Module biométrique",                  1, "Backend API bancaire"),
    ]
    
    for proj_a, task_a, proj_b, task_b in dependency_pairs:
        try:
            tid_a = task_ids.get((proj_a, task_a))
            tid_b = task_ids.get((proj_b, task_b))
            if tid_a and tid_b:
                db.execute_query(
                    "UPDATE Taches SET depende_de_id = %s WHERE id_tache = %s AND depende_de_id IS NULL;",
                    (tid_b, tid_a)
                )
                deps_added += 1
        except Exception as e:
            pass

    print(f"  ✅ {deps_added} dépendances de tâches configurées")

    db.close()
    
    print("\n" + "=" * 60)
    print("🎉 Données de test insérées avec succès !")
    print("=" * 60)
    print()
    print("📋 Comptes de test créés (mot de passe : test123) :")
    print("-" * 60)
    print(f"  {'Nom':<25} {'Email':<35} {'Rôle'}")
    print("-" * 60)
    role_names = {1: "Administrateur", 2: "Chef de Projet", 3: "Membre Équipe", 4: "Client", 5: "Direction"}
    for name, email, role_id, _, actif in USERS:
        status = " [INACTIF]" if not actif else ""
        print(f"  {name:<25} {email:<35} {role_names[role_id]}{status}")
    print("-" * 60)
    print()


if __name__ == "__main__":
    seed()
