# Verificación SERIES DE TIEMPO - muestra_series24.csv
# Script de R para series de tiempo con fórmulas explícitas
# Usar en Posit Cloud (posit.cloud)

# ============================================================================
# CARGA DE DATOS
# ============================================================================

datos <- read.csv('datos/muestra_series24.csv')
precip <- datos$precipitacion_mm
conjunto <- datos$conjunto
meses <- datos$mes
anios <- datos$anio

n_total <- length(precip)
n_ent <- sum(conjunto == "entrenamiento")
n_val <- n_total - n_ent

cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n")
cat("VERIFICACIÓN SERIES DE TIEMPO - muestra_series24.csv\n")
cat("=" %+% paste(rep("=", 78), collapse="") %+% "\n\n")

cat("Datos cargados:\n")
print(datos)

precip_ent <- precip[1:n_ent]
precip_val <- precip[(n_ent + 1):n_total]
meses_val <- meses[(n_ent + 1):n_total]
anios_val <- anios[(n_ent + 1):n_total]

cat("\nEntrenamiento (t=1 a", n_ent, "):\n")
for (i in 1:n_ent) {
  cat(sprintf("   t=%2d: %.4f mm\n", i, precip_ent[i]))
}

cat("\nValidación (t=", n_ent + 1, "a", n_total, "):\n")
for (i in 1:n_val) {
  cat(sprintf("   t=%2d (%d-%02d): %.4f mm\n", n_ent + i, anios_val[i], meses_val[i], precip_val[i]))
}

# ============================================================================
# 1. PROMEDIO MÓVIL 3 (PM3)
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("1️⃣  PROMEDIO MÓVIL 3 (PM3)\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

cat("   Fórmula: PM3_t = (y_t + y_(t-1) + y_(t-2)) / 3\n\n")
cat("   t | Dato       | PM3\n")
cat("   " %+% paste(rep("-", 35), collapse="") %+% "\n")

pm3 <- numeric(n_ent)
for (i in 1:n_ent) {
  if (i < 3) {
    pm3[i] <- NA
    cat(sprintf("   %2d | %10.4f | N/A (no hay 3 datos)\n", i, precip_ent[i]))
  } else {
    pm3[i] <- (precip_ent[i] + precip_ent[i - 1] + precip_ent[i - 2]) / 3
    cat(sprintf("   %2d | %10.4f | (%.2f + %.2f + %.2f) / 3 = %.4f\n",
                i, precip_ent[i], precip_ent[i], precip_ent[i - 1], precip_ent[i - 2], pm3[i]))
  }
}

# ============================================================================
# 2. ÍNDICES ESTACIONALES
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("2️⃣  ÍNDICES ESTACIONALES\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

# Media general de entrenamiento
media_gral <- mean(precip_ent)
cat("   Media general (entrenamiento):", round(media_gral, 4), "\n\n")

# Extraer valores por mes
datos_por_mes <- list()
for (mes_i in 1:12) {
  datos_por_mes[[mes_i]] <- precip_ent[meses[1:n_ent] == mes_i]
}

cat("   Mes | Valores                    | Media mes | Índice\n")
cat("   " %+% paste(rep("-", 75), collapse="") %+% "\n")

indices_estacionales <- numeric(12)
for (mes_i in 1:12) {
  vals <- datos_por_mes[[mes_i]]
  if (length(vals) > 0) {
    media_mes <- mean(vals)
    indice <- media_mes / media_gral
    indices_estacionales[mes_i] <- indice
    
    vals_str <- paste(sprintf("%.2f", vals), collapse = ", ")
    cat(sprintf("   %2d  | %-26s | %9.4f | %.4f\n",
                mes_i, substr(vals_str, 1, 26), media_mes, indice))
  }
}

suma_indices <- sum(indices_estacionales, na.rm = TRUE)
cat("\n   Suma de índices:", round(suma_indices, 4), "(debe ser ≈ 12.0000)\n")

# ============================================================================
# 3. PRONÓSTICOS - MÉTODOS DE REFERENCIA
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("3️⃣  PRONÓSTICOS CON MÉTODOS DE REFERENCIA\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

# Método 1: Ingenuo (naive)
cat("   MÉTODO 1: INGENUO (Naive) - ŷ_t = y_(t-1)\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")
cat("   t | Mes-Año    | Real       | ŷ         | Error\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")

pron_naive <- numeric(n_val)
for (i in 1:n_val) {
  if (i == 1) {
    pred <- precip_ent[n_ent]
  } else {
    pred <- precip_val[i - 1]
  }
  pron_naive[i] <- pred
  error <- precip_val[i] - pred
  cat(sprintf("   %2d | %d-%02d   | %10.4f | %9.4f | %9.4f\n",
              n_ent + i, anios_val[i], meses_val[i], precip_val[i], pred, error))
}

# Método 2: Estacional Ingenuo
cat("\n   MÉTODO 2: ESTACIONAL INGENUO - ŷ_t = y_(t-12)\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")
cat("   t | Mes-Año    | Real       | ŷ         | Error\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")

pron_seasonal <- numeric(n_val)
for (i in 1:n_val) {
  idx_12_atras <- (n_ent + i - 12)
  if (idx_12_atras >= 1) {
    pred <- precip[idx_12_atras]
  } else {
    pred <- precip_ent[(n_ent + i - 12) %% length(precip_ent)]
  }
  pron_seasonal[i] <- pred
  error <- precip_val[i] - pred
  cat(sprintf("   %2d | %d-%02d   | %10.4f | %9.4f | %9.4f\n",
              n_ent + i, anios_val[i], meses_val[i], precip_val[i], pred, error))
}

# Método 3: Promedio
cat("\n   MÉTODO 3: PROMEDIO - ŷ_t = promedio_entrenamiento\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")
cat("   t | Mes-Año    | Real       | ŷ         | Error\n")
cat("   " %+% paste(rep("-", 50), collapse="") %+% "\n")

media_ent <- mean(precip_ent)
pron_promedio <- rep(media_ent, n_val)

for (i in 1:n_val) {
  error <- precip_val[i] - pron_promedio[i]
  cat(sprintf("   %2d | %d-%02d   | %10.4f | %9.4f | %9.4f\n",
              n_ent + i, anios_val[i], meses_val[i], precip_val[i], pron_promedio[i], error))
}

# ============================================================================
# 4. MÉTRICAS DE ERROR
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("4️⃣  MÉTRICAS DE ERROR (MAE, RMSE, SMAPE)\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

# Funciones
mae_func <- function(real, pred) {
  mean(abs(real - pred))
}

rmse_func <- function(real, pred) {
  sqrt(mean((real - pred)^2))
}

smape_func <- function(real, pred) {
  mean(abs(real - pred) / (abs(real) + abs(pred))) * 100
}

# Calcular para cada método
metodos <- list(
  "Ingenuo" = pron_naive,
  "Estacional Ingenuo" = pron_seasonal,
  "Promedio" = pron_promedio
)

cat("   Método                 | MAE        | RMSE       | SMAPE (%)\n")
cat("   " %+% paste(rep("-", 60), collapse="") %+% "\n")

resultados <- list()
for (nombre in names(metodos)) {
  pred <- metodos[[nombre]]
  mae_val <- mae_func(precip_val, pred)
  rmse_val <- rmse_func(precip_val, pred)
  smape_val <- smape_func(precip_val, pred)
  
  cat(sprintf("   %-22s | %10.4f | %10.4f | %9.4f\n",
              nombre, mae_val, rmse_val, smape_val))
  
  resultados[[nombre]] <- list(MAE = mae_val, RMSE = rmse_val, SMAPE = smape_val)
}

# Ganador
smape_vals <- sapply(resultados, function(x) x$SMAPE)
metodo_ganador <- names(resultados)[which.min(smape_vals)]
smape_ganador <- min(smape_vals)

cat("\n   🏆 Método ganador (menor SMAPE):", metodo_ganador, "con SMAPE =", round(smape_ganador, 4), "%\n")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n")
cat("📊 RESUMEN DE RESULTADOS (4 decimales)\n")
cat(paste(rep("=", 80), collapse="") %+% "\n\n")

cat("Promedio Móvil 3 (últimos 3 valores del entrenamiento):\n")
if (!is.na(pm3[n_ent])) {
  cat("   PM3_", n_ent, " = ", round(pm3[n_ent], 4), " mm\n\n", sep = "")
}

cat("Índices Estacionales (12 meses):\n")
for (mes_i in 1:12) {
  cat(sprintf("   Mes %2d: %.4f\n", mes_i, indices_estacionales[mes_i]))
}

cat("\nMétricas de Error:\n")
cat("Método                 | MAE        | RMSE       | SMAPE (%)\n")
cat("-" %+% paste(rep("-", 60), collapse="") %+% "\n")
for (nombre in names(resultados)) {
  r <- resultados[[nombre]]
  cat(sprintf("%-22s | %10.4f | %10.4f | %10.4f\n",
              nombre, r$MAE, r$RMSE, r$SMAPE))
}

cat("\n🏆 Ganador:", metodo_ganador, "(SMAPE =", round(smape_ganador, 4), "%)\n")

cat("\n" %+% paste(rep("=", 80), collapse="") %+% "\n\n")
