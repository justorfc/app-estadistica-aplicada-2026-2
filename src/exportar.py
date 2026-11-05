"""
Exportación de resultados en múltiples formatos.

Permite descargar tablas (Excel), figuras (PNG, PDF) y reportes (Markdown).
"""

import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


def tabla_a_excel(df, nombre_hoja="Resultados"):
    """
    Convierte un DataFrame a Excel (BytesIO).
    
    Parámetros
    ----------
    df : pd.DataFrame
        Tabla a exportar
    nombre_hoja : str, default "Resultados"
        Nombre de la hoja de cálculo
    
    Retorna
    -------
    BytesIO
        Buffer con el archivo Excel
    """
    buffer = io.BytesIO()
    
    # Usar ExcelWriter con openpyxl para más control
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=nombre_hoja, index=False)
        
        # Formatear: encabezados en negrita y azul
        worksheet = writer.sheets[nombre_hoja]
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Ajustar ancho de columnas
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    buffer.seek(0)
    return buffer


def figura_a_png(fig):
    """
    Convierte una figura de matplotlib a PNG (BytesIO).
    
    Parámetros
    ----------
    fig : matplotlib.figure.Figure
        Figura a exportar
    
    Retorna
    -------
    BytesIO
        Buffer con la imagen PNG
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    return buffer


def figura_a_pdf(fig):
    """
    Convierte una figura de matplotlib a PDF (BytesIO).
    
    Parámetros
    ----------
    fig : matplotlib.figure.Figure
        Figura a exportar
    
    Retorna
    -------
    BytesIO
        Buffer con el PDF
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='pdf', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    return buffer


def crear_reporte_eda(df_original, columnas_seleccionadas, stats_dict):
    """
    Crea un reporte Markdown con resultados de EDA.
    
    Parámetros
    ----------
    df_original : pd.DataFrame
        DataFrame cargado
    columnas_seleccionadas : list
        Columnas analizadas
    stats_dict : dict
        Diccionario de estadísticas {var: {medida: valor}}
    
    Retorna
    -------
    str
        Reporte en formato Markdown
    """
    reporte = "# Reporte de Análisis Exploratorio de Datos (EDA)\n\n"
    
    reporte += f"## Resumen de Datos\n"
    reporte += f"- **Número de filas:** {len(df_original)}\n"
    reporte += f"- **Columnas analizadas:** {', '.join(columnas_seleccionadas)}\n"
    reporte += f"- **Fecha de generación:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    reporte += "## Estadísticas Descriptivas\n\n"
    
    for variable, stats in stats_dict.items():
        reporte += f"### {variable}\n"
        reporte += f"| Medida | Valor |\n"
        reporte += f"|--------|-------|\n"
        for medida, valor in stats.items():
            if isinstance(valor, float):
                reporte += f"| {medida} | {valor:.4f} |\n"
            else:
                reporte += f"| {medida} | {valor} |\n"
        reporte += "\n"
    
    return reporte


def crear_reporte_distribuciones(variable, params_gumbel, x_periodos, riesgo):
    """
    Crea un reporte Markdown con resultados de distribuciones.
    
    Parámetros
    ----------
    variable : str
        Nombre de la variable analizada
    params_gumbel : dict
        Parámetros Gumbel {mu, sigma, beta}
    x_periodos : dict
        Períodos de retorno {10: x10, 50: x50, 100: x100}
    riesgo : dict
        Riesgo {(50, 25): valor}
    
    Retorna
    -------
    str
        Reporte en formato Markdown
    """
    reporte = "# Reporte de Análisis de Distribuciones de Extremos\n\n"
    
    reporte += f"## Variable Analizada: {variable}\n\n"
    
    reporte += "## Parámetros de la Distribución Gumbel\n\n"
    reporte += "| Parámetro | Valor |\n"
    reporte += "|-----------|-------|\n"
    reporte += f"| Media (μ) | {params_gumbel['mu']:.4f} |\n"
    reporte += f"| Beta (β) | {params_gumbel['beta']:.4f} |\n"
    reporte += f"| Sigma (σ) | {params_gumbel.get('sigma', 'N/A'):.4f} |\n\n"
    
    reporte += "## Períodos de Retorno\n\n"
    reporte += "| Período (años) | Valor (mm) |\n"
    reporte += "|----------------|------------|\n"
    for periodo, valor in x_periodos.items():
        reporte += f"| {periodo} | {valor:.4f} |\n"
    reporte += "\n"
    
    reporte += "## Riesgo de Excedencia\n\n"
    for (T, N), valor in riesgo.items():
        reporte += f"- Riesgo de excedencia en {T} años durante {N} años: {valor:.4f} ({valor*100:.2f}%)\n"
    
    return reporte


def crear_reporte_regresion(x_var, y_var, coeficientes, r2, p_value, ic_95):
    """
    Crea un reporte Markdown con resultados de regresión.
    
    Parámetros
    ----------
    x_var, y_var : str
        Nombres de variables
    coeficientes : dict
        Coeficientes {b0, b1}
    r2 : float
        Coeficiente de determinación
    p_value : float
        P-valor de la regresión
    ic_95 : tuple
        Intervalo de confianza (b1_inf, b1_sup)
    
    Retorna
    -------
    str
        Reporte en formato Markdown
    """
    reporte = "# Reporte de Regresión Lineal Simple\n\n"
    
    reporte += f"## Variables\n"
    reporte += f"- **Variable independiente (X):** {x_var}\n"
    reporte += f"- **Variable dependiente (Y):** {y_var}\n\n"
    
    reporte += "## Ecuación de la Recta\n\n"
    reporte += f"**ŷ = {coeficientes['b0']:.4f} + {coeficientes['b1']:.4f} × {x_var}**\n\n"
    
    reporte += "## Bondad de Ajuste\n\n"
    reporte += f"| Medida | Valor |\n"
    reporte += f"|--------|-------|\n"
    reporte += f"| R² | {r2:.4f} |\n"
    reporte += f"| % Variabilidad explicada | {r2*100:.2f}% |\n"
    reporte += f"| p-value | {p_value:.4f} |\n"
    reporte += f"| Significancia | {'Sí (p < 0.05)' if p_value < 0.05 else 'No (p ≥ 0.05)'} |\n\n"
    
    reporte += "## Intervalo de Confianza 95%\n\n"
    reporte += f"**IC 95% para b₁:** [{ic_95[0]:.4f}, {ic_95[1]:.4f}]\n\n"
    
    return reporte


def crear_reporte_series(n_entrenamiento, metodos_pronos, metricas):
    """
    Crea un reporte Markdown con resultados de series de tiempo.
    
    Parámetros
    ----------
    n_entrenamiento : int
        Número de datos de entrenamiento
    metodos_pronos : dict
        Métodos y pronósticos {metodo: [valores]}
    metricas : dict
        Métricas por método {metodo: {MAE, RMSE, SMAPE}}
    
    Retorna
    -------
    str
        Reporte en formato Markdown
    """
    reporte = "# Reporte de Análisis de Series de Tiempo\n\n"
    
    n_total = n_entrenamiento + 6  # Asumimos 6 meses de validación
    
    reporte += f"## Configuración\n"
    reporte += f"- **Período de entrenamiento:** {n_entrenamiento} observaciones\n"
    reporte += f"- **Período de validación:** 6 observaciones\n"
    reporte += f"- **Total:** {n_total} observaciones\n\n"
    
    reporte += "## Comparación de Métodos de Pronóstico\n\n"
    reporte += "| Método | MAE | RMSE | SMAPE |\n"
    reporte += "|--------|-----|------|-------|\n"
    
    for metodo, metros_dict in metricas.items():
        mae = metros_dict.get('MAE', 0)
        rmse = metros_dict.get('RMSE', 0)
        smape = metros_dict.get('SMAPE', 0)
        reporte += f"| {metodo} | {mae:.4f} | {rmse:.4f} | {smape:.2f}% |\n"
    
    reporte += "\n"
    
    # Identificar ganador
    ganador = min(metricas.keys(), key=lambda m: metricas[m].get('SMAPE', float('inf')))
    reporte += f"## Método Ganador\n\n"
    reporte += f"**{ganador}** con SMAPE = {metricas[ganador]['SMAPE']:.2f}%\n\n"
    
    return reporte


def botones_descarga(titulo_seccion, archivos_dict):
    """
    Crea un expander con botones de descarga.
    
    Parámetros
    ----------
    titulo_seccion : str
        Título del expander (ej: "Descargar resultados")
    archivos_dict : dict
        Diccionario {nombre_boton: (contenido, tipo, extension)}
        - tipo: 'excel', 'png', 'pdf', 'markdown'
        - extension: 'xlsx', 'png', 'pdf', 'md'
        - contenido: BytesIO o str
    """
    with st.expander(f"📥 {titulo_seccion}"):
        cols = st.columns(len(archivos_dict))
        
        for idx, (nombre_archivo, (contenido, tipo_archivo, extension)) in enumerate(archivos_dict.items()):
            with cols[idx]:
                # Definir etiqueta y MIME type
                if tipo_archivo == 'excel':
                    label = f"📊 {nombre_archivo}"
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    filename = f"{nombre_archivo}.{extension}"
                elif tipo_archivo == 'png':
                    label = f"🖼️  {nombre_archivo}"
                    mime = "image/png"
                    filename = f"{nombre_archivo}.{extension}"
                elif tipo_archivo == 'pdf':
                    label = f"📄 {nombre_archivo}"
                    mime = "application/pdf"
                    filename = f"{nombre_archivo}.{extension}"
                elif tipo_archivo == 'markdown':
                    label = f"📝 {nombre_archivo}"
                    mime = "text/markdown"
                    filename = f"{nombre_archivo}.{extension}"
                    # Convertir string a bytes para markdown
                    if isinstance(contenido, str):
                        contenido = contenido.encode('utf-8')
                else:
                    continue
                
                st.download_button(
                    label=label,
                    data=contenido,
                    file_name=filename,
                    mime=mime,
                    key=f"descargar_{nombre_archivo}_{idx}"
                )
