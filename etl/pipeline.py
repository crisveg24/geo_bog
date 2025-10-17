"""
Pipeline ETL principal
"""
import logging
from pathlib import Path
from etl.extract.extractor import DataExtractor
from etl.transform.transformer import DataTransformer
from etl.load.loader import DataLoader
from utils.logger import setup_logger

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Clase principal para ejecutar el pipeline ETL"""
    
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
    
    def run_pipeline(self, source_file: Path, table_name: str, file_type: str = 'csv'):
        """
        Ejecuta el pipeline ETL completo
        
        Args:
            source_file: Ruta al archivo fuente
            table_name: Nombre de la tabla destino
            file_type: Tipo de archivo ('csv', 'excel', 'json')
        """
        try:
            logger.info(f"Iniciando pipeline ETL para {source_file}")
            
            # EXTRACT
            logger.info("Fase 1: Extracción")
            if file_type == 'csv':
                df = self.extractor.extract_from_csv(source_file)
            elif file_type == 'excel':
                df = self.extractor.extract_from_excel(source_file)
            elif file_type == 'json':
                df = self.extractor.extract_from_json(source_file)
            else:
                raise ValueError(f"Tipo de archivo no soportado: {file_type}")
            
            # TRANSFORM
            logger.info("Fase 2: Transformación")
            df_clean = self.transformer.clean_nulls(df, strategy='drop')
            # Aquí puedes agregar más transformaciones según necesites
            
            # LOAD
            logger.info("Fase 3: Carga")
            success = self.loader.load_dataframe(df_clean, table_name, if_exists='append')
            
            if success:
                logger.info("Pipeline ETL completado exitosamente")
            else:
                logger.error("Pipeline ETL falló en la fase de carga")
                
        except Exception as e:
            logger.error(f"Error en el pipeline ETL: {e}")
            raise


if __name__ == "__main__":
    setup_logger()
    pipeline = ETLPipeline()
    # Ejemplo de uso:
    # pipeline.run_pipeline(Path("data/raw/datos.csv"), "geographic_data", "csv")
