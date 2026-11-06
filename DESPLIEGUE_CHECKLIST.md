# Despliegue en Streamlit Cloud: Checklist Rápido

**Estudiante:** Justo Fuentes (6820995)

---

## ✅ Archivos Preparados

He preparado todo lo necesario para desplegar tu app en Streamlit Cloud:

| Archivo | Acción | Status |
|---------|--------|--------|
| `runtime.txt` | **CREADO** con `python-3.11.7` | ✅ LISTO |
| `requirements.txt` | Verificado y optimizado | ✅ LISTO |
| `.streamlit/config.toml` | Actualizado con seguridad | ✅ LISTO |
| `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md` | Guía completa paso a paso | ✅ LISTO |
| `README.md` | Agregada sección "App en línea" | ✅ LISTO |

---

## 🚀 Resumen: Cómo Desplegar en 5 Pasos

### 1. Sube los cambios a GitHub

```bash
git add runtime.txt .streamlit/config.toml README.md
git commit -m "Preparación para despliegue en Streamlit Cloud"
git push origin main
```

### 2. Ve a Streamlit Cloud

🔗 https://share.streamlit.io → Sign in with GitHub

### 3. Crea nueva app

- Click en **"New app"**
- **Repository:** `justorfc/app-estadistica-aplicada-2026-2`
- **Branch:** `main`
- **Main file path:** `app.py`

### 4. Click "Deploy" y espera

- Espera 3-5 minutos en el primer despliegue
- Verás los logs en vivo
- Cuando cambie a "Running" (verde), ¡está listo!

### 5. Comparte tu enlace

Tu app estará en:
```
https://<nombre-tu-app>.streamlit.app
```

Actualiza esta línea en el **README.md:**
```markdown
🔗 [Abre la App aquí](https://share.streamlit.io/justorfc/app-estadistica-aplicada-2026-2)
```

---

## ⚠️ Problemas Comunes (Soluciones Rápidas)

### Error: "ModuleNotFoundError: No module named 'src'"
✅ **Solución:** `app.py` ya lo arregla. Si sigue fallando, checa que `app.py` tenga:
```python
import sys
from pathlib import Path
ruta_src = Path(__file__).parent / 'src'
sys.path.insert(0, str(ruta_src))
```

### Error: "FileNotFoundError: datos/clima_mensual.csv"
✅ **Solución:** Checa que `src/datos.py` use rutas relativas con `Path(__file__)`

### Error: "ModuleNotFoundError: No module named 'autots'"
✅ **Solución:** Verifica que `requirements.txt` tenga `autots>=0.6.0`

### Página de Series de Tiempo muy lenta
✅ **Solución:** Genera pronósticos localmente:
```bash
.venv/bin/streamlit run app.py
# → Ve a Series de Tiempo → Genera pronósticos
# → Guarda resultado en resultados/
# → git push
```

En Cloud, la app leerá los resultados guardados (instantáneo).

---

## 📚 Documentación Completa

Para más detalles, consulta **`GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`**:

1. ✅ Verificación de `requirements.txt`
2. ✅ Creación de `runtime.txt` (ya hecho)
3. ✅ Configuración de `.streamlit/config.toml` (ya hecho)
4. ✅ Despliegue paso a paso
5. ✅ Gestión de AutoTS en la nube
6. ✅ Errores comunes y soluciones
7. ✅ Monitoreo y mantenimiento

---

## 📞 Resumen de Tu Situación

✅ **requirements.txt:** Optimizado (streamlit, pandas, scipy, statsmodels, autots, etc.)  
✅ **Python:** 3.11.7 especificado en `runtime.txt`  
✅ **app.py:** Ya usa rutas correctas para Cloud  
✅ **Datos:** Guardados en `datos/` (Cloud los clona)  
✅ **Seguridad:** `.streamlit/config.toml` actualizado (XSRF activado)

**Próximo paso:** Sube los cambios a GitHub y crea la app en Streamlit Cloud.

**Tiempo estimado:** 20 minutos (5 min setup + 15 min esperar despliegue)

---

**Éxito en tu despliegue! 🚀**

