"""
pages/4_Regresion.py - Módulo de Regresión Lineal Simple

Estado: EN CONSTRUCCIÓN

Temas a implementar:
1. Correlación de Pearson y Spearman
2. Regresión lineal por Mínimos Cuadrados Ordinarios (MCO)
3. Estimación de parámetros e intervalos de confianza
4. Bondad de ajuste (R², R² ajustado)
5. Inferencia sobre la pendiente (test t)
6. Diagnóstico de residuos
7. Detección de influencia (Distancia de Cook)
8. Comparación de modelos de secado en capa delgada
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
    page_title="Regresión - Estadística Aplicada",
    page_icon="📉",
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

st.markdown("# 📉 Módulo: Regresión Lineal Simple")
st.markdown("**Modela relaciones lineales entre dos variables**")

st.markdown("---")

# Estado: EN CONSTRUCCIÓN
st.info("""
🚧 **PÁGINA EN CONSTRUCCIÓN** 

Esta página está siendo desarrollada. Los temas se agregarán en las próximas versiones.
Mientras tanto, puedes ajustar regresiones manualmente con muestra_reg8.csv.
""")

st.markdown("---")

st.markdown("## 📋 Temas a Implementar")

st.markdown("""
### 1. 📊 Correlación

**Correlación de Pearson (r):**
- Relación lineal entre variables
- r ∈ [-1, 1]
  - r = 1: Correlación positiva perfecta
  - r = 0: Sin correlación
  - r = -1: Correlación negativa perfecta
- Supuestos: Normalidad, linealidad

**Correlación de Spearman (ρ):**
- Basada en rangos (no-paramétrica)
- Menos sensible a outliers que Pearson
- Captura relaciones monótonas (no necesariamente lineales)

### 2. 📈 Regresión Lineal Simple: Y = β₀ + β₁·X

**Estimación de parámetros (MCO - Mínimos Cuadrados Ordinarios):**
- β₁ = Σ[(Xᵢ - X̄)(Yᵢ - Ȳ)] / Σ[(Xᵢ - X̄)²]
- β₀ = Ȳ - β₁·X̄

**Interpretación:**
- β₀: Intercepto (valor de Y cuando X = 0)
- β₁: Pendiente (cambio en Y por unidad de X)
- Ejemplo: Si β₁ = 0.5 t/ha·mm → +1 mm riego → +0.5 t/ha rendimiento

### 3. 📐 Bondad de Ajuste

**Coeficiente de Determinación (R²):**
- R² = 1 - (SS_res / SS_tot)
- R² ∈ [0, 1]
- Proporción de variabilidad en Y explicada por X
- R² = 0.85 → El modelo explica 85% de variabilidad

**R² Ajustado:**
- R²_adj = 1 - [(n-1)/(n-p)] × (1 - R²)
- Penaliza el número de parámetros (p)
- Mejor para comparar modelos con diferente número de variables

**Error Estándar de la Estimación:**
- s = √(SS_res / (n-2))
- Desviación típica de residuos
- Unidades de Y

### 4. 🔬 Inferencia sobre la Pendiente

**Test t para H₀: β₁ = 0**
- t = β₁ / SE(β₁)
- SE(β₁) = s / √Σ[(Xᵢ - X̄)²]
- p-value: Probabilidad de observar β₁ si no existe relación
- Si p-value < 0.05 → Rechazar H₀ (relación significativa)

**Intervalo de Confianza (95%):**
- β₁ ± t(α/2, n-2) × SE(β₁)
- Rango probable del verdadero parámetro

### 5. 🔍 Diagnóstico de Residuos

**Gráfico de Residuos vs. Predichos:**
- Evaluación de linealidad: Residuos distribuidos aleatoriamente
- Homocedasticidad: Varianza constante (no forma de "embudo")

**Q-Q Plot de Residuos:**
- Evaluación de normalidad
- Puntos sobre línea y=x → Residuos normales

**Escala-Ubicación Plot:**
- √|residuos estandarizados| vs. predichos
- Alternativa para detectar heterocedasticidad

### 6. 👁️ Distancia de Cook (Influencia)

**Detecta observaciones influyentes:**
- D_i = (ê_i²/p) × (h_ii / (1-h_ii)) × s²
- D_i > 4/n → Observación potencialmente influyente
- Evalúa impacto de eliminar cada fila en β

### 7. 🌾 Modelos de Secado en Capa Delgada

**Modelo de Page:**
- MR = exp(-k·t^n)
- ln(MR) = -k·t^n (linealización parcial)
- k, n parámetros a estimar
- Comparar AICc con otros modelos

**Modelos Alternativos:**
- Newton: MR = exp(-k·t)
- Henderson: MR = a·exp(-k·t) + (1-a)·exp(-b·t)
- Criterio: AICc para muestras pequeñas
""")

st.markdown("---")

st.markdown("""
### 🌾 Ejemplos Agrícolas

**Regresión 1: Rendimiento vs. Lámina de Riego**
- Y = rendimiento (t/ha)
- X = lámina_riego (mm)
- Datos: muestra_reg8.csv (8 parcelas)
- Pregunta: ¿Cuánto aumenta rendimiento por mm de riego?

**Regresión 2: Rendimiento vs. Dosis de N**
- Y = rendimiento (t/ha)
- X = dosis_N (kg/ha)
- ¿Existe optimum? ¿Relación linear?

**Secado de Capa Delgada:**
- Y = ln(MR) (log de razón de humedad)
- X = tiempo (min)
- Modelo: Ajustar n, k en MR = exp(-k·t^n)
- Comparar con otros modelos usando AICc
""")

st.markdown("---")

st.markdown("""
### ✏️ Habilidades que Practicarás

- **Python:** Statsmodels, Scikit-learn, regresión
- **Estadística:** MCO, R², test t, intervalos de confianza, residuos
- **Visualización:** Scatter + recta, residuos, Q-Q plot, Cook
- **Interpretación:** Pendiente agrícola, bondad de ajuste, supuestos
- **Comparación de Modelos:** AICc para secado de capa delgada
""")
