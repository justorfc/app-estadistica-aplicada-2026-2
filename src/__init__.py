"""
Módulo principal: Utilidades y funciones compartidas para la app de Estadística Aplicada.

Este paquete contiene:
- utilidades.py: Funciones auxiliares generales (carga de datos, formateo, etc.)
- datos.py: Estadística descriptiva y análisis de datos
- eda.py: Análisis exploratorio de datos
- distribuciones.py: Ajuste de modelos de distribución
- regresion.py: Análisis de regresión
- series_tiempo.py: Descomposición y pronóstico de series de tiempo
"""

__version__ = "0.1.0"
__author__ = "Tutor de Estadística Aplicada"

# Importar funciones comunes para facilitar acceso
try:
    from .utilidades import cargar_datos, formatear_numero
    __all__ = ['cargar_datos', 'formatear_numero']
except ImportError:
    # Si utilidades.py no existe aún, no fallar
    pass
