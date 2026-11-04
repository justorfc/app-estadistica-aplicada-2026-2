"""
pages/5_Series_de_tiempo.py - Módulo de Series de Tiempo

Estado: EN CONSTRUCCIÓN

Temas a implementar:
1. Componentes de una serie (tendencia, estacionalidad, ruido)
2. Descomposición clásica (aditiva y multiplicativa)
3. Promedios móviles
4. Índices estacionales
5. Métodos de referencia (naive, seasonal naive)
6. Validación con MAE, RMSE, SMAPE
7. Pronóstico con AutoTS
8. Análisis de incertidumbre
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
    page_title="Series de Tiempo - Estadística Aplicada",
    page_icon="🕐",
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

st.markdown("# 🕐 Módulo: Series de Tiempo")
st.markdown("**Analiza, descompón y pronostica fenómenos temporales**")

st.markdown("---")

# Estado: EN CONSTRUCCIÓN
st.info("""
🚧 **PÁGINA EN CONSTRUCCIÓN** 

Esta página está siendo desarrollada. Los temas se agregarán en las próximas versiones.
Mientras tanto, puedes analizar series manualmente con clima_mensual.csv y muestra_series24.csv.
""")

st.markdown("---")

st.markdown("## 📋 Temas a Implementar")

st.markdown("""
### 1. 📊 Componentes de una Serie de Tiempo

**Aditivo:** Y_t = T_t + S_t + R_t
- T_t: Tendencia (dirección general a LP)
- S_t: Estacionalidad (patrón repetitivo)
- R_t: Ruido (variación aleatoria)

**Multiplicativo:** Y_t = T_t × S_t × R_t
- Usado cuando amplitud de estacionalidad varía con tendencia
- Ejemplo: Demanda que crece y también es estacional

**Ejemplo: Precipitación Mensual (2015-2025)**
- T: Leve crecimiento/descenso en LP
- S: Bimodal (abr-may y sep-nov altas, dic-mar bajas)
- R: Variabilidad mes a mes

### 2. 🔨 Descomposición Clásica

**Método Aditivo:**
1. Calcular T con promedio móvil de 12 meses
2. Calcular (Y - T) → S + R
3. Promediar por mes → S
4. R = Y - T - S

**Método Multiplicativo:**
1. Calcular T con promedio móvil
2. Y / T → S × R
3. Promediar por mes → S
4. R = (Y / T) / S

**Visualización:**
- Original | Tendencia | Estacionalidad | Residuos (4 gráficas)

### 3. 📈 Promedios Móviles

**Simple (MA):**
- Y_t^(ma) = (Y_(t-k) + ... + Y_t) / (2k+1)
- Orden k: típicamente 12 para datos mensuales
- Suaviza series eliminando ruido

**Ponderado (WMA):**
- Pesos mayores para observaciones recientes
- WMA = Σ(w_i × Y_(t-i)) / Σw_i
- Más responsivo que MA simple

**Exponencial (EMA):**
- EMA_t = α·Y_t + (1-α)·EMA_(t-1)
- α ∈ (0,1): Factor de suavización
- Mejor para pronósticos corto plazo

### 4. 📊 Índices Estacionales

**Factor Estacional para mes m:**
- S_m = (Promedio de Y en mes m) / (Media general)
- S_m = 1 → Mes con comportamiento promedio
- S_m > 1 → Mes por encima del promedio
- S_m < 1 → Mes por debajo del promedio

**Ejemplo (Precipitación):**
- S_abril = 206 / 140 ≈ 1.47 → Abril es 47% más lluvioso que promedio
- S_diciembre = 55 / 140 ≈ 0.39 → Diciembre es 61% más seco

**Verificación:** Σ S_m = 12 (para método aditivo normalizado)

### 5. 🎯 Métodos de Referencia (Benchmark)

**Naive:**
- Ŷ_(t+1) = Y_t (último valor observado)
- Útil para evaluar si modelo propuesto es mejor

**Seasonal Naive:**
- Ŷ_(t+1) = Y_(t-s) (valor de hace 1 año/período)
- Mantiene estacionalidad constante

**Media Móvil:**
- Ŷ_(t+1) = promedio de últimos k valores
- Captura tendencia reciente

### 6. 📏 Métricas de Validación

**MAE (Error Absoluto Medio):**
- MAE = Σ|Y_t - Ŷ_t| / n
- Unidades: mismas que Y
- Fácil interpretación

**RMSE (Raíz del Error Cuadrático Medio):**
- RMSE = √(Σ(Y_t - Ŷ_t)² / n)
- Penaliza errores grandes más que MAE
- Sensible a outliers

**MAPE (Error Porcentual Absoluto Medio):**
- MAPE = 100 × Σ|Y_t - Ŷ_t| / |Y_t| / n
- Porcentaje → Comparable entre series

**SMAPE (Simétrico MAPE):**
- SMAPE = 100 × Σ(2|Y_t - Ŷ_t| / (|Y_t| + |Ŷ_t|)) / n
- Mejor cuando Y_t cerca de cero
- Rango: 0-100%

### 7. 🔮 Pronóstico con AutoTS

**AutoTS:**
- Selección automática de modelo (ARIMA, Prophet, etc.)
- Ajusta múltiples modelos y elige mejor por métrica
- Opción: early_stopping para evitar overfitting
- Genera pronósticos con intervalos de confianza

**Entrada:**
- Serie temporal (muestra_series24.csv)
- Período de entrenamiento: 18 meses
- Período de validación: 6 meses
- Pronóstico: siguientes 6 meses

**Salida:**
- Modelo seleccionado, parámetros, métrica de validación
- Gráfico con histórico + pronóstico
- Intervalo de confianza (95%)

### 8. 📊 Análisis de Incertidumbre

**Intervalo de Confianza del Pronóstico:**
- Rango probable del valor futuro (95% confianza)
- Aumenta con horizonte de pronóstico
- Refleja variabilidad de residuos históricos

**Sensibilidad a Parámetros:**
- Variación en resultados según k (MA), α (EMA)
- Validación cruzada: múltiples divisiones train/test

**Cambios de Régimen:**
- ¿Patrón consistente o cambios en estacionalidad?
- Detección de puntos de quiebre (change points)
""")

st.markdown("---")

st.markdown("""
### 🌾 Aplicaciones Agrícolas

**Precipitación Mensual (2015-2025, 132 meses):**
- Identificar componentes: Tendencia, ciclos estacionales, ruido
- Régimen bimodal: abr-may altas, dic-mar bajas, sep-nov altas
- Pronóstico de lluvia próximos 6 meses (muestra_series24.csv)
- Riesgo de sequía/exceso de agua

**Temperatura:**
- Tendencia creciente (cambio climático)
- Ciclo anual predecible
- Pronóstico para planificación agrícola

**Secado de Capa Delgada:**
- No es serie temporal tradicional (no hay repetición temporal)
- Pero sí hay componentes: Tendencia exponencial decreciente, ruido
- Usar regresión con modelo MR = exp(-k·t^n)
""")

st.markdown("---")

st.markdown("""
### ✏️ Habilidades que Practicarás

- **Python:** Statsmodels (descomposition, seasonal_decompose), AutoTS, Pandas
- **Estadística:** Tendencia, estacionalidad, ruido, promedios móviles
- **Visualización:** Gráficas temporales, componentes, pronósticos
- **Validación:** MAE, RMSE, SMAPE, validación cruzada
- **Pronóstico:** AutoTS, intervalos de confianza, análisis de incertidumbre
- **Interpretación:** Patrones agrícolas, planificación hídrica, riesgo climático
""")
