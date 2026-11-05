"""
Módulo: Análisis de Regresión Lineal
====================================

Regresión lineal simple y múltiple con cálculos manuales y statsmodels.
Incluye correlación, ajuste de modelos, predicción e intervalos de confianza.

Datos utilizados:
- datos/parcelas.csv: 100 parcelas con variables agrícolas
- datos/muestra_reg8.csv: 8 parcelas para verificación manual

Fórmulas base (regresión lineal simple):
  y = b0 + b1·x + ε
  b1 = Sxy / Sxx
  b0 = ȳ - b1·x̄
  R² = 1 - SCE / SCT
  t = b1 / SE(b1)

Referencia: Kutner, Nachtsheim, Neter (2004), Applied Linear Regression Models.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import t as t_dist, shapiro, f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# 1. MATRIZ DE CORRELACIÓN
# ============================================================================

def matriz_correlacion(df, metodo='pearson'):
    """
    Calcula matriz de correlación de variables numéricas.
    
    Parámetros
    ----------
    df : DataFrame
        Base de datos con variables numéricas
    metodo : str
        'pearson' (por defecto) o 'spearman'
    
    Retorna
    -------
    DataFrame
        Matriz de correlación (simétricas, diagonal = 1)
    
    Ejemplo
    -------
    >>> df = pd.read_csv('datos/parcelas.csv')
    >>> corr = matriz_correlacion(df, metodo='pearson')
    >>> print(corr.loc['lamina_riego', 'rendimiento'])  # r ≈ 0.15
    """
    # Seleccionar solo variables numéricas
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Calcular correlación
    if metodo == 'pearson':
        return df_numeric.corr(method='pearson')
    elif metodo == 'spearman':
        return df_numeric.corr(method='spearman')
    else:
        raise ValueError(f"Método '{metodo}' no reconocido. Use 'pearson' o 'spearman'.")


# ============================================================================
# 2. CÁLCULO MANUAL DE REGRESIÓN LINEAL SIMPLE
# ============================================================================

def calculo_manual(x, y):
    """
    Realiza regresión lineal simple con cálculos manuales.
    
    Ecuación:
      y_i = b0 + b1·x_i + e_i
    
    Parámetros
    ----------
    x : array
        Variable independiente
    y : array
        Variable dependiente
    
    Retorna
    -------
    dict
        Diccionario con:
        - 'n': tamaño de muestra
        - 'media_x', 'media_y': medias
        - 'Sxx', 'Syy', 'Sxy': sumas de cuadrados y productos
        - 'r_pearson': coeficiente de correlación de Pearson
        - 'rho_spearman': coeficiente de Spearman
        - 'b1': pendiente
        - 'b0': intercepto
        - 'y_ajustado': valores predichos
        - 'residuos': e_i = y_i - ŷ_i
        - 'SCE': suma de cuadrados de error
        - 'SCR': suma de cuadrados de regresión
        - 'SCT': suma de cuadrados total
        - 'R2': coeficiente de determinación
        - 'RSE': error estándar residual
        - 'SE_b1': error estándar de b1
        - 't_b1': estadístico t para b1
        - 't_critico': valor crítico bilateral (α=0.05)
        - 'p_valor': p-valor bilateral
        - 'IC_b1_lower', 'IC_b1_upper': intervalo de confianza 95% de b1
    
    Fórmulas
    --------
    Medias:
      x̄ = Σx_i / n
      ȳ = Σy_i / n
    
    Sumas de cuadrados:
      Sxx = Σ(x_i - x̄)² = Σx_i² - (Σx_i)²/n
      Syy = Σ(y_i - ȳ)² = Σy_i² - (Σy_i)²/n
      Sxy = Σ(x_i - x̄)(y_i - ȳ) = Σx_i·y_i - (Σx_i)(Σy_i)/n
    
    Correlación de Pearson:
      r = Sxy / √(Sxx·Syy)
    
    Parámetros:
      b1 = Sxy / Sxx
      b0 = ȳ - b1·x̄
    
    Predicciones y residuos:
      ŷ_i = b0 + b1·x_i
      e_i = y_i - ŷ_i
    
    Sumas de cuadrados:
      SCE = Σe_i² = Σ(y_i - ŷ_i)²     (error)
      SCR = Σ(ŷ_i - ȳ)² = b1²·Sxx     (regresión)
      SCT = Syy = SCE + SCR            (total)
    
    R² = 1 - SCE/SCT = SCR/SCT
    
    Error estándar residual:
      RSE = √(SCE / (n-2))  donde n-2 = grados de libertad
    
    Error estándar de b1:
      SE(b1) = RSE / √Sxx
    
    Estadístico t:
      t = b1 / SE(b1)
    
    Intervalo de confianza 95% de b1:
      IC = b1 ± t_crítico(α/2, n-2) · SE(b1)
    
    Ejemplo
    -------
    >>> x = np.array([1, 2, 3, 4, 5])
    >>> y = np.array([2, 4, 5, 4, 5])
    >>> resultado = calculo_manual(x, y)
    >>> print(f"b0={resultado['b0']:.4f}, b1={resultado['b1']:.4f}")
    >>> print(f"R²={resultado['R2']:.4f}, p-valor={resultado['p_valor']:.4f}")
    """
    # Convertir a arrays
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    
    # Medias
    media_x = np.mean(x)
    media_y = np.mean(y)
    
    # Sumas de cuadrados y productos
    # Sxx = Σ(x_i - x̄)²
    Sxx = np.sum((x - media_x)**2)
    
    # Syy = Σ(y_i - ȳ)²
    Syy = np.sum((y - media_y)**2)
    
    # Sxy = Σ(x_i - x̄)(y_i - ȳ)
    Sxy = np.sum((x - media_x) * (y - media_y))
    
    # Correlación de Pearson
    r_pearson = Sxy / np.sqrt(Sxx * Syy) if (Sxx * Syy) > 0 else 0
    
    # Correlación de Spearman (con scipy)
    if n >= 3:
        rho_spearman, _ = stats.spearmanr(x, y)
    else:
        rho_spearman = np.nan
    
    # Parámetros de regresión
    # b1 = Sxy / Sxx
    b1 = Sxy / Sxx if Sxx != 0 else 0
    
    # b0 = ȳ - b1·x̄
    b0 = media_y - b1 * media_x
    
    # Predicciones
    y_ajustado = b0 + b1 * x
    
    # Residuos
    residuos = y - y_ajustado
    
    # Sumas de cuadrados
    # SCE = Σ(y_i - ŷ_i)²
    SCE = np.sum(residuos**2)
    
    # SCR = Σ(ŷ_i - ȳ)² = b1² · Sxx
    SCR = b1**2 * Sxx
    
    # SCT = Syy
    SCT = Syy
    
    # R²
    R2 = 1 - (SCE / SCT) if SCT != 0 else 0
    
    # Error estándar residual
    # RSE = √(SCE / (n-2))
    RSE = np.sqrt(SCE / (n - 2)) if n > 2 else np.nan
    
    # Error estándar de b1
    # SE(b1) = RSE / √Sxx
    SE_b1 = RSE / np.sqrt(Sxx) if Sxx > 0 else np.nan
    
    # Estadístico t
    # t = b1 / SE(b1)
    t_b1 = b1 / SE_b1 if SE_b1 > 0 else np.nan
    
    # Valor crítico bilateral (α = 0.05, gl = n-2)
    alpha = 0.05
    gl = n - 2
    t_critico = t_dist.ppf(1 - alpha/2, gl)
    
    # P-valor bilateral
    # P = 2 · P(T > |t|) donde T ~ t(n-2)
    p_valor = 2 * (1 - t_dist.cdf(np.abs(t_b1), gl)) if not np.isnan(t_b1) else np.nan
    
    # Intervalo de confianza 95% de b1
    margen_error = t_critico * SE_b1
    IC_b1_lower = b1 - margen_error
    IC_b1_upper = b1 + margen_error
    
    return {
        'n': n,
        'media_x': media_x,
        'media_y': media_y,
        'Sxx': Sxx,
        'Syy': Syy,
        'Sxy': Sxy,
        'r_pearson': r_pearson,
        'rho_spearman': rho_spearman,
        'b1': b1,
        'b0': b0,
        'y_ajustado': y_ajustado,
        'residuos': residuos,
        'SCE': SCE,
        'SCR': SCR,
        'SCT': SCT,
        'R2': R2,
        'RSE': RSE,
        'SE_b1': SE_b1,
        't_b1': t_b1,
        't_critico': t_critico,
        'p_valor': p_valor,
        'IC_b1_lower': IC_b1_lower,
        'IC_b1_upper': IC_b1_upper
    }


# ============================================================================
# 3. AJUSTE CON STATSMODELS (OLS)
# ============================================================================

def ajustar_rls(df, x, y):
    """
    Ajusta regresión lineal simple usando statsmodels.
    
    Parámetros
    ----------
    df : DataFrame
        Base de datos
    x : str
        Nombre de variable independiente
    y : str
        Nombre de variable dependiente
    
    Retorna
    -------
    RegressionResults
        Objeto con todos los parámetros y estadísticos
    
    Ejemplo
    -------
    >>> df = pd.read_csv('datos/muestra_reg8.csv')
    >>> modelo = ajustar_rls(df, 'lamina_riego', 'rendimiento')
    >>> print(modelo.summary())
    """
    # Fórmula de statsmodels
    formula = f"{y} ~ {x}"
    
    # Ajustar OLS
    modelo = ols(formula, data=df).fit()
    
    return modelo


# ============================================================================
# 4. PREDICCIÓN CON INTERVALO DE CONFIANZA E INTERVALO DE PREDICCIÓN
# ============================================================================

def predecir(modelo, x0, nivel=0.95):
    """
    Realiza predicción con intervalos de confianza y predicción.
    
    Parámetros
    ----------
    modelo : RegressionResults
        Modelo ajustado (de ajustar_rls)
    x0 : float o array
        Valor(es) de x para los que predecir
    nivel : float
        Nivel de confianza (por defecto 0.95)
    
    Retorna
    -------
    dict
        - 'y_pred': predicción puntual
        - 'IC_lower', 'IC_upper': intervalo de confianza 95% (para E[Y|X])
        - 'IP_lower', 'IP_upper': intervalo de predicción 95% (para Y individual)
    
    Fórmulas
    --------
    Predicción: ŷ = b0 + b1·x0
    
    Error estándar de predicción del valor medio:
      SE(ŷ) = RSE · √(1/n + (x0 - x̄)²/Sxx)
    
    Intervalo de confianza (para E[Y|X]):
      IC: ŷ ± t_crítico · SE(ŷ)
    
    Error estándar de predicción individual:
      SE(ŷ_indiv) = RSE · √(1 + 1/n + (x0 - x̄)²/Sxx)
    
    Intervalo de predicción (para Y individual):
      IP: ŷ ± t_crítico · SE(ŷ_indiv)
    
    Ejemplo
    -------
    >>> modelo = ajustar_rls(df, 'x', 'y')
    >>> pred = predecir(modelo, x0=100)
    >>> print(f"y_pred = {pred['y_pred']:.2f}")
    >>> print(f"IC95%: [{pred['IC_lower']:.2f}, {pred['IC_upper']:.2f}]")
    """
    # Si x0 es escalar, convertir a array
    x0 = np.atleast_1d(x0)
    
    # Usar predicción de statsmodels
    # summary_table devuelve tabla con IC e IP
    pred_df = pd.DataFrame({'Intercept': 1, modelo.model.exog_names[1]: x0})
    
    pred_result = modelo.get_prediction(pred_df)
    pred_summary = pred_result.summary_frame(alpha=1-nivel)
    
    resultados = []
    for i, val_x in enumerate(x0):
        resultado = {
            'x': val_x,
            'y_pred': pred_summary['mean'].iloc[i],
            'IC_lower': pred_summary['mean_ci_lower'].iloc[i],
            'IC_upper': pred_summary['mean_ci_upper'].iloc[i],
            'IP_lower': pred_summary['obs_ci_lower'].iloc[i],
            'IP_upper': pred_summary['obs_ci_upper'].iloc[i]
        }
        resultados.append(resultado)
    
    if len(resultados) == 1:
        return resultados[0]
    else:
        return resultados


# ============================================================================
# 5. DIAGNÓSTICO DE RESIDUOS
# ============================================================================

def diagnostico_residuos(modelo):
    """
    Realiza diagnóstico de residuos del modelo.
    
    Parámetros
    ----------
    modelo : RegressionResults
        Modelo ajustado (de ajustar_rls)
    
    Retorna
    -------
    dict
        - 'residuos': vector de residuos
        - 'ajustados': valores predichos
        - 'shapiro_stat', 'shapiro_pvalue': test de normalidad
        - 'breusch_pagan_stat', 'breusch_pagan_pvalue': test de heterocedasticidad
    
    Tests
    -----
    Shapiro-Wilk (normalidad):
      H0: Residuos distribuidos normalmente
      H1: Residuos NO distribuyen normalmente
      Si p-valor > 0.05: No rechazar H0 (residuos normales)
    
    Breusch-Pagan (homocedasticidad):
      H0: Varianza constante (homocedasticidad)
      H1: Varianza NO constante (heterocedasticidad)
      Si p-valor > 0.05: No rechazar H0 (varianza constante)
    
    Ejemplo
    -------
    >>> modelo = ajustar_rls(df, 'x', 'y')
    >>> diag = diagnostico_residuos(modelo)
    >>> print(f"Normalidad (p-valor): {diag['shapiro_pvalue']:.4f}")
    """
    residuos = modelo.resid
    ajustados = modelo.fittedvalues
    
    # Shapiro-Wilk (normalidad)
    shapiro_stat, shapiro_pvalue = shapiro(residuos)
    
    # Breusch-Pagan (heterocedasticidad)
    from statsmodels.stats.diagnostic import het_breuschpagan
    bp_stat, bp_pvalue, _, _ = het_breuschpagan(residuos, modelo.model.exog)
    
    return {
        'residuos': residuos,
        'ajustados': ajustados,
        'shapiro_stat': shapiro_stat,
        'shapiro_pvalue': shapiro_pvalue,
        'breusch_pagan_stat': bp_stat,
        'breusch_pagan_pvalue': bp_pvalue
    }


# ============================================================================
# 6. REGRESIÓN LINEAL MÚLTIPLE
# ============================================================================

def ajustar_multiple(df, y, lista_x):
    """
    Ajusta regresión lineal múltiple.
    
    Parámetros
    ----------
    df : DataFrame
        Base de datos
    y : str
        Nombre de variable dependiente
    lista_x : list of str
        Lista de nombres de variables independientes
    
    Retorna
    -------
    RegressionResults
        Modelo ajustado
    
    Nota
    ----
    Elimina automáticamente filas con NaN en las variables utilizadas.
    
    Ejemplo
    -------
    >>> modelo = ajustar_multiple(df, 'rendimiento', ['lamina_riego', 'dosis_N'])
    >>> print(modelo.summary())
    """
    # Seleccionar columnas
    cols = [y] + lista_x
    df_limpio = df[cols].dropna()
    
    # Fórmula
    formula = f"{y} ~ {' + '.join(lista_x)}"
    
    # Ajustar
    modelo = ols(formula, data=df_limpio).fit()
    
    return modelo


# ============================================================================
# PRUEBA DEL MÓDULO
# ============================================================================

if __name__ == "__main__":
    import pandas as pd
    
    print("="*80)
    print("PRUEBA DEL MÓDULO: REGRESIÓN LINEAL")
    print("="*80)
    
    # Cargar datos
    df_muestra = pd.read_csv('datos/muestra_reg8.csv')
    
    print("\nDatos de prueba (8 parcelas):")
    print(df_muestra)
    
    print("\n" + "="*80)
    print("COMPARACIÓN: CÁLCULO MANUAL vs STATSMODELS")
    print("="*80)
    
    x_data = df_muestra['lamina_riego'].values
    y_data = df_muestra['rendimiento'].values
    
    # Cálculo manual
    print("\n1. CÁLCULO MANUAL:")
    resultado_manual = calculo_manual(x_data, y_data)
    
    print(f"  n = {resultado_manual['n']}")
    print(f"  x̄ = {resultado_manual['media_x']:.4f}")
    print(f"  ȳ = {resultado_manual['media_y']:.4f}")
    print(f"  Sxx = {resultado_manual['Sxx']:.4f}")
    print(f"  Sxy = {resultado_manual['Sxy']:.4f}")
    print(f"  b1 = {resultado_manual['b1']:.6f}")
    print(f"  b0 = {resultado_manual['b0']:.6f}")
    print(f"  R² = {resultado_manual['R2']:.6f}")
    print(f"  RSE = {resultado_manual['RSE']:.6f}")
    print(f"  SE(b1) = {resultado_manual['SE_b1']:.6f}")
    print(f"  t = {resultado_manual['t_b1']:.6f}")
    print(f"  p-valor = {resultado_manual['p_valor']:.6f}")
    print(f"  IC95% b1: [{resultado_manual['IC_b1_lower']:.6f}, {resultado_manual['IC_b1_upper']:.6f}]")
    
    # Ajuste con statsmodels
    print("\n2. AJUSTE CON STATSMODELS:")
    modelo_sm = ajustar_rls(df_muestra, 'lamina_riego', 'rendimiento')
    
    print(f"  b1 = {modelo_sm.params['lamina_riego']:.6f}")
    print(f"  b0 = {modelo_sm.params['Intercept']:.6f}")
    print(f"  R² = {modelo_sm.rsquared:.6f}")
    print(f"  RSE = {np.sqrt(modelo_sm.mse_resid):.6f}")
    print(f"  SE(b1) = {modelo_sm.bse['lamina_riego']:.6f}")
    print(f"  t = {modelo_sm.tvalues['lamina_riego']:.6f}")
    print(f"  p-valor = {modelo_sm.pvalues['lamina_riego']:.6f}")
    
    # Intervalo de confianza
    conf_int = modelo_sm.conf_int(alpha=0.05)
    print(f"  IC95% b1: [{conf_int.loc['lamina_riego', 0]:.6f}, {conf_int.loc['lamina_riego', 1]:.6f}]")
    
    # Comparación
    print("\n" + "="*80)
    print("VERIFICACIÓN DE COINCIDENCIA:")
    print("="*80)
    
    tol = 1e-5
    
    def verificar(nombre, manual, statsmodels, tolerancia=tol):
        diff = abs(manual - statsmodels)
        match = "✓" if diff < tolerancia else "❌"
        print(f"  {match} {nombre:20s}: manual={manual:.6f}, sm={statsmodels:.6f}, diff={diff:.2e}")
    
    verificar("b0", resultado_manual['b0'], modelo_sm.params['Intercept'])
    verificar("b1", resultado_manual['b1'], modelo_sm.params['lamina_riego'])
    verificar("R²", resultado_manual['R2'], modelo_sm.rsquared)
    verificar("RSE", resultado_manual['RSE'], np.sqrt(modelo_sm.mse_resid))
    verificar("t", resultado_manual['t_b1'], modelo_sm.tvalues['lamina_riego'])
    verificar("p-valor", resultado_manual['p_valor'], modelo_sm.pvalues['lamina_riego'])
    
    print("\n" + "="*80)
    print("✓ Prueba completada exitosamente")
    print("="*80)
