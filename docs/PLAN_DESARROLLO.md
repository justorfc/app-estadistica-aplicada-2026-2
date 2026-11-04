# Plan de Desarrollo: App de Estadística Aplicada

**Objetivo:** Construir una aplicación web multipágina en Streamlit para análisis estadístico aplicado a Ingeniería Agrícola, con énfasis en precipitación máxima anual y series de tiempo.

---

## 1. Descripción General de Cada Página

### 1.1 Página: **Inicio**

**Propósito:** Bienvenida, navegación y contexto de la aplicación.

**Entradas:**
- Sin entradas (página informativa)

**Contenido a mostrar:**
- Título y descripción de la app
- Objetivo del análisis estadístico
- Instrucciones básicas de navegación
- Créditos y referencias bibliográficas
- Pequeño resumen del flujo de trabajo

**Cálculos:** Ninguno

---

### 1.2 Página: **Datos**

**Propósito:** Carga, validación e inspección inicial de datos.

**Entradas:**
- Archivo CSV o Excel cargado por el usuario
- Selección de columna para analizar (precipitación, variable agrícola, etc.)
- Filtros opcionales (rango de fechas, valores atípicos)

**Contenido a mostrar:**

| Elemento | Descripción |
|----------|-------------|
| **Tabla resumen** | Primeras y últimas filas del dataset |
| **Estadísticas descriptivas** | n, media, desv. est., mín, máx, cuartiles, asimetría, curtosis |
| **Gráfica: Series temporal** | Línea del tiempo de los datos cargados |
| **Gráfica: Histograma** | Distribución de frecuencias |
| **Tabla de validación** | Datos faltantes, duplicados, fuera de rango |
| **Botón de descarga** | CSV limpio para análisis posterior |

**Cálculos estadísticos:**
- Estadísticas descriptivas (media, mediana, moda, desv. est., CV, asimetría, curtosis)
- Detección de valores faltantes y atípicos
- Validación de integridad de datos

---

### 1.3 Página: **EDA (Análisis Exploratorio de Datos)**

**Propósito:** Exploración visual y numérica de patrones en los datos.

**Entradas:**
- Dataset cargado desde la página "Datos"
- Selección de variable(s) a analizar
- Selección de tipo de análisis (univariado/bivariado)

**Contenido a mostrar:**

| Elemento | Descripción |
|----------|-------------|
| **Tabla correlaciones** | Matriz de correlación (si hay múltiples variables) |
| **Gráfica: Boxplot** | Detección visual de atípicos y simetría |
| **Gráfica: Violín** | Distribución detallada y densidad |
| **Gráfica: Scatter plot** | Relación entre dos variables (si aplica) |
| **Gráfica: Q-Q plot** | Comparación con normalidad teórica |
| **Tabla de tendencias** | Media móvil, máximos y mínimos por período |
| **Análisis de outliers** | Método IQR y Z-score |

**Cálculos estadísticos:**
- Correlación de Pearson y Spearman (preliminar)
- Cuartiles, rango intercuartílico
- Índices de asimetría y curtosis
- Detección de valores atípicos (IQR, Z-score, modificado Z-score)

---

### 1.4 Página: **Distribuciones**

**Propósito:** Ajuste y comparación de modelos de distribución probabilística para precipitación máxima anual.

**Entradas:**
- Variable de precipitación máxima anual
- Selección de modelos: Normal, Lognormal, Gamma, Weibull, Gumbel, GEV
- Selección de criterios de bondad de ajuste
- Período de retorno T (años) para pronósticos

**Contenido a mostrar:**

| Elemento | Descripción |
|----------|-------------|
| **Tabla: Parámetros estimados** | μ, σ, α, β, k, etc. según cada modelo |
| **Tabla: Pruebas KS y Anderson-Darling** | Estadístico, p-valor, decisión (α=0.05) |
| **Tabla: Criterios de información** | AIC, BIC, AICc para cada modelo |
| **Gráfica: Ajuste visual** | Histograma + curva teórica de cada modelo |
| **Gráfica: P-P plot** | Probabilidad empírica vs teórica |
| **Gráfica: Ranking de modelos** | Comparación visual AICc |
| **Tabla: Período de retorno** | Cuantiles para T=2, 5, 10, 25, 50, 100 años |
| **Tabla: Riesgo e incertidumbre** | P(X > x_T) y IC 95% para cada modelo |
| **Gráfica: Función de supervivencia** | 1 - F(x) con IC |

**Cálculos estadísticos:**

**Estimación de parámetros:**
- Máxima verosimilitud (MLE) para cada distribución
- Método de momentos (opcional)

**Pruebas de bondad de ajuste:**
- Prueba de Kolmogórov-Smirnov (KS): D = max|F_n(x) - F(x)|
- Prueba de Anderson-Darling: A² = -n - Σ[(2i-1)/n · ln(F(x_i)) + ln(1-F(x_n+1-i))]
- Criterios de información:
  - AIC = 2k - 2ln(L)
  - BIC = k·ln(n) - 2ln(L)
  - AICc = AIC + 2k(k+1)/(n-k-1)

**Cuantiles y período de retorno:**
- x_T = F⁻¹(1 - 1/T)
- Intervalo de confianza: Bootstrap o delta method

**Riesgo e incertidumbre:**
- Riesgo en T años: R = 1 - (1 - 1/T)^T
- Propagación de incertidumbre en parámetros

---

### 1.5 Página: **Regresión**

**Propósito:** Análisis de relaciones lineales y diagnóstico de residuos.

**Entradas:**
- Variable independiente (X) y dependiente (Y)
- Selección de método de correlación
- Opciones de diagnóstico

**Contenido a mostrar:**

| Elemento | Descripción |
|----------|-------------|
| **Tabla: Correlaciones** | Pearson (r, IC 95%, p-valor) y Spearman (ρ, p-valor) |
| **Tabla: Modelo de regresión** | Intercepto, pendiente, IC 95%, errores estándar, t-stat, p-valor |
| **Tabla: Bondad de ajuste** | R², R² ajustado, F-stat, p-valor |
| **Gráfica: Scatter + recta ajustada** | Datos + línea de regresión con IC 95% de la media |
| **Gráfica: Residuos vs predichos** | Evaluación de homocedasticidad |
| **Gráfica: Q-Q plot residuos** | Normalidad de residuos |
| **Gráfica: Escala-ubicación** | Raíz de residuos estandarizados vs predichos |
| **Gráfica: Distancia de Cook** | Identificación de puntos influyentes |
| **Tabla: Inferencia sobre la pendiente** | H₀: β = 0, intervalo de confianza |
| **Tabla: Predicciones** | Y_pred para nuevos valores de X con IC 95% |

**Cálculos estadísticos:**

**Correlación:**
- Pearson: r = Σ[(x_i - x̄)(y_i - ȳ)] / √[Σ(x_i - x̄)² · Σ(y_i - ȳ)²]
- Spearman: ρ basado en rangos

**Regresión lineal simple:**
- β₁ = Σ[(x_i - x̄)(y_i - ȳ)] / Σ(x_i - x̄)²
- β₀ = ȳ - β₁·x̄
- Varianza residual: σ² = Σ(e_i²) / (n - 2)

**Bondad de ajuste:**
- SCT = Σ(y_i - ȳ)²
- SCR = Σ(ŷ_i - ȳ)²
- SCE = Σ(e_i²)
- R² = SCR / SCT
- F = (SCR/1) / (SCE/(n-2))

**Diagnóstico de residuos:**
- Test de Shapiro-Wilk (normalidad)
- Test de Breusch-Pagan (homocedasticidad)
- Distancia de Cook: D_i = e_i² / (2·σ²·h_ii) · [h_ii/(1-h_ii)]
- Verificación de autocorrelación (Durbin-Watson)

---

### 1.6 Página: **Series de Tiempo**

**Propósito:** Análisis completo de series temporales: descomposición, pronóstico y validación.

**Entradas:**
- Serie de tiempo con fecha y valor
- Selección de periodicidad (anual, mensual, semanal)
- Selección de método de pronóstico (MA, Exponencial, ARIMA, AutoTS)
- Horizonte de pronóstico (h períodos)
- División de validación (e.g., últimas 10 observaciones)

**Contenido a mostrar:**

| Elemento | Descripción |
|----------|-------------|
| **Gráfica: Serie original** | Temporal plot con tendencia visual |
| **Tabla: Componentes** | Tendencia (T), ciclo/estacionalidad (S), irregular (I) |
| **Gráfica: Descomposición clásica** | 4 subgráficas: original, T, S, I |
| **Tabla: Índices estacionales** | Factores mensuales/trimestrales/anuales |
| **Gráfica: Promedios móviles** | MA(3), MA(6), MA(12) según periodicidad |
| **Tabla: Métodos de referencia** | Último valor, promedio histórico, estacional naive |
| **Tabla: Validación con MAE, RMSE, SMAPE** | Comparación de modelos en conjunto test |
| **Gráfica: Pronóstico AutoTS** | Predicciones futuras con IC 80% y 95% |
| **Tabla: Pronóstico puntual** | Valores predichos y errores estándar |
| **Gráfica: ACF y PACF** | Correlogramas para identificar estructura |

**Cálculos estadísticos:**

**Descomposición clásica aditiva:**
- X_t = T_t + S_t + I_t
- Tendencia: media móvil centrada
- Estacionalidad: promedio desestacionalizado
- Irregular: residuo

**Descomposición multiplicativa:**
- X_t = T_t · S_t · I_t
- Aplicable cuando varianza aumenta con nivel

**Índices estacionales:**
- S_j = (1/n_j) · Σ(X_t / T_t) para cada estación j
- Normalización: Σ S_j = L (longitud período)

**Promedios móviles simples:**
- MA(k) = (X_t + X_{t-1} + ... + X_{t-k+1}) / k

**Métodos de referencia:**
- Naive: Ŷ_{t+h} = Y_t
- Seasonal naive: Ŷ_{t+h} = Y_{t-s+h} donde s = estación
- Promedio histórico: Ŷ_{t+h} = (1/n) · Σ Y_i

**Métricas de validación:**
- MAE = (1/n) · Σ|e_t|
- RMSE = √[(1/n) · Σ(e_t²)]
- SMAPE = (100/n) · Σ[|e_t| / (|Y_t| + |Ŷ_t|) / 2]

**AutoTS:**
- Busca automáticamente mejor ARIMA/ETS
- Genera IC mediante simulaciones o bootstrap

---

### Comparación de Modelos de Secado en Capa Delgada (Bonus)

**Entradas:** Datos de humedad vs tiempo
**Modelos a comparar:** Lewis, Page, Modified Page, Henderson, Overhulse, Wang Singh, etc.
**Criterio:** AICc
**Salida:** Tabla comparativa y gráfica ajuste + residuos

---

## 2. Organización Modular del Proyecto

```
app-estadistica-aplicada-2026-2/
├── app.py                      # Punto de entrada de Streamlit
├── README.md                   # Documentación general
├── .gitignore                  # Gitignore
├── requirements.txt            # Dependencias Python
│
├── docs/
│   ├── PLAN_DESARROLLO.md      # Este archivo
│   ├── GUIA_USO.md            # Manual para usuarios
│   └── NOTAS_TECNICAS.md      # Detalles estadísticos
│
├── src/                        # Código reutilizable (lógica estadística)
│   ├── __init__.py
│   ├── datos.py               # Carga y validación de datos
│   ├── eda.py                 # EDA (correlaciones, outliers, etc.)
│   ├── distribuciones.py      # Ajuste de distribuciones, KS, AD, cuantiles
│   ├── regresion.py           # Correlación y regresión lineal
│   ├── series_tiempo.py       # Descomposición, pronóstico, AutoTS
│   └── utilidades.py          # Funciones comunes (gráficas, formatos)
│
├── pages/                      # Páginas de Streamlit (app multipágina)
│   ├── 1_Inicio.py
│   ├── 2_Datos.py
│   ├── 3_EDA.py
│   ├── 4_Distribuciones.py
│   ├── 5_Regresion.py
│   └── 6_Series_Tiempo.py
│
├── datos/                      # Datasets de ejemplo
│   ├── ejemplo_precipitacion.csv
│   ├── ejemplo_agricultura.csv
│   └── README_datos.md
│
└── verificacion/              # Tests y validación
    ├── test_datos.py
    ├── test_distribuciones.py
    ├── test_regresion.py
    └── test_series_tiempo.py
```

### Descripción de módulos:

| Módulo | Responsabilidad | Funciones principales |
|--------|------------------|----------------------|
| **src/datos.py** | Carga, limpieza, validación | `cargar_datos()`, `validar_datos()`, `estadisticas_descriptivas()`, `detectar_outliers()` |
| **src/eda.py** | Análisis exploratorio | `correlacion_pearson()`, `correlacion_spearman()`, `boxplot_data()`, `qq_plot()` |
| **src/distribuciones.py** | Ajuste de distribuciones | `ajustar_distribuciones()`, `prueba_ks()`, `prueba_anderson_darling()`, `aic_bic_aicc()`, `cuantiles_retorno()` |
| **src/regresion.py** | Análisis de regresión | `regresion_lineal()`, `diagnostico_residuos()`, `distancia_cook()` |
| **src/series_tiempo.py** | Series temporales | `descomponer_serie()`, `indices_estacionales()`, `promedios_moviles()`, `auto_forecast()` |
| **src/utilidades.py** | Funciones auxiliares | `crear_tabla_bonita()`, `guardar_csv()`, `colorear_resultados()` |

---

## 3. Orden de Construcción Recomendado

### Fase 1: Infraestructura Base (Semana 1)
1. ✅ Crear estructura de carpetas
2. ✅ Crear `app.py` con navegación multipágina
3. ✅ Crear página "Inicio"
4. ✅ Crear `requirements.txt` y configurar dependencias
5. ✅ Crear archivo `src/utilidades.py` con funciones base

**Por qué:** Establece el marco de trabajo. Las demás páginas dependen de esto.

---

### Fase 2: Gestión de Datos (Semana 2)
6. ✅ Crear `src/datos.py` con funciones de carga y validación
7. ✅ Crear página "Datos" con carga interactiva
8. ✅ Probar con datos de ejemplo
9. ✅ Crear archivos de datos en `datos/`

**Por qué:** Todo análisis necesita datos limpios. Es requisito para las siguientes fases.

---

### Fase 3: Análisis Exploratorio (Semana 3)
10. ✅ Crear `src/eda.py` con funciones de exploración
11. ✅ Crear página "EDA" con visualizaciones
12. ✅ Integrar con datos cargados

**Por qué:** Proporciona comprensión inicial de datos. Base para decisiones posteriores.

---

### Fase 4: Distribuciones Probabilísticas (Semana 4)
13. ✅ Crear `src/distribuciones.py` con:
    - Estimación MLE para 6 distribuciones
    - Pruebas KS y Anderson-Darling
    - Cálculo de AIC, BIC, AICc
    - Cuantiles y período de retorno
14. ✅ Crear página "Distribuciones" (es la más compleja)
15. ✅ Validar con datos simulados

**Por qué:** Núcleo del análisis para precipitación. Requiere `datos.py` estable.

---

### Fase 5: Regresión (Semana 5)
16. ✅ Crear `src/regresion.py` con:
    - Correlaciones (Pearson, Spearman)
    - Regresión lineal simple
    - Diagnóstico de residuos
17. ✅ Crear página "Regresión"
18. ✅ Validar diagnósticos

**Por qué:** Análisis fundamental de relaciones lineales. Independiente de distribuciones.

---

### Fase 6: Series de Tiempo (Semana 6)
19. ✅ Crear `src/series_tiempo.py` con:
    - Descomposición clásica
    - Índices estacionales
    - Promedios móviles
    - AutoTS o similar
20. ✅ Crear página "Series de Tiempo"
21. ✅ Validar pronósticos

**Por qué:** Análisis más complejo. Beneficia de experiencia con otras páginas.

---

### Fase 7: Refinamiento y Testing (Semana 7)
22. ✅ Crear tests en `verificacion/`
23. ✅ Validación de todos los cálculos vs R/Excel
24. ✅ Optimización de visualizaciones
25. ✅ Documentación final

**Por qué:** Asegura confiabilidad. Se hace al final cuando todas las funciones están estables.

---

## 4. Justificación del Orden

| Razón | Beneficio |
|-------|-----------|
| **Construcción bottom-up (datos → análisis)** | Cada fase está lista cuando la siguiente la necesita |
| **EDA antes de distribuciones** | Comprensión de patrones guía la selección de modelos |
| **Regresión en paralelo con distribuciones** | Son independientes; pueden avanzar simultáneamente |
| **Series de tiempo al final** | Usa técnicas de las fases anteriores (MA, análisis de residuos) |
| **Testing después del desarrollo** | Evita refactorización prematura |

---

## 5. Stack Tecnológico Recomendado

| Herramienta | Versión | Propósito |
|------------|---------|----------|
| **Python** | 3.9+ | Lenguaje base |
| **Streamlit** | 1.28+ | Framework web |
| **pandas** | 2.0+ | Manipulación de datos |
| **numpy** | 1.24+ | Cálculos numéricos |
| **scipy** | 1.11+ | Distribuciones, pruebas estadísticas |
| **matplotlib** | 3.7+ | Gráficas básicas |
| **plotly** | 5.15+ | Gráficas interactivas |
| **seaborn** | 0.13+ | Gráficas estadísticas |
| **statsmodels** | 0.14+ | Series de tiempo, regresión, diagnósticos |
| **scikit-learn** | 1.3+ | Validación cruzada, métricas |
| **pyrts** o **AutoTS** | Latest | Pronóstico automático |

---

## 6. Resumen de Funciones Clave por Módulo

### `src/datos.py`
- `cargar_datos(archivo)` → DataFrame
- `validar_datos(df)` → dict con report de calidad
- `estadisticas_descriptivas(serie)` → dict con stats
- `detectar_outliers(serie, metodo='iqr')` → array de índices
- `limpiar_datos(df, eliminar_nulos=True)` → DataFrame limpio

### `src/eda.py`
- `correlacion_completa(df)` → dict con Pearson, Spearman, p-valores
- `matriz_correlacion(df)` → DataFrame correlación
- `generar_graficas_eda(df, columna)` → dict con figuras

### `src/distribuciones.py`
- `ajustar_distribuciones(datos)` → dict con parámetros MLE
- `prueba_ks(datos, dist, params)` → (estadístico, p_valor)
- `prueba_anderson_darling(datos, dist)` → (estadístico, p_valor)
- `calcular_aic_bic_aicc(datos, dist, params)` → dict con criterios
- `cuantiles_retorno(dist, params, periodos=[2,5,10,25,50,100])` → DataFrame
- `riesgo_incertidumbre(dist, params, periodo, n_bootstrap=1000)` → dict con riesgo e IC

### `src/regresion.py`
- `regresion_simple(x, y)` → dict con coeficientes, R², p-valores
- `diagnostico_residuos(x, y, modelo)` → dict con tests (Shapiro, Breusch-Pagan)
- `distancia_cook(x, y)` → array de distancias

### `src/series_tiempo.py`
- `descomponer_serie(y, periodo, modelo='aditivo')` → dict con T, S, I
- `indices_estacionales(y, periodo)` → array de factores
- `promedios_moviles(y, ventanas=[3,6,12])` → dict con series suavizadas
- `auto_forecast(y, h=12, metodo='auto')` → dict con predicciones e IC
- `metricas_validacion(y_true, y_pred)` → dict con MAE, RMSE, SMAPE

### `src/utilidades.py`
- `crear_tabla_bonita(df, decimales=2)` → Streamlit.dataframe formateado
- `guardar_descarga_csv(df, nombre)` → widget de descarga
- `crear_figura_subplots(datos_lista, titulos)` → matplotlib.figure
- `formato_numerico(valor, decimales=2)` → string formateado

---

## 7. Notas Importantes

### Sobre la modularidad:
- Cada función de `src/` debe ser **pura** (sin estado)
- Retornar estructuras (dict, DataFrame) que las páginas consumen
- Las páginas (`pages/`) usan Streamlit para UI, no lógica estadística

### Sobre los tests:
- Validar contra resultados conocidos (R, Excel)
- Usar datos simulados con distribuciones conocidas
- Cubrir casos extremos (n=2, valores atípicos, etc.)

### Sobre la documentación:
- Comentar funciones complejas de estadística
- Incluir fórmulas en docstrings
- Ejemplos de uso en cada módulo

### Sobre versiones de paquetes:
- Especificar versiones mínimas en `requirements.txt`
- Probar compatibilidad con nuevas versiones antes de actualizar

---

## 8. Tabla Resumen: Páginas y Funciones

| Página | Entrada | Salida Principal | Módulo | Complejidad |
|--------|---------|------------------|--------|------------|
| Inicio | - | Info + navegación | - | Baja |
| Datos | CSV/Excel | Stats + gráficas | datos.py | Baja-Media |
| EDA | DataFrame | Correlaciones + boxplots | eda.py | Media |
| Distribuciones | Series | Ajustes + cuantiles + riesgo | distribuciones.py | **Alta** |
| Regresión | X, Y | Modelo + diagnósticos | regresion.py | Media |
| Series Tiempo | Serie + h | Descomposición + pronóstico | series_tiempo.py | Media-Alta |

---

## 9. Timeline Estimado

| Fase | Duración | Dependencias | Entregable |
|------|----------|--------------|-----------|
| 1: Infraestructura | 3-5 días | Ninguna | app.py + páginas vacías |
| 2: Datos | 3-5 días | Fase 1 | Carga de CSV + validación |
| 3: EDA | 4-6 días | Fase 2 | Gráficas exploratorias |
| 4: Distribuciones | 7-10 días | Fase 3 | Ajuste + KS/AD + cuantiles |
| 5: Regresión | 4-6 días | Fase 2 | Modelo + diagnósticos |
| 6: Series Tiempo | 6-8 días | Fase 3 | Descomposición + pronóstico |
| 7: Testing + Docs | 5-7 días | Fases 1-6 | Tests + documentación |
| **Total** | **32-47 días** | - | App completamente funcional |

---

**Próximo paso:** Comienza con Fase 1. Crea `app.py` con estructura multipágina y la página "Inicio".
