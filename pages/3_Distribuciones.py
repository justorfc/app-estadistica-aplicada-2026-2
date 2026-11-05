"""
Página 3: Distribuciones de Probabilidad para Máximos Anuales
Selección del mejor modelo estadístico con criterios de información y bondad de ajuste.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Importar funciones del módulo
from src.distribuciones import (
    ajustar, log_verosimilitud, criterios_informacion,
    bondad_ajuste, tabla_comparativa, posiciones_graficas,
    cuantil_retorno, riesgo_falla, bootstrap_cuantil,
    gumbel_momentos, DISTRIBUCIONES_CANDIDATAS
)

# Configuración de estilos
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

st.set_page_config(page_title="Distribuciones", layout="wide")

# ============================================================================
# CARGA DE DATOS Y CACHE
# ============================================================================

@st.cache_data
def cargar_datos():
    """Carga datos de precipitación máxima anual."""
    df_pmax = pd.read_csv('datos/precip_max_anual.csv')
    df_dist10 = pd.read_csv('datos/muestra_dist10.csv')
    return df_pmax, df_dist10

df_pmax, df_dist10 = cargar_datos()
datos_pmax = df_pmax['pmax24h_mm'].dropna().values
datos_anios = df_pmax['año'].dropna().values if 'año' in df_pmax.columns else np.arange(len(datos_pmax))

# ============================================================================
# FUNCIÓN CACHE PARA TABLA COMPARATIVA
# ============================================================================

@st.cache_data
def calcular_tabla_comparativa(datos, n_mc):
    """Calcula tabla comparativa con cache."""
    return tabla_comparativa(datos, n_mc=n_mc)

# ============================================================================
# ENCABEZADO
# ============================================================================

st.title("📊 Distribuciones de Probabilidad")
st.markdown("Selección del mejor modelo para máximos anuales de precipitación (período de retorno)")

# ============================================================================
# 1. LOS DATOS
# ============================================================================

with st.container():
    st.header("1️⃣ Los Datos: Serie de Máximos Anuales")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras por año
        fig, ax = plt.subplots(figsize=(12, 5))
        años_label = [str(int(a)) for a in datos_anios]
        ax.bar(años_label, datos_pmax, color='steelblue', edgecolor='navy', alpha=0.7)
        ax.set_xlabel('Año', fontsize=11, fontweight='bold')
        ax.set_ylabel('Precipitación Máxima 24h (mm)', fontsize=11, fontweight='bold')
        ax.set_title('Precipitación Máxima Anual', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Resumen numérico
        st.subheader("Resumen Estadístico")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("N (años)", len(datos_pmax))
            st.metric("Media (mm)", f"{np.mean(datos_pmax):.2f}")
            st.metric("Mín (mm)", f"{np.min(datos_pmax):.2f}")
        with col_b:
            st.metric("Desv.Est. (mm)", f"{np.std(datos_pmax, ddof=1):.2f}")
            st.metric("Mediana (mm)", f"{np.median(datos_pmax):.2f}")
            st.metric("Máx (mm)", f"{np.max(datos_pmax):.2f}")
    
    # Histograma
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.hist(datos_pmax, bins=15, color='steelblue', edgecolor='black', alpha=0.7)
    ax.axvline(np.mean(datos_pmax), color='red', linestyle='--', linewidth=2, label=f'Media = {np.mean(datos_pmax):.2f}')
    ax.axvline(np.median(datos_pmax), color='green', linestyle='--', linewidth=2, label=f'Mediana = {np.median(datos_pmax):.2f}')
    ax.set_xlabel('Precipitación Máxima 24h (mm)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
    ax.set_title('Distribución de Máximos Anuales', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================================
# 2. CANDIDATAS Y AJUSTE
# ============================================================================

st.header("2️⃣ Distribuciones Candidatas y Ajuste por MV")

col1, col2 = st.columns([1, 2])

with col1:
    # Multiselect de distribuciones
    dist_disponibles = list(DISTRIBUCIONES_CANDIDATAS.keys())
    dist_seleccionadas = st.multiselect(
        "Selecciona distribuciones para visualizar:",
        dist_disponibles,
        default=dist_disponibles
    )

with col2:
    st.info("""
    **Respaldo teórico para máximos anuales:**
    
    - 🏆 **Gumbel**: Teorema de valores extremos (máximos independientes, cola derecha exponencial)
    - 🏆 **GEV**: Generalización que captura diferentes comportamientos extremales
    - ⭐ **Lognormal, Gamma, Weibull**: Distribuciones asimétricas, competidoras
    - ✓ **Normal**: Baseline de referencia (simetría, no ideal para extremos)
    """)

# Calcular ajustes y mostrar histograma con densidades
if dist_seleccionadas:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Histograma de datos
    ax.hist(datos_pmax, bins=15, density=True, color='lightgray', edgecolor='black', 
            alpha=0.6, label='Datos observados')
    
    # Colores para las distribuciones
    colores = plt.cm.tab10(np.linspace(0, 1, len(dist_seleccionadas)))
    
    # Rango para las curvas de densidad
    x_range = np.linspace(datos_pmax.min() - 5, datos_pmax.max() + 10, 200)
    
    for dist_nombre, color in zip(dist_seleccionadas, colores):
        try:
            params, _ = ajustar(datos_pmax, dist_nombre)
            dist = DISTRIBUCIONES_CANDIDATAS[dist_nombre]
            
            if dist_nombre in ['Lognormal', 'Gamma', 'Weibull']:
                # loc fijo en 0
                y_vals = dist.pdf(x_range, params[0], loc=0, scale=params[2])
            else:
                y_vals = dist.pdf(x_range, *params)
            
            ax.plot(x_range, y_vals, linewidth=2.5, color=color, label=dist_nombre)
        except Exception as e:
            st.warning(f"Error al ajustar {dist_nombre}: {e}")
    
    ax.set_xlabel('Precipitación Máxima 24h (mm)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Densidad de Probabilidad', fontsize=11, fontweight='bold')
    ax.set_title('Histograma con Densidades Ajustadas', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

# ============================================================================
# 3. BONDAD DE AJUSTE
# ============================================================================

st.header("3️⃣ Pruebas de Bondad de Ajuste")

# Slider para n_mc (número de simulaciones Monte Carlo)
col1, col2 = st.columns([1, 3])
with col1:
    n_mc = st.slider(
        "Simulaciones Monte Carlo (n_mc):",
        min_value=99,
        max_value=499,
        value=199,
        step=50,
        help="Mayor valor = más precisión pero más tiempo"
    )

with col2:
    st.info("Los valores p se calculan por Monte Carlo, lo que corrige el problema de Lilliefors.")

# Calcular tabla comparativa (con cache)
tabla = calcular_tabla_comparativa(datos_pmax, n_mc)

# Tabla de bondad de ajuste (K-S y Anderson-Darling)
st.subheader("Tabla: Kolmogorov-Smirnov y Anderson-Darling")
tabla_ba = tabla[['Distribución', 'KS_stat', 'KS_pvalue_mc', 'KS_pvalue_naive', 
                   'AD_stat', 'AD_pvalue_mc']].copy()
tabla_ba.columns = ['Distribución', 'KS stat', 'KS valor p (MC)', 'KS valor p (ingenuo)', 
                    'A-D stat', 'A-D valor p (MC)']

# Formatear números
for col in ['KS stat', 'KS valor p (MC)', 'KS valor p (ingenuo)', 'A-D stat', 'A-D valor p (MC)']:
    tabla_ba[col] = tabla_ba[col].apply(lambda x: f"{x:.4f}")

st.dataframe(tabla_ba, use_container_width=True, hide_index=True)

# Q-Q plots para cada distribución
st.subheader("Gráficos Q-Q para Cada Distribución")

pos = posiciones_graficas(datos_pmax)
datos_ord = pos['datos_ord']
gringorten = pos['gringorten']

# Crear cuadrícula de Q-Q plots
n_dists = len(tabla)
n_cols = 3
n_rows = (n_dists + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4*n_rows))
axes = axes.flatten()

for idx, (_, row) in enumerate(tabla.iterrows()):
    dist_nombre = row['Distribución']
    params = row['params_tuple']
    dist = DISTRIBUCIONES_CANDIDATAS[dist_nombre]
    
    try:
        # Cuantiles teóricos
        if dist_nombre in ['Lognormal', 'Gamma', 'Weibull']:
            q_teor = dist.ppf(gringorten, params[0], loc=0, scale=params[2])
        else:
            q_teor = dist.ppf(gringorten, *params)
        
        ax = axes[idx]
        ax.scatter(q_teor, datos_ord, alpha=0.6, s=60, edgecolor='navy')
        
        # Línea de referencia (45 grados)
        min_val = min(q_teor.min(), datos_ord.min())
        max_val = max(q_teor.max(), datos_ord.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Referencia')
        
        ax.set_xlabel('Cuantiles Teóricos (mm)', fontsize=10)
        ax.set_ylabel('Cuantiles Observados (mm)', fontsize=10)
        ax.set_title(f'{dist_nombre}', fontsize=11, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9)
    except Exception as e:
        axes[idx].text(0.5, 0.5, f"Error: {dist_nombre}", ha='center', va='center',
                      transform=axes[idx].transAxes)

# Eliminar ejes vacíos
for idx in range(n_dists, len(axes)):
    fig.delaxes(axes[idx])

plt.tight_layout()
st.pyplot(fig)

# ============================================================================
# 4. CRITERIOS DE INFORMACIÓN
# ============================================================================

st.header("4️⃣ Criterios de Información: AIC, BIC, AICc")

# Tabla de criterios ordenada por AIC
st.subheader("Tabla Comparativa (Ordenada por AIC)")
tabla_crit = tabla[['Distribución', 'k', 'ℓ (log-vero)', 'AIC', 'BIC', 'AICc', 
                     'ΔAIC', 'Interpretación ΔAIC', 'Rechaza H₀ (KS 5%)', 
                     'Rechaza H₀ (AD 5%)']].copy()

tabla_crit_display = tabla_crit.copy()
for col in ['ℓ (log-vero)', 'AIC', 'BIC', 'AICc', 'ΔAIC']:
    tabla_crit_display[col] = tabla_crit_display[col].apply(lambda x: f"{x:.2f}")

st.dataframe(tabla_crit_display, use_container_width=True, hide_index=True)

# Gráfico de barras de ΔAIC
fig, ax = plt.subplots(figsize=(10, 5))
colores_daic = ['green' if x < 2 else 'yellow' if x < 7 else 'red' 
                for x in tabla['ΔAIC'].values]
ax.bar(tabla['Distribución'], tabla['ΔAIC'], color=colores_daic, edgecolor='black', alpha=0.7)
ax.axhline(y=2, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='ΔAIC = 2')
ax.axhline(y=7, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='ΔAIC = 7')
ax.set_ylabel('ΔAIC = AIC - AIC_mín', fontsize=11, fontweight='bold')
ax.set_title('Comparación de Criterios de Información', fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

# Recomendación del modelo con semáforo
st.subheader("🎯 Modelo Recomendado")

mejor_dist = tabla.iloc[0]['Distribución']
mejor_aic = tabla.iloc[0]['AIC']
mejor_daic = tabla.iloc[0]['ΔAIC']
mejor_ks_pval = tabla.iloc[0]['KS_pvalue_mc']
mejor_ad_pval = tabla.iloc[0]['AD_pvalue_mc']

# Semáforo
respaldo_fisico = mejor_dist in ['Gumbel', 'GEV']
qq_aceptable = mejor_ks_pval > 0.05  # No rechaza H0
no_rechaza_ad = mejor_ad_pval > 0.05
daic_pequeno = mejor_daic < 2

col1, col2, col3, col4 = st.columns(4)

with col1:
    color_i = "🟢" if respaldo_fisico else "🟡"
    st.metric("Respaldo físico", color_i + (" Sí" if respaldo_fisico else " No"))

with col2:
    color_ii = "🟢" if qq_aceptable else "🟠"
    st.metric("Q-Q aceptable", color_ii + (" Sí" if qq_aceptable else " No"))

with col3:
    color_iii = "🟢" if no_rechaza_ad else "🟠"
    st.metric("No rechaza H₀ (A-D)", color_iii + (" Sí" if no_rechaza_ad else " No"))

with col4:
    color_iv = "🟢" if daic_pequeno else "🟡"
    st.metric("ΔAIC pequeño", color_iv + (" Sí" if daic_pequeno else " No"))

if respaldo_fisico and qq_aceptable and no_rechaza_ad and daic_pequeno:
    st.success(f"""
    ✅ **Recomendación: {mejor_dist}**
    
    - **ΔAIC = {mejor_daic:.2f}** (soporte sustancial)
    - **K-S p-valor = {mejor_ks_pval:.4f}** (no rechaza H₀)
    - **A-D p-valor = {mejor_ad_pval:.4f}** (excelente)
    - **AIC = {mejor_aic:.2f}**
    
    Modelo robusto y bien fundamentado teóricamente.
    """)
else:
    st.warning(f"""
    ⚠️ **Seleccionado: {mejor_dist}** (por criterio de información)
    
    Aunque {mejor_dist} es óptimo por AIC, revisar los otros criterios.
    """)

# ============================================================================
# 5. PERÍODO DE RETORNO Y DISEÑO
# ============================================================================

st.header("5️⃣ Período de Retorno y Diseño de Infraestructura")

# Tabla de cuantiles para cada distribución
st.subheader("Tabla: Cuantiles de Período de Retorno (x_T)")

periodos_retorno = [2, 5, 10, 25, 50, 100]
data_cuantiles = []

for _, row in tabla.iterrows():
    dist_nombre = row['Distribución']
    params = row['params_tuple']
    fila = {'Distribución': dist_nombre}
    
    try:
        for T in periodos_retorno:
            x_T = cuantil_retorno(dist_nombre, params, T)
            fila[f'T={T}'] = f"{x_T:.2f}"
    except:
        fila.update({f'T={T}': '—' for T in periodos_retorno})
    
    data_cuantiles.append(fila)

df_cuantiles = pd.DataFrame(data_cuantiles)
st.dataframe(df_cuantiles, use_container_width=True, hide_index=True)

# Gráfico en papel de Gumbel (variable reducida)
st.subheader("Gráfico en Papel de Gumbel")

fig, ax = plt.subplots(figsize=(12, 6))

# Variable reducida y = -ln(-ln(1 - 1/T))
periodo_vals = np.array([1.5, 2, 3, 5, 10, 25, 50, 100, 200, 500, 1000])
y_vals = -np.log(-np.log(1 - 1/periodo_vals))

# Datos con posición de Gringorten
pos = posiciones_graficas(datos_pmax)
y_gringorten = -np.log(-np.log(1 - pos['gringorten']))

ax.scatter(y_gringorten, pos['datos_ord'], s=70, alpha=0.7, edgecolor='navy', 
           color='steelblue', label='Datos observados (Gringorten)', zorder=3)

# Rectas de las distribuciones ajustadas
for _, row in tabla.iterrows():
    dist_nombre = row['Distribución']
    params = row['params_tuple']
    
    try:
        x_cuantiles = cuantil_retorno(dist_nombre, params, periodo_vals)
        ax.plot(y_vals, x_cuantiles, linewidth=2, label=dist_nombre, alpha=0.8)
    except:
        pass

ax.set_xlabel('Variable Reducida: -ln(-ln(1 - 1/T))', fontsize=11, fontweight='bold')
ax.set_ylabel('Precipitación Máxima 24h (mm)', fontsize=11, fontweight='bold')
ax.set_title('Papel de Gumbel: Período de Retorno', fontsize=12, fontweight='bold')

# Eje secundario con valores de T
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2_ticks_pos = y_vals
ax2_ticks_labels = [f'{int(T)}' for T in periodo_vals]
ax2.set_xticks(ax2_ticks_pos[::2])
ax2.set_xticklabels(ax2_ticks_labels[::2])
ax2.set_xlabel('Período de Retorno T (años)', fontsize=11, fontweight='bold')

ax.legend(loc='upper left', fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

# Intervalo de confianza bootstrap para un T elegido
st.subheader("Intervalo de Confianza Bootstrap al 95%")

col1, col2 = st.columns([1, 2])

with col1:
    T_seleccionado = st.selectbox(
        "Período de retorno (años):",
        periodos_retorno,
        index=2  # T=10 por defecto
    )

with col2:
    # Calcular IC para la mejor distribución
    mejor_dist_nombre = tabla.iloc[0]['Distribución']
    mejor_params = tabla.iloc[0]['params_tuple']
    
    boot_result = bootstrap_cuantil(datos_pmax, mejor_dist_nombre, T_seleccionado, B=500)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("x_T (estimado)", f"{boot_result['x_T']:.2f} mm")
    with col_b:
        st.metric("Límite inferior (2.5%)", f"{boot_result['ic_lower']:.2f} mm")
    with col_c:
        st.metric("Límite superior (97.5%)", f"{boot_result['ic_upper']:.2f} mm")

# Visualización del IC bootstrap
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(boot_result['muestras_bootstrap'], bins=30, color='steelblue', 
        edgecolor='black', alpha=0.7, density=True)
ax.axvline(boot_result['x_T'], color='red', linestyle='-', linewidth=2, 
          label=f'Estimado = {boot_result["x_T"]:.2f}')
ax.axvline(boot_result['ic_lower'], color='green', linestyle='--', linewidth=2, 
          label=f'IC 95%: [{boot_result["ic_lower"]:.2f}, {boot_result["ic_upper"]:.2f}]')
ax.axvline(boot_result['ic_upper'], color='green', linestyle='--', linewidth=2)
ax.set_xlabel('Cuantil x_T (mm)', fontsize=11, fontweight='bold')
ax.set_ylabel('Densidad', fontsize=11, fontweight='bold')
ax.set_title(f'Distribución Bootstrap para T = {T_seleccionado} años', fontsize=12, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

# Calculadora de riesgo
st.subheader("Calculadora de Riesgo de Falla")

col1, col2 = st.columns(2)

with col1:
    T_diseno = st.number_input(
        "Período de retorno de diseño (años):",
        min_value=1,
        max_value=500,
        value=100,
        step=5,
        help="Período para el que se diseña la infraestructura"
    )

with col2:
    N_vida = st.number_input(
        "Vida útil de la obra (años):",
        min_value=1,
        max_value=100,
        value=25,
        step=1,
        help="Horizonte de tiempo esperado de funcionamiento"
    )

riesgo_pct = riesgo_falla(T_diseno, N_vida) * 100

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("R = 1 - (1 - 1/T)^N", f"{riesgo_pct:.2f}%")
with col_b:
    st.metric("Probabilidad de excedencia", f"{1/T_diseno*100:.2f}% anual")
with col_c:
    st.metric("Probabilidad de NO excedencia", f"{(1 - 1/T_diseno)*100:.2f}% anual")

# Tabla de riesgos para diferentes N
st.write(f"**Riesgos de falla (%) en N años para T = {T_diseno} años:**")
n_valores = [5, 10, 25, 50, 100]
riesgos = [riesgo_falla(T_diseno, N) * 100 for N in n_valores]

df_riesgos = pd.DataFrame({
    'Vida útil (años)': n_valores,
    'Riesgo (%)': [f'{r:.2f}' for r in riesgos]
})

st.dataframe(df_riesgos, use_container_width=True, hide_index=True)

# ============================================================================
# 6. VERIFICACIÓN DEL CÁLCULO A MANO (10 años)
# ============================================================================

st.header("6️⃣ Verificación del Cálculo a Mano (Muestra 10 años)")

st.info("""
Esta sección verifica los cálculos manuales del estudiante usando la muestra `muestra_dist10.csv`
que contiene los primeros 10 años de la serie.
""")

# Datos de muestra
datos_dist10 = df_dist10['pmax24h_mm'].dropna().values

# Tabla con posición de Weibull
st.subheader("Tabla de Datos Ordenados con Posición de Weibull")

pos10 = posiciones_graficas(datos_dist10)
datos_ord10 = pos10['datos_ord']
weibull10 = pos10['weibull']
periodo_ret10 = pos10['periodo_retorno']

df_verificacion = pd.DataFrame({
    'i': np.arange(1, len(datos_ord10) + 1),
    'x_i (mm)': [f'{x:.2f}' for x in datos_ord10],
    'p = i/(n+1)': [f'{p:.4f}' for p in weibull10],
    'T = 1/(1-p) años': [f'{t:.2f}' for t in periodo_ret10]
})

st.dataframe(df_verificacion, use_container_width=True, hide_index=True)

# Estadísticos muestrales
col1, col2, col3 = st.columns(3)

media10 = np.mean(datos_dist10)
desv10 = np.std(datos_dist10, ddof=1)
n10 = len(datos_dist10)

with col1:
    st.metric("n (número de años)", n10)
    st.metric("Media x̄ (mm)", f"{media10:.4f}")

with col2:
    st.metric("Desv. Estándar s (mm)", f"{desv10:.4f}")
    st.metric("Σx (suma)", f"{np.sum(datos_dist10):.2f}")

with col3:
    st.metric("Σx² (suma cuadrados)", f"{np.sum(datos_dist10**2):.2f}")

# Método de momentos para Gumbel
st.subheader("Parámetros de Gumbel: Método de Momentos")

mom10 = gumbel_momentos(datos_dist10)

col1, col2 = st.columns(2)

with col1:
    st.write("**Fórmulas:**")
    st.write("- β = s · √6/π")
    st.write("- μ = x̄ - γ · β  (γ = 0.5772...)")

with col2:
    st.metric("β (escala)", f"{mom10['beta']:.4f} mm")
    st.metric("μ (posición)", f"{mom10['mu']:.4f} mm")

# Cálculo paso a paso
st.write("**Cálculo paso a paso:**")
st.write(f"- β = {desv10:.4f} × {np.sqrt(6)/np.pi:.4f} = {mom10['beta']:.4f}")
st.write(f"- μ = {media10:.4f} - 0.5772 × {mom10['beta']:.4f} = {mom10['mu']:.4f}")

# Comparación: Momentos vs MV
st.subheader("Comparación: Método de Momentos vs Máxima Verosimilitud")

params_mv10, _ = ajustar(datos_dist10, 'Gumbel')

df_comparacion = pd.DataFrame({
    'Método': ['Momentos', 'Máxima Verosimilitud'],
    'μ (mm)': [f'{mom10["mu"]:.4f}', f'{params_mv10[0]:.4f}'],
    'β (mm)': [f'{mom10["beta"]:.4f}', f'{params_mv10[1]:.4f}']
})

st.dataframe(df_comparacion, use_container_width=True, hide_index=True)

# Cuantiles para T = 10, 50, 100 años
st.subheader("Cuantiles x_T para Diferentes Períodos de Retorno")

periodos_verif = [10, 50, 100]

data_comparacion_xt = []

for T in periodos_verif:
    fila = {'T (años)': T}
    
    # Por momentos
    x_T_mom = cuantil_retorno('Gumbel', (mom10['mu'], mom10['beta']), T)
    fila['x_T (Momentos)'] = f'{x_T_mom:.4f}'
    
    # Por máxima verosimilitud
    x_T_mv = cuantil_retorno('Gumbel', params_mv10, T)
    fila['x_T (MV)'] = f'{x_T_mv:.4f}'
    
    # Diferencia
    dif = abs(x_T_mv - x_T_mom)
    fila['Diferencia (mm)'] = f'{dif:.4f}'
    
    data_comparacion_xt.append(fila)

df_cuantiles_verif = pd.DataFrame(data_comparacion_xt)
st.dataframe(df_cuantiles_verif, use_container_width=True, hide_index=True)

# Riesgo de falla
st.subheader("Riesgo de Falla: T = 50 años, N = 25 años")

T_verif = 50
N_verif = 25

riesgo_verif = riesgo_falla(T_verif, N_verif)
prob_no_excedencia_anual = (1 - 1/T_verif)
prob_no_excedencia_25 = prob_no_excedencia_anual ** N_verif

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Período de diseño (T)", f"{T_verif} años")

with col2:
    st.metric("Vida útil (N)", f"{N_verif} años")

with col3:
    st.metric("R = 1 - (1 - 1/T)^N", f"{riesgo_verif:.4f}")

st.write(f"""
**Cálculo detallado:**
- Probabilidad anual de no excedencia: p = 1 - 1/{T_verif} = {prob_no_excedencia_anual:.4f}
- Probabilidad en {N_verif} años: p^{N_verif} = {prob_no_excedencia_25:.4f}
- Riesgo de falla: R = 1 - {prob_no_excedencia_25:.4f} = **{riesgo_verif:.4f}** ({riesgo_verif*100:.2f}%)
""")

# ============================================================================
# 7. INGENIERÍA: MODELOS DE SECADO (AICc)
# ============================================================================

st.header("7️⃣ Ingeniería: Modelos de Secado (AICc)")

st.info("""
Esta sección aplica criterios de información (AICc) para seleccionar el mejor
modelo semiempírico de secado. Ilustra la **navaja de Ockham**: no compres una
secadora más compleja si la sencilla seca igual.
""")

# Importar módulo de curvas
from src.modelos_curvas import tabla_modelos, MODELOS_SECADO

# Cargar datos de secado
try:
    df_secado = pd.read_csv('datos/secado.csv')
    tiempo_min = df_secado['tiempo_min'].values
    MR_secado = df_secado['MR'].values
    
    # Convertir tiempo a horas
    t_secado = tiempo_min / 60.0
    
    st.subheader("Datos de Secado Observados")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de datos observados
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.scatter(t_secado, MR_secado, s=100, alpha=0.7, edgecolor='navy', 
                   color='steelblue', label='Datos observados')
        ax.set_xlabel('Tiempo (h)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Ratio de Humedad (MR)', fontsize=11, fontweight='bold')
        ax.set_title('Curva de Secado Observada', fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Resumen")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("N (observaciones)", len(t_secado))
            st.metric("Tiempo inicial (h)", f"{t_secado[0]:.2f}")
        with col_b:
            st.metric("Tiempo final (h)", f"{t_secado[-1]:.2f}")
            st.metric("MR inicial", f"{MR_secado[0]:.4f}")
    
    # Ajustar tabla de modelos
    st.subheader("Ajuste de 5 Modelos Semiempíricos")
    
    tabla_sec = tabla_modelos(t_secado, MR_secado)
    
    # Tabla comparativa
    st.write("**Tabla de Modelos (ordenada por AICc):**")
    
    tabla_sec_display = tabla_sec[['Modelo', 'Parámetros', 'k', 'R²', 'RMSE', 
                                     'AICc', 'ΔAICc', 'Interpretación']].copy()
    
    for col in ['R²', 'RMSE', 'AICc', 'ΔAICc']:
        tabla_sec_display[col] = tabla_sec_display[col].apply(lambda x: f"{x:.4f}")
    
    st.dataframe(tabla_sec_display, use_container_width=True, hide_index=True)
    
    # Gráfico de ΔAICc
    fig, ax = plt.subplots(figsize=(10, 5))
    colores_daic_sec = ['green' if x < 2 else 'yellow' if x < 7 else 'red' 
                        for x in tabla_sec['ΔAICc'].values]
    ax.bar(tabla_sec['Modelo'], tabla_sec['ΔAICc'], color=colores_daic_sec, 
           edgecolor='black', alpha=0.7)
    ax.axhline(y=2, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='ΔAICc = 2')
    ax.axhline(y=7, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='ΔAICc = 7')
    ax.set_ylabel('ΔAICc = AICc - AICc_mín', fontsize=11, fontweight='bold')
    ax.set_title('Comparación de Modelos de Secado', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Curvas ajustadas
    st.subheader("Curvas Ajustadas de Cada Modelo")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Datos observados
    ax.scatter(t_secado, MR_secado, s=80, alpha=0.8, edgecolor='navy', 
               color='steelblue', label='Observados', zorder=3)
    
    # Curvas ajustadas
    t_suave = np.linspace(t_secado.min(), t_secado.max(), 200)
    
    colores_lineas = ['red', 'green', 'orange', 'purple', 'brown']
    
    for idx, (_, row) in enumerate(tabla_sec.iterrows()):
        modelo_nombre = row['Modelo']
        params = row['params_tuple']
        modelo_info = MODELOS_SECADO[modelo_nombre]
        func = modelo_info['func']
        
        try:
            MR_suave = func(t_suave, *params)
            ax.plot(t_suave, MR_suave, linewidth=2.5, 
                   label=f"{modelo_nombre} (ΔAICc={row['ΔAICc']:.2f})",
                   color=colores_lineas[idx], alpha=0.8)
        except:
            pass
    
    ax.set_xlabel('Tiempo (h)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Ratio de Humedad (MR)', fontsize=11, fontweight='bold')
    ax.set_title('Curvas Ajustadas: Comparación de Modelos', fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_ylim([-0.05, 1.1])
    plt.tight_layout()
    st.pyplot(fig)
    
    # Gráfico de residuos del mejor modelo
    st.subheader("Análisis de Residuos del Mejor Modelo")
    
    mejor_modelo_sec = tabla_sec.iloc[0]['Modelo']
    mejor_params_sec = tabla_sec.iloc[0]['params_tuple']
    mejor_residuos = tabla_sec.iloc[0]['residuos']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    
    # Residuos vs valores ajustados
    MR_ajust_mejor = MODELOS_SECADO[mejor_modelo_sec]['func'](t_secado, *mejor_params_sec)
    ax1.scatter(MR_ajust_mejor, mejor_residuos, s=80, alpha=0.7, 
               edgecolor='navy', color='steelblue')
    ax1.axhline(y=0, color='red', linestyle='--', linewidth=2)
    ax1.set_xlabel('Valores Ajustados', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Residuos', fontsize=11, fontweight='bold')
    ax1.set_title(f'Residuos vs Ajustados ({mejor_modelo_sec})', fontsize=11, fontweight='bold')
    ax1.grid(alpha=0.3)
    
    # Histograma de residuos
    ax2.hist(mejor_residuos, bins=8, edgecolor='black', alpha=0.7, color='steelblue')
    ax2.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Media = 0')
    ax2.set_xlabel('Residuos', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Frecuencia', fontsize=11, fontweight='bold')
    ax2.set_title('Distribución de Residuos', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Recomendación
    st.subheader("🎯 Recomendación: Navaja de Ockham")
    
    mejor_aicc = tabla_sec.iloc[0]['AICc']
    mejor_r2 = tabla_sec.iloc[0]['R²']
    mejor_k = tabla_sec.iloc[0]['k']
    segundo_k = tabla_sec.iloc[1]['k'] if len(tabla_sec) > 1 else mejor_k
    segundo_daic = tabla_sec.iloc[1]['ΔAICc'] if len(tabla_sec) > 1 else np.inf
    
    st.success(f"""
    ✅ **Modelo Recomendado: {mejor_modelo_sec}**
    
    - **AICc = {mejor_aicc:.2f}** (mejor modelo)
    - **R² = {mejor_r2:.4f}** (excelente ajuste)
    - **Parámetros: {mejor_k}** (simplicidad)
    
    **¿Por qué AICc castiga parámetros extra?**
    
    El AICc implementa la **navaja de Ockham**: entre dos modelos con ajuste similar,
    elige el más simple. Analógicamente:
    
    - **Secadora sencilla (Lewis, k=1 parámetro)**: Seca bien, bajo costo, mantenimiento simple.
    - **Secadora compleja (Dos Términos, k=4 parámetros)**: Seca bien, alto costo, difícil de operar.
    
    Si ambas secan igual, ¿por qué comprar la compleja?
    
    La fórmula AICc = AIC + 2k(k+1)/(n-k-1) penaliza k extra. Así, un modelo con
    más parámetros **solo** se prefiere si mejora **significativamente** el ajuste
    (ΔAICc > 10). Aquí, {mejor_modelo_sec} es óptimo con {mejor_k} parámetro(s),
    mientras que modelos más complejos no justifican su costo.
    """)
    
except Exception as e:
    st.error(f"Error cargando datos de secado: {e}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
**Módulo de Distribuciones de Probabilidad e Ingeniería de Secado**  
Análisis estadístico de máximos anuales de precipitación y modelado de procesos de secado.  
*Instrumento didáctico para Estadística Aplicada - Ingeniería Agrícola*
""")
