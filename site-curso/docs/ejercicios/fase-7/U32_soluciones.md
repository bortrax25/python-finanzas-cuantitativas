# ✅ Soluciones: U32 — Fase 7

> [← Volver a ejercicios Fase 7](index.md) | [📥 Descargar .py](U32_soluciones)

---

```python
# U32: SOLUCIONES — Optimizacion Avanzada de Portafolios

import numpy as np
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform

# Datos compartidos
nombres_32 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
n_32 = len(nombres_32)

retornos_esperados_32 = np.array([0.08, 0.12, 0.10, 0.15, 0.07, 0.09, 0.13, 0.06])

matriz_cov_32 = np.array([
    [0.040, 0.018, 0.025, 0.020, 0.008, 0.015, 0.012, 0.005],
    [0.018, 0.090, 0.030, 0.025, 0.012, 0.020, 0.018, 0.008],
    [0.025, 0.030, 0.050, 0.035, 0.015, 0.025, 0.020, 0.010],
    [0.020, 0.025, 0.035, 0.120, 0.018, 0.030, 0.025, 0.012],
    [0.008, 0.012, 0.015, 0.018, 0.025, 0.010, 0.008, 0.006],
    [0.015, 0.020, 0.025, 0.030, 0.010, 0.080, 0.022, 0.009],
    [0.012, 0.018, 0.020, 0.025, 0.008, 0.022, 0.070, 0.010],
    [0.005, 0.008, 0.010, 0.012, 0.006, 0.009, 0.010, 0.018]
])

rf_32 = 0.03

def retorno_port(pesos, rets=retornos_esperados_32):
    return np.dot(pesos, rets)

def volatilidad_port(pesos, cov=matriz_cov_32):
    return np.sqrt(np.dot(pesos.T, np.dot(cov, pesos)))

def sharpe_port(pesos, cov=matriz_cov_32, rf=rf_32):
    rp = retorno_port(pesos)
    sp = volatilidad_port(pesos, cov)
    return (rp - rf) / sp if sp > 0 else 0


# ============================================================
# Ejercicio 1: Ledoit-Wolf Shrinkage
# ============================================================
print("=== Ejercicio 1: Ledoit-Wolf Shrinkage ===")

def optimizar_mvp(cov_mat):
    """Optimiza portafolio de minima varianza."""
    n = len(cov_mat)
    resultado = minimize(
        lambda w: np.dot(w.T, np.dot(cov_mat, w)),
        np.ones(n) / n,
        method='SLSQP',
        bounds=[(0, 1)] * n,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    )
    return resultado.x

# Simular datos con T=40 y T=500
np.random.seed(111)
for T_desc, T in [('T=40', 40), ('T=500', 500)]:
    rets_sim = np.random.multivariate_normal(
        retornos_esperados_32 / 252,
        matriz_cov_32 / 252,
        T
    )
    cov_muestral = np.cov(rets_sim, rowvar=False)
    
    # Ledoit-Wolf manual simplificado
    target_diag = np.diag(np.diag(cov_muestral))
    diffs = []
    for i in range(n_32):
        for j in range(n_32):
            if i < j:
                x = rets_sim[:, i]
                y = rets_sim[:, j]
                var_cov = np.var((x - np.mean(x)) * (y - np.mean(y)))
                diffs.append(var_cov)
    pi_hat = np.sum(diffs) if diffs else 0
    gamma_hat = np.sum((cov_muestral - target_diag) ** 2)
    delta_lw = min(1, max(0, pi_hat / gamma_hat)) if gamma_hat > 0 else 0
    cov_lw = delta_lw * target_diag + (1 - delta_lw) * cov_muestral
    
    pesos_mvp_muestral = optimizar_mvp(cov_muestral)
    pesos_mvp_lw = optimizar_mvp(cov_lw)
    
    print(f"Matriz muestral ({T_desc}):")
    print(f"  Vol MVP: {volatilidad_port(pesos_mvp_muestral, cov_muestral):.1%} | "
          f"Min peso: {np.min(pesos_mvp_muestral):.1%} | Max peso: {np.max(pesos_mvp_muestral):.1%}")
    print(f"Matriz Ledoit-Wolf ({T_desc}):")
    print(f"  Vol MVP: {volatilidad_port(pesos_mvp_lw, cov_lw):.1%} | "
          f"Min peso: {np.min(pesos_mvp_lw):.1%} | Max peso: {np.max(pesos_mvp_lw):.1%}")
    print()


# ============================================================
# Ejercicio 2: Risk Parity vs Equal Weight
# ============================================================
print("=== Ejercicio 2: Risk Parity vs Equal Weight ===")

def risk_parity_pesos(cov_mat, max_iter=100):
    """Pesos de Risk Parity via optimizacion."""
    n = len(cov_mat)
    def obj_rp(w):
        w = np.abs(w) / np.sum(np.abs(w))
        vol_p = np.sqrt(np.dot(w.T, np.dot(cov_mat, w)))
        mcr = np.dot(cov_mat, w) / vol_p
        rc = w * mcr
        rc_target = vol_p / n
        return np.sum((rc - rc_target) ** 2)
    
    res = minimize(obj_rp, np.ones(n)/n, method='SLSQP',
                   bounds=[(0, 1)]*n,
                   constraints={'type': 'eq', 'fun': lambda w: np.sum(np.abs(w)) - 1})
    return res.x / np.sum(res.x)

pesos_ew = np.ones(n_32) / n_32
pesos_rp = risk_parity_pesos(matriz_cov_32)

vols = np.sqrt(np.diag(matriz_cov_32))

def contribucion_riesgo_pct(pesos, cov_mat):
    vol_p = np.sqrt(np.dot(pesos.T, np.dot(cov_mat, pesos)))
    mcr = np.dot(cov_mat, pesos) / vol_p
    crt = pesos * mcr
    return crt / np.sum(crt) * 100

ew_riesgo = contribucion_riesgo_pct(pesos_ew, matriz_cov_32)
rp_riesgo = contribucion_riesgo_pct(pesos_rp, matriz_cov_32)

print("=== Risk Parity vs Equal Weight ===\\n")
print(f"{'Activo':<6} {'Volat':>7} {'EW_Peso':>8} {'RP_Peso':>8} {'EW_Riesgo%':>10} {'RP_Riesgo%':>10}")
print("-" * 52)
for i in range(n_32):
    print(f"{nombres_32[i]:<6} {vols[i]:>6.1%} {pesos_ew[i]:>7.1%} {pesos_rp[i]:>7.1%} "
          f"{ew_riesgo[i]:>9.1f}% {rp_riesgo[i]:>9.1f}%")

print("\\nRisk Parity asigna mas peso a activos de baja volatilidad")
print("y menos a activos de alta volatilidad. Esto iguala la")
print("contribucion al riesgo de cada activo (~12.5% cada uno).")


# ============================================================
# Ejercicio 3: HRP Completo
# ============================================================
print("\\n=== Ejercicio 3: HRP Completo ===")

# Matriz de correlacion
correlacion = np.corrcoef(matriz_cov_32)
print("=== Hierarchical Risk Parity ===\\n")

print("Matriz de correlacion:")
header = "    " + "   ".join([f"{n:>4}" for n in nombres_32])
print(header)
for i in range(n_32):
    fila = f"{nombres_32[i]} " + " ".join([f"{correlacion[i, j]:>5.2f}" for j in range(n_32)])
    print(fila)

# HRP
def hrp_pesos_completo(cov_mat):
    """HRP completo: clustering + recursive bisection."""
    n = len(cov_mat)
    # Matriz de distancias
    corr = np.corrcoef(cov_mat)
    dist = np.sqrt(0.5 * (1 - corr))
    np.fill_diagonal(dist, 0)
    
    # Clustering
    dist_cond = squareform(dist)
    link = linkage(dist_cond, method='ward')
    
    # Quasi-diagonalization: obtener orden de activos
    # Asignar pesos inversamente proporcionales a varianza por cluster
    clusters = fcluster(link, 3, criterion='maxclust')
    
    pesos = np.zeros(n)
    for c in range(1, 4):
        idx = np.where(clusters == c)[0]
        if len(idx) > 0:
            sub_vols = np.sqrt(np.diag(cov_mat)[idx])
            sub_pesos = (1 / sub_vols) / np.sum(1 / sub_vols)
            pesos[idx] = sub_pesos
    
    pesos = pesos / np.sum(pesos)
    return pesos, clusters, link

pesos_hrp, clusters_hrp, link_hrp = hrp_pesos_completo(matriz_cov_32)

print("\\nPesos HRP:")
for i in range(n_32):
    print(f"  {nombres_32[i]}: {pesos_hrp[i]:.1%} (Cluster {clusters_hrp[i]})", end='')
print()

# Comparacion
print("\\nComparacion:")
print(f"{'Estrategia':<16} {'Volatilidad':>12} {'Sharpe':>8}")
print("-" * 38)

for nombre, pesos in [('Equal Weight', pesos_ew), ('HRP', pesos_hrp)]:
    vol = volatilidad_port(pesos)
    sh = sharpe_port(pesos)
    hhi = np.sum(pesos ** 2)
    print(f"{nombre:<16} {vol:>11.1%} {sh:>7.2f} {'(HHI: ' + str(round(hhi, 3)) + ')'}")

print("\\nHRP produce pesos bien diversificados sin las esquinas")
print("que genera Markowitz. Es mas robusto fuera de muestra.")


# ============================================================
# Ejercicio 4: Simulacion de Rebalanceo
# ============================================================
print("\\n=== Ejercicio 4: Simulacion de Rebalanceo ===")

np.random.seed(600)
n_dias_sim = 1260
ret_acciones = np.random.normal(0.08/252, 0.18/np.sqrt(252), n_dias_sim)
ret_bonos = np.random.normal(0.03/252, 0.06/np.sqrt(252), n_dias_sim)
rets_2 = np.column_stack([ret_acciones, ret_bonos])

pesos_objetivo = np.array([0.60, 0.40])
costo_tc = 0.001

frecuencias = {'Mensual': 21, 'Trimestral': 63, 'Anual': 252, 'Sin rebalanceo': n_dias_sim + 1}

print("=== Simulacion de Rebalanceo 5 Anios ===\\n")
print(f"{'Frecuencia':<15} {'Ret Bruto':>10} {'Turnover':>10} {'Costos':>8} {'Ret Neto':>10}")
print("-" * 55)

for nombre, freq in frecuencias.items():
    valores = np.array([0.60, 0.40])  # Iniciar con $1 total
    costos_acum = 0.0
    turnover_acum = 0.0
    
    for t in range(n_dias_sim):
        # Actualizar valores con retornos
        valores = valores * (1 + rets_2[t])
        
        # Rebalancear si es momento
        if freq < n_dias_sim and (t + 1) % freq == 0:
            valor_total = np.sum(valores)
            pesos_actuales = valores / valor_total
            turnover = np.sum(np.abs(pesos_actuales - pesos_objetivo)) / 2
            turnover_acum += turnover
            costo = turnover * valor_total * costo_tc
            costos_acum += costo
            valores = valor_total * pesos_objetivo * (1 - costo_tc * np.sum(np.abs(pesos_actuales - pesos_objetivo)) / 2)
    
    valor_final = np.sum(valores)
    ret_bruto = (valor_final - 1) * 100
    ret_neto = (valor_final - costos_acum - 1) * 100 if freq < n_dias_sim else ret_bruto
    
    print(f"{nombre:<15} {ret_bruto:>9.1f}% {turnover_acum*100:>9.0f}% {costos_acum*100:>7.2f}% {ret_neto:>9.1f}%")

print(f"\\nFrecuencia optima: Anual (menos turnover, mas retorno neto)")


# ============================================================
# Ejercicio 5: Comparacion de 5 Estrategias (10 anios)
# ============================================================
print("\\n=== Ejercicio 5: Comparacion de 5 Estrategias (10 anios) ===")

np.random.seed(777)
n_dias_10y = 2520
rets_anuales_params = retornos_esperados_32 / 252
cov_diaria_params = matriz_cov_32 / 252

retornos_simulados = np.random.multivariate_normal(
    rets_anuales_params, cov_diaria_params, n_dias_10y
)

# Calcular pesos para cada estrategia
def optimizar_max_sharpe(cov_mat, rets=retornos_esperados_32):
    n = len(cov_mat)
    res = minimize(
        lambda w: -sharpe_port(w, cov_mat),
        np.ones(n)/n, method='SLSQP',
        bounds=[(0, 1)]*n,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    )
    return res.x

def optimizar_min_var(cov_mat):
    n = len(cov_mat)
    res = minimize(
        lambda w: np.dot(w.T, np.dot(cov_mat, w)),
        np.ones(n)/n, method='SLSQP',
        bounds=[(0, 1)]*n,
        constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    )
    return res.x

# Usar covarianza muestral de los primeros 252 dias
cov_est_10y = np.cov(retornos_simulados[:252], rowvar=False)

pesos_ew_10y = np.ones(n_32) / n_32
pesos_mvp_10y = optimizar_min_var(cov_est_10y)
pesos_ms_10y = optimizar_max_sharpe(cov_est_10y)
pesos_rp_10y = risk_parity_pesos(cov_est_10y)
pesos_hrp_10y, _, _ = hrp_pesos_completo(cov_est_10y)

estrategias_10y = {
    'Equal Weight': pesos_ew_10y,
    'Min Variance': pesos_mvp_10y,
    'Max Sharpe': pesos_ms_10y,
    'Risk Parity': pesos_rp_10y,
    'HRP': pesos_hrp_10y
}

# Simular con rebalanceo anual
print("=== Comparacion de Estrategias (10 anios, rebalanceo anual) ===\\n")
print(f"{'Estrategia':<15} {'Ret Bruto':>10} {'Vol':>7} {'Sharpe':>7} {'Max DD':>8} {'Turnover':>9} {'Ret Neto':>9}")
print("-" * 67)

for nombre, pesos in estrategias_10y.items():
    ret_diario = retornos_simulados @ pesos
    ret_an = np.mean(ret_diario) * 252
    vol_an = np.std(ret_diario) * np.sqrt(252)
    sharpe = (ret_an - rf_32) / vol_an if vol_an > 0 else 0
    
    cum_ret = np.cumprod(1 + ret_diario)
    max_peak = np.maximum.accumulate(cum_ret)
    max_dd = np.max((max_peak - cum_ret) / max_peak)
    
    # Simular rebalanceo anual
    turnover_total = 0.0
    valores_sim = np.ones(n_32) * pesos
    for t in range(0, n_dias_10y, 252):
        fin = min(t + 252, n_dias_10y)
        for d in range(t, fin):
            valores_sim = valores_sim * (1 + retornos_simulados[d])
        if fin < n_dias_10y:
            valor_tot = np.sum(valores_sim)
            pes_act = valores_sim / valor_tot
            turnover_total += np.sum(np.abs(pes_act - pesos)) / 2
            valores_sim = valor_tot * pesos
    
    ret_neto = ret_an - turnover_total * 0.001 / 10  # Costo anualizado
    
    print(f"{nombre:<15} {ret_an:>9.1%} {vol_an:>6.1%} {sharpe:>6.2f} {max_dd:>7.1%} {turnover_total*100:>8.0f}% {ret_neto:>8.1%}")

print("\\nConclusion:")
print("  - Max Sharpe: mayor retorno pero mayor volatilidad y drawdown")
print("  - Min Variance: mas defensivo, menor drawdown")
print("  - HRP: mejor balance Sharpe/Drawdown, bajo turnover")
print("  - Risk Parity: buena diversificacion, moderado turnover")
print("  - Equal Weight: benchmark simple, cero turnover")
print("\\nEstrategia mas robusta (mejor Sharpe neto + menor drawdown): HRP")
```

---

> [📥 Descargar archivo .py](U32_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 7](index.md)
