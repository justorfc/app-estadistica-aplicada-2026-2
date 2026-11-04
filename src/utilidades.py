"""
Módulo utilidades: Funciones auxiliares compartidas para toda la app.

Contiene:
- Carga y validación de datos
- Formateo de números y tablas
- Caché de datos
- Funciones de configuración
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import streamlit as st


def obtener_ruta_datos(archivo: str) -> Path:
    """
    Obtiene la ruta completa a un archivo en la carpeta datos/.
    
    Args:
        archivo (str): Nombre del archivo (ej: 'parcelas.csv')
    
    Returns:
        Path: Ruta absoluta al archivo
    """
    raiz = Path(__file__).parent.parent
    return raiz / 'datos' / archivo


@st.cache_data
def cargar_datos(archivo: str) -> pd.DataFrame:
    """
    Carga un archivo CSV de la carpeta datos/ con caché de Streamlit.
    
    Args:
        archivo (str): Nombre del archivo CSV (ej: 'parcelas.csv')
    
    Returns:
        pd.DataFrame: Datos cargados
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        pd.errors.ParserError: Si el CSV está corrupto
    """
    ruta = obtener_ruta_datos(archivo)
    
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    
    return pd.read_csv(ruta)


@st.cache_data
def cargar_metadatos() -> dict:
    """
    Carga los metadatos del estudiante desde metadatos.json.
    
    Returns:
        dict: Diccionario con código, nombre, cultivo, municipio, etc.
    
    Raises:
        FileNotFoundError: Si metadatos.json no existe
        json.JSONDecodeError: Si JSON está corrupto
    """
    ruta = obtener_ruta_datos('metadatos.json')
    
    if not ruta.exists():
        raise FileNotFoundError(f"Metadatos no encontrados: {ruta}")
    
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def formatear_numero(valor: float, decimales: int = 2, notacion: str = 'f') -> str:
    """
    Formatea un número con separador de miles y decimales.
    
    Args:
        valor (float): Número a formatear
        decimales (int): Número de decimales (por defecto 2)
        notacion (str): 'f' (fijo), 'e' (científica)
    
    Returns:
        str: Número formateado
    
    Ejemplo:
        >>> formatear_numero(1234.5678, decimales=2)
        '1.234,57'
    """
    if pd.isna(valor):
        return "N/D"
    
    formato = f"{{:,.{decimales}{notacion}}}"
    # Formatear según notación
    resultado = formato.format(valor)
    
    # Reemplazar separadores para formato español
    if notacion == 'f':
        resultado = resultado.replace(',', '[TEMP]').replace('.', ',').replace('[TEMP]', '.')
    
    return resultado


def crear_tabla_resumen(df: pd.DataFrame, columnas_numericas: list = None) -> pd.DataFrame:
    """
    Crea una tabla de resumen estadístico de un DataFrame.
    
    Args:
        df (pd.DataFrame): Datos a resumir
        columnas_numericas (list): Columnas a incluir (si None, detectar automático)
    
    Returns:
        pd.DataFrame: Tabla con count, mean, std, min, 25%, 50%, 75%, max
    
    Nota:
        Usa formato español: comas para decimales, puntos para miles
    """
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    resumen = df[columnas_numericas].describe().T
    
    # Renombrar índices en español
    resumen.index.name = 'Variable'
    resumen.columns = ['Contar', 'Media', 'Desv. Est.', 'Mín', '25%', 'Mediana', '75%', 'Máx']
    
    # Formatear números
    for col in resumen.columns:
        resumen[col] = resumen[col].apply(lambda x: formatear_numero(x, decimales=2))
    
    return resumen


def detectar_outliers_iqr(df: pd.DataFrame, columna: str, multiplicador: float = 1.5) -> pd.DataFrame:
    """
    Detecta outliers usando el método del rango intercuartílico (IQR).
    
    Args:
        df (pd.DataFrame): Datos
        columna (str): Columna donde detectar outliers
        multiplicador (float): Multiplicador de IQR (1.5 por defecto)
    
    Returns:
        pd.DataFrame: Subset con filas que contienen outliers
    
    Fórmula:
        - Q1 = percentil 25%
        - Q3 = percentil 75%
        - IQR = Q3 - Q1
        - Límite inferior = Q1 - multiplicador * IQR
        - Límite superior = Q3 + multiplicador * IQR
        - Outliers: valores fuera de [inferior, superior]
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inf = Q1 - multiplicador * IQR
    limite_sup = Q3 + multiplicador * IQR
    
    outliers = df[(df[columna] < limite_inf) | (df[columna] > limite_sup)]
    
    return outliers


def validar_datos(df: pd.DataFrame, nombre_archivo: str = "") -> dict:
    """
    Realiza validaciones básicas de integridad de datos.
    
    Args:
        df (pd.DataFrame): Datos a validar
        nombre_archivo (str): Nombre del archivo (opcional, para reportes)
    
    Returns:
        dict: Reporte de validación con claves:
            - filas: número de filas
            - columnas: número de columnas
            - faltantes: dict {columna: número de NaN}
            - duplicados: número de filas duplicadas
            - tipos: dict {columna: tipo}
            - valido: bool (True si no hay problemas críticos)
    """
    reporte = {
        'archivo': nombre_archivo,
        'filas': len(df),
        'columnas': len(df.columns),
        'faltantes': df.isnull().sum().to_dict(),
        'duplicados': df.duplicated().sum(),
        'tipos': df.dtypes.to_dict(),
        'valido': True
    }
    
    # Validaciones
    if reporte['duplicados'] > 0:
        reporte['advertencia_duplicados'] = f"{reporte['duplicados']} filas duplicadas detectadas"
    
    faltantes_total = df.isnull().sum().sum()
    if faltantes_total > 0:
        reporte['advertencia_faltantes'] = f"{faltantes_total} valores faltantes (N/D) detectados"
    
    return reporte


def agrupar_y_contar(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """
    Agrupa por una columna categórica y cuenta frecuencias.
    
    Args:
        df (pd.DataFrame): Datos
        columna (str): Columna categórica
    
    Returns:
        pd.DataFrame: Tabla con 'Categoría', 'Contar', 'Porcentaje (%)'
    """
    conteos = df[columna].value_counts()
    tabla = pd.DataFrame({
        'Categoría': conteos.index,
        'Contar': conteos.values,
        'Porcentaje (%)': (conteos.values / len(df) * 100).round(1)
    })
    
    return tabla.reset_index(drop=True)
