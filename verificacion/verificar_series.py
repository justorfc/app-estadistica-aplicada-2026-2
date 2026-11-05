#!/usr/bin/env python3
"""
Verificación a mano de Series de Tiempo
Muestra: muestra_series24.csv (24 meses: 18 entrenamiento + 6 validación)
Cálculos con fórmulas explícitas
"""

import pandas as pd
import math

print("\n" + "="*80)
print("VERIFICACIÓN SERIES DE TIEMPO - muestra_series24.csv")
print("="*80)

# 1. Cargar datos
df = pd.read_csv('datos/muestra_series24.csv')
print("\n📊 Datos cargados:")
print(df.to_string())

# Extraer precipitación y período
precip = df['precipitacion_mm'].values.tolist()
periodos = df['periodo'].values.tolist()
conjunto = df['conjunto'].values.tolist()
meses = df['mes'].values.tolist()
anios = df['anio'].values.tolist()

n_total = len(precip)
n_ent = sum(1 for c in conjunto if c == 'entrenamiento')
n_val = n_total - n_ent

print(f"\nTotal de datos: {n_total} (Entrenamiento: {n_ent}, Validación: {n_val})")

# Separar entrenamiento y validación
precip_ent = precip[:n_ent]
precip_val = precip[n_ent:]
meses_val = meses[n_ent:]
anios_val = anios[n_ent:]

print(f"Datos de entrenamiento (t=1 a {n_ent}):")
for i, p in enumerate(precip_ent, 1):
    print(f"   t={i:2d}: {p:.4f} mm")

print(f"\nDatos de validación (t={n_ent+1} a {n_total}):")
for i, (p, m, a) in enumerate(zip(precip_val, meses_val, anios_val), n_ent+1):
    print(f"   t={i:2d} ({a}-{m:02d}): {p:.4f} mm")

# ============================================================================
# 1. PROMEDIO MÓVIL 3 (PM3) DE 2025
# ============================================================================
print("\n" + "="*80)
print("1️⃣  PROMEDIO MÓVIL 3 (PM3) DEL PERÍODO DE ENTRENAMIENTO")
print("="*80)
print(f"   Fórmula: PM3_t = (y_t + y_(t-1) + y_(t-2)) / 3")
print(f"\n   t | Dato        | PM3")
print(f"   " + "-" * 35)

pm3 = []
for i in range(n_ent):
    if i < 2:
        pm3_val = None
        pm3.append(pm3_val)
        print(f"   {i+1:2d} | {precip_ent[i]:11.4f} | N/A (no hay 3 datos)")
    else:
        # PM3 usando los 3 últimos valores hasta la posición i
        pm3_val = (precip_ent[i] + precip_ent[i-1] + precip_ent[i-2]) / 3
        pm3.append(pm3_val)
        print(f"   {i+1:2d} | {precip_ent[i]:11.4f} | ({precip_ent[i]:.2f} + {precip_ent[i-1]:.2f} + {precip_ent[i-2]:.2f}) / 3 = {pm3_val:.4f}")

# ============================================================================
# 2. ÍNDICES ESTACIONALES (12 meses)
# ============================================================================
print("\n" + "="*80)
print("2️⃣  ÍNDICES ESTACIONALES POR MES")
print("="*80)

# Extraer valores por mes del período de entrenamiento
datos_por_mes = {mes: [] for mes in range(1, 13)}
for i, (p, m) in enumerate(zip(precip_ent, meses[:n_ent])):
    datos_por_mes[m].append(p)

# Media general de entrenamiento
media_general = sum(precip_ent) / len(precip_ent)

print(f"   Media general (entrenamiento): {media_general:.4f}")
print(f"\n   Mes | Valores                    | Media mes | Índice = Media_mes / Media_gral")
print(f"   " + "-" * 75)

indices_estacionales = {}
for mes in range(1, 13):
    vals = datos_por_mes[mes]
    if vals:
        media_mes = sum(vals) / len(vals)
        indice = media_mes / media_general
        indices_estacionales[mes] = indice
        vals_str = ", ".join([f"{v:.2f}" for v in vals])
        print(f"   {mes:2d}  | {vals_str:26s} | {media_mes:9.4f} | {indice:.4f}")

# Verificar suma de índices (debe ser ≈12)
suma_indices = sum(indices_estacionales.values())
print(f"\n   Suma de índices: {suma_indices:.4f} (debe ser ≈ 12.0000)")

# ============================================================================
# 3. MÉTODOS DE REFERENCIA - PRONÓSTICOS PARA VALIDACIÓN (6 meses)
# ============================================================================
print("\n" + "="*80)
print("3️⃣  PRONÓSTICOS CON MÉTODOS DE REFERENCIA")
print("="*80)

# Método 1: Ingenuo (naive) - ŷ_t = y_(t-1)
print(f"\n   MÉTODO 1: INGENUO (Naive) - ŷ_t = y_(t-1)")
print(f"   _______________________________________________")
print(f"   t | Mes-Año    | Real       | ŷ         | Error")
print(f"   " + "-" * 50)

pron_naive = []
for i, (real, mes, anio) in enumerate(zip(precip_val, meses_val, anios_val)):
    # El pronóstico es el último valor del entrenamiento (o el anterior si i>0)
    if i == 0:
        pred = precip_ent[-1]  # Último valor del entrenamiento
    else:
        pred = precip_val[i-1]  # Valor anterior en validación
    
    pron_naive.append(pred)
    error = real - pred
    print(f"   {n_ent+i+1:2d} | {anio}-{mes:02d}   | {real:10.4f} | {pred:9.4f} | {error:9.4f}")

# Método 2: Estacional Ingenuo (seasonal naive) - ŷ_t = y_(t-12)
print(f"\n   MÉTODO 2: ESTACIONAL INGENUO - ŷ_t = y_(t-12)")
print(f"   _______________________________________________")
print(f"   t | Mes-Año    | Real       | ŷ         | Error")
print(f"   " + "-" * 50)

pron_seasonal = []
for i, (real, mes, anio) in enumerate(zip(precip_val, meses_val, anios_val)):
    # El pronóstico es el valor del mismo mes pero 12 meses atrás
    idx_12_atras = (n_ent + i - 12)
    if idx_12_atras >= 0:
        pred = precip[idx_12_atras]
    else:
        pred = precip_ent[(n_ent + i - 12) % len(precip_ent)]
    
    pron_seasonal.append(pred)
    error = real - pred
    print(f"   {n_ent+i+1:2d} | {anio}-{mes:02d}   | {real:10.4f} | {pred:9.4f} | {error:9.4f}")

# Método 3: Promedio - ŷ_t = promedio de todos los datos de entrenamiento
print(f"\n   MÉTODO 3: PROMEDIO - ŷ_t = promedio_entrenamiento")
print(f"   _______________________________________________")
print(f"   t | Mes-Año    | Real       | ŷ         | Error")
print(f"   " + "-" * 50)

media_ent = sum(precip_ent) / len(precip_ent)
pron_promedio = []

for i, (real, mes, anio) in enumerate(zip(precip_val, meses_val, anios_val)):
    pred = media_ent
    pron_promedio.append(pred)
    error = real - pred
    print(f"   {n_ent+i+1:2d} | {anio}-{mes:02d}   | {real:10.4f} | {pred:9.4f} | {error:9.4f}")

# ============================================================================
# 4. MÉTRICAS DE ERROR
# ============================================================================
print("\n" + "="*80)
print("4️⃣  MÉTRICAS DE ERROR (MAE, RMSE, SMAPE)")
print("="*80)

def mae(reales, predicciones):
    """Mean Absolute Error"""
    return sum(abs(r - p) for r, p in zip(reales, predicciones)) / len(reales)

def rmse(reales, predicciones):
    """Root Mean Squared Error"""
    sse = sum((r - p) ** 2 for r, p in zip(reales, predicciones))
    return math.sqrt(sse / len(reales))

def smape(reales, predicciones):
    """Symmetric Mean Absolute Percentage Error"""
    errores = [abs(r - p) / (abs(r) + abs(p)) for r, p in zip(reales, predicciones)]
    return (sum(errores) / len(errores)) * 100

# Calcular para cada método
metodos = {
    'Ingenuo': pron_naive,
    'Estacional Ingenuo': pron_seasonal,
    'Promedio': pron_promedio
}

print(f"\n   Método                 | MAE        | RMSE       | SMAPE (%)")
print(f"   " + "-" * 60)

resultados_metricas = {}
for nombre_metodo, predicciones in metodos.items():
    mae_val = mae(precip_val, predicciones)
    rmse_val = rmse(precip_val, predicciones)
    smape_val = smape(precip_val, predicciones)
    
    resultados_metricas[nombre_metodo] = {
        'MAE': mae_val,
        'RMSE': rmse_val,
        'SMAPE': smape_val
    }
    
    print(f"   {nombre_metodo:22s} | {mae_val:10.4f} | {rmse_val:10.4f} | {smape_val:9.4f}")

# Método ganador
metodo_ganador = min(resultados_metricas.items(), key=lambda x: x[1]['SMAPE'])
print(f"\n   🏆 Método ganador (menor SMAPE): {metodo_ganador[0]} con SMAPE = {metodo_ganador[1]['SMAPE']:.4f}%")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("📊 RESUMEN DE RESULTADOS (4 decimales)")
print("="*80)

print(f"\nPromedio Móvil 3 (últimos 3 valores del entrenamiento):")
print(f"   PM3_18 = {pm3[-1]:.4f} mm")

print(f"\nÍndices Estacionales (12 meses):")
for mes in range(1, 13):
    print(f"   Mes {mes:2d}: {indices_estacionales[mes]:.4f}")

print(f"\nMétricas de Error:")
print(f"{'Método':22s} | {'MAE':>10s} | {'RMSE':>10s} | {'SMAPE (%)':>10s}")
print("-" * 60)
for nombre, metricas in resultados_metricas.items():
    print(f"{nombre:22s} | {metricas['MAE']:10.4f} | {metricas['RMSE']:10.4f} | {metricas['SMAPE']:10.4f}")

print(f"\n🏆 Ganador: {metodo_ganador[0]} (SMAPE = {metodo_ganador[1]['SMAPE']:.4f}%)")

print("\n" + "="*80 + "\n")
