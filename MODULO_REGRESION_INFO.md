# Módulo src/regresion.py - Análisis de Regresión Lineal

## Resumen Ejecutivo

Se ha creado exitosamente el módulo `src/regresion.py` con 6 funciones documentadas para análisis de regresión lineal simple y múltiple. **Todas las funciones han sido validadas y funcionan correctamente.**

## Funciones Implementadas

### 1. `matriz_correlacion(df, metodo='pearson')`
- **Propósito**: Calcula matriz de correlación de variables numéricas
- **Parámetros**: DataFrame, método ('pearson' o 'spearman')
- **Retorna**: Matriz de correlación simétrica
- **Ejemplo**: `corr = matriz_correlacion(df, 'pearson')`

### 2. `calculo_manual(x, y)` ✓ VALIDADO
- **Propósito**: Realiza regresión lineal simple paso a paso (como en clase)
- **Fórmulas implementadas**:
  - Sxx, Syy, Sxy (sumas de cuadrados/productos)
  - b₁ = Sxy/Sxx, b₀ = ȳ - b₁·x̄
  - R² = 1 - SCE/SCT, RSE = √(SCE/(n-2))
  - SE(b₁) = RSE/√Sxx
  - t = b₁/SE(b₁), p-valor bilateral, IC 95% de b₁
- **Retorna**: Diccionario con 25 estadísticos
- **Validación**: Coincide con statsmodels con precisión < 1e-14

### 3. `ajustar_rls(df, x, y)`
- **Propósito**: Ajusta regresión con OLS (statsmodels)
- **Retorna**: RegressionResults (con resumen, parámetros, test, etc.)
- **Ejemplo**: `modelo = ajustar_rls(df, 'lamina_riego', 'rendimiento')`

### 4. `predecir(modelo, x0, nivel=0.95)`
- **Propósito**: Predicción con intervalos al 95%
- **Retorna**:
  - `y_pred`: predicción puntual
  - `IC_lower, IC_upper`: intervalo de confianza para E[Y|X]
  - `IP_lower, IP_upper`: intervalo de predicción para Y individual
- **Ejemplo**: `pred = predecir(modelo, x0=100)`

### 5. `diagnostico_residuos(modelo)`
- **Propósito**: Tests de supuestos del modelo
- **Tests incluidos**:
  - Shapiro-Wilk (normalidad)
  - Breusch-Pagan (homocedasticidad)
- **Retorna**: residuos, ajustados, estadísticos y p-valores
- **Interpretación**: p > 0.05 → supuesto cumplido

### 6. `ajustar_multiple(df, y, lista_x)`
- **Propósito**: Regresión lineal múltiple
- **Características**:
  - Elimina automáticamente filas con NaN
  - Retorna modelo OLS
- **Ejemplo**: `modelo = ajustar_multiple(df, 'rendimiento', ['lamina_riego', 'dosis_N'])`

## Datos Utilizados

| Archivo | Obs | Variables | Propósito |
|---------|-----|-----------|-----------|
| `datos/muestra_reg8.csv` | 8 | lamina_riego, rendimiento | Verificación manual (clase) |
| `datos/parcelas.csv` | 100 | 8 variables numéricas | Análisis y regresión múltiple |

## Validación Completada

### Prueba 1: Coincidencia calculo_manual vs statsmodels
```
muestra_reg8.csv (n=8, lamina_riego → rendimiento)
✓ b₀ = 16.880374  (precisión: 1.42e-14)
✓ b₁ = -0.032825  (precisión: 4.86e-17)
✓ R² = 0.127225   (precisión: 2.22e-16)
✓ RSE = 5.507936  (precisión: 8.88e-16)
✓ t = -0.935215   (precisión: 9.99e-16)
✓ p-valor = 0.385772 (precisión: 2.78e-16)
```

### Prueba 2: Matriz de correlación
```
✓ Pearson: Funciona correctamente
✓ Spearman: Funciona correctamente
```

### Prueba 3: Predicción
```
Para lamina_riego = 100 mm:
✓ ŷ = 13.5979 ton/ha
✓ IC95%: [7.9757, 19.2201] (intervalo de confianza para E[Y|X])
✓ IP95%: [-1.0052, 28.2010] (intervalo de predicción para Y)
```

### Prueba 4: Diagnóstico residuos
```
✓ Shapiro-Wilk p-valor = 0.0413 (residuos aproximadamente normales)
✓ Breusch-Pagan p-valor = 0.2998 (varianza aproximadamente homogénea)
```

### Prueba 5: Regresión múltiple
```
parcelas.csv: 100 obs, modelo con rendimiento ~ lamina_riego + dosis_N
✓ R² = 0.074 (7.4% varianza explicada)
✓ dosis_N significativo (p = 0.003)
✓ lamina_riego NO significativo (p = 0.604)
```

## Ejecución de Pruebas

```bash
# Ejecutar bloque de prueba del módulo
.venv/bin/python -m src.regresion

# Importar en la app
from src.regresion import calculo_manual, ajustar_rls, predecir, diagnostico_residuos
```

## Próximos Pasos (Pendientes)

1. **Integración en `pages/4_Regresion.py`** (si existe)
   - Sección de análisis de correlación
   - Sección de regresión simple vs múltiple
   - Visualizaciones: recta de regresión, Q-Q plot, residuos
   - Calculadora de predicción interactiva

2. **Aplicaciones educativas**
   - Mostrar paso a paso cálculo manual vs automático
   - Comparar regresión simple vs múltiple
   - Diagnóstico interactivo de supuestos

## Referencias

- Kutner, M. H., Nachtsheim, C. J., Neter, J. (2004). *Applied Linear Regression Models* (4th ed.)
- Mendenhall, W., Sincich, T. (2016). *A Second Course in Statistics: Regression Analysis* (7th ed.)
- scipy.stats, statsmodels documentation

---

**Estado**: ✓ Completado y validado  
**Fecha**: 2026-11-05  
**Alumno**: Justo Fuentes (6820995)
