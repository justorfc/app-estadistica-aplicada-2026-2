# Verificación DISTRIBUCIONES - muestra_dist10.csv
# Script de R para análisis de distribuciones probabilísticas
# Usar en Posit Cloud (posit.cloud)

# ============================================================================
# INSTALACIÓN DE LIBRERÍAS (ejecutar una sola vez)
# ============================================================================

# Para máxima verosimilitud Gumbel y GEV, necesitas:
# install.packages("fitdistrplus")  # Distribuciones y ajuste flexible
# install.packages("evd")            # Distribuciones de valores extremos

# En Posit Cloud:
# 1. Ve a "Packages" → "Install"
# 2. Escribe "fitdistrplus" → "Install"
# 3. Escribe "evd" → "Install"

# Una vez instaladas, cargar:
library(fitdistrplus)  # Para ajuste por máxima verosimilitud
library(evd)           # Para distribuciones GEV y Gumbel

# ============================================================================
# CARGA DE DATOS
# ============================================================================

datos <- read.csv('datos/muestra_dist10.csv')
x <- sort(datos$pmax24h_mm)  # Ordenar de menor a mayor
n <- length(x)

cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n")
cat("VERIFICACIÓN DISTRIBUCIONES - muestra_dist10.csv\n")
cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n\n")

cat("Datos ordenados (n =", n, "):\n")
for (i in 1:n) {
  cat(sprintf("   x(%d) = %.4f\n", i, x[i]))
}

# ============================================================================
# 1. POSICIÓN DE WEIBULL
# ============================================================================

cat("\n1️⃣  POSICIÓN DE WEIBULL\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")
cat("   i  | x(i)       | F(x) = i/(n+1)\n")
cat("   " %+% paste(rep("-", 38), collapse="") %+% "\n")

posiciones_weibull <- numeric(n)
for (i in 1:n) {
  f_x <- i / (n + 1)
  posiciones_weibull[i] <- f_x
  cat(sprintf("   %2d | %10.4f | %.4f\n", i, x[i], f_x))
}

# ============================================================================
# 2. GUMBEL POR MOMENTOS
# ============================================================================

cat("\n2️⃣  DISTRIBUCIÓN DE GUMBEL - MÉTODO DE MOMENTOS\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

media <- mean(x)
desv_est <- sd(x)

cat("   Media =", round(media, 4), "\n")
cat("   Desviación estándar =", round(desv_est, 4), "\n")

# Parámetros de Gumbel por momentos
gamma_euler <- 0.5772156649
pi_val <- pi
sqrt6 <- sqrt(6)

beta <- desv_est * sqrt6 / pi_val
mu <- media - beta * gamma_euler

cat("\n   Constante de Euler γ =", round(gamma_euler, 10), "\n")
cat("   √6 / π =", round(sqrt6 / pi_val, 10), "\n")
cat("   β = σ × (√6 / π) =", round(desv_est, 4), "×", round(sqrt6/pi_val, 10), "=", round(beta, 4), "\n")
cat("   μ = media - β × γ =", round(media, 4), "-", round(beta, 4), "×", round(gamma_euler, 10), "=", round(mu, 4), "\n")

# ============================================================================
# 3. PERÍODO DE RETORNO EMPÍRICO
# ============================================================================

cat("\n3️⃣  PERÍODO DE RETORNO EMPÍRICO T\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")
cat("   i  | x(i)       | T = (n+1)/i\n")
cat("   " %+% paste(rep("-", 38), collapse="") %+% "\n")

periodos_empiricos <- numeric(n)
for (i in 1:n) {
  t_emp <- (n + 1) / i
  periodos_empiricos[i] <- t_emp
  cat(sprintf("   %2d | %10.4f | %.4f años\n", i, x[i], t_emp))
}

# ============================================================================
# 4. x_T PARA PERÍODOS ESPECÍFICOS (10, 50, 100 años)
# ============================================================================

cat("\n4️⃣  CÁLCULO DE x_T PARA PERÍODOS DE RETORNO ESPECÍFICOS (Gumbel)\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")
cat("   Fórmula: x_T = μ - β × ln(-ln(1 - 1/T))\n\n")

periodos_target <- c(10, 50, 100)
valores_xt <- numeric(length(periodos_target))

for (idx in 1:length(periodos_target)) {
  T <- periodos_target[idx]
  prob <- 1 - (1 / T)
  ln_prob <- log(-log(prob))
  x_t <- mu - beta * ln_prob
  valores_xt[idx] <- x_t
  
  cat(sprintf("   T = %d años:\n", T))
  cat(sprintf("      P(x ≤ x_T) = 1 - 1/%d = %.6f\n", T, prob))
  cat(sprintf("      -ln(-ln(%.6f)) = %.4f\n", prob, ln_prob))
  cat(sprintf("      x_%d = %.4f - %.4f × %.4f = %.4f mm\n\n", T, mu, beta, ln_prob, x_t))
}

# ============================================================================
# 5. RIESGO PARA T = 50 AÑOS, N = 25 AÑOS
# ============================================================================

cat("5️⃣  RIESGO PARA T = 50 AÑOS, N = 25 AÑOS\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

T_riesgo <- 50
N_riesgo <- 25

prob_no_excedencia <- 1 - (1 / T_riesgo)
prob_no_excedencia_n <- prob_no_excedencia ^ N_riesgo
riesgo <- 1 - prob_no_excedencia_n

cat("   Fórmula: R = 1 - (1 - 1/T)^N\n")
cat(sprintf("   P(no excedencia en 1 año) = 1 - 1/%d = %.6f\n", T_riesgo, prob_no_excedencia))
cat(sprintf("   P(no excedencia en %d años) = (%.6f)^%d = %.6f\n", N_riesgo, prob_no_excedencia, N_riesgo, prob_no_excedencia_n))
cat(sprintf("   Riesgo R = 1 - %.6f = %.4f (%.2f%%)\n", prob_no_excedencia_n, riesgo, riesgo * 100))

# ============================================================================
# 6. AJUSTE POR MÁXIMA VEROSIMILITUD (opcional, con fitdistrplus)
# ============================================================================

cat("\n6️⃣  AJUSTE POR MÁXIMA VEROSIMILITUD (MLE) - fitdistrplus\n")
cat("-" %+% paste(rep("-", 78), collapse="") %+% "\n")

# Ajuste Gumbel usando fitdistrplus
# Nota: fitdist() requiere una función de densidad y parámetros iniciales

# Para Gumbel en fitdistrplus, usar dgumbel (del paquete evd)
# Alternativamente, usar la función personalizada

tryCatch({
  # Ajuste Gumbel con evd
  fit_gumbel <- fgumbel(x)  # Máxima verosimilitud con evd
  
  cat("   Ajuste Gumbel (MLE con evd):\n")
  cat("   μ (parámetro de localización) =", round(fit_gumbel$estimate['mu'], 4), "\n")
  cat("   σ (parámetro de escala) =", round(fit_gumbel$estimate['sigma'], 4), "\n")
  cat("   Nota: Este método puede diferir del ajuste por momentos\n\n")
}, error = function(e) {
  cat("   (Nota: Para usar MLE, instala primero: install.packages('evd'))\n\n")
})

# ============================================================================
# RESUMEN FINAL
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("📊 RESUMEN DE RESULTADOS (4 decimales)\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

cat("Parámetros de Gumbel (Método de Momentos):\n")
cat("   μ (localización) =", round(mu, 4), "\n")
cat("   β (escala) =", round(beta, 4), "\n\n")

cat("Valores de x_T (precipitación máxima esperada):\n")
for (idx in 1:length(periodos_target)) {
  T <- periodos_target[idx]
  cat(sprintf("   x_%d años = %.4f mm\n", T, valores_xt[idx]))
}

cat(sprintf("\nRiesgo para T = %d años, N = %d años: %.4f (%.2f%%)\n", T_riesgo, N_riesgo, riesgo, riesgo * 100))

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n\n")

# ============================================================================
# INSTRUCCIONES PARA POSIT CLOUD
# ============================================================================

cat("INSTRUCCIONES PARA POSIT CLOUD:\n")
cat("================================\n")
cat("1. Copia este script en una ventana R en Posit Cloud\n")
cat("2. Antes de ejecutar, instala las librerías:\n")
cat("   - Ve a 'Packages' → 'Install'\n")
cat("   - Busca y instala 'fitdistrplus'\n")
cat("   - Busca y instala 'evd'\n")
cat("3. Ejecuta el script línea por línea o todo a la vez\n")
cat("4. Los resultados aparecerán en la consola\n\n")
