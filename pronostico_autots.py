"""
Script de pronóstico automático con AutoTS.

Ejecuta AutoTS para encontrar el mejor modelo de pronóstico de precipitación,
similar a un ensayo de evaluación de variedades agrícolas donde:
- Las "generaciones" son ciclos de siembra y selección
- Los "modelos" son diferentes variedades de cultivo
- Las "validaciones" son cosechas de prueba (backtesting)

Uso: .venv/bin/python pronostico_autots.py
"""

import json
import pandas as pd
from pathlib import Path
from src.series import cargar_serie, ejecutar_autots

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

# Leer código del estudiante desde metadatos.json
# (Como un identificador único de la "parcela" experimental)
ruta_metadata = Path("metadatos.json")
with open(ruta_metadata, 'r') as f:
    metadata = json.load(f)

# Extraer código y convertir a semilla (como código de variedad)
codigo_estudiante = int(metadata.get("codigo", "6820995"))
semilla = codigo_estudiante % 10000  # Mantener entre 0-9999

# Definir parámetros del experimento (como un protocolo agrícola)
horizonte_pronostico = 12  # Pronosticar 12 meses adelante
model_list = "superfast"   # Modelos rápidos pero buenos
generaciones = 5           # 5 ciclos de selección genética
validaciones = 2           # 2 períodos de backtesting
intervalo_confianza = 0.9  # 90% de confianza

# Crear carpeta de resultados si no existe
carpeta_resultados = Path("resultados")
carpeta_resultados.mkdir(exist_ok=True)

print("=" * 70)
print("PRONÓSTICO AUTOMÁTICO CON AutoTS - ENSAYO DE VARIEDADES")
print("=" * 70)
print()
print("📋 CONFIGURACIÓN DEL EXPERIMENTO")
print("-" * 70)
print(f"Código de estudiante (semilla): {codigo_estudiante} → {semilla}")
print(f"Variable: precipitación (mm)")
print(f"Período de datos: 2015-2025")
print(f"Horizonte de pronóstico: {horizonte_pronostico} meses")
print(f"Conjunto de modelos: {model_list} (variedades rápidas pero buenas)")
print(f"Generaciones de selección: {generaciones} ciclos evolutivos")
print(f"Validaciones hacia atrás: {validaciones} cosechas de prueba")
print(f"Intervalo de confianza: {int(intervalo_confianza*100)}%")
print()

# ============================================================================
# PASO 1: CARGAR SERIE DE PRECIPITACIÓN
# ============================================================================

print("1️⃣  CARGANDO SERIE DE PRECIPITACIÓN (2015-2025)")
print("-" * 70)

# Cargar serie histórica desde datos/clima_mensual.csv
# (Como obtener datos históricos de rendimiento de una variedad)
serie_precip = cargar_serie("precipitacion_mm")

print(f"✓ Serie cargada: {len(serie_precip)} observaciones mensuales")
print(f"  Período: {serie_precip.index[0].date()} a {serie_precip.index[-1].date()}")
print(f"  Valores: min={serie_precip.min():.1f}mm, "
      f"media={serie_precip.mean():.1f}mm, max={serie_precip.max():.1f}mm")
print()

# ============================================================================
# PASO 2: EJECUTAR AUTOTS (PROCESO DE SELECCIÓN GENÉTICA)
# ============================================================================

print("2️⃣  EJECUTANDO AutoTS - EVALUACIÓN Y SELECCIÓN DE MODELOS")
print("-" * 70)
print("AutoTS está evaluando múltiples 'variedades' de modelos en un proceso")
print("de selección genética artificial. Esto puede tardar de 1 a 4 minutos...")
print()

# Ejecutar AutoTS
# (Como simular múltiples generaciones de cultivo con evaluación de cada una)
resultado_autots = ejecutar_autots(
    serie=serie_precip,
    horizonte=horizonte_pronostico,
    model_list=model_list,
    generaciones=generaciones,
    validaciones=validaciones,
    intervalo=intervalo_confianza,
    semilla=semilla
)

print("✓ AutoTS completó la evaluación y selección de variedades")
print()

# ============================================================================
# PASO 3: MOSTRAR RESULTADOS DEL MEJOR MODELO
# ============================================================================

print("3️⃣  RESULTADOS - MEJOR MODELO SELECCIONADO")
print("-" * 70)

# Extraer información del mejor modelo
nombre_modelo = resultado_autots['modelo_nombre']
params_modelo = resultado_autots['modelo_params']
trans_modelo = resultado_autots['modelo_transformaciones']

# Mostrar ganador (como anunciar la variedad ganadora de un concurso)
print(f"🏆 MODELO GANADOR: {nombre_modelo}")
print(f"   (Es la 'variedad' que mostró mejor desempeño en la evaluación)")
print()
print(f"Parámetros: {params_modelo}")
print(f"Transformaciones aplicadas: {trans_modelo}")
print()

# ============================================================================
# PASO 4: MOSTRAR TOP 10 MODELOS
# ============================================================================

print("4️⃣  TOP 10 MODELOS - RANKING DE VARIEDADES")
print("-" * 70)
print("(Como una tabla de resultados de un concurso de variedades)")
print()

# Obtener tabla de top 10
top_10 = resultado_autots['top_10_modelos'].copy()

# Mostrar tabla con posiciones
for idx, row in top_10.iterrows():
    posicion = idx + 1
    modelo = row['Model']
    smape = row['smape']
    mae = row['mae']
    rmse = row['rmse']
    score = row['Score']
    
    # Decorador especial para ganador y SeasonalNaive
    prefijo = ""
    if posicion == 1:
        prefijo = "🏆 "
    elif "SeasonalNaive" in str(modelo):
        prefijo = "📊 "
    
    print(f"{prefijo}{posicion:2d}. {modelo:25s} | "
          f"SMAPE: {smape:8.4f} | MAE: {mae:8.4f} | "
          f"RMSE: {rmse:8.4f} | Score: {score:8.4f}")

print()

# Buscar posición de SeasonalNaive
posicion_seasonal = None
for idx, row in top_10.iterrows():
    if "SeasonalNaive" in str(row['Model']):
        posicion_seasonal = idx + 1
        break

if posicion_seasonal:
    print(f"📊 SeasonalNaive (nuestro benchmark) está en posición #{posicion_seasonal}")
else:
    print(f"📊 SeasonalNaive no está en el top 10 (fue superado por AutoTS)")
print()

# ============================================================================
# PASO 5: MOSTRAR PRONÓSTICOS
# ============================================================================

print("5️⃣  PRONÓSTICOS PARA LOS PRÓXIMOS 12 MESES")
print("-" * 70)

# Obtener pronósticos
df_pronostico = resultado_autots['pronostico'].copy()

# Mostrar pronósticos con intervalos
for idx, row in df_pronostico.iterrows():
    fecha = row['fecha'].strftime('%Y-%m-%d')
    pron = row['pronostico_mm']
    inf = row['limite_inferior_mm']
    sup = row['limite_superior_mm']
    
    # Gráfico ASCII simple
    ancho = 40
    pct = (pron - inf) / (sup - inf) if sup > inf else 0.5
    pct = max(0, min(1, pct))
    pos = int(pct * ancho)
    
    barra = "█" * pos + "░" * (ancho - pos)
    
    print(f"{fecha}: {pron:6.1f}mm [{barra}] {inf:.1f}-{sup:.1f}mm")

print()

# ============================================================================
# PASO 6: GUARDAR RESULTADOS
# ============================================================================

print("6️⃣  GUARDANDO RESULTADOS EN CARPETA 'resultados/'")
print("-" * 70)

# 1. Guardar pronósticos (con fecha y límites)
ruta_pronostico = carpeta_resultados / "autots_pronostico.csv"
df_pronostico.to_csv(ruta_pronostico, index=False)
print(f"✓ Pronósticos guardados: {ruta_pronostico.name}")

# 2. Guardar top 10 modelos
ruta_top10 = carpeta_resultados / "autots_top10_modelos.csv"
top_10.to_csv(ruta_top10, index=False)
print(f"✓ Top 10 guardado: {ruta_top10.name}")

# 3. Guardar información del mejor modelo
info_mejor_modelo = {
    "nombre_modelo": nombre_modelo,
    "parametros": str(params_modelo),
    "transformaciones": str(trans_modelo),
    "horizonte": horizonte_pronostico,
    "generaciones": generaciones,
    "validaciones": validaciones,
    "intervalo_confianza": intervalo_confianza,
    "semilla": semilla,
    "codigo_estudiante": codigo_estudiante,
    "datos": {
        "observaciones": len(serie_precip),
        "fecha_inicio": str(serie_precip.index[0]),
        "fecha_fin": str(serie_precip.index[-1]),
        "precip_min_mm": float(serie_precip.min()),
        "precip_media_mm": float(serie_precip.mean()),
        "precip_max_mm": float(serie_precip.max())
    },
    "posicion_seasonal_naive": posicion_seasonal if posicion_seasonal else "No en top 10"
}

ruta_mejor_modelo = carpeta_resultados / "autots_mejor_modelo.json"
with open(ruta_mejor_modelo, 'w') as f:
    json.dump(info_mejor_modelo, f, indent=2)
print(f"✓ Mejor modelo guardado: {ruta_mejor_modelo.name}")

print()
print("=" * 70)
print("✅ EXPERIMENTO COMPLETADO - ARCHIVOS GUARDADOS EN 'resultados/'")
print("=" * 70)
