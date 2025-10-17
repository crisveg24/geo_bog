"""
Transformador de datos
"""
import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataTransformer:
    """Clase para transformar y limpiar datos"""
    
    @staticmethod
    def clean_nulls(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """
        Limpia valores nulos del DataFrame
        
        Args:
            df: DataFrame a limpiar
            strategy: Estrategia ('drop', 'fill_mean', 'fill_median', 'fill_zero')
            
        Returns:
            DataFrame limpio
        """
        try:
            if strategy == 'drop':
                cleaned_df = df.dropna()
            elif strategy == 'fill_mean':
                cleaned_df = df.fillna(df.mean())
            elif strategy == 'fill_median':
                cleaned_df = df.fillna(df.median())
            elif strategy == 'fill_zero':
                cleaned_df = df.fillna(0)
            else:
                logger.warning(f"Estrategia '{strategy}' no reconocida, usando 'drop'")
                cleaned_df = df.dropna()
            
            logger.info(f"Limpieza completada: {len(df)} -> {len(cleaned_df)} filas")
            return cleaned_df
        except Exception as e:
            logger.error(f"Error al limpiar datos: {e}")
            raise
    
    @staticmethod
    def rename_columns(df: pd.DataFrame, column_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Renombra columnas del DataFrame
        
        Args:
            df: DataFrame a transformar
            column_mapping: Diccionario con el mapeo de nombres
            
        Returns:
            DataFrame con columnas renombradas
        """
        try:
            df_renamed = df.rename(columns=column_mapping)
            logger.info(f"Columnas renombradas: {list(column_mapping.keys())}")
            return df_renamed
        except Exception as e:
            logger.error(f"Error al renombrar columnas: {e}")
            raise
    
    @staticmethod
    def filter_data(df: pd.DataFrame, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        Filtra datos según condiciones
        
        Args:
            df: DataFrame a filtrar
            conditions: Diccionario con las condiciones (columna: valor)
            
        Returns:
            DataFrame filtrado
        """
        try:
            filtered_df = df.copy()
            for column, value in conditions.items():
                if column in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[column] == value]
            
            logger.info(f"Filtrado completado: {len(df)} -> {len(filtered_df)} filas")
            return filtered_df
        except Exception as e:
            logger.error(f"Error al filtrar datos: {e}")
            raise
    
    @staticmethod
    def convert_types(df: pd.DataFrame, type_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Convierte tipos de datos de columnas
        
        Args:
            df: DataFrame a transformar
            type_mapping: Diccionario con el mapeo de tipos (columna: tipo)
            
        Returns:
            DataFrame con tipos convertidos
        """
        try:
            df_converted = df.copy()
            for column, dtype in type_mapping.items():
                if column in df_converted.columns:
                    df_converted[column] = df_converted[column].astype(dtype)
            
            logger.info(f"Tipos convertidos: {list(type_mapping.keys())}")
            return df_converted
        except Exception as e:
            logger.error(f"Error al convertir tipos: {e}")
            raise
