"""
Aplicación web Flask para visualizar estadísticas
"""
from flask import Flask, render_template, jsonify
import logging
from pathlib import Path
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.config import WEB_HOST, WEB_PORT, DEBUG
from database.db_manager import DatabaseManager
from utils.logger import setup_logger

# Configurar logging
setup_logger()
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
db_manager = DatabaseManager()


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/mapa')
def mapa():
    """Página del mapa interactivo"""
    return render_template('mapa.html')


@app.route('/api/animales-microchip')
def get_animales_microchip():
    """Endpoint para obtener datos de animales con microchip"""
    try:
        with db_manager:
            query = "SELECT * FROM animales_microchip LIMIT 100"
            results = db_manager.execute_query(query)
            
            data = [dict(row) for row in results] if results else []
            
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error al obtener datos de animales: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/estadisticas-localidad')
def get_estadisticas_localidad():
    """Endpoint para obtener estadísticas por localidad"""
    try:
        with db_manager:
            query = "SELECT * FROM estadisticas_localidad ORDER BY total_animales DESC"
            results = db_manager.execute_query(query)
            
            data = [dict(row) for row in results] if results else []
            
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/geographic-data')
def get_geographic_data():
    """Endpoint para obtener datos geográficos"""
    try:
        with db_manager:
            query = "SELECT * FROM geographic_data LIMIT 100"
            results = db_manager.execute_query(query)
            
            data = [dict(row) for row in results] if results else []
            
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error al obtener datos geográficos: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics')
def get_statistics():
    """Endpoint para obtener estadísticas"""
    try:
        with db_manager:
            query = """
                SELECT 
                    metric_name,
                    AVG(metric_value) as avg_value,
                    MIN(metric_value) as min_value,
                    MAX(metric_value) as max_value,
                    COUNT(*) as count
                FROM statistics
                GROUP BY metric_name
            """
            results = db_manager.execute_query(query)
            
            data = [dict(row) for row in results] if results else []
            
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error al obtener estadísticas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics/category/<category>')
def get_statistics_by_category(category):
    """Endpoint para obtener estadísticas por categoría"""
    try:
        with db_manager:
            query = """
                SELECT * FROM statistics 
                WHERE category = ?
                ORDER BY metric_date DESC
                LIMIT 50
            """
            results = db_manager.execute_query(query, (category,))
            
            data = [dict(row) for row in results] if results else []
            
        return jsonify({
            'success': True,
            'data': data,
            'category': category,
            'count': len(data)
        })
    except Exception as e:
        logger.error(f"Error al obtener estadísticas por categoría: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health_check():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'service': 'geo_bog_web'
    })


if __name__ == '__main__':
    logger.info(f"Iniciando servidor web en {WEB_HOST}:{WEB_PORT}")
    app.run(host=WEB_HOST, port=WEB_PORT, debug=DEBUG)
