# Verificación de Cálculos - RESULTADOS

**Estudiante:** Justo Fuentes (Código: 6820995)  
**Asignatura:** Estadística Aplicada 2026-2  
**Fecha de cálculo:** [Completar]

---

## 📊 1. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
**Muestra:** `muestra_eda10.csv`

| Medida | A mano | Python | R | App | ¿Coincide? |
|--------|--------|--------|---|-----|-----------|
| Media | | | | | ☐ Sí ☐ No |
| Mediana | | | | | ☐ Sí ☐ No |
| Varianza (S²) | | | | | ☐ Sí ☐ No |
| Desv. Estándar (S) | | | | | ☐ Sí ☐ No |
| CV (%) | | | | | ☐ Sí ☐ No |
| Q1 (tipo 7) | | | | | ☐ Sí ☐ No |
| Q3 (tipo 7) | | | | | ☐ Sí ☐ No |
| RIC | | | | | ☐ Sí ☐ No |
| Valla inferior | | | | | ☐ Sí ☐ No |
| Valla superior | | | | | ☐ Sí ☐ No |
| Atípicos (cantidad) | | | | | ☐ Sí ☐ No |
| Media riego=Sí | | | | | ☐ Sí ☐ No |
| Media riego=No | | | | | ☐ Sí ☐ No |

### Observaciones EDA:
- Cálculos coinciden: ☐ Totalmente ☐ Parcialmente ☐ No coinciden
- Diferencias encontradas:
  
  [Completar]

---

## 📈 2. DISTRIBUCIONES PROBABILÍSTICAS
**Muestra:** `muestra_dist10.csv`

| Medida | A mano | Python | R | App | ¿Coincide? |
|--------|--------|--------|---|-----|-----------|
| Posición Weibull (F₁) | | | | | ☐ Sí ☐ No |
| T empírico (T₁) | | | | | ☐ Sí ☐ No |
| μ Gumbel (momentos) | | | | | ☐ Sí ☐ No |
| β Gumbel (momentos) | | | | | ☐ Sí ☐ No |
| x₁₀ (T=10 años) | | | | | ☐ Sí ☐ No |
| x₅₀ (T=50 años) | | | | | ☐ Sí ☐ No |
| x₁₀₀ (T=100 años) | | | | | ☐ Sí ☐ No |
| Riesgo (T=50, N=25) | | | | | ☐ Sí ☐ No |

### Observaciones Distribuciones:
- Cálculos coinciden: ☐ Totalmente ☐ Parcialmente ☐ No coinciden
- MLE vs Momentos: [Comparar resultados de R con Python]
- Diferencias encontradas:
  
  [Completar]

---

## 📉 3. REGRESIÓN LINEAL SIMPLE
**Muestra:** `muestra_reg8.csv` (lámina de riego vs rendimiento)

| Medida | A mano | Python | R | App | ¿Coincide? |
|--------|--------|--------|---|-----|-----------|
| Sxx | | | | | ☐ Sí ☐ No |
| Syy | | | | | ☐ Sí ☐ No |
| Sxy | | | | | ☐ Sí ☐ No |
| r (Pearson) | | | | | ☐ Sí ☐ No |
| ρ (Spearman) | | | | | ☐ Sí ☐ No |
| b₀ | | | | | ☐ Sí ☐ No |
| b₁ | | | | | ☐ Sí ☐ No |
| SCE | | | | | ☐ Sí ☐ No |
| R² | | | | | ☐ Sí ☐ No |
| RSE | | | | | ☐ Sí ☐ No |
| SE(b₁) | | | | | ☐ Sí ☐ No |
| t | | | | | ☐ Sí ☐ No |
| Decisión (α=0.05) | | | | | ☐ Sí ☐ No |
| IC 95% para b₁ | | | | | ☐ Sí ☐ No |

### Observaciones Regresión:
- Cálculos coinciden: ☐ Totalmente ☐ Parcialmente ☐ No coinciden
- ¿Significativa la relación? ☐ Sí ☐ No
- Diferencias encontradas:
  
  [Completar]

---

## ⏱️ 4. SERIES DE TIEMPO
**Muestra:** `muestra_series24.csv` (18 entrenamiento + 6 validación)

| Medida | A mano | Python | R | App | ¿Coincide? |
|--------|--------|--------|---|-----|-----------|
| PM3 (t=18) | | | | | ☐ Sí ☐ No |
| Índice mes 1 | | | | | ☐ Sí ☐ No |
| Índice mes 6 | | | | | ☐ Sí ☐ No |
| Índice mes 12 | | | | | ☐ Sí ☐ No |
| Suma de índices | | | | | ☐ Sí ☐ No |
| MAE (Ingenuo) | | | | | ☐ Sí ☐ No |
| RMSE (Est. Ingenuo) | | | | | ☐ Sí ☐ No |
| SMAPE (Promedio) | | | | | ☐ Sí ☐ No |
| Método ganador | | | | | ☐ Sí ☐ No |

### Observaciones Series:
- Cálculos coinciden: ☐ Totalmente ☐ Parcialmente ☐ No coinciden
- Mejor método: [Completar]
- Diferencias encontradas:
  
  [Completar]

---

## 🔍 PREGUNTAS DE REFLEXIÓN

### ¿Se cumplió mi predicción previa?

**Antes de ejecutar los cálculos, ¿esperabas que coincidieran?**
- ☐ Sí, esperaba que todo coincidiera
- ☐ Parcialmente, con pequeñas diferencias de redondeo
- ☐ No estaba seguro
- ☐ Otra: [Completar]

**¿Se cumplió?**
- ☐ Sí, exactamente como esperaba
- ☐ Hay pequeñas diferencias que son aceptables
- ☐ No, encontré discrepancias importantes

---

## 📋 DIFERENCIAS ENCONTRADAS Y SU CAUSA

### Diferencias de Redondeo
(Son normales y aceptables si son < 0.0001)

| Tema | Python | R | App | Causa probable |
|------|--------|---|-----|-----------------|
| [Completar] | | | | Precisión de punto flotante |
| [Completar] | | | | Método de cálculo diferente |

### Diferencias Importantes
(Revisar fórmulas si la diferencia es > 0.0001)

| Tema | Python | R | App | Causa investigada |
|------|--------|---|-----|------------------|
| [Completar] | | | | [Completar] |
| [Completar] | | | | [Completar] |

---

## ✅ CONCLUSIÓN GENERAL

**Resumen de la verificación:**
- Total de medidas verificadas: ___
- Coincidencias totales: ___
- Coincidencias parciales: ___
- Discrepancias: ___

**¿La app está correcta?**
- ☐ Sí, todos los cálculos son correctos
- ☐ Sí, con pequeñas diferencias de redondeo esperadas
- ☐ No, hay errores que corregir
- ☐ Revisar (especificar cuál)

**Cálculos confiables para:**
- ☐ EDA
- ☐ Distribuciones
- ☐ Regresión
- ☐ Series de Tiempo

---

## 📝 Notas finales

[Espacio para notas adicionales del estudiante]

---

**Completado por:** ___________________  
**Fecha:** ___________________
