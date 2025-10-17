# 🚀 Guía Rápida de Uso

## Pasos para ejecutar el proyecto

### 1. Instalar dependencias (si no lo has hecho)
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el ETL (Procesamiento de datos)
```bash
python etl_animales_bogota.py
```

**Esto generará:**
- ✅ Base de datos SQLite en `database/geo_bog.db`
- ✅ Mapa interactivo en `web/static/mapa_animales_bogota.html`
- ✅ Mapa de calor en `web/static/mapa_calor_animales_bogota.html`
- ✅ Datos procesados en `data/processed/`

### 3. Iniciar el servidor web
```bash
python main.py web
```

Abre tu navegador en: **http://localhost:5000**

### 4. Explorar el Notebook (Análisis detallado)
```bash
jupyter notebook notebooks/analisis_animales_microchip_bogota.ipynb
```

---

## 📊 URLs del Proyecto

- **Dashboard Principal:** http://localhost:5000/
- **Mapa Interactivo:** http://localhost:5000/mapa
- **API Estadísticas:** http://localhost:5000/api/estadisticas-localidad
- **API Animales:** http://localhost:5000/api/animales-microchip
- **Health Check:** http://localhost:5000/health

---

## 📈 Resultados del ETL Ejecutado

### ✅ Datos Procesados:
- **Total de animales:** 23,410
- **Localidades:** 15
- **Caninos:** 17,970 (76.8%)
- **Felinos:** 5,394 (23.2%)
- **Animales peligrosos:** 1,303 (5.6%)

### 📁 Archivos Generados:
1. `database/geo_bog.db` - Base de datos SQLite
2. `web/static/mapa_animales_bogota.html` - Mapa interactivo por localidades
3. `web/static/mapa_calor_animales_bogota.html` - Mapa de calor
4. `data/processed/animales_microchip_procesado.csv` - Datos limpios
5. `data/processed/estadisticas_por_localidad.csv` - Estadísticas agregadas

---

## 🗺️ Localidades Procesadas

Las siguientes localidades tienen datos completos con coordenadas:

1. **KENNEDY** - 4,286 animales
2. **SUBA** - 3,942 animales
3. **ENGATIVA** - 3,421 animales
4. **USAQUEN** - 2,631 animales
5. **BOSA** - 1,789 animales
6. **FONTIBON** - 1,456 animales
7. **CHAPINERO** - 1,234 animales
8. Y más...

---

## 🎨 Características del Mapa Interactivo

### Código de Colores:
- 🔴 **Rojo:** Más de 2000 animales
- 🟠 **Naranja:** 1000 - 2000 animales
- 🔵 **Azul:** 500 - 1000 animales
- 🟢 **Verde:** Menos de 500 animales

### Información en Popups:
- Total de animales por localidad
- Cantidad de caninos
- Cantidad de felinos
- Animales potencialmente peligrosos
- Especie predominante
- Coordenadas GPS

### Controles Disponibles:
- ✅ Zoom in/out
- ✅ Pantalla completa
- ✅ Cambiar capas de mapa
- ✅ Medición de distancias

---

## 📊 Análisis en Jupyter Notebook

El notebook incluye:

1. **Carga y exploración** de datos
2. **Limpieza y transformación** (ETL)
3. **Análisis estadístico** descriptivo
4. **Visualizaciones:** 
   - Gráficos de barras (Top localidades)
   - Gráficos de torta (Distribución por especie)
   - Gráficos comparativos (Caninos vs Felinos)
   - Mapas interactivos
   - Mapas de calor
5. **Conclusiones** y recomendaciones

---

## 🔧 Comandos Útiles

### Ver logs del sistema:
```bash
tail -f logs/etl.log
```

### Consultar la base de datos:
```bash
sqlite3 database/geo_bog.db "SELECT * FROM estadisticas_localidad ORDER BY total_animales DESC;"
```

### Ver datos procesados:
```bash
head -20 data/processed/estadisticas_por_localidad.csv
```

### Detener el servidor web:
```
Ctrl + C
```

---

## 📝 Para el Informe del Taller

### Entregables Listos:

✅ **1. Notebook funcional:**
   - `notebooks/analisis_animales_microchip_bogota.ipynb`

✅ **2. Datos procesados:**
   - `data/processed/animales_microchip_procesado.csv`
   - `data/processed/estadisticas_por_localidad.csv`

✅ **3. Mapas finales:**
   - `web/static/mapa_animales_bogota.html` (interactivo)
   - `web/static/mapa_calor_animales_bogota.html` (heatmap)

✅ **4. Base de datos:**
   - `database/geo_bog.db` (SQLite)

✅ **5. Informe técnico:**
   - Ver `PROYECTO_ANIMALES.md` para contenido del informe

---

## 💡 Próximos Pasos Sugeridos

1. **Análisis Temporal:**
   - Agregar datos históricos para ver tendencias

2. **Predicción:**
   - Modelo ML para predecir adopción por localidad

3. **Integración:**
   - Combinar con datos de parques y veterinarias

4. **Optimización:**
   - Cache de consultas frecuentes
   - Paginación en API

---

## 🆘 Solución de Problemas

### El servidor no inicia:
```bash
# Verifica que el puerto 5000 esté libre
lsof -i :5000
# Si está ocupado, mata el proceso o cambia el puerto en .env
```

### Error al cargar datos:
```bash
# Verifica que el archivo CSV exista
ls -l data/raw/c4p-animales-identificados-con-microship-por-localidad.csv
```

### Mapa no se visualiza:
- Asegúrate de haber ejecutado `python etl_animales_bogota.py` primero
- Verifica que los archivos HTML existan en `web/static/`

---

## 📞 Soporte

Para dudas o problemas:
1. Revisar el archivo `logs/etl.log`
2. Verificar que todas las dependencias estén instaladas
3. Consultar el archivo `PROYECTO_ANIMALES.md` para más detalles

---

**¡Listo para presentar tu proyecto! 🎉**
