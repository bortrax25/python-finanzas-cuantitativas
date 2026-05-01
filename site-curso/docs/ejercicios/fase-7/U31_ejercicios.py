# U31: EJERCICIOS — Gestion de Riesgo: VaR, CVaR y Stress Testing

import numpy as np

# Datos compartidos: retornos diarios simulados de un portafolio
np.random.seed(300)
n_obs = 500
# Portafolio de $5M con 4 activos
retornos_portafolio = np.random.normal(-0.0002, 0.018, n_obs)
valor_portafolio = 5_000_000

# Datos para stress tests: exposiciones a clases de activos
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
# Para el portafolio de $5M, calcula el VaR diario al 95% y 99%
# usando los tres metodos:
#   (a) Historico
#   (b) Parametrico (asumiendo normalidad)
#   (c) Monte Carlo (10,000 simulaciones, param. desde historico)
# Reporta el VaR en % y en USD. Compara los resultados.
# ============================================================
print("=== Ejercicio 1: VaR por 3 Metodos ===")

# Escribe tu codigo aqui



# Output esperado:
# === VaR Diario (Portafolio $5,000,000) ===
# 
# Nivel 95%:
#   Historico:     -3.12%  ($156,000)
#   Parametrico:   -3.01%  ($150,500)
#   Monte Carlo:   -3.05%  ($152,500)
# 
# Nivel 99%:
#   Historico:     -4.45%  ($222,500)
#   Parametrico:   -4.23%  ($211,500)
#   Monte Carlo:   -4.31%  ($215,500)
# 
# Observacion: VaR 99% es ~40% mayor que VaR 95% (cola mas gruesa)


# ============================================================
# Ejercicio 2: CVaR y Perdida en Cola
# Calcula el CVaR (Expected Shortfall) al 95% y 99% para el
# mismo portafolio. Compara el ratio CVaR/VaR para cada nivel
# de confianza. ¿Por que el ratio es mayor al 99%?
# ============================================================
print("\n=== Ejercicio 2: CVaR y Perdida en Cola ===")

# Escribe tu codigo aqui



# Output esperado:
# === CVaR vs VaR ===
# 
# Nivel 95%:
#   VaR:      -3.12%
#   CVaR:     -3.85%
#   CVaR/VaR: 1.23x
# 
# Nivel 99%:
#   VaR:      -4.45%
#   CVaR:     -5.62%
#   CVaR/VaR: 1.26x
# 
# El CVaR siempre es mayor que el VaR. El ratio CVaR/VaR
# aumenta con el nivel de confianza porque la cola tiene
# menos observaciones y las perdidas son mas extremas.


# ============================================================
# Ejercicio 3: Sistema de Stress Testing
# Define 4 escenarios de stress con shocks a 6 clases de activos:
#   - Crisis 2008: equity_us -40%, equity_em -55%, credito -30%,
#                   commodities -45%, bonos +5%, efectivo 0%
#   - COVID 2020: equity_us -34%, equity_em -25%, credito -15%,
#                 commodities -30%, bonos +8%, efectivo 0%
#   - Dot-com 2000: equity_us -25%, equity_em -15%, credito -5%,
#                   commodities -10%, bonos +10%, efectivo 0%
#   - Estanflacion: equity_us -20%, equity_em -18%, credito -12%,
#                   commodities +25%, bonos -15%, efectivo -5%
# Aplica cada escenario y reporta la perdida en % y USD.
# ============================================================
print("\n=== Ejercicio 3: Sistema de Stress Testing ===")

# Escribe tu codigo aqui



# Output esperado:
# === Stress Testing (Portafolio $5,000,000) ===
# 
# Escenario          Perdida %     Perdida USD
# Crisis 2008         -22.8%       -$1,137,500
# COVID 2020          -17.9%       -$895,000
# Dot-com 2000        -13.7%       -$685,000
# Estanflacion         -9.4%       -$470,000
# 
# Escenario mas severo: Crisis 2008 (-22.8%)
# Capital necesario (peor caso): $1,137,500


# ============================================================
# Ejercicio 4: Kupiec Backtesting
# Implementa un sistema de backtesting rolling con ventana de 252
# dias. Calcula el VaR parametrico al 95% en cada ventana y
# registra las violaciones. Aplica el test de Kupiec para evaluar
# si el modelo es adecuado.
# Usa 500 dias de retornos simulados con cambio de regimen a
# partir del dia 300 (aumenta la volatilidad).
# ============================================================
print("\n=== Ejercicio 4: Kupiec Backtesting ===")

np.random.seed(400)
# Retornos con cambio de regimen
retornos_regimen = np.concatenate([
    np.random.normal(0.0005, 0.015, 300),   # Regimen normal
    np.random.normal(-0.001, 0.025, 200)     # Regimen volatil (crisis)
])

# Escribe tu codigo aqui



# Output esperado:
# === Kupiec Backtesting (VaR 95%, ventana 252d) ===
# 
# Periodo completo (500 dias):
#   Ventanas backtesteadas: 248
#   Violaciones: 34 / 248
#   Observado: 13.7% | Esperado: 5.0%
#   LR Statistic: 18.42
#   p-value: 0.00002
#   Rechazar H0: SI -> Modelo INADECUADO
# 
# Regimen normal (dias 1-300):
#   Violaciones: 5 / 48
#   Observado: 10.4% | Esperado: 5.0%
#   Conclusión: El cambio de regimen en dia 300 rompe el modelo
# 
# Conclusion: El modelo VaR no se adapta a cambios de regimen.
# Necesita recalibracion o modelos condicionales (GARCH).


# ============================================================
# Ejercicio 5: Risk Budgeting
# Para un portafolio de 6 activos con los siguientes datos:
#   Pesos: [25%, 20%, 15%, 15%, 15%, 10%]
#   Matriz de covarianza (proporcionada)
# Calcula la contribucion porcentual de cada activo al riesgo
# total. Identifica cuales activos concentran el mayor riesgo
# y evalua si la diversificacion es adecuada.
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

# Escribe tu codigo aqui



# Output esperado:
# === Risk Budgeting ===
# 
# Volatilidad del portafolio: 16.8%
# 
# Activo  Peso    Contribucion Marginal  Contribucion Total  % del Riesgo
#   1    25.0%        0.184                0.046                27.4%
#   2    20.0%        0.162                0.032                19.1%
#   3    15.0%        0.120                0.018                10.7%
#   4    15.0%        0.215                0.032                19.1%
#   5    15.0%        0.168                0.025                14.9%
#   6    10.0%        0.148                0.015                 8.9%
# 
# Activos que concentran mas riesgo: 1 y 4 (46.5% del riesgo total)
# con solo 40% del capital. La diversificacion es moderada.
# Para mejorar: reducir peso del activo 4 (el mas volatil) o
# del activo 1.
