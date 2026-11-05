"""
pages/2_EDA.py - Módulo de Análisis Exploratorio de Datos (EDA)

Análisis univariado, bivariado, cualitativo y detección de atípicos
con datos de parcelas.csv y muestra_eda10.csv.

Estudiante: Justo Fuentes (6820995)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sys
from pathlib import Path

# Agregar carpeta src al path (CRÍTICO)
ruta_src = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(ruta_src))

from datos import tarjeta_estudiante
from eda import resumen_numerico, vallas_tukey, tabla_frecuencias

# ============================================================================
# Configuración
# ============================================================================

st.set_page_config(
    page_title="EDA - Estadística Aplicada",
    page_icon="🔍",
    layout="wide"
)

# Configurar estilo de gráficos
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# Cargar datos
# ============================================================================

@st.cache_data
def cargar_datos():
    """Cargar datos de parcelas y muestra para EDA"""
    df_parcelas = pd.read_csv('datos/parcelas.csv')
    df_muestra = pd.read_csv('datos/muestra_eda10.csv')
    return df_parcelas, df_muestra

df_parcelas, df_muestra = cargar_datos()

# ============================================================================
# Barra lateral: Filtros
# ============================================================================

with st.sidebar:
    tarjeta_estudiante(ubicacion='sidebar')
    
    st.markdown("---")
    st.markdown("## 🔧 Filtros de Datos")
    
    # Selector de tipo de suelo
    suelos_disponibles = ['Todos'] + sorted(df_parcelas['suelo'].unique().tolist())
    suelo_seleccionado = st.selectbox('Tipo de Suelo', suelos_disponibles)
    
    # Selector de riego
    riego_disponible = ['Todos'] + sorted(df_parcelas['riego'].unique().tolist())
    riego_seleccionado = st.selectbox('Riego', riego_disponible)
    
    # Aplicar filtros
    df_filtrado = df_parcelas.copy()
    
    if suelo_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['suelo'] == suelo_seleccionado]
    
    if riego_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['riego'] == riego_seleccionado]
    
    st.markdown(f"**Parcelas seleccionadas:** {len(df_filtrado)} de {len(df_parcelas)}")

# ============================================================================
# Página Principal
# ============================================================================

st.markdown("# 🔍 Análisis Exploratorio de Datos (EDA)")
st.markdown("**Descubre patrones, relaciones y anomalías en tus datos**")

st.markdown("---")

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Univariado", "📈 Cualitativo", "🔗 Bivariado", "⚠️ Faltantes y Atípicos", "✓ Verificación Manual"]
)

# ============================================================================
# TAB 1: ANÁLISIS UNIVARIADO
# ============================================================================

with tab1:
    st.markdown("## 📊 Análisis Univariado")
    st.markdown("Análisis detallado de variables numéricas individuales")
    
    # Selector de variable numérica
    variables_numericas = ['rendimiento', 'dosis_N', 'lamina_riego', 'materia_organica', 'ph']
    variable_seleccionada = st.selectbox(
        'Selecciona una variable numérica',
        variables_numericas,
        key='univariado'
    )
    
    serie = df_filtrado[variable_seleccionada]
    
    # Calcular resumen numérico
    resumen = resumen_numerico(serie)
    
    if resumen:
        # Mostrar tabla de resumen
        st.markdown("### 📋 Tabla de Resumen")
        
        tabla_resumen = pd.DataFrame({
            'Estadística': [
                'n (tamaño muestral)',
                'Media',
                'Mediana',
                'Desv. Est. Muestral',
                'Varianza',
                'CV (%)',
                'Mínimo',
                'Q1 (25%)',
                'Q3 (75%)',
                'Máximo',
                'RIC',
                'Asimetría'
            ],
            'Valor': [
                f"{int(resumen['n'])}",
                f"{resumen['media']:.4f}",
                f"{resumen['mediana']:.4f}",
                f"{resumen['desv_est_muestral']:.4f}",
                f"{resumen['varianza']:.4f}",
                f"{resumen['coef_variacion_pct']:.4f}",
                f"{resumen['minimo']:.4f}",
                f"{resumen['q1']:.4f}",
                f"{resumen['q3']:.4f}",
                f"{resumen['maximo']:.4f}",
                f"{resumen['rango_intercuartil']:.4f}",
                f"{resumen['asimetria']:.4f}"
            ]
        })
        
        st.dataframe(tabla_resumen, width='stretch')
        
        # Dos columnas para gráficos
        col1, col2 = st.columns(2)
        
        # Histograma con curva de densidad
        with col1:
            st.markdown("### 📊 Histograma con Densidad")
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Histograma
            ax.hist(serie.dropna(), bins=20, density=True, alpha=0.7, 
                   color='skyblue', edgecolor='black', label='Frecuencia')
            
            # Curva de densidad (KDE)
            serie.dropna().plot(kind='density', ax=ax, color='red', 
                               linewidth=2, label='Densidad (KDE)')
            
            ax.set_xlabel(f'{variable_seleccionada}', fontsize=11)
            ax.set_ylabel('Densidad', fontsize=11)
            ax.set_title(f'Distribución de {variable_seleccionada}', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            plt.close()
        
        # Diagrama de caja
        with col2:
            st.markdown("### 📦 Diagrama de Caja (Boxplot)")
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Boxplot
            bp = ax.boxplot(serie.dropna(), vert=True, patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
            bp['boxes'][0].set_alpha(0.7)
            
            ax.set_ylabel(f'{variable_seleccionada}', fontsize=11)
            ax.set_title(f'Boxplot de {variable_seleccionada}', fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            st.pyplot(fig)
            plt.close()
        
        # Detectar atípicos con vallas de Tukey
        limite_inf, limite_sup, atipicos = vallas_tukey(serie)
        
        st.markdown("### ⚠️ Valores Atípicos (Vallas de Tukey)")
        st.markdown(f"""
        - **Límite Inferior:** {limite_inf:.4f}
        - **Límite Superior:** {limite_sup:.4f}
        - **Criterio:** 1.5 × RIC
        """)
        
        if atipicos:
            st.warning(f"🔴 Se encontraron **{len(atipicos)}** valores atípicos")
            tabla_atipicos = pd.DataFrame({
                'Parcela': [idx for idx, _ in atipicos],
                'Valor': [val for _, val in atipicos]
            })
            st.dataframe(tabla_atipicos, width='stretch')
        else:
            st.success("✅ No se encontraron valores atípicos")

# ============================================================================
# TAB 2: ANÁLISIS CUALITATIVO
# ============================================================================

with tab2:
    st.markdown("## 📈 Análisis de Variables Cualitativas")
    st.markdown("Frecuencias y gráficos de barras para variables categóricas")
    
    # Selector de variable cualitativa
    variables_cualitativas = ['suelo', 'riego']
    variable_cualitativa = st.selectbox(
        'Selecciona una variable cualitativa',
        variables_cualitativas,
        key='cualitativo'
    )
    
    # Tabla de frecuencias
    tabla_freq = tabla_frecuencias(df_filtrado[variable_cualitativa])
    
    st.markdown("### 📊 Tabla de Frecuencias")
    st.dataframe(tabla_freq, width='stretch')
    
    # Gráfico de barras
    st.markdown("### 📊 Gráfico de Barras")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    barras = ax.bar(tabla_freq['Categoría'], tabla_freq['Frecuencia Absoluta'],
                    color=colores[:len(tabla_freq)], alpha=0.8, edgecolor='black')
    
    # Agregar valores en las barras
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
               f'{int(altura)}',
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel(variable_cualitativa.capitalize(), fontsize=11)
    ax.set_ylabel('Frecuencia Absoluta', fontsize=11)
    ax.set_title(f'Distribución de {variable_cualitativa.capitalize()}', 
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    st.pyplot(fig)
    plt.close()

# ============================================================================
# TAB 3: ANÁLISIS BIVARIADO
# ============================================================================

with tab3:
    st.markdown("## 🔗 Análisis Bivariado")
    st.markdown("Relaciones entre pares de variables")
    
    st.markdown("---")
    
    # Subsección: Boxplot de rendimiento por suelo y riego
    st.markdown("### 📦 Rendimiento por Tipo de Suelo y Riego")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Rendimiento por Tipo de Suelo**")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        sns.boxplot(data=df_filtrado, x='suelo', y='rendimiento', 
                   palette='Set2', ax=ax)
        
        ax.set_xlabel('Tipo de Suelo', fontsize=11)
        ax.set_ylabel('Rendimiento', fontsize=11)
        ax.set_title('Distribución de Rendimiento por Suelo', 
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("**Rendimiento por Riego**")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        sns.boxplot(data=df_filtrado, x='riego', y='rendimiento', 
                   palette='Set1', ax=ax)
        
        ax.set_xlabel('Riego', fontsize=11)
        ax.set_ylabel('Rendimiento', fontsize=11)
        ax.set_title('Distribución de Rendimiento por Riego', 
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        st.pyplot(fig)
        plt.close()
    
    st.markdown("---")
    
    # Subsección: Diagrama de dispersión
    st.markdown("### 📊 Dispersión: Variable vs. Rendimiento")
    
    variables_scatter = ['dosis_N', 'lamina_riego', 'materia_organica', 'ph']
    variable_x = st.selectbox('Selecciona variable X', variables_scatter, key='scatter')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Colorear por riego
    colores_riego = {'Sí': '#FF6B6B', 'No': '#4ECDC4'}
    for riego in df_filtrado['riego'].unique():
        mascara = df_filtrado['riego'] == riego
        ax.scatter(df_filtrado[mascara][variable_x], 
                  df_filtrado[mascara]['rendimiento'],
                  label=f'Riego: {riego}',
                  alpha=0.6, s=80, color=colores_riego.get(riego, 'gray'))
    
    ax.set_xlabel(variable_x, fontsize=11)
    ax.set_ylabel('Rendimiento', fontsize=11)
    ax.set_title(f'{variable_x} vs. Rendimiento (coloreado por Riego)', 
                fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    st.markdown("---")
    
    # Subsección: Matriz de correlación
    st.markdown("### 🔥 Matriz de Correlación de Pearson")
    
    variables_corr = ['rendimiento', 'dosis_N', 'lamina_riego', 'materia_organica', 'ph']
    df_corr = df_filtrado[variables_corr].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(df_corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
               cbar_kws={'label': 'Correlación'}, ax=ax, 
               vmin=-1, vmax=1, square=True)
    
    ax.set_title('Matriz de Correlación de Pearson', fontsize=12, fontweight='bold')
    
    st.pyplot(fig)
    plt.close()
    
    st.markdown("""
    **Interpretación:**
    - **r = 1:** Correlación positiva perfecta
    - **r = 0:** Sin correlación
    - **r = -1:** Correlación negativa perfecta
    """)

# ============================================================================
# TAB 4: DATOS FALTANTES Y ATÍPICOS
# ============================================================================

with tab4:
    st.markdown("## ⚠️ Datos Faltantes y Valores Atípicos")
    
    st.markdown("---")
    
    st.markdown("### 📋 Análisis de Valores Faltantes")
    
    # Contar faltantes por columna
    faltantes = df_parcelas.isnull().sum()
    faltantes_pct = (faltantes / len(df_parcelas)) * 100
    
    tabla_faltantes = pd.DataFrame({
        'Variable': faltantes.index,
        'Faltantes': faltantes.values,
        'Porcentaje': faltantes_pct.values
    })
    
    tabla_faltantes = tabla_faltantes[tabla_faltantes['Faltantes'] > 0]
    
    if len(tabla_faltantes) == 0:
        st.success("✅ **No hay valores faltantes en el dataset**")
    else:
        st.warning("🔴 Se encontraron valores faltantes:")
        st.dataframe(tabla_faltantes, width='stretch')
    
    st.markdown("---")
    
    st.markdown("### 📍 Recomendaciones para Manejo de Datos Faltantes")
    
    st.markdown("""
    **Estrategias según la situación:**
    
    1. **Eliminar registros (listwise deletion):**
       - ✅ Usar si: faltantes < 5% y datos MCAR (Missing Completely At Random)
       - ❌ Evitar si: Pérdida importante de información
    
    2. **Imputación por media/mediana:**
       - ✅ Usar si: Variable es continua y faltantes aleatorios
       - ⚠️ Riesgo: Reduce varianza y oculta patrones
    
    3. **Imputación por regresión:**
       - ✅ Usar si: Relación lineal con otras variables
       - ⚠️ Riesgo: Introduce sesgo si el modelo es incorrecto
    
    4. **Mantener como faltante:**
       - ✅ Usar si: Faltante tiene significado (ej: datos no disponibles)
       - ✅ Usar si: Análisis es robusto a faltantes
    
    **Para este proyecto:**
    - 📊 Mantener faltantes visibles en análisis descriptivo
    - 📈 Documentar estrategia elegida para inferencia
    - ✓ No eliminar observaciones sin justificación
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Resumen de Valores Atípicos por Variable")
    
    for var in ['rendimiento', 'dosis_N', 'lamina_riego', 'materia_organica', 'ph']:
        _, _, atipicos = vallas_tukey(df_parcelas[var])
        if atipicos:
            st.markdown(f"**{var}:** {len(atipicos)} atípicos detectados")
            for parcela, valor in atipicos[:3]:  # Mostrar máximo 3
                st.caption(f"  - {parcela}: {valor:.4f}")

# ============================================================================
# TAB 5: VERIFICACIÓN MANUAL (10 PARCELAS)
# ============================================================================

with tab5:
    st.markdown("## ✓ Verificación del Cálculo a Mano (10 Parcelas)")
    st.markdown("Cálculos paso a paso sobre muestra_eda10.csv")
    
    st.markdown("---")
    
    st.markdown("### 📋 Datos de Muestra (10 Parcelas)")
    
    # Mostrar tabla de muestra
    df_muestra_display = df_muestra.copy()
    st.dataframe(df_muestra_display, width='stretch')
    
    st.markdown("---")
    
    st.markdown("### 📊 Resumen Numérico de la Muestra")
    
    # Calcular resumen para rendimiento
    resumen_muestra = resumen_numerico(df_muestra['rendimiento'])
    
    tabla_resumen_muestra = pd.DataFrame({
        'Estadística': [
            'n',
            'Media',
            'Mediana',
            'Desv. Est. Muestral',
            'Varianza',
            'CV (%)',
            'Mínimo',
            'Q1',
            'Q3',
            'Máximo',
            'RIC',
            'Asimetría'
        ],
        'Valor': [
            f"{int(resumen_muestra['n'])}",
            f"{resumen_muestra['media']:.4f}",
            f"{resumen_muestra['mediana']:.4f}",
            f"{resumen_muestra['desv_est_muestral']:.4f}",
            f"{resumen_muestra['varianza']:.4f}",
            f"{resumen_muestra['coef_variacion_pct']:.4f}",
            f"{resumen_muestra['minimo']:.4f}",
            f"{resumen_muestra['q1']:.4f}",
            f"{resumen_muestra['q3']:.4f}",
            f"{resumen_muestra['maximo']:.4f}",
            f"{resumen_muestra['rango_intercuartil']:.4f}",
            f"{resumen_muestra['asimetria']:.4f}"
        ]
    })
    
    st.dataframe(tabla_resumen_muestra, width='stretch')
    
    st.markdown("---")
    
    st.markdown("### 📐 Tabla de Desviaciones (x - media) y (x - media)²")
    
    media = resumen_muestra['media']
    tabla_desviaciones = pd.DataFrame({
        'Parcela': df_muestra['parcela'],
        'Rendimiento (x)': df_muestra['rendimiento'].apply(lambda x: f"{x:.4f}"),
        '(x - media)': df_muestra['rendimiento'].apply(lambda x: f"{(x - media):.4f}"),
        '(x - media)²': df_muestra['rendimiento'].apply(lambda x: f"{(x - media)**2:.4f}")
    })
    
    st.dataframe(tabla_desviaciones, width='stretch')
    
    # Mostrar cálculo de varianza
    suma_desv_cuadrado = ((df_muestra['rendimiento'] - media) ** 2).sum()
    varianza_manual = suma_desv_cuadrado / (len(df_muestra) - 1)
    
    st.markdown(f"""
    **Cálculo de Varianza (Muestral):**
    
    Σ(x - media)² = {suma_desv_cuadrado:.4f}
    
    Varianza = Σ(x - media)² / (n - 1) = {suma_desv_cuadrado:.4f} / {len(df_muestra) - 1} = {varianza_manual:.4f}
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚠️ Vallas de Tukey (Detección de Atípicos)")
    
    limite_inf_muestra, limite_sup_muestra, atipicos_muestra = vallas_tukey(df_muestra['rendimiento'])
    
    st.markdown(f"""
    - **Q1:** {resumen_muestra['q1']:.4f}
    - **Q3:** {resumen_muestra['q3']:.4f}
    - **RIC:** {resumen_muestra['rango_intercuartil']:.4f}
    
    **Límites de Tukey:**
    - **L_inf = Q1 - 1.5 × RIC** = {resumen_muestra['q1']:.4f} - 1.5 × {resumen_muestra['rango_intercuartil']:.4f} = {limite_inf_muestra:.4f}
    - **L_sup = Q3 + 1.5 × RIC** = {resumen_muestra['q3']:.4f} + 1.5 × {resumen_muestra['rango_intercuartil']:.4f} = {limite_sup_muestra:.4f}
    """)
    
    if atipicos_muestra:
        st.warning(f"🔴 **Valores Atípicos:** {len(atipicos_muestra)}")
        for parcela, valor in atipicos_muestra:
            st.caption(f"  - {parcela}: {valor:.4f}")
    else:
        st.success("✅ **No hay valores atípicos en la muestra**")
    
    st.markdown("---")
    
    st.markdown("### 📊 Media de Rendimiento por Riego")
    
    media_por_riego = df_muestra.groupby('riego')['rendimiento'].mean()
    
    tabla_media_riego = pd.DataFrame({
        'Riego': media_por_riego.index,
        'Media de Rendimiento': media_por_riego.apply(lambda x: f"{x:.4f}")
    })
    
    st.dataframe(tabla_media_riego, width='stretch')
