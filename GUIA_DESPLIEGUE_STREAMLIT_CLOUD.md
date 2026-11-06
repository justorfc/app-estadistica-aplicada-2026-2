# Guía Completa: Desplegar en Streamlit Community Cloud

**Estudiante:** Justo Fuentes (6820995)  
**Última actualización:** 2026-11-06

---

## Índice

1. [Preparación Inicial](#1-preparación-inicial)
2. [Paso a Paso: Despliegue](#2-paso-a-paso-despliegue)
3. [Verificación en la Nube](#3-verificación-en-la-nube)
4. [Gestión de AutoTS en la Nube](#4-gestión-de-autots-en-la-nube)
5. [Errores Comunes y Soluciones](#5-errores-comunes-y-soluciones)
6. [Monitoreo y Mantenimiento](#6-monitoreo-y-mantenimiento)

---

## 1. Preparación Inicial

### 1.1 Verifica requirements.txt

El archivo `requirements.txt` ha sido optimizado para la nube:

```
# Streamlit y UI
streamlit>=1.28.0              ← Compatible con Cloud

# Manipulación de datos
pandas>=2.0.0                   ← Stable, ampliamente soportado
numpy>=1.24.0                   ← Compatible con pandas 2.0+
openpyxl>=3.0.0                 ← Para lectura de Excel

# Estadística y distribuciones
scipy>=1.11.0                   ← Stable
statsmodels>=0.14.0             ← Compatible con scipy 1.11+
scikit-learn>=1.3.0             ← Usado en regresión/distribuciones

# Gráficas
matplotlib>=3.7.0               ← Stable
seaborn>=0.13.0                 ← Depende de matplotlib 3.7+
plotly>=5.15.0                  ← Para gráficas interactivas

# Pronóstico automático
autots>=0.6.0                   ← ⚠️ CRÍTICO: versión con caché

# Testing (NO se instala en Cloud, solo local)
pytest>=7.4.0
pytest-cov>=4.1.0
```

**✅ STATUS:** requirements.txt ya está optimizado para Cloud.

**Nota sobre Testing:** Pytest y pytest-cov se instalan solo localmente. Para evitar que Cloud intente instalarlos:

```bash
# requirements.txt actual está bien (Cloud los ignora si no los usa)
# Pero si quieres ser explícito, puedes crear:
# - requirements-dev.txt  (con pytest, pytest-cov)
# - requirements.txt (solo producción)
```

### 1.2 Crea runtime.txt

Streamlit Cloud usa Python por defecto, pero es buena práctica especificar la versión:

**Archivo:** `runtime.txt` (en la raíz del repositorio)

```
python-3.11.7
```

**¿Por qué 3.11?**
- ✅ Soportado por Streamlit Cloud
- ✅ Compatible con todas nuestras librerías
- ✅ Mejor rendimiento que 3.9-3.10
- ✅ Actualización reciente (seguridad)

**Alternativas válidas:**
- `python-3.12.0` (más nuevo, pero puede tener librerías con issues)
- `python-3.10.13` (más estable, pero más lento)

**✅ ACCIÓN:** Crear `runtime.txt` con `python-3.11.7`

### 1.3 Verifica .streamlit/config.toml

El archivo `config.toml` ya existe. Revisa que contenga:

```toml
[theme]
primaryColor = "#2d5016"        # Verde agrícola
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true         # Útil en desarrollo

[logger]
level = "info"
```

**Para Cloud, agregar:**

```toml
[server]
maxUploadSize = 50              # MB (por defecto 200)
enableXsrfProtection = true     # Seguridad
```

---

## 2. Paso a Paso: Despliegue

### Prerequisitos

✅ Cuenta en GitHub (tu repositorio `justorfc/app-estadistica-aplicada-2026-2`)  
✅ Cuenta en [Streamlit Community Cloud](https://share.streamlit.io)  
✅ Cambios locales guardados y pushed a GitHub

### Paso 1: Asegura que GitHub esté actualizado

```bash
# En tu Codespace o máquina local
cd /workspaces/app-estadistica-aplicada-2026-2

# Verifica estado
git status

# Si hay cambios pendientes, commítelos
git add -A
git commit -m "Preparación para despliegue en Streamlit Cloud"
git push origin main
```

### Paso 2: Inicia sesión en Streamlit Cloud

1. Ve a https://share.streamlit.io
2. Haz clic en **"Sign in with GitHub"**
3. Autoriza Streamlit para acceder a tu repositorio
4. Si es la primera vez, GitHub te pedirá permisos

### Paso 3: Crea una nueva app

1. En Streamlit Cloud, haz clic en **"New app"** (arriba a la derecha)

2. **Llena los campos:**
   - **Repository:** `justorfc/app-estadistica-aplicada-2026-2`
   - **Branch:** `main` (o la rama que despliegues)
   - **Main file path:** `app.py` ← **CRÍTICO**

3. Haz clic en **"Deploy"**

### Paso 4: Espera el despliegue

Streamlit Cloud:
- ✅ Clonará tu repositorio
- ✅ Leerá `runtime.txt` → instalará Python 3.11.7
- ✅ Ejecutará `pip install -r requirements.txt`
- ✅ Ejecutará `streamlit run app.py`
- ✅ Expondrá la app en `https://<nombre-tu-app>.streamlit.app`

**Tiempo esperado:** 3-5 minutos en el primer despliegue (después ~30 seg)

### Paso 5: Verifica los logs

Durante el despliegue:
- **"Running"** (naranja) = Instalando dependencias
- **"Running"** (verde) = App activa
- **"Error"** = Problema (revisa los logs)

Haz clic en **"View logs"** para ver detalles si algo falla.

---

## 3. Verificación en la Nube

Una vez que la app esté en línea, verifica cada página:

### 3.1 Página Principal (Home)
- ✅ Tarjeta del estudiante visible
- ✅ Descripción del proyecto legible
- ✅ Navegación en sidebar funciona

### 3.2 Página 1: Datos
- ✅ Carga datos desde `datos/` sin errores
- ✅ Muestra tabla de datos completa
- ✅ Descarga en Excel funciona

### 3.3 Página 2: EDA
- ✅ Gráficas se renderean (histograma, box plot)
- ✅ Tabla de resumen numérico visible
- ✅ Sin errores de carga de datos

### 3.4 Página 3: Distribuciones
- ✅ Tabla comparativa se calcula
- ✅ Gráficas Q-Q plots se muestran
- ✅ Cuantiles de retorno se calculan
- ⚠️ **PUEDE SER LENTO en Cloud (ver sección 4)**

### 3.5 Página 4: Regresión
- ✅ Modelo se ajusta sin errores
- ✅ Gráficos de diagnóstico visibles
- ✅ Predicción en nuevas parcelas funciona

### 3.6 Página 5: Series de Tiempo
- ✅ Descomposición se calcula
- ✅ Gráficas de componentes visibles
- ⚠️ **PUEDE SER LENTO si AutoTS genera (ver sección 4)**

---

## 4. Gestión de AutoTS en la Nube

### El Problema

AutoTS (búsqueda automática de modelos ARIMA/ETS) es **muy lento en Cloud** porque:
- Requiere muchos cálculos (genera 50+ modelos por defecto)
- Cloud tiene CPU limitado
- Timeout de Streamlit Cloud = 24 horas (pero la app se refresca si llega a ~10 min)

### La Solución: Usar "Resultados Guardados"

#### Opción A: Calcular Localmente y Guardar (RECOMENDADO)

**En tu Codespace/máquina local:**

```bash
# 1. Ejecuta la app localmente
.venv/bin/streamlit run app.py

# 2. Ve a la página de "Series de Tiempo"
# 3. En el sidebar, selecciona "Generar pronósticos"
# 4. Espera a que AutoTS termine (puede tardar 2-5 minutos localmente)
# 5. Los resultados se guardan automáticamente en resultados/

# 6. Verifica que se creó:
ls -la resultados/
# Debe mostrar archivos como: pronostico_autots_*.csv
```

**Después, en Cloud:**
- Cuando se carga la página de Series, lee los archivos guardados
- **No regenera** AutoTS (solo muestra resultados)
- Es **instantáneo** (~2 segundos)

#### Opción B: Limitar Generaciones en Cloud

Si quieres que Cloud genere pronósticos (pero rápidamente):

**En `pages/5_Series_de_tiempo.py`, modifica:**

```python
# ANTES:
n_models = 100  # AutoTS prueba 100 modelos

# DESPUÉS (para Cloud):
n_models = 5    # AutoTS prueba solo 5 modelos (rápido)
```

**Trade-off:**
- ✅ Rápido (1-2 minutos en Cloud)
- ❌ Pronósticos menos optimizados

#### Opción C: Desactivar AutoTS en Cloud

Si quieres que Cloud no genere nada:

```python
# En pages/5_Series_de_tiempo.py:

if st.sidebar.checkbox("Generar pronósticos (AutoTS)"):
    # Verificar si estamos en Cloud
    import streamlit as st
    if "STREAMLIT_SERVER_HEADLESS" in os.environ:  # Cloud mode
        st.warning("⚠️ AutoTS desactivado en Cloud. Usa resultados guardados.")
        st.info("Genera pronósticos localmente y sube a GitHub.")
    else:  # Modo local
        # Ejecutar AutoTS normalmente
        ...
```

### ✅ RECOMENDACIÓN FINAL

**Usa la Opción A (Resultados Guardados):**

1. **Localmente** (una sola vez):
   ```bash
   .venv/bin/streamlit run app.py
   # → Genera pronósticos → se guardan en resultados/
   git add resultados/
   git commit -m "Pronósticos AutoTS precalculados"
   git push
   ```

2. **En Cloud** (siempre rápido):
   - La app lee resultados guardados
   - Carga en 2 segundos
   - Sin timeout

---

## 5. Errores Comunes y Soluciones

### Error 1: "ModuleNotFoundError: No module named 'src'"

**Síntoma:** App falla al iniciar, error en importaciones de `src/`

**Causa:** Las rutas relativas no funcionan igual en Cloud

**Solución:** El archivo `app.py` ya incluye esto:

```python
import sys
from pathlib import Path

ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))
```

**✅ Verificación:** Si sigue fallando, revisa que `app.py` tenga estas líneas al inicio.

---

### Error 2: "FileNotFoundError: datos/clima_mensual.csv"

**Síntoma:** No encuentra archivos en la carpeta `datos/`

**Causa:** En Cloud, `os.getcwd()` apunta a otra carpeta

**Solución (EN CADA MÓDULO):**

```python
# ANTES (INCORRECTO):
datos = pd.read_csv('datos/clima_mensual.csv')

# DESPUÉS (CORRECTO):
from pathlib import Path
ruta_datos = Path(__file__).parent.parent / 'datos'  # Sube 2 niveles
datos = pd.read_csv(ruta_datos / 'clima_mensual.csv')
```

**Estado actual:** Los módulos `src/datos.py` ya usan rutas relativas correctas.

**✅ Verificación:**
```bash
grep -n "Path(__file__)" src/datos.py
# Debe mostrar líneas con rutas relativas
```

---

### Error 3: "ModuleNotFoundError: No module named 'autots'"

**Síntoma:** Cloud dice que autots no está instalado

**Causa:** No está en requirements.txt o hay incompatibilidad

**Solución:**

```bash
# Verifica que requirements.txt tenga:
grep autots requirements.txt
# Debe mostrar: autots>=0.6.0

# Si no está, agrégalo:
echo "autots>=0.6.0" >> requirements.txt
git add requirements.txt
git commit -m "Agregar autots a requirements"
git push
```

---

### Error 4: "MemoryError" en Distribuciones o Series

**Síntoma:** La app se cuelga cuando calculas con muchas muestras

**Causa:** Cloud tiene 1 GB RAM compartida entre múltiples usuarios

**Solución:**

En `pages/3_Distribuciones.py`:
```python
# Limita el tamaño de la muestra en Cloud
n_mc_max = 5000  # Si n > 5000, avisar al usuario
if n_datos > n_mc_max:
    st.warning(f"⚠️ Muestra muy grande. Usando {n_mc_max} obs.")
    datos = datos.sample(n=n_mc_max)
```

---

### Error 5: "TimeoutError: App is taking too long"

**Síntoma:** La app no responde en más de 5 minutos

**Causa:** AutoTS o cálculos pesados tardando demasiado

**Solución:** Usa la **Opción A de la Sección 4** (Resultados Guardados)

---

### Error 6: "Pandas interpolation parameter deprecated"

**Síntoma:** Advertencia sobre `interpolation='linear'` en cuantiles

**Causa:** Pandas 3.2+ cambió a `method='linear'`

**Solución (cuando actualices Pandas):**

```python
# ANTES:
q1 = datos.quantile(0.25, interpolation='linear')

# DESPUÉS:
q1 = datos.quantile(0.25, method='linear')
```

---

## 6. Monitoreo y Mantenimiento

### 6.1 Actualizar la App en la Nube

Cualquier cambio que hagas localmente y pushes a GitHub se **despliega automáticamente** en Cloud.

```bash
# Flujo normal:
git add cambios
git commit -m "Descripción del cambio"
git push origin main

# Cloud detecta el push automáticamente
# Espera 30 segundos a 2 minutos
# Tu app se actualiza
```

### 6.2 Revisar Logs en Cloud

Si algo falla después de un despliegue:

1. Ve a https://share.streamlit.io/your-username/app-name
2. Haz clic en **"☰" (menú) → Manage app"**
3. En la sección **"Logs"**, verás:
   - Errores de instalación de dependencias
   - Errores de ejecución (ImportError, etc.)
   - Avisos de rendimiento

### 6.3 Redesplegrar Manualmente

Si deseas forzar un redesplegue sin cambios:

1. Ve a https://share.streamlit.io/your-username/app-name
2. Haz clic en **"☰ (menú) → Reboot app"**
3. La app se reinicia en ~1 minuto

### 6.4 Monitoreo de Recursos

Streamlit Cloud te permite ver:
- **CPU usage:** Si sube a >80%, es que algo está lento
- **Memory usage:** Si llega a 100%, la app falla
- **Disk usage:** No es problema (tenemos espacio)

**Si ves problemas:**
- Reduce tamaño de muestra (datos/)
- Limita iteraciones de AutoTS
- Cachea resultados (usar `@st.cache_data`)

---

## Resumen de Archivos Necesarios

| Archivo | Ubicación | Status | Acción |
|---------|-----------|--------|--------|
| `app.py` | Raíz | ✅ Existe | Asegura que `sys.path` apunte a `src/` |
| `requirements.txt` | Raíz | ✅ Existe | Verifica versiones (OK) |
| `runtime.txt` | Raíz | ⚠️ Crear | Crea con `python-3.11.7` |
| `.streamlit/config.toml` | Carpeta `.streamlit/` | ✅ Existe | Asegura que tenga temas y configs |
| `datos/` | Raíz | ✅ Existe | NO modificar, Cloud lo clona |
| `src/` | Raíz | ✅ Existe | Todas las importaciones usan rutas relativas |
| `pages/` | Raíz | ✅ Existe | Todas las páginas cargan bien |

---

## Checklist Final Antes de Desplegar

- [ ] `git status` muestra "nothing to commit, working tree clean"
- [ ] `git push origin main` completado sin errores
- [ ] `runtime.txt` creado con `python-3.11.7`
- [ ] `requirements.txt` revisado (sin librerías innecesarias)
- [ ] `.streamlit/config.toml` existe y tiene tema
- [ ] `app.py` importa desde `src/` usando `sys.path`
- [ ] Todas las páginas cargan localmente sin errores: `.venv/bin/streamlit run app.py`
- [ ] Tests pasan: `.venv/bin/pytest tests/ -v`
- [ ] Pronósticos AutoTS pre-generados (opcional pero recomendado)

---

## Soporte y Troubleshooting

**Si algo falla en Cloud:**

1. **Revisa los logs:** Haz clic en "View logs" en https://share.streamlit.io
2. **Búsqueda en Google:** "streamlit error: <mensaje>"
3. **Documentación oficial:** https://docs.streamlit.io/knowledge-base/using-streamlit/deploy-streamlit-app

**Preguntas frecuentes:**

- **¿Puedo usar una BD en Cloud?** Sí, con SQLite (local) o PostgreSQL (remoto)
- **¿Puedo guardar archivos en Cloud?** Sí, en carpeta temporal; pero se pierden al reiniciar
- **¿Cuánto cuesta?** Gratis en Community Cloud (con límites de CPU)
- **¿Puedo usar un dominio personalizado?** Sí (con pago en Streamlit Cloud Pro)

---

**Fin de la guía.**

Próximo paso: Crea `runtime.txt` y ejecuta el checklist.

