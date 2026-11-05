# Página: pages/4_Regresion.py - Análisis de Regresión Lineal

## Estado

✅ **COMPLETADA Y VALIDADA** - Lissta para usar en la app Streamlit

## Descripción General

La página `pages/4_Regresion.py` implementa un análisis completo de **regresión lineal simple y múltiple** con 6 secciones interactivas, usando datos agrícolas reales (parcelas de 100 obs, muestra de 8 obs para verificación manual).

**Propósito educativo**: Conectar cálculos manuales (fórmulas de clase) con estadísticos automáticos (statsmodels), enseñar interpretación agrícola y demostrar predicción con intervalos de confianza.

## Secciones Implementadas

### 1. 🔗 Correlación (Matriz y Tabla)

- **Radio selector**: Elegir entre Pearson o Spearman
- **Heatmap**: Matriz de correlación con seaborn (colores: rojo = positivo, azul = negativo)
- **Tabla**: Cada variable con rendimiento, ordenada por |r| (correlación en valor absoluto)
- **Nota pedagógica**: "Correlación ≠ Causalidad"

**Datos usados**: `datos/parcelas.csv` (116 parcelas, 5 variables numéricas)

### 2. 📈 Regresión Lineal Simple

- **Selectbox**: Elegir variable X (por defecto: `lamina_riego`)
- **Gráfico dispersión + recta**: Con etiqueta de ecuación ajustada
- **Ecuación en LaTeX**: Rendimiento = b₀ + b₁·X con unidades (mm, kg/ha, %)
- **Métricas** (3 columnas):
  - r: Correlación de Pearson
  - R²: Coeficiente de determinación
  - RSE: Error estándar residual (ton/ha)
- **Tabla de coeficientes**: 
  - Variable, Coeficiente, Error Estándar, t, p-valor, IC95%
- **Decisión H₀** (β₁ = 0):
  - Verde (✅): Si p < 0.05 → Rechazo H₀, relación significativa
  - Naranja (❌): Si p ≥ 0.05 → No rechazar H₀, no hay relación
  - Incluye interpretación de b₁ (cambio en rendimiento por unidad de X)

**Datos usados**: `datos/parcelas.csv` (116 obs)

### 3. 🔍 Diagnóstico de Residuos

**4 gráficos en cuadrícula (2×2)**:
1. **Residuos vs Ajustados**: Línea en y=0, nube de puntos (debe ser aleatoria, no "embudo")
2. **Histograma**: Distribución de residuos (debe ser aproximadamente normal)
3. **Q-Q Plot**: Residuos vs Normal teórica (puntos deben seguir línea y=x)
4. **Escala-Ubicación**: √|Residuos Estandarizados| vs Ajustados

**Tests estadísticos**:
- **Shapiro-Wilk** (normalidad): 
  - H₀: Residuos distribuyen normalmente
  - p > 0.05 → ✅ No rechazar (residuos normales)
  - p ≤ 0.05 → ⚠️ Rechazar (residuos NO normales)
- **Breusch-Pagan** (homocedasticidad):
  - H₀: Varianza constante
  - p > 0.05 → ✅ No rechazar (varianza constante)
  - p ≤ 0.05 → ⚠️ Rechazar (varianza NO constante)

### 4. 🎯 Predicción

**a) Slider en rango observado**:
- Rango: [X_min, X_max] de los datos
- Muestra: Predicción puntual + IC95% (para E[Y|X]) + IP95% (para Y individual)

**b) Input libre**:
- `st.number_input`: Cualquier valor de X
- ⚠️ **Warning de extrapolación**: Si X fuera del rango → "EXTRAPOLACIÓN, predicciones poco confiables"

**Intervalos**:
- **IC95% (para E[Y|X])**: Intervalo de confianza para la media predicha
- **IP95% (para Y individual)**: Intervalo de predicción (más ancho que IC)

### 5. 🌾 Regresión Múltiple (Vista Previa)

**Modelo**: Rendimiento ~ dosis_N + lamina_riego + materia_organica + pH

**Tabla de coeficientes**:
- Variable, Coeficiente, Error Estándar, t, p-valor

**Métricas**:
- R² (determinación)
- R² Ajustado (penaliza parámetros extra)

**Nota pedagógica**: R² Ajustado ≤ R² porque castiga variables que no mejoran el ajuste significativamente (principio de parsimonia / navaja de Ockham).

### 6. ✏️ Verificación del Cálculo a Mano (8 Parcelas)

**a) Tabla de cálculos**:
- Parcela, Lámina (mm), Rendimiento, x-x̄, y-ȳ, Ŷ Ajustado, Residuo (e)

**b) Tabla de resultados de `calculo_manual()`** (16 filas):
- Estadístico, Valor
- Incluye: n, medias, Sxx, Syy, Sxy, r, b₁, b₀, R², RSE, SE(b₁), t, p-valor, IC95% de b₁
- Formato: 4 decimales (excepto b₁ en 6 decimales)

**c) Gráfico de regresión manual**:
- Dispersión (8 puntos) + recta ajustada
- Etiqueta: Ŷ = b₀ + b₁·X (con valores específicos)

**d) Tabla comparativa** (5 filas):
- Estadístico, Muestra (n=8), Datos Completos (n=116)
- Compara: b₁, r, R², t, p-valor
- Ilustra cómo muestra pequeña → mayor variabilidad

**Nota pedagógica**: Demuestra que n pequeño (8) es inestable; n grande (116) es más confiable.

## Archivos Utilizados

| Archivo | Función | Observaciones |
|---------|---------|---------------|
| `src/regresion.py` | Funciones de regresión | 6 funciones: matriz_correlacion, calculo_manual, ajustar_rls, predecir, diagnostico_residuos, ajustar_multiple |
| `datos/parcelas.csv` | Datos completos | 116 obs × 8 vars: parcela, suelo, riego, dosis_N, lamina_riego, materia_organica, ph, rendimiento |
| `datos/muestra_reg8.csv` | Verificación manual | 8 obs × 2 vars: parcela, lamina_riego, rendimiento |
| `datos/__init__.py` | Módulo de datos | Incluye `tarjeta_estudiante()` |

## Flujo de Interacción

```
Usuario abre la página → 
  1. Selecciona Pearson/Spearman → Ve matriz heatmap + tabla
  2. Selecciona variable X → Ve gráfico regresión + ecuación + test H₀
  3. Visualiza diagnóstico residuos automáticamente
  4. Mueve slider/ingresa input → Ve predicción con IC e IP
  5. Ve resumen de regresión múltiple
  6. Revisa cálculos manuales de 8 parcelas vs 116 completas
```

## Validación Completada

### ✅ Prueba 1: Sintaxis y Imports
- Código Python correcto
- Todos los módulos importan sin errores
- Dependencias disponibles

### ✅ Prueba 2: Funcionalidad de Datos
- `datos/parcelas.csv`: 116 filas cargadas correctamente
- `datos/muestra_reg8.csv`: 8 filas cargadas correctamente
- Variables numéricas identificadas

### ✅ Prueba 3: Cálculos Estadísticos
- matriz_correlacion: Matriz 5×5 de Pearson
- calculo_manual: b₀, b₁, R², RSE, t, p-valor calculados correctamente
- ajustar_rls: Modelo OLS ajustado
- predecir: IC e IP calculados
- diagnostico_residuos: Shapiro-Wilk y Breusch-Pagan ejecutados
- ajustar_multiple: Regresión de 4 predictores exitosa

### ✅ Prueba 4: Visualizaciones
- Heatmap de correlación (colores)
- Gráfico dispersión + recta (rojo, 2 ejes)
- 4 gráficos diagnóstico (residuos, histograma, Q-Q, escala-ubicación)
- Ecuación en LaTeX

### ✅ Prueba 5: Comparabilidad
- Cálculo manual de 8 parcelas vs datos completos (116)
- Muestra pequeña es más variable (esperado)
- Datos completos son más estables

## Características Pedagógicas

### Para el Estudiante
- 📚 **Fórmulas paso a paso**: Sxx, Syy, Sxy, b₁, b₀, R², RSE, t, IC
- 🎓 **Contexto agrícola**: Unidades (mm riego, ton/ha rendimiento, kg/ha dosis)
- 🔍 **Verificación manual**: Compara 8 parcelas vs 116 para ver estabilidad
- ⚠️ **Extrapolación**: Advertencia cuando se predice fuera del rango
- 📊 **Diagnóstico**: Gráficos + tests estadísticos de supuestos

### Para el Instructor
- 📋 Tabla de desviaciones para corregir cálculos manuales
- 📈 Regresión múltiple para comparar modelos
- 🧪 Pruebas de normalidad y homocedasticidad
- 💾 Datos reales (no sintéticos)

## Errores Anticipados y Soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| Valores NaN en gráficos | Datos faltantes en X o Y | Se elimina automáticamente con `.dropna()` |
| IC e IP muy anchos | Muestra pequeña o gran RSE | Esperado; mostramos en las tablas |
| R² muy pequeño | Relación débil | Normal en datos reales; interpretamos p-valor |
| Residuos NO normales | Datos sesgados | Shapiro-Wilk lo detecta; se nota en Q-Q |

## Próximos Pasos (Opcionales Futuros)

1. **Distancia de Cook**: Detectar observaciones influyentes
2. **Transformaciones**: Log, raíz cuadrada si residuos NO normales
3. **Polinomios**: Y ~ X + X² si relación es curvilínea
4. **Modelos anidados**: Comparar RLS vs RLM con test F
5. **Tabla ANOVA**: Descomponer SCT = SCR + SCE

## Cómo Ejecutar

```bash
# Desde la carpeta del proyecto
cd /workspaces/app-estadistica-aplicada-2026-2

# Ejecutar la app
.venv/bin/streamlit run app.py

# En el navegador:
# 1. Aparecerá menú lateral con páginas
# 2. Seleccionar "4 - Regresión"
# 3. Interactuar con selectores, sliders e inputs
```

## Especificaciones Técnicas

- **Framework**: Streamlit 1.x
- **Backend estadístico**: statsmodels (OLS), scipy.stats (tests)
- **Visualización**: Matplotlib + Seaborn
- **Almacenamiento**: @st.cache_data para cargar datos una sola vez
- **Performance**: <2 seg de carga (con caché)

## Referencias Bibliográficas

- Kutner, M. H., Nachtsheim, C. J., Neter, J. (2004). *Applied Linear Regression Models* (4th ed.). McGraw-Hill.
- Montgomery, D. C., Peck, E. A., Vining, G. G. (2012). *Introduction to Linear Regression Analysis* (5th ed.). Wiley.
- Mendenhall, W., Sincich, T. (2016). *A Second Course in Statistics: Regression Analysis* (7th ed.). Pearson.

---

**Alumno**: Justo Fuentes (6820995)  
**Fecha**: 2026-11-05  
**Versión**: 1.0 (Inicial)  
**Estado**: ✅ Completada
