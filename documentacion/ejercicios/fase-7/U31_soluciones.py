# U31: SOLUCIONES — Gestion de Riesgo: VaR, CVaR y Stress Testing

import numpy as np
from scipy import stats

# Datos compartidos
np.random.seed(300)
n_obs = 500
retornos_portafolio = np.random.normal(-0.0002, 0.018, n_obs)
valor_portafolio = 5_000_000

exposiciones_stress = {
    'equity_us': 0.45,
    'equity_em': 0.10,
    'bonos_gobierno': 0.15,
    'credito_high_yield': 0.10,
    'commodities': 0.05,
    'efectivo': 0.15
}


# ============================================================
# Ejercicio 1: VaR por 3 Metodos
# ============================================================
print("=== Ejercicio 1: VaR por 3 Metodos ===")

print("=== VaR Diario (Portafolio $5,000,000) ===\n")

for confianza in [95, 99]:
    pct_nivel = 100 - confianza
    
    # Historico
    var_hist = np.percentile(retornos_portafolio, pct_nivel)
    
    # Parametrico
    mu = np.mean(retornos_portafolio)
    sigma = np.std(retornos_portafolio, ddof=1)
    z_alpha = stats.norm.ppf(pct_nivel / 100)
    var_param = mu + z_alpha * sigma
    
    # Monte Carlo
    np.random.seed(500)
    futuros = np.random.normal(mu, sigma, 10000)
    var_mc = np.percentile(futuros, pct_nivel)
    
    print(f"Nivel {confianza}%:")
    print(f"  Historico:     {var_hist:+.4%}  (${abs(var_hist * valor_portafolio):,.0f})")
    print(f"  Parametrico:   {var_param:+.4%}  (${abs(var_param * valor_portafolio):,.0f})")
    print(f"  Monte Carlo:   {var_mc:+.4%}  (${abs(var_mc * valor_portafolio):,.0f})")
    print()

print("Observacion: VaR 99% es ~40% mayor que VaR 95% (cola mas gruesa)")


# ============================================================
# Ejercicio 2: CVaR y Perdida en Cola
# ============================================================
print("=== Ejercicio 2: CVaR y Perdida en Cola ===\n")

print("=== CVaR vs VaR ===\n")

for confianza in [95, 99]:
    pct_nivel = 100 - confianza
    
    var_nivel = np.percentile(retornos_portafolio, pct_nivel)
    cola = retornos_portafolio[retornos_portafolio <= var_nivel]
    cvar_val = np.mean(cola)
    ratio = abs(cvar_val) / abs(var_nivel)
    
    print(f"Nivel {confianza}%:")
    print(f"  VaR:      {var_nivel:+.2%}")
    print(f"  CVaR:     {cvar_val:+.2%}")
    print(f"  CVaR/VaR: {ratio:.2f}x")
    print()

print("El CVaR siempre es mayor que el VaR. El ratio CVaR/VaR")
print("aumenta con el nivel de confianza porque la cola tiene")
print("menos observaciones y las perdidas son mas extremas.")


# ============================================================
# Ejercicio 3: Sistema de Stress Testing
# ============================================================
print("\n=== Ejercicio 3: Sistema de Stress Testing ===")

escenarios = {
    'Crisis 2008': {
        'equity_us': -0.40, 'equity_em': -0.55, 'credito_high_yield': -0.30,
        'commodities': -0.45, 'bonos_gobierno': 0.05, 'efectivo': 0.00
    },
    'COVID 2020': {
        'equity_us': -0.34, 'equity_em': -0.25, 'credito_high_yield': -0.15,
        'commodities': -0.30, 'bonos_gobierno': 0.08, 'efectivo': 0.00
    },
    'Dot-com 2000': {
        'equity_us': -0.25, 'equity_em': -0.15, 'credito_high_yield': -0.05,
        'commodities': -0.10, 'bonos_gobierno': 0.10, 'efectivo': 0.00
    },
    'Estanflacion': {
        'equity_us': -0.20, 'equity_em': -0.18, 'credito_high_yield': -0.12,
        'commodities': 0.25, 'bonos_gobierno': -0.15, 'efectivo': -0.05
    }
}

print("=== Stress Testing (Portafolio $5,000,000) ===\n")
print(f"{'Escenario':<18} {'Perdida %':>10} {'Perdida USD':>15}")
print("-" * 45)

for nombre, shocks in escenarios.items():
    perdida = sum(exposiciones_stress[clase] * shocks[clase] for clase in exposiciones_stress)
    perdida_usd = valor_portafolio * abs(perdida)
    print(f"{nombre:<18} {perdida:>9.1%} ${perdida_usd:>14,.0f}")

peor_escenario = min(escenarios.items(), key=lambda x: sum(exposiciones_stress[k] * v for k, v in x[1].items()))
perdida_peor = sum(exposiciones_stress[k] * v for k, v in peor_escenario[1].items())
print(f"\nEscenario mas severo: {peor_escenario[0]} ({perdida_peor:.1%})")
print(f"Capital necesario (peor caso): ${valor_portafolio * abs(perdida_peor):,.0f}")


# ============================================================
# Ejercicio 4: Kupiec Backtesting
# ============================================================
print("\n=== Ejercicio 4: Kupiec Backtesting ===")

np.random.seed(400)
retornos_regimen = np.concatenate([
    np.random.normal(0.0005, 0.015, 300),
    np.random.normal(-0.001, 0.025, 200)
])

ventana = 252
confianza_bt = 95
n_total = len(retornos_regimen)
violaciones = 0
total_bt = 0

vars_predichos = np.full(n_total - ventana, np.nan)

for t in range(ventana, n_total):
    datos_ventana = retornos_regimen[t - ventana:t]
    mu_w = np.mean(datos_ventana)
    sigma_w = np.std(datos_ventana, ddof=1)
    z_alpha = stats.norm.ppf(1 - confianza_bt / 100)
    var_dia = mu_w + z_alpha * sigma_w
    vars_predichos[t - ventana] = var_dia
    
    if retornos_regimen[t] < var_dia:
        violaciones += 1
    total_bt += 1

p_esperado = 1 - confianza_bt / 100
p_observado = violaciones / total_bt

# Kupiec LR statistic
if violaciones == 0:
    lr_stat = -2 * np.log((1 - p_esperado) ** total_bt)
elif violaciones == total_bt:
    lr_stat = -2 * np.log(p_esperado ** total_bt)
else:
    lr_stat = -2 * np.log(
        ((1 - p_esperado) ** (total_bt - violaciones) * p_esperado ** violaciones)
        / ((1 - p_observado) ** (total_bt - violaciones) * p_observado ** violaciones)
    )

p_value = 1 - stats.chi2.cdf(lr_stat, 1)

print("=== Kupiec Backtesting (VaR 95%, ventana 252d) ===\n")
print(f"Periodo completo (500 dias):")
print(f"  Ventanas backtesteadas: {total_bt}")
print(f"  Violaciones: {violaciones} / {total_bt}")
print(f"  Observado: {p_observado:.1%} | Esperado: {p_esperado:.1%}")
print(f"  LR Statistic: {lr_stat:.2f}")
print(f"  p-value: {p_value:.5f}")
print(f"  Rechazar H0: {'SI -> Modelo INADECUADO' if p_value < 0.05 else 'NO -> Modelo adecuado'}")

# Analisis por sub-periodos
print(f"\nRegimen normal (dias 1-300):")
viol_1 = sum(retornos_regimen[ventana:300] < vars_predichos[:300 - ventana])
print(f"  Violaciones: {viol_1} / {300 - ventana}")
print(f"  Conclusión: El cambio de regimen en dia 300 rompe el modelo")

print(f"\nConclusion: El modelo VaR no se adapta a cambios de regimen.")
print(f"Necesita recalibracion o modelos condicionales (GARCH).")


# ============================================================
# Ejercicio 5: Risk Budgeting
# ============================================================
print("\n=== Ejercicio 5: Risk Budgeting ===")

pesos_risk_budget = np.array([0.25, 0.20, 0.15, 0.15, 0.15, 0.10])

matriz_cov_rb = np.array([
    [0.045, 0.012, 0.008, 0.015, 0.006, 0.010],
    [0.012, 0.040, 0.018, 0.020, 0.010, 0.005],
    [0.008, 0.018, 0.025, 0.012, 0.008, 0.003],
    [0.015, 0.020, 0.012, 0.065, 0.015, 0.008],
    [0.006, 0.010, 0.008, 0.015, 0.050, 0.012],
    [0.010, 0.005, 0.003, 0.008, 0.012, 0.030]
])

n_rb = len(pesos_risk_budget)
vol_port_rb = np.sqrt(np.dot(pesos_risk_budget.T, np.dot(matriz_cov_rb, pesos_risk_budget)))

# Contribucion marginal al riesgo
mcr = np.dot(matriz_cov_rb, pesos_risk_budget) / vol_port_rb

# Contribucion total al riesgo
crt = pesos_risk_budget * mcr

# Porcentaje del riesgo
riesgo_pct = crt / np.sum(crt) * 100

print("=== Risk Budgeting ===\n")
print(f"Volatilidad del portafolio: {vol_port_rb:.1%}\n")
print(f"{'Activo':>6} {'Peso':>7} {'Contrib Marginal':>19} {'Contrib Total':>16} {'% del Riesgo':>13}")
print("-" * 63)
for i in range(n_rb):
    print(f"{i + 1:>6} {pesos_risk_budget[i]:>6.1%} {mcr[i]:>17.3f} {crt[i]:>15.3f} {riesgo_pct[i]:>12.1f}%")

idx_top = np.argsort(riesgo_pct)[::-1][:2]
print(f"\nActivos que concentran mas riesgo: {idx_top[0] + 1} y {idx_top[1] + 1} "
      f"({riesgo_pct[idx_top[0]] + riesgo_pct[idx_top[1]]:.1f}% del riesgo total)")
print(f"con solo {pesos_risk_budget[idx_top[0]] + pesos_risk_budget[idx_top[1]]:.0%} del capital. "
      f"La diversificacion es moderada.")
print(f"Para mejorar: reducir peso del activo {idx_top[0] + 1} (el mas volatil) o")
print(f"del activo {idx_top[1] + 1}.")
