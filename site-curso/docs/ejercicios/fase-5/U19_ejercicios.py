# U19: EJERCICIOS — NumPy: Computación Numérica de Alto Rendimiento

# ============================================================
# Ejercicio 1: Matriz de covarianza y correlación de 10 activos
# Genera retornos sintéticos para 10 activos durante 252 días usando
# np.random.normal con μ=0.0005 y σ=0.015 para todos.
# Luego:
#   - Calcula la matriz de covarianza (10×10) con np.cov
#   - Calcula la matriz de correlación (10×10) con np.corrcoef
#   - Encuentra el par de activos (i, j, i≠j) con mayor correlación
#   - Encuentra el par de activos (i, j, i≠j) con menor correlación
#   - Imprime los resultados con nombres de activos: ACT_0, ACT_1, ..., ACT_9
# ============================================================
print("=== Ejercicio 1: Matriz de covarianza y correlación ===")

# Escribe tu código aquí



# Output esperado:
# Matriz de covarianza (10×10) calculada
# Matriz de correlación (10×10) calculada
# Par más correlacionado: ACT_2 vs ACT_7 (corr=0.XX)
# Par menos correlacionado: ACT_4 vs ACT_9 (corr=-0.XX)


# ============================================================
# Ejercicio 2: Simulación GBM — 10,000 trayectorias
# Simula 10,000 trayectorias GBM con:
#   - spot = 100.0
#   - mu = 0.07 (retorno anual esperado)
#   - sigma = 0.22 (volatilidad anual)
#   - T = 1 año, 252 días
# Usa np.random.seed(42) para reproducibilidad.
# Calcula e imprime:
#   - Precio esperado al final (media de ST)
#   - Mediana de ST
#   - Probabilidad de que una CALL con K=110 sea ITM: P(ST > 110)
#   - Percentil 5 y 95 de ST
#   - Máximo y mínimo precio simulado
# ============================================================
print("\n=== Ejercicio 2: Simulación GBM 10,000 trayectorias ===")

# Escribe tu código aquí



# Output esperado:
# Parámetros: S0=100.0, μ=0.07, σ=0.22, T=1 año, 252 días
# Simulaciones: 10,000 trayectorias
# Precio esperado ST: $107.XX
# Mediana ST: $106.XX
# P(ITM) CALL K=110: XX.X%
# Percentil 5 ST: $8X.XX
# Percentil 95 ST: $13X.XX
# Min ST: $XX.XX | Max ST: $2XX.XX


# ============================================================
# Ejercicio 3: Benchmark — Loops vs Vectorizado
# Con np.random.seed(123), genera 1,000,000 de precios con distribución
# log-normal (np.random.lognormal). Luego:
#   - Mide el tiempo de calcular retornos diarios con un loop Python
#   - Mide el tiempo de calcular retornos diarios con np.diff (vectorizado)
#   - Reporta la aceleración (loop_time / vectorized_time)
# NO imprimas los retornos, solo los tiempos.
# ============================================================
print("\n=== Ejercicio 3: Benchmark Loops vs Vectorizado ===")

# Escribe tu código aquí



# Output esperado:
# N = 1,000,000 precios generados
# Loop Python: X.XXXXs
# NumPy vectorizado: 0.00XXs
# Aceleración: XXX.Xx


# ============================================================
# Ejercicio 4: Portafolio correlacionado con descomposición de Cholesky
# Dados 5 activos con:
#   spots = np.array([100, 200, 50, 75, 150])
#   mu = np.array([0.08, 0.06, 0.12, 0.04, 0.10])
#   sigmas = np.array([0.22, 0.15, 0.30, 0.18, 0.25])
#   correlacion predefinida (ver más abajo)
#   pesos equal-weight: np.array([0.2, 0.2, 0.2, 0.2, 0.2])
#
# 1. Construye la matriz de covarianza: cov = outer(sigmas, sigmas) * corr
# 2. Calcula L = np.linalg.cholesky(cov)
# 3. Simula 5,000 trayectorias de 252 días con shocks correlacionados
# 4. Calcula el valor del portafolio para cada trayectoria
# 5. Reporta: valor esperado final, VaR 95%, CVaR 95% (Expected Shortfall)
#    VaR 95% = percentil 5 de los retornos del portafolio
#    CVaR 95% = media de los retornos que caen bajo el VaR 95%
# ============================================================
print("\n=== Ejercicio 4: Portafolio con Cholesky y VaR ===")

# Escribe tu código aquí



# Output esperado:
# Matriz de correlación:
# [[1.  0.6 0.3 0.4 0.5]
#  [0.6 1.  0.2 0.5 0.4]
#  [0.3 0.2 1.  0.1 0.2]
#  [0.4 0.5 0.1 1.  0.6]
#  [0.5 0.4 0.2 0.6 1. ]]
# Simulaciones: 5,000 × 252 días
# Valor inicial portafolio: $XXX.XX
# Valor esperado final: $XXX.XX
# VaR 95%: -XX.X%
# CVaR 95%: -XX.X%
