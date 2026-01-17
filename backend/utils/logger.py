import logging
import json
from typing import Dict, Any, Optional
import os

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logging strutturato per l'applicazione.

    Args:
        name: Nome del logger
        level: Livello di logging (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configurato
    """
    # Crea directory logs se non esiste
    log_dir = os.path.dirname(os.getenv('LOG_FILE', 'logs/app.log'))
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Configurazione base
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Handler per file
        file_handler = logging.FileHandler(os.getenv('LOG_FILE', 'logs/app.log'))
        file_handler.setLevel(getattr(logging, level))

        # Handler per console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))

        # Formattatore JSON per file
        file_formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)

        # Formattatore semplice per console
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(getattr(logging, level))

    return logger

# Logger globale
logger = setup_logger('agenti-ollama')