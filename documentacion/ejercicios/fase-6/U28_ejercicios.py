# U28: EJERCICIOS — Derivados: Opciones y Modelos de Pricing

import numpy as np

# ============================================================
# Ejercicio 1: BSM Pricer + Griegas
# Implementa Black-Scholes-Merton para calls y puts europeas y
# calcula las 5 griegas (Delta, Gamma, Theta, Vega, Rho).
# Prueba con: S0=100, K=105, r=4%, sigma=30%, T=0.5 anios
# Muestra el precio y todas las griegas para call y put.
# ============================================================
print("=== Ejercicio 1: BSM Pricer + Griegas ===")
s0 = 100.0
k = 105.0
r = 0.04
sigma = 0.30
T = 0.5

# Escribe tu codigo aqui



# Output esperado:
# === BSM Pricer ===
# Parametros: S0=$100, K=$105, r=4.0%, sigma=30.0%, T=0.5 anios
# 
# Call: $7.80
#   Delta: 0.401  Gamma: 0.0253  Theta: -12.34/dia  Vega: $0.190  Rho: $0.171
# Put:  $10.72
#   Delta: -0.599  Gamma: 0.0253  Theta: -10.88/dia  Vega: $0.190  Rho: -$0.319


# ============================================================
# Ejercicio 2: Binomial vs BSM — Convergencia
# Implementa el modelo binomial CRR y compara los precios con BSM
# para 10, 50, 100, 500 y 2000 pasos. Muestra la convergencia.
# Mismos parametros que ejercicio 1 (call).
# ============================================================
print("\n=== Ejercicio 2: Binomial vs BSM ===")
pasos_a_probar = [10, 50, 100, 500, 2000]

# Escribe tu codigo aqui



# Output esperado:
# === Convergencia Binomial → BSM ===
# Pasos    Binomial    BSM         Diferencia
#    10    $7.4501     $7.8005     $0.3504
#    50    $7.7298     $7.8005     $0.0707
#   100    $7.7651     $7.8005     $0.0354
#   500    $7.7934     $7.8005     $0.0071
#  2000    $7.7987     $7.8005     $0.0018
# 
# Con 500+ pasos, la diferencia es < $0.01


# ============================================================
# Ejercicio 3: Volatility Smile
# Dados los siguientes precios de mercado para calls con
# S0=$185 (AAPL), r=4.5%, T=30/365, calcula la IV de cada uno
# y grafica el volatility smile.
# Strikes y precios de mercado:
#   170: $16.50   180: $8.70   185: $6.00
#   190: $3.95   200: $1.50   210: $0.52
# Explica la forma del smile.
# ============================================================
print("\n=== Ejercicio 3: Volatility Smile ===")
s0_aapl = 185.0
r_aapl = 0.045
T_aapl = 30 / 365
strikes_aapl = [170, 180, 185, 190, 200, 210]
precios_mercado = [16.50, 8.70, 6.00, 3.95, 1.50, 0.52]

# Escribe tu codigo aqui



# Output esperado:
# === Volatility Smile AAPL ===
# Strike  Precio Mercado   IV
# $170       $16.50       26.7%
# $180        $8.70       24.9%
# $185        $6.00       25.0%
# $190        $3.95       25.3%
# $200        $1.50       26.0%
# $210        $0.52       27.3%
# 
# Forma: Smile (concava hacia arriba). IV minima cerca de ATM.
# Las opciones OTM (tanto calls altas como puts bajas) tienen
# IV mas alta → mercado asigna mayor probabilidad a movimientos
# extremos que la distribucion log-normal de BSM.


# ============================================================
# Ejercicio 4: Payoff de Estrategias
# Define funciones para graficar los payoffs (sin prima) de:
#   (a) Covered Call: long stock a $100 + short call K=$110
#   (b) Protective Put: long stock a $100 + long put K=$95
#   (c) Bull Spread con calls: long call K=$100, short call K=$110
#   (d) Straddle: long call + long put, K=$100
# Para cada estrategia, reporta: costo, max ganancia, max perdida,
# break-even(s).
# ============================================================
print("\n=== Ejercicio 4: Payoff de Estrategias ===")
precio_compra_stock = 100.0
strike_largo = 100.0
strike_corto = 110.0
strike_put_protect = 95.0
prima_call_atm = 7.80
prima_put_atm = 10.72
prima_call_otm = 2.50  # Call K=110

# Escribe tu codigo aqui



# Output esperado:
# === Analisis de Estrategias ===
# 
# Covered Call (Long Stock + Short Call K=$110):
#   Costo neto: $97.50 | Max Ganancia: $12.50 | Max Perdida: -$97.50
#   Break-even: $97.50
# 
# Protective Put (Long Stock + Long Put K=$95):
#   Costo neto: $110.72 | Max Ganancia: Ilimitada | Max Perdida: -$15.72
#   Break-even: $110.72
# 
# Bull Spread (Long Call K=$100 + Short Call K=$110):
#   Costo neto: $5.30 | Max Ganancia: $4.70 | Max Perdida: -$5.30
#   Break-even: $105.30
# 
# Straddle (Long Call + Long Put K=$100):
#   Costo neto: $18.52 | Max Ganancia: Ilimitada | Max Perdida: -$18.52
#   Break-even (down): $81.48 | Break-even (up): $118.52


# ============================================================
# Ejercicio 5: IV Surface (Superficie de Volatilidad)
# Para un conjunto de opciones con:
#   - Strikes: 80, 90, 100, 110, 120
#   - Vencimientos: 1M (30d), 3M (90d), 6M (180d), 1Y (365d)
# S0=$100, r=5%. Define una funcion que genere precios sinteticos
# con IV variable (skew negativo + term structure) y luego
# calcula la IV de cada opcion. Presenta la superficie como tabla
# (filas: strikes, columnas: vencimientos).
# ============================================================
print("\n=== Ejercicio 5: IV Surface ===")
s0_surf = 100.0
r_surf = 0.05
strikes_surf = [80, 90, 100, 110, 120]
T_surf = [30/365, 90/365, 180/365, 365/365]

# Escribe tu codigo aqui



# Output esperado:
# === Superficie de Volatilidad Implicita ===
# Strike   1M      3M      6M      1Y
# $ 80    28.5%   27.0%   26.0%   25.0%
# $ 90    25.5%   24.5%   23.8%   23.5%
# $100    22.0%   22.0%   22.0%   22.0%
# $110    20.5%   21.0%   21.5%   22.0%
# $120    19.5%   20.5%   21.2%   22.0%
# 
# Observaciones:
#   - Skew: puts OTM (strikes bajos) tienen mayor IV
#   - Term structure: a mayor plazo, menor skew (se aplana)
#   - La IV ATM aumenta ligeramente con el plazo (contango tipico)
