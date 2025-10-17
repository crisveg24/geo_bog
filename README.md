# 🗺️ Geo Bog - Sistema ETL y Visualización

Sistema ETL (Extract, Transform, Load) con visualización web para datos geográficos y estadísticas usando SQLite.

## 📁 Estructura del Proyecto

```
geo_bog/
├── config/                 # Configuración del proyecto
│   └── config.py          # Variables de configuración
├── data/                  # Datos del proyecto
│   ├── raw/              # Datos crudos (CSV, Excel, JSON)
│   └── processed/        # Datos procesados
├── database/             # Base de datos SQLite
│   ├── schema.sql       # Schema de la base de datos
│   └── db_manager.py    # Gestor de conexiones
├── etl/                 # Pipeline ETL
│   ├── extract/        # Módulo de extracción
│   ├── transform/      # Módulo de transformación
│   ├── load/          # Módulo de carga
│   └── pipeline.py    # Pipeline principal
├── utils/              # Utilidades
│   └── logger.py      # Sistema de logging
├── web/                # Aplicación web
│   ├── static/        # Archivos estáticos (CSS, JS)
│   ├── templates/     # Templates HTML
│   └── app.py         # Aplicación Flask
├── logs/               # Logs del sistema
├── notebooks/          # Jupyter notebooks para análisis
├── main.py            # Script principal
├── requirements.txt   # Dependencias del proyecto
└── .env.example      # Ejemplo de variables de entorno
```

## 🚀 Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd geo_bog
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env según tus necesidades
```

5. **Inicializar la base de datos:**
```bash
python main.py init-db
```

## 📊 Uso

### 1. Ejecutar Pipeline ETL

Para procesar datos desde un archivo CSV:
```bash
python main.py etl data/raw/datos.csv geographic_data --type csv
```

Para archivos Excel:
```bash
python main.py etl data/raw/datos.xlsx geographic_data --type excel
```

Para archivos JSON:
```bash
python main.py etl data/raw/datos.json statistics --type json
```

### 2. Iniciar Servidor Web

```bash
python main.py web
```

El servidor estará disponible en: `http://localhost:5000`

### 3. Uso Programático

```python
from etl.pipeline import ETLPipeline
from pathlib import Path

# Crear instancia del pipeline
pipeline = ETLPipeline()

# Ejecutar ETL
pipeline.run_pipeline(
    source_file=Path("data/raw/datos.csv"),
    table_name="geographic_data",
    file_type="csv"
)
```

## 🔌 API Endpoints

- `GET /` - Página principal del dashboard
- `GET /api/geographic-data` - Obtener datos geográficos
- `GET /api/statistics` - Obtener estadísticas agregadas
- `GET /api/statistics/category/<category>` - Estadísticas por categoría
- `GET /health` - Estado del servicio

## 🗄️ Estructura de la Base de Datos

### Tabla: geographic_data
- `id` - INTEGER PRIMARY KEY
- `name` - VARCHAR(255)
- `latitude` - REAL
- `longitude` - REAL
- `category` - VARCHAR(100)
- `description` - TEXT
- `created_at` - TIMESTAMP
- `updated_at` - TIMESTAMP

### Tabla: statistics
- `id` - INTEGER PRIMARY KEY
- `metric_name` - VARCHAR(255)
- `metric_value` - REAL
- `metric_date` - DATE
- `category` - VARCHAR(100)
- `created_at` - TIMESTAMP

## 📝 Desarrollo

### Agregar nuevas transformaciones

Edita `etl/transform/transformer.py` y agrega tus funciones:

```python
@staticmethod
def mi_transformacion(df: pd.DataFrame) -> pd.DataFrame:
    # Tu lógica aquí
    return df_transformado
```

### Agregar nuevos endpoints

Edita `web/app.py`:

```python
@app.route('/api/mi-endpoint')
def mi_endpoint():
    # Tu lógica aquí
    return jsonify({'data': data})
```

## 📊 Notebooks de Análisis

Los notebooks Jupyter para análisis exploratorio se encuentran en la carpeta `notebooks/`.

Para iniciar Jupyter:
```bash
jupyter notebook
```

## 🔍 Logs

Los logs del sistema se guardan en `logs/etl.log`. Puedes configurar el nivel de logging en el archivo `.env`:

```
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Flask** - Framework web
- **Pandas** - Manipulación de datos
- **SQLite** - Base de datos
- **Plotly.js** - Visualizaciones interactivas
- **Matplotlib & Seaborn** - Gráficos estadísticos

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.