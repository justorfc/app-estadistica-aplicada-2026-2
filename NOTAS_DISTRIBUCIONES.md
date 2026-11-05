# Módulo `src/distribuciones.py`

Módulo para seleccionar el mejor modelo de distribución de probabilidad para la precipitación máxima anual usando múltiples criterios estadísticos de ajuste.

## Funciones Principales

### 1. **ajustar(datos, nombre)** → (params, k)
- Ajusta una distribución a datos por máxima verosimilitud
- Retorna parámetros estimados y número de parámetros libres
- Nota: Para distribuciones con `loc=0` fijo (Lognormal, Gamma, Weibull), retorna 3 elementos: (shape, loc=0, scale)

### 2. **log_verosimilitud(datos, nombre, params)** → float
- Calcula ℓ = Σ ln(f(x_i | θ)) (suma de log-densidades)

### 3. **criterios_informacion(datos, nombre, params)** → dict
- Retorna AIC, BIC y AICc
- AIC = 2k - 2ℓ
- BIC = k·ln(n) - 2ℓ
- AICc = AIC + 2k(k+1)/(n-k-1)

### 4. **bondad_ajuste(datos, nombre, n_mc=199)** → dict
- Pruebas de bondad de ajuste con valores p por Monte Carlo
- Estadísticos: Kolmogorov-Smirnov (K-S) y Anderson-Darling (A-D)
- Corrige el problema de Lilliefors

### 5. **tabla_comparativa(datos, n_mc=199)** → DataFrame
- Tabla con todas las 6 distribuciones ordenadas por AIC
- Columnas: Parámetros, k, log-verosimilitud, AIC, BIC, AICc, ΔAIC, interpretación, tests
- **Interpretación ΔAIC** (Burnham & Anderson):
  - ΔAIC < 2: Soporte sustancial
  - ΔAIC 4-7: Considerablemente menos soporte
  - ΔAIC > 10: Esencialmente sin soporte

### 6. **posiciones_graficas(datos)** → dict
- Calcula posiciones para Q-Q plots
- Incluye: datos ordenados, posiciones de Weibull y Gringorten, período de retorno empírico

### 7. **cuantil_retorno(nombre, params, T)** → float o array
- Calcula x_T = F⁻¹(1 - 1/T) para período de retorno T años
- F = probabilidad acumulada = 1 - 1/T

### 8. **riesgo_falla(T, N)** → float
- R = 1 - (1 - 1/T)^N
- Probabilidad de excedencia en N años para período de retorno T

### 9. **bootstrap_cuantil(datos, nombre, T, B=500, semilla=42)** → dict
- Intervalo de confianza al 95% del cuantil x_T
- Bootstrap paramétrico: resamplea de la distribución ajustada

### 10. **gumbel_momentos(datos)** → dict
- Método de momentos para Gumbel (cálculo manual)
- β = s·√6/π
- μ = x̄ - 0.5772·β

## Distribuciones Candidatas

| Distribución | Scipy | Parámetros | loc fijo |
|--------------|-------|------------|----------|
| Normal | `norm` | (μ, σ) | No |
| Lognormal | `lognorm` | (s, σ) | 0 |
| Gamma | `gamma` | (α, β) | 0 |
| Weibull | `weibull_min` | (c, σ) | 0 |
| Gumbel | `gumbel_r` | (μ, β) | No |
| GEV | `genextreme` | (ξ, μ, σ) | No |

**Nota sobre GEV:** En scipy, c = -ξ (opuesto del índice de forma)

## Uso Ejemplo

```python
import pandas as pd
from src.distribuciones import tabla_comparativa, cuantil_retorno

# Cargar datos
df = pd.read_csv('datos/precip_max_anual.csv')
datos = df['pmax24h_mm'].dropna().values

# Tabla comparativa
tabla = tabla_comparativa(datos, n_mc=199)
print(tabla)

# Mejor distribución
mejor_dist = tabla.iloc[0]['Distribución']
params = tabla.iloc[0]['params_tuple']

# Cuantil para T = 100 años
x_100 = cuantil_retorno(mejor_dist, params, 100)
print(f"Precipitación esperada cada 100 años: {x_100:.2f} mm")
```

## Ejecución de Prueba

```bash
.venv/bin/python -m src.distribuciones
```

Genera:
- Tabla comparativa ordenada por AIC
- Cuantiles de retorno con intervalos de confianza
- Riesgos de falla
- Parámetros de Gumbel por método de momentos
