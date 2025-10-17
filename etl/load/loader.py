"""
Cargador de datos a SQLite
"""
import pandas as pd
import logging
from database.db_manager import DatabaseManager
from config.config import DATABASE_PATH

logger = logging.getLogger(__name__)


class DataLoader:
    """Clase para cargar datos a la base de datos SQLite"""
    
    def __init__(self):
        self.db_manager = DatabaseManager(DATABASE_PATH)
    
    def load_dataframe(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> bool:
        """
        Carga un DataFrame a una tabla SQLite
        
        Args:
            df: DataFrame a cargar
            table_name: Nombre de la tabla destino
            if_exists: Acción si la tabla existe ('fail', 'replace', 'append')
            
        Returns:
            True si la carga fue exitosa
        """
        try:
            with self.db_manager:
                df.to_sql(
                    table_name,
                    self.db_manager.connection,
                    if_exists=if_exists,
                    index=False
                )
            logger.info(f"Cargadas {len(df)} filas en la tabla '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            return False
    
    def load_batch(self, data: list, table_name: str, columns: list) -> bool:
        """
        Carga datos en lotes a la base de datos
        
        Args:
            data: Lista de tuplas con los datos
            table_name: Nombre de la tabla
            columns: Lista con nombres de columnas
            
        Returns:
            True si la carga fue exitosa
        """
        try:
            placeholders = ','.join(['?' for _ in columns])
            columns_str = ','.join(columns)
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            with self.db_manager:
                self.db_manager.execute_many(query, data)
            
            logger.info(f"Cargadas {len(data)} filas en la tabla '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Error al cargar batch: {e}")
            return False
