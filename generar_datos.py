"""
Script de generación de datos simulados personalizados para App de Estadística Aplicada

Este script genera datos personalizados basados en el código estudiantil, garantizando que
cada estudiante tenga un conjunto de datos reproducible y único. Los datos se guardan en
la carpeta datos/ y constan de 6 archivos CSV + 1 JSON de metadatos.

Uso: .venv/bin/python generar_datos.py
"""

import os
import json
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import gumbel_r

# ==============================================================================
# CONFIGURACIÓN Y PARÁMETROS DEL ESTUDIANTE
# ==============================================================================

CODIGO_ESTUDIANTIL = "6820995"
NOMBRES_APELLIDOS = "Justo Fuentes"

# Definir opciones disponibles (mismas para todos)
CULTIVOS = ["Maíz", "Arroz", "Yuca", "Ñame", "Ajonjolí", "Plátano", "Frijol", "Sorgo"]
RENDIMIENTOS_BASE = {
    "Maíz": 4.5, "Arroz": 4.0, "Yuca": 12.0, "Ñame": 8.0,
    "Ajonjolí": 1.2, "Plátano": 15.0, "Frijol": 1.8, "Sorgo": 2.5
}
MUNICIPIOS = ["Sincelejo", "Corozal", "Sampués", "Los Palmitos", 
              "San Marcos", "Majagual", "Tolú", "Ovejas"]

# Crear generador de números aleatorios con semilla del estudiante
semilla = int(CODIGO_ESTUDIANTIL) % (2**32)
rng = np.random.default_rng(semilla)

# Seleccionar cultivo y municipio según semilla
idx_cultivo = semilla % len(CULTIVOS)
idx_municipio = (semilla // len(CULTIVOS)) % len(MUNICIPIOS)
CULTIVO_ELEGIDO = CULTIVOS[idx_cultivo]
MUNICIPIO_ELEGIDO = MUNICIPIOS[idx_municipio]

print("\n" + "="*70)
print("GENERACIÓN DE DATOS SIMULADOS - ESTADÍSTICA APLICADA")
print("="*70)
print(f"\nEstudiante: {NOMBRES_APELLIDOS}")
print(f"Código: {CODIGO_ESTUDIANTIL}")
print(f"Cultivo asignado: {CULTIVO_ELEGIDO}")
print(f"Municipio asignado: {MUNICIPIO_ELEGIDO}")
print(f"Semilla RNG: {semilla}\n")

# Crear carpeta datos/ si no existe
os.makedirs("datos", exist_ok=True)

# ==============================================================================
# 1. ARCHIVO: parcelas.csv
# ==============================================================================
print("📊 Generando parcelas.csv...")

n_parcelas = rng.integers(80, 121)  # Entre 80 y 120

# Generar datos base
parcelas_data = {
    "parcela": [f"P{i+1:03d}" for i in range(n_parcelas)],
    "suelo": rng.choice(["Franco", "Arcilloso", "Arenoso"], n_parcelas),
    "riego": rng.choice(["Sí", "No"], n_parcelas),
    "dosis_N": rng.uniform(0, 180, n_parcelas),
    "lamina_riego": rng.uniform(50, 250, n_parcelas),  # mm
    "materia_organica": np.full(n_parcelas, np.nan),  # Se llenará con ~90% datos
    "ph": rng.uniform(4.8, 7.8, n_parcelas),
}

# Llenar materia_organica con ~90% de datos (3-6 faltantes)
n_faltantes = rng.integers(3, 7)
idx_faltantes = rng.choice(n_parcelas, n_faltantes, replace=False)
for i in range(n_parcelas):
    if i not in idx_faltantes:
        parcelas_data["materia_organica"][i] = rng.uniform(1, 8)

# Calcular rendimiento con dependencia de variables (con ruido)
rendimiento_base = RENDIMIENTOS_BASE[CULTIVO_ELEGIDO]
rendimiento = []

# Factores de influencia normalizados (0 a 1)
dosis_N_norm = parcelas_data["dosis_N"] / 180
lamina_riego_norm = parcelas_data["lamina_riego"] / 250
ph_norm = np.clip((parcelas_data["ph"] - 4.8) / (7.8 - 4.8), 0, 1)  # Óptimo cerca de 6.5
mo_norm = np.nanmean(parcelas_data["materia_organica"]) / 8 if not np.isnan(parcelas_data["materia_organica"]).all() else 0.5

# Función logística para modelar efectos
for i in range(n_parcelas):
    # Efecto positivo de N (con rendimientos decrecientes)
    efecto_N = dosis_N_norm[i] * 0.4
    
    # Efecto positivo de riego
    efecto_riego = 0.2 if parcelas_data["riego"][i] == "Sí" else 0
    
    # Efecto de pH (óptimo cerca de 6.5)
    efecto_pH = 0.3 * (1 - np.abs(ph_norm[i] - 0.5) * 2)
    
    # Efecto de materia orgánica
    if np.isnan(parcelas_data["materia_organica"][i]):
        efecto_MO = 0
    else:
        efecto_MO = np.clip(parcelas_data["materia_organica"][i] / 8, 0, 1) * 0.25
    
    # Efecto de tipo de suelo
    efecto_suelo = {"Franco": 1.0, "Arcilloso": 0.85, "Arenoso": 0.75}[parcelas_data["suelo"][i]]
    
    # Rendimiento final con ruido
    rend = rendimiento_base * (1 + efecto_N + efecto_riego + efecto_pH + efecto_MO) * efecto_suelo
    rend += rng.normal(0, rend * 0.15)  # Ruido 15%
    rendimiento.append(max(rend * 0.5, rend))  # Evitar valores negativos

parcelas_data["rendimiento"] = rendimiento

# Convertir a DataFrame
df_parcelas = pd.DataFrame(parcelas_data)

# Insertar 2 parcelas atípicas (1 muy alta, 1 muy baja)
if n_parcelas >= 2:
    idx_alta = rng.choice(n_parcelas)
    idx_baja = rng.choice(n_parcelas)
    df_parcelas.loc[idx_alta, "rendimiento"] = df_parcelas["rendimiento"].max() * 1.5
    df_parcelas.loc[idx_baja, "rendimiento"] = df_parcelas["rendimiento"].min() * 0.4

df_parcelas.to_csv("datos/parcelas.csv", index=False)
print(f"   ✓ {n_parcelas} parcelas guardadas")

# ==============================================================================
# 2. ARCHIVO: precip_max_anual.csv
# ==============================================================================
print("📊 Generando precip_max_anual.csv...")

# Parámetros Gumbel personalizados según semilla
mu_gumbel = 70 + (semilla % 31) * (30 / 2**32)  # Entre 70 y 100
beta_gumbel = 12 + (semilla % 100) * (8 / 2**32)  # Entre 12 y 20

# Generar serie histórica (1986-2025: 40 años)
años = np.arange(1986, 2026)
precip_max = gumbel_r.rvs(loc=mu_gumbel, scale=beta_gumbel, size=len(años), random_state=rng)
precip_max = np.maximum(precip_max, 20)  # Mínimo 20 mm

df_precip = pd.DataFrame({
    "anio": años,
    "pmax24h_mm": precip_max
})

df_precip.to_csv("datos/precip_max_anual.csv", index=False)
print(f"   ✓ {len(años)} años de precipitación máxima anual")

# ==============================================================================
# 3. ARCHIVO: clima_mensual.csv
# ==============================================================================
print("📊 Generando clima_mensual.csv...")

# Generar clima mensual 2015-2025 (132 meses)
fechas_inicio = pd.date_range("2015-01", "2025-12", freq="MS")
meses = fechas_inicio.month
años_clima = fechas_inicio.year

# Precipitación con régimen bimodal caribeño
precip = []
for mes in meses:
    # Lluvias: abril-mayo (4-5), septiembre-noviembre (9-11)
    # Secas: diciembre-marzo (12, 1, 2, 3)
    if mes in [4, 5, 9, 10, 11]:
        base = rng.uniform(150, 250)  # Lluvia
    elif mes in [12, 1, 2, 3]:
        base = rng.uniform(30, 80)  # Seca
    else:
        base = rng.uniform(80, 150)  # Transición
    
    # Ruido lognormal
    precip_mes = base * np.exp(rng.normal(0, 0.25))
    precip.append(max(precip_mes, 10))

# Temperatura con tendencia creciente y ciclo anual
temp = []
for i, (año, mes) in enumerate(zip(años_clima, meses)):
    # Ciclo anual (máximo en julio-agosto)
    ciclo = 2 * np.sin(2 * np.pi * (mes - 1) / 12)
    # Tendencia: +0.02°C por año desde 2015
    tendencia = (año - 2015) * 0.02
    # Base regional (~27°C)
    temp_mes = 27 + ciclo + tendencia + rng.normal(0, 0.5)
    temp.append(temp_mes)

df_clima = pd.DataFrame({
    "fecha": fechas_inicio,
    "precipitacion_mm": precip,
    "temperatura_c": temp
})

df_clima.to_csv("datos/clima_mensual.csv", index=False)
print(f"   ✓ {len(fechas_inicio)} meses de datos climáticos")

# ==============================================================================
# 4. ARCHIVO: secado.csv
# ==============================================================================
print("📊 Generando secado.csv...")

# Parámetros del modelo de Page: MR = exp(-k·t^n)
k_page = 0.001 + (semilla % 10000) * (0.005 / 10000)
n_page = 0.5 + (semilla % 5) * (1.0 / 5)

# Tiempo de secado: 0 a 300 minutos, cada 15 minutos
tiempo = np.arange(0, 315, 15)
MR = []

for t in tiempo:
    if t == 0:
        mr = 1.0
    else:
        mr = np.exp(-k_page * t**n_page)
    
    # Agregar ruido pequeño (lognormal)
    mr_ruido = mr * np.exp(rng.normal(0, 0.05))
    mr_ruido = np.clip(mr_ruido, 0.01, 1.0)  # Entre 0.01 y 1
    MR.append(mr_ruido)

df_secado = pd.DataFrame({
    "tiempo_min": tiempo,
    "MR": MR
})

df_secado.to_csv("datos/secado.csv", index=False)
print(f"   ✓ {len(tiempo)} tiempos de secado simulados")

# ==============================================================================
# 5. ARCHIVOS: Muestras pequeñas
# ==============================================================================
print("📊 Generando muestras pequeñas...")

# 5.1 muestra_eda10.csv: 10 parcelas incluyendo 1 atípico
idx_muestra_eda = rng.choice(n_parcelas, 10, replace=False)
df_eda10 = df_parcelas.iloc[idx_muestra_eda][["parcela", "suelo", "riego", "rendimiento"]].copy()
df_eda10 = df_eda10.reset_index(drop=True)
df_eda10.to_csv("datos/muestra_eda10.csv", index=False)

# 5.2 muestra_dist10.csv: 10 años de precipitación máxima
idx_muestra_dist = rng.choice(len(df_precip), 10, replace=False)
df_dist10 = df_precip.iloc[idx_muestra_dist].copy()
df_dist10 = df_dist10.reset_index(drop=True)
df_dist10.to_csv("datos/muestra_dist10.csv", index=False)

# 5.3 muestra_reg8.csv: 8 parcelas sin atípicos repartidas por lamina_riego
df_para_reg = df_parcelas.copy()
# Ordenar por lámina de riego y dividir en 8 grupos
df_para_reg = df_para_reg.sort_values("lamina_riego").reset_index(drop=True)
# Usar qcut para 8 grupos iguales
df_para_reg["grupo"] = pd.qcut(df_para_reg["lamina_riego"], q=8, labels=False, duplicates="drop")
# Tomar una parcela por grupo (la primera de cada grupo)
df_reg8 = df_para_reg.groupby("grupo", as_index=False).first()[["parcela", "lamina_riego", "rendimiento"]]
df_reg8 = df_reg8.head(8).copy()
df_reg8 = df_reg8.reset_index(drop=True)
df_reg8.to_csv("datos/muestra_reg8.csv", index=False)

# 5.4 muestra_series24.csv: 24 meses de 2024-2025
df_series24 = df_clima[df_clima["fecha"].dt.year >= 2024].copy()
df_series24["periodo"] = range(1, len(df_series24) + 1)
df_series24["anio"] = df_series24["fecha"].dt.year
df_series24["mes"] = df_series24["fecha"].dt.month
df_series24["conjunto"] = ["entrenamiento"] * 18 + ["validacion"] * (len(df_series24) - 18)
df_series24 = df_series24[["periodo", "fecha", "anio", "mes", "precipitacion_mm", "conjunto"]]
df_series24.to_csv("datos/muestra_series24.csv", index=False)

print(f"   ✓ muestra_eda10.csv (10 parcelas)")
print(f"   ✓ muestra_dist10.csv (10 años)")
print(f"   ✓ muestra_reg8.csv (8 parcelas para regresión)")
print(f"   ✓ muestra_series24.csv (24 meses de 2024-2025)")

# ==============================================================================
# 6. ARCHIVO: metadatos.json
# ==============================================================================
print("📊 Generando metadatos.json...")

# Calcular huella (primeros 8 caracteres en mayúscula del MD5)
suma_rendimiento = df_parcelas["rendimiento"].sum()
huella_input = f"{CODIGO_ESTUDIANTIL}|{n_parcelas}|{suma_rendimiento:.2f}"
huella_md5 = hashlib.md5(huella_input.encode()).hexdigest()[:8].upper()

metadatos = {
    "codigo": CODIGO_ESTUDIANTIL,
    "nombre": NOMBRES_APELLIDOS,
    "cultivo": CULTIVO_ELEGIDO,
    "municipio": MUNICIPIO_ELEGIDO,
    "n_parcelas": int(n_parcelas),
    "huella": huella_md5,
    "fecha_generacion": datetime.now().isoformat(),
    "semilla": int(semilla)
}

with open("datos/metadatos.json", "w", encoding="utf-8") as f:
    json.dump(metadatos, f, indent=2, ensure_ascii=False)

print(f"   ✓ metadatos.json guardado")

# ==============================================================================
# 7. RESUMEN Y VERIFICACIÓN
# ==============================================================================
print("\n" + "="*70)
print("RESUMEN DE GENERACIÓN")
print("="*70)

print(f"\n👤 ESTUDIANTE:")
print(f"   Nombre:   {NOMBRES_APELLIDOS}")
print(f"   Código:   {CODIGO_ESTUDIANTIL}")
print(f"   Cultivo:  {CULTIVO_ELEGIDO}")
print(f"   Municipio: {MUNICIPIO_ELEGIDO}")
print(f"   Huella:   {huella_md5}")

print(f"\n📁 ARCHIVOS GENERADOS EN datos/:")
print(f"   1. parcelas.csv ({n_parcelas} parcelas)")
print(f"   2. precip_max_anual.csv (40 años: 1986-2025)")
print(f"   3. clima_mensual.csv (132 meses: 2015-2025)")
print(f"   4. secado.csv (21 tiempos: 0-300 min)")
print(f"   5. muestra_eda10.csv (10 parcelas)")
print(f"   6. muestra_dist10.csv (10 años)")
print(f"   7. muestra_reg8.csv (8 parcelas)")
print(f"   8. muestra_series24.csv (24 meses)")
print(f"   9. metadatos.json (metadatos)")

# ==============================================================================
# 8. MOSTRAR MUESTRAS PEQUEÑAS
# ==============================================================================
print("\n" + "="*70)
print("MUESTRAS PEQUEÑAS (para cálculo manual)")
print("="*70)

print("\n📋 muestra_eda10.csv (10 parcelas para EDA):")
print(df_eda10.to_string(index=False))

print("\n📋 muestra_dist10.csv (10 años para distribuciones):")
print(df_dist10.to_string(index=False))

print("\n📋 muestra_reg8.csv (8 parcelas para regresión):")
print(df_reg8.to_string(index=False))

print("\n📋 muestra_series24.csv (24 meses para series de tiempo):")
print(df_series24.to_string(index=False))

print("\n" + "="*70)
print("✅ Generación completada exitosamente")
print("="*70 + "\n")
