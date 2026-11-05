#!/usr/bin/env python3
"""
Verificación a mano de Análisis Exploratorio de Datos (EDA)
Muestra: muestra_eda10.csv (10 observaciones)
Cálculos con fórmulas explícitas, sin funciones de la app
"""

import pandas as pd
import math

print("\n" + "="*80)
print("VERIFICACIÓN EDA - muestra_eda10.csv")
print("="*80)

# 1. Cargar datos
df = pd.read_csv('datos/muestra_eda10.csv')
print("\n📊 Datos cargados:")
print(df)

# Extraer rendimiento (variable de análisis)
datos = df['rendimiento'].values.tolist()
n = len(datos)

print(f"\n📋 Datos: {datos}")
print(f"n = {n}\n")

# ============================================================================
# 2. MEDIA (promedio aritmético)
# ============================================================================
print("1️⃣  MEDIA (Promedio)")
print("-" * 80)
suma = sum(datos)
media = suma / n
print(f"   Fórmula: media = Σ(x) / n")
print(f"   Σ(x) = {suma:.4f}")
print(f"   media = {suma:.4f} / {n} = {media:.4f}")

# ============================================================================
# 3. MEDIANA
# ============================================================================
print("\n2️⃣  MEDIANA")
print("-" * 80)
datos_ordenados = sorted(datos)
print(f"   Datos ordenados: {[f'{x:.4f}' for x in datos_ordenados]}")

if n % 2 == 1:
    # n impar: mediana es el valor central
    mediana = datos_ordenados[n // 2]
    print(f"   n={n} es impar → posición central = {n//2 + 1}")
    print(f"   mediana = {mediana:.4f}")
else:
    # n par: mediana es el promedio de los dos valores centrales
    idx1, idx2 = n // 2 - 1, n // 2
    val1, val2 = datos_ordenados[idx1], datos_ordenados[idx2]
    mediana = (val1 + val2) / 2
    print(f"   n={n} es par → promedios posiciones {idx1+1} y {idx2+1}")
    print(f"   mediana = ({val1:.4f} + {val2:.4f}) / 2 = {mediana:.4f}")

# ============================================================================
# 4. VARIANZA
# ============================================================================
print("\n3️⃣  VARIANZA (S²)")
print("-" * 80)
print(f"   Fórmula: S² = Σ(x - media)² / (n-1)  [muestral]")

# Calcular desviaciones
desviaciones_cuadrado = [(x - media) ** 2 for x in datos]
print(f"\n   Desviaciones al cuadrado (x - {media:.4f})²:")
for i, (x, d2) in enumerate(zip(datos, desviaciones_cuadrado)):
    print(f"      ({x:.4f} - {media:.4f})² = {d2:.4f}")

suma_dev_cuad = sum(desviaciones_cuadrado)
varianza = suma_dev_cuad / (n - 1)
print(f"\n   Σ(x - media)² = {suma_dev_cuad:.4f}")
print(f"   S² = {suma_dev_cuad:.4f} / {n-1} = {varianza:.4f}")

# ============================================================================
# 5. DESVIACIÓN ESTÁNDAR
# ============================================================================
print("\n4️⃣  DESVIACIÓN ESTÁNDAR (S)")
print("-" * 80)
desv_est = math.sqrt(varianza)
print(f"   Fórmula: S = √(S²)")
print(f"   S = √({varianza:.4f}) = {desv_est:.4f}")

# ============================================================================
# 6. COEFICIENTE DE VARIACIÓN (CV)
# ============================================================================
print("\n5️⃣  COEFICIENTE DE VARIACIÓN (CV)")
print("-" * 80)
cv = (desv_est / media) * 100
print(f"   Fórmula: CV = (S / media) × 100")
print(f"   CV = ({desv_est:.4f} / {media:.4f}) × 100 = {cv:.4f}%")

# ============================================================================
# 7. CUARTILES (Q1, Q3) - Método tipo 7 (QUARTILE.INC de Excel)
# ============================================================================
print("\n6️⃣  CUARTILES (Método tipo 7 - QUARTILE.INC)")
print("-" * 80)

def quantile_tipo7(datos_ord, p):
    """
    Cálculo de cuantil tipo 7 (método por defecto en Excel, R y SciPy)
    Fórmula: h = (n-1) * p
    Si h es entero: Q = x[h]
    Si h es decimal: Q = x[piso(h)] + frac(h) * (x[piso(h)+1] - x[piso(h)])
    """
    n = len(datos_ord)
    h = (n - 1) * p
    h_piso = int(h)
    h_frac = h - h_piso
    
    if h_frac == 0:
        return datos_ord[h_piso]
    else:
        x_inf = datos_ord[h_piso]
        x_sup = datos_ord[h_piso + 1]
        return x_inf + h_frac * (x_sup - x_inf)

q1 = quantile_tipo7(datos_ordenados, 0.25)
q3 = quantile_tipo7(datos_ordenados, 0.75)

print(f"   Fórmula: h = (n-1) × p")
print(f"   Para Q1 (p=0.25): h = ({n}-1) × 0.25 = {(n-1)*0.25:.4f}")
print(f"   Q1 = {q1:.4f}")
print(f"\n   Para Q3 (p=0.75): h = ({n}-1) × 0.75 = {(n-1)*0.75:.4f}")
print(f"   Q3 = {q3:.4f}")

# ============================================================================
# 8. RANGO INTERCUARTÍLICO (RIC)
# ============================================================================
print("\n7️⃣  RANGO INTERCUARTÍLICO (RIC)")
print("-" * 80)
ric = q3 - q1
print(f"   Fórmula: RIC = Q3 - Q1")
print(f"   RIC = {q3:.4f} - {q1:.4f} = {ric:.4f}")

# ============================================================================
# 9. VALLAS DE TUKEY Y VALORES ATÍPICOS
# ============================================================================
print("\n8️⃣  VALLAS DE TUKEY")
print("-" * 80)

valla_inf = q1 - 1.5 * ric
valla_sup = q3 + 1.5 * ric

print(f"   Fórmula: Valla inferior = Q1 - 1.5 × RIC")
print(f"            Valla superior = Q3 + 1.5 × RIC")
print(f"\n   Valla inferior = {q1:.4f} - 1.5 × {ric:.4f} = {valla_inf:.4f}")
print(f"   Valla superior = {q3:.4f} + 1.5 × {ric:.4f} = {valla_sup:.4f}")

# Detectar atípicos
atipicos = [x for x in datos if x < valla_inf or x > valla_sup]
print(f"\n   Valores atípicos (fuera de [{valla_inf:.4f}, {valla_sup:.4f}]):")
if atipicos:
    for x in atipicos:
        print(f"      {x:.4f}")
else:
    print(f"      Ninguno")

# ============================================================================
# 10. MEDIA POR RIEGO
# ============================================================================
print("\n9️⃣  MEDIA POR GRUPO (RIEGO)")
print("-" * 80)

grupos = df.groupby('riego')['rendimiento'].apply(list).to_dict()
print(f"   Datos agrupados por riego:")

medias_riego = {}
for riego, valores in grupos.items():
    media_grupo = sum(valores) / len(valores)
    medias_riego[riego] = media_grupo
    print(f"\n   Riego = {riego}:")
    print(f"      Valores: {valores}")
    print(f"      Media = {sum(valores):.4f} / {len(valores)} = {media_grupo:.4f}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("📊 RESUMEN DE RESULTADOS (4 decimales)")
print("="*80)
print(f"Media                          : {media:.4f}")
print(f"Mediana                        : {mediana:.4f}")
print(f"Varianza (S²)                  : {varianza:.4f}")
print(f"Desviación estándar (S)        : {desv_est:.4f}")
print(f"Coeficiente de variación (CV)  : {cv:.4f}%")
print(f"Q1 (Cuartil 1)                 : {q1:.4f}")
print(f"Q3 (Cuartil 3)                 : {q3:.4f}")
print(f"Rango Intercuartílico (RIC)    : {ric:.4f}")
print(f"Valla inferior de Tukey        : {valla_inf:.4f}")
print(f"Valla superior de Tukey        : {valla_sup:.4f}")
print(f"Cantidad de atípicos           : {len(atipicos)}")

print(f"\nMedia por riego (Sí)           : {medias_riego.get('Sí', 'N/A'):.4f}")
print(f"Media por riego (No)           : {medias_riego.get('No', 'N/A'):.4f}")

print("\n" + "="*80 + "\n")
