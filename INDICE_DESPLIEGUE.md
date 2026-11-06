# Índice de Documentación: Despliegue en Streamlit Cloud

**Estudiante:** Justo Fuentes (6820995)  
**Fecha:** 2026-11-06

---

## 📚 Documentos de Despliegue

### 1. **EXPLICACION_DESPLIEGUE.md** (11 KB) ← **EMPIEZA AQUÍ**

**¿Qué es?** Explicación completa en español de todo lo que se preparó.

**Contenido:**
- ✅ Revisión de `requirements.txt`
- ✅ Creación de `runtime.txt` (Python 3.11.7)
- ✅ Actualización de `.streamlit/config.toml`
- ✅ Por qué `app.py` funciona en Cloud
- ✅ Solución del problema AutoTS lentitud
- ✅ 6 errores comunes + soluciones
- ✅ 5 pasos para desplegar
- ✅ Resumen ejecutivo

**👉 Usar cuando:** Quieras entender qué se preparó y por qué.

---

### 2. **DESPLIEGUE_CHECKLIST.md** (3.3 KB) ← **RÁPIDO Y PRÁCTICO**

**¿Qué es?** Resumen ejecutivo con checklist rápido.

**Contenido:**
- ✅ Archivos preparados (tabla)
- ✅ Status de módulos
- ✅ 5 pasos resumidos (copy-paste ready)
- ✅ Problemas comunes con soluciones rápidas
- ✅ Links a documentación

**👉 Usar cuando:** Necesites hacer el despliegue rápidamente.

---

### 3. **GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md** (14 KB) ← **MÁS DETALLADO**

**¿Qué es?** Guía técnica completa con todos los detalles.

**Contenido:**
- ✅ Verificación de `requirements.txt` línea por línea
- ✅ Cómo crear `runtime.txt`
- ✅ Configuración de `.streamlit/config.toml`
- ✅ Despliegue paso a paso
- ✅ Verificación en la nube (página por página)
- ✅ Gestión de AutoTS (3 opciones diferentes)
- ✅ 6 errores comunes + soluciones detalladas
- ✅ Monitoreo y mantenimiento en Cloud
- ✅ Actualizaciones automáticas
- ✅ Apéndices técnicos

**👉 Usar cuando:** Necesites más detalles o solucionar un error específico.

---

## 🎯 ¿POR DÓNDE EMPIEZO?

**Flujo recomendado:**

1. **Leer:** `EXPLICACION_DESPLIEGUE.md` (10 min)
   → Entiende qué se preparó y por qué

2. **Hacer:** `DESPLIEGUE_CHECKLIST.md` (20 min)
   → Ejecuta los 5 pasos del despliegue

3. **Consultar (si falla):** `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`
   → Soluciona problemas específicos

---

## 📋 Archivos de Configuración Creados/Actualizados

| Archivo | Tipo | Tamaño | ¿Qué Hace? |
|---------|------|--------|----------|
| `runtime.txt` | Config | 14 bytes | Especifica Python 3.11.7 para Cloud |
| `requirements-prod.txt` | Config | 435 bytes | Dependencias sin pytest (opcional) |
| `.streamlit/config.toml` | Config | 368 bytes | Seguridad + tema + límites (ACTUALIZADO) |
| `README.md` | Doc | +300 bytes | Sección "App en línea" agregada |

---

## ✅ Verificación: ¿Está Todo Listo?

```
✅ app.py importa desde src/ correctamente
✅ requirements.txt tiene todas las librerías
✅ runtime.txt especifica Python 3.11.7
✅ .streamlit/config.toml tiene seguridad
✅ Todos los módulos importan sin errores
✅ Datos en datos/ están intactos (READ-ONLY)
✅ 3 guías de despliegue completas
✅ Checklist de 5 pasos listo

🚀 LISTO PARA DESPLEGAR
```

---

## 🚀 Los 5 Pasos Resumidos

### **PASO 1:** Sube a GitHub
```bash
git add runtime.txt .streamlit/config.toml README.md
git commit -m "Preparación para despliegue en Streamlit Cloud"
git push origin main
```

### **PASO 2:** Ve a Streamlit Cloud
🔗 https://share.streamlit.io → Sign in with GitHub

### **PASO 3:** Crea nueva app
- Click "New app"
- Repository: `justorfc/app-estadistica-aplicada-2026-2`
- Branch: `main`
- Main file: `app.py`

### **PASO 4:** Deploy
- Click "Deploy"
- Espera 3-5 minutos

### **PASO 5:** Tu app está en línea
- URL: `https://<algo>.streamlit.app`
- Actualiza el README con tu enlace

---

## ⚠️ Problema Principal: AutoTS Lentitud

**El problema:** Generar pronósticos en Cloud tarda demasiado (10+ minutos).

**La solución (RECOMENDADA):**

```bash
# 1. Genera localmente (una sola vez)
.venv/bin/streamlit run app.py
# → Ve a Series de Tiempo → Genera pronósticos
# → Espera 2-5 minutos

# 2. Sube resultados a GitHub
git add resultados/
git commit -m "Pronósticos precalculados"
git push

# 3. En Cloud: lectura instantánea (sin AutoTS)
```

**Resultado:** Página de Series carga en 2 segundos en Cloud.

Más detalles en `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md` (Sección 4).

---

## 🎓 Para Presentar Tu Proyecto

**Enlace a compartir:**
```
Aquí va tu app: https://<nombre-tu-app>.streamlit.app
```

**Información técnica:**
- Alojado en Streamlit Community Cloud (gratuito)
- Despliega automáticamente desde GitHub
- Ejecuta Python 3.11.7 + 20 librerías
- Actualiza en tiempo real con tus cambios

---

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| ❌ "ModuleNotFoundError: src" | Ver `EXPLICACION_DESPLIEGUE.md`, sección "Error 1" |
| ❌ "FileNotFoundError: datos/" | Ver `EXPLICACION_DESPLIEGUE.md`, sección "Error 2" |
| ❌ AutoTS muy lentitud | Ver `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`, sección 4 |
| ❌ Timeout en Cloud | Usa pronósticos precalculados (ver arriba) |
| ❌ MemoryError | Limita muestra a 5000 obs (ver guía) |
| ✅ La app está lenta | Revisa logs en https://share.streamlit.io/your-app |

---

## 🎯 Próximas Acciones

1. **Ahora:** Lee `EXPLICACION_DESPLIEGUE.md` (10 min)
2. **Luego:** Sigue los 5 pasos en `DESPLIEGUE_CHECKLIST.md`
3. **Después:** Prueba la app en Cloud (5 min)
4. **Finalmente:** Comparte tu enlace 🎉

---

## 📊 Resumen de Recursos

| Recurso | Líneas | Enfoque | Tiempo |
|---------|--------|---------|--------|
| `EXPLICACION_DESPLIEGUE.md` | 300 | Conceptual + Paso a Paso | 10 min |
| `DESPLIEGUE_CHECKLIST.md` | 100 | Ejecutable + Rápido | 5 min |
| `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md` | 400 | Técnico + Detallado | 20 min |

**Total:** 800 líneas de documentación cobriendo cada aspecto.

---

**¡Adelante con tu despliegue! 🚀**

*Si tienes preguntas, consulta las guías o los logs de Cloud.*

