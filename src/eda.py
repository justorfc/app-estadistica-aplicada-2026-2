"""
src/eda.py - Funciones de Análisis Exploratorio de Datos (EDA)

Módulo con funciones documentadas para análisis univariado, bivariado
y detección de valores atípicos usando el método de Tukey.

Estudiante: Justo Fuentes (6820995)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


def resumen_numerico(serie: pd.Series) -> Dict[str, float]:
    """
    Calcula estadísticas descriptivas completas para una variable numérica.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de pandas con valores numéricos. Se ignoran NaN automáticamente.
    
    Retorna
    -------
    dict
        Diccionario con estadísticas: n, media, mediana, desv_est_muestral,
        varianza, coef_variacion_pct, minimo, q1, q3, maximo, rango_intercuartil,
        asimetria.
    
    Notas
    -----
    - Desviación estándar: ddof=1 (estimador insesgado para muestras)
    - Cuartiles: tipo 7 (por defecto en pandas y R)
    - Coeficiente de variación: (std / media) * 100
    - Asimetría: medida de simetría de la distribución
    
    Ejemplo
    -------
    >>> serie = pd.Series([1, 2, 3, 4, 5])
    >>> resumen = resumen_numerico(serie)
    >>> print(f"Media: {resumen['media']:.2f}")
    Media: 3.00
    """
    # Eliminar valores faltantes
    datos = serie.dropna()
    n = len(datos)
    
    if n == 0:
        return {}
    
    # Calcular estadísticas básicas
    media = datos.mean()
    mediana = datos.median()
    desv_est_muestral = datos.std(ddof=1)  # Estimador insesgado
    varianza = datos.var(ddof=1)  # Varianza muestral
    
    # Coeficiente de variación (CV %)
    if media != 0:
        coef_variacion_pct = (desv_est_muestral / abs(media)) * 100
    else:
        coef_variacion_pct = 0
    
    # Mínimo y máximo
    minimo = datos.min()
    maximo = datos.max()
    
    # Cuartiles: tipo 7 (default en pandas y R)
    q1 = datos.quantile(0.25, interpolation='linear')
    q3 = datos.quantile(0.75, interpolation='linear')
    
    # Rango intercuartil (RIC)
    rango_intercuartil = q3 - q1
    
    # Asimetría (skewness)
    asimetria = datos.skew()
    
    return {
        'n': n,
        'media': media,
        'mediana': mediana,
        'desv_est_muestral': desv_est_muestral,
        'varianza': varianza,
        'coef_variacion_pct': coef_variacion_pct,
        'minimo': minimo,
        'q1': q1,
        'q3': q3,
        'maximo': maximo,
        'rango_intercuartil': rango_intercuartil,
        'asimetria': asimetria
    }


def vallas_tukey(serie: pd.Series) -> Tuple[float, float, List[Tuple]]:
    """
    Calcula los límites de vallas de Tukey y detecta valores atípicos.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de pandas con valores numéricos. Se ignoran NaN automáticamente.
    
    Retorna
    -------
    tuple
        (limite_inferior, limite_superior, lista_atipicos)
        
        - limite_inferior: L_inf = Q1 - 1.5 * RIC
        - limite_superior: L_sup = Q3 + 1.5 * RIC
        - lista_atipicos: lista de tuplas (índice, valor) para valores fuera de vallas
    
    Notas
    -----
    - Atípico: valor < L_inf o valor > L_sup
    - Método de Tukey es robusto a la distribución
    - Se usa 1.5 * RIC como criterio estándar
    
    Ejemplo
    -------
    >>> serie = pd.Series([1, 2, 3, 4, 5, 100])
    >>> l_inf, l_sup, atipicos = vallas_tukey(serie)
    >>> print(f"Límites: [{l_inf:.2f}, {l_sup:.2f}]")
    Límites: [-1.50, 9.50]
    >>> print(f"Atípicos: {len(atipicos)}")
    Atípicos: 1
    """
    # Eliminar valores faltantes
    datos = serie.dropna()
    
    # Calcular cuartiles
    q1 = datos.quantile(0.25, interpolation='linear')
    q3 = datos.quantile(0.75, interpolation='linear')
    ric = q3 - q1
    
    # Calcular vallas
    limite_inferior = q1 - 1.5 * ric
    limite_superior = q3 + 1.5 * ric
    
    # Detectar atípicos
    atipicos = []
    for idx, val in datos.items():
        if val < limite_inferior or val > limite_superior:
            atipicos.append((idx, val))
    
    return limite_inferior, limite_superior, atipicos


def tabla_frecuencias(serie: pd.Series) -> pd.DataFrame:
    """
    Calcula tabla de frecuencias absolutas y relativas para variable cualitativa.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie de pandas con valores categóricos (texto).
    
    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas: Categoría, Frecuencia Absoluta, Frecuencia Relativa
    
    Notas
    -----
    - Frecuencia Absoluta: conteo de casos por categoría
    - Frecuencia Relativa: proporción (0-1), expresada como porcentaje
    - Se ordena por frecuencia descendente
    - Los NaN se ignoran automáticamente
    
    Ejemplo
    -------
    >>> serie = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'])
    >>> tabla = tabla_frecuencias(serie)
    >>> print(tabla)
      Categoría  Frecuencia Absoluta  Frecuencia Relativa (%)
    0         A                    3                    50.0
    1         B                    2                    33.3
    2         C                    1                    16.7
    """
    # Contar frecuencias
    frecuencias_abs = serie.value_counts().sort_values(ascending=False)
    
    # Calcular frecuencias relativas (en porcentaje)
    n_total = len(serie.dropna())
    frecuencias_rel = (frecuencias_abs / n_total) * 100
    
    # Crear tabla
    tabla = pd.DataFrame({
        'Categoría': frecuencias_abs.index,
        'Frecuencia Absoluta': frecuencias_abs.values,
        'Frecuencia Relativa (%)': frecuencias_rel.values
    }).reset_index(drop=True)
    
    return tabla
