"""
Módulo src/datos.py: Funciones centrales para carga de datos y UI.

Contiene:
- cargar_csv(): Carga archivos CSV con parseado automático de fechas
- cargar_metadatos(): Carga metadatos del estudiante
- tarjeta_estudiante(): Widget para barra lateral con datos del estudiante
"""

import pandas as pd
import json
import streamlit as st
from pathlib import Path


def obtener_ruta_datos(archivo: str) -> Path:
    """
    Obtiene la ruta absoluta a un archivo en la carpeta datos/.
    
    Args:
        archivo (str): Nombre del archivo CSV o JSON
    
    Returns:
        Path: Ruta absoluta al archivo
    
    Ejemplo:
        >>> obtener_ruta_datos('parcelas.csv')
        PosixPath('/workspaces/app-estadistica-aplicada-2026-2/datos/parcelas.csv')
    """
    raiz = Path(__file__).parent.parent  # Sube desde src/ a raíz
    return raiz / 'datos' / archivo


@st.cache_data
def cargar_csv(nombre: str) -> pd.DataFrame:
    """
    Carga un archivo CSV de la carpeta datos/ con caché de Streamlit.
    
    Características:
    - Usa @st.cache_data para optimizar (carga solo una vez por sesión)
    - Detecta columnas de fecha automáticamente:
      * Nombres que contienen 'fecha', 'date', 'time', 'anio', 'año'
      * Las parsea como datetime64 para análisis temporal
    - Maneja errores de archivo no encontrado
    
    Args:
        nombre (str): Nombre del archivo CSV (ej: 'parcelas.csv')
    
    Returns:
        pd.DataFrame: Datos cargados con tipos apropiados
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        pd.errors.ParserError: Si el CSV está corrupto
    
    Ejemplo:
        >>> df = cargar_csv('parcelas.csv')
        >>> df.shape
        (116, 8)
        >>> df.dtypes
        parcela             object
        suelo              object
        riego              object
        dosis_N           float64
        lamina_riego      float64
        materia_organica  float64
        ph                float64
        rendimiento       float64
    
    Nota:
        Si existen columnas 'fecha', 'fecha_inicio', 'date', se convierten a datetime.
    """
    ruta = obtener_ruta_datos(nombre)
    
    if not ruta.exists():
        raise FileNotFoundError(f"❌ Archivo no encontrado: {ruta}")
    
    # Leer CSV
    df = pd.read_csv(ruta)
    
    # Detectar y parsear columnas de fecha
    columnas_fecha = [col for col in df.columns 
                     if any(x in col.lower() for x in ['fecha', 'date', 'time', 'anio', 'año'])]
    
    for col in columnas_fecha:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except Exception:
            pass  # Si falla, dejar como está
    
    return df


@st.cache_data
def cargar_metadatos() -> dict:
    """
    Carga los metadatos personalizados del estudiante.
    
    Contiene:
    - código: Código estudiantil
    - nombre: Nombres y apellidos completos
    - cultivo: Cultivo elegido (Maíz, Arroz, Yuca, Ñame, etc.)
    - municipio: Municipio de la Sucre (Sincelejo, Corozal, etc.)
    - n_parcelas: Número de parcelas en el dataset
    - huella: Hash MD5 truncado (primeros 8 caracteres en mayúscula)
    
    Returns:
        dict: Diccionario con claves {'código', 'nombre', 'cultivo', 'municipio', 'n_parcelas', 'huella'}
    
    Raises:
        FileNotFoundError: Si metadatos.json no existe
        json.JSONDecodeError: Si JSON está corrupto
    
    Ejemplo:
        >>> metadatos = cargar_metadatos()
        >>> metadatos['nombre']
        'Justo Fuentes'
        >>> metadatos['cultivo']
        'Ñame'
    """
    ruta = obtener_ruta_datos('metadatos.json')
    
    if not ruta.exists():
        raise FileNotFoundError(f"❌ Metadatos no encontrados: {ruta}")
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            metadatos = json.load(f)
        return metadatos
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON corrupto en metadatos.json: {e}")


def tarjeta_estudiante(ubicacion: str = 'sidebar') -> None:
    """
    Muestra una tarjeta visual con los datos del estudiante.
    
    Ubicaciones:
    - 'sidebar': Barra lateral (recomendado, aparece en todas las páginas)
    - 'main': Área principal de la app
    - 'expander': Dentro de un st.expander
    
    Contenido mostrado:
    - Nombre del estudiante (principal)
    - Código estudiantil
    - Cultivo elegido (con emoji 🌾)
    - Municipio (Sucre)
    - Huella única (primeros 8 caracteres del MD5)
    - Número de parcelas
    
    Args:
        ubicacion (str): Dónde mostrar la tarjeta ('sidebar', 'main', 'expander')
    
    Returns:
        None (escribe directamente en Streamlit)
    
    Nota:
        Usa @st.cache_data de cargar_metadatos() para no recargar múltiples veces.
    
    Ejemplo:
        >>> with st.sidebar:
        ...     tarjeta_estudiante()
    """
    try:
        metadatos = cargar_metadatos()
    except Exception as e:
        st.error(f"❌ Error al cargar metadatos: {e}")
        return
    
    # Seleccionar contenedor
    if ubicacion == 'sidebar':
        contenedor = st.sidebar
    elif ubicacion == 'expander':
        contenedor = st.expander("👤 Datos del Estudiante")
    else:
        contenedor = st
    
    # Renderizar tarjeta
    with contenedor:
        st.markdown("### 👤 Estudiante")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{metadatos['nombre']}**")
            st.caption(f"Código: {metadatos['codigo']}")
        with col2:
            st.markdown(f"🌾")
        
        st.divider()
        
        # Datos en dos columnas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Cultivo", metadatos['cultivo'])
        with col2:
            st.metric("Municipio", metadatos['municipio'])
        
        # Información adicional
        st.markdown(f"""
        **Parcelas:** {metadatos['n_parcelas']}  
        **Huella:** `{metadatos['huella']}`
        """)


def formatear_numero(valor, decimales: int = 2) -> str:
    """
    Formatea un número con separadores españoles (1.234,57).
    
    Args:
        valor: Número a formatear (int, float, np.float64, etc.)
        decimales: Número de decimales (por defecto 2)
    
    Returns:
        str: Número formateado en estilo español
    
    Ejemplo:
        >>> formatear_numero(1234.5678, decimales=2)
        '1.234,57'
        >>> formatear_numero(3.14159, decimales=1)
        '3,1'
    """
    if pd.isna(valor):
        return "N/D"
    
    # Formatear con separadores de miles
    formateado = f"{valor:,.{decimales}f}"
    
    # Reemplazar separadores: 1,234.57 → 1.234,57
    formateado = formateado.replace(',', '[TEMP]')  # Guardar miles
    formateado = formateado.replace('.', ',')       # . → ,
    formateado = formateado.replace('[TEMP]', '.')  # miles de vuelta
    
    return formateado


def resumen_estadistico(df: pd.DataFrame, columnas_numericas: list = None) -> pd.DataFrame:
    """
    Crea una tabla de resumen estadístico en formato español.
    
    Estadísticas calculadas:
    - Count: Número de valores no nulos
    - Mean: Media aritmética
    - Std: Desviación estándar
    - Min: Mínimo
    - 25%, 50%, 75%: Percentiles
    - Max: Máximo
    
    Args:
        df (pd.DataFrame): Datos a resumir
        columnas_numericas (list): Columnas específicas (si None, detecta automático)
    
    Returns:
        pd.DataFrame: Tabla formateada con nombres en español
    
    Ejemplo:
        >>> df = cargar_csv('parcelas.csv')
        >>> resumen_estadistico(df)
        
        Variable          Count   Media  Desv. Est.    Mín     Mediana    Máx
        dosis_N            116  105,34      42,12   0,00    105,00  180,00
        rendimiento        116   10,64       3,00   1,71     10,54   25,15
    """
    import numpy as np
    
    if columnas_numericas is None:
        columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    resumen = df[columnas_numericas].describe().T
    
    # Renombrar columnas en español
    resumen.columns = ['Count', 'Media', 'Desv. Est.', 'Mín', '25%', 'Mediana', '75%', 'Máx']
    
    # Formatear números
    for col in resumen.columns:
        if col != 'Count':
            resumen[col] = resumen[col].apply(lambda x: formatear_numero(x, decimales=2))
        else:
            resumen[col] = resumen[col].astype(int)
    
    return resumen
