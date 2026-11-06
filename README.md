# Aplicación de Estadística Aplicada: Análisis de Precipitación Máxima Anual

## Datos del Estudiante

| Campo | Valor |
|-------|-------|
| **Nombre** | Justo Fuentes |
| **Código** | 6820995 |
| **Grupo** | Ingeniería Agrícola |
| **Cultivo de Estudio** | Ñame |
| **Municipio** | Sincelejo |
| **Huella de Datos** | 43DA0A2A |

---

## Descripción General

Esta es una aplicación web interactiva desarrollada en **Streamlit** para el análisis estadístico aplicado a la ingeniería agrícola, con énfasis especial en el estudio de **precipitación máxima anual** en el municipio de Sincelejo. La aplicación implementa un flujo completo de análisis desde la carga de datos hasta la modelación probabilística y pronóstico de series de tiempo, permitiendo al estudiante explorar metodologías estadísticas fundamentales en el contexto de la agronomía.

---

## Objetivo Académico

Desarrollar competencias en **análisis estadístico aplicado** mediante:

1. **Exploración de datos (EDA):** Caracterizar variables agroclimáticas a través de análisis descriptivos y visualizaciones.
2. **Modelación probabilística:** Ajustar distribuciones teóricas a datos de precipitación máxima anual y evaluar su bondad de ajuste.
3. **Análisis de regresión:** Establecer relaciones estadísticas entre precipitación y otras variables climáticas.
4. **Pronóstico con series de tiempo:** Generar predicciones a mediano plazo usando modelos estadísticos y de aprendizaje automático.
5. **Comunicación de resultados:** Documentar hallazgos, limitaciones y recomendaciones de forma clara y profesional.

---

## Páginas de la Aplicación

La aplicación consta de **seis páginas principales**:

### 1. **Inicio**
   - Bienvenida y descripción general del proyecto.
   - Objetivo del análisis estadístico.
   - Instrucciones de navegación.
   - Créditos y referencias bibliográficas.

### 2. **Datos**
   - Carga y validación inicial de datos.
   - Estadísticas descriptivas: media, mediana, desviación estándar, cuartiles, asimetría y curtosis.
   - Visualización de series temporal e histogramas.
   - Detección de valores faltantes y atípicos.
   - Opción de descarga de datos limpios.

### 3. **EDA (Análisis Exploratorio de Datos)**
   - Análisis univariado y bivariado.
   - Gráficas: boxplots, violines, Q-Q plots.
   - Matriz de correlaciones.
   - Detección de outliers mediante IQR y Z-score.
   - Tendencias: media móvil, máximos y mínimos por período.

### 4. **Distribuciones**
   - Ajuste de modelos probabilísticos: Normal, Lognormal, Gamma, Weibull, Gumbel, GEV.
   - Pruebas de bondad de ajuste: Kolmogorov-Smirnov y Anderson-Darling.
   - Criterios de información: AIC, BIC, AICc.
   - Cálculo de precipitaciones para períodos de retorno específicos (T años).
   - Gráficas de ajuste visual: histogramas con curvas teóricas superpuestas.

### 5. **Regresión**
   - Regresión lineal simple: precipitación vs. temperatura (u otra variable).
   - Regresión lineal múltiple: incorporación de variables adicionales.
   - Análisis de residuales: normalidad, homocedasticidad, independencia.
   - Diagnósticos: R², RMSE, AIC, BIC.
   - Tabla de coeficientes con intervalos de confianza.
   - Gráficas de ajuste y residuales.

### 6. **Series de Tiempo**
   - Descomposición temporal: tendencia, estacionalidad y residual.
   - Métodos de referencia: naive, seasonal naive, media móvil.
   - Pronósticos con modelos automáticos (AutoTS).
   - Métricas de desempeño: MAE, RMSE, SMAPE.
   - Visualización comparativa de predicciones vs. observados.

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|----------|
| **Python** | 3.9+ | Lenguaje de programación principal |
| **Streamlit** | 1.28+ | Framework para interfaz web interactiva |
| **Pandas** | 2.0+ | Manipulación y análisis de datos |
| **NumPy** | 1.24+ | Cálculos numéricos |
| **Matplotlib** | 3.7+ | Visualización estática |
| **Seaborn** | 0.12+ | Gráficas estadísticas avanzadas |
| **SciPy** | 1.10+ | Funciones estadísticas y distribuciones |
| **Scikit-learn** | 1.3+ | Modelos de regresión y métricas |
| **Statsmodels** | 0.14+ | Análisis econométrico y series de tiempo |
| **AutoTS** | 0.3+ | Pronóstico automático de series de tiempo |

---

## Estructura del Proyecto

```
app-estadistica-aplicada-2026-2/
├── README.md                          # Este archivo
├── BITACORA_IA.md                     # Registro de interacciones con IA
├── LICENSE                             # Licencia del proyecto
├── app.py                              # Punto de entrada principal
├── requirements.txt                    # Dependencias Python
│
├── datos/                              # Datos base (READ-ONLY)
│   ├── metadatos.json                 # Información del estudiante
│   ├── precipitacion.csv              # Serie de precipitación máxima anual
│   └── generar_datos.py               # Script de generación (no modificar)
│
├── src/                                # Módulos de lógica estadística
│   ├── __init__.py
│   ├── carga_datos.py                 # Carga y validación
│   ├── eda.py                         # Análisis exploratorio
│   ├── distribuciones.py              # Modelos probabilísticos
│   ├── regresion.py                   # Análisis de regresión
│   ├── series.py                      # Análisis de series de tiempo
│   └── utils.py                       # Funciones auxiliares
│
├── pages/                              # Páginas de Streamlit
│   ├── 1_Inicio.py
│   ├── 2_Datos.py
│   ├── 3_EDA.py
│   ├── 4_Distribuciones.py
│   ├── 5_Regresion.py
│   └── 6_Series_de_Tiempo.py
│
├── verificacion/                       # Tests y validación
│   ├── test_carga_datos.py
│   ├── test_eda.py
│   ├── test_distribuciones.py
│   ├── test_regresion.py
│   ├── test_series.py
│   └── conftest.py
│
├── docs/                               # Documentación
│   ├── PLAN_DESARROLLO.md             # Especificación técnica
│   └── METODOLOGIA.md                 # Descripción de métodos
│
├── resultados/                         # Outputs generados (no versionados)
│   └── .gitkeep
│
└── .github/                            # Configuración GitHub
    └── copilot-instructions.md        # Instrucciones para IA
```

---

## Cómo Ejecutarla en un Codespace

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/justorfc/app-estadistica-aplicada-2026-2.git
cd app-estadistica-aplicada-2026-2
```

### Paso 2: Crear el Entorno Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate        # En macOS/Linux
# o en Windows:
# .venv\Scripts\activate
```

### Paso 3: Instalar Dependencias
```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

### Paso 4: Generar Datos (Opcional - Ya Están Generados)
Si necesitas regenerar los datos:
```bash
.venv/bin/python generar_datos.py
```

### Paso 5: Ejecutar la Aplicación
```bash
.venv/bin/streamlit run app.py
```

Streamlit abrirá automáticamente la aplicación en `http://localhost:8501` en tu navegador.

### Paso 6: Navegar por las Páginas
- Usa la barra lateral izquierda para cambiar entre páginas.
- Cada página incluye instrucciones adicionales y widgets interactivos.

### Paso 7: Ejecutar Tests (Opcional)
```bash
.venv/bin/pytest verificacion/ -v
# Con cobertura:
.venv/bin/pytest verificacion/ --cov=src
```

---

## App en Línea

### Despliegue en Streamlit Community Cloud

La aplicación está disponible en línea en:

🔗 **[Abre la App aquí](https://share.streamlit.io/justorfc/app-estadistica-aplicada-2026-2)** *(enlace a completar tras despliegue)*

**Nota:** El despliegue en Streamlit Cloud es totalmente gratuito y automático. Cualquier cambio que hagas en el repositorio GitHub se despliega automáticamente en la app en línea.

#### Para desplegar tu propia versión:

1. **Crea una cuenta gratuita** en [Streamlit Community Cloud](https://share.streamlit.io)
2. **Autoriza tu repositorio GitHub**
3. **Conecta este repositorio** especificando:
   - Repository: `justorfc/app-estadistica-aplicada-2026-2`
   - Branch: `main`
   - Main file: `app.py`

Consulta la guía completa en **[GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md](./GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md)** para:
- Preparar `runtime.txt` y `requirements.txt`
- Manejar AutoTS en la nube (lentitud)
- Resolver errores comunes
- Monitoreo y mantenimiento

---

## Metodología: El Lápiz y El Algoritmo

Esta aplicación implementa la metodología **"El Lápiz y el Algoritmo"**, un enfoque pedagógico que equilibra:

1. **El Lápiz (Fundamentos Teóricos):**
   - Comprensión conceptual de cada método estadístico.
   - Deducción manual de fórmulas y cálculos.
   - Documentación clara de supuestos y limitaciones.

2. **El Algoritmo (Implementación Computacional):**
   - Traducción de métodos a código Python.
   - Uso de librerías especializadas (SciPy, Statsmodels, Scikit-learn).
   - Validación de resultados contra referencias conocidas.

**Aplicación en este proyecto:**
- Cada página implementa análisis que el estudiante ha derivado teóricamente.
- El código es transparente: se pueden inspeccionar las fórmulas exactas.
- Los resultados se comparan con cálculos de referencia (ej: R, libros de texto).

---

## Limitaciones

### 1. **Datos Simulados**
   - Los datos de precipitación y variables climáticas son **generados sintéticamente** con base en parámetros estadísticos realistas.
   - No representan mediciones reales; tienen propósito puramente educativo.
   - La correlación entre variables se genera artificialmente.

### 2. **AutoTS con Modelos Rápidos**
   - El módulo **AutoTS** utiliza un conjunto reducido de modelos por eficiencia computacional:
     - ARIMA, Exponential Smoothing, Naive, Seasonal Naive.
     - Excluye redes neuronales y ensambles complejos.
   - Período de entrenamiento: 18 meses; validación: 6 meses.
   - Tiene naturaleza stochástica: resultados pueden variar ligeramente entre ejecuciones.

### 3. **Supuestos de Modelos Estadísticos**

   **Modelos de Distribución:**
   - Suponen **independencia de observaciones** (años separados).
   - Asumen **estacionariedad**: los parámetros poblacionales no cambian en el tiempo.
   - Pueden no ser robustos ante cambios climáticos de largo plazo.

   **Regresión Lineal:**
   - Supone **relación lineal** entre variables (puede no ser cierto).
   - Asume **normalidad de residuales**, **homocedasticidad** y **no multicolinealidad**.
   - Sensible a valores atípicos extremos.

   **Series de Tiempo:**
   - Métodos estadísticos suponen **patrón estable** en el tiempo.
   - La presencia de cambios estructurales (ej: nueva presa) invalida pronósticos.
   - Desempeño es mejor en horizontes cortos (< 12 meses).

### 4. **Alcance Académico**
   - Enfocada en **técnicas univariadas y bivariadas**.
   - No incluye modelos multivariados avanzados (PCA, clustering, etc.).
   - La interpretación agrológica final es responsabilidad del estudiante.

---

## Posibles Mejoras

1. **Integración de Datos Reales:**
   - Conexión a bases de datos públicas (IDEAM, SEDEMA).
   - Carga desde APIs de estaciones meteorológicas.

2. **Análisis Multivariado Avanzado:**
   - Análisis de Componentes Principales (PCA).
   - Análisis de Correspondencia.
   - Clustering de períodos similares.

3. **Modelos No Lineales:**
   - Regresión polinomial y splines.
   - Redes neuronales para pronósticos.
   - Modelos de machine learning (Random Forest, XGBoost).

4. **Análisis Espacial:**
   - Interpolación de datos entre municipios.
   - Mapas de precipitación estimada.
   - Análisis de variabilidad espacial.

5. **Interfaz Mejorada:**
   - Exportación de reportes en PDF.
   - Gráficas interactivas con Plotly.
   - Dashboard de comparación entre cultivos/municipios.

6. **Documentación Ampliada:**
   - Videos tutoriales de cada página.
   - Conjunto de problemas propuestos.
   - Sección de literatura científica recomendada.

---

## Hallazgos del EDA

### *Escrito por el estudiante, con cifras y unidades*

---

## Hallazgos de Distribuciones

### *Escrito por el estudiante, con cifras y unidades*

---

## Hallazgos de la Regresión

### *Escrito por el estudiante, con cifras y unidades*

---

## Hallazgos de Series de Tiempo

### *Escrito por el estudiante, con cifras y unidades*

---

## Referencias Bibliográficas

### Estadística Fundamental
- **Walpole, R. E., Myers, R. H., Myers, S. L., & Ye, K.** (2012). *Probability & Statistics for Engineers & Scientists* (9th ed.). Pearson.
- **Devore, J. L.** (2015). *Probability and Statistics for Engineering and the Sciences* (9th ed.). Cengage Learning.

### Hidrología e Ingeniería Agrícola
- **Monsalve Sáenz, G.** (1999). *Hidrología en la Ingeniería* (2ª ed.). Escuela Colombiana de Ingeniería.
- **Linsley, R. K., Kohler, M. A., & Paulhus, J. L. H.** (1975). *Hydrology for Engineers* (2nd ed.). McGraw-Hill.

### Análisis de Series de Tiempo
- **Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M.** (2015). *Time Series Analysis: Forecasting and Control* (5th ed.). Wiley.
- **Shumway, R. H., & Stoffer, D. S.** (2017). *Time Series Analysis and Its Applications* (4th ed.). Springer.

### Modelación Probabilística
- **Johnson, N. L., Kotz, S., & Balakrishnan, N.** (1994). *Continuous Univariate Distributions* (Vol. 1 & 2). Wiley.
- **Rao, C. R., & Toutenburg, H.** (1999). *Linear Models: Least Squares and Alternatives* (2nd ed.). Springer.

### Herramientas y Software
- **Streamlit Documentation.** https://docs.streamlit.io/
- **Pandas Documentation.** https://pandas.pydata.org/docs/
- **SciPy Documentation.** https://docs.scipy.org/
- **Statsmodels Documentation.** https://www.statsmodels.org/

---

## Cómo Contribuir

Este proyecto es desarrollado como trabajo académico. Para reportar errores o sugerir mejoras, contacta al autor o abre un issue en el repositorio.

---

## Licencia

Este proyecto está bajo licencia **MIT**. Ver el archivo `LICENSE` para más detalles.

---

**Generado:** 2026-11-06  
**Versión:** 1.0  
**Repositorio:** [justorfc/app-estadistica-aplicada-2026-2](https://github.com/justorfc/app-estadistica-aplicada-2026-2)
