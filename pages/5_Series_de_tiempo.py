"""
Página de análisis y pronóstico de series de tiempo climáticas.

Módulos:
1. Exploración: gráficos de línea con promedios móviles y análisis estacional
2. Descomposición clásica: tendencia, estacionalidad, residuos
3. Métodos de referencia: comparación de 3 métodos simples
4. AutoTS: pronóstico automático con selección genética
5. Resultados guardados: visualización de pronósticos previos
6. Verificación manual: cálculo paso a paso con 24 meses

Utiliza src/series.py para todas las operaciones estadísticas.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Configurar path para importar src/series
ruta_src = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(ruta_src))

from series import (
    cargar_serie, promedio_movil, indices_estacionales, descomponer,
    metodos_referencia, metricas, concurso_referencia, ejecutar_autots
)

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Series de Tiempo",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Análisis de Series de Tiempo Climáticas")
st.markdown("""
Análisis estadístico de **precipitación y temperatura** de la región caribeña (2015-2025).
Incluye exploración, descomposición clásica, pronósticos de referencia y forecasting automático con AutoTS.
""")

# ============================================================================
# FUNCIONES DE CACHÉ Y CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_metadatos():
    """Carga información del estudiante y configuración."""
    ruta = Path(__file__).parent.parent / 'metadatos.json'
    with open(ruta, 'r') as f:
        return json.load(f)

@st.cache_data
def cargar_muestra_24():
    """Carga datos de muestra de 24 meses."""
    ruta = Path(__file__).parent.parent / 'datos' / 'muestra_series24.csv'
    df = pd.read_csv(ruta, parse_dates=['fecha'], index_col='fecha')
    df.index.freq = 'MS'
    return df.iloc[:, 0]  # Retornar como Series

@st.cache_resource
def cache_autots(
    serie_str, horizonte, model_list, generaciones, validaciones, intervalo, semilla
):
    """Cachea resultados de AutoTS por parámetros."""
    serie = cargar_serie(serie_str)
    return ejecutar_autots(
        serie, horizonte, model_list, generaciones, validaciones, intervalo, semilla
    )

# Cargar datos
try:
    metadatos = cargar_metadatos()
    semilla = int(metadatos.get('codigo', '6820995')) % 10000
except Exception as e:
    st.error(f"❌ Error al cargar metadatos: {e}")
    st.stop()

# Nombres de meses en español
MESES_ES = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# ============================================================================
# CREACIÓN DE TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Exploración",
    "📊 Descomposición",
    "📉 Métodos Ref.",
    "🤖 AutoTS",
    "💾 Resultados",
    "✅ Verificación"
])

# ============================================================================
# TAB 1: EXPLORACIÓN
# ============================================================================
with tab1:
    st.header("🔍 Exploración de Series Temporales")
    
    # Selector de variable
    col1, col2 = st.columns([1, 3])
    with col1:
        variable = st.radio(
            "Selecciona variable:",
            options=["precipitacion_mm", "temperatura_c"],
            format_func=lambda x: "🌧️ Precipitación (mm)" if x == "precipitacion_mm" else "🌡️ Temperatura (°C)"
        )
    
    # Cargar serie
    serie = cargar_serie(variable)
    
    # Calcular promedios móviles
    pm3 = promedio_movil(serie, 3)
    pm12 = promedio_movil(serie, 12)
    
    # --- Gráfico de línea con promedios móviles ---
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(serie.index, serie.values, label='Serie original', linewidth=1, alpha=0.6, color='steelblue')
    ax.plot(pm3.index, pm3.values, label='PM 3 meses', linewidth=2, color='orange')
    ax.plot(pm12.index, pm12.values, label='PM 12 meses', linewidth=2, color='red')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor (mm)' if variable == 'precipitacion_mm' else 'Temperatura (°C)')
    ax.set_title(f'Serie Original y Promedios Móviles - {variable}')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()
    
    # --- Diagrama de caja por mes ---
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Preparar datos por mes
    mes_valores = []
    mes_labels = []
    for mes in range(1, 13):
        valores = serie[serie.index.month == mes]
        if len(valores) > 0:
            mes_valores.append(valores.values)
            mes_labels.append(MESES_ES[mes-1])
    
    ax.boxplot(mes_valores)
    ax.set_xticklabels(mes_labels)
    ax.set_ylabel('Valor (mm)' if variable == 'precipitacion_mm' else 'Temperatura (°C)')
    ax.set_title(f'Distribución por Mes - {variable}')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close()
    
    # --- Explicación de componentes ---
    st.subheader("📋 Análisis de Componentes")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Tendencia**")
        st.write("Cambio a largo plazo (PM 12 meses). El promedio móvil de 12 meses suaviza fluctuaciones mensuales y revela la dirección general de la serie.")
    
    with col2:
        st.write("**Estacionalidad**")
        st.write("Patrón que se repite cada año. El Caribe presenta régimen bimodal de lluvias: primavera (abril-mayo) e otoño (septiembre-octubre).")
    
    with col3:
        st.write("**Irregularidad**")
        st.write("Variaciones aleatorias. Residuos después de remover tendencia y estacionalidad, causadas por eventos no predecibles.")

# ============================================================================
# TAB 2: DESCOMPOSICIÓN CLÁSICA
# ============================================================================
with tab2:
    st.header("📊 Descomposición Clásica de la Serie")
    
    # Selector de variable
    col1, col2 = st.columns([1, 3])
    with col1:
        variable_descomp = st.radio(
            "Variable:",
            options=["precipitacion_mm", "temperatura_c"],
            format_func=lambda x: "🌧️ Precipitación" if x == "precipitacion_mm" else "🌡️ Temperatura",
            key="descomp_var"
        )
    
    # Descomponer serie
    serie_descomp = cargar_serie(variable_descomp)
    trend, seasonal, resid, descomposicion = descomponer(serie_descomp)
    
    # Gráfico de descomposición
    fig, axes = plt.subplots(4, 1, figsize=(14, 10))
    
    axes[0].plot(serie_descomp.index, serie_descomp.values, 'b-', linewidth=1)
    axes[0].set_ylabel('Observada')
    axes[0].set_title(f'Descomposición de {variable_descomp}')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(trend.index, trend.values, 'g-', linewidth=1.5)
    axes[1].set_ylabel('Tendencia')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(seasonal.index, seasonal.values, 'r-', linewidth=1)
    axes[2].set_ylabel('Estacional')
    axes[2].grid(True, alpha=0.3)
    
    axes[3].plot(resid.index, resid.values, 'k-', linewidth=0.8)
    axes[3].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    axes[3].set_ylabel('Residuo')
    axes[3].set_xlabel('Fecha')
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Tabla de índices estacionales
    st.subheader("📅 Índices Estacionales por Mes")
    indices = indices_estacionales(serie_descomp)
    
    # Crear tabla
    df_indices = pd.DataFrame({
        'Mes': MESES_ES,
        'Índice Estacional': indices,
        'Interpretación': ['Arriba del promedio' if i > 0 else 'Abajo del promedio' for i in indices]
    })
    
    st.dataframe(df_indices, use_container_width=True)
    
    # Estadísticas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Suma de Índices", f"{indices.sum():.4f}", "≈ 0 (aditivo)")
    col2.metric("Max Índice", f"{indices.max():.2f}", MESES_ES[indices.argmax()])
    col3.metric("Min Índice", f"{indices.min():.2f}", MESES_ES[indices.argmin()])
    col4.metric("Rango", f"{indices.max() - indices.min():.2f}")


# ============================================================================
# TAB 3: MÉTODOS DE REFERENCIA Y VALIDACIÓN
# ============================================================================
with tab3:
    st.header("📉 Métodos de Referencia y Validación")
    st.write("Últimos 12 meses como validación (entrenamiento: 2015-2024, validación: últimos 12)")
    
    # Selector de variable
    col1, col2 = st.columns([1, 3])
    with col1:
        variable_ref = st.radio(
            "Variable:",
            options=["precipitacion_mm", "temperatura_c"],
            format_func=lambda x: "🌧️ Precip." if x == "precipitacion_mm" else "🌡️ Temp.",
            key="ref_var"
        )
    
    # Cargar serie y dividir
    serie_ref = cargar_serie(variable_ref)
    n_entrenamiento = len(serie_ref) - 12
    entrenamiento = serie_ref.iloc[:n_entrenamiento]
    validacion = serie_ref.iloc[n_entrenamiento:]
    
    # Generar pronósticos
    h = 12
    pronosticos_dict = metodos_referencia(entrenamiento, h)
    
    # Gráfico: Real vs Pronósticos
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(validacion.index, validacion.values, 'ko-', linewidth=2, markersize=6, label='Real', zorder=3)
    
    for nombre, pron in pronosticos_dict.items():
        etiqueta = nombre.replace('_', ' ').title()
        ax.plot(pron.index, pron.values, 'o-', linewidth=1.5, markersize=5, label=etiqueta, alpha=0.7)
    
    # Línea vertical entre entrenamiento y validación
    ax.axvline(x=entrenamiento.index[-1], color='red', linestyle='--', linewidth=2, alpha=0.5, label='Corte E/V')
    
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor (mm)' if variable_ref == 'precipitacion_mm' else 'Temperatura (°C)')
    ax.set_title(f'Pronósticos de Métodos de Referencia - {variable_ref}')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()
    
    # Tabla de métricas
    st.subheader("📊 Métricas de Evaluación")
    
    resultados_lista = []
    for nombre_metodo, valores_pron in pronosticos_dict.items():
        metr = metricas(validacion, valores_pron)
        resultados_lista.append({
            'Método': nombre_metodo.replace('_', ' ').title(),
            'MAE': f"{metr['MAE']:.4f}",
            'RMSE': f"{metr['RMSE']:.4f}",
            'SMAPE': f"{metr['SMAPE']:.2f}%"
        })
    
    df_metricas = pd.DataFrame(resultados_lista)
    # Ordenar por SMAPE (descendente para obtener porcentaje de menor a mayor)
    st.dataframe(df_metricas, use_container_width=True)
    
    st.info("ℹ️ **MAE**: Error absoluto medio. **RMSE**: Raíz del error cuadrado medio (penaliza errores grandes). **SMAPE**: Error porcentual absoluto simétrico (comparable entre series).")

# ============================================================================
# TAB 4: PRONÓSTICO AUTOMÁTICO CON AutoTS
# ============================================================================
with tab4:
    st.header("🤖 Pronóstico Automático con AutoTS")
    st.write("""
    **Analogía con ensayo de variedades agrícolas:**
    - **Generaciones**: ciclos de siembra y selección
    - **Modelos**: variedades de cultivo a evaluar
    - **Validaciones**: cosechas de prueba (backtesting)
    - **Intervalo de confianza**: rango de rendimiento esperado
    """)
    
    # Formulario de parámetros
    with st.form("autots_form"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            horizonte = st.slider(
                "Horizonte (meses)",
                min_value=6, max_value=24, value=12, step=1
            )
        
        with col2:
            model_list = st.selectbox(
                "Modelos",
                options=["superfast", "fast"],
                index=0
            )
        
        with col3:
            generaciones = st.slider(
                "Generaciones",
                min_value=1, max_value=10, value=5, step=1
            )
        
        with col4:
            validaciones = st.slider(
                "Validaciones",
                min_value=1, max_value=3, value=2, step=1
            )
        
        col1_inter, col2_inter = st.columns(2)
        with col1_inter:
            intervalo = st.selectbox(
                "Intervalo confianza",
                options=[0.8, 0.9, 0.95],
                index=1
            )
        
        with col2_inter:
            ejecutar = st.form_submit_button("🚀 Ejecutar AutoTS")
    
    if ejecutar:
        with st.spinner(f"⏳ Ejecutando AutoTS ({generaciones} generaciones, {validaciones} validaciones)..."):
            try:
                serie_autots = cargar_serie('precipitacion_mm')
                
                resultados = cache_autots(
                    'precipitacion_mm',
                    horizonte=horizonte,
                    model_list=model_list,
                    generaciones=generaciones,
                    validaciones=validaciones,
                    intervalo=intervalo,
                    semilla=semilla
                )
                
                # Mostrar modelo ganador
                st.subheader("🏆 Modelo Ganador")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Nombre", resultados['modelo_nombre'])
                
                with col2:
                    st.json(resultados['modelo_params'])
                
                # Gráfico pronóstico con intervalo de confianza
                st.subheader("📈 Pronóstico y Banda de Confianza")
                
                fig, ax = plt.subplots(figsize=(14, 6))
                
                # Últimos 24 meses de histórico
                historico = serie_autots.tail(24)
                ax.plot(historico.index, historico.values, 'b-', linewidth=2, label='Histórico', zorder=2)
                
                # Pronóstico
                pron_df = resultados['pronostico']
                ax.plot(pron_df['fecha'], pron_df['pronostico_mm'], 'ro-', linewidth=2, markersize=6, label='Pronóstico', zorder=2)
                
                # Banda de confianza
                ax.fill_between(
                    pron_df['fecha'],
                    pron_df['limite_inferior_mm'],
                    pron_df['limite_superior_mm'],
                    alpha=0.2, color='red', label=f'Intervalo {int(intervalo*100)}%'
                )
                
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Precipitación (mm)')
                ax.set_title(f'Pronóstico AutoTS - {horizonte} meses ({intervalo*100:.0f}% confianza)')
                ax.legend(loc='best')
                ax.grid(True, alpha=0.3)
                ax.axvline(x=serie_autots.index[-1], color='gray', linestyle='--', alpha=0.5)
                st.pyplot(fig)
                plt.close()
                
                # Tabla de pronóstico
                st.subheader("📋 Tabla de Pronóstico")
                st.dataframe(pron_df, use_container_width=True)
                
                # Descargar pronóstico
                csv = pron_df.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar Pronóstico (CSV)",
                    data=csv,
                    file_name=f"pronostico_autots_{horizonte}meses.csv",
                    mime="text/csv"
                )
                
                # Top 10 modelos
                if 'top_modelos' in resultados:
                    st.subheader("🏅 Top 10 Modelos Evaluados")
                    st.dataframe(resultados['top_modelos'], use_container_width=True)
                
                # Información conceptual
                st.info("""
                🌾 **Analogía del Ensayo de Variedades:**
                
                AutoTS funciona como un protocolo agrícola:
                1. **Generaciones**: Cada generación es un ciclo de siembra → crecimiento → selección
                2. **Backtesting**: Se prueba cada modelo en múltiples períodos pasados (cosechas)
                3. **Ensemble**: El modelo final combina los mejores, como un cultivo mixto optimizado
                4. **Intervalo de confianza**: El rango de rendimiento esperado (e.g., 90% de cosechas)
                """)
                
                # Guardar resultados
                carpeta = Path(__file__).parent.parent / 'resultados'
                carpeta.mkdir(exist_ok=True)
                
                ruta_resultado = carpeta / f"autots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(ruta_resultado, 'w') as f:
                    json.dump({
                        'parametros': {
                            'horizonte': horizonte,
                            'model_list': model_list,
                            'generaciones': generaciones,
                            'validaciones': validaciones,
                            'intervalo': intervalo
                        },
                        'modelo_nombre': resultados['modelo_nombre'],
                        'modelo_params': resultados['modelo_params'],
                        'pronostico': pron_df.to_dict('records'),
                        'fecha_ejecucion': datetime.now().isoformat()
                    }, f, indent=2, default=str)
                
                st.success(f"✅ Resultados guardados en resultados/")
                
            except Exception as e:
                st.error(f"❌ Error en AutoTS: {e}")
                st.write("Asegúrate de tener `autots` instalado: `.venv/bin/pip install autots`")


# ============================================================================
# TAB 5: RESULTADOS GUARDADOS
# ============================================================================
with tab5:
    st.header("💾 Resultados de Pronósticos Guardados")
    
    carpeta_resultados = Path(__file__).parent.parent / 'resultados'
    
    if not carpeta_resultados.exists():
        st.info("ℹ️ No hay resultados guardados aún. Ejecuta AutoTS en la sección anterior.")
    else:
        archivos = sorted(carpeta_resultados.glob("autots_*.json"), reverse=True)
        
        if not archivos:
            st.info("ℹ️ No hay archivos de AutoTS en resultados/")
        else:
            # Selector de archivo
            archivo_seleccionado = st.selectbox(
                "Selecciona un resultado:",
                options=archivos,
                format_func=lambda x: x.name
            )
            
            # Cargar resultado
            with open(archivo_seleccionado, 'r') as f:
                resultado_json = json.load(f)
            
            # Mostrar información
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**Parámetros de Ejecución:**")
                if 'parametros' in resultado_json:
                    st.json(resultado_json['parametros'])
            
            with col2:
                st.write("**Modelo Ganador:**")
                if 'modelo_nombre' in resultado_json and 'modelo_params' in resultado_json:
                    st.json({
                        'nombre': resultado_json['modelo_nombre'],
                        'parámetros': resultado_json['modelo_params']
                    })
                else:
                    st.info("ℹ️ Información del modelo no disponible en este archivo")
            
            # Tabla de pronóstico
            if 'pronostico' in resultado_json:
                st.subheader("📋 Pronóstico")
                df_pron = pd.DataFrame(resultado_json['pronostico'])
                st.dataframe(df_pron, use_container_width=True)
                
                # Descargar
                csv = df_pron.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar Pronóstico",
                    data=csv,
                    file_name=f"pronostico_{archivo_seleccionado.stem}.csv",
                    mime="text/csv"
                )
            else:
                st.info("ℹ️ No hay datos de pronóstico en este archivo")

# ============================================================================
# TAB 6: VERIFICACIÓN DEL CÁLCULO A MANO (24 MESES)
# ============================================================================
with tab6:
    st.header("✅ Verificación del Cálculo a Mano (24 Meses)")
    st.write("Muestra de 24 meses: 18 entrenamiento + 6 validación. Verificación paso a paso.")
    
    # Cargar muestra
    try:
        muestra = cargar_muestra_24()
    except Exception as e:
        st.error(f"❌ Error al cargar muestra_series24.csv: {e}")
        st.stop()
    
    # División
    n_entrenamiento = 18
    entrenamiento_24 = muestra.iloc[:n_entrenamiento]
    validacion_24 = muestra.iloc[n_entrenamiento:]
    
    # -------- Sección 1: Muestra y Promedios Móviles --------
    st.subheader("📊 1. Muestra de Datos y Promedios Móviles")
    
    pm3_24 = promedio_movil(muestra, 3)
    
    df_muestra = pd.DataFrame({
        'Fecha': muestra.index.strftime('%Y-%m'),
        'Valor': muestra.values,
        'PM3': pm3_24.values
    }).reset_index(drop=True)
    
    st.dataframe(df_muestra, use_container_width=True)
    
    # -------- Sección 2: Índices Estacionales --------
    st.subheader("📅 2. Índices Estacionales")
    
    indices_24 = indices_estacionales(entrenamiento_24)
    
    df_indices_24 = pd.DataFrame({
        'Mes': MESES_ES,
        'Índice': indices_24.round(4),
        'Interpretación': ['✅ Arriba' if i > 0 else '❌ Abajo' for i in indices_24]
    })
    
    st.dataframe(df_indices_24, use_container_width=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Suma de índices", f"{indices_24.sum():.6f}", "Debe ser ≈ 0")
    col2.metric("Rango", f"{indices_24.max() - indices_24.min():.4f}")
    
    # -------- Sección 3: Pronósticos de 3 Métodos --------
    st.subheader("📈 3. Pronósticos de Julio-Diciembre 2025")
    
    pronosticos_24 = metodos_referencia(entrenamiento_24, 6)
    
    # Crear tabla con pronósticos y valores reales
    df_pron_24 = pd.DataFrame({
        'Mes': [MESES_ES[validacion_24.index[i].month - 1] for i in range(6)],
        'Ingenuo': pronosticos_24['ingenuo'].values.round(2),
        'Estac. Ingenuo': pronosticos_24['estacional_ingenuo'].values.round(2),
        'Promedio': pronosticos_24['promedio'].values.round(2),
        'Real': validacion_24.values.round(2)
    })
    
    st.dataframe(df_pron_24, use_container_width=True)
    
    # -------- Sección 4: Tabla de Errores --------
    st.subheader("🔍 4. Análisis de Errores por Método")
    
    # Calcular errores para cada método
    for metodo_nombre, pron_valores in pronosticos_24.items():
        st.write(f"**{metodo_nombre.replace('_', ' ').title()}**")
        
        errores = validacion_24.values - pron_valores.values
        errores_abs = np.abs(errores)
        errores_cuad = errores ** 2
        denominador = np.abs(validacion_24.values) + np.abs(pron_valores.values)
        denominador = np.where(denominador == 0, 1e-10, denominador)
        ape_abs = 100 * errores_abs / denominador
        
        df_errores = pd.DataFrame({
            'Mes': [MESES_ES[validacion_24.index[i].month - 1] for i in range(6)],
            'Real': validacion_24.values.round(2),
            'Pronóstico': pron_valores.values.round(2),
            '|e|': errores_abs.round(4),
            'e²': errores_cuad.round(4),
            'APE%': ape_abs.round(2)
        })
        
        st.dataframe(df_errores, use_container_width=True)
    
    # -------- Sección 5: Resumen de Métricas --------
    st.subheader("📊 5. Resumen de Métricas por Método")
    
    resultados_24 = []
    for nombre_metodo, pron_valores in pronosticos_24.items():
        metr = metricas(validacion_24, pron_valores)
        resultados_24.append({
            'Método': nombre_metodo.replace('_', ' ').title(),
            'MAE': f"{metr['MAE']:.4f}",
            'RMSE': f"{metr['RMSE']:.4f}",
            'SMAPE': f"{metr['SMAPE']:.2f}%"
        })
    
    df_resumen = pd.DataFrame(resultados_24)
    st.dataframe(df_resumen, use_container_width=True)
    
    # Método ganador
    st.subheader("🏆 Método Ganador")
    
    # Extraer SMAPE y encontrar el menor
    smape_valores = []
    for nombre_metodo, pron_valores in pronosticos_24.items():
        metr = metricas(validacion_24, pron_valores)
        smape_valores.append((nombre_metodo.replace('_', ' ').title(), metr['SMAPE']))
    
    metodo_ganador, smape_min = min(smape_valores, key=lambda x: x[1])
    st.success(f"✅ **{metodo_ganador}** con SMAPE = {smape_min:.2f}%")
    
    # -------- Sección 6: Gráfico Final --------
    st.subheader("📉 6. Gráfico: Entrenamiento vs Validación con Pronósticos")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Histórico entrenamiento
    ax.plot(entrenamiento_24.index, entrenamiento_24.values, 'b-o', linewidth=2, markersize=4, label='Entrenamiento', zorder=2)
    
    # Validación
    ax.plot(validacion_24.index, validacion_24.values, 'ko-', linewidth=2, markersize=6, label='Real', zorder=2)
    
    # Pronósticos
    for nombre_metodo, pron_valores in pronosticos_24.items():
        etiqueta = nombre_metodo.replace('_', ' ').title()
        ax.plot(pron_valores.index, pron_valores.values, 'o--', linewidth=1.5, markersize=5, label=etiqueta, alpha=0.7)
    
    # Línea de corte
    ax.axvline(x=entrenamiento_24.index[-1], color='red', linestyle='--', linewidth=2, alpha=0.5, label='Corte Entrenamiento/Validación')
    
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor')
    ax.set_title('Verificación: Entrenamiento (18 meses) + Validación (6 meses)')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

