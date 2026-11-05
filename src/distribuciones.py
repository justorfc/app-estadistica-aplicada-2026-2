"""
Módulo para seleccionar el mejor modelo de distribución de probabilidad
para la precipitación máxima anual usando múltiples criterios de ajuste.

Este módulo implementa:
- Ajuste por máxima verosimilitud de 6 distribuciones candidatas
- Criterios de información: AIC, BIC, AICc
- Pruebas de bondad de ajuste: Kolmogorov-Smirnov y Anderson-Darling
- Tabla comparativa con interpretación
- Cálculo de cuantiles de retorno
- Intervalos de confianza por bootstrap paramétrico
- Método de momentos para Gumbel (como cálculo manual)
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import (
    norm, lognorm, gamma, weibull_min, gumbel_r, genextreme
)
import warnings

# Suprimir advertencias de convergencia que pueden no ser relevantes
warnings.filterwarnings('ignore', category=RuntimeWarning)


# ============================================================================
# 1. DICCIONARIO DE DISTRIBUCIONES CANDIDATAS
# ============================================================================

DISTRIBUCIONES_CANDIDATAS = {
    'Normal': norm,
    'Lognormal': lognorm,  # loc fijo en 0
    'Gamma': gamma,         # loc fijo en 0
    'Weibull': weibull_min, # loc fijo en 0
    'Gumbel': gumbel_r,
    'GEV': genextreme       # NOTA: en scipy, c = -ξ (opuesto del índice de forma)
}


# ============================================================================
# 2. AJUSTE POR MÁXIMA VEROSIMILITUD
# ============================================================================

def ajustar(datos, nombre):
    """
    Ajusta una distribución a datos por máxima verosimilitud.
    
    Para distribuciones con parámetros fijos (loc), el número de parámetros
    libres no los incluye.
    
    Parámetros
    ----------
    datos : array-like
        Datos de precipitación máxima anual (mm)
    nombre : str
        Nombre de la distribución ('Normal', 'Lognormal', 'Gamma', etc.)
    
    Retorna
    -------
    params : tuple
        Parámetros estimados (sin incluir loc ni scale si están fijos)
    k : int
        Número de parámetros libres (sin contar los fijos)
    
    Ejemplo
    -------
    >>> params, k = ajustar(datos, 'Gumbel')
    >>> print(f"Gumbel: loc={params[0]:.2f}, scale={params[1]:.2f}, k={k}")
    """
    datos = np.asarray(datos)
    dist = DISTRIBUCIONES_CANDIDATAS[nombre]
    
    if nombre == 'Normal':
        # Normal(loc, scale) → 2 parámetros libres
        params = dist.fit(datos)
        k = 2
    elif nombre == 'Lognormal':
        # Lognormal(s, loc=0, scale) → s y scale libres, loc fijo en 0
        params = dist.fit(datos, floc=0)
        k = 2
    elif nombre == 'Gamma':
        # Gamma(a, loc=0, scale) → a y scale libres, loc fijo en 0
        params = dist.fit(datos, floc=0)
        k = 2
    elif nombre == 'Weibull':
        # Weibull(c, loc=0, scale) → c y scale libres, loc fijo en 0
        params = dist.fit(datos, floc=0)
        k = 2
    elif nombre == 'Gumbel':
        # Gumbel(loc, scale) → 2 parámetros libres
        params = dist.fit(datos)
        k = 2
    elif nombre == 'GEV':
        # GEV(c, loc, scale) → 3 parámetros libres
        # NOTA: c = -ξ, donde ξ es el índice de forma usual
        params = dist.fit(datos)
        k = 3
    else:
        raise ValueError(f"Distribución desconocida: {nombre}")
    
    return params, k


# ============================================================================
# 3. LOG-VEROSIMILITUD
# ============================================================================

def log_verosimilitud(datos, nombre, params):
    """
    Calcula la log-verosimilitud de una distribución ajustada.
    
    ℓ = Σ ln(f(x_i | θ)) donde f es la función de densidad.
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    nombre : str
        Nombre de la distribución
    params : tuple
        Parámetros estimados (como retorna ajustar())
    
    Retorna
    -------
    ll : float
        Log-verosimilitud total (suma de logpdf)
    
    Ejemplo
    -------
    >>> ll = log_verosimilitud(datos, 'Gumbel', params)
    """
    datos = np.asarray(datos)
    dist = DISTRIBUCIONES_CANDIDATAS[nombre]
    
    if nombre in ['Lognormal', 'Gamma', 'Weibull']:
        # Estas tienen loc fijo en 0: params = (shape, loc, scale)
        logpdf_vals = dist.logpdf(datos, params[0], loc=0, scale=params[2])
    else:
        # Normal y Gumbel: params = (loc, scale)
        # GEV: params = (c, loc, scale)
        logpdf_vals = dist.logpdf(datos, *params)
    
    ll = np.sum(logpdf_vals)
    return ll


# ============================================================================
# 4. CRITERIOS DE INFORMACIÓN (AIC, BIC, AICc)
# ============================================================================

def criterios_informacion(datos, nombre, params):
    """
    Calcula criterios de información para comparación de modelos.
    
    AIC = 2k - 2ℓ          (Criterio de Información de Akaike)
    BIC = k·ln(n) - 2ℓ     (Criterio de Información Bayesiano)
    AICc = AIC + 2k(k+1)/(n-k-1)  (AIC corregido, preferible si n/k < 40)
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    nombre : str
        Nombre de la distribución
    params : tuple
        Parámetros estimados
    
    Retorna
    -------
    dict con claves 'AIC', 'BIC', 'AICc'
    
    Ejemplo
    -------
    >>> crit = criterios_informacion(datos, 'Gumbel', params)
    >>> print(f"AIC={crit['AIC']:.2f}, BIC={crit['BIC']:.2f}")
    """
    n = len(datos)
    _, k = ajustar(datos, nombre)
    ll = log_verosimilitud(datos, nombre, params)
    
    aic = 2 * k - 2 * ll
    bic = k * np.log(n) - 2 * ll
    aicc = aic + (2 * k * (k + 1)) / (n - k - 1) if n > k + 1 else aic
    
    return {'AIC': aic, 'BIC': bic, 'AICc': aicc}


# ============================================================================
# 5. BONDAD DE AJUSTE (K-S y Anderson-Darling)
# ============================================================================

def bondad_ajuste(datos, nombre, n_mc=199):
    """
    Calcula estadísticos y valores p de pruebas de bondad de ajuste.
    
    Utiliza:
    - Kolmogorov-Smirnov: máxima distancia entre empírica y teórica
    - Anderson-Darling: suma ponderada de desviaciones (pesa más colas)
    
    Ambos con valor p por Monte Carlo (corrige problema de Lilliefors).
    También calcula el valor p "ingenuo" de kstest (Kolmogorov original, sin corrección).
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    nombre : str
        Nombre de la distribución
    n_mc : int
        Número de simulaciones Monte Carlo para el valor p
    
    Retorna
    -------
    dict con:
        'KS_stat': estadístico de K-S
        'KS_pvalue_mc': valor p de K-S por Monte Carlo (recomendado)
        'KS_pvalue_naive': valor p de K-S ingenuo (sin corrección)
        'AD_stat': estadístico de Anderson-Darling
        'AD_pvalue_mc': valor p de Anderson-Darling por Monte Carlo
    
    Ejemplo
    -------
    >>> ba = bondad_ajuste(datos, 'Gumbel', n_mc=199)
    >>> print(f"KS valor p = {ba['KS_pvalue_mc']:.4f}")
    """
    datos = np.asarray(datos)
    params, _ = ajustar(datos, nombre)
    dist = DISTRIBUCIONES_CANDIDATAS[nombre]
    
    # Usar scipy.stats.goodness_of_fit (disponible en scipy >= 1.7.0)
    # que calcula valores p por Monte Carlo y corrige el problema de Lilliefors
    
    result_ks = stats.goodness_of_fit(
        dist, datos, 
        statistic='ks',
        n_mc_samples=n_mc,
        random_state=42
    )
    
    result_ad = stats.goodness_of_fit(
        dist, datos,
        statistic='ad',
        n_mc_samples=n_mc,
        random_state=42
    )
    
    # Valor p "ingenuo" de kstest para comparación
    if nombre in ['Lognormal', 'Gamma', 'Weibull']:
        cdf_func = lambda x: dist.cdf(x, params[0], loc=0, scale=params[1])
    else:
        cdf_func = lambda x: dist.cdf(x, *params)
    
    ks_naive_result = stats.kstest(datos, cdf_func)
    
    return {
        'KS_stat': result_ks.statistic,
        'KS_pvalue_mc': result_ks.pvalue,
        'KS_pvalue_naive': ks_naive_result.pvalue,
        'AD_stat': result_ad.statistic,
        'AD_pvalue_mc': result_ad.pvalue
    }


# ============================================================================
# 6. TABLA COMPARATIVA
# ============================================================================

def tabla_comparativa(datos, n_mc=199):
    """
    Genera tabla comparativa de todas las distribuciones candidatas.
    
    Incluye: parámetros, k, log-verosimilitud, AIC, BIC, AICc, ΔAIC,
    interpretación de ΔAIC, estadísticos de bondad, valores p, rechazo H₀.
    
    Interpretación ΔAIC (Burnham & Anderson):
    - ΔAIC < 2: soporte sustancial
    - ΔAIC 4-7: considerablemente menos soporte
    - ΔAIC > 10: esencialmente sin soporte
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    n_mc : int
        Número de simulaciones Monte Carlo
    
    Retorna
    -------
    pd.DataFrame con una fila por distribución, ordenada por AIC
    
    Ejemplo
    -------
    >>> tabla = tabla_comparativa(datos, n_mc=199)
    >>> print(tabla)
    """
    datos = np.asarray(datos)
    resultados = []
    
    # Ajustar cada distribución
    for nombre in DISTRIBUCIONES_CANDIDATAS.keys():
        params, k = ajustar(datos, nombre)
        ll = log_verosimilitud(datos, nombre, params)
        crit = criterios_informacion(datos, nombre, params)
        ba = bondad_ajuste(datos, nombre, n_mc=n_mc)
        
        # Guardar parámetros como string
        if nombre == 'Normal':
            params_str = f"μ={params[0]:.2f}, σ={params[1]:.2f}"
        elif nombre == 'Lognormal':
            # params = (s, loc, scale) pero loc es 0 (fijo)
            params_str = f"s={params[0]:.2f}, σ={params[2]:.2f}"
        elif nombre == 'Gamma':
            # params = (a, loc, scale) pero loc es 0 (fijo)
            params_str = f"α={params[0]:.2f}, β={params[2]:.2f}"
        elif nombre == 'Weibull':
            # params = (c, loc, scale) pero loc es 0 (fijo)
            params_str = f"c={params[0]:.2f}, σ={params[2]:.2f}"
        elif nombre == 'Gumbel':
            params_str = f"μ={params[0]:.2f}, β={params[1]:.2f}"
        elif nombre == 'GEV':
            params_str = f"ξ={-params[0]:.2f}, μ={params[1]:.2f}, σ={params[2]:.2f}"
        
        resultados.append({
            'Distribución': nombre,
            'Parámetros': params_str,
            'k': k,
            'ℓ (log-vero)': ll,
            'AIC': crit['AIC'],
            'BIC': crit['BIC'],
            'AICc': crit['AICc'],
            'KS_stat': ba['KS_stat'],
            'KS_pvalue_mc': ba['KS_pvalue_mc'],
            'KS_pvalue_naive': ba['KS_pvalue_naive'],
            'AD_stat': ba['AD_stat'],
            'AD_pvalue_mc': ba['AD_pvalue_mc'],
            'params_tuple': params  # para uso interno
        })
    
    df = pd.DataFrame(resultados)
    
    # Ordenar por AIC
    df = df.sort_values('AIC').reset_index(drop=True)
    
    # Calcular ΔAIC respecto al mínimo
    aic_min = df['AIC'].min()
    df['ΔAIC'] = df['AIC'] - aic_min
    
    # Interpretación de ΔAIC
    def interpretar_daic(delta_aic):
        if delta_aic < 2:
            return "Soporte sustancial"
        elif delta_aic < 4:
            return "Menos soporte"
        elif delta_aic <= 7:
            return "Considerablemente menos"
        else:
            return "Esencialmente sin soporte"
    
    df['Interpretación ΔAIC'] = df['ΔAIC'].apply(interpretar_daic)
    
    # Rechazo H₀ al nivel 5%
    df['Rechaza H₀ (KS 5%)'] = df['KS_pvalue_mc'] < 0.05
    df['Rechaza H₀ (AD 5%)'] = df['AD_pvalue_mc'] < 0.05
    
    return df


# ============================================================================
# 7. POSICIONES GRÁFICAS PARA Q-Q PLOTS
# ============================================================================

def posiciones_graficas(datos):
    """
    Calcula posiciones gráficas para diagramas de probabilidad.
    
    Retorna datos ordenados, posición de Weibull p = i/(n+1),
    posición de Gringorten p = (i - 0.44)/(n + 0.12), y
    período de retorno empírico T = 1/(1 - p).
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    
    Retorna
    -------
    dict con:
        'datos_ord': datos ordenados
        'weibull': posiciones de Weibull
        'gringorten': posiciones de Gringorten
        'periodo_retorno': período de retorno empírico
    
    Ejemplo
    -------
    >>> pos = posiciones_graficas(datos)
    >>> plt.scatter(pos['datos_ord'], pos['periodo_retorno'])
    """
    datos = np.asarray(datos)
    datos_ord = np.sort(datos)
    n = len(datos)
    
    # Índices i = 1, 2, ..., n
    i = np.arange(1, n + 1)
    
    # Posición de Weibull: p = i / (n + 1)
    weibull = i / (n + 1)
    
    # Posición de Gringorten: p = (i - 0.44) / (n + 0.12)
    gringorten = (i - 0.44) / (n + 0.12)
    
    # Período de retorno empírico: T = 1 / (1 - p)
    # Usamos Weibull por defecto
    periodo_retorno = 1 / (1 - weibull)
    
    return {
        'datos_ord': datos_ord,
        'weibull': weibull,
        'gringorten': gringorten,
        'periodo_retorno': periodo_retorno
    }


# ============================================================================
# 8. CUANTIL DE PERÍODO DE RETORNO
# ============================================================================

def cuantil_retorno(nombre, params, T):
    """
    Calcula el cuantil x_T = F⁻¹(1 - 1/T) para período de retorno T.
    
    Esto es: dado un período de retorno T años, ¿qué precipitación
    tiene probabilidad 1 - 1/T de no ser excedida en un año?
    
    Parámetros
    ----------
    nombre : str
        Nombre de la distribución
    params : tuple
        Parámetros estimados (como retorna ajustar())
    T : float o array
        Período de retorno en años (2, 5, 10, 25, 50, 100, etc.)
    
    Retorna
    -------
    float o array
        Cuantil x_T
    
    Ejemplo
    -------
    >>> x_100 = cuantil_retorno('Gumbel', params, 100)
    >>> print(f"Precipitación esperada cada 100 años: {x_100:.2f} mm")
    """
    dist = DISTRIBUCIONES_CANDIDATAS[nombre]
    
    # Probabilidad acumulada: F = 1 - 1/T
    F = 1 - 1 / np.asarray(T)
    
    if nombre in ['Lognormal', 'Gamma', 'Weibull']:
        x_T = dist.ppf(F, params[0], loc=0, scale=params[1])
    else:
        x_T = dist.ppf(F, *params)
    
    return x_T


# ============================================================================
# 9. RIESGO DE FALLA
# ============================================================================

def riesgo_falla(T, N):
    """
    Calcula la probabilidad de que precipitación de período T sea excedida
    al menos una vez en N años.
    
    R = 1 - (1 - 1/T)^N
    
    Esto es útil para diseño de infraestructura: si diseñamos para T=100,
    ¿cuál es el riesgo de que falle en N=50 años?
    
    Parámetros
    ----------
    T : float
        Período de retorno en años
    N : int o array
        Número de años
    
    Retorna
    -------
    float o array
        Riesgo de falla en N años
    
    Ejemplo
    -------
    >>> r = riesgo_falla(100, 50)
    >>> print(f"Riesgo en 50 años: {r*100:.1f}%")
    """
    R = 1 - (1 - 1 / T) ** np.asarray(N)
    return R


# ============================================================================
# 10. BOOTSTRAP PARAMÉTRICO PARA INTERVALO DE CONFIANZA
# ============================================================================

def bootstrap_cuantil(datos, nombre, T, B=500, semilla=42):
    """
    Calcula intervalo de confianza al 95% del cuantil x_T por bootstrap paramétrico.
    
    Procedimiento:
    1. Ajustar distribución a datos originales
    2. Generar B muestras simuladas de esa distribución
    3. Ajustar distribución a cada muestra simulada
    4. Calcular x_T para cada muestra
    5. Intervalo = percentiles 2.5% y 97.5%
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    nombre : str
        Nombre de la distribución
    T : float
        Período de retorno
    B : int
        Número de muestras bootstrap
    semilla : int
        Semilla para reproducibilidad
    
    Retorna
    -------
    dict con:
        'x_T': cuantil estimado
        'ic_lower': límite inferior del IC 95%
        'ic_upper': límite superior del IC 95%
    
    Ejemplo
    -------
    >>> boot = bootstrap_cuantil(datos, 'Gumbel', T=100, B=500)
    >>> print(f"x_100 = {boot['x_T']:.2f} [{boot['ic_lower']:.2f}, {boot['ic_upper']:.2f}]")
    """
    np.random.seed(semilla)
    datos = np.asarray(datos)
    n = len(datos)
    
    # Ajuste original
    params_orig, _ = ajustar(datos, nombre)
    x_T_orig = cuantil_retorno(nombre, params_orig, T)
    
    # Muestras bootstrap
    dist = DISTRIBUCIONES_CANDIDATAS[nombre]
    cuantiles_boot = []
    
    for _ in range(B):
        # Generar muestra simulada
        if nombre in ['Lognormal', 'Gamma', 'Weibull']:
            muestra_sim = dist.rvs(params_orig[0], loc=0, scale=params_orig[1], size=n)
        else:
            muestra_sim = dist.rvs(*params_orig, size=n)
        
        # Ajuste a muestra simulada
        try:
            params_sim, _ = ajustar(muestra_sim, nombre)
            x_T_sim = cuantil_retorno(nombre, params_sim, T)
            cuantiles_boot.append(x_T_sim)
        except:
            # En caso de convergencia fallida, usar el del original
            cuantiles_boot.append(x_T_orig)
    
    cuantiles_boot = np.array(cuantiles_boot)
    
    # Intervalo de confianza al 95%
    ic_lower = np.percentile(cuantiles_boot, 2.5)
    ic_upper = np.percentile(cuantiles_boot, 97.5)
    
    return {
        'x_T': x_T_orig,
        'ic_lower': ic_lower,
        'ic_upper': ic_upper,
        'muestras_bootstrap': cuantiles_boot
    }


# ============================================================================
# 11. MÉTODO DE MOMENTOS PARA GUMBEL
# ============================================================================

def gumbel_momentos(datos):
    """
    Calcula parámetros de Gumbel por método de momentos.
    
    Gumbel: E[X] = μ + γ·β, Var[X] = (π²/6)·β²
    donde γ ≈ 0.5772 es la constante de Euler-Mascheroni.
    
    Invirtiendo:
    β = s·√6/π       (donde s es la desv. estándar muestral)
    μ = x̄ - 0.5772·β  (donde x̄ es la media muestral)
    
    Este es el cálculo que el estudiante hace a mano para Gumbel.
    
    Parámetros
    ----------
    datos : array-like
        Datos observados
    
    Retorna
    -------
    dict con:
        'mu': parámetro de posición
        'beta': parámetro de escala
        'media_emp': media empírica
        'desv_emp': desviación estándar empírica
    
    Ejemplo
    -------
    >>> mom = gumbel_momentos(datos)
    >>> print(f"Gumbel: μ = {mom['mu']:.2f}, β = {mom['beta']:.2f}")
    """
    datos = np.asarray(datos)
    
    # Estadísticos muestrales
    media_emp = np.mean(datos)
    desv_emp = np.std(datos, ddof=1)  # ddof=1 para muestra
    
    # Constante de Euler-Mascheroni
    gamma_euler = 0.5772156649
    
    # Parámetro de escala β
    beta = desv_emp * np.sqrt(6) / np.pi
    
    # Parámetro de posición μ
    mu = media_emp - gamma_euler * beta
    
    return {
        'mu': mu,
        'beta': beta,
        'media_emp': media_emp,
        'desv_emp': desv_emp
    }


# ============================================================================
# BLOQUE PRINCIPAL PARA PRUEBA
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Cargar datos
    try:
        df_datos = pd.read_csv('datos/precip_max_anual.csv')
        datos = df_datos['pmax24h_mm'].dropna().values
        print(f"✓ Datos cargados: n = {len(datos)} observaciones")
        print(f"  Rango: [{datos.min():.2f}, {datos.max():.2f}] mm")
        print(f"  Media: {datos.mean():.2f} mm, Desv.Est.: {datos.std():.2f} mm")
        print()
    except FileNotFoundError:
        print("✗ Error: No se encontró 'datos/precip_max_anual.csv'")
        sys.exit(1)
    
    # Tabla comparativa
    print("=" * 150)
    print("TABLA COMPARATIVA DE DISTRIBUCIONES (ordenada por AIC)")
    print("=" * 150)
    
    tabla = tabla_comparativa(datos, n_mc=199)
    
    # Mostrar columnas principales de la tabla
    columnas_mostrar = [
        'Distribución', 'Parámetros', 'k', 'ℓ (log-vero)',
        'AIC', 'ΔAIC', 'Interpretación ΔAIC',
        'KS_stat', 'KS_pvalue_mc', 'AD_stat', 'AD_pvalue_mc',
        'Rechaza H₀ (KS 5%)', 'Rechaza H₀ (AD 5%)'
    ]
    
    # Crear tabla simplificada para impresión
    tabla_print = tabla[columnas_mostrar].copy()
    
    # Redondear números
    for col in ['AIC', 'ΔAIC', 'KS_stat', 'KS_pvalue_mc', 'AD_stat', 'AD_pvalue_mc']:
        tabla_print[col] = tabla_print[col].apply(lambda x: f"{x:.4f}")
    
    print(tabla_print.to_string(index=False))
    print()
    
    # Mejor distribución
    mejor_dist = tabla.iloc[0]['Distribución']
    mejor_aic = tabla.iloc[0]['AIC']
    print(f"✓ Mejor distribución por AIC: {mejor_dist} (AIC = {mejor_aic:.2f})")
    print()
    
    # Cuantiles de retorno para la mejor distribución
    print(f"Cuantiles de período de retorno para {mejor_dist}:")
    print("-" * 60)
    
    params_mejor = tabla.iloc[0]['params_tuple']
    periodos = [2, 5, 10, 25, 50, 100]
    
    for T in periodos:
        x_T = cuantil_retorno(mejor_dist, params_mejor, T)
        boot = bootstrap_cuantil(datos, mejor_dist, T, B=500)
        print(f"  T = {T:3d} años: x_T = {x_T:7.2f} mm "
              f"[IC95%: {boot['ic_lower']:7.2f}, {boot['ic_upper']:7.2f}]")
    
    print()
    
    # Riesgos de falla
    print("Riesgos de falla (%) para diferentes períodos de retorno:")
    print("-" * 60)
    anos = [5, 10, 25, 50, 100]
    for T in [10, 25, 50, 100]:
        riesgos = [riesgo_falla(T, N) * 100 for N in anos]
        print(f"  T = {T:3d} años: {', '.join([f'{r:5.1f}%' for r in riesgos])}")
    print()
    
    # Método de momentos para Gumbel
    print("Método de momentos para Gumbel (cálculo manual):")
    print("-" * 60)
    mom = gumbel_momentos(datos)
    print(f"  Media empírica: x̄ = {mom['media_emp']:.2f} mm")
    print(f"  Desv. estándar: s = {mom['desv_emp']:.2f} mm")
    print(f"  β = s·√6/π = {mom['desv_emp']:.2f} · {np.sqrt(6)/np.pi:.4f} = {mom['beta']:.2f} mm")
    print(f"  μ = x̄ - 0.5772·β = {mom['media_emp']:.2f} - 0.5772·{mom['beta']:.2f} = {mom['mu']:.2f} mm")
    print()
    
    print("=" * 150)
    print("✓ Prueba completada exitosamente")
