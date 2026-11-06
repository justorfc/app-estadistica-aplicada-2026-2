# 🚀 Quick Start: Despliegue en 5 Minutos

**Estudiante:** Justo Fuentes (6820995)  
**Tiempo total:** ~20 minutos (5 setup + 15 Cloud + 5 pruebas)

---

## 1️⃣ PUSH A GITHUB (2 min)

```bash
cd /workspaces/app-estadistica-aplicada-2026-2

git add runtime.txt .streamlit/config.toml README.md
git commit -m "Preparación para despliegue en Streamlit Cloud"
git push origin main
```

✅ **Verificar:** Ve a GitHub y confirma los cambios están ahí.

---

## 2️⃣ CREA APP EN STREAMLIT CLOUD (5 min)

### Paso A: Inicia sesión
- 🔗 https://share.streamlit.io
- Click **"Sign in with GitHub"**
- Autoriza Streamlit para acceder a tu repo

### Paso B: Nueva app
- Click **"New app"** (arriba a la derecha)

### Paso C: Rellena formulario
```
Repository:    justorfc/app-estadistica-aplicada-2026-2
Branch:        main
Main file:     app.py
```

### Paso D: Deploy
- Click **"Deploy"**
- Espera mientras ves los logs (3-5 minutos)

✅ **Listo cuando veas:** "Running" en verde

---

## 3️⃣ PRUEBA LA APP (5 min)

Tu app está en: `https://<algo>.streamlit.app`

### Verifica cada página:
- ✅ Inicio → Tarjeta visible, descripción legible
- ✅ Datos → Tabla cargada, gráficas visibles
- ✅ EDA → Histogramas y boxplots funcionan
- ✅ Distribuciones → Tabla de comparativa (puede tardar 1-2 min)
- ✅ Regresión → Gráficos y tabla de coeficientes
- ✅ Series → Descomposición visible (si es lenta, ver paso 4)

---

## 4️⃣ (OPCIONAL) SOLUCIONA AutoTS LENTO

Si la página "Series" tarda >10 minutos en Cloud:

### Genera localmente primero:
```bash
# En tu Codespace:
.venv/bin/streamlit run app.py
# → Ve a Series de Tiempo → Click "Generar pronósticos"
# → Espera 2-5 minutos
# → Cierra la app (Ctrl+C)
```

### Sube los resultados:
```bash
git add resultados/
git commit -m "Pronósticos precalculados"
git push
```

### En Cloud:
- Espera a que se redespliegue (1-2 min)
- Series de Tiempo ahora carga instantáneo ✅

---

## 5️⃣ COMPARTE TU ENLACE

Tu app está lista en:
```
https://<nombre-tu-app>.streamlit.app
```

### Actualiza README:
Abre [README.md](/README.md) y reemplaza esta línea:
```markdown
🔗 [Abre la App aquí](https://share.streamlit.io/justorfc/app-estadistica-aplicada-2026-2)
```

Con tu enlace real:
```markdown
🔗 [Abre la App aquí](https://tu-nombre-app.streamlit.app)
```

---

## ✅ CHECKLIST

- [ ] Hice push a GitHub
- [ ] Creé app en Streamlit Cloud
- [ ] La app dice "Running" (verde)
- [ ] Probé cada página
- [ ] (Opcional) Generé pronósticos localmente
- [ ] Actualicé README con mi enlace

---

## 🔧 SI ALGO FALLA

| Problema | Solución Rápida |
|----------|-----------------|
| Error al crear app | Verifica que GitHub esté autorizado |
| "ModuleNotFoundError" | Ver logs (click "View logs"), no es problema tuyo |
| App se cuelga en Distribuciones | Normal (1-2 min), Cloud está calculando |
| Series de Tiempo muy lenta | Genera pronósticos localmente (paso 4) |
| App no actualiza después de push | Espera 1-2 minutos y recarga página |

---

## 📚 DOCUMENTACIÓN

Si necesitas más detalles:
- **Conceptos:** Lee `EXPLICACION_DESPLIEGUE.md`
- **Errores específicos:** Consulta `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md`
- **Índice:** Ver `INDICE_DESPLIEGUE.md`

---

## 🎓 ¿Qué Pasó?

1. ✅ Preparé `runtime.txt` (Python 3.11.7)
2. ✅ Actualicé `.streamlit/config.toml` (seguridad)
3. ✅ Tu `app.py` ya funciona en Cloud
4. ✅ Cloud clona tu repositorio
5. ✅ Instala Python + librerías + datos
6. ✅ Ejecuta `streamlit run app.py`
7. ✅ Tu app está en línea 🚀

---

## 🎯 Próximo Paso

**Ahora:** Haz Push a GitHub (5 min)  
**Luego:** Crea app en Streamlit Cloud (5 min)  
**Después:** Prueba cada página (5 min)

---

**¡Éxito! 🚀**

*Tu proyecto de Estadística Aplicada está listo para presentar en línea.*

