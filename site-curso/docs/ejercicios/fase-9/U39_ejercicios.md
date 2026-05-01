# 📝 Ejercicios: U39 — Fase 9

> [← Volver a ejercicios Fase 9](index.md) | [📥 Descargar .py](U39_ejercicios)

---

```python
# U39: EJERCICIOS — Algorithmic Trading: Estrategias y Backtesting

# ============================================================
# Ejercicio 1: Momentum con backtester
# Implementa una estrategia de momentum para un solo activo:
#   - Señal: +1 si retorno de los últimos 60 días > 0, -1 si < 0
#   - Costo: 10 bps por trade (0.001)
#   - Capital inicial: $100,000
# Usa la clase Backtester de la teoría para evaluar.
# Reporta: retorno total, Sharpe, Sortino, max drawdown, Calmar.
# Compara con buy-and-hold (posición=1 siempre).
# ============================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)
dias = 1260  # 5 años
retornos_sim = np.random.normal(0.0004, 0.012, dias)
precios = 100 * np.exp(np.cumsum(retornos_sim))
precios_serie = pd.Series(precios, index=pd.date_range('2020-01-01', periods=dias, freq='B'), name='activo')

print("=== Ejercicio 1: Momentum con Backtester ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Momentum con Backtester ===
# Estrategia Momentum:
#   Retorno Total:    +23.45%
#   Sharpe Ratio:      0.45
#   Max Drawdown:    -18.23%
# Buy-and-Hold:
#   Retorno Total:    +28.67%
#   Sharpe Ratio:      0.52
#   Max Drawdown:    -22.15%


# ============================================================
# Ejercicio 2: Comparación de 3 estrategias
# Implementa y backtestea 3 estrategias sobre los mismos datos:
#   (a) Momentum (ventana=60 días, umbral=0)
#   (b) Mean reversion (Bollinger: ventana 20, 2 desv. std)
#   (c) Cruce de medias móviles (SMA 20 cruza SMA 50):
#       +1 cuando SMA 20 > SMA 50, -1 cuando SMA 20 < SMA 50
# Grafica las 3 equity curves en el mismo plot.
# Reporta Sharpe, Sortino y max drawdown para cada una.
# ============================================================
print("\\n=== Ejercicio 2: Comparación de 3 Estrategias ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Comparación de 3 Estrategias ===
# Estrategia          | Sharpe | Sortino | Max DD
# Momentum            | 0.45   | 0.62    | -18.2%
# Mean Reversion      | 0.23   | 0.31    | -14.5%
# Cruce SMA           | 0.38   | 0.51    | -20.1%


# ============================================================
# Ejercicio 3: Pairs Trading
# Genera 2 series de precios cointegradas:
#   - Activo A: random walk
#   - Activo B: 0.8 * A + ruido estacionario (reversión)
# Verifica cointegración con el test de Engle-Granger (coint).
# Implementa pairs trading con z-score:
#   - Calcula spread = A - hedge_ratio * B
#   - z_score = (spread - media_roll(60)) / std_roll(60)
#   - Entrada: |z| > 2.0, Salida: |z| < 0.5
# Backtestea y compara Sharpe vs buy-and-hold de A y B.
# ============================================================
from statsmodels.tsa.stattools import coint

print("\\n=== Ejercicio 3: Pairs Trading ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Pairs Trading ===
# Test de cointegración: p-value = 0.0001 (COINTEGRADOS)
# Hedge ratio: 0.8123
# Estrategia          | Sharpe | Max DD
# Pairs Trading       | 0.67   | -8.2%
# Buy-and-Hold A      | 0.52   | -22.1%
# Buy-and-Hold B      | 0.48   | -19.8%


# ============================================================
# Ejercicio 4: Walk-forward optimization
# Implementa walk-forward backtest para optimizar la ventana
# de momentum de la estrategia del Ejercicio 1.
# Prueba ventanas: [20, 40, 60, 80, 100] días.
# Configuración walk-forward:
#   - Ventana train: 2 años (~504 días)
#   - Ventana test: 6 meses (~126 días)
#   - Paso: 3 meses (~63 días)
# Reporta:
#   - Parámetro óptimo en cada ventana
#   - Sharpe out-of-sample acumulado
#   - Compara con usar siempre ventana=60 (naive)
# ¿El walk-forward supera al naive?
# ============================================================
print("\\n=== Ejercicio 4: Walk-Forward Optimization ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Walk-Forward Optimization ===
# Ventana | Train      | Test       | Param óptimo | Sharpe OOS
# 1       | 2020-2021  | 2022 H1    | 60           | 0.34
# 2       | 2020-2021  | 2022 H2    | 40           | 0.41
# 3       | 2021-2022  | 2023 H1    | 80           | 0.28
# ...
# Walk-forward Sharpe acumulado: 0.38
# Naive (ventana=60) Sharpe:     0.35
# Mejora walk-forward: +8.6%
```

---

> [📥 Descargar archivo .py](U39_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 9](index.md)
