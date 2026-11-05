# Verificación de Cálculos - Manual y Automatizado

Esta carpeta contiene scripts independientes de la app que permiten verificar los cálculos estadísticos a mano usando fórmulas explícitas (sin funciones de librerías estadísticas).

## 📁 Contenido

### Scripts Python
Ejecutables con: `.venv/bin/python nombre_script.py`

1. **`verificar_eda.py`** (≈650 líneas)
   - Análisis exploratorio con muestra_eda10.csv
   - Calcula: media, mediana, varianza, desv. estándar, CV, Q1, Q3, RIC, vallas de Tukey, atípicos, media por grupo
   - Todas las fórmulas explícitas, paso a paso
   - Salida formateada con 4 decimales

2. **`verificar_distribuciones.py`** (≈270 líneas)
   - Análisis de distribuciones con muestra_dist10.csv
   - Calcula: posición de Weibull, período de retorno empírico, parámetros Gumbel por momentos, x_T para T=10/50/100, riesgo
   - Todas las fórmulas con explicaciones
   - Salida formateada con 4 decimales

3. **`verificar_regresion.py`** (≈430 líneas)
   - Regresión lineal simple con muestra_reg8.csv
   - Calcula: Sxx, Syy, Sxy, r (Pearson), ρ (Spearman), b0, b1, SCE, R², RSE, SE(b1), t, p-value, IC 95%
   - Todas las fórmulas explícitas sin funciones de regresión del paquete
   - Salida formateada con 4 decimales

4. **`verificar_series.py`** (≈400 líneas)
   - Series de tiempo con muestra_series24.csv
   - Calcula: PM3, índices estacionales, 3 métodos de pronóstico (ingenuo, est. ingenuo, promedio), MAE, RMSE, SMAPE
   - Todas las fórmulas paso a paso
   - Salida formateada con 4 decimales

### Scripts R
Para ejecutar en Posit Cloud (posit.cloud)

1. **`verificar_eda.R`**
   - Funciones base de R (no requiere instalación extra)
   - Cálculos equivalentes al script Python

2. **`verificar_distribuciones.R`**
   - Require: `fitdistrplus` y `evd` (instalar en Posit Cloud)
   - Incluye instrucciones de instalación
   - Cálculos MLE además del método de momentos

3. **`verificar_regresion.R`**
   - Funciones base de R con `lm()` y `summary()`
   - Verificación usando estadísticas base de R

4. **`verificar_series.R`**
   - Funciones base de R
   - Análisis de series de tiempo

### Plantilla de Resultados

5. **`RESULTADOS.md`**
   - Plantilla con 4 tablas (una por tema)
   - Columnas: Medida | A mano | Python | R | App | ¿Coincide?
   - Secciones de reflexión y análisis de diferencias
   - Espacios para documentar conclusiones

## 🚀 Uso

### Para estudiantes

1. **Ejecutar scripts Python:**
   ```bash
   cd /workspaces/app-estadistica-aplicada-2026-2
   .venv/bin/python verificacion/verificar_eda.py
   .venv/bin/python verificacion/verificar_distribuciones.py
   .venv/bin/python verificacion/verificar_regresion.py
   .venv/bin/python verificacion/verificar_series.py
   ```

2. **Ejecutar scripts R en Posit Cloud:**
   - Ve a posit.cloud
   - Abre una nueva consola R
   - Copia y pega el contenido de cada archivo .R
   - Ejecuta línea por línea para ver los resultados paso a paso

3. **Llenar plantilla RESULTADOS.md:**
   - Copia los resultados de Python y R en sus respectivas columnas
   - Compara con los valores en la app
   - Completa las observaciones

## 📊 Resultados Esperados (4 decimales)

### EDA (muestra_eda10.csv)
```
Media                          : 8.9245
Mediana                        : 8.9465
Varianza (S²)                  : 2.8793
Desviación estándar (S)        : 1.6969
CV (%)                         : 19.0135%
Q1                             : 7.5636
Q3                             : 10.4336
RIC                            : 2.8700
Valla inferior                 : 3.2585
Valla superior                 : 14.7386
Atípicos                       : 0
Media riego=Sí                 : 9.7438
Media riego=No                 : 8.5733
```

### Distribuciones (muestra_dist10.csv)
```
μ Gumbel                       : 72.9269
β Gumbel                       : 11.8905
x₁₀                            : 99.6849 mm
x₅₀                            : 119.3229 mm
x₁₀₀                           : 127.6250 mm
Riesgo (T=50, N=25)            : 0.3965 (39.65%)
```

### Regresión (muestra_reg8.csv)
```
Sxx                            : 24626.0518
Syy                            : 208.5580
Sxy                            : -808.3467
r (Pearson)                    : -0.3567
ρ (Spearman)                   : -0.2857
b₀                             : 16.8804
b₁                             : -0.0328
SCE                            : 182.0241
R²                             : 0.1272
RSE                            : 5.5079
SE(b₁)                         : 0.0351
t                              : -0.9352
Decisión                       : No significativo
IC 95% b₁                      : [-0.1187, 0.0531]
```

### Series (muestra_series24.csv)
```
PM3₁₈                          : 118.8530 mm
∑ índices                      : 13.0486 (esperado ≈ 12)
MAE (Ingenuo)                  : 97.5569
RMSE (Est. Ingenuo)            : 39.2727
SMAPE (Promedio)               : 22.9126%
Ganador                        : Estacional Ingenuo (SMAPE=9.6943%)
```

## 💡 Notas Importantes

1. **Diferencias de redondeo:** Es normal que haya pequeñas diferencias (< 0.0001) entre Python y R debido a precisión de punto flotante.

2. **Métodos de cálculo:** Algunos métodos (ej: cuartiles) tienen variaciones según la implementación. Los scripts usan el método tipo 7 (QUARTILE.INC de Excel).

3. **MLE vs Momentos:** En distribuciones, el método de máxima verosimilitud puede diferir del método de momentos. Esto es esperado.

4. **Validación de la app:** Si los resultados Python coinciden con R y ambos coinciden con la app, entonces la app es correcta.

## 🔗 Referencias

- **EDA:** Tukey, J. W. (1977). Exploratory Data Analysis
- **Distribuciones:** Jenkinson, A. F. (1955). The frequency distribution of the annual maximum (or minimum) values of meteorological elements
- **Regresión:** Draper, N. R., & Smith, H. (1998). Applied Regression Analysis
- **Series:** Brockwell, P. J., & Davis, R. A. (2016). Introduction to Time Series and Forecasting

## ✅ Checklist de Verificación

- [ ] He ejecutado todos los scripts Python y revisado la salida
- [ ] He ejecutado todos los scripts R en Posit Cloud
- [ ] He llenado la plantilla RESULTADOS.md
- [ ] Todos los valores coinciden (o tienen diferencias < 0.0001)
- [ ] Entiendo dónde salen las diferencias (si las hay)
- [ ] Confío en que la app es correcta
- [ ] Puedo explicar cada cálculo paso a paso

---

**Creado:** 2026-11-05  
**Versión:** 1.0  
**Estudiante:** Justo Fuentes (6820995)
