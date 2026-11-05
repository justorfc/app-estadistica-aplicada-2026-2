"""
pages/4_Regresion.py - Análisis de Regresión Lineal Simple y Múltiple

Secciones:
1. Correlación (Pearson/Spearman)
2. Regresión lineal simple (datos completos)
3. Diagnóstico de residuos
4. Predicción (slider + input libre)
5. Regresión múltiple (preview)
6. Verificación manual (8 parcelas)

Usa módulos:
- src/regresion.py: calculo_manual, ajustar_rls, matriz_correlacion, etc.
- datos/parcelas.csv: 100 parcelas
- datos/muestra_reg8.csv: 8 parcelas para verificación manual
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Agregar carpeta src al path
ruta_src = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(ruta_src))

from regresion import (
    matriz_correlacion, calculo_manual, ajustar_rls,
    predecir, diagnostico_residuos, ajustar_multiple
)
from datos import tarjeta_estudiante

# ============================================================================
# Configuración
# ============================================================================

st.set_page_config(
    page_title="Regresión - Estadística Aplicada",
    page_icon="📉",
    layout="wide"
)

sns.set_style("darkgrid")

# ============================================================================
# Barra lateral
# ============================================================================

with st.sidebar:
    tarjeta_estudiante(ubicacion='sidebar')

# ============================================================================
# Título
# ============================================================================

st.markdown("# 📉 Regresión Lineal Simple y Múltiple")
st.markdown("Análisis de relaciones lineales: correlación, ajuste de modelos, diagnóstico y predicción")

st.markdown("---")

# Cargar datos
@st.cache_data
def cargar_datos():
    df_completo = pd.read_csv('datos/parcelas.csv')
    df_muestra = pd.read_csv('datos/muestra_reg8.csv')
    return df_completo, df_muestra

df_completo, df_muestra = cargar_datos()

# ============================================================================
# SECCIÓN 1: CORRELACIÓN
# ============================================================================

st.markdown("## 1️⃣ Correlación")
st.markdown("**Matriz de correlación de variables numéricas con rendimiento**")

col1, col2 = st.columns([1, 3])
with col1:
    metodo_corr = st.radio("Método:", ["Pearson", "Spearman"], label_visibility="collapsed")
    
with col2:
    st.write("")

# Calcular correlación
metodo_corr_lower = metodo_corr.lower()
corr_matrix = matriz_correlacion(df_completo, metodo=metodo_corr_lower)

# Mapa de calor (heatmap)
fig_heatmap, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            cbar_kws={'label': f'Correlación {metodo_corr}'}, ax=ax, square=True)
plt.title(f"Matriz de Correlación ({metodo_corr})")
st.pyplot(fig_heatmap)

# Tabla de correlación con rendimiento
st.markdown("### Correlación de cada variable con Rendimiento (ordenada por |r|)")
corr_rend = corr_matrix['rendimiento'].drop('rendimiento').sort_values(key=abs, ascending=False)
df_corr_table = pd.DataFrame({
    'Variable': corr_rend.index,
    f'Correlación ({metodo_corr})': corr_rend.values
})
st.dataframe(df_corr_table, use_container_width=True, hide_index=True)

st.info("""
💡 **Nota**: La correlación mide asociación lineal, NO causalidad.
- r > 0: Relación positiva (aumentan juntas)
- r < 0: Relación negativa (aumentan en direcciones opuestas)
- |r| > 0.7: Correlación fuerte
- |r| < 0.3: Correlación débil
""")

st.markdown("---")

# ============================================================================
# SECCIÓN 2: REGRESIÓN LINEAL SIMPLE
# ============================================================================

st.markdown("## 2️⃣ Regresión Lineal Simple")
st.markdown("**Modelo: Rendimiento = β₀ + β₁·X**")

col1, col2 = st.columns(2)
with col1:
    # Selector de variable X
    vars_numericas = df_completo.select_dtypes(include=[np.number]).columns.tolist()
    if 'rendimiento' in vars_numericas:
        vars_numericas.remove('rendimiento')
    
    x_var = st.selectbox("Variable independiente (X):", vars_numericas, 
                         index=0 if 'lamina_riego' not in vars_numericas else vars_numericas.index('lamina_riego'),
                         label_visibility="visible")

with col2:
    st.write("")  # Espaciador

# Ajustar modelo
x_data = df_completo[x_var].dropna()
y_data = df_completo.loc[x_data.index, 'rendimiento']
mask = ~(x_data.isna() | y_data.isna())
x_data = x_data[mask]
y_data = y_data[mask]

modelo = ajustar_rls(pd.DataFrame({x_var: x_data, 'rendimiento': y_data}), x_var, 'rendimiento')

# Gráfico de dispersión + recta ajustada
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x_data, y_data, alpha=0.6, s=50, edgecolors='black', linewidth=0.5, label='Datos observados')

# Recta ajustada
x_rango = np.linspace(x_data.min(), x_data.max(), 100)
b0 = modelo.params['Intercept']
b1 = modelo.params[x_var]
y_pred = b0 + b1 * x_rango
ax.plot(x_rango, y_pred, 'r-', linewidth=2.5, label=f'Recta ajustada: Ŷ = {b0:.2f} + {b1:.4f}·X')

ax.set_xlabel(f'{x_var} (unidad original)', fontsize=11)
ax.set_ylabel('Rendimiento (ton/ha)', fontsize=11)
ax.set_title(f'Regresión Lineal: Rendimiento vs {x_var}', fontsize=13, fontweight='bold')
ax.legend(fontsize=10, loc='best')
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Ecuación con unidades
st.markdown(f"### Ecuación del modelo:")
unidades_x = "mm" if x_var == "lamina_riego" else "kg/ha" if x_var == "dosis_N" else "%"
st.latex(f"\\text{{Rendimiento (t/ha)}} = {b0:.4f} + {b1:.6f} \\times \\text{{{x_var} ({unidades_x})}}")

# Métricas en st.metric
col1, col2, col3 = st.columns(3)
with col1:
    r = np.corrcoef(x_data, y_data)[0, 1]
    st.metric(label="r (correlación)", value=f"{r:.4f}")
with col2:
    r2 = modelo.rsquared
    st.metric(label="R² (determinación)", value=f"{r2:.4f}")
with col3:
    rse = np.sqrt(modelo.mse_resid)
    st.metric(label="RSE (error estándar)", value=f"{rse:.4f} ton/ha")

# Tabla de coeficientes
st.markdown("### Tabla de Coeficientes")
coef_tabla = pd.DataFrame({
    'Variable': ['Intercepto', x_var],
    'Coeficiente': [modelo.params['Intercept'], modelo.params[x_var]],
    'Error Est.': [modelo.bse['Intercept'], modelo.bse[x_var]],
    't': [modelo.tvalues['Intercept'], modelo.tvalues[x_var]],
    'p-valor': [modelo.pvalues['Intercept'], modelo.pvalues[x_var]],
    'IC 95% Inferior': [modelo.conf_int().loc['Intercept', 0], modelo.conf_int().loc[x_var, 0]],
    'IC 95% Superior': [modelo.conf_int().loc['Intercept', 1], modelo.conf_int().loc[x_var, 1]]
})
st.dataframe(coef_tabla, use_container_width=True, hide_index=True)

# Decisión sobre H0: β1 = 0
alpha = 0.05
p_valor_b1 = modelo.pvalues[x_var]
if p_valor_b1 < alpha:
    st.success(f"""
    ✅ **Rechazo H₀**: Existe relación significativa entre {x_var} y rendimiento (p = {p_valor_b1:.4f} < 0.05).
    
    Por cada {unidades_x} aumentado en {x_var}, el rendimiento aumenta (o disminuye) 
    aproximadamente **{abs(b1):.6f} ton/ha** en promedio.
    """)
else:
    st.warning(f"""
    ❌ **No rechazar H₀**: No hay relación significativa entre {x_var} y rendimiento (p = {p_valor_b1:.4f} ≥ 0.05).
    
    La pendiente no es significativamente diferente de cero. Los datos no proporcionan
    suficiente evidencia de una relación lineal.
    """)

st.markdown("---")

# ============================================================================
# SECCIÓN 3: DIAGNÓSTICO DE RESIDUOS
# ============================================================================

st.markdown("## 3️⃣ Diagnóstico de Residuos")
st.markdown("**Evaluación de supuestos: linealidad, normalidad y homocedasticidad**")

diag = diagnostico_residuos(modelo)
residuos = diag['residuos']
ajustados = diag['ajustados']

# Gráficos (2x2)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Residuos vs Ajustados
axes[0, 0].scatter(ajustados, residuos, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
axes[0, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
axes[0, 0].set_xlabel('Valores Ajustados')
axes[0, 0].set_ylabel('Residuos')
axes[0, 0].set_title('Residuos vs Ajustados')
axes[0, 0].grid(True, alpha=0.3)

# 2. Histograma de residuos
axes[0, 1].hist(residuos, bins=15, edgecolor='black', alpha=0.7, color='skyblue')
axes[0, 1].set_xlabel('Residuos')
axes[0, 1].set_ylabel('Frecuencia')
axes[0, 1].set_title('Histograma de Residuos')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# 3. Q-Q Plot
stats.probplot(residuos, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Gráfico Q-Q')
axes[1, 0].grid(True, alpha=0.3)

# 4. Escala-Ubicación (sqrt(|residuos estandarizados|) vs ajustados)
residuos_std = residuos / np.std(residuos)
axes[1, 1].scatter(ajustados, np.sqrt(np.abs(residuos_std)), alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
axes[1, 1].set_xlabel('Valores Ajustados')
axes[1, 1].set_ylabel('√|Residuos Estandarizados|')
axes[1, 1].set_title('Escala-Ubicación')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# Tests estadísticos
col1, col2 = st.columns(2)

with col1:
    sw_stat = diag['shapiro_stat']
    sw_pval = diag['shapiro_pvalue']
    st.markdown("### Shapiro-Wilk (Normalidad de Residuos)")
    if sw_pval > 0.05:
        st.success(f"✅ p-valor = {sw_pval:.4f} > 0.05: Residuos distribuyen normalmente")
    else:
        st.warning(f"⚠️ p-valor = {sw_pval:.4f} < 0.05: Residuos NO distribuyen normalmente")

with col2:
    bp_stat = diag['breusch_pagan_stat']
    bp_pval = diag['breusch_pagan_pvalue']
    st.markdown("### Breusch-Pagan (Homocedasticidad)")
    if bp_pval > 0.05:
        st.success(f"✅ p-valor = {bp_pval:.4f} > 0.05: Varianza constante")
    else:
        st.warning(f"⚠️ p-valor = {bp_pval:.4f} < 0.05: Varianza NO constante")

st.markdown("---")

# ============================================================================
# SECCIÓN 4: PREDICCIÓN
# ============================================================================

st.markdown("## 4️⃣ Predicción")
st.markdown("**Intervalo de confianza (para E[Y|X]) e intervalo de predicción (para Y individual)**")

col1, col2 = st.columns([2, 1])

with col1:
    x_pred_slider = st.slider(
        f"Selecciona valor de {x_var}:",
        min_value=float(x_data.min()),
        max_value=float(x_data.max()),
        value=float(x_data.mean()),
        step=1.0
    )
    
    pred_slider = predecir(modelo, x0=x_pred_slider, nivel=0.95)
    
    st.markdown(f"### Para {x_var} = {x_pred_slider:.1f} {unidades_x}:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Predicción (Ŷ)", f"{pred_slider['y_pred']:.4f} t/ha")
    with col_b:
        st.metric("IC95% Inferior", f"{pred_slider['IC_lower']:.4f} t/ha")
    with col_c:
        st.metric("IC95% Superior", f"{pred_slider['IC_upper']:.4f} t/ha")
    
    st.write(f"**Intervalo de Confianza (95% para E[Y|X]):** [{pred_slider['IC_lower']:.4f}, {pred_slider['IC_upper']:.4f}] t/ha")
    st.write(f"**Intervalo de Predicción (95% para Y):** [{pred_slider['IP_lower']:.4f}, {pred_slider['IP_upper']:.4f}] t/ha")

with col2:
    st.write("")

# Predicción libre con warning de extrapolación
st.markdown("### Predicción Libre")
x_pred_libre = st.number_input(
    f"Ingresa un valor de {x_var}:",
    value=float(x_data.mean()),
    step=1.0
)

if x_pred_libre < x_data.min() or x_pred_libre > x_data.max():
    st.warning(f"""
    ⚠️ **EXTRAPOLACIÓN**: El valor {x_pred_libre} está FUERA del rango observado [{x_data.min():.1f}, {x_data.max():.1f}].
    
    Las predicciones fuera del rango de datos son POCO CONFIABLES porque el modelo
    podría no ser lineal en esa región. Úsalas con cautela.
    """)

pred_libre = predecir(modelo, x0=x_pred_libre, nivel=0.95)
st.markdown(f"**Para {x_var} = {x_pred_libre:.1f}:**")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Predicción (Ŷ)", f"{pred_libre['y_pred']:.4f} t/ha")
with col_b:
    st.metric("IC95%", f"[{pred_libre['IC_lower']:.2f}, {pred_libre['IC_upper']:.2f}]")
with col_c:
    st.metric("IP95%", f"[{pred_libre['IP_lower']:.2f}, {pred_libre['IP_upper']:.2f}]")

st.markdown("---")

# ============================================================================
# SECCIÓN 5: REGRESIÓN MÚLTIPLE (Vista Previa)
# ============================================================================

st.markdown("## 5️⃣ Regresión Múltiple (Vista Previa)")
st.markdown("**Modelo: Rendimiento ~ Dosis_N + Lamina_Riego + Materia_Organica + pH**")

modelo_mult = ajustar_multiple(
    df_completo, 'rendimiento',
    ['dosis_N', 'lamina_riego', 'materia_organica', 'ph']
)

# Coeficientes
st.markdown("### Coeficientes")
coef_mult = pd.DataFrame({
    'Variable': modelo_mult.params.index,
    'Coeficiente': modelo_mult.params.values,
    'Error Est.': modelo_mult.bse.values,
    't': modelo_mult.tvalues.values,
    'p-valor': modelo_mult.pvalues.values
})
st.dataframe(coef_mult, use_container_width=True, hide_index=True)

# R² y R² ajustado
col1, col2 = st.columns(2)
with col1:
    st.metric("R²", f"{modelo_mult.rsquared:.4f}")
with col2:
    st.metric("R² Ajustado", f"{modelo_mult.rsquared_adj:.4f}")

st.info("""
💡 **R² Ajustado**: Penaliza variables adicionales que no mejoran significativamente el ajuste.
Mejor para comparar modelos con diferente número de predictores.
""")

st.markdown("---")

# ============================================================================
# SECCIÓN 6: VERIFICACIÓN MANUAL (8 parcelas)
# ============================================================================

st.markdown("## 6️⃣ Verificación del Cálculo a Mano (8 Parcelas)")
st.markdown("**Comparación entre cálculo manual y todos los datos**")

# Preparar datos de muestra
x_muestra = df_muestra['lamina_riego'].values
y_muestra = df_muestra['rendimiento'].values

# Cálculo manual
resultado_manual = calculo_manual(x_muestra, y_muestra)

# Tabla de desviaciones y productos cruzados
st.markdown("### Tabla de Cálculos (Muestra de 8 Parcelas)")
tabla_calc = pd.DataFrame({
    'Parcela': df_muestra['parcela'],
    'Lámina (mm)': x_muestra,
    'Rendimiento': y_muestra,
    'x - x̄': x_muestra - resultado_manual['media_x'],
    'y - ȳ': y_muestra - resultado_manual['media_y'],
    'Ŷ Ajustado': resultado_manual['y_ajustado'],
    'Residuo (e)': resultado_manual['residuos']
})
st.dataframe(tabla_calc, use_container_width=True, hide_index=True)

# Tabla de resultados de cálculo_manual
st.markdown("### Resultados del Cálculo Manual (4 decimales, b1 en 6)")
res_tabla = pd.DataFrame({
    'Estadístico': [
        'n', 'x̄ (media)', 'ȳ (media)', 'Sxx', 'Syy', 'Sxy',
        'r (Pearson)', 'b1 (pendiente)', 'b0 (intercepto)',
        'R²', 'RSE', 'SE(b1)', 't', 'p-valor',
        'IC95% b1 inferior', 'IC95% b1 superior'
    ],
    'Valor': [
        f"{resultado_manual['n']}",
        f"{resultado_manual['media_x']:.4f}",
        f"{resultado_manual['media_y']:.4f}",
        f"{resultado_manual['Sxx']:.4f}",
        f"{resultado_manual['Syy']:.4f}",
        f"{resultado_manual['Sxy']:.4f}",
        f"{resultado_manual['r_pearson']:.4f}",
        f"{resultado_manual['b1']:.6f}",
        f"{resultado_manual['b0']:.4f}",
        f"{resultado_manual['R2']:.4f}",
        f"{resultado_manual['RSE']:.4f}",
        f"{resultado_manual['SE_b1']:.4f}",
        f"{resultado_manual['t_b1']:.4f}",
        f"{resultado_manual['p_valor']:.4f}",
        f"{resultado_manual['IC_b1_lower']:.6f}",
        f"{resultado_manual['IC_b1_upper']:.6f}"
    ]
})
st.dataframe(res_tabla, use_container_width=True, hide_index=True)

# Gráfico de muestra con recta
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x_muestra, y_muestra, s=80, alpha=0.7, edgecolors='black', linewidth=1, label='8 parcelas')

# Recta de muestra
x_rango_muestra = np.linspace(x_muestra.min(), x_muestra.max(), 100)
y_pred_muestra = resultado_manual['b0'] + resultado_manual['b1'] * x_rango_muestra
ax.plot(x_rango_muestra, y_pred_muestra, 'r-', linewidth=2.5,
        label=f"Ŷ = {resultado_manual['b0']:.4f} + {resultado_manual['b1']:.6f}·X")

ax.set_xlabel('Lámina de Riego (mm)', fontsize=11)
ax.set_ylabel('Rendimiento (ton/ha)', fontsize=11)
ax.set_title('Regresión Manual (8 Parcelas)', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# Comparación: Muestra (8) vs Datos Completos
st.markdown("### Comparación: Muestra (8 Parcelas) vs Datos Completos (100 Parcelas)")

resultado_completo = calculo_manual(df_completo['lamina_riego'].dropna().values,
                                     df_completo.loc[df_completo['lamina_riego'].dropna().index, 'rendimiento'].values)

comparacion = pd.DataFrame({
    'Estadístico': ['b1 (pendiente)', 'r (correlación)', 'R²', 't', 'p-valor'],
    'Muestra (n=8)': [
        f"{resultado_manual['b1']:.6f}",
        f"{resultado_manual['r_pearson']:.4f}",
        f"{resultado_manual['R2']:.4f}",
        f"{resultado_manual['t_b1']:.4f}",
        f"{resultado_manual['p_valor']:.4f}"
    ],
    'Datos Completos (n=116)': [
        f"{resultado_completo['b1']:.6f}",
        f"{resultado_completo['r_pearson']:.4f}",
        f"{resultado_completo['R2']:.4f}",
        f"{resultado_completo['t_b1']:.4f}",
        f"{resultado_completo['p_valor']:.4f}"
    ]
})

st.dataframe(comparacion, use_container_width=True, hide_index=True)

st.info("""
💡 **Observación**: Con n=8 (pequeña muestra) los resultados tienen mayor variabilidad.
Con n=116 (datos completos) la estimación es más estable y confiable.
Esto ilustra por qué las muestras grandes son preferibles en regresión.
""")

st.markdown("---")

st.success("✅ Análisis de regresión completado.")

