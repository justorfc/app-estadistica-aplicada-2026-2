"""
Módulo: Modelos Semiempíricos de Secado
========================================

Ajuste de curvas de secado con 5 modelos semiempíricos y comparación
mediante información de Akaike corregida (AICc).

Modelos disponibles:
1. Lewis: MR = exp(-k·t)
2. Henderson-Pabis: MR = a·exp(-k·t)
3. Page: MR = exp(-k·t^n)
4. Logarítmico: MR = a·exp(-k·t) + c
5. Dos Términos: MR = a·exp(-k0·t) + b·exp(-k1·t)

El ratio de humedad (MR) se define como:
  MR = (M_t - M_∞) / (M_0 - M_∞)
donde M_t es humedad en tiempo t, M_0 inicial, M_∞ de equilibrio.

Referencia: ASAE D245.4 (1992), ASAE Standards.
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# DICCIONARIO DE MODELOS
# ============================================================================

def lewis(t, k):
    """
    Modelo de Lewis.
    
    MR = exp(-k·t)
    
    Parámetros
    ----------
    t : array
        Tiempo (h)
    k : float
        Constante de secado (h⁻¹)
    
    Retorna
    -------
    array
        Ratio de humedad MR
    """
    return np.exp(-k * t)


def henderson_pabis(t, a, k):
    """
    Modelo de Henderson-Pabis.
    
    MR = a·exp(-k·t)
    
    Parámetros
    ----------
    t : array
        Tiempo (h)
    a : float
        Factor (≈1)
    k : float
        Constante de secado (h⁻¹)
    
    Retorna
    -------
    array
        Ratio de humedad MR
    """
    return a * np.exp(-k * t)


def page(t, k, n):
    """
    Modelo de Page.
    
    MR = exp(-k·t^n)
    
    Parámetros
    ----------
    t : array
        Tiempo (h)
    k : float
        Constante de secado (h⁻ⁿ)
    n : float
        Exponente (≈1)
    
    Retorna
    -------
    array
        Ratio de humedad MR
    """
    return np.exp(-k * t**n)


def logaritmico(t, a, k, c):
    """
    Modelo Logarítmico.
    
    MR = a·exp(-k·t) + c
    
    Parámetros
    ----------
    t : array
        Tiempo (h)
    a : float
        Factor (≈1)
    k : float
        Constante de secado (h⁻¹)
    c : float
        Término constante (≈0)
    
    Retorna
    -------
    array
        Ratio de humedad MR
    """
    return a * np.exp(-k * t) + c


def dos_terminos(t, a, k0, b, k1):
    """
    Modelo de Dos Términos.
    
    MR = a·exp(-k0·t) + b·exp(-k1·t)
    
    Parámetros
    ----------
    t : array
        Tiempo (h)
    a : float
        Factor del primer término (≈0.5)
    k0 : float
        Constante del primer término (h⁻¹)
    b : float
        Factor del segundo término (≈0.5)
    k1 : float
        Constante del segundo término (h⁻¹)
    
    Retorna
    -------
    array
        Ratio de humedad MR
    """
    return a * np.exp(-k0 * t) + b * np.exp(-k1 * t)


# Diccionario con los modelos y valores iniciales
MODELOS_SECADO = {
    'Lewis': {
        'func': lewis,
        'params': ['k'],
        'initial_guess': [0.1],
        'bounds': ([0.001], [10])
    },
    'Henderson-Pabis': {
        'func': henderson_pabis,
        'params': ['a', 'k'],
        'initial_guess': [1.0, 0.1],
        'bounds': ([0.5, 0.001], [1.5, 10])
    },
    'Page': {
        'func': page,
        'params': ['k', 'n'],
        'initial_guess': [0.1, 1.0],
        'bounds': ([0.001, 0.5], [10, 3])
    },
    'Logarítmico': {
        'func': logaritmico,
        'params': ['a', 'k', 'c'],
        'initial_guess': [1.0, 0.1, 0.0],
        'bounds': ([0.5, 0.001, -0.5], [1.5, 10, 0.5])
    },
    'Dos Términos': {
        'func': dos_terminos,
        'params': ['a', 'k0', 'b', 'k1'],
        'initial_guess': [0.5, 0.05, 0.5, 0.15],
        'bounds': ([0.01, 0.001, 0.01, 0.001], [1.5, 10, 1.5, 10])
    }
}


# ============================================================================
# AJUSTE DE CURVA
# ============================================================================

def ajustar_curva(t, MR, nombre):
    """
    Ajusta un modelo semiempírico de secado a datos observados.
    
    Utiliza mínimos cuadrados no lineales (Levenberg-Marquardt).
    
    Parámetros
    ----------
    t : array
        Tiempos (h)
    MR : array
        Ratios de humedad observados
    nombre : str
        Nombre del modelo ('Lewis', 'Henderson-Pabis', 'Page', 'Logarítmico', 'Dos Términos')
    
    Retorna
    -------
    tuple
        (parámetros ajustados, covarianza)
    
    Ejemplo
    -------
    >>> params, cov = ajustar_curva(t_data, MR_data, 'Page')
    >>> MR_pred = page(t_data, params[0], params[1])
    """
    if nombre not in MODELOS_SECADO:
        raise ValueError(f"Modelo '{nombre}' no reconocido")
    
    modelo_info = MODELOS_SECADO[nombre]
    func = modelo_info['func']
    p0 = modelo_info['initial_guess']
    bounds = modelo_info['bounds']
    
    try:
        # Ajuste con curve_fit
        popt, pcov = curve_fit(
            func, t, MR,
            p0=p0,
            bounds=bounds,
            maxfev=10000,
            ftol=1e-10
        )
        return popt, pcov
    except RuntimeError:
        # Si falla el ajuste, retornar valores iniciales
        return np.array(p0), None


# ============================================================================
# MÉTRICAS DE BONDAD DE AJUSTE
# ============================================================================

def metricas_curva(MR_obs, MR_ajust, k):
    """
    Calcula métricas de bondad de ajuste para una curva de secado.
    
    Parámetros
    ----------
    MR_obs : array
        Valores observados
    MR_ajust : array
        Valores ajustados
    k : int
        Número de parámetros del modelo
    
    Retorna
    -------
    dict
        Diccionario con:
        - 'R2': Coeficiente de determinación
        - 'RMSE': Raíz del error cuadrático medio (√(MSE))
        - 'chi2_red': Chi-cuadrado reducido
        - 'AIC': Criterio de información de Akaike
        - 'AICc': AIC corregido (para muestras pequeñas)
    
    Fórmulas
    --------
    R² = 1 - (SS_res / SS_tot)
    
    RMSE = √(Σ(y_i - ŷ_i)² / n)
    
    χ² reducido = Σ(y_i - ŷ_i)² / (n - k)
    
    AIC = n·ln(SCE/n) + 2k
      donde SCE = Σ(y_i - ŷ_i)²
    
    AICc = AIC + 2k(k+1)/(n-k-1)
    
    Ejemplo
    -------
    >>> metricas = metricas_curva(MR_obs, MR_pred, k=2)
    >>> print(f"R² = {metricas['R2']:.4f}, AICc = {metricas['AICc']:.2f}")
    """
    n = len(MR_obs)
    
    # Residuos
    residuos = MR_obs - MR_ajust
    
    # Suma de cuadrados
    SS_res = np.sum(residuos**2)
    SS_tot = np.sum((MR_obs - np.mean(MR_obs))**2)
    
    # R² (coeficiente de determinación)
    R2 = 1 - (SS_res / SS_tot) if SS_tot != 0 else 0
    
    # RMSE (raíz del error cuadrático medio)
    RMSE = np.sqrt(SS_res / n)
    
    # Chi-cuadrado reducido
    chi2_red = SS_res / (n - k) if (n - k) > 0 else np.inf
    
    # AIC = n·ln(SCE/n) + 2k
    AIC = n * np.log(SS_res / n) + 2 * k
    
    # AICc = AIC + 2k(k+1)/(n-k-1)
    if n - k - 1 > 0:
        AICc = AIC + 2 * k * (k + 1) / (n - k - 1)
    else:
        AICc = np.inf
    
    return {
        'R2': R2,
        'RMSE': RMSE,
        'chi2_red': chi2_red,
        'AIC': AIC,
        'AICc': AICc,
        'residuos': residuos
    }


# ============================================================================
# TABLA COMPARATIVA DE MODELOS
# ============================================================================

def tabla_modelos(t, MR):
    """
    Ajusta todos los modelos y retorna tabla comparativa ordenada por AICc.
    
    Parámetros
    ----------
    t : array
        Tiempos (h)
    MR : array
        Ratios de humedad observados
    
    Retorna
    -------
    DataFrame
        Tabla con una fila por modelo, columnas:
        - 'Modelo': nombre del modelo
        - 'Parámetros': string con valores ajustados
        - 'k': número de parámetros
        - 'R²': coeficiente de determinación
        - 'RMSE': raíz del error cuadrático medio
        - 'χ² reducido': chi-cuadrado reducido
        - 'AICc': criterio de información corregido
        - 'ΔAICc': diferencia respecto al mejor modelo
        - 'Interpretación': soporte sustancial, considerablemente menos, sin soporte
        - 'params_tuple': tupla de parámetros (para uso posterior)
        - 'residuos': vector de residuos
    
    Ejemplo
    -------
    >>> tabla = tabla_modelos(t_data, MR_data)
    >>> print(tabla[['Modelo', 'R²', 'AICc']].to_string())
    """
    datos_tabla = []
    
    for nombre_modelo, info_modelo in MODELOS_SECADO.items():
        # Ajustar modelo
        params, _ = ajustar_curva(t, MR, nombre_modelo)
        
        # Predicciones
        func = info_modelo['func']
        MR_ajust = func(t, *params)
        
        # Número de parámetros
        k = len(params)
        
        # Métricas
        metricas = metricas_curva(MR, MR_ajust, k)
        
        # String de parámetros
        param_names = info_modelo['params']
        param_str = ", ".join([f"{name}={val:.4f}" for name, val in zip(param_names, params)])
        
        datos_tabla.append({
            'Modelo': nombre_modelo,
            'Parámetros': param_str,
            'k': k,
            'R²': metricas['R2'],
            'RMSE': metricas['RMSE'],
            'χ² reducido': metricas['chi2_red'],
            'AICc': metricas['AICc'],
            'AIC': metricas['AIC'],
            'params_tuple': tuple(params),
            'residuos': metricas['residuos']
        })
    
    # Crear DataFrame
    df = pd.DataFrame(datos_tabla)
    
    # Ordenar por AICc
    df = df.sort_values('AICc').reset_index(drop=True)
    
    # Calcular ΔAICc (diferencia respecto al mejor modelo)
    AICc_min = df['AICc'].iloc[0]
    df['ΔAICc'] = df['AICc'] - AICc_min
    
    # Interpretación de ΔAICc según Burnham & Anderson (2002)
    def interpretar_daic(daic):
        if daic < 2:
            return "Soporte sustancial"
        elif daic < 7:
            return "Considerablemente menos"
        else:
            return "Esencialmente sin soporte"
    
    df['Interpretación'] = df['ΔAICc'].apply(interpretar_daic)
    
    return df


# ============================================================================
# PRUEBA DEL MÓDULO
# ============================================================================

if __name__ == "__main__":
    import pandas as pd
    
    print("="*80)
    print("PRUEBA DEL MÓDULO: MODELOS DE SECADO")
    print("="*80)
    
    # Generar datos de prueba (simulados con modelo Page)
    np.random.seed(42)
    t_test = np.array([0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20])
    MR_true = page(t_test, k=0.1, n=1.3)
    MR_obs = MR_true + np.random.normal(0, 0.02, len(t_test))  # Ruido
    MR_obs = np.clip(MR_obs, 0, 1)  # Clip entre 0 y 1
    
    print("\nDatos de prueba (14 puntos, generados con modelo Page):")
    print(f"  Tiempo (h): {t_test}")
    print(f"  MR observado: {MR_obs.round(4)}")
    
    # Ajustar tabla de modelos
    print("\nAjustando 5 modelos...")
    tabla = tabla_modelos(t_test, MR_obs)
    
    print("\nTABLA COMPARATIVA (ordenada por AICc):")
    print("="*80)
    
    tabla_display = tabla[['Modelo', 'Parámetros', 'k', 'R²', 'RMSE', 'AICc', 'ΔAICc', 'Interpretación']].copy()
    
    for col in ['R²', 'RMSE', 'AICc', 'ΔAICc']:
        tabla_display[col] = tabla_display[col].apply(lambda x: f"{x:.4f}")
    
    print(tabla_display.to_string(index=False))
    
    print("\n" + "="*80)
    mejor_modelo = tabla.iloc[0]['Modelo']
    mejor_aicc = tabla.iloc[0]['AICc']
    print(f"✓ Mejor modelo por AICc: {mejor_modelo} (AICc = {mejor_aicc:.2f})")
    print("="*80)
