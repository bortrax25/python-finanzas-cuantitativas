# U19: SOLUCIONES — NumPy: Computación Numérica de Alto Rendimiento

import numpy as np
np.random.seed(42)

# ============================================================
# Ejercicio 1: Matriz de covarianza y correlación de 10 activos
# ============================================================
print("=== Ejercicio 1: Matriz de covarianza y correlación ===")

retornos = np.random.normal(0.0005, 0.015, (252, 10))
matriz_cov = np.cov(retornos.T)
matriz_corr = np.corrcoef(retornos.T)

print("Matriz de covarianza (10×10) calculada")
print("Matriz de correlación (10×10) calculada")

# Encontrar par más y menos correlacionado (excluyendo diagonal)
corr_max = -2.0
corr_min = 2.0
par_max = (0, 0)
par_min = (0, 0)

for i in range(10):
    for j in range(i + 1, 10):
        corr = matriz_corr[i, j]
        if corr > corr_max:
            corr_max = corr
            par_max = (i, j)
        if corr < corr_min:
            corr_min = corr
            par_min = (i, j)

print(f"Par más correlacionado: ACT_{par_max[0]} vs ACT_{par_max[1]} (corr={corr_max:.3f})")
print(f"Par menos correlacionado: ACT_{par_min[0]} vs ACT_{par_min[1]} (corr={corr_min:.3f})")

# ============================================================
# Ejercicio 2: Simulación GBM — 10,000 trayectorias
# ============================================================
print("\n=== Ejercicio 2: Simulación GBM 10,000 trayectorias ===")

np.random.seed(42)
spot = 100.0
mu = 0.07
sigma = 0.22
T = 1.0
dias = 252
dt = T / dias
simulaciones = 10_000

Z = np.random.standard_normal((simulaciones, dias))
retornos_log = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
trayectorias = spot * np.exp(np.cumsum(retornos_log, axis=1))

precios_finales = trayectorias[:, -1]
precio_esperado = precios_finales.mean()
mediana = np.median(precios_finales)
prob_itm = (precios_finales > 110).mean() * 100
p5 = np.percentile(precios_finales, 5)
p95 = np.percentile(precios_finales, 95)
precio_min = precios_finales.min()
precio_max = precios_finales.max()

print(f"Parámetros: S0={spot}, μ={mu}, σ={sigma}, T={T} año, {dias} días")
print(f"Simulaciones: {simulaciones:,} trayectorias")
print(f"Precio esperado ST: ${precio_esperado:.2f}")
print(f"Mediana ST: ${mediana:.2f}")
print(f"P(ITM) CALL K=110: {prob_itm:.1f}%")
print(f"Percentil 5 ST: ${p5:.2f}")
print(f"Percentil 95 ST: ${p95:.2f}")
print(f"Min ST: ${precio_min:.2f} | Max ST: ${precio_max:.2f}")

# ============================================================
# Ejercicio 3: Benchmark — Loops vs Vectorizado
# ============================================================
print("\n=== Ejercicio 3: Benchmark Loops vs Vectorizado ===")

import time

np.random.seed(123)
n = 1_000_000
precios = np.random.lognormal(mean=0, sigma=0.02, size=n)

# Loop Python
inicio = time.perf_counter()
retornos_loop = []
for i in range(1, len(precios)):
    retornos_loop.append((precios[i] - precios[i - 1]) / precios[i - 1])
tiempo_loop = time.perf_counter() - inicio

# NumPy vectorizado
inicio = time.perf_counter()
retornos_vec = np.diff(precios) / precios[:-1]
tiempo_vec = time.perf_counter() - inicio

aceleracion = tiempo_loop / tiempo_vec

print(f"N = {n:,} precios generados")
print(f"Loop Python: {tiempo_loop:.4f}s")
print(f"NumPy vectorizado: {tiempo_vec:.4f}s")
print(f"Aceleración: {aceleracion:.1f}x")

# ============================================================
# Ejercicio 4: Portafolio correlacionado con descomposición de Cholesky
# ============================================================
print("\n=== Ejercicio 4: Portafolio con Cholesky y VaR ===")

np.random.seed(42)

spots = np.array([100.0, 200.0, 50.0, 75.0, 150.0])
mu = np.array([0.08, 0.06, 0.12, 0.04, 0.10])
sigmas = np.array([0.22, 0.15, 0.30, 0.18, 0.25])
pesos = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

correlacion = np.array([
    [1.0, 0.6, 0.3, 0.4, 0.5],
    [0.6, 1.0, 0.2, 0.5, 0.4],
    [0.3, 0.2, 1.0, 0.1, 0.2],
    [0.4, 0.5, 0.1, 1.0, 0.6],
    [0.5, 0.4, 0.2, 0.6, 1.0],
])

print("Matriz de correlación:")
print(correlacion)

cov_matrix = np.outer(sigmas, sigmas) * correlacion
L = np.linalg.cholesky(cov_matrix)

sims, dias = 5_000, 252
T, dt = 1.0, 1 / 252

Z = np.random.standard_normal((sims, dias, 5))
shocks_corr = Z @ L.T
retornos_log = (mu - 0.5 * sigmas**2) * dt + np.sqrt(dt) * shocks_corr
trayectorias = spots * np.exp(np.cumsum(retornos_log, axis=1))

valores_portafolio = (trayectorias * pesos).sum(axis=2)
valor_inicial = valores_portafolio[:, 0].mean()
precios_finales = valores_portafolio[:, -1]
retornos_port = precios_finales / valor_inicial - 1

var_95 = np.percentile(retornos_port, 5)
debajo_var = retornos_port[retornos_port <= var_95]
cvar_95 = debajo_var.mean() if len(debajo_var) > 0 else var_95

print(f"Simulaciones: {sims:,} × {dias} días")
print(f"Valor inicial portafolio: ${valor_inicial:.2f}")
print(f"Valor esperado final: ${precios_finales.mean():.2f}")
print(f"VaR 95%: {var_95:.2%}")
print(f"CVaR 95%: {cvar_95:.2%}")
