"""
app.py - Página Principal de la App de Estadística Aplicada

Punto de entrada para la app multipágina Streamlit.
Estructura:
1. Configuración de página
2. Barra lateral: tarjeta del estudiante + navegación
3. Página principal: introducción, propósito, descripción de módulos, 
   sección "Lápiz y Algoritmo", advertencia académica

Ejecución:
    .venv/bin/streamlit run app.py

Acceso:
    http://localhost:8501 (local)
    http://<IP>:8501 (red)
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar carpeta src al path (CRÍTICO para evitar ModuleNotFoundError)
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))

# Importar funciones del módulo datos
from datos import cargar_metadatos, tarjeta_estudiante

# ============================================================================
# Configuración de página
# ============================================================================

st.set_page_config(
    page_title="Estadística Aplicada con Python y R",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Estilos CSS personalizados
# ============================================================================

st.markdown("""
<style>
    /* Colores corporativos agrícolas */
    :root {
        --verde-oscuro: #2d5016;
        --verde-claro: #558b2f;
        --verde-suave: #f1f5e8;
    }
    
    /* Títulos */
    .titulo-principal {
        text-align: center;
        color: #2d5016;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.3em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .subtitulo {
        text-align: center;
        color: #558b2f;
        font-size: 1.3em;
        margin-bottom: 1.5em;
        font-weight: 500;
    }
    
    /* Cajas de contenido */
    .card {
        border-left: 5px solid #2d5016;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        background-color: #f9faf7;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .card-warning {
        border-left: 5px solid #ff6b6b;
        background-color: #fff5f5;
    }
    
    .card-success {
        border-left: 5px solid #51cf66;
        background-color: #f1fce4;
    }
    
    /* Separador */
    .divider {
        margin: 30px 0;
        border-top: 2px solid #2d5016;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Barra lateral: Tarjeta del estudiante + Navegación
# ============================================================================

with st.sidebar:
    st.markdown("---")
    
    # Tarjeta del estudiante
    tarjeta_estudiante(ubicacion='sidebar')
    
    st.markdown("---")
    
    # Menú de módulos
    st.markdown("### 📚 Módulos de la App")
    st.markdown("""
    1. **📊 Datos** - Exploración y validación
    2. **🔍 EDA** - Análisis exploratorio
    3. **📈 Distribuciones** - Modelos probabilísticos
    4. **📉 Regresión** - Correlación y ajuste lineal
    5. **🕐 Series de Tiempo** - Tendencias y pronósticos
    """)
    
    st.markdown("---")
    
    # Referencias
    st.markdown("### 📖 Referencias")
    st.markdown("""
    - [Plan de Desarrollo](https://github.com)
    - [Datos](datos/)
    - [Python Docs](https://docs.python.org)
    """)

# ============================================================================
# Página Principal
# ============================================================================

# Encabezado
st.markdown('<h1 class="titulo-principal">🌾 App de Estadística Aplicada</h1>', 
            unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Ingeniería Agrícola, Unisucre</p>', 
            unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECCIÓN 1: Propósito de la App
# ============================================================================

st.markdown("## 📋 Propósito de la App")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    Esta aplicación web **interactiva y educativa** te guía a través de un 
    análisis estadístico completo de tus datos agrícolas.
    
    **Características:**
    - 📊 Datos personalizados según tu código estudiantil
    - 🔄 Reproducible (misma semilla = mismos datos)
    - 🎓 Apoyo pedagógico en cada paso
    - 🐍 Código en Python con verificación en R
    - 📈 Visualizaciones con Matplotlib y Seaborn
    """)

with col2:
    st.markdown("""
    **¿Qué aprenderás?**
    
    1. **Exploración de Datos** (EDA)
    2. **Distribuciones de Probabilidad**
    3. **Regresión Lineal**
    4. **Series de Tiempo**
    5. **Pronósticos y Tendencias**
    
    Todo con énfasis en **interpretación agrícola**.
    """)

st.markdown("---")

# ============================================================================
# SECCIÓN 2: Descripción de Módulos
# ============================================================================

st.markdown("## 🚀 Módulos de Aprendizaje")

tabs = st.tabs(["📊 Datos", "🔍 EDA", "📈 Distribuciones", "📉 Regresión", "🕐 Series de Tiempo"])

with tabs[0]:
    st.markdown("""
    ### 📊 Módulo: Datos
    
    **Objetivo:** Explorar, validar y comprender tu dataset.
    
    **Contenido:**
    - Carga de archivos CSV
    - Tabla de datos interactiva
    - Estadísticas descriptivas (media, desv. est., percentiles)
    - Detección de valores atípicos (outliers)
    - Análisis de valores faltantes (N/D)
    - Histogramas y distribuciones univariadas
    
    **Archivos disponibles:**
    - `parcelas.csv`: 116 parcelas con rendimiento
    - `precip_max_anual.csv`: 40 años de precipitación máxima
    - `clima_mensual.csv`: 132 meses de clima
    - `secado.csv`: Curvas de secado de capa delgada
    
    **Cálculos a mano:** Selecciona una muestra pequeña y calcula media, desv. est., 
    luego verifica con la app.
    """)

with tabs[1]:
    st.markdown("""
    ### 🔍 Módulo: Análisis Exploratorio de Datos (EDA)
    
    **Objetivo:** Descubrir patrones, relaciones y anomalías.
    
    **Contenido:**
    - Matriz de correlaciones (Pearson y Spearman)
    - Gráfico de dispersión (scatter plots)
    - Boxplots por grupos
    - Q-Q plots (normalidad)
    - Heatmaps de correlación
    - Análisis de interacciones
    
    **Preguntas a responder:**
    - ¿Cuál es la relación entre dosis de N y rendimiento?
    - ¿Los atípicos afectan la correlación?
    - ¿Hay diferencias por tipo de suelo?
    
    **Verificación:** Calcula correlaciones manualmente en 8 parcelas (muestra_reg8.csv)
    """)

with tabs[2]:
    st.markdown("""
    ### 📈 Módulo: Distribuciones de Probabilidad
    
    **Objetivo:** Ajustar y comparar modelos de distribución.
    
    **Modelos implementados:**
    - **Normal:** Distribución gaussiana (campana)
    - **Lognormal:** Log-transformada (positiva)
    - **Gamma:** Forma y escala
    - **Weibull:** Eventos extremos
    - **Gumbel:** Máximos anuales (precipitación)
    - **GEV:** Teoría de valores extremos
    
    **Pruebas de bondad de ajuste:**
    - Kolmogorov-Smirnov (KS)
    - Anderson-Darling (AD)
    - Criterios de información: AIC, BIC, AICc
    
    **Aplicación agrícola:**
    - Precipitación máxima anual (Gumbel)
    - Período de retorno (T años)
    - Riesgo de eventos extremos
    
    **Verificación:** Ajusta distribuciones manualmente en 10 años (muestra_dist10.csv)
    """)

with tabs[3]:
    st.markdown("""
    ### 📉 Módulo: Regresión Lineal Simple
    
    **Objetivo:** Modelar relaciones lineales entre variables.
    
    **Contenido:**
    - Correlación de Pearson y Spearman
    - Regresión lineal por Mínimos Cuadrados Ordinarios (MCO)
    - Estimación de parámetros (pendiente, intercepto)
    - Bondad de ajuste (R², coeficiente de determinación)
    - Intervalos de confianza
    - Inferencia sobre la pendiente (test t)
    - Diagnóstico de residuos:
      * Q-Q plots (normalidad)
      * Gráfico residuos vs. predichos (homocedasticidad)
      * Distancia de Cook (influencia)
    
    **Ejemplo agrícola:**
    - Rendimiento vs. Lámina de riego
    - Relación lineal: Y = β₀ + β₁·X
    
    **Verificación:** Regresión manualmente en 8 parcelas (muestra_reg8.csv)
    """)

with tabs[4]:
    st.markdown("""
    ### 🕐 Módulo: Series de Tiempo
    
    **Objetivo:** Analizar, descomponer y pronosticar datos temporales.
    
    **Componentes de una serie:**
    - **Tendencia:** Dirección general a largo plazo
    - **Estacionalidad:** Patrones repetitivos (meses, años)
    - **Ruido:** Variación aleatoria
    
    **Métodos implementados:**
    - Descomposición clásica (aditiva y multiplicativa)
    - Promedios móviles simples y ponderados
    - Índices estacionales (factores mensuales)
    - Métodos de referencia (naive, seasonal naive)
    - AutoTS (selección automática de modelo)
    
    **Validación:**
    - MAE (Error Absoluto Medio)
    - RMSE (Raíz del Error Cuadrático Medio)
    - SMAPE (Error Porcentual Absoluto Simétrico)
    
    **Aplicación agrícola:**
    - Precipitación mensual (2015-2025, 132 meses)
    - Identificar estación seca/lluviosa
    - Pronóstico para los próximos 6 meses
    
    **Verificación:** Pronóstico manualmente en 24 meses (muestra_series24.csv)
    """)

st.markdown("---")

# ============================================================================
# SECCIÓN 3: Lápiz y Algoritmo
# ============================================================================

st.markdown("## ✏️ Metodología: Lápiz y Algoritmo")

st.markdown("""
<div class="card card-success">
    <h3>✏️ Lápiz y Algoritmo: Aprendizaje Dual</h3>
    
    <p><strong>Filosofía:</strong> Antes de usar la app, 
    <strong>calcula a mano</strong> los resultados. Luego 
    <strong>verifica con Python</strong> y <strong>compara con R</strong>.</p>
    
    <p><strong>¿Por qué?</strong></p>
    <ul>
        <li>🧮 Entiendes la <strong>matemática detrás</strong> de cada cálculo</li>
        <li>🐍 Aprendes <strong>Python</strong> viendo el código</li>
        <li>📊 Practicas <strong>R</strong> para verificar resultados</li>
        <li>✅ Detectas <strong>errores</strong> rápidamente</li>
        <li>🎓 Desarrollas <strong>pensamiento crítico</strong></li>
    </ul>
    
    <p><strong>Proceso en cada módulo:</strong></p>
    <ol>
        <li>📖 Lee el <strong>enunciado</strong> y datos (muestra pequeña, ~10 filas)</li>
        <li>📝 Calcula <strong>a mano</strong> en tu cuaderno (30-45 min)</li>
        <li>💻 Usa la <strong>app</strong> para verificar (5 min)</li>
        <li>🐍 Lee el <strong>código Python</strong> en la app (anotaciones en español)</li>
        <li>🔴 Ejecuta código <strong>R</strong> si es necesario (scripts en repo)</li>
        <li>✍️ Anota <strong>conclusiones</strong> agrícolas</li>
    </ol>
    
    <p><strong>Ejemplo: Regresión Lineal Simple</strong></p>
    <ul>
        <li>📋 Muestra: 8 parcelas (lamina_riego vs. rendimiento)</li>
        <li>✏️ A mano: Calcula Σx, Σy, Σxy, β₀, β₁, R²</li>
        <li>💻 App: Sube datos y compara</li>
        <li>🐍 Python: Visualiza la ecuación de la recta</li>
        <li>🔴 R: Usa lm() y verifica intervalos de confianza</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECCIÓN 4: Advertencia Académica
# ============================================================================

st.markdown("## ⚠️ Advertencia Académica")

st.markdown("""
<div class="card card-warning">
    <h3>⚠️ Responsabilidad Académica</h3>
    
    <p>Esta app es una <strong>herramienta pedagógica</strong> que apoya tu aprendizaje. 
    <strong>TÚ eres responsable de:</strong></p>
    
    <ul>
        <li>✏️ <strong>Interpretar correctamente</strong> los resultados estadísticos</li>
        <li>🎓 <strong>Comprender la teoría</strong> detrás de cada cálculo</li>
        <li>📖 <strong>Validar hipótesis</strong> con bibliografía científica</li>
        <li>📊 <strong>Documentar decisiones</strong> analíticas en tu informe</li>
        <li>✍️ <strong>No copiar</strong> gráficas/tablas sin entenderlas</li>
        <li>🔍 <strong>Verificar resultados</strong> de forma crítica</li>
        <li>📝 <strong>Citar fuentes</strong> (app, libros, papers) en tu trabajo</li>
    </ul>
    
    <p><strong>Sobre los datos:</strong></p>
    <ul>
        <li>📊 Datos simulados pero <strong>estadísticamente realistas</strong></li>
        <li>🌾 Parámetros basados en <strong>investigación agrícola real</strong></li>
        <li>🔄 <strong>Reproducibles</strong> (semilla = tu código estudiantil)</li>
        <li>🎯 <strong>Únicas</strong> para cada estudiante (no comparables directamente)</li>
    </ul>
    
    <p><strong>Uso ético:</strong></p>
    <ul>
        <li>✅ PERMITIDO: Usar la app para aprender y verificar tus cálculos</li>
        <li>✅ PERMITIDO: Compartir resultados con compañeros para comparar métodos</li>
        <li>❌ PROHIBIDO: Copiar resultados de compañeros (datos diferentes)</li>
        <li>❌ PROHIBIDO: Modificar generar_datos.py o carpeta datos/</li>
        <li>❌ PROHIBIDO: Comprometer datos/ en Git</li>
    </ul>
    
    <p><strong>Si encuentras un error:</strong> Reporta en el aula virtual con 
    evidencia (screenshot + resultado esperado).</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECCIÓN 5: Inicio Rápido
# ============================================================================

st.markdown("## 🚀 Inicio Rápido")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1️⃣ Datos
    Explora y valida tu dataset. 
    Calcula estadísticas descriptivas.
    """)
    if st.button("Ir a Datos →", key="btn1", use_container_width=True):
        st.switch_page("pages/1_Datos.py")

with col2:
    st.markdown("""
    ### 2️⃣ EDA
    Descubre patrones y 
    relaciones entre variables.
    """)
    if st.button("Ir a EDA →", key="btn2", use_container_width=True):
        st.switch_page("pages/2_EDA.py")

with col3:
    st.markdown("""
    ### 3️⃣ Distribuciones
    Ajusta modelos probabilísticos
    a tus datos.
    """)
    if st.button("Ir a Distribuciones →", key="btn3", use_container_width=True):
        st.switch_page("pages/3_Distribuciones.py")

st.markdown("---")

# Pie de página
st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #666;">
    <small>
    Estadística Aplicada para Ingeniería Agrícola | Unisucre 2026  
    Tutor IA con Python, R y Streamlit | 
    <a href="docs/PLAN_DESARROLLO.md">Plan de Desarrollo</a>
    </small>
</div>
""", unsafe_allow_html=True)
