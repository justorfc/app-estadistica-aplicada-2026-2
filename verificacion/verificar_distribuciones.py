#!/usr/bin/env python3
"""
Verificación a mano de Distribuciones Probabilísticas
Muestra: muestra_dist10.csv (10 valores de precipitación máxima en 24h)
Cálculos con fórmulas explícitas para Weibull y Gumbel
"""

import pandas as pd
import math

print("\n" + "="*80)
print("VERIFICACIÓN DISTRIBUCIONES - muestra_dist10.csv")
print("="*80)

# 1. Cargar datos
df = pd.read_csv('datos/muestra_dist10.csv')
print("\n📊 Datos cargados:")
print(df)

# Extraer precipitación máxima en 24h
datos = sorted(df['pmax24h_mm'].values.tolist())
n = len(datos)

print(f"\n📋 Datos ordenados (n={n}):")
for i, x in enumerate(datos, 1):
    print(f"   x({i}) = {x:.4f}")

# ============================================================================
# 2. POSICIÓN DE WEIBULL (para gráfico de probabilidad)
# ============================================================================
print("\n" + "="*80)
print("1️⃣  POSICIÓN DE WEIBULL (para gráfico de probabilidad)")
print("="*80)
print(f"   Fórmula: F(x) = i / (n + 1)")
print(f"\n   i  | x(i)       | F(x) = i/{n+1}")
print(f"   " + "-" * 40)

posiciones_weibull = []
for i in range(1, n + 1):
    f_x = i / (n + 1)
    posiciones_weibull.append(f_x)
    print(f"   {i:2d} | {datos[i-1]:10.4f} | {f_x:.4f}")

# ============================================================================
# 3. DISTRIBUCIÓN DE GUMBEL - AJUSTE POR MOMENTOS
# ============================================================================
print("\n" + "="*80)
print("2️⃣  DISTRIBUCIÓN DE GUMBEL - MÉTODO DE MOMENTOS")
print("="*80)

# Calcular media y desviación estándar
media = sum(datos) / n
print(f"   Media = {media:.4f}")

suma_dev_cuad = sum((x - media) ** 2 for x in datos)
varianza = suma_dev_cuad / (n - 1)  # muestral
desv_est = math.sqrt(varianza)
print(f"   Desviación estándar (muestral) = {desv_est:.4f}")

# Gumbel: media = μ + γ*C, var = (π²/6)*β²
# donde γ = 0.5772... (constante de Euler), C = 0.5772...
# Inversas: μ = media - (π/√6) * σ, β = σ * √6 / π

gamma_euler = 0.5772156649
pi = math.pi
sqrt6 = math.sqrt(6)

# Parámetros de Gumbel ajustados por momentos
beta = desv_est * sqrt6 / pi
mu = media - beta * gamma_euler

print(f"\n   Constante de Euler γ = {gamma_euler:.10f}")
print(f"   √6 / π = {sqrt6 / pi:.10f}")
print(f"\n   β = σ × (√6 / π) = {desv_est:.4f} × {sqrt6/pi:.10f} = {beta:.4f}")
print(f"   μ = media - β × γ = {media:.4f} - {beta:.4f} × {gamma_euler:.10f} = {mu:.4f}")

# ============================================================================
# 4. T EMPÍRICO (Período de retorno empírico)
# ============================================================================
print("\n" + "="*80)
print("3️⃣  PERÍODO DE RETORNO EMPÍRICO T")
print("="*80)
print(f"   Fórmula: T = (n + 1) / i")
print(f"\n   i  | x(i)       | T = {n+1}/i")
print(f"   " + "-" * 40)

periodos_empiricos = []
for i in range(1, n + 1):
    t_emp = (n + 1) / i
    periodos_empiricos.append(t_emp)
    print(f"   {i:2d} | {datos[i-1]:10.4f} | {t_emp:.4f} años")

# ============================================================================
# 5. VALORES DE x PARA PERÍODOS DE RETORNO ESPECÍFICOS (10, 50, 100 años)
# ============================================================================
print("\n" + "="*80)
print("4️⃣  CÁLCULO DE x_T PARA T = 10, 50, 100 AÑOS (Gumbel)")
print("="*80)
print(f"   Fórmula Gumbel: x_T = μ - β × ln(-ln(1 - 1/T))")
print(f"   Parámetros: μ = {mu:.4f}, β = {beta:.4f}\n")

periodos_target = [10, 50, 100]
valores_xt = {}

for T in periodos_target:
    # Probability: 1 - 1/T
    prob = 1 - (1 / T)
    # -ln(-ln(prob))
    ln_prob = math.log(-math.log(prob))
    x_t = mu - beta * ln_prob
    
    valores_xt[T] = x_t
    print(f"   T = {T} años:")
    print(f"      P(x ≤ x_T) = 1 - 1/{T} = {prob:.6f}")
    print(f"      -ln(-ln({prob:.6f})) = {ln_prob:.4f}")
    print(f"      x_{T} = {mu:.4f} - {beta:.4f} × {ln_prob:.4f} = {x_t:.4f} mm")
    print()

# ============================================================================
# 6. RIESGO PARA T = 50 AÑOS y N = 25 AÑOS
# ============================================================================
print("="*80)
print("5️⃣  RIESGO PARA T = 50 AÑOS, N = 25 AÑOS")
print("="*80)
print(f"   Fórmula: R = 1 - (1 - 1/T)^N")
print(f"   Concepto: Probabilidad de que ocurra al menos 1 evento")
print(f"             en un período de N años cuando T es el período de retorno")

T_riesgo = 50
N_riesgo = 25

# Probabilidad anual de NO excedencia
prob_no_excedencia = 1 - (1 / T_riesgo)

# Probabilidad de no excedencia en N años
prob_no_excedencia_n = prob_no_excedencia ** N_riesgo

# Riesgo: probabilidad de excedencia al menos 1 vez
riesgo = 1 - prob_no_excedencia_n

print(f"\n   T = {T_riesgo} años, N = {N_riesgo} años")
print(f"   P(no excedencia en 1 año) = 1 - 1/{T_riesgo} = {prob_no_excedencia:.6f}")
print(f"   P(no excedencia en {N_riesgo} años) = ({prob_no_excedencia:.6f})^{N_riesgo} = {prob_no_excedencia_n:.6f}")
print(f"   Riesgo R = 1 - {prob_no_excedencia_n:.6f} = {riesgo:.4f} ({riesgo*100:.2f}%)")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("📊 RESUMEN DE RESULTADOS (4 decimales)")
print("="*80)
print(f"\nParámetros de Gumbel (Método de Momentos):")
print(f"  μ (localización)  = {mu:.4f}")
print(f"  β (escala)        = {beta:.4f}")

print(f"\nValores de x_T (precipitación máxima esperada):")
for T in periodos_target:
    print(f"  x_{T} años = {valores_xt[T]:.4f} mm")

print(f"\nRiesgo para T = {T_riesgo} años, N = {N_riesgo} años: {riesgo:.4f} ({riesgo*100:.2f}%)")

print(f"\nTabla completa de Posiciones y Períodos:")
print(f"{'i':>2} | {'x(i)':>10} | {'F(x) Weib.':>10} | {'T empírico':>10}")
print("-" * 45)
for i in range(n):
    print(f"{i+1:2d} | {datos[i]:10.4f} | {posiciones_weibull[i]:10.4f} | {periodos_empiricos[i]:10.4f}")

print("\n" + "="*80 + "\n")
