"""
Script ETL específico para análisis de animales con microchip en Bogotá
"""
import pandas as pd
import numpy as np
import sqlite3
import folium
from folium import plugins
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_data(file_path):
    """Extrae datos del archivo CSV"""
    logger.info(f"Extrayendo datos de {file_path}")
    df = pd.read_csv(file_path, sep=';', encoding='latin-1')
    logger.info(f"✅ {len(df)} registros extraídos")
    return df


def transform_data(df):
    """Transforma y limpia los datos"""
    logger.info("Transformando datos...")
    
    # Eliminar duplicados
    df = df.drop_duplicates(subset='microchip_animal')
    
    # Limpiar y normalizar texto
    df['localidad_territorializacion'] = df['localidad_territorializacion'].str.strip().str.upper()
    df['especie'] = df['especie'].str.strip().str.upper()
    df['sexo_animal'] = df['sexo_animal'].str.strip().str.upper()
    df['tamano_animal'] = df['tamano_animal'].str.strip().str.upper()
    df['potencialmente_peligroso'] = df['potencialmente_peligroso'].str.strip().str.upper()
    
    logger.info("✅ Datos transformados")
    return df


def create_locality_stats(df):
    """Crea estadísticas por localidad"""
    logger.info("Generando estadísticas por localidad...")
    
    # Coordenadas de las localidades de Bogotá
    coordenadas_localidades = {
        'USAQUEN': {'lat': 4.6944, 'lon': -74.0306},
        'CHAPINERO': {'lat': 4.6308, 'lon': -74.0658},
        'SANTA FE': {'lat': 4.6053, 'lon': -74.0755},
        'SAN CRISTOBAL': {'lat': 4.5653, 'lon': -74.0825},
        'USME': {'lat': 4.4825, 'lon': -74.1284},
        'TUNJUELITO': {'lat': 4.5748, 'lon': -74.1329},
        'BOSA': {'lat': 4.6186, 'lon': -74.1878},
        'KENNEDY': {'lat': 4.6281, 'lon': -74.1550},
        'FONTIBON': {'lat': 4.6728, 'lon': -74.1444},
        'ENGATIVA': {'lat': 4.7011, 'lon': -74.1122},
        'SUBA': {'lat': 4.7565, 'lon': -74.0826},
        'BARRIOS UNIDOS': {'lat': 4.6639, 'lon': -74.0819},
        'TEUSAQUILLO': {'lat': 4.6417, 'lon': -74.0875},
        'LOS MARTIRES': {'lat': 4.6117, 'lon': -74.0939},
        'ANTONIO NARINO': {'lat': 4.5850, 'lon': -74.1111},
        'PUENTE ARANDA': {'lat': 4.6144, 'lon': -74.1194},
        'LA CANDELARIA': {'lat': 4.5964, 'lon': -74.0739},
        'RAFAEL URIBE URIBE': {'lat': 4.5528, 'lon': -74.1153},
        'CIUDAD BOLIVAR': {'lat': 4.5753, 'lon': -74.1772},
        'SUMAPAZ': {'lat': 4.2417, 'lon': -74.2481}
    }
    
    # Agregar por localidad
    df_agregado = df.groupby('localidad_territorializacion').agg({
        'microchip_animal': 'count',
        'especie': lambda x: x.value_counts().index[0],
    }).reset_index()
    
    df_agregado.columns = ['localidad', 'total_animales', 'especie_predominante']
    
    # Estadísticas adicionales
    caninos = df[df['especie'] == 'CANINO'].groupby('localidad_territorializacion').size()
    felinos = df[df['especie'] == 'FELINO'].groupby('localidad_territorializacion').size()
    peligrosos = df[df['potencialmente_peligroso'] == 'SI'].groupby('localidad_territorializacion').size()
    
    df_agregado['total_caninos'] = df_agregado['localidad'].map(caninos).fillna(0).astype(int)
    df_agregado['total_felinos'] = df_agregado['localidad'].map(felinos).fillna(0).astype(int)
    df_agregado['total_peligrosos'] = df_agregado['localidad'].map(peligrosos).fillna(0).astype(int)
    
    # Agregar coordenadas
    df_agregado['latitud'] = df_agregado['localidad'].map(lambda x: coordenadas_localidades.get(x, {}).get('lat'))
    df_agregado['longitud'] = df_agregado['localidad'].map(lambda x: coordenadas_localidades.get(x, {}).get('lon'))
    
    # Eliminar localidades sin coordenadas
    df_agregado = df_agregado.dropna(subset=['latitud', 'longitud'])
    
    logger.info(f"✅ {len(df_agregado)} localidades procesadas")
    return df_agregado


def load_to_database(df, df_stats, db_path):
    """Carga datos a la base de datos SQLite"""
    logger.info(f"Cargando datos a {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    # Crear tablas
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS animales_microchip (
        microchip TEXT PRIMARY KEY,
        especie TEXT,
        sexo TEXT,
        tamano TEXT,
        potencialmente_peligroso TEXT,
        localidad TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estadisticas_localidad (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        localidad TEXT UNIQUE,
        latitud REAL,
        longitud REAL,
        total_animales INTEGER,
        total_caninos INTEGER,
        total_felinos INTEGER,
        total_peligrosos INTEGER,
        especie_predominante TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Cargar datos
    df_db = df[['microchip_animal', 'especie', 'sexo_animal', 'tamano_animal', 
                'potencialmente_peligroso', 'localidad_territorializacion']].copy()
    df_db.columns = ['microchip', 'especie', 'sexo', 'tamano', 'potencialmente_peligroso', 'localidad']
    
    df_db.to_sql('animales_microchip', conn, if_exists='replace', index=False)
    df_stats.to_sql('estadisticas_localidad', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ {len(df_db)} animales y {len(df_stats)} localidades cargadas")


def create_interactive_map(df_stats, output_path):
    """Crea mapa interactivo con Folium"""
    logger.info("Creando mapa interactivo...")
    
    bogota_coords = [4.6097, -74.0817]
    mapa = folium.Map(location=bogota_coords, zoom_start=11, tiles='OpenStreetMap')
    
    # Agregar capas
    folium.TileLayer('CartoDB positron', name='CartoDB Positron').add_to(mapa)
    
    # Normalizar valores
    min_animals = df_stats['total_animales'].min()
    max_animals = df_stats['total_animales'].max()
    
    # Agregar marcadores
    for idx, row in df_stats.iterrows():
        size = 10 + (row['total_animales'] - min_animals) / (max_animals - min_animals) * 30
        
        if row['total_animales'] > 2000:
            color = 'red'
        elif row['total_animales'] > 1000:
            color = 'orange'
        elif row['total_animales'] > 500:
            color = 'blue'
        else:
            color = 'green'
        
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="color: #2C3E50; margin-bottom: 10px;">{row['localidad']}</h4>
            <hr style="margin: 5px 0;">
            <b>📊 Total Animales:</b> {row['total_animales']:,}<br>
            <b>🐕 Caninos:</b> {row['total_caninos']:,}<br>
            <b>🐱 Felinos:</b> {row['total_felinos']:,}<br>
            <b>⚠️ Peligrosos:</b> {row['total_peligrosos']:,}<br>
            <b>🏆 Predominante:</b> {row['especie_predominante']}<br>
        </div>
        """
        
        folium.CircleMarker(
            location=[row['latitud'], row['longitud']],
            radius=size,
            popup=folium.Popup(popup_html, max_width=300),
            color=color,
            fillColor=color,
            fillOpacity=0.6,
            weight=2
        ).add_to(mapa)
        
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            icon=folium.DivIcon(html=f"""
                <div style="font-size: 9px; color: black; font-weight: bold; 
                text-shadow: 1px 1px 2px white; white-space: nowrap;">
                {row['localidad']}</div>
            """)
        ).add_to(mapa)
    
    # Leyenda
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 220px; 
    background-color: white; border: 2px solid grey; z-index: 9999; 
    font-size: 14px; padding: 10px; border-radius: 5px;">
        <h4 style="margin: 0 0 10px 0;">🗺️ Leyenda</h4>
        <p style="margin: 5px 0;"><span style="color: red;">●</span> &gt; 2000 animales</p>
        <p style="margin: 5px 0;"><span style="color: orange;">●</span> 1000 - 2000 animales</p>
        <p style="margin: 5px 0;"><span style="color: blue;">●</span> 500 - 1000 animales</p>
        <p style="margin: 5px 0;"><span style="color: green;">●</span> &lt; 500 animales</p>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl().add_to(mapa)
    plugins.Fullscreen().add_to(mapa)
    
    mapa.save(output_path)
    logger.info(f"✅ Mapa guardado en {output_path}")


def create_heatmap(df_stats, output_path):
    """Crea mapa de calor"""
    logger.info("Creando mapa de calor...")
    
    bogota_coords = [4.6097, -74.0817]
    mapa_calor = folium.Map(location=bogota_coords, zoom_start=11, tiles='CartoDB positron')
    
    heat_data = [[row['latitud'], row['longitud'], row['total_animales']/100] 
                 for idx, row in df_stats.iterrows()]
    
    plugins.HeatMap(
        heat_data,
        min_opacity=0.4,
        radius=25,
        blur=30,
        gradient={0.0: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}
    ).add_to(mapa_calor)
    
    title_html = '''
    <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
    width: 600px; background-color: white; border: 2px solid grey; z-index: 9999; 
    font-size: 16px; padding: 10px; border-radius: 5px; text-align: center;">
        <h3 style="margin: 0;">🔥 Densidad de Animales con Microchip por Localidad</h3>
    </div>
    '''
    mapa_calor.get_root().html.add_child(folium.Element(title_html))
    
    mapa_calor.save(output_path)
    logger.info(f"✅ Mapa de calor guardado en {output_path}")


def main():
    """Función principal del ETL"""
    logger.info("🚀 Iniciando proceso ETL")
    
    # Rutas
    base_dir = Path(__file__).parent
    input_file = base_dir / 'data' / 'raw' / 'c4p-animales-identificados-con-microship-por-localidad.csv'
    db_path = base_dir / 'database' / 'geo_bog.db'
    map_output = base_dir / 'web' / 'static' / 'mapa_animales_bogota.html'
    heatmap_output = base_dir / 'web' / 'static' / 'mapa_calor_animales_bogota.html'
    processed_output = base_dir / 'data' / 'processed' / 'animales_microchip_procesado.csv'
    stats_output = base_dir / 'data' / 'processed' / 'estadisticas_por_localidad.csv'
    
    # ETL
    df = extract_data(input_file)
    df = transform_data(df)
    df_stats = create_locality_stats(df)
    load_to_database(df, df_stats, db_path)
    
    # Mapas
    create_interactive_map(df_stats, map_output)
    create_heatmap(df_stats, heatmap_output)
    
    # Exportar procesados
    df.to_csv(processed_output, index=False, encoding='utf-8')
    df_stats.to_csv(stats_output, index=False, encoding='utf-8')
    
    # Resumen
    logger.info("\n" + "="*70)
    logger.info("✅ ETL COMPLETADO EXITOSAMENTE")
    logger.info("="*70)
    logger.info(f"\n📊 Resumen:")
    logger.info(f"   • Total de animales: {len(df):,}")
    logger.info(f"   • Localidades procesadas: {len(df_stats)}")
    logger.info(f"   • Caninos: {len(df[df['especie']=='CANINO']):,}")
    logger.info(f"   • Felinos: {len(df[df['especie']=='FELINO']):,}")
    logger.info(f"   • Animales peligrosos: {len(df[df['potencialmente_peligroso']=='SI']):,}")
    logger.info("\n📁 Archivos generados:")
    logger.info(f"   ✓ {db_path}")
    logger.info(f"   ✓ {map_output}")
    logger.info(f"   ✓ {heatmap_output}")
    logger.info(f"   ✓ {processed_output}")
    logger.info(f"   ✓ {stats_output}")
    logger.info("="*70)


if __name__ == "__main__":
    main()
