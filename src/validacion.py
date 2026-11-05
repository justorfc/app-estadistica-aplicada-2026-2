"""
Validaciones pedagógicas para la app de estadística aplicada.

Detecta errores comunes y proporciona mensajes claros que expliquen
al estudiante qué pasó y cómo corregirlo.
"""

import pandas as pd
import streamlit as st


def validar_archivo_cargado(df):
    """
    Verifica que se haya cargado un archivo y tenga datos.
    
    Parámetros
    ----------
    df : pd.DataFrame o None
        DataFrame cargado o None
    
    Retorna
    -------
    bool
        True si es válido, False si hay error (mostrando st.error)
    """
    if df is None:
        st.error(
            "📁 **No hay archivo cargado.** "
            "Por favor, carga un archivo CSV en la barra lateral."
        )
        return False
    
    if df.empty:
        st.error(
            "📭 **El archivo está vacío.** "
            "Verifica que el CSV tenga al menos una fila de datos."
        )
        return False
    
    return True


def validar_columnas_seleccionadas(columnas_seleccionadas):
    """
    Verifica que se hayan seleccionado columnas.
    
    Parámetros
    ----------
    columnas_seleccionadas : list
        Lista de columnas seleccionadas
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    if not columnas_seleccionadas or len(columnas_seleccionadas) == 0:
        st.error(
            "📊 **No hay columnas seleccionadas.** "
            "En la barra lateral, selecciona al menos una columna numérica "
            "para analizar."
        )
        return False
    
    return True


def validar_variable_numerica(serie, nombre_variable):
    """
    Verifica que una variable sea numérica.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie a validar
    nombre_variable : str
        Nombre de la variable (para el mensaje)
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    if not pd.api.types.is_numeric_dtype(serie):
        st.error(
            f"🔢 **'{nombre_variable}' no es numérica.** "
            f"Este análisis requiere valores números (enteros o decimales). "
            f"Verifica que la columna no contenga texto o símbolos especiales."
        )
        return False
    
    return True


def validar_datos_faltantes(df, nombre_variable, permitir_faltantes=False):
    """
    Verifica que no haya datos faltantes (NaN).
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    nombre_variable : str
        Nombre de la columna a revisar
    permitir_faltantes : bool, default False
        Si True, solo advierte; si False, detiene con error
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    faltantes = df[nombre_variable].isna().sum()
    
    if faltantes > 0:
        porcentaje = (faltantes / len(df)) * 100
        mensaje = (
            f"⚠️  **'{nombre_variable}' tiene {faltantes} valores faltantes "
            f"({porcentaje:.1f}% del total).** "
            f"Para este análisis, se usarán solo los {len(df) - faltantes} valores completos."
        )
        
        if permitir_faltantes:
            st.warning(mensaje)
            return True
        else:
            st.error(
                f"❌ {mensaje}\n\n"
                f"**Solución:** Verifica tu archivo y asegúrate de que "
                f"no haya celdas vacías o valores 'NaN'."
            )
            return False
    
    return True


def validar_tamaño_minimo(n, minimo, contexto):
    """
    Verifica que haya suficientes datos.
    
    Parámetros
    ----------
    n : int
        Número de datos disponibles
    minimo : int
        Número mínimo requerido
    contexto : str
        Descripción del análisis (ej: "para ajustar una distribución")
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    if n < minimo:
        st.error(
            f"📉 **Datos insuficientes {contexto}.** "
            f"Tienes {n} datos, pero se requieren al menos {minimo}. "
            f"\n\n**Solución:** Carga más datos o usa una muestra más grande."
        )
        return False
    
    return True


def validar_valores_positivos(serie, nombre_variable):
    """
    Verifica que todos los valores sean positivos.
    
    Parámetros
    ----------
    serie : pd.Series
        Serie a validar
    nombre_variable : str
        Nombre de la variable
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    negativos = (serie < 0).sum()
    ceros = (serie == 0).sum()
    
    if negativos > 0 or ceros > 0:
        msg_extra = ""
        if negativos > 0:
            msg_extra += f"{negativos} negativos"
        if ceros > 0:
            if msg_extra:
                msg_extra += f" y {ceros} ceros"
            else:
                msg_extra = f"{ceros} ceros"
        
        st.error(
            f"➖ **'{nombre_variable}' contiene valores no positivos:** {msg_extra}. "
            f"Para análisis de extremos, se requieren valores estrictamente positivos. "
            f"\n\n**Solución:** Revisa los datos o aplica una transformación "
            f"(por ejemplo, suma una constante o usa valor absoluto)."
        )
        return False
    
    return True


def validar_variabilidad(serie, nombre_variable):
    """
    Verifica que la serie tenga variabilidad (no sea constante).
    
    Parámetros
    ----------
    serie : pd.Series
        Serie a validar
    nombre_variable : str
        Nombre de la variable
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    desv = serie.std()
    
    if desv == 0 or desv < 1e-10:
        st.error(
            f"🔍 **'{nombre_variable}' no tiene variabilidad.** "
            f"Todos los valores son idénticos o prácticamente iguales. "
            f"Esto impide cualquier análisis estadístico significativo. "
            f"\n\n**Solución:** Verifica que tus datos sean correctos. "
            f"Si es un error de ingreso, corrígelo. Si no, tus datos no son apropiados "
            f"para este análisis."
        )
        return False
    
    return True


def validar_correlacion(x, y, nombre_x, nombre_y):
    """
    Verifica que x e y no sean colineales perfectos.
    
    Parámetros
    ----------
    x, y : pd.Series
        Variables a correlacionar
    nombre_x, nombre_y : str
        Nombres de las variables
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    # Remover NaN
    datos = pd.DataFrame({nombre_x: x, nombre_y: y}).dropna()
    
    if len(datos) < 3:
        st.error(
            f"📊 **Datos insuficientes para regresión.** "
            f"Después de remover valores faltantes, quedan solo {len(datos)} datos. "
            f"Se requieren al menos 3. "
            f"\n\n**Solución:** Verifica que ambas variables tengan datos completos."
        )
        return False
    
    # Verificar que x tenga variabilidad
    if datos[nombre_x].std() == 0:
        st.error(
            f"📍 **La variable '{nombre_x}' no tiene variabilidad.** "
            f"No puedo ajustar una regresión si X es constante."
        )
        return False
    
    # Verificar que y tenga variabilidad
    if datos[nombre_y].std() == 0:
        st.warning(
            f"⚠️  **La variable '{nombre_y}' no tiene variabilidad.** "
            f"Si ajustamos, obtendremos R²=0 (sin relación)."
        )
        # Esto no es error, solo aviso
    
    return True


def validar_serie_temporal(n_datos, n_minimo=24):
    """
    Verifica que haya suficientes datos para análisis de series.
    
    Parámetros
    ----------
    n_datos : int
        Número de datos disponibles
    n_minimo : int, default 24
        Número mínimo requerido (por defecto, 24 meses = 2 años)
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    if n_datos < n_minimo:
        st.error(
            f"📅 **Serie demasiado corta.** "
            f"Tienes {n_datos} observaciones, pero se requieren al menos {n_minimo} "
            f"(generalmente 2 años de datos mensuales). "
            f"Esto es necesario para identificar patrones de estacionalidad. "
            f"\n\n**Solución:** Carga una serie temporal más larga o usa datos a escala diferente "
            f"(diaria, semanal, etc., siempre que tengas al menos {n_minimo} puntos)."
        )
        return False
    
    return True


def validar_ajuste_modelo(exito, tipo_modelo, error_msg=""):
    """
    Verifica que el ajuste de un modelo haya sido exitoso.
    
    Parámetros
    ----------
    exito : bool
        True si el ajuste fue exitoso
    tipo_modelo : str
        Tipo de modelo (ej: "distribución Gumbel", "AutoTS")
    error_msg : str, default ""
        Mensaje técnico del error (se ocultará al usuario)
    
    Retorna
    -------
    bool
        True si es válido, False si hay error
    """
    if not exito:
        st.error(
            f"⚙️  **No fue posible ajustar {tipo_modelo}.** "
            f"Esto puede deberse a: "
            f"\n• Datos con valores extremos o inconsistentes"
            f"\n• Serie muy corta o sin variabilidad suficiente"
            f"\n• Parámetros fuera de rango numérico válido"
            f"\n\n**Solución:** Revisa tus datos. Si usas muestras de prueba pequeñas, "
            f"considera usar datos más grandes o una base de datos completa."
        )
        return False
    
    return True


def limpiar_datos(df, columnas):
    """
    Limpia los datos: remueve filas con NaN en columnas especificadas.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame original
    columnas : list
        Columnas a considerar para limpieza
    
    Retorna
    -------
    pd.DataFrame
        DataFrame limpio
    
    Nota
    ----
    Informa al usuario cuántas filas fueron removidas.
    """
    n_original = len(df)
    df_limpio = df[columnas].dropna()
    n_limpio = len(df_limpio)
    
    if n_original != n_limpio:
        n_removidas = n_original - n_limpio
        st.info(
            f"🧹 **Limpieza automática:** Se removieron {n_removidas} filas "
            f"con valores faltantes. Se usan {n_limpio} datos completos."
        )
    
    return df_limpio
