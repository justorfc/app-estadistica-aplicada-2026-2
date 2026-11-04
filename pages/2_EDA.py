"""
pages/2_EDA.py - Módulo de Análisis Exploratorio de Datos (EDA)

Estado: EN CONSTRUCCIÓN

Temas a implementar:
1. Matriz de correlaciones (Pearson y Spearman)
2. Gráficos de dispersión (scatter plots)
3. Boxplots por grupos
4. Q-Q plots para normalidad
5. Heatmaps de correlación
6. Análisis de interacciones entre variables
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
    page_title="EDA - Estadística Aplicada",
    page_icon="🔍",
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

st.markdown("# 🔍 Módulo: Análisis Exploratorio de Datos (EDA)")
st.markdown("**Descubre patrones, relaciones y anomalías en tus datos**")

st.markdown("---")

# Estado: EN CONSTRUCCIÓN
st.info("""
🚧 **PÁGINA EN CONSTRUCCIÓN** 

Esta página está siendo desarrollada. Los temas se agregarán en las próximas versiones.
Mientras tanto, puedes calcular correlaciones manualmente con muestra_reg8.csv.
""")

st.markdown("---")

st.markdown("## 📋 Temas a Implementar")

st.markdown("""
### 1. 📊 Correlación y Covarianza
- **Correlación de Pearson:** Relación lineal entre variables numéricas
- **Correlación de Spearman:** Relación monótona (no necesariamente lineal)
- Matriz de correlaciones en formato tabla
- Interpretación: r ∈ [-1, 1]

### 2. 📈 Gráficos de Dispersión (Scatter Plots)
- X vs Y para pares de variables
- Visualización de relaciones
- Identificación de outliers
- Tendencia lineal con línea de regresión

### 3. 📦 Boxplots por Grupos
- Distribución de variable numérica por categoría
- Comparación entre tipos de suelo, riego (Sí/No)
- Identificación visual de medianas, cuartiles, atípicos

### 4. 📐 Q-Q Plots (Quantile-Quantile)
- Evaluación gráfica de normalidad
- Comparación de distribución observada vs. teórica
- Diagnóstico: si puntos están sobre línea y=x → Normal

### 5. 🔥 Heatmaps de Correlación
- Matriz visual de todas las correlaciones
- Escala de colores (rojo = positiva, azul = negativa)
- Identificación rápida de relaciones fuertes

### 6. 🔗 Análisis de Interacciones
- Efecto combinado de dos variables en una tercera
- Gráficos de líneas por grupo
- Ejemplo: rendimiento vs. dosis_N, color por tipo de suelo
""")

st.markdown("---")

st.markdown("""
### 📚 Preguntas de Investigación

**Con datos de parcelas.csv:**
- ¿Correlación entre dosis_N y rendimiento? ¿Lineal?
- ¿Diferencias de rendimiento por tipo de suelo?
- ¿Riego afecta la relación N-rendimiento?
- ¿Impacto del pH en rendimiento?
- ¿Valores extremos (outliers) afectan las correlaciones?

**Con datos de precip_max_anual.csv:**
- ¿Tendencia en precipitación máxima anual?
- ¿Años extremos (máximas muy altas/bajas)?
- ¿Distribución: Normal, Sesgada, Uniforme?

**Con datos de clima_mensual.csv:**
- ¿Patrón bimodal de precipitación (abril-mayo, sep-nov)?
- ¿Correlación entre precipitación y temperatura?
- ¿Tendencia de temperatura en el tiempo?
""")

st.markdown("---")

st.markdown("""
### ✏️ Habilidades que Practicarás

- **Python:** Pandas (corr(), groupby()), Seaborn, Matplotlib
- **Estadística:** Correlación de Pearson/Spearman, normalidad
- **Visualización:** Scatter, boxplot, heatmap, Q-Q plot
- **Interpretación:** Relaciones entre variables, causalidad vs. correlación
""")
