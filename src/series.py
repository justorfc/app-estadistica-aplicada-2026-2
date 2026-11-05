"""
Módulo de análisis y pronóstico de series de tiempo.

Proporciona funciones para cargar datos, descomponer series, calcular índices
estacionales y evaluar métodos de pronóstico contra benchmarks.

Autor: Copilot
Versión: 1.0
"""

import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.seasonal import seasonal_decompose
from typing import Tuple, Dict


# ============================================================================
# 1. CARGAR SERIE DE TIEMPO
# ============================================================================

def cargar_serie(variable: str) -> pd.Series:
    """
    Carga una serie de tiempo desde CSV con índice de fechas y frecuencia mensual.
    
    Lee el archivo datos/clima_mensual.csv o datos/muestra_series24.csv,
    filtra la variable solicitada y retorna una serie con índice de fechas
    en frecuencia mensual (MS - Month Start).
    
    Parámetros
    ----------
    variable : str
        Nombre de la variable a extraer del CSV (ej: 'precipitacion_mm', 'temperatura_c')
    
    Retorna
    -------
    pd.Series
        Serie de tiempo con índice de fechas (frecuencia 'MS') y valores numéricos
    
    Ejemplo
    -------
    >>> serie_temp = cargar_serie('temperatura_c')
    >>> print(serie_temp.index.freq)
    <MonthBegin>
    """
    # Construcción de ruta relativa al directorio del proyecto
    ruta_proyecto = Path(__file__).parent.parent
    ruta_csv = ruta_proyecto / "datos" / "clima_mensual.csv"
    
    # Lectura del CSV con parseo de fechas
    df = pd.read_csv(ruta_csv, parse_dates=['fecha'], index_col='fecha')
    
    # Selección de la variable solicitada
    serie = df[variable].copy()
    
    # Asignación de frecuencia mensual (MS: Month Start)
    serie.index = pd.to_datetime(serie.index)
    serie = serie.asfreq('MS')
    
    return serie


# ============================================================================
# 2. PROMEDIO MÓVIL
# ============================================================================

def promedio_movil(serie: pd.Series, orden: int) -> pd.Series:
    """
    Calcula el promedio móvil centrado en el último mes de la ventana.
    
    Aplica una ventana móvil que incluye el mes actual y los (orden-1) meses
    anteriores, calculando la media de esos valores.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de tiempo con índice de fechas
    orden : int
        Tamaño de la ventana (número de meses incluidos)
    
    Retorna
    -------
    pd.Series
        Serie suavizada con promedio móvil
    
    Ejemplo
    -------
    >>> pm = promedio_movil(serie, 12)
    >>> print(pm.head())
    """
    # Aplicar rolling con ventana de tamaño 'orden'
    # center=False asegura que la ventana termina en el mes actual
    # min_periods=orden requiere todos los datos para calcular
    p_movil = serie.rolling(window=orden, center=False, min_periods=orden).mean()
    
    return p_movil


# ============================================================================
# 3. ÍNDICES ESTACIONALES (MODELO ADITIVO)
# ============================================================================

def indices_estacionales(serie: pd.Series) -> np.ndarray:
    """
    Calcula índices estacionales aditivos por mes.
    
    Para modelo aditivo: Y_t = T_t + S_t + E_t
    
    Índice estacional de cada mes = promedio de valores en ese mes - promedio general
    
    La suma de los 12 índices debe ser aproximadamente 0 (restricción aditiva).
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de tiempo con índice de fechas (frecuencia mensual)
    
    Retorna
    -------
    np.ndarray
        Array de 12 valores (índices para enero, febrero, ..., diciembre)
    
    Ejemplo
    -------
    >>> indices = indices_estacionales(serie)
    >>> print(f"Suma de índices: {indices.sum():.4f}")  # Debe ser ≈ 0
    >>> print(f"Enero: {indices[0]:.2f}, Febrero: {indices[1]:.2f}")
    """
    # Extraer mes de cada observación (1-12)
    meses = serie.index.month
    
    # Promedios por mes
    promedios_mensuales = np.array([
        serie[meses == mes].mean() for mes in range(1, 13)
    ])
    
    # Promedio general de toda la serie
    promedio_general = serie.mean()
    
    # Índices aditivos: desviación de cada mes respecto al promedio general
    indices = promedios_mensuales - promedio_general
    
    return indices


# ============================================================================
# 4. DESCOMPOSICIÓN DE SERIES (ADITIVA)
# ============================================================================

def descomponer(serie: pd.Series) -> Tuple:
    """
    Descompone la serie de tiempo en componentes: tendencia, estacionalidad y residuo.
    
    Utiliza el método de descomposición clásica aditiva de statsmodels:
    Y_t = Tendencia_t + Estacional_t + Residuo_t
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de tiempo con índice de fechas (debe tener al menos 2 períodos)
    
    Retorna
    -------
    tuple
        Tupla con 4 elementos:
        - componente trend: tendencia
        - componente seasonal: estacionalidad
        - componente resid: residuos
        - objeto descomposición completo de statsmodels
    
    Ejemplo
    -------
    >>> trend, estacional, residuo, descomp = descomponer(serie)
    >>> print(trend.head())
    """
    # Aplicar descomposición estacional (período = 12 meses)
    descomposicion = seasonal_decompose(
        serie,
        model='additive',  # Modelo aditivo
        period=12,         # Períodos en 1 año (12 meses)
        extrapolate_trend='period'  # Extrapolación para evitar NaN en bordes
    )
    
    return (
        descomposicion.trend,
        descomposicion.seasonal,
        descomposicion.resid,
        descomposicion
    )


# ============================================================================
# 5. MÉTODOS DE REFERENCIA (BENCHMARKS)
# ============================================================================

def metodos_referencia(entrenamiento: pd.Series, h: int) -> Dict[str, pd.Series]:
    """
    Genera pronósticos con tres métodos de referencia simples.
    
    Métodos:
    1. Ingenuo: último valor del entrenamiento para todos los h meses
    2. Estacional ingenuo: valor del mismo mes del año anterior
    3. Promedio: media de toda la serie de entrenamiento
    
    Parámetros
    ----------
    entrenamiento : pd.Series
        Serie de entrenamiento con índice de fechas
    h : int
        Horizonte de pronóstico (número de meses a pronosticar)
    
    Retorna
    -------
    dict
        Diccionario con claves 'ingenuo', 'estacional_ingenuo', 'promedio'
        Cada valor es un pd.Series con h pronósticos
    
    Ejemplo
    -------
    >>> pronosticos = metodos_referencia(entrenamiento, h=6)
    >>> print(pronosticos['ingenuo'])
    """
    # Crear fechas futuras para el pronóstico (frecuencia mensual)
    fecha_siguiente = entrenamiento.index[-1] + pd.DateOffset(months=1)
    fechas_futuras = pd.date_range(start=fecha_siguiente, periods=h, freq='MS')
    
    # -------- Método 1: Ingenuo (naive forecast) --------
    # Repite el último valor observado
    pron_ingenuo = pd.Series(
        data=[entrenamiento.iloc[-1]] * h,
        index=fechas_futuras,
        name='Ingenuo'
    )
    
    # -------- Método 2: Estacional ingenuo (seasonal naive) --------
    # Toma el valor del mismo mes hace 12 meses
    pron_estacional = []
    for i in range(h):
        fecha_fut = fechas_futuras[i]
        # Buscar el mes correspondiente hace 1 año (12 meses atrás)
        fecha_hace_un_ano = fecha_fut - pd.DateOffset(years=1)
        
        if fecha_hace_un_ano in entrenamiento.index:
            pron_estacional.append(entrenamiento[fecha_hace_un_ano])
        else:
            # Si no existe (primer año), usar el promedio disponible para ese mes
            mes = fecha_fut.month
            valores_mes = entrenamiento[entrenamiento.index.month == mes]
            if len(valores_mes) > 0:
                pron_estacional.append(valores_mes.mean())
            else:
                # Último recurso: usar media general
                pron_estacional.append(entrenamiento.mean())
    
    pron_estacional = pd.Series(
        data=pron_estacional,
        index=fechas_futuras,
        name='Estacional Ingenuo'
    )
    
    # -------- Método 3: Promedio (mean) --------
    # Pronóstico constante = media de entrenamiento
    pron_promedio = pd.Series(
        data=[entrenamiento.mean()] * h,
        index=fechas_futuras,
        name='Promedio'
    )
    
    return {
        'ingenuo': pron_ingenuo,
        'estacional_ingenuo': pron_estacional,
        'promedio': pron_promedio
    }


# ============================================================================
# 6. MÉTRICAS DE EVALUACIÓN
# ============================================================================

def metricas(real: pd.Series, pronostico: pd.Series) -> Dict[str, float]:
    """
    Calcula métricas de evaluación de pronósticos.
    
    Métricas:
    - MAE: Mean Absolute Error (error absoluto medio)
    - RMSE: Root Mean Squared Error (raíz del error cuadrado medio)
    - SMAPE: Symmetric Mean Absolute Percentage Error
            = 200 * media(|e_t| / (|y_t| + |ŷ_t|))
    
    Parámetros
    ----------
    real : pd.Series
        Valores reales (validación o test)
    pronostico : pd.Series
        Valores pronosticados
    
    Retorna
    -------
    dict
        Diccionario con las métricas: {'MAE': float, 'RMSE': float, 'SMAPE': float}
    
    Ejemplo
    -------
    >>> metr = metricas(validacion, pronostico_ingenuo)
    >>> print(f"MAE: {metr['MAE']:.2f}")
    """
    # Asegurar que tienen el mismo índice para comparación
    real_vals = real.values
    pron_vals = pronostico.values
    
    # Errores (residuos)
    errores = real_vals - pron_vals
    errores_abs = np.abs(errores)
    errores_cuad = errores ** 2
    
    # -------- MAE: Error Absoluto Medio --------
    mae = np.mean(errores_abs)
    
    # -------- RMSE: Raíz del Error Cuadrado Medio --------
    rmse = np.sqrt(np.mean(errores_cuad))
    
    # -------- SMAPE: Error Porcentual Absoluto Medio Simétrico --------
    # SMAPE = 200 * media(|e_t| / (|y_t| + |ŷ_t|))
    denominador = np.abs(real_vals) + np.abs(pron_vals)
    # Evitar división por cero
    denominador = np.where(denominador == 0, 1e-10, denominador)
    smape = 200 * np.mean(errores_abs / denominador)
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'SMAPE': smape
    }


# ============================================================================
# 7. CONCURSO DE MÉTODOS DE REFERENCIA
# ============================================================================

def concurso_referencia(ruta_muestra24: str = None) -> pd.DataFrame:
    """
    Ejecuta concurso de pronóstico con datos de muestra.
    
    Procesa un archivo CSV que contiene 24 meses de datos:
    - Primeros 18 meses: conjunto de entrenamiento
    - Últimos 6 meses: conjunto de validación/test
    
    Entrena los tres métodos de referencia con los 18 meses iniciales,
    genera pronósticos para los 6 meses finales, calcula métricas y
    retorna tabla ordenada por SMAPE (de menor a mayor).
    
    Parámetros
    ----------
    ruta_muestra24 : str, optional
        Ruta completa al archivo CSV. Si None, busca datos/muestra_series24.csv
    
    Retorna
    -------
    pd.DataFrame
        Tabla de resultados con columnas [Método, MAE, RMSE, SMAPE]
        ordenada ascendentemente por SMAPE
    
    Ejemplo
    -------
    >>> resultados = concurso_referencia()
    >>> print(resultados)
    """
    # Determinar ruta del archivo
    if ruta_muestra24 is None:
        ruta_proyecto = Path(__file__).parent.parent
        ruta_muestra24 = ruta_proyecto / "datos" / "muestra_series24.csv"
    else:
        ruta_muestra24 = Path(ruta_muestra24)
    
    # Cargar datos (esperado formato: fecha, valor)
    df = pd.read_csv(ruta_muestra24, parse_dates=['fecha'], index_col='fecha')
    serie_completa = df.iloc[:, 0].copy()  # Primera columna de valores
    serie_completa.index = pd.to_datetime(serie_completa.index)
    serie_completa = serie_completa.asfreq('MS')
    
    # División: 18 meses entrenamiento, 6 validación
    n_entrenamiento = 18
    entrenamiento = serie_completa.iloc[:n_entrenamiento]
    validacion = serie_completa.iloc[n_entrenamiento:]
    
    h = len(validacion)  # Horizonte = 6 meses
    
    # Generar pronósticos con los tres métodos
    pronosticos_dict = metodos_referencia(entrenamiento, h)
    
    # Calcular métricas para cada método
    resultados_lista = []
    for nombre_metodo, valores_pronostico in pronosticos_dict.items():
        metr = metricas(validacion, valores_pronostico)
        resultados_lista.append({
            'Método': nombre_metodo.replace('_', ' ').title(),
            'MAE': metr['MAE'],
            'RMSE': metr['RMSE'],
            'SMAPE': metr['SMAPE']
        })
    
    # Crear DataFrame y ordenar por SMAPE (ascendente = mejor primero)
    resultados_df = pd.DataFrame(resultados_lista)
    resultados_df = resultados_df.sort_values(by='SMAPE', ascending=True)
    resultados_df = resultados_df.reset_index(drop=True)
    
    return resultados_df


# ============================================================================
# 8. AUTOTS: PRONÓSTICO AUTOMÁTICO CON SELECCIÓN GENÉTICA
# ============================================================================

def ejecutar_autots(
    serie: pd.Series,
    horizonte: int,
    model_list: str = "superfast",
    generaciones: int = 5,
    validaciones: int = 2,
    intervalo: float = 0.9,
    semilla: int = None
) -> Dict:
    """
    Ejecuta AutoTS para encontrar automáticamente el mejor modelo de pronóstico.
    
    Analogía: Como un ensayo de evaluación de variedades agrícolas donde:
    - Las "generaciones" son ciclos de siembra y selección
    - Los "modelos" son diferentes variedades de cultivo
    - Las "validaciones" son cosechas de prueba (backtesting)
    - El "intervalo de confianza" es el rango de rendimiento esperado
    - El "ensemble" (mezcla) es usar múltiples variedades juntas
    
    AutoTS evalúa automáticamente cientos de modelos (ARIMA, Prophet, TBATS, etc.)
    en múltiples "generaciones" (iteraciones) y retiene los mejores según
    validación hacia atrás (backwards), mejorando progresivamente.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de tiempo con índice de fechas (frecuencia mensual)
    horizonte : int
        Número de meses a pronosticar en el futuro
    model_list : str, default "superfast"
        Conjunto de modelos a evaluar ("superfast", "fast", "default", etc.)
    generaciones : int, default 5
        Número de iteraciones de evolución/selección (más = mejor pero más lento)
    validaciones : int, default 2
        Número de períodos de validación hacia atrás (backtesting)
    intervalo : float, default 0.9
        Nivel de confianza para límites (0.9 = 90%, 0.95 = 95%)
    semilla : int, optional
        Semilla para reproducibilidad
    
    Retorna
    -------
    dict
        Diccionario con claves:
        - 'pronostico': DataFrame con fecha, pronostico_mm, limite_inferior_mm, limite_superior_mm
        - 'modelo_nombre': nombre del mejor modelo
        - 'modelo_params': parámetros del mejor modelo
        - 'modelo_transformaciones': transformaciones aplicadas
        - 'top_10_modelos': DataFrame con top 10 modelos (Model, smape, mae, rmse, Score)
        - 'objeto_autots': objeto AutoTS completo para análisis posterior
    
    Ejemplo
    -------
    >>> resultado = ejecutar_autots(serie_precip, horizonte=12, generaciones=3)
    >>> print(resultado['modelo_nombre'])
    >>> print(resultado['top_10_modelos'])
    """
    # Importar AutoTS (librería de pronóstico automático)
    from autots import AutoTS
    
    # Validar entrada
    if len(serie) < 24:
        raise ValueError("Serie debe tener al menos 24 observaciones para AutoTS")
    
    # Configurar semilla para reproducibilidad
    if semilla is not None:
        np.random.seed(semilla)
    
    # -------- CREAR MODELO AUTOTS --------
    # AutoTS es como un sistema automático de evaluación de variedades:
    # - frequency="MS": datos mensuales (Month Start)
    # - max_generaciones: ciclos de selección (cada generación evalúa y mejora)
    # - num_validaciones: cuántos períodos "hacia atrás" se valida (backtesting)
    # - intervalo: rango de confianza para límites de pronóstico
    # - model_list: conjunto de modelos candidatos ("superfast" = quick & good)
    # - ensemble: None = no mezclar modelos, None = usar solo el mejor
    # - transformer_list: "superfast" = transformaciones rápidas (log, detrend)
    # - validation_method: "backwards" = validar hacia atrás (como pruebas históricas)
    # - no_negatives: True = no permitir pronósticos negativos (para precipitación)
    # - n_jobs: 1 = usar 1 procesador (más = paralelización)
    # - verbose: 0 = silencioso, no imprimir progreso
    
    autots_modelo = AutoTS(
        forecast_length=horizonte,      # Horizonte de pronóstico
        frequency="MS",                 # Frecuencia: Month Start (mensual)
        max_generations=generaciones,   # Número de "generaciones" de selección
        num_validations=validaciones,   # Número de validaciones hacia atrás
        prediction_interval=intervalo,  # Nivel de confianza (e.g., 0.9 = 90%)
        model_list=model_list,          # Conjunto de modelos: "superfast"
        ensemble=None,                  # No usar ensemble (solo mejor modelo)
        transformer_list="superfast",   # Transformaciones rápidas
        validation_method="backwards",  # Método: validación hacia atrás
        no_negatives=True,              # No permitir valores negativos
        random_seed=semilla             # Semilla para reproducibilidad
    )
    
    # -------- ENTRENAR AUTOTS --------
    # Convertir serie a DataFrame (AutoTS lo requiere)
    datos_entrada = pd.DataFrame({
        'valor': serie.values
    }, index=serie.index)
    
    # Ajustar AutoTS: evalúa y selecciona modelos en múltiples generaciones
    # (Como un proceso de selección natural: generación → evaluación → mejor)
    autots_modelo.fit(datos_entrada)
    
    # -------- OBTENER MEJOR MODELO --------
    # Después de "generaciones" de evolución, tenemos el mejor modelo
    mejor_modelo = autots_modelo.model
    nombre_mejor = autots_modelo.best_model_name  # Ej: "ARIMA", "Prophet"
    params_mejor = autots_modelo.best_model_params
    trans_mejor = autots_modelo.best_model_transformation_params
    
    # -------- GENERAR PRONÓSTICOS CON INTERVALOS --------
    # Pronósticar horizonte meses, con límites inferior y superior
    pronosticos = autots_modelo.predict(
        forecast_length=horizonte,
        prediction_interval=intervalo  # Intervalo de confianza
    )
    
    # Extraer pronósticos y límites (PredictionObject tiene atributos)
    valores_pronostico = pronosticos.forecast.values.flatten()
    limites_inf = pronosticos.lower_forecast.values.flatten()
    limites_sup = pronosticos.upper_forecast.values.flatten()
    
    # Crear fechas futuras para los pronósticos
    fecha_siguiente = serie.index[-1] + pd.DateOffset(months=1)
    fechas_pronostico = pd.date_range(start=fecha_siguiente, periods=horizonte, freq='MS')
    
    # Crear DataFrame de pronósticos
    df_pronostico = pd.DataFrame({
        'fecha': fechas_pronostico,
        'pronostico_mm': valores_pronostico,
        'limite_inferior_mm': limites_inf,
        'limite_superior_mm': limites_sup
    })
    
    # -------- OBTENER TOP 10 MODELOS --------
    # Tabla de rankings (como tabla de resultados de una evaluación de variedades)
    # Muestra los 10 mejores modelos según SMAPE (error porcentual)
    resultados_validacion = autots_modelo.results("validation")
    
    # Seleccionar top 10 y renombrar columnas
    top_10 = resultados_validacion.head(10)[['Model', 'smape', 'mae', 'rmse', 'Score']].copy()
    top_10 = top_10.reset_index(drop=True)
    
    # -------- RETORNAR RESULTADO --------
    return {
        'pronostico': df_pronostico,
        'modelo_nombre': nombre_mejor,
        'modelo_params': params_mejor,
        'modelo_transformaciones': trans_mejor,
        'top_10_modelos': top_10,
        'objeto_autots': autots_modelo
    }


if __name__ == "__main__":
    """
    Ejecutar análisis de concurso con datos de muestra.
    
    Comando: .venv/bin/python -m src.series
    """
    print("=" * 70)
    print("CONCURSO DE MÉTODOS DE REFERENCIA - MUESTRA 24 MESES")
    print("=" * 70)
    print()
    
    # Ejecutar concurso
    tabla_resultados = concurso_referencia()
    
    # Mostrar resultados
    print(tabla_resultados.to_string(index=False))
    print()
    
    # Análisis de ganador
    print("=" * 70)
    mejor_metodo = tabla_resultados.iloc[0]
    print(f"🏆 Mejor método: {mejor_metodo['Método']}")
    print(f"   SMAPE: {mejor_metodo['SMAPE']:.4f}")
    print(f"   MAE:   {mejor_metodo['MAE']:.4f}")
    print(f"   RMSE:  {mejor_metodo['RMSE']:.4f}")
    print("=" * 70)
