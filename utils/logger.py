"""
Configuración del sistema de logging
"""
import logging
import sys
from pathlib import Path
from config.config import LOG_FILE, LOG_LEVEL


def setup_logger():
    """Configura el sistema de logging del proyecto"""
    
    # Crear el directorio de logs si no existe
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Formato del log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configuración básica
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado")
    
    return logger
