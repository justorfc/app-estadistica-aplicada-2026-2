"""
pages/3_Distribuciones.py - Módulo de Distribuciones de Probabilidad

Estado: EN CONSTRUCCIÓN

Temas a implementar:
1. Ajuste de distribuciones (Normal, Lognormal, Gamma, Weibull, Gumbel, GEV)
2. Pruebas de bondad de ajuste (Kolmogorov-Smirnov, Anderson-Darling)
3. Criterios de información (AIC, BIC, AICc)
4. Período de retorno y riesgo
5. Comparación de modelos
6. Análisis de incertidumbre
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
    page_title="Distribuciones - Estadística Aplicada",
    page_icon="📈",
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

st.markdown("# 📈 Módulo: Distribuciones de Probabilidad")
st.markdown("**Ajusta y compara modelos probabilísticos para tus datos**")

st.markdown("---")

# Estado: EN CONSTRUCCIÓN
st.info("""
🚧 **PÁGINA EN CONSTRUCCIÓN** 

Esta página está siendo desarrollada. Los temas se agregarán en las próximas versiones.
Mientras tanto, puedes ajustar distribuciones manualmente con muestra_dist10.csv.
""")

st.markdown("---")

st.markdown("## 📋 Temas a Implementar")

st.markdown("""
### 1. 📊 Distribuciones a Ajustar

| Distribución | Uso | Parámetros | Aplicación |
|---|---|---|---|
| **Normal** | Datos simétricos, central limit theorem | μ (media), σ² (varianza) | Rendimiento |
| **Lognormal** | Datos positivos, sesgados | μ, σ (en log-escala) | Concentración de nutrientes |
| **Gamma** | Datos positivos, forma flexible | α (forma), β (escala) | Tiempo de secado |
| **Weibull** | Confiabilidad, tiempos de falla | k (forma), λ (escala) | Vida útil de equipos |
| **Gumbel** | Máximos anuales | μ, β (escala) | Precipitación máxima anual |
| **GEV** | Extremos generalizados | ξ, μ, σ | Eventos climáticos |

### 2. ✅ Pruebas de Bondad de Ajuste

**Kolmogorov-Smirnov (KS):**
- Compara CDF empírica vs. teórica
- Estadístico: D = max|F_obs(x) - F_teo(x)|
- p-value: Si > 0.05 → datos consistentes con modelo

**Anderson-Darling (AD):**
- Similar a KS pero da más peso a colas
- Mejor para detectar desviaciones en extremos
- Más sensible que KS

### 3. 📐 Criterios de Información

**AIC (Akaike Information Criterion):**
- AIC = 2k - 2ln(L)
- k = número de parámetros
- L = máxima verosimilitud
- **Menor AIC = Mejor modelo**

**BIC (Bayesian Information Criterion):**
- BIC = k·ln(n) - 2ln(L)
- Penaliza más parámetros que AIC
- Preferible con muestras grandes

**AICc (AIC Corregido):**
- AICc = AIC + 2k(k+1)/(n-k-1)
- Recomendado cuando n/k < 40
- Mejor para muestras pequeñas

### 4. 🔮 Período de Retorno y Riesgo

**Período de Retorno (T años):**
- T = 1 / P(X > x)
- Ejemplo: precipitación que ocurre 1 vez cada 10 años
- T₁₀ = 1/0.1 = 10 años

**Riesgo (en T años):**
- R = 1 - (1 - 1/T)^T
- Probabilidad de ocurrir al menos 1 vez en T años
- Ejemplo: Riesgo de precipitación máxima 10-años en próximos 25 años

**Incertidumbre:**
- Intervalo de confianza del cuantil (95%, 90%)
- Bootstrap paramétrico
- Variabilidad en parámetros estimados

### 5. 📊 Visualizaciones

- Histograma de datos observados vs. densidad teórica
- CDF empírica vs. CDF teórica
- P-P plot (Probability-Probability)
- Q-Q plot (Quantile-Quantile)
- Gráfico de residuos

### 6. 🏆 Selección de Modelo

Tabla comparativa:
- Distribución | KS p-value | AD | AIC | BIC | AICc | Recomendación
- Mejor modelo según criterio elegido
- Justificación agrícola
""")

st.markdown("---")

st.markdown("""
### 🌾 Aplicaciones Agrícolas

**Precipitación Máxima Anual (Gumbel):**
- ¿Con qué frecuencia se presentan lluvias extremas?
- ¿Qué lámina se espera cada 25, 50, 100 años?
- Diseño de sistemas de drenaje

**Rendimiento (Normal/Lognormal):**
- ¿Cuántas parcelas producen menos de cierto umbral?
- Predicción de cosechas
- Análisis de riesgo de pérdida

**Secado de Capa Delgada (Gamma/Weibull):**
- ¿Tiempo promedio hasta 50% humedad?
- Variabilidad en procesos de secado
- Optimización de energía
""")

st.markdown("---")

st.markdown("""
### ✏️ Habilidades que Practicarás

- **Python:** SciPy (stats), Statsmodels, ajuste de parámetros
- **Estadística:** Distribuciones, bondad de ajuste, criterios de información
- **Visualización:** Histogramas con ajustes, Q-Q plots, CDF
- **Interpretación:** Período de retorno, riesgo, incertidumbre agrícola
""")
