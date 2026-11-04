"""
Paquete src: Módulos compartidos para la app de Estadística Aplicada.

Submódulos:
- datos.py: Carga CSV, metadatos, tarjeta estudiante
- eda.py: Análisis exploratorio (próximamente)
- distribuciones.py: Ajuste de distribuciones (próximamente)
- regresion.py: Regresión lineal (próximamente)
- series_tiempo.py: Series de tiempo (próximamente)

Uso:
    from datos import cargar_csv, cargar_metadatos, tarjeta_estudiante
    df = cargar_csv('parcelas.csv')
    metadatos = cargar_metadatos()
    tarjeta_estudiante('sidebar')
"""

__version__ = "0.1.0"
__author__ = "Tutor Estadística - Ingeniería Agrícola, Unisucre"

# Exports comunes desde datos.py
from .datos import (
    cargar_csv,
    cargar_metadatos,
    tarjeta_estudiante,
    obtener_ruta_datos,
    formatear_numero,
    resumen_estadistico,
    tipos_de_variables,
    valores_faltantes
)

__all__ = [
    'cargar_csv',
    'cargar_metadatos',
    'tarjeta_estudiante',
    'obtener_ruta_datos',
    'formatear_numero',
    'resumen_estadistico',
    'tipos_de_variables',
    'valores_faltantes'
]
