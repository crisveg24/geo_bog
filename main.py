"""
Script principal para ejecutar el proyecto
"""
import argparse
import logging
from pathlib import Path
import sys

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.config import DATABASE_PATH, DATABASE_DIR
from database.db_manager import DatabaseManager
from etl.pipeline import ETLPipeline
from utils.logger import setup_logger

# Configurar logging
setup_logger()
logger = logging.getLogger(__name__)


def init_database():
    """Inicializa la base de datos con el schema"""
    logger.info("Inicializando base de datos...")
    schema_file = DATABASE_DIR / "schema.sql"
    
    try:
        db_manager = DatabaseManager(DATABASE_PATH)
        with db_manager:
            db_manager.init_schema(schema_file)
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar base de datos: {e}")
        raise


def run_etl(source_file: str, table_name: str, file_type: str):
    """Ejecuta el pipeline ETL"""
    logger.info(f"Ejecutando ETL desde {source_file}")
    
    try:
        pipeline = ETLPipeline()
        pipeline.run_pipeline(Path(source_file), table_name, file_type)
    except Exception as e:
        logger.error(f"Error al ejecutar ETL: {e}")
        raise


def start_web_server():
    """Inicia el servidor web"""
    logger.info("Iniciando servidor web...")
    
    try:
        from web.app import app
        from config.config import WEB_HOST, WEB_PORT, DEBUG
        app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG)
    except Exception as e:
        logger.error(f"Error al iniciar servidor web: {e}")
        raise


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Geo Bog - Sistema ETL y Visualización')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando para inicializar DB
    subparsers.add_parser('init-db', help='Inicializar base de datos')
    
    # Comando para ejecutar ETL
    etl_parser = subparsers.add_parser('etl', help='Ejecutar pipeline ETL')
    etl_parser.add_argument('source', help='Archivo fuente de datos')
    etl_parser.add_argument('table', help='Tabla destino en la base de datos')
    etl_parser.add_argument('--type', default='csv', choices=['csv', 'excel', 'json'],
                          help='Tipo de archivo (default: csv)')
    
    # Comando para iniciar servidor web
    subparsers.add_parser('web', help='Iniciar servidor web')
    
    args = parser.parse_args()
    
    if args.command == 'init-db':
        init_database()
    elif args.command == 'etl':
        run_etl(args.source, args.table, args.type)
    elif args.command == 'web':
        start_web_server()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
