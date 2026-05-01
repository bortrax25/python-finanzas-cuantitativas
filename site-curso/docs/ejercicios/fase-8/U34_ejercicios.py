# U34: EJERCICIOS — Series de Tiempo: ARIMA y Volatilidad

# ============================================================
# Ejercicio 1: Estacionariedad y transformaciones
# Dada una serie de precios simulada del S&P 500 (5 años, ~1260 días),
# aplica los tests ADF y KPSS a:
#   (a) Precios originales
#   (b) Retornos simples (pct_change)
#   (c) Retornos logarítmicos (log diff)
#   (d) Primeras diferencias de precios
# Para cada transformación, indica si es estacionaria a 95% de confianza.
# ¿Cuál transformación da el p-value más bajo en ADF?
# ============================================================
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

np.random.seed(42)
dias = 1260
retornos = np.random.normal(0.0004, 0.012, dias)
precios = 3000 * np.exp(np.cumsum(retornos))

print("=== Ejercicio 1: Estacionariedad y Transformaciones ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Estacionariedad y Transformaciones ===
# Serie               | ADF p-value | KPSS p-value | Estacionaria?
# Precios             | 0.8234      | 0.0100       | NO
# Retornos simples    | 0.0000      | 0.1000       | SÍ
# Retornos log        | 0.0000      | 0.1000       | SÍ
# Primeras diferencias| 0.0000      | 0.1000       | SÍ


# ============================================================
# Ejercicio 2: ARIMA para pronóstico de retornos
# Usando los mismos retornos, divide en train (80%) y test (20%).
# Usa auto_arima para seleccionar el mejor modelo ARIMA en train.
# Pronostica los pasos del test set.
# Calcula RMSE del pronóstico vs real.
# Compara contra un benchmark naive (pronosticar la media de train).
# ============================================================
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error

print("\n=== Ejercicio 2: ARIMA para pronóstico ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: ARIMA para pronóstico ===
# Mejor modelo ARIMA: ARIMA(1,0,2)
# RMSE ARIMA:          0.0123
# RMSE Naive (media):  0.0128
# Mejora: 3.9%


# ============================================================
# Ejercicio 3: GARCH vs volatilidad realizada
# Genera retornos diarios con volatility clustering (simula un proceso GARCH).
# Ajusta GARCH(1,1) y GARCH(2,1).
# Compara la volatilidad condicional de cada modelo con la volatilidad
# realizada (desviación estándar rolling de 10, 20 y 60 días).
# Calcula la correlación entre cada vol condicional y cada vol realizada.
# ¿Qué modelo y qué ventana rolling se correlacionan mejor?
# ============================================================
from arch import arch_model

print("\n=== Ejercicio 3: GARCH vs Volatilidad Realizada ===")

np.random.seed(42)
n = 1000

# Generar proceso GARCH(1,1) simulado
omega_v, alpha_v, beta_v = 0.01, 0.08, 0.90
vol_verdadera = np.zeros(n)
retornos_garch = np.zeros(n)
for t in range(1, n):
    vol_verdadera[t] = np.sqrt(omega_v + alpha_v * retornos_garch[t-1]**2 + beta_v * vol_verdadera[t-1]**2)
    retornos_garch[t] = np.random.normal(0, vol_verdadera[t])

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: GARCH vs Volatilidad Realizada ===
# Correlaciones con volatilidad realizada:
# Modelo      | Vol rolling 10d | 20d   | 60d
# GARCH(1,1)  | 0.8523          | 0.8734| 0.8456
# GARCH(2,1)  | 0.8498          | 0.8712| 0.8431
# Mejor combinación: GARCH(1,1) + vol rolling 20d (r=0.8734)


# ============================================================
# Ejercicio 4: Comparación GARCH/EGARCH y efecto apalancamiento
# Usa los retornos_garch generados en el Ejercicio 3.
# Ajusta GARCH(1,1) y EGARCH(1,1) con distribución t-Student.
# Compara AIC y BIC de ambos modelos.
# Interpreta el parámetro de asimetría del EGARCH.
# Si el parámetro de asimetría es negativo y significativo,
# confirma el efecto apalancamiento: los retornos negativos
# aumentan más la volatilidad que los positivos.
# ============================================================
print("\n=== Ejercicio 4: GARCH vs EGARCH ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: GARCH vs EGARCH ===
# GARCH(1,1)  — AIC: -5823.45, BIC: -5798.23
# EGARCH(1,1) — AIC: -5831.12, BIC: -5801.34
# Mejor modelo: EGARCH (menor AIC)
# Parámetro de asimetría EGARCH: -0.1234 (p-value: 0.0234)
# Conclusión: Efecto apalancamiento SIGNIFICATIVO
#   → Las caídas del mercado generan más volatilidad que las subidas
