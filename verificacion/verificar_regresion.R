# Verificación REGRESIÓN LINEAL - muestra_reg8.csv
# Script de R para regresión con fórmulas explícitas
# Usar en Posit Cloud (posit.cloud)

# ============================================================================
# CARGA DE DATOS
# ============================================================================

datos <- read.csv('datos/muestra_reg8.csv')
x <- datos$lamina_riego
y <- datos$rendimiento
n <- length(x)

cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n")
cat("VERIFICACIÓN REGRESIÓN LINEAL - muestra_reg8.csv\n")
cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n\n")

cat("Variable X (lámina de riego):\n")
print(round(x, 4))
cat("\nVariable Y (rendimiento):\n")
print(round(y, 4))

# ============================================================================
# 1. REGRESIÓN LINEAL CON lm()
# ============================================================================

# Ajustar el modelo
modelo <- lm(y ~ x)

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("1️⃣  MODELO DE REGRESIÓN LINEAL: y = b₀ + b₁×x\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

# Resumen del modelo
print(summary(modelo))

# Extraer parámetros del modelo
b0 <- coef(modelo)[1]
b1 <- coef(modelo)[2]

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("2️⃣  PARÁMETROS DEL MODELO\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

cat("   b₀ (intercepción) =", round(b0, 4), "\n")
cat("   b₁ (pendiente) =", round(b1, 4), "\n")
cat("   Ecuación: ŷ = ", round(b0, 4), "+ ", round(b1, 4), "× x\n\n")

# ============================================================================
# 3. SUMAS DE CUADRADOS (Sxx, Syy, Sxy)
# ============================================================================

cat("3️⃣  SUMAS DE CUADRADOS\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

media_x <- mean(x)
media_y <- mean(y)

# Sxx
sxx <- sum((x - media_x)^2)
cat("   Sxx = Σ(x - x̄)² =", round(sxx, 4), "\n")

# Syy
syy <- sum((y - media_y)^2)
cat("   Syy = Σ(y - ȳ)² =", round(syy, 4), "\n")

# Sxy
sxy <- sum((x - media_x) * (y - media_y))
cat("   Sxy = Σ(x - x̄)(y - ȳ) =", round(sxy, 4), "\n\n")

# ============================================================================
# 4. CORRELACIÓN
# ============================================================================

cat("4️⃣  CORRELACIÓN\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

# Pearson
r_pearson <- cor(x, y, method = "pearson")
cat("   r (Pearson) =", round(r_pearson, 4), "\n")

# Spearman
r_spearman <- cor(x, y, method = "spearman")
cat("   ρ (Spearman) =", round(r_spearman, 4), "\n\n")

# ============================================================================
# 5. SUMA DE CUADRADOS DEL ERROR (SCE)
# ============================================================================

cat("5️⃣  SUMA DE CUADRADOS DEL ERROR\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

# Predicciones
y_pred <- predict(modelo)
residuos <- residuals(modelo)
sce <- sum(residuos^2)

cat("   Predicciones y residuos:\n")
cat(sprintf("   i | x_i        | y_i        | ŷ_i        | e_i        | e_i²\n"))
cat("   " %+% paste(rep("-", 60), collapse="") %+% "\n")

for (i in 1:n) {
  cat(sprintf("   %d | %10.4f | %10.4f | %10.4f | %10.4f | %10.4f\n",
              i, x[i], y[i], y_pred[i], residuos[i], residuos[i]^2))
}

cat("   " %+% paste(rep("-", 60), collapse="") %+% "\n")
cat("   SCE = Σ(e²) =", round(sce, 4), "\n\n")

# ============================================================================
# 6. R² Y RSE
# ============================================================================

cat("6️⃣  COEFICIENTE DE DETERMINACIÓN (R²) Y ERROR ESTÁNDAR\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

# R²
r_squared <- 1 - (sce / syy)
cat("   R² = 1 - (SCE / Syy) = 1 - (", round(sce, 4), "/", round(syy, 4), ") =", round(r_squared, 4), "\n")

# RSE (Residual Standard Error)
gl <- n - 2
rse <- sqrt(sce / gl)
cat("   GL = n - 2 =", gl, "\n")
cat("   RSE = √(SCE / GL) = √(", round(sce, 4), "/", gl, ") =", round(rse, 4), "\n\n")

# ============================================================================
# 7. ERROR ESTÁNDAR DE b₁
# ============================================================================

cat("7️⃣  ERROR ESTÁNDAR DE b₁\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

se_b1 <- rse / sqrt(sxx)
cat("   SE(b₁) = RSE / √(Sxx) =", round(rse, 4), "/ √(", round(sxx, 4), ") =", round(se_b1, 4), "\n\n")

# ============================================================================
# 8. ESTADÍSTICO t Y VALOR p
# ============================================================================

cat("8️⃣  ESTADÍSTICO t Y VALOR p\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

t_stat <- b1 / se_b1
p_value <- 2 * (1 - pt(abs(t_stat), gl))

cat("   t = b₁ / SE(b₁) = ", round(b1, 4), "/", round(se_b1, 4), "=", round(t_stat, 4), "\n")
cat("   Grados de libertad = GL =", gl, "\n")
cat("   Valor p (dos colas) =", round(p_value, 4), "\n")

alpha <- 0.05
decision <- if (p_value < alpha) "Significativo (p < 0.05)" else "No significativo (p >= 0.05)"
cat("   Decisión (α = 0.05):", decision, "\n\n")

# ============================================================================
# 9. INTERVALO DE CONFIANZA AL 95% PARA b₁
# ============================================================================

cat("9️⃣  INTERVALO DE CONFIANZA AL 95% PARA b₁\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

t_critico <- qt(0.975, gl)
margen_error <- t_critico * se_b1
ic_inf <- b1 - margen_error
ic_sup <- b1 + margen_error

cat("   t_0.025,", gl, "=", round(t_critico, 4), "\n")
cat("   Margen de error = ", round(t_critico, 4), "×", round(se_b1, 4), "=", round(margen_error, 4), "\n")
cat("   IC 95% = [", round(ic_inf, 4), ",", round(ic_sup, 4), "]\n\n")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("📊 RESUMEN DE RESULTADOS (4 decimales)\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

cat("n                              :", n, "\n")
cat("Sxx                            :", round(sxx, 4), "\n")
cat("Syy                            :", round(syy, 4), "\n")
cat("Sxy                            :", round(sxy, 4), "\n")
cat("Correlación de Pearson (r)     :", round(r_pearson, 4), "\n")
cat("Correlación de Spearman (ρ)    :", round(r_spearman, 4), "\n")
cat("b₀ (intercepción)              :", round(b0, 4), "\n")
cat("b₁ (pendiente)                 :", round(b1, 4), "\n")
cat("SCE                            :", round(sce, 4), "\n")
cat("R²                             :", round(r_squared, 4), "\n")
cat("RSE                            :", round(rse, 4), "\n")
cat("SE(b₁)                         :", round(se_b1, 4), "\n")
cat("t = b₁ / SE(b₁)                :", round(t_stat, 4), "\n")
cat("Decisión (α=0.05)              :", decision, "\n")
cat("IC 95% para b₁                 : [", round(ic_inf, 4), ",", round(ic_sup, 4), "]\n")

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n\n")
