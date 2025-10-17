"""
Gestor de base de datos SQLite
"""
import sqlite3
import logging
from pathlib import Path
from typing import List, Tuple, Any, Optional
from config.config import DATABASE_PATH

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Clase para gestionar la conexión y operaciones con SQLite"""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Para acceder por nombre de columna
            self.cursor = self.connection.cursor()
            logger.info(f"Conexión establecida con {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Error al conectar con la base de datos: {e}")
            raise
    
    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            logger.info("Conexión cerrada")
    
    def execute_query(self, query: str, params: Tuple = ()) -> Optional[List[sqlite3.Row]]:
        """
        Ejecuta una consulta SQL
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta
            
        Returns:
            Resultados de la consulta
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            raise
    
    def execute_many(self, query: str, data: List[Tuple]):
        """
        Ejecuta múltiples inserciones
        
        Args:
            query: Consulta SQL con placeholders
            data: Lista de tuplas con los datos a insertar
        """
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()
            logger.info(f"Insertadas {len(data)} filas")
        except sqlite3.Error as e:
            logger.error(f"Error al ejecutar múltiples inserciones: {e}")
            self.connection.rollback()
            raise
    
    def commit(self):
        """Confirma los cambios en la base de datos"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        """Revierte los cambios en la base de datos"""
        if self.connection:
            self.connection.rollback()
    
    def init_schema(self, schema_file: Path):
        """
        Inicializa el schema de la base de datos
        
        Args:
            schema_file: Ruta al archivo SQL con el schema
        """
        try:
            with open(schema_file, 'r') as f:
                schema = f.read()
            self.cursor.executescript(schema)
            self.connection.commit()
            logger.info("Schema inicializado correctamente")
        except (sqlite3.Error, IOError) as e:
            logger.error(f"Error al inicializar schema: {e}")
            raise
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()
