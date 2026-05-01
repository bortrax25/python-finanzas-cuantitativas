# ✅ Soluciones: U29 — Fase 7

> [← Volver a ejercicios Fase 7](index.md) | [📥 Descargar .py](U29_soluciones)

---

```python
# U29: SOLUCIONES — Teoria Moderna de Portafolios (Markowitz)

import numpy as np
from scipy.optimize import minimize

# Datos compartidos: 10 activos
nombres_activos = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM', 'JNJ', 'XOM', 'PG', 'TSLA', 'NVDA']

retornos_esperados = np.array([0.12, 0.11, 0.10, 0.14, 0.08, 0.07, 0.09, 0.06, 0.18, 0.20])

matriz_covarianza = np.array([
    [0.045, 0.018, 0.015, 0.022, 0.008, 0.005, 0.006, 0.004, 0.025, 0.030],
    [0.018, 0.040, 0.017, 0.020, 0.007, 0.006, 0.005, 0.005, 0.015, 0.020],
    [0.015, 0.017, 0.042, 0.025, 0.006, 0.005, 0.004, 0.004, 0.018, 0.022],
    [0.022, 0.020, 0.025, 0.065, 0.008, 0.005, 0.005, 0.004, 0.025, 0.030],
    [0.008, 0.007, 0.006, 0.008, 0.025, 0.005, 0.008, 0.006, 0.008, 0.008],
    [0.005, 0.006, 0.005, 0.005, 0.005, 0.020, 0.003, 0.008, 0.004, 0.005],
    [0.006, 0.005, 0.004, 0.005, 0.008, 0.003, 0.030, 0.005, 0.006, 0.006],
    [0.004, 0.005, 0.004, 0.004, 0.006, 0.008, 0.005, 0.018, 0.003, 0.004],
    [0.025, 0.015, 0.018, 0.025, 0.008, 0.004, 0.006, 0.003, 0.090, 0.035],
    [0.030, 0.020, 0.022, 0.030, 0.008, 0.005, 0.006, 0.004, 0.035, 0.100]
])

rf = 0.03
n_activos = len(retornos_esperados)

def retorno_portafolio(pesos):
    return np.dot(pesos, retornos_esperados)

def volatilidad_portafolio(pesos):
    return np.sqrt(np.dot(pesos.T, np.dot(matriz_covarianza, pesos)))

def sharpe_portafolio(pesos):
    rp = retorno_portafolio(pesos)
    sp = volatilidad_portafolio(pesos)
    return (rp - rf) / sp if sp > 0 else 0


# ============================================================
# Ejercicio 1: Frontera Eficiente (10,000 portafolios)
# ============================================================
print("=== Ejercicio 1: Frontera Eficiente ===")
np.random.seed(42)
n_sims = 10000

resultados = np.zeros((3, n_sims))
pesos_simulados = np.zeros((n_sims, n_activos))

for i in range(n_sims):
    w_bruto = np.random.random(n_activos)
    w = w_bruto / np.sum(w_bruto)
    pesos_simulados[i] = w
    resultados[0, i] = retorno_portafolio(w)
    resultados[1, i] = volatilidad_portafolio(w)
    resultados[2, i] = sharpe_portafolio(w)

idx_min_vol = np.argmin(resultados[1])
idx_max_sharpe = np.argmax(resultados[2])

print("=== Frontera Eficiente (10,000 simulaciones) ===\\n")

print("Portafolio de Minima Varianza:")
print(f"  Retorno: {resultados[0, idx_min_vol]:.1%} | "
      f"Volatilidad: {resultados[1, idx_min_vol]:.1%} | "
      f"Sharpe: {resultados[2, idx_min_vol]:.2f}")
pesos_mvp_sim = pesos_simulados[idx_min_vol]
top_mvp = np.argsort(pesos_mvp_sim)[::-1][:3]
pesos_str_mvp = '  '.join([f"{nombres_activos[j]} {pesos_mvp_sim[j]:.0%}" for j in top_mvp])
print(f"  Pesos principales: {pesos_str_mvp}...\\n")

print("Portafolio de Maximo Sharpe (Tangente):")
print(f"  Retorno: {resultados[0, idx_max_sharpe]:.1%} | "
      f"Volatilidad: {resultados[1, idx_max_sharpe]:.1%} | "
      f"Sharpe: {resultados[2, idx_max_sharpe]:.2f}")
pesos_ms_sim = pesos_simulados[idx_max_sharpe]
top_ms = np.argsort(pesos_ms_sim)[::-1][:3]
pesos_str_ms = '  '.join([f"{nombres_activos[j]} {pesos_ms_sim[j]:.0%}" for j in top_ms])
print(f"  Pesos principales: {pesos_str_ms}...\\n")

pesos_ew = np.ones(n_activos) / n_activos
rp_ew = retorno_portafolio(pesos_ew)
sp_ew = volatilidad_portafolio(pesos_ew)
sh_ew = sharpe_portafolio(pesos_ew)
print("Equal Weight:")
print(f"  Retorno: {rp_ew:.1%} | Volatilidad: {sp_ew:.1%} | Sharpe: {sh_ew:.2f}")


# ============================================================
# Ejercicio 2: Optimizacion con Restricciones
# ============================================================
print("\\n=== Ejercicio 2: Optimizacion con Restricciones ===")

def optimizar_portafolio(funcion_objetivo, **kwargs):
    """Optimiza portafolio con SLSQP."""
    resultado = minimize(
        funcion_objetivo,
        np.ones(n_activos) / n_activos,
        method='SLSQP',
        bounds=[(0, 1)] * n_activos,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        options={'maxiter': 1000, 'ftol': 1e-12},
        **kwargs
    )
    return resultado.x

pesos_mvp_opt = optimizar_portafolio(lambda w: np.dot(w.T, np.dot(matriz_covarianza, w)))
pesos_ms_opt = optimizar_portafolio(lambda w: -sharpe_portafolio(w))

print("=== Optimizacion con SLSQP ===\\n")

print("Minima Varianza (optimizado):")
for i in np.argsort(pesos_mvp_opt)[::-1]:
    if pesos_mvp_opt[i] > 0.001:
        print(f"  {nombres_activos[i]}: {pesos_mvp_opt[i]:.1%}", end='')
print()
rp_mvp = retorno_portafolio(pesos_mvp_opt)
sp_mvp = volatilidad_portafolio(pesos_mvp_opt)
sh_mvp = sharpe_portafolio(pesos_mvp_opt)
print(f"  Retorno: {rp_mvp:.1%} | Volatilidad: {sp_mvp:.1%} | Sharpe: {sh_mvp:.2f}\\n")

print("Maximo Sharpe (optimizado):")
for i in np.argsort(pesos_ms_opt)[::-1]:
    if pesos_ms_opt[i] > 0.001:
        print(f"  {nombres_activos[i]}: {pesos_ms_opt[i]:.1%}", end='')
print()
rp_ms = retorno_portafolio(pesos_ms_opt)
sp_ms = volatilidad_portafolio(pesos_ms_opt)
sh_ms = sharpe_portafolio(pesos_ms_opt)
print(f"  Retorno: {rp_ms:.1%} | Volatilidad: {sp_ms:.1%} | Sharpe: {sh_ms:.2f}")


# ============================================================
# Ejercicio 3: Capital Market Line (CML)
# ============================================================
print("\\n=== Ejercicio 3: Capital Market Line ===")

rp_tangente = rp_ms
sp_tangente = sp_ms
sharpe_tangente = sh_ms

print(f"Portafolio Tangente: ret={rp_tangente:.1%}, vol={sp_tangente:.1%}, Sharpe={sharpe_tangente:.2f}")
print(f"Tasa libre de riesgo: {rf:.1%}\\n")

for retorno_objetivo in [0.10, 0.15]:
    peso_tangente = (retorno_objetivo - rf) / (rp_tangente - rf)
    peso_rf = 1 - peso_tangente
    vol_objetivo = abs(peso_tangente) * sp_tangente
    
    print(f"Para retorno objetivo {retorno_objetivo:.1%}:")
    print(f"  Peso en rf: {peso_rf:.1%} | Peso en tangente: {peso_tangente:.1%}")
    print(f"  Volatilidad: {vol_objetivo:.1%}")
    if peso_rf < 0:
        print(f"  Nota: Peso negativo en rf implica pedir prestado a la tasa libre.")
    print()


# ============================================================
# Ejercicio 4: Analisis de Robustez
# ============================================================
print("=== Ejercicio 4: Analisis de Robustez ===")
np.random.seed(99)
n_perturb = 100
sigma_ruido = 0.005

pesos_perturbados = np.zeros((n_perturb, n_activos))
for i in range(n_perturb):
    ruido = np.random.normal(0, sigma_ruido, n_activos)
    rets_pert = retornos_esperados + ruido
    
    # Optimizar Sharpe con retornos perturbados
    def sharpe_neg_pert(w):
        rp_pert = np.dot(w, rets_pert)
        sp_pert = np.sqrt(np.dot(w.T, np.dot(matriz_covarianza, w)))
        return -(rp_pert - rf) / sp_pert if sp_pert > 0 else 1e10
    
    pesos_perturbados[i] = optimizar_portafolio(sharpe_neg_pert)

desviaciones_pesos = np.std(pesos_perturbados, axis=0)

print("=== Robustez de Markowitz (100 perturbaciones, sigma=0.5%) ===\\n")
print("Volatilidad de los pesos del portafolio tangente:")
orden = np.argsort(desviaciones_pesos)[::-1]
for i in orden:
    print(f"  {nombres_activos[i]}: {desviaciones_pesos[i]:.1%}", end='')
print()
print("\\nActivos mas sensibles: los de alto retorno y volatilidad")
print("La optimizacion 'persigue' pequenios cambios en retornos esperados")
print("-> Error maximization de Markowitz")


# ============================================================
# Ejercicio 5: Comparacion de Estrategias (10 anios)
# ============================================================
print("\\n=== Ejercicio 5: Comparacion de Estrategias ===")
np.random.seed(777)
n_dias = 2520  # 10 anios

# Simular retornos diarios
rets_diarios = np.random.multivariate_normal(
    retornos_esperados / 252,
    matriz_covarianza / 252,
    n_dias
)

estrategias = {
    'Equal Weight': pesos_ew,
    'Min Variance': pesos_mvp_opt,
    'Max Sharpe': pesos_ms_opt
}

print("=== Simulacion 10 Anios (2520 dias) ===\\n")
print(f"{'Estrategia':<16} {'Ret Anual':>10} {'Vol Anual':>10} {'Sharpe':>8} {'Max DD':>10}")
print("-" * 56)

for nombre, pesos in estrategias.items():
    ret_diario_port = rets_diarios @ pesos
    ret_anual = np.mean(ret_diario_port) * 252
    vol_anual = np.std(ret_diario_port) * np.sqrt(252)
    sharpe = (ret_anual - rf) / vol_anual if vol_anual > 0 else 0
    
    cum_ret = np.cumprod(1 + ret_diario_port)
    max_peak = np.maximum.accumulate(cum_ret)
    drawdowns = (max_peak - cum_ret) / max_peak
    max_dd = np.max(drawdowns)
    
    print(f"{nombre:<16} {ret_anual:>9.1%} {vol_anual:>9.1%} {sharpe:>7.2f} {max_dd:>9.1%}")

print("\\nMax Sharpe tiene mayor retorno pero peor drawdown.")
print("Min Variance es la mas defensiva (menor volatilidad y drawdown).")
print("Equal Weight es el mejor balance Sharpe vs Drawdown.")
```

---

> [📥 Descargar archivo .py](U29_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 7](index.md)
