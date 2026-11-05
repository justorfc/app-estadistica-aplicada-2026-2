#!/usr/bin/env python3
"""
Verificación a mano de Regresión Lineal Simple
Muestra: muestra_reg8.csv (8 pares: lámina de riego vs rendimiento)
Cálculos con fórmulas explícitas
"""

import pandas as pd
import math
from scipy import stats as sp_stats

print("\n" + "="*80)
print("VERIFICACIÓN REGRESIÓN LINEAL - muestra_reg8.csv")
print("="*80)

# 1. Cargar datos
df = pd.read_csv('datos/muestra_reg8.csv')
print("\n📊 Datos cargados:")
print(df)

# Extraer variables
x_datos = df['lamina_riego'].values.tolist()
y_datos = df['rendimiento'].values.tolist()
n = len(x_datos)

print(f"\nVariable X (lámina de riego): {[f'{v:.4f}' for v in x_datos]}")
print(f"Variable Y (rendimiento):     {[f'{v:.4f}' for v in y_datos]}")
print(f"n = {n}\n")

# ============================================================================
# 2. SUMAS Y PROMEDIOS
# ============================================================================
print("="*80)
print("1️⃣  CÁLCULOS PREVIOS")
print("="*80)

suma_x = sum(x_datos)
suma_y = sum(y_datos)
media_x = suma_x / n
media_y = suma_y / n

print(f"   Σ(x)    = {suma_x:.4f}")
print(f"   Σ(y)    = {suma_y:.4f}")
print(f"   x̄      = {media_x:.4f}")
print(f"   ȳ      = {media_y:.4f}")

# ============================================================================
# 3. SUMA DE CUADRADOS
# ============================================================================
print("\n" + "="*80)
print("2️⃣  SUMA DE CUADRADOS")
print("="*80)

# Sxx: suma de (x - media_x)²
sxx_terminos = [(x - media_x) ** 2 for x in x_datos]
sxx = sum(sxx_terminos)
print(f"\n   Sxx = Σ(x - x̄)²")
print(f"   Términos (x - {media_x:.4f})²:")
for i, (x, t) in enumerate(zip(x_datos, sxx_terminos)):
    print(f"      ({x:.4f} - {media_x:.4f})² = {t:.4f}")
print(f"   Sxx = {sxx:.4f}")

# Syy: suma de (y - media_y)²
syy_terminos = [(y - media_y) ** 2 for y in y_datos]
syy = sum(syy_terminos)
print(f"\n   Syy = Σ(y - ȳ)²")
print(f"   Términos (y - {media_y:.4f})²:")
for i, (y, t) in enumerate(zip(y_datos, syy_terminos)):
    print(f"      ({y:.4f} - {media_y:.4f})² = {t:.4f}")
print(f"   Syy = {syy:.4f}")

# Sxy: suma de (x - media_x) * (y - media_y)
sxy_terminos = [(x - media_x) * (y - media_y) for x, y in zip(x_datos, y_datos)]
sxy = sum(sxy_terminos)
print(f"\n   Sxy = Σ(x - x̄)(y - ȳ)")
print(f"   Términos (x - {media_x:.4f}) × (y - {media_y:.4f}):")
for i, ((x, y), t) in enumerate(zip(zip(x_datos, y_datos), sxy_terminos)):
    print(f"      ({x:.4f} - {media_x:.4f}) × ({y:.4f} - {media_y:.4f}) = {t:.4f}")
print(f"   Sxy = {sxy:.4f}")

# ============================================================================
# 4. CORRELACIÓN
# ============================================================================
print("\n" + "="*80)
print("3️⃣  CORRELACIÓN (r de Pearson)")
print("="*80)

r_pearson = sxy / math.sqrt(sxx * syy)
print(f"   Fórmula: r = Sxy / √(Sxx × Syy)")
print(f"   r = {sxy:.4f} / √({sxx:.4f} × {syy:.4f})")
print(f"   r = {sxy:.4f} / √({sxx * syy:.4f})")
print(f"   r = {sxy:.4f} / {math.sqrt(sxx * syy):.4f}")
print(f"   r = {r_pearson:.4f}")

# Correlación de Spearman (rangos)
rangos_x = [sorted(x_datos).index(x) + 1 for x in x_datos]
rangos_y = [sorted(y_datos).index(y) + 1 for y in y_datos]

d_terminos = [(rx - ry) ** 2 for rx, ry in zip(rangos_x, rangos_y)]
suma_d2 = sum(d_terminos)
rho_spearman = 1 - (6 * suma_d2) / (n * (n**2 - 1))

print(f"\n   Correlación de Spearman (ρ) - Método de rangos:")
print(f"   Rangos X: {rangos_x}")
print(f"   Rangos Y: {rangos_y}")
print(f"   Fórmula: ρ = 1 - (6 × Σ(d²)) / (n × (n² - 1))")
print(f"   ρ = 1 - (6 × {suma_d2:.4f}) / ({n} × {n**2 - 1})")
print(f"   ρ = {rho_spearman:.4f}")

# ============================================================================
# 5. REGRESIÓN LINEAL: y = b0 + b1*x
# ============================================================================
print("\n" + "="*80)
print("4️⃣  REGRESIÓN LINEAL y = b₀ + b₁×x")
print("="*80)

# Pendiente b1
b1 = sxy / sxx
print(f"   b₁ = Sxy / Sxx = {sxy:.4f} / {sxx:.4f} = {b1:.4f}")

# Intercepción b0
b0 = media_y - b1 * media_x
print(f"   b₀ = ȳ - b₁ × x̄ = {media_y:.4f} - {b1:.4f} × {media_x:.4f} = {b0:.4f}")

print(f"\n   Ecuación: ŷ = {b0:.4f} + {b1:.4f} × x")

# ============================================================================
# 6. SUMA DE CUADRADOS DEL ERROR (SCE)
# ============================================================================
print("\n" + "="*80)
print("5️⃣  SUMA DE CUADRADOS DEL ERROR (SCE)")
print("="*80)

# Predicciones
y_pred = [b0 + b1 * x for x in x_datos]
residuos = [y - yp for y, yp in zip(y_datos, y_pred)]

print(f"   Predicciones ŷ_i y residuos (e_i = y_i - ŷ_i):")
print(f"   i | x_i        | y_i        | ŷ_i        | e_i        | e_i²")
print(f"   " + "-" * 60)

sce_terminos = []
for i, (x, y, yp, e) in enumerate(zip(x_datos, y_datos, y_pred, residuos)):
    e2 = e ** 2
    sce_terminos.append(e2)
    print(f"   {i+1} | {x:10.4f} | {y:10.4f} | {yp:10.4f} | {e:10.4f} | {e2:10.4f}")

sce = sum(sce_terminos)
print(f"   " + "-" * 60)
print(f"   SCE = Σ(e²) = {sce:.4f}")

# ============================================================================
# 7. COEFICIENTE DE DETERMINACIÓN (R²)
# ============================================================================
print("\n" + "="*80)
print("6️⃣  COEFICIENTE DE DETERMINACIÓN (R²)")
print("="*80)

r_squared = 1 - (sce / syy)
print(f"   Fórmula: R² = 1 - (SCE / Syy)")
print(f"   R² = 1 - ({sce:.4f} / {syy:.4f})")
print(f"   R² = {r_squared:.4f}")
print(f"   Interpretación: El modelo explica el {r_squared*100:.2f}% de la variabilidad")

# ============================================================================
# 8. ERROR ESTÁNDAR DE ESTIMACIÓN (RSE)
# ============================================================================
print("\n" + "="*80)
print("7️⃣  ERROR ESTÁNDAR DE ESTIMACIÓN (RSE)")
print("="*80)

gl = n - 2  # grados de libertad
mse = sce / gl  # Mean Squared Error
rse = math.sqrt(mse)

print(f"   Grados de libertad: GL = n - 2 = {n} - 2 = {gl}")
print(f"   MSE = SCE / GL = {sce:.4f} / {gl} = {mse:.4f}")
print(f"   RSE = √(MSE) = √({mse:.4f}) = {rse:.4f}")

# ============================================================================
# 9. ERROR ESTÁNDAR DE b1
# ============================================================================
print("\n" + "="*80)
print("8️⃣  ERROR ESTÁNDAR DE b₁")
print("="*80)

se_b1 = rse / math.sqrt(sxx)
print(f"   Fórmula: SE(b₁) = RSE / √(Sxx)")
print(f"   SE(b₁) = {rse:.4f} / √({sxx:.4f})")
print(f"   SE(b₁) = {rse:.4f} / {math.sqrt(sxx):.4f} = {se_b1:.4f}")

# ============================================================================
# 10. ESTADÍSTICO t PARA b1
# ============================================================================
print("\n" + "="*80)
print("9️⃣  ESTADÍSTICO t PARA b₁")
print("="*80)

t_stat = b1 / se_b1
print(f"   Fórmula: t = b₁ / SE(b₁)")
print(f"   t = {b1:.4f} / {se_b1:.4f} = {t_stat:.4f}")

# Valor p (test de dos colas)
p_value = 2 * (1 - sp_stats.t.cdf(abs(t_stat), gl))
print(f"   Grados de libertad: {gl}")
print(f"   Valor p (dos colas): {p_value:.4f}")

# Decisión a α = 0.05
alpha = 0.05
if p_value < alpha:
    decision = "Rechazar H₀: b₁ es significativamente diferente de 0 (p < 0.05)"
else:
    decision = "No rechazar H₀: b₁ NO es significativamente diferente de 0 (p ≥ 0.05)"

print(f"   Decisión (α = {alpha}): {decision}")

# ============================================================================
# 11. INTERVALO DE CONFIANZA AL 95% PARA b1
# ============================================================================
print("\n" + "="*80)
print("🔟  INTERVALO DE CONFIANZA AL 95% PARA b₁")
print("="*80)

# t crítico para α/2 = 0.025 con gl grados de libertad
t_critico = sp_stats.t.ppf(0.975, gl)
margen_error = t_critico * se_b1

ic_inf = b1 - margen_error
ic_sup = b1 + margen_error

print(f"   Fórmula: IC = b₁ ± t_α/2 × SE(b₁)")
print(f"   t_0.025,{gl} = {t_critico:.4f}")
print(f"   Margen de error = {t_critico:.4f} × {se_b1:.4f} = {margen_error:.4f}")
print(f"   IC 95% = [{ic_inf:.4f}, {ic_sup:.4f}]")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("📊 RESUMEN DE RESULTADOS (4 decimales)")
print("="*80)
print(f"n                              : {n}")
print(f"Sxx                            : {sxx:.4f}")
print(f"Syy                            : {syy:.4f}")
print(f"Sxy                            : {sxy:.4f}")
print(f"Correlación de Pearson (r)     : {r_pearson:.4f}")
print(f"Correlación de Spearman (ρ)    : {rho_spearman:.4f}")
print(f"b₀ (intercepción)              : {b0:.4f}")
print(f"b₁ (pendiente)                 : {b1:.4f}")
print(f"SCE                            : {sce:.4f}")
print(f"R²                             : {r_squared:.4f}")
print(f"RSE                            : {rse:.4f}")
print(f"SE(b₁)                         : {se_b1:.4f}")
print(f"t = b₁ / SE(b₁)                : {t_stat:.4f}")
print(f"Decisión (α=0.05)              : {'Sig.' if p_value < 0.05 else 'No sig.'}")
print(f"IC 95% para b₁                 : [{ic_inf:.4f}, {ic_sup:.4f}]")

print("\n" + "="*80 + "\n")
