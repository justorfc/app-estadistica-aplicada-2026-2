"""
Página 1_Datos.py: Módulo de Carga y Exploración de Datos

Permite al estudiante:
1. Elegir entre archivos de datos predefinidos (parcelas, precipitación, clima, secado)
2. Cargar un archivo CSV o Excel personalizado (opcional)
3. Ver tabla de datos, tipos de variables, valores faltantes
4. Descargar los datos en CSV

Pedagogía:
- El estudiante PRIMERO explora datos a mano con muestra_*.csv
- Luego verifica con esta app usando archivos completos
- Aprende a interpretar tipos de dato y completitud de datos
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO, BytesIO

# Importar funciones de src/datos.py
ruta_src = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(ruta_src))
from datos import (
    cargar_csv,
    cargar_metadatos,
    tarjeta_estudiante,
    tipos_de_variables,
    valores_faltantes,
    resumen_estadistico
)

# Configuración de página
st.set_page_config(page_title="Datos", layout="wide")

# ============================================================================
# SIDEBAR: Tarjeta del estudiante
# ============================================================================
with st.sidebar:
    tarjeta_estudiante()

# ============================================================================
# ENCABEZADO
# ============================================================================
st.markdown("# 📊 Datos")
st.markdown("## Carga y Exploración Básica de Datos")

st.info(
    "📌 Esta página te enseña a **cargar, explorar y validar datos**. "
    "Elige un archivo predefinido o carga el tuyo en CSV/Excel. "
    "Verifica tipos de dato, completitud y estadísticas básicas."
)

# ============================================================================
# SECCIÓN 1: SELECTOR DE ARCHIVOS
# ============================================================================
st.markdown("---")
st.markdown("### 1️⃣ Elige un Archivo de Datos")

# Diccionario con descripciones
archivos_disponibles = {
    "parcelas.csv": {
        "descripcion": "Rendimiento agrícola en diferentes parcelas",
        "contenido": "Suelo, riego, dosis N, lámina, materia orgánica, pH, rendimiento (t/ha)",
        "uso": "EDA, Regresión",
        "muestra": "muestra_eda10.csv"
    },
    "precip_max_anual.csv": {
        "descripcion": "Precipitación máxima anual en 24 horas",
        "contenido": "Año (1986-2025), precipitación máxima (mm), distribución Gumbel",
        "uso": "Distribuciones, período de retorno",
        "muestra": "muestra_dist10.csv"
    },
    "clima_mensual.csv": {
        "descripcion": "Datos de clima mensual (2015-2025)",
        "contenido": "Fecha, precipitación (régimen bimodal Caribe), temperatura (°C)",
        "uso": "Series de tiempo, pronósticos",
        "muestra": "muestra_series24.csv"
    },
    "secado.csv": {
        "descripcion": "Cinética de secado en capa delgada",
        "contenido": "Tiempo (min), MR (razón de humedad), modelo de Page",
        "uso": "Distribuciones (modelo thin-layer drying)",
        "muestra": "No aplica"
    }
}

col1, col2 = st.columns(2)

with col1:
    archivo_seleccionado = st.selectbox(
        "Selecciona un archivo:",
        options=list(archivos_disponibles.keys()),
        format_func=lambda x: f"📋 {x}",
        index=0,
        help="Elige uno de los archivos de datos predefinidos"
    )

with col2:
    st.markdown("")
    if st.button("📚 Ver muestra pequeña", help="Carga muestra para cálculos a mano"):
        muestra = archivos_disponibles[archivo_seleccionado]["muestra"]
        if muestra != "No aplica":
            st.info(f"👉 Usa `{muestra}` para aprender a mano primero")

# Información del archivo
info_archivo = archivos_disponibles[archivo_seleccionado]
st.write(f"**Descripción:** {info_archivo['descripcion']}")
st.write(f"**Contenido:** {info_archivo['contenido']}")
st.write(f"**Usar en:** {info_archivo['uso']}")

# ============================================================================
# SECCIÓN 2: FILE UPLOADER (OPCIONAL)
# ============================================================================
st.markdown("---")
st.markdown("### 2️⃣ O Carga Tu Propio Archivo (Opcional)")

archivo_usuario = st.file_uploader(
    "Sube un CSV o Excel (si no subes nada, usaremos datos predefinidos):",
    type=["csv", "xlsx", "xls"],
    help="Soporta CSV y Excel. Debe tener encabezados (header)"
)

# Decidir cuál archivo usar
if archivo_usuario is not None:
    # Cargar archivo del usuario
    try:
        if archivo_usuario.name.endswith('.csv'):
            df = pd.read_csv(archivo_usuario, parse_dates=True)
        else:  # xlsx o xls
            df = pd.read_excel(archivo_usuario)
        
        st.success(f"✅ Archivo cargado: {archivo_usuario.name}")
        nombre_archivo_actual = archivo_usuario.name
    except Exception as e:
        st.error(f"❌ Error al cargar archivo: {e}")
        df = cargar_csv(archivo_seleccionado)
        nombre_archivo_actual = archivo_seleccionado
else:
    # Usar archivo predefinido
    df = cargar_csv(archivo_seleccionado)
    nombre_archivo_actual = archivo_seleccionado

# ============================================================================
# SECCIÓN 3: TABLA DE DATOS
# ============================================================================
st.markdown("---")
st.markdown("### 3️⃣ Tabla de Datos")

# Métricas: filas, columnas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Filas", len(df))
with col2:
    st.metric("📋 Columnas", len(df.columns))
with col3:
    st.metric("💾 Tamaño", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# Dataframe interactivo
st.dataframe(
    df,
    use_container_width=True,
    height=300,
    hide_index=False
)

# ============================================================================
# SECCIÓN 4: TIPOS DE VARIABLES
# ============================================================================
st.markdown("---")
st.markdown("### 4️⃣ Clasificación de Variables")

st.write("**¿Qué tipo de dato es cada variable?** Aprende a clasificar:")
st.markdown("""
- **Cualitativa Nominal:** Texto sin orden (ej: color, suelo, sexo)
- **Cualitativa Ordinal:** Texto con orden (ej: bajo/medio/alto)
- **Cuantitativa Discreta:** Números enteros (ej: cantidad de plantas)
- **Cuantitativa Continua:** Números reales (ej: rendimiento en t/ha, precipitación en mm)
- **Temporal:** Fechas y tiempos
""")

df_tipos = tipos_de_variables(df)
st.dataframe(
    df_tipos,
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# SECCIÓN 5: VALORES FALTANTES
# ============================================================================
st.markdown("---")
st.markdown("### 5️⃣ Análisis de Valores Faltantes (N/D)")

st.write("**¿Qué variables tienen datos incompletos?** Identifica faltantes:")

df_faltantes = valores_faltantes(df)

# Filtrar solo variables con faltantes
df_faltantes_con_datos = df_faltantes[df_faltantes['Faltantes'] > 0]

if len(df_faltantes_con_datos) > 0:
    st.warning(f"⚠️ {len(df_faltantes_con_datos)} variable(s) con datos faltantes")
    st.dataframe(
        df_faltantes_con_datos,
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ Todos los datos están completos (sin N/D)")

# Tabla completa de N/D
with st.expander("📊 Ver tabla completa de faltantes (todas las variables)"):
    st.dataframe(
        df_faltantes,
        use_container_width=True,
        hide_index=True
    )

# ============================================================================
# SECCIÓN 6: ESTADÍSTICAS DESCRIPTIVAS
# ============================================================================
st.markdown("---")
st.markdown("### 6️⃣ Estadísticas Descriptivas")

st.write("**Resumen de variables numéricas:** Media, desviación estándar, mín, máx, cuartiles")

df_resumen = resumen_estadistico(df)
st.dataframe(
    df_resumen,
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# SECCIÓN 7: DESCARGA DE DATOS
# ============================================================================
st.markdown("---")
st.markdown("### 7️⃣ Descargar Datos")

# Opción 1: Descargar como CSV
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
csv_string = csv_buffer.getvalue()

st.download_button(
    label="⬇️ Descargar como CSV",
    data=csv_string,
    file_name=f"datos_{nombre_archivo_actual}",
    mime="text/csv",
    help="Descarga los datos en formato CSV"
)

# Opción 2: Descargar como Excel
col1, col2 = st.columns(2)

with col1:
    # Crear archivo Excel en memoria
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos', index=False)
        df_tipos.to_excel(writer, sheet_name='Tipos de Variables', index=False)
        df_faltantes.to_excel(writer, sheet_name='Faltantes', index=False)
        df_resumen.to_excel(writer, sheet_name='Estadísticas', index=False)
    
    excel_buffer.seek(0)
    
    st.download_button(
        label="⬇️ Descargar como Excel (4 hojas)",
        data=excel_buffer.getvalue(),
        file_name=f"datos_{nombre_archivo_actual.replace('.csv', '.xlsx')}",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Descarga con 4 hojas: Datos, Tipos, Faltantes, Estadísticas"
    )

# ============================================================================
# SECCIÓN 8: HABILIDADES QUE PRACTICARÁS
# ============================================================================
st.markdown("---")
st.markdown("### ✏️ Habilidades que Practicarás")

st.markdown("""
**Pandas:**
- `pd.read_csv()`: Cargar archivos CSV
- `pd.read_excel()`: Cargar archivos Excel
- `df.dtypes`: Tipos de dato
- `df.isnull()`: Detectar faltantes
- `df.describe()`: Estadísticas descriptivas

**NumPy:**
- `np.isnan()`: Valores faltantes
- `np.percentile()`: Cuartiles y percentiles

**Streamlit:**
- `st.selectbox()`: Selector de opciones
- `st.file_uploader()`: Cargar archivos
- `st.dataframe()`: Mostrar tablas interactivas
- `st.metric()`: Mostrar números destacados
- `st.download_button()`: Descargar archivos

**Interpretación Estadística:**
- Clasificar variables (cualitativa vs cuantitativa)
- Identificar datos faltantes
- Evaluar completitud de datos
- Interpretar estadísticas descriptivas por tipo de variable
""")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    """
    💡 **Consejo:** Comienza con `muestra_eda10.csv` (10 parcelas) o `muestra_dist10.csv` 
    (10 años) para aprender a mano. Luego verifica con archivos completos en esta app.
    """
)
