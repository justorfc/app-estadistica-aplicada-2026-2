# 🚀 Guía Rápida - Verificación de Cálculos

## En 5 Minutos

### 1️⃣ Ejecutar Scripts Python (desde terminal)
```bash
cd /workspaces/app-estadistica-aplicada-2026-2

# Uno a uno
.venv/bin/python verificacion/verificar_eda.py
.venv/bin/python verificacion/verificar_distribuciones.py
.venv/bin/python verificacion/verificar_regresion.py
.venv/bin/python verificacion/verificar_series.py

# O todos en una línea
for f in eda distribuciones regresion series; do 
  echo "Ejecutando $f..."; 
  .venv/bin/python verificacion/verificar_$f.py; 
  echo "---"; 
done
```

### 2️⃣ Ejecutar Scripts R (en Posit Cloud)
1. Ve a https://posit.cloud
2. Abre una consola R
3. Copia y pega cada script .R
4. Ejecuta línea por línea

### 3️⃣ Completar Plantilla
Abre [RESULTADOS.md](RESULTADOS.md) y llena las 4 tablas con:
- Columna "A mano": Tus cálculos manuales (opcional)
- Columna "Python": Resultados de verificar_*.py
- Columna "R": Resultados de verificar_*.R
- Columna "App": Resultados de la aplicación Streamlit
- Columna "¿Coincide?": Sí/No

## ✨ Resultados Clave

### EDA
```
Media: 8.9245
Mediana: 8.9465
Varianza: 2.8793
Q1: 7.5636, Q3: 10.4336
Atípicos: 0
```

### Distribuciones
```
μ Gumbel: 72.9269
β Gumbel: 11.8905
x₁₀: 99.6849 mm
x₅₀: 119.3229 mm
x₁₀₀: 127.6250 mm
Riesgo (T=50, N=25): 39.65%
```

### Regresión
```
Ecuación: ŷ = 16.8804 - 0.0328×x
R²: 0.1272
Significancia: NO (p=0.3858)
IC 95% b₁: [-0.1187, 0.0531]
```

### Series
```
PM3₁₈: 118.8530 mm
Ganador: Estacional Ingenuo
SMAPE: 9.6943%
Suma índices: 13.0486 ≈ 12
```

## 🔍 ¿Qué Buscar?

| Diferencia | Causa probable | Acción |
|------------|-----------------|--------|
| < 0.0001  | Redondeo | Aceptar |
| 0.0001-0.001 | Método diferente | Revisar |
| > 0.01    | Error en cálculo | Investigar |

## 📝 Checklist

- [ ] Ejecuté verificar_eda.py
- [ ] Ejecuté verificar_distribuciones.py
- [ ] Ejecuté verificar_regresion.py
- [ ] Ejecuté verificar_series.py
- [ ] Copié resultados a RESULTADOS.md
- [ ] Ejecuté los scripts .R en Posit Cloud
- [ ] Completé toda la plantilla
- [ ] Revisé diferencias
- [ ] Entiendo todos los cálculos
- [ ] Confío en la app ✅

## 📚 Archivos

| Archivo | Propósito |
|---------|-----------|
| verificar_eda.py | Análisis descriptivo (13 medidas) |
| verificar_distribuciones.py | Weibull y Gumbel (8 medidas) |
| verificar_regresion.py | Regresión lineal (14 medidas) |
| verificar_series.py | Series de tiempo (13 medidas) |
| verificar_*.R | Equivalentes en R |
| RESULTADOS.md | Plantilla para completar |
| README.md | Documentación completa |
| SALIDA_SCRIPTS.txt | Resumen de resultados |

## 🎯 Objetivo Final

Tener **4 fuentes de cálculos** (A mano, Python, R, App) que coincidan entre sí, demostrando que:
1. ✅ Entiendes cada fórmula
2. ✅ La implementación es correcta
3. ✅ La app es confiable

---

**¡Que disfrutes verificando!** 📊✨

