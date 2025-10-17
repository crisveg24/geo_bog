"""
Extractor de datos desde diferentes fuentes
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


class DataExtractor:
    """Clase para extraer datos desde diferentes fuentes"""
    
    @staticmethod
    def extract_from_csv(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Extrae datos desde un archivo CSV
        
        Args:
            file_path: Ruta al archivo CSV
            **kwargs: Argumentos adicionales para pd.read_csv
            
        Returns:
            DataFrame con los datos
        """
        try:
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Datos extraídos de {file_path}: {len(df)} filas")
            return df
        except Exception as e:
            logger.error(f"Error al extraer datos de CSV: {e}")
            raise
    
    @staticmethod
    def extract_from_excel(file_path: Union[str, Path], sheet_name: str = 0, **kwargs) -> pd.DataFrame:
        """
        Extrae datos desde un archivo Excel
        
        Args:
            file_path: Ruta al archivo Excel
            sheet_name: Nombre o índice de la hoja
            **kwargs: Argumentos adicionales para pd.read_excel
            
        Returns:
            DataFrame con los datos
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            logger.info(f"Datos extraídos de {file_path}: {len(df)} filas")
            return df
        except Exception as e:
            logger.error(f"Error al extraer datos de Excel: {e}")
            raise
    
    @staticmethod
    def extract_from_json(file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Extrae datos desde un archivo JSON
        
        Args:
            file_path: Ruta al archivo JSON
            **kwargs: Argumentos adicionales para pd.read_json
            
        Returns:
            DataFrame con los datos
        """
        try:
            df = pd.read_json(file_path, **kwargs)
            logger.info(f"Datos extraídos de {file_path}: {len(df)} filas")
            return df
        except Exception as e:
            logger.error(f"Error al extraer datos de JSON: {e}")
            raise
