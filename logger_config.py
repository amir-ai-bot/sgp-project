"""
logger_config.py
----------------
Configuration centralisée du système de journalisation (logging) pour l'application SGP.
Utilise une rotation de fichiers pour éviter que le fichier de log ne devienne trop volumineux.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "SGP", log_file: str = "sgp_app.log", level=logging.INFO) -> logging.Logger:
    """
    Configure et retourne un logger nommé avec sortie console et fichier rotatif.

    Args:
        name: Nom du logger (par défaut "SGP").
        log_file: Chemin du fichier de log (par défaut "sgp_app.log" dans le répertoire du script).
        level: Niveau de logging (INFO par défaut).

    Returns:
        logging.Logger: Instance du logger configuré.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # Éviter d'ajouter des handlers en double si le logger est déjà configuré
        return logger

    logger.setLevel(level)

    # Formatter commun
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # Handler fichier avec rotation (5 fichiers de 2 Mo max)
    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(log_dir, log_file)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=2 * 1024 * 1024,  # 2 Mo
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Logger global de l'application
app_logger = setup_logger("SGP")
