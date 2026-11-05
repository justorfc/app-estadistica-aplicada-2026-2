# Verificación EDA - muestra_eda10.csv
# Script de R para análisis exploratorio con fórmulas explícitas
# Usar en Posit Cloud (posit.cloud)
# Nota: No requiere librerías externas

# Instrucciones de instalación:
# En Posit Cloud, todas las funciones base están disponibles

# ============================================================================
# 1. CARGA DE DATOS
# ============================================================================

# Leer el archivo CSV
datos <- read.csv('datos/muestra_eda10.csv')
print("Datos cargados:")
print(datos)

# Extraer la variable de análisis (rendimiento)
x <- datos$rendimiento
n <- length(x)

cat("\nn =", n, "\n")
cat("Datos:", round(x, 4), "\n\n")

# ============================================================================
# 2. ESTADÍSTICOS DESCRIPTIVOS
# ============================================================================

cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n")
cat("VERIFICACIÓN EDA - muestra_eda10.csv\n")
cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n\n")

# Media
media <- mean(x)
cat("1️⃣  MEDIA\n")
cat("   media =", round(media, 4), "\n\n")

# Mediana
mediana <- median(x)
cat("2️⃣  MEDIANA\n")
cat("   mediana =", round(mediana, 4), "\n\n")

# Varianza (muestral)
varianza <- var(x)  # Por defecto usa n-1
cat("3️⃣  VARIANZA (S²)\n")
cat("   S² =", round(varianza, 4), "\n\n")

# Desviación estándar
desv_est <- sd(x)  # Por defecto usa n-1
cat("4️⃣  DESVIACIÓN ESTÁNDAR (S)\n")
cat("   S =", round(desv_est, 4), "\n\n")

# Coeficiente de variación
cv <- (desv_est / media) * 100
cat("5️⃣  COEFICIENTE DE VARIACIÓN (CV)\n")
cat("   CV =", round(cv, 4), "%\n\n")

# Cuartiles (R usa el método 7 por defecto, equivalente a QUARTILE.INC de Excel)
q1 <- quantile(x, 0.25, type = 7)
q3 <- quantile(x, 0.75, type = 7)
cat("6️⃣  CUARTILES (tipo 7)\n")
cat("   Q1 =", round(q1, 4), "\n")
cat("   Q3 =", round(q3, 4), "\n\n")

# Rango Intercuartílico
ric <- q3 - q1
cat("7️⃣  RANGO INTERCUARTÍLICO (RIC)\n")
cat("   RIC =", round(ric, 4), "\n\n")

# Vallas de Tukey
valla_inf <- q1 - 1.5 * ric
valla_sup <- q3 + 1.5 * ric
cat("8️⃣  VALLAS DE TUKEY\n")
cat("   Valla inferior =", round(valla_inf, 4), "\n")
cat("   Valla superior =", round(valla_sup, 4), "\n")

# Valores atípicos
atipicos <- x[x < valla_inf | x > valla_sup]
cat("   Valores atípicos:", if(length(atipicos) == 0) "Ninguno" else round(atipicos, 4), "\n\n")

# Media por riego
cat("9️⃣  MEDIA POR RIEGO\n")
media_por_riego <- aggregate(rendimiento ~ riego, data = datos, FUN = mean)
print(media_por_riego)

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n\n")

cat("RESUMEN DE RESULTADOS (4 decimales)\n")
cat("Media:                         ", round(media, 4), "\n")
cat("Mediana:                       ", round(mediana, 4), "\n")
cat("Varianza (S²):                 ", round(varianza, 4), "\n")
cat("Desviación estándar (S):       ", round(desv_est, 4), "\n")
cat("Coeficiente de variación (CV): ", round(cv, 4), "%\n")
cat("Q1:                            ", round(q1, 4), "\n")
cat("Q3:                            ", round(q3, 4), "\n")
cat("RIC:                           ", round(ric, 4), "\n")
cat("Valla inferior:                ", round(valla_inf, 4), "\n")
cat("Valla superior:                ", round(valla_sup, 4), "\n")
cat("Cantidad de atípicos:          ", length(atipicos), "\n")

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n\n")
