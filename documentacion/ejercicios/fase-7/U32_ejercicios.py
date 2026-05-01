# U32: EJERCICIOS — Optimizacion Avanzada de Portafolios

import numpy as np
import pandas as pd

# Datos compartidos: 8 activos con retornos y covarianza
nombres_32 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']

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

# ============================================================
# Ejercicio 1: Ledoit-Wolf Shrinkage
# Compara los portafolios de minima varianza construidos con la
# matriz de covarianza muestral vs la matriz Ledoit-Wolf
# (usando sklearn.covariance.LedoitWolf si esta disponible o
# implementando manualmente). Usa datos simulados con pocos
# periodos (T=40) vs muchos (T=500) para comparar.
# ¿La matriz shrinkage produce pesos mas estables en T bajos?
# ============================================================
print("=== Ejercicio 1: Ledoit-Wolf Shrinkage ===")

# Escribe tu codigo aqui



# Output esperado:
# === Ledoit-Wolf Shrinkage ===
# 
# Matriz muestral (T=40 observaciones):
#   Volatilidad MVP: 12.8% | Min peso: 2.1% | Max peso: 35.2%
# 
# Matriz Ledoit-Wolf (T=40):
#   Volatilidad MVP: 12.4% | Min peso: 5.8% | Max peso: 28.1%
# 
# Matriz muestral (T=500 observaciones):
#   Volatilidad MVP: 11.5% | Min peso: 4.5% | Max peso: 30.5%
# 
# Matriz Ledoit-Wolf (T=500):
#   Volatilidad MVP: 11.6% | Min peso: 5.1% | Max peso: 29.2%
# 
# Shrinkage es mas importante con pocos datos. Con T=500,
# la diferencia es minima (la muestra converge a la verdad).


# ============================================================
# Ejercicio 2: Risk Parity vs Equal Weight
# Implementa Risk Parity para los 8 activos. Compara los pesos
# con Equal Weight. Muestra la contribucion al riesgo de cada
# activo en ambas estrategias. ¿Que activos reciben mas peso
# en Risk Parity? ¿Por que?
# ============================================================
print("\n=== Ejercicio 2: Risk Parity vs Equal Weight ===")

# Escribe tu codigo aqui



# Output esperado:
# === Risk Parity vs Equal Weight ===
# 
# Activo  Volatilidad  EW_Peso  RP_Peso  EW_Riesgo%  RP_Riesgo%
# A4      34.6%        12.5%     5.2%      17.1%      12.5%
# A2      30.0%        12.5%     5.9%      15.8%      12.5%
# A6      28.3%        12.5%     6.3%      14.0%      12.5%
# A7      26.5%        12.5%     6.8%      13.2%      12.5%
# A3      22.4%        12.5%     8.1%      11.5%      12.5%
# A1      20.0%        12.5%     9.1%      10.2%      12.5%
# A5      15.8%        12.5%    11.5%       8.5%      12.5%
# A8      13.4%        12.5%    47.1%       9.7%      12.5%
# 
# Risk Parity asigna mas peso a activos de baja volatilidad
# y menos a activos de alta volatilidad. Esto iguala la
# contribucion al riesgo de cada activo (~12.5% cada uno).


# ============================================================
# Ejercicio 3: HRP Completo
# Implementa Hierarchical Risk Parity. Pasos:
#   1. Calcular matriz de distancias basada en correlacion
#   2. Clustering jerarquico (method='ward')
#   3. Quasi-diagonalization (reordenar activos segun dendrograma)
#   4. Recursive bisection: asignar pesos de abajo hacia arriba
# Aplica a los 8 activos. Compara pesos y diversificacion con
# Markowitz (max Sharpe) y Equal Weight.
# ============================================================
print("\n=== Ejercicio 3: HRP Completo ===")

# Escribe tu codigo aqui



# Output esperado:
# === Hierarchical Risk Parity ===
# 
# Matriz de correlacion:
#     A1    A2    A3    A4    A5    A6    A7    A8
# A1 1.00  0.30  0.56  0.29  0.25  0.27  0.23  0.19
# A2 0.30  1.00  0.45  0.24  0.25  0.24  0.23  0.20
# ...
# 
# Pesos HRP:
# A1: 13.5% | A2: 8.2% | A3: 10.1% | A4: 5.8%
# A5: 18.2% | A6: 9.5% | A7: 8.8% | A8: 25.9%
# 
# Comparacion:
# Estrategia    Volatilidad   Sharpe   Concentracion (HHI)
# Equal Weight    16.5%        0.52       0.125
# Max Sharpe      19.2%        0.62       0.385
# HRP             15.8%        0.55       0.168
# 
# HRP tiene volatilidad similar a EW pero mejor Sharpe.
# Mejor diversificado que Max Sharpe (menor concentracion).


# ============================================================
# Ejercicio 4: Simulacion de Rebalanceo
# Simula 5 anios (1260 dias) de rebalanceo para un portafolio
# 60/40 (acciones/bonos) con frecuencias: mensual (21d),
# trimestral (63d) y anual (252d). Costo de transaccion: 0.1%.
# Calcula: turnover acumulado, costos totales, retorno neto.
# ¿Cual frecuencia optimiza el trade-off?
# ============================================================
print("\n=== Ejercicio 4: Simulacion de Rebalanceo ===")

np.random.seed(600)
n_dias_sim = 1260  # 5 anios
# Acciones: retorno anual 8%, vol 18%
ret_acciones = np.random.normal(0.08/252, 0.18/np.sqrt(252), n_dias_sim)
# Bonos: retorno anual 3%, vol 6%
ret_bonos = np.random.normal(0.03/252, 0.06/np.sqrt(252), n_dias_sim)

# Escribe tu codigo aqui



# Output esperado:
# === Simulacion de Rebalanceo 5 Anios ===
# 
# Frecuencia   Ret Bruto   Turnover   Costos    Ret Neto
# Mensual       57.2%       285%      2.85%     54.4%
# Trimestral    57.6%       142%      1.42%     56.2%
# Anual         57.4%        48%      0.48%     56.9%
# Sin rebalanceo 55.1%        0%      0.00%     55.1%
# 
# Frecuencia optima: Anual (max retorno neto, min turnover)
# Mensual genera mucho turnover y costos sin mejorar retorno.
# Sin rebalanceo, la deriva de pesos reduce diversificacion.


# ============================================================
# Ejercicio 5: Comparacion de 5 Estrategias (10 anios)
# Simula 10 anios (2520 dias) con los 8 activos. Compara:
#   (a) Equal Weight
#   (b) Minima Varianza
#   (c) Maximo Sharpe
#   (d) Risk Parity
#   (e) HRP
# Reporta: retorno anualizado, volatilidad, Sharpe, Sortino,
# max drawdown, turnover anual y retorno neto de costos (0.1%).
# Rebalanceo anual. ¿Cual estrategia es mas robusta?
# ============================================================
print("\n=== Ejercicio 5: Comparacion de 5 Estrategias (10 anios) ===")

np.random.seed(777)
n_dias_10y = 2520
rets_anuales_params = retornos_esperados_32 / 252
cov_diaria_params = matriz_cov_32 / 252

retornos_simulados = np.random.multivariate_normal(
    rets_anuales_params, cov_diaria_params, n_dias_10y
)

# Escribe tu codigo aqui



# Output esperado:
# === Comparacion de Estrategias (10 anios, rebalanceo anual) ===
# 
# Estrategia    Ret Bruto  Vol   Sharpe  Sortino  Max DD   Turnover  Ret Neto
# Equal Weight   10.8%    16.1%   0.49    0.71    -35.2%    0.0%      10.8%
# Min Variance    8.2%    12.5%   0.42    0.58    -25.1%   48.2%       8.0%
# Max Sharpe     12.5%    18.5%   0.51    0.72    -42.1%   78.5%      12.0%
# Risk Parity     9.5%    14.2%   0.46    0.65    -30.2%   32.1%       9.3%
# HRP            10.2%    14.8%   0.49    0.68    -32.5%   25.8%      10.1%
# 
# Conclusion:
#   - Max Sharpe: mayor retorno pero mayor volatilidad y drawdown
#   - Min Variance: mas defensivo, menor drawdown
#   - HRP: mejor balance Sharpe/Drawdown, bajo turnover
#   - Risk Parity: buena diversificacion, moderado turnover
#   - Equal Weight: benchmark simple, cero turnover
# 
# Estrategia mas robusta (mejor Sharpe neto + menor drawdown): HRP
