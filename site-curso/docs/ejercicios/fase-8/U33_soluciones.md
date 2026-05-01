# ✅ Soluciones: U33 — Fase 8

> [← Volver a ejercicios Fase 8](index.md) | [📥 Descargar .py](U33_soluciones)

---

```python
# U33: SOLUCIONES — Probabilidad, Estadística y Distribuciones Financieras

# ============================================================
# Ejercicio 1: Estadísticas y tests de normalidad
# ============================================================
import numpy as np
import scipy.stats as stats

np.random.seed(42)
retornos = np.random.standard_t(df=5, size=(252, 50)) * 0.005 + 0.0005

print("=== Ejercicio 1: Estadísticas y Tests de Normalidad ===")

n_activos = retornos.shape[1]
no_normales = 0

for i in range(n_activos):
    r = retornos[:, i]
    media = r.mean()
    vol = r.std(ddof=1)
    skew = stats.skew(r)
    kurt = stats.kurtosis(r)
    jb_stat, jb_p = stats.jarque_bera(r)
    es_normal = jb_p > 0.05
    if not es_normal:
        no_normales += 1
    if i < 5:
        print(f"Activo {i}: media={media:.6f}, vol={vol:.6f}, skew={skew:.4f}, kurt={kurt:.4f}, Normal: {es_normal}")

print(f"...")
print(f"Total activos: {n_activos}")
print(f"Activos que rechazan normalidad (JB, 95%): {no_normales} / {n_activos} ({no_normales / n_activos * 100:.1f}%)")


# ============================================================
# Ejercicio 2: Ajuste t-Student y comparación de VaR
# ============================================================
print("\\n=== Ejercicio 2: Ajuste t-Student y VaR ===")

retornos_activo = retornos[:, 0]

# Ajuste t-Student
df_t, loc_t, scale_t = stats.t.fit(retornos_activo)
print(f"Parámetros t-Student: df={df_t:.2f}, loc={loc_t:.6f}, scale={scale_t:.6f}")

# VaR al 95%
var_95_historico = np.percentile(retornos_activo, 5)
var_95_normal = stats.norm.ppf(0.05, loc=retornos_activo.mean(), scale=retornos_activo.std(ddof=1))
var_95_t = stats.t.ppf(0.05, df=df_t, loc=loc_t, scale=scale_t)

print(f"VaR 95% Histórico:   {var_95_historico:.4%}")
print(f"VaR 95% Normal:       {var_95_normal:.4%}")
print(f"VaR 95% t-Student:    {var_95_t:.4%}")

# VaR al 99%
var_99_historico = np.percentile(retornos_activo, 1)
var_99_normal = stats.norm.ppf(0.01, loc=retornos_activo.mean(), scale=retornos_activo.std(ddof=1))
var_99_t = stats.t.ppf(0.01, df=df_t, loc=loc_t, scale=scale_t)

print(f"VaR 99% Histórico:    {var_99_historico:.4%}")
print(f"VaR 99% Normal:        {var_99_normal:.4%}")
print(f"VaR 99% t-Student:     {var_99_t:.4%}")


# ============================================================
# Ejercicio 3: Simulación GBM y comparación con bootstrap
# ============================================================
print("\\n=== Ejercicio 3: Simulación GBM vs Bootstrap ===")

np.random.seed(123)
precio_inicial = 4500
mu = 0.09
sigma = 0.18
dias = 252
n_sim = 5000

# GBM
dt = 1 / 252
trayectorias_gbm = np.zeros((dias, n_sim))
trayectorias_gbm[0, :] = precio_inicial

for i in range(1, dias):
    z = np.random.standard_normal(n_sim)
    trayectorias_gbm[i, :] = trayectorias_gbm[i - 1, :] * np.exp(
        (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    )

precios_finales_gbm = trayectorias_gbm[-1, :]
p_gbm = np.percentile(precios_finales_gbm, [5, 25, 50, 75, 95])

print("GBM — Precios finales:")
print(f"  P5={p_gbm[0]:.2f}, P25={p_gbm[1]:.2f}, P50={p_gbm[2]:.2f}, P75={p_gbm[3]:.2f}, P95={p_gbm[4]:.2f}")

# Bootstrap histórico
retornos_historicos = np.random.normal(mu / 252, sigma / np.sqrt(252), 1260)  # 5 años simulados
trayectorias_bs = np.zeros((dias, n_sim))
trayectorias_bs[0, :] = precio_inicial

for j in range(n_sim):
    precios_tray = [precio_inicial]
    for i in range(1, dias):
        r = np.random.choice(retornos_historicos)
        precios_tray.append(precios_tray[-1] * (1 + r))
    trayectorias_bs[:, j] = np.array(precios_tray)

precios_finales_bs = trayectorias_bs[-1, :]
p_bs = np.percentile(precios_finales_bs, [5, 25, 50, 75, 95])

print("Bootstrap — Precios finales:")
print(f"  P5={p_bs[0]:.2f}, P25={p_bs[1]:.2f}, P50={p_bs[2]:.2f}, P75={p_bs[3]:.2f}, P95={p_bs[4]:.2f}")

diferencia_mediana = abs(p_gbm[2] - p_bs[2]) / p_gbm[2] * 100
print(f"Diferencia en mediana: {diferencia_mediana:.2f}%")


# ============================================================
# Ejercicio 4: Validación de supuestos para portafolio
# ============================================================
print("\\n=== Ejercicio 4: Validación de Supuestos para Portafolio ===")

np.random.seed(99)
retornos_5 = np.random.standard_t(df=6, size=(252, 5)) * 0.005 + 0.0004

n_activos = retornos_5.shape[1]
normales = []

for i in range(n_activos):
    r = retornos_5[:, i]
    jb_stat, jb_p = stats.jarque_bera(r)
    sh_stat, sh_p = stats.shapiro(r)
    es_normal = (jb_p > 0.05) and (sh_p > 0.05)
    normales.append(es_normal)
    print(f"Activo {i}: JB p={jb_p:.4f}, SW p={sh_p:.4f} → {'Normal' if es_normal else 'NO normal'}")

# Matriz de covarianza clásica
cov_clasica = np.cov(retornos_5.T)

# Matriz de covarianza bootstrap
n_obs = retornos_5.shape[0]
n_bootstrap = 1000
cov_bootstrap = np.zeros((n_activos, n_activos))

for b in range(n_bootstrap):
    indices = np.random.choice(n_obs, size=n_obs, replace=True)
    muestra_b = retornos_5[indices, :]
    cov_bootstrap += np.cov(muestra_b.T)

cov_bootstrap /= n_bootstrap

# Comparar
diferencia = np.abs(cov_clasica - cov_bootstrap)
print(f"\\nCov clásica vs bootstrap — diferencia media: {diferencia.mean():.6f}")
print(f"Cov clásica vs bootstrap — diferencia máxima: {diferencia.max():.6f}")
print(f"Las diferencias son pequeñas; el supuesto de normalidad afecta más")
print(f"a métricas de cola (VaR, CVaR) que a la covarianza.")
```

---

> [📥 Descargar archivo .py](U33_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 8](index.md)
