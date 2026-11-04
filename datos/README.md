# Carpeta de Datos - Estadística Aplicada

**⚠️ IMPORTANTE: Esta carpeta contiene datos personalizados. NO MODIFICAR NI COMPROMETER EN GIT**

## Descripción

Estos datos fueron generados automáticamente por `generar_datos.py` usando el código estudiantil como semilla. Esto garantiza que:

1. **Reproducibilidad**: Misma semilla = mismos datos
2. **Unicidad**: Cada estudiante tiene datos diferentes
3. **Consistencia**: Los datos son estables para todo el análisis

## Archivos Generados

### Archivos Principales (4)

| Archivo | Registros | Propósito |
|---------|-----------|----------|
| **parcelas.csv** | 116 | Datos de cultivo con rendimiento, dosis de N, riego, pH, materia orgánica. Incluye 2 outliers intencionales y 3 valores faltantes. |
| **precip_max_anual.csv** | 40 | Precipitación máxima anual en 24 horas (1986-2025) simulada con distribución Gumbel. Base para análisis de eventos extremos. |
| **clima_mensual.csv** | 132 | Datos climáticos mensuales (2015-2025): precipitación con régimen bimodal caribeño y temperatura con tendencia. |
| **secado.csv** | 21 | Razón de humedad (MR) en secado de capa delgada: modelo de Page MR = exp(-k·t^n). |

### Muestras Pequeñas para Cálculo Manual (4)

| Archivo | Registros | Uso |
|---------|-----------|-----|
| **muestra_eda10.csv** | 10 | 10 parcelas para análisis exploratorio (incluye 1 atípico) |
| **muestra_dist10.csv** | 10 | 10 años aleatorios para ajuste de distribuciones |
| **muestra_reg8.csv** | 8 | 8 parcelas distribuidas por lámina de riego para regresión |
| **muestra_series24.csv** | 24 | 24 meses de 2024-2025 (18 entrenamiento, 6 validación) |

### Metadatos (1)

| Archivo | Contenido |
|---------|-----------|
| **metadatos.json** | Código, nombre, cultivo, municipio, número de parcelas, huella única (hash MD5 de personalización) |

## Especificaciones Técnicas

### parcelas.csv
- **Columnas**: parcela, suelo, riego, dosis_N, lamina_riego, materia_organica, ph, rendimiento
- **Tipos**:
  - `parcela`: string (P001...P116)
  - `suelo`: categorical (Franco, Arcilloso, Arenoso)
  - `riego`: categorical (Sí, No)
  - `dosis_N`, `lamina_riego`, `ph`, `rendimiento`: float64
  - `materia_organica`: float64 (con 3 NaN propositales)

### precip_max_anual.csv
- **Columnas**: anio, pmax24h_mm
- **Distribución**: Gumbel (μ≈85 mm, β≈15 mm)
- **Asimetría**: 0.87 (típica de Gumbel para máximos)

### clima_mensual.csv
- **Columnas**: fecha, precipitacion_mm, temperatura_c
- **Régimen**: Bimodal caribeño
  - Lluvias: abril-mayo, septiembre-noviembre (~206 mm/mes)
  - Secas: diciembre-marzo (~56 mm/mes)
- **Temperatura**: 27°C ± 1.5°C con tendencia +0.02°C/año

### secado.csv
- **Columnas**: tiempo_min, MR
- **Modelo**: MR = exp(-k·t^n), donde k y n dependen de la semilla
- **Rango MR**: 0.93 a 1.00 (humedad desde ~93% hasta 100% al inicio)

### muestra_series24.csv
- **Columnas adicionales**: periodo, anio, mes, conjunto
- **Conjunto**: "entrenamiento" (primeros 18 meses), "validacion" (últimos 6)

## Características Especiales Incluidas

### En parcelas.csv
- ✅ Relaciones no-lineales entre variables y rendimiento
- ✅ 2 parcelas atípicas (1 muy alta, 1 muy baja)
- ✅ 3 valores faltantes en materia_organica (propositales para enseñanza)
- ✅ Balanceo: suelo ~30-40 cada uno, riego ~50-50

### En clima_mensual.csv
- ✅ Régimen bimodal caribeño realista
- ✅ Tendencia de temperatura (cambio climático)
- ✅ Ruido lognormal en precipitación

### En muestra_reg8.csv
- ✅ Distribuidas uniformemente por lámina de riego (usando pd.qcut)
- ✅ Sin outliers (para facilitar regresión lineal simple)

### En muestra_series24.csv
- ✅ División entrenamiento/validación (75/25)
- ✅ Régimen bimodal visible en los 24 meses

## No Modificar

- ❌ Cambiar valores en archivos CSV
- ❌ Eliminar archivos
- ❌ Agregar columnas
- ❌ Modificar generar_datos.py
- ❌ Comprometer en Git (están en .gitignore)

## Regenerar (si es necesario)

```bash
.venv/bin/python generar_datos.py
```

Esto regenerará todos los archivos con la misma semilla, produciendo idénticos resultados.

## Contacto

Si hay problemas con los datos, ejecuta nuevamente:
```bash
.venv/bin/python generar_datos.py
```

---

**Generado**: 2026-11-04  
**Estudiante**: Justo Fuentes (6820995)  
**Cultivo**: Ñame  
**Municipio**: Sincelejo  
**Huella**: 43DA0A2A
