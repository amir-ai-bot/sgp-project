"""
db_connection.py
----------------
Module de connexion à la base de données PostgreSQL via psycopg2.
Toutes les requêtes sont paramétrées pour prévenir les injections SQL.
Le logging enregistre les connexions, erreurs et actions critiques.
"""

import psycopg2
from psycopg2 import Error
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from logger_config import app_logger


class DbConnection:
    """
    Classe gérant la connexion et les opérations sur la base de données PostgreSQL.
    Toutes les requêtes SQL sont paramétrées (protection contre les injections SQL).
    """

    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432'):
        """
        Initialise les paramètres de connexion.

        Args:
            dbname: Nom de la base de données.
            user: Nom d'utilisateur PostgreSQL.
            password: Mot de passe PostgreSQL.
            host: Hôte du serveur (défaut: localhost).
            port: Port du serveur (défaut: 5432).
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """
        Établit la connexion à la base de données.

        Returns:
            psycopg2.connection | None: La connexion si réussie, None sinon.
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            app_logger.info(f"Connexion DB établie — base: {self.dbname}@{self.host}:{self.port}")
            return self.connection
        except Error as e:
            app_logger.error(f"Échec de connexion PostgreSQL — {e}")
            return None

    def close(self):
        """Ferme proprement la connexion à la base de données."""
        if self.connection:
            try:
                self.connection.close()
                app_logger.debug("Connexion DB fermée.")
            except Exception as e:
                app_logger.warning(f"Erreur lors de la fermeture de la connexion: {e}")
            finally:
                self.connection = None

    def execute_query(self, query: str, params=None, fetch_one: bool = False, fetch_all: bool = False):
        """
        Exécute une requête SQL paramétrée.

        Args:
            query: Requête SQL avec placeholders %s.
            params: Paramètres de la requête (tuple ou None).
            fetch_one: Si True, retourne une seule ligne.
            fetch_all: Si True, retourne toutes les lignes.

        Returns:
            bool | tuple | list | None: Résultat selon les flags de fetch.

        Raises:
            Exception: Relancée après rollback si une erreur se produit.
        """
        if not self.connection:
            app_logger.error("Tentative d'exécution de requête sans connexion active.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()
            return True
        except Error as e:
            app_logger.error(f"Erreur SQL: {e} | Requête: {query[:80]}...")
            self.connection.rollback()
            raise  # Relancer pour que les vues puissent afficher l'erreur correcte

    def fetch_data(self, query: str, params=None):
        """Raccourci pour fetch_all."""
        return self.execute_query(query, params, fetch_all=True)

    def fetch_single_data(self, query: str, params=None):
        """Raccourci pour fetch_one."""
        return self.execute_query(query, params, fetch_one=True)


# Bloc de test (usage standalone)
if __name__ == '__main__':
    # NOTE: Use environment variables or a secure config file for production.
    # The credentials below are placeholders for development/demonstration.
    db_config = {
        'dbname': os.getenv('DB_NAME', 'your_db_name'),
        'user': os.getenv('DB_USER', 'your_db_user'),
        'password': os.getenv('DB_PASSWORD', 'your_db_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

    db = DbConnection(**db_config)
    if db.connect():
        roles = db.fetch_data("SELECT * FROM Roles;")
        if roles:
            print("Rôles:", roles)
        db.close()
