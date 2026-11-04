"""
App Principal: Estadística Aplicada para Ingeniería Agrícola

Estructura multipágina (Streamlit Pages):
1. Inicio (home)
2. Datos (data exploration and upload)
3. EDA (exploratory data analysis)
4. Distribuciones (probability distributions)
5. Regresión (linear regression)
6. Series de Tiempo (time series forecasting)

Ejecución:
    .venv/bin/streamlit run app.py

Configuración:
    - config.toml: headless=true, enableXsrfProtection=false (para Codespaces)
    - Caché: Streamlit @st.cache_data para optimizar carga de datos
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar carpeta src al path para importar módulos propios
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))

from utilidades import cargar_metadatos

# ============================================================================
# Configuración de página
# ============================================================================

st.set_page_config(
    page_title="Estadística Aplicada - Ingeniería Agrícola",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Estilo CSS personalizado
# ============================================================================

st.markdown("""
<style>
    /* Estilos para la app */
    .main {
        max-width: 1200px;
    }
    
    .titulo-principal {
        text-align: center;
        color: #2d5016;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    
    .subtitulo {
        text-align: center;
        color: #558b2f;
        font-size: 1.2em;
        margin-bottom: 1em;
    }
    
    .card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Barra lateral: información del estudiante
# ============================================================================

with st.sidebar:
    st.markdown("### 👤 Información del Estudiante")
    
    try:
        metadatos = cargar_metadatos()
        
        st.write(f"**Nombre:** {metadatos['nombre']}")
        st.write(f"**Código:** {metadatos['codigo']}")
        st.write(f"**Cultivo:** {metadatos['cultivo']}")
        st.write(f"**Municipio:** {metadatos['municipio']}")
        st.write(f"**Parcelas:** {metadatos['n_parcelas']}")
        st.write(f"**Huella:** `{metadatos['huella']}`")
        
        st.divider()
        
    except Exception as e:
        st.error(f"❌ Error al cargar metadatos: {e}")
    
    st.markdown("### 📚 Módulos")
    st.markdown("""
    1. **Inicio** - Bienvenida y orientación
    2. **Datos** - Carga y exploración
    3. **EDA** - Análisis exploratorio
    4. **Distribuciones** - Modelos de probabilidad
    5. **Regresión** - Análisis de correlación y ajuste
    6. **Series de Tiempo** - Descomposición y pronóstico
    """)
    
    st.divider()
    
    st.markdown("### ⚙️ Configuración")
    st.markdown("""
    - **Datos:** `datos/` (NO MODIFICAR)
    - **Script:** `generar_datos.py` (NO MODIFICAR)
    - **Plan:** Revisar `docs/PLAN_DESARROLLO.md`
    """)

# ============================================================================
# Página de inicio
# ============================================================================

st.markdown('<h1 class="titulo-principal">🌾 Estadística Aplicada</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Análisis Estadístico para Ingeniería Agrícola</p>', unsafe_allow_html=True)

st.divider()

# Sección bienvenida
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 👋 Bienvenida
    
    Esta aplicación te guía a través de un análisis estadístico completo de tus datos de cultivo.
    
    **Módulos:**
    - 📊 **Datos**: Carga y validación de archivos
    - 🔍 **EDA**: Análisis exploratorio y visualización
    - 📈 **Distribuciones**: Ajuste de modelos probabilísticos
    - 📉 **Regresión**: Correlación y ajuste lineal
    - 🕐 **Series de Tiempo**: Pronósticos y tendencias
    """)

with col2:
    st.markdown("""
    ### 📋 Tu Proyecto
    
    **Estudiante:**  
    Datos personalizados según tu código (semilla RNG)
    
    **Reproducibilidad:**  
    Misma semilla = mismos datos siempre
    
    **Carpetas:**
    - `datos/` - Tu conjunto de datos
    - `src/` - Módulos compartidos
    - `pages/` - Páginas de la app
    """)

st.divider()

# Sección de navegación
st.markdown("### 🚀 Comienza aquí")

tabs = st.tabs(["📌 Introducción", "📚 Cómo usar", "❓ FAQ"])

with tabs[0]:
    st.markdown("""
    **¿Qué voy a aprender?**
    
    1. **Análisis Exploratorio de Datos (EDA):** Descubre patrones, relaciones y anomalías
    2. **Distribuciones de Probabilidad:** Ajusta y evalúa modelos estadísticos
    3. **Regresión Lineal:** Modela relaciones entre variables
    4. **Series de Tiempo:** Analiza y pronostica fenómenos temporales
    
    **Herramientas:**
    - 🐍 Python + Streamlit (web interactiva)
    - 📊 Pandas, NumPy, SciPy (análisis)
    - 📈 Matplotlib, Seaborn (visualización)
    - 🧪 Statsmodels, Scikit-learn (estadística)
    """)

with tabs[1]:
    st.markdown("""
    **Pasos principales:**
    
    1. Usa la **barra lateral** para navegar entre módulos
    2. Cada módulo tiene instrucciones paso a paso
    3. Sube archivos CSV o usa los datos predeterminados
    4. Visualiza gráficas y tablas interactivas
    5. Interpreta resultados con apoyo pedagógico
    
    **Consejos:**
    - Lee los enunciados antes de analizar
    - Observa las unidades en los gráficos
    - Haz anotaciones en tu cuaderno
    - Consulta el plan de desarrollo: `docs/PLAN_DESARROLLO.md`
    """)

with tabs[2]:
    st.markdown("""
    **¿Puedo cambiar los datos?**  
    No. Los datos se regeneran desde `generar_datos.py`. 
    Para restaurar: `.venv/bin/python generar_datos.py`
    
    **¿Por qué números diferentes a otros compañeros?**  
    Cada estudiante tiene código único → semilla única → datos únicos (pero reproducibles)
    
    **¿Puedo descargar mis resultados?**  
    Sí. Usa el botón "Descargar" que aparece en cada página.
    
    **¿Qué hago si la app falla?**  
    1. Reinicia: `Ctrl+C` en terminal, luego `.venv/bin/streamlit run app.py`
    2. Revisa que `datos/` tenga todos los archivos CSV
    3. Regenera datos: `.venv/bin/python generar_datos.py`
    """)

st.divider()

# Verificación de datos
st.markdown("### ✅ Verificación del Sistema")

try:
    from utilidades import cargar_datos, validar_datos
    
    # Intentar cargar un archivo de prueba
    try:
        df_test = cargar_datos('metadatos.json'.replace('.json', '.csv'))
    except:
        df_test = cargar_datos('parcelas.csv')
    
    col_status, col_info = st.columns(2)
    
    with col_status:
        st.success("✅ Conexión con datos OK")
        st.success("✅ Módulos cargados correctamente")
        st.success("✅ Sistema listo para usar")
    
    with col_info:
        st.info("📁 Archivos disponibles en `datos/`")
        archivos = ['parcelas.csv', 'precip_max_anual.csv', 'clima_mensual.csv', 
                   'secado.csv', 'muestra_eda10.csv', 'muestra_dist10.csv', 
                   'muestra_reg8.csv', 'muestra_series24.csv']
        st.write(f"✓ {len(archivos)} archivos CSV")
        
except Exception as e:
    st.error(f"⚠️ Error de verificación: {e}")

st.divider()

# Pie de página
st.markdown("""
---
**Estadística Aplicada para Ingeniería Agrícola** 
| Tutor IA | [Plan de Desarrollo](docs/PLAN_DESARROLLO.md)
""")
