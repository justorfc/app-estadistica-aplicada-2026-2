# Instrucciones Permanentes para Copilot - App de Estadística Aplicada

## Principios Generales

### Idioma y Comunicación
- **Responder siempre en español**.
- **Explicar cada paso antes de ejecutarlo** en 1-2 líneas claras.
- Usar vocabulario técnico pero accesible para estudiantes de Ingeniería Agrícola.

### Entorno y Herramientas
- **Usar siempre** `.venv/bin/python`, `.venv/bin/pip` y `.venv/bin/streamlit` en todos los comandos.
- **No crear nuevas dependencias** sin preguntar al estudiante.
- Usar **solo las librerías** especificadas en `requirements.txt`.
- Si se necesita agregar una librería, pedir permiso explícito antes de modificar `requirements.txt`.

## Código y Documentación

### Estilo de Código
- **Comentar cada sección importante** paso a paso.
- Escribir **docstrings en español** con formato:
  ```python
  def nombre_funcion(param1, param2):
      """
      Descripción breve en español.
      
      Parámetros
      ----------
      param1 : tipo
          Descripción
      param2 : tipo
          Descripción
      
      Retorna
      -------
      tipo
          Descripción del retorno
      
      Ejemplo
      -------
      >>> resultado = nombre_funcion(10, 20)
      >>> print(resultado)
      """
  ```
- Usar **nombres de variables descriptivos** en español cuando sea apropiado (ej: `numero_datos`, `valor_p`).

### Gráficas y Visualización
- **Ejes siempre con nombre y unidades**.
- Ejemplo: `plt.xlabel('Precipitación (mm)')`, `plt.ylabel('Frecuencia')`
- Usar **seaborn y matplotlib** como librerías principales.
- Gráficas Plotly solo para visualizaciones interactivas avanzadas.
- Temas: usar `seaborn.set_style("darkgrid")` o similar para legibilidad.

### Interfaz de Usuario
- **Todos los textos en la interfaz Streamlit en español**.
- Usar títulos claros (ej: `st.title("Análisis de Precipitación Máxima Anual")`)
- Mantener consistencia en naming: "Precipitación", "Distribución", "Período de retorno", etc.

## Gestión de Archivos

### Carpeta `datos/`
- **NO modificar** una vez creada.
- Solo lectura durante el proyecto.
- Si se agrega datos de ejemplo, crear `datos/generar_datos.py` documentado.
- **NO tocar `generar_datos.py`** después de creado.

### Estructura de Proyecto
- Mantener modularidad: `src/` para lógica, `pages/` para UI, `datos/` para datasets.
- No crear archivos fuera de la estructura definida en `PLAN_DESARROLLO.md`.

## Git y Versionado

### Commits
- **NO hacer commits** ni `git push`.
- El estudiante es responsable de commits.
- Si se pide verificar cambios, usar `git status` sin hacer commit.

## Verificación Final

### Al Terminar Cada Tarea
1. Ejecutar: `.venv/bin/streamlit run app.py`
2. Verificar que **no haya errores** de sintaxis o importación.
3. Verificar que la app cargue correctamente.
4. Si hay errores, **mostrar claramente dónde están y corregir**.
5. Probar la funcionalidad básica de la página implementada.

### Before Moving Forward
- ✅ Código sin errores de sintaxis
- ✅ Imports correctamente resueltos
- ✅ Streamlit ejecuta sin excepciones
- ✅ Funcionalidad de la página verificada

## Testing

### Desarrollo de Tests
- Usar **pytest** en carpeta `verificacion/`.
- Tests para funciones de `src/` (lógica pura).
- Nombrar archivos `test_*.py`.
- Ejecutar con: `.venv/bin/pytest verificacion/ -v`

## Especificidades del Proyecto

### Estadística
- Usar **scipy.stats** para distribuciones (Normal, Lognormal, Gamma, Weibull, Gumbel, GEV).
- Usar **statsmodels** para pruebas estadísticas y regresión.
- **Validar cálculos** contra referencias conocidas (R, libros de estadística).

### Streamlit
- Usar `@st.cache_data` para cachear datos pesados.
- Usar `@st.cache_resource` para modelos reutilizables.
- Mantener orden lógico en widgets (inputs → procesamiento → outputs).

### Datos
- Siempre validar integridad antes de análisis.
- Manejo de valores faltantes: documentar estrategia (eliminar, imputar, etc.).
- Detección de outliers: usar IQR y Z-score, nunca silenciosamente eliminar.

---

## Resumen de Comandos Frecuentes

```bash
# Entorno virtual
.venv/bin/python --version
.venv/bin/pip install -r requirements.txt

# Ejecutar app
.venv/bin/streamlit run app.py

# Testing
.venv/bin/pytest verificacion/ -v
.venv/bin/pytest verificacion/ --cov=src

# Git (sin hacer commit)
git status
git diff
```

---

**Última actualización:** 2026-11-04  
**Versión del proyecto:** 1.0 (Fase 1: Infraestructura)
