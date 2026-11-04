"""
pages/1_Datos.py - Módulo de Carga y Exploración de Datos

Estado: EN CONSTRUCCIÓN

Temas a implementar:
1. Carga de archivos CSV
2. Vista de tabla de datos (interactiva, st.dataframe)
3. Estadísticas descriptivas básicas
4. Detección de valores atípicos (outliers)
5. Análisis de valores faltantes
6. Histogramas y gráficas univariadas
7. Descarga de resultados
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar carpeta src al path (CRÍTICO)
ruta_src = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(ruta_src))

from datos import tarjeta_estudiante

# ============================================================================
# Configuración
# ============================================================================

st.set_page_config(
    page_title="Datos - Estadística Aplicada",
    page_icon="📊",
    layout="wide"
)

# ============================================================================
# Barra lateral: Tarjeta del estudiante
# ============================================================================

with st.sidebar:
    tarjeta_estudiante(ubicacion='sidebar')

# ============================================================================
# Página Principal
# ============================================================================

st.markdown("# 📊 Módulo: Datos")
st.markdown("**Exploración, validación y análisis de tu dataset**")

st.markdown("---")

# Estado: EN CONSTRUCCIÓN
st.info("""
🚧 **PÁGINA EN CONSTRUCCIÓN** 

Esta página está siendo desarrollada. Los temas se agregarán en las próximas versiones.
Mientras tanto, puedes explorar tu dataset manualmente en la carpeta `datos/`.
""")

st.markdown("---")

st.markdown("## 📋 Temas a Implementar")

st.markdown("""
### 1. 📥 Carga de Archivos CSV
- Selector de archivo predeterminado
- Opción para subir archivo personalizado
- Validación de estructura

### 2. 📊 Tabla de Datos
- Vista interactiva con st.dataframe
- Ordenamiento y filtrado
- Información de dimensiones (filas × columnas)

### 3. 📈 Estadísticas Descriptivas
- Tabla resumen: media, desv. est., min, 25%, mediana, 75%, máx
- Formato español (1.234,57)
- Separación por tipo de variable (numérica vs. categórica)

### 4. ⚠️ Detección de Outliers
- Método IQR (Rango Intercuartílico)
- Visualización de atípicos
- Lista de filas con valores anómalos

### 5. 🔍 Análisis de Valores Faltantes
- Conteo de N/D por columna
- Porcentaje de completitud
- Gráfico de patrón de faltantes

### 6. 📉 Histogramas Univariados
- Gráficas para cada variable numérica
- Distribuciones observadas
- Identificación de formas (normal, sesgada, etc.)

### 7. ⬇️ Descarga de Resultados
- Botón para descargar tabla resumen en CSV
- Botón para descargar gráficas en PNG
""")

st.markdown("---")

st.markdown("""
### ✏️ Habilidades que Practicarás

- **Python:** Lectura de CSV con Pandas, cálculo de estadísticas
- **Estadística:** Media, mediana, percentiles, IQR, outliers
- **Visualización:** Histogramas con Matplotlib/Seaborn
- **Interpretación:** Detectar patrones y anomalías en datos reales
""")
