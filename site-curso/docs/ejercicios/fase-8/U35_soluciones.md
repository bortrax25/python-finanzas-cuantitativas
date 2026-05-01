# ✅ Soluciones: U35 — Fase 8

> [← Volver a ejercicios Fase 8](index.md) | [📥 Descargar .py](U35_soluciones)

---

```python
# U35: SOLUCIONES — Econometría Financiera: Regresión y Panel Data

# ============================================================
# Ejercicio 1: Diagnóstico de regresión CAPM
# ============================================================
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

np.random.seed(42)
n = 500
retorno_mercado = np.random.normal(0.0005, 0.012, n)
alfa_verdadero = 0.0002
beta_verdadero = 1.2

ruido = np.where(
    retorno_mercado < 0,
    np.random.normal(0, 0.012, n),
    np.random.normal(0, 0.006, n)
)
retorno_accion = alfa_verdadero + beta_verdadero * retorno_mercado + ruido

print("=== Ejercicio 1: Diagnóstico de regresión CAPM ===")

X = sm.add_constant(retorno_mercado)
modelo = sm.OLS(retorno_accion, X)

# (a) OLS simple
res = modelo.fit()
print(f"OLS: alfa={res.params[0]:.4f} (p={res.pvalues[0]:.3f}), beta={res.params[1]:.3f} (p={res.pvalues[1]:.3f})")

# (b) Breusch-Pagan
bp_stat, bp_pval, _, _ = het_breuschpagan(res.resid, X)
print(f"Breusch-Pagan: p={bp_pval:.4f} → {'Heterocedasticidad DETECTADA' if bp_pval < 0.05 else 'Homocedástico'}")

# (c) Durbin-Watson
dw = durbin_watson(res.resid)
print(f"Durbin-Watson: {dw:.2f} → {'Autocorrelación positiva' if dw < 1.5 else 'Sin autocorrelación apreciable' if dw < 2.5 else 'Autocorrelación negativa'}")

# (d) White HC3
res_hc3 = modelo.fit(cov_type='HC3')
print(f"White (HC3):  alfa={res_hc3.params[0]:.4f} (p={res_hc3.pvalues[0]:.3f}), beta={res_hc3.params[1]:.3f} (p={res_hc3.pvalues[1]:.3f})")

# (e) Newey-West
res_nw = modelo.fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print(f"Newey-West:   alfa={res_nw.params[0]:.4f} (p={res_nw.pvalues[0]:.3f}), beta={res_nw.params[1]:.3f} (p={res_nw.pvalues[1]:.3f})")

print(f"Conclusión: Significancia del alfa es similar; los SE son ligeramente mayores con errores robustos")


# ============================================================
# Ejercicio 2: Errores clustered vs robustos
# ============================================================
print("\\n=== Ejercicio 2: Errores Clustered vs Robustos ===")

np.random.seed(42)
n_empresas = 80
n_meses = 60
n_total = n_empresas * n_meses

# Crear panel
empresa_id = np.repeat(np.arange(n_empresas), n_meses)
sector_id = empresa_id % 8  # 8 sectores
tiempo = np.tile(np.arange(n_meses), n_empresas)

retorno_mercado = np.random.normal(0.0005, 0.012, n_total)

# Ruido: correlacionado dentro del mismo sector
ruido_sector = np.random.normal(0, 0.005, (8, n_meses))
ruido_empresa = np.random.normal(0, 0.003, (n_empresas, n_meses))
ruido_idio = np.random.normal(0, 0.008, n_total)

ruido_total = ruido_sector[sector_id, tiempo] + ruido_empresa[empresa_id, tiempo] + ruido_idio
retorno_accion = 0.0002 + 1.0 * retorno_mercado + ruido_total

X = sm.add_constant(retorno_mercado)
modelo = sm.OLS(retorno_accion, X)

# (a) OLS simple
res_ols = modelo.fit()
print("Error estándar de beta:")
print(f"OLS simple:          {res_ols.bse[1]:.4f}")

# (b) White HC3
res_hc3 = modelo.fit(cov_type='HC3')
print(f"White (HC3):         {res_hc3.bse[1]:.4f}")

# (c) Newey-West (5 lags)
res_nw = modelo.fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print(f"Newey-West (5):      {res_nw.bse[1]:.4f}")

# (d) Clustered por empresa
res_cl_emp = modelo.fit(cov_type='cluster', cov_kwds={'groups': empresa_id})
print(f"Clustered empresa:   {res_cl_emp.bse[1]:.4f}")

# (e) Clustered por sector
res_cl_sec = modelo.fit(cov_type='cluster', cov_kwds={'groups': sector_id})
print(f"Clustered sector:    {res_cl_sec.bse[1]:.4f}")

print(f"El clustering por sector es el más conservador")


# ============================================================
# Ejercicio 3: Fixed Effects vs Pooled OLS
# ============================================================
from linearmodels.panel import PanelOLS

print("\\n=== Ejercicio 3: Fixed Effects vs Pooled OLS ===")

np.random.seed(42)
n_empresas = 30
n_periodos = 40
n_total = n_empresas * n_periodos

# Generar datos con efectos fijos
empresa_id = np.repeat(np.arange(n_empresas), n_periodos)
tiempo = np.tile(np.arange(n_periodos), n_empresas)
alfa_fijos = np.random.normal(0, 0.02, n_empresas)  # efectos fijos por empresa

x = np.random.normal(0, 1, n_total)
verdadero_beta = 1.0
ruido = np.random.normal(0, 0.01, n_total)

y = alfa_fijos[empresa_id] + verdadero_beta * x + ruido

# DataFrame para panel
df = pd.DataFrame({
    'y': y,
    'x': x,
    'empresa': empresa_id,
    'tiempo': tiempo
})

# Pooled OLS
X_pooled = sm.add_constant(df['x'])
pooled = sm.OLS(df['y'], X_pooled).fit()

# Panel Fixed Effects
df_panel = df.set_index(['empresa', 'tiempo'])
fe = PanelOLS(df_panel['y'], sm.add_constant(df_panel[['x']]), entity_effects=True).fit()

print(f"Pooled OLS beta:    {pooled.params[1]:.4f}")
print(f"Fixed Effects beta: {fe.params['x']:.4f} (valor verdadero: {verdadero_beta})")
print(f"R² (Pooled):        {pooled.rsquared:.4f}")
print(f"R² Within (FE):     {fe.rsquared_within:.4f}")
print(f"R² Between (FE):    {fe.rsquared_between:.4f}")
print(f"El R² within es más bajo porque FE explota solo la variación temporal")
print(f"dentro de cada empresa, ignorando diferencias entre empresas")


# ============================================================
# Ejercicio 4: Fama-MacBeth
# ============================================================
print("\\n=== Ejercicio 4: Fama-MacBeth ===")

np.random.seed(42)
T, N, ventana = 120, 30, 36

# Betas verdaderas
betas_verdaderas = np.random.uniform(0.5, 1.5, N)
prima_mercado = 0.006

# Factores de mercado
retornos_mercado = np.random.normal(0.0005, 0.012, T)

# Paso 1: Betas estimadas (verdaderas + ruido)
betas_estimadas = np.tile(betas_verdaderas, (T, 1))
betas_estimadas += np.random.normal(0, 0.15, size=(T, N))

# Paso 2: Fama-MacBeth cross-sectional
gammas_mercado = []
gammas_intercepto = []

for t in range(T):
    retornos_t = 0.001 + prima_mercado * betas_verdaderas + np.random.normal(0, 0.02, N)
    X = sm.add_constant(betas_estimadas[t])
    modelo_cs = sm.OLS(retornos_t, X).fit()
    gammas_intercepto.append(modelo_cs.params[0])
    gammas_mercado.append(modelo_cs.params[1])

gammas_intercepto = np.array(gammas_intercepto)
gammas_mercado = np.array(gammas_mercado)

# Estadísticas Fama-MacBeth
gamma_estimado = gammas_mercado.mean()
se_fm = gammas_mercado.std(ddof=1) / np.sqrt(T)
t_stat = gamma_estimado / se_fm

print(f"Prima verdadera: {prima_mercado:.4f}")
print(f"Prima estimada (gamma): {gamma_estimado:.4f}")
print(f"Error estándar FM:      {se_fm:.4f}")
print(f"t-statistic:            {t_stat:.2f}")
print(f"Significativa: {'SÍ (|t| > 1.96)' if abs(t_stat) > 1.96 else 'NO'}")
```

---

> [📥 Descargar archivo .py](U35_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 8](index.md)
