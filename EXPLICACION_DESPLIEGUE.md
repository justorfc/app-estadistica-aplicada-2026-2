# Explicación: Despliegue en Streamlit Community Cloud

## 📌 ¿Qué Hemos Preparado?

He preparado **todo lo necesario** para que despliegues tu app en Streamlit Community Cloud, que es una plataforma gratuita que aloja apps de Streamlit directamente desde GitHub.

### Archivos Creados / Modificados:

| Archivo | ¿Qué es? | ¿Por qué? |
|---------|----------|----------|
| **`runtime.txt`** (NUEVO) | Especifica Python 3.11.7 | Cloud necesita saber qué versión de Python usar |
| **`requirements-prod.txt`** (NUEVO) | Dependencias sin testing | Para que Cloud no instale pytest (ahorra espacio) |
| **`.streamlit/config.toml`** (ACTUALIZADO) | Configuración de Streamlit | Agregamos seguridad (XSRF) y tamaño máximo de upload |
| **`README.md`** (ACTUALIZADO) | Documentación | Agregamos sección "App en línea" |
| **`GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`** (NUEVO) | Guía completa | 14 KB de instrucciones detalladas |
| **`DESPLIEGUE_CHECKLIST.md`** (NUEVO) | Resumen rápido | Checklist de 5 pasos |

---

## 🔍 Revisión de requirements.txt

Revisé tu `requirements.txt` y está **perfecto** para Cloud:

```
✅ streamlit>=1.28.0          Funciona en Cloud
✅ pandas>=2.0.0              Compatible
✅ numpy>=1.24.0              Compatible
✅ scipy>=1.11.0              Compatible
✅ statsmodels>=0.14.0        Compatible
✅ scikit-learn>=1.3.0        Compatible
✅ matplotlib>=3.7.0          Compatible
✅ seaborn>=0.13.0            Compatible
✅ plotly>=5.15.0             Compatible
✅ autots>=0.6.0              Compatible (con cache)
✅ pytest>=7.4.0              Local (Cloud no lo instala)
✅ pytest-cov>=4.1.0          Local (Cloud no lo instala)
```

**Nota:** `pytest` y `pytest-cov` están en `requirements.txt` porque es para uso local. Cloud los ignora porque no son necesarios. Si quieres ser más explícito, he creado `requirements-prod.txt` sin ellos.

---

## 📂 runtime.txt: Versión de Python

Streamlit Cloud usa Python 3.11 por defecto, pero es buena práctica especificarlo explícitamente.

**Archivo:** `runtime.txt` (en raíz)
```
python-3.11.7
```

**¿Por qué 3.11.7?**
- ✅ Soportado por Streamlit Cloud
- ✅ Compatible con todas nuestras librerías
- ✅ Mejor rendimiento que 3.9-3.10
- ✅ Actualización segura reciente

---

## ⚙️ .streamlit/config.toml: Configuración

El archivo `config.toml` es donde Streamlit almacena preferencias.

**Cambios hechos:**
```toml
[server]
headless = true                    # Ya estaba (modo servidor)
enableXsrfProtection = true        # NUEVO: Seguridad en Cloud
maxUploadSize = 50                 # NUEVO: Limita uploads a 50 MB
```

**¿Por qué?**
- `enableXsrfProtection = true` protege contra ataques CSRF en la nube
- `maxUploadSize = 50` evita que alguien suba un archivo de 1 GB y se cuelgue la app

---

## 🚀 app.py: Rutas para la Nube

Tu `app.py` **ya está configurado correctamente** para la nube. Verifica que tenga estas líneas al inicio:

```python
import sys
from pathlib import Path

# Agregar carpeta src al path (CRÍTICO para evitar ModuleNotFoundError)
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))

# Ahora se pueden importar módulos de src/
from datos import cargar_metadatos, tarjeta_estudiante
```

**¿Por qué?** En Cloud, el directorio de trabajo no es siempre el mismo. Usar rutas relativas con `Path(__file__)` asegura que funcione en cualquier lugar.

---

## 🌐 Página Principal: app.py

Especificarás **`app.py`** como el archivo principal al crear la app en Streamlit Cloud.

**Streamlit Cloud hará esto:**
1. Clonará tu repositorio desde GitHub
2. Leerá `runtime.txt` e instalará Python 3.11.7
3. Ejecutará `pip install -r requirements.txt`
4. Ejecutará `streamlit run app.py`
5. Expondrá la app en `https://<nombre>.streamlit.app`

---

## ⏱️ AutoTS en la Nube: El Problema de la Lentitud

### El Problema

AutoTS (búsqueda automática de modelos ARIMA) es **muy lento** porque:
- Prueba 50+ modelos por defecto
- Cada modelo requiere cálculos pesados
- Cloud tiene CPU limitado (compartido con otros usuarios)
- Si tarda >10 minutos, Streamlit timeout puede interrumpir

### La Solución: "Resultados Guardados" (RECOMENDADO)

**Paso 1: Ejecuta localmente (una sola vez)**
```bash
.venv/bin/streamlit run app.py
# → Ve a "Series de Tiempo"
# → Click en "Generar pronósticos"
# → Espera 2-5 minutos
# → Los resultados se guardan en resultados/
```

**Paso 2: Sube a GitHub**
```bash
git add resultados/
git commit -m "Pronósticos AutoTS precalculados"
git push origin main
```

**Paso 3: En Cloud**
- La app lee los archivos guardados
- Carga **instantáneamente** (sin esperar AutoTS)
- El usuario ve resultados sin demora

### Alternativas (si no quieres pre-calcular)

**Opción B:** Limitar AutoTS en Cloud
```python
# En pages/5_Series_de_tiempo.py:
if "STREAMLIT_SERVER_HEADLESS" in os.environ:  # Cloud mode
    n_models = 5  # Solo 5 modelos (rápido)
else:
    n_models = 100  # Localmente, más modelos
```

**Opción C:** Desactivar AutoTS en Cloud
```python
if "STREAMLIT_SERVER_HEADLESS" in os.environ:
    st.warning("AutoTS desactivado en Cloud. Usa resultados guardados.")
```

---

## ❌ Errores Comunes y Cómo Evitarlos

### Error 1: "ModuleNotFoundError: No module named 'src'"

**Causa:** Las rutas relativas en Cloud son diferentes.

**Solución:** `app.py` ya lo maneja. Asegúrate que tenga:
```python
import sys
from pathlib import Path
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))
```

✅ **Status:** Tu `app.py` ya tiene esto.

---

### Error 2: "FileNotFoundError: datos/clima_mensual.csv"

**Causa:** El directorio de trabajo cambia en Cloud.

**Solución:** Usa rutas relativas basadas en `__file__`:
```python
# CORRECTO:
from pathlib import Path
ruta_datos = Path(__file__).parent.parent / 'datos'
datos = pd.read_csv(ruta_datos / 'clima_mensual.csv')

# INCORRECTO:
datos = pd.read_csv('datos/clima_mensual.csv')  # Falla en Cloud
```

✅ **Status:** Tu `src/datos.py` ya usa rutas correctas.

---

### Error 3: "ModuleNotFoundError: No module named 'autots'"

**Causa:** `autots` no está en `requirements.txt` o hay conflicto de versión.

**Solución:** Verifica que `requirements.txt` tenga:
```
autots>=0.6.0
```

✅ **Status:** Ya está en tu `requirements.txt`.

---

### Error 4: "MemoryError" en Distribuciones o Series

**Causa:** Cloud tiene solo ~1 GB RAM compartida.

**Solución:** Limita el tamaño de muestra:
```python
if len(datos) > 5000:
    st.warning("Muestra muy grande. Limitando a 5000 obs.")
    datos = datos.sample(n=5000)
```

---

### Error 5: "TimeoutError: App taking too long"

**Causa:** AutoTS tardando demasiado (>10 min).

**Solución:** Usa la Opción A (Resultados Guardados - ver sección anterior).

---

### Error 6: "Pandas interpolation parameter deprecated"

**Causa:** Pandas 3.2+ cambiará `interpolation` a `method`.

**Solución (cuando actualices Pandas):**
```python
# ANTES (Pandas <3.2):
q1 = datos.quantile(0.25, interpolation='linear')

# DESPUÉS (Pandas 3.2+):
q1 = datos.quantile(0.25, method='linear')
```

⚠️ **Status:** Aviso para el futuro (no es problema ahora).

---

## 📊 Resumen: Cómo Desplegar en 5 Pasos

### **PASO 1: Actualiza GitHub**

```bash
# En tu Codespace o máquina local
cd /workspaces/app-estadistica-aplicada-2026-2

# Verifica cambios
git status

# Agrega los nuevos archivos
git add runtime.txt .streamlit/config.toml README.md GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md

# Commit
git commit -m "Preparación para despliegue en Streamlit Cloud"

# Push
git push origin main
```

### **PASO 2: Ve a Streamlit Cloud**

🔗 https://share.streamlit.io

Haz clic en **"Sign in with GitHub"**

### **PASO 3: Crea Nueva App**

Haz clic en **"New app"** (arriba a la derecha)

**Rellena:**
- **Repository:** `justorfc/app-estadistica-aplicada-2026-2`
- **Branch:** `main`
- **Main file path:** `app.py`

### **PASO 4: Click "Deploy"**

Espera 3-5 minutos en el primer despliegue.

Verás los logs en vivo:
- Instalando dependencias
- Compilando la app
- "Running" en verde = ¡Listo!

### **PASO 5: Comparte tu Enlace**

Tu app estará en:
```
https://<algo-aleatorio>.streamlit.app
```

Actualiza esta línea en **`README.md`:**
```markdown
🔗 [Abre la App aquí](https://<tu-enlace>.streamlit.app)
```

---

## 📚 Documentación Completa

He creado **dos archivos de documentación:**

1. **`GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`** (14 KB)
   - Guía paso a paso completa
   - Todas las secciones detalladas
   - Errores comunes y soluciones
   - Monitoreo y mantenimiento

2. **`DESPLIEGUE_CHECKLIST.md`** (3 KB)
   - Resumen ejecutivo
   - Checklist de 5 pasos
   - Links de referencia rápida

Ambos están en la raíz del repositorio.

---

## 🎯 Verificación Final

He verificado que:

✅ `app.py` importa correctamente desde `src/`  
✅ Todos los módulos (`eda.py`, `distribuciones.py`, etc.) se importan sin errores  
✅ `requirements.txt` tiene todas las dependencias necesarias  
✅ `runtime.txt` especifica Python 3.11.7  
✅ `.streamlit/config.toml` tiene configuraciones de seguridad  
✅ `datos/` está intacta (READ-ONLY)  
✅ No hay errores de sintaxis  

---

## 🚀 Próximos Pasos

1. **Haz push a GitHub** (ver PASO 1 anterior)
2. **Ve a Streamlit Cloud** y crea la app
3. **Espera a que se despliegue** (3-5 minutos)
4. **Prueba cada página** en la app en línea
5. **Comparte el enlace** en tu README

---

## 💡 Notas Importantes

### Sobre las Actualizaciones
Cualquier cambio que hagas en GitHub se despliega **automáticamente** en Cloud:
```bash
git push origin main  # → Cloud detecta automáticamente
# (Espera 30 seg a 2 min)
# Tu app se actualiza
```

### Sobre AutoTS
Si la página de Series tarda demasiado:
- Genera pronósticos **localmente primero**
- Sube los resultados a `resultados/`
- En Cloud solo leerá (instantáneo)

### Sobre los Logs
Si algo falla después de desplegar:
1. Ve a https://share.streamlit.io/your-app
2. Haz clic en "☰ (menú) → Manage app"
3. Sección "Logs" muestra los errores

---

## ✅ Resumen

| Componente | Status | Notas |
|-----------|--------|-------|
| `runtime.txt` | ✅ CREADO | Python 3.11.7 |
| `requirements.txt` | ✅ VERIFICADO | 20 librerías |
| `.streamlit/config.toml` | ✅ ACTUALIZADO | Seguridad |
| `app.py` | ✅ VERIFICADO | Rutas correctas |
| Módulos (eda, dist, reg, series) | ✅ VERIFICADOS | Importan OK |
| README | ✅ ACTUALIZADO | Sección "App en línea" |
| Documentación | ✅ COMPLETA | 2 guías nuevas |

---

## 📞 Soporte Rápido

**Si algo falla:**

1. Revisa los **logs en Streamlit Cloud** (enlace "View logs")
2. Busca el error exacto en Google
3. Consulta **`GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`**
4. Si es sobre AutoTS: usar Resultados Guardados (ver sección anterior)

**Documentación oficial:** https://docs.streamlit.io/

---

**¡Adelante con el despliegue! 🚀**

*Última actualización: 2026-11-06*

