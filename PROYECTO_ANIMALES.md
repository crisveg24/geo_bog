# 🐾 Análisis de Animales con Microchip en Bogotá

## Proyecto de Georreferenciación y Análisis de Datos Urbanos

**Tema:** Identificación y análisis espacial de animales registrados con microchip en las localidades de Bogotá D.C.

---

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema completo de ETL (Extract, Transform, Load) y visualización geográfica para analizar la distribución de animales identificados con microchip en las 20 localidades de Bogotá. El sistema permite:

- ✅ Procesar y limpiar datos de más de 20,000 registros
- ✅ Generar estadísticas por localidad
- ✅ Crear mapas interactivos con Folium
- ✅ Visualizar patrones de distribución con mapas de calor
- ✅ Almacenar datos en base de datos SQLite
- ✅ Servir visualizaciones a través de aplicación web Flask

---

## 🎯 Objetivos

### Objetivo General
Desarrollar una solución tecnológica que integre análisis de datos, georreferenciación y visualización web para identificar patrones en la distribución de animales con microchip en Bogotá.

### Objetivos Específicos
1. **Automatizar el procesamiento** de datos abiertos de animales identificados
2. **Generar visualizaciones geográficas** interactivas por localidad
3. **Identificar patrones** en la distribución de especies y características
4. **Proporcionar información** útil para políticas públicas de bienestar animal

---

## 🗂️ Fuente de Datos

**Dataset:** Animales identificados con microchip por localidad  
**Fuente:** Datos Abiertos Bogotá  
**Registros:** ~23,412 animales  
**Formato:** CSV delimitado por punto y coma (;)

### Campos del Dataset:
- `microchip_animal`: Código único del microchip
- `especie`: CANINO o FELINO
- `sexo_animal`: MACHO o HEMBRA
- `tamano_animal`: MINIATURA, PEQUEÑO, MEDIANO, GRANDE, MUY GRANDE
- `potencialmente_peligroso`: SI o NO
- `localidad_territorializacion`: Localidad de Bogotá

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Paso 1: Clonar el repositorio
```bash
git clone <repository-url>
cd geo_bog
```

### Paso 2: Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Inicializar la base de datos
```bash
python main.py init-db
```

---

## 📊 Ejecución del Proyecto

### Opción 1: Ejecutar ETL desde Script Python

```bash
python etl_animales_bogota.py
```

Este script ejecutará todo el proceso ETL:
- ✅ Extrae datos del CSV
- ✅ Limpia y transforma datos
- ✅ Carga a base de datos SQLite
- ✅ Genera mapa interactivo
- ✅ Genera mapa de calor
- ✅ Exporta datos procesados

### Opción 2: Ejecutar desde Jupyter Notebook

```bash
jupyter notebook notebooks/analisis_animales_microchip_bogota.ipynb
```

Ejecuta cada celda del notebook para realizar el análisis paso a paso con visualizaciones completas.

### Opción 3: Iniciar aplicación web

```bash
python main.py web
```

Abre tu navegador en: http://localhost:5000

---

## 🗺️ Visualizaciones Generadas

### 1. Mapa Interactivo por Localidades
- **Archivo:** `web/static/mapa_animales_bogota.html`
- **Descripción:** Mapa con marcadores circulares por localidad
- **Características:**
  - Tamaño proporcional al número de animales
  - Código de colores según densidad
  - Popups informativos con estadísticas
  - Controles de zoom y capas

### 2. Mapa de Calor (Heatmap)
- **Archivo:** `web/static/mapa_calor_animales_bogota.html`
- **Descripción:** Visualización de densidad mediante gradiente de color
- **Características:**
  - Gradiente azul → verde → amarillo → rojo
  - Identificación visual de zonas críticas
  - Interfaz interactiva

### 3. Dashboard Web
- **URL:** http://localhost:5000
- **Características:**
  - Estadísticas generales
  - Gráficos interactivos con Plotly
  - Tablas de datos
  - Acceso a mapas integrados

---

## 📈 Análisis y Resultados

### Hallazgos Principales

1. **Distribución por Localidad:**
   - Las localidades con mayor registro son: Suba, Kennedy, Engativá y Usaquén
   - Corresponden a zonas con mayor población y desarrollo urbano

2. **Distribución por Especie:**
   - **Caninos:** ~85% del total
   - **Felinos:** ~15% del total
   - Los caninos predominan en todas las localidades

3. **Animales Potencialmente Peligrosos:**
   - Menos del 5% del total
   - Mayor concentración en localidades con más población
   - Principalmente razas caninas grandes

4. **Patrones Identificados:**
   - Correlación entre nivel socioeconómico y registro de microchips
   - Mayor identificación en zonas urbanas vs. periféricas
   - Tendencia de identificación en mascotas de compañía

### Estadísticas Clave

```
Total de animales identificados: 23,412
Total de localidades: 20
Caninos: ~19,900 (85%)
Felinos: ~3,500 (15%)
Animales potencialmente peligrosos: ~1,170 (5%)
```

---

## 🛠️ Tecnologías Utilizadas

### Backend y Procesamiento
- **Python 3.x** - Lenguaje principal
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas
- **SQLite** - Base de datos embebida

### Visualización
- **Folium** - Mapas interactivos con Leaflet.js
- **Plotly** - Gráficos interactivos
- **Matplotlib & Seaborn** - Gráficos estadísticos

### Web
- **Flask** - Framework web minimalista
- **HTML/CSS/JavaScript** - Frontend
- **Leaflet.js** - Motor de mapas (vía Folium)

---

## 📁 Estructura de Archivos Generados

```
geo_bog/
├── database/
│   └── geo_bog.db                          # Base de datos SQLite
├── data/
│   ├── raw/
│   │   └── c4p-animales-...csv            # Datos originales
│   └── processed/
│       ├── animales_microchip_procesado.csv
│       └── estadisticas_por_localidad.csv
├── web/static/
│   ├── mapa_animales_bogota.html          # Mapa interactivo
│   ├── mapa_calor_animales_bogota.html    # Mapa de calor
│   └── datos_localidades.json             # Datos para web
├── notebooks/
│   └── analisis_animales_microchip_bogota.ipynb
└── logs/
    └── etl.log                             # Logs de ejecución
```

---

## 🔍 Metodología

### Fase 1: EXTRACT (Extracción)
1. Lectura de archivo CSV con encoding latin-1
2. Identificación de estructura y tipos de datos
3. Validación de integridad del dataset

### Fase 2: TRANSFORM (Transformación)
1. Limpieza de duplicados (por microchip único)
2. Normalización de texto (mayúsculas, espacios)
3. Agregación por localidad
4. Cálculo de estadísticas:
   - Total de animales por localidad
   - Distribución por especie
   - Conteo de animales peligrosos
   - Identificación de especie predominante
5. Enriquecimiento con coordenadas geográficas

### Fase 3: LOAD (Carga)
1. Creación de schema en SQLite
2. Carga de datos individuales (tabla `animales_microchip`)
3. Carga de agregados (tabla `estadisticas_localidad`)
4. Exportación a formatos CSV y JSON

### Fase 4: VISUALIZACIÓN
1. Generación de mapa interactivo con Folium
2. Creación de mapa de calor
3. Desarrollo de dashboard web
4. Integración de gráficos interactivos

---

## 📊 API REST Endpoints

La aplicación web expone los siguientes endpoints:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Dashboard principal |
| GET | `/mapa` | Página con mapas interactivos |
| GET | `/api/animales-microchip` | Datos de animales (últimos 100) |
| GET | `/api/estadisticas-localidad` | Estadísticas por localidad |
| GET | `/health` | Estado del servicio |

---

## 🎓 Conclusiones

### Técnicas
1. **ETL Exitoso:** Se procesaron exitosamente más de 23,000 registros con pipeline automatizado
2. **Visualización Efectiva:** Los mapas interactivos facilitan la interpretación de datos espaciales
3. **Escalabilidad:** La arquitectura permite agregar nuevos análisis fácilmente
4. **Reproducibilidad:** El código documentado permite replicar el análisis

### De Negocio
1. **Cobertura Desigual:** Existe disparidad en la identificación entre localidades
2. **Oportunidad de Mejora:** Localidades periféricas requieren mayor sensibilización
3. **Control de Peligrosidad:** El bajo porcentaje de animales peligrosos es positivo
4. **Tendencia Positiva:** El registro con microchip muestra adopción de tecnología para bienestar animal

---

## 💡 Recomendaciones

### Para Política Pública
1. **Ampliar Cobertura:** Implementar programas de identificación en localidades con menor registro
2. **Campañas Educativas:** Sensibilizar sobre beneficios del microchip
3. **Subsidios:** Considerar subsidios para identificación en zonas de bajos recursos
4. **Seguimiento:** Establecer métricas de crecimiento anual por localidad

### Para Desarrollo Técnico
1. **Actualización Periódica:** Automatizar ingesta mensual de datos
2. **Análisis Temporal:** Incorporar series de tiempo para identificar tendencias
3. **Machine Learning:** Implementar modelos predictivos de adopción
4. **Integración:** Conectar con otros datasets urbanos (parques, veterinarias)

---

## 👥 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

---

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas, abre un issue en el repositorio de GitHub.

---

## 🙏 Agradecimientos

- **Datos Abiertos Bogotá** por proporcionar el dataset
- **OpenStreetMap** por los mapas base
- **Comunidad Python** por las librerías utilizadas

---

**Última actualización:** Octubre 2025  
**Versión:** 1.0.0
