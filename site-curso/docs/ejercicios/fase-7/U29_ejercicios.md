# 📝 Ejercicios: U29 — Fase 7

> [← Volver a ejercicios Fase 7](index.md) | [📥 Descargar .py](U29_ejercicios)

---

```python
# U29: EJERCICIOS — Teoria Moderna de Portafolios (Markowitz)

import numpy as np

# Datos compartidos: 10 activos del S&P 500 (retornos anualizados y covarianza)
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

rf = 0.03  # Tasa libre de riesgo anual

# ============================================================
# Ejercicio 1: Frontera Eficiente (10,000 portafolios)
# Simula 10,000 portafolios aleatorios para los 10 activos.
# Grafica (o reporta en tabla) la nube de portafolios,
# identifica el portafolio de minima varianza (MVP) y el de
# maximo Sharpe (portafolio tangente). Reporta pesos, retorno,
# volatilidad y Sharpe de ambos.
# ============================================================
print("=== Ejercicio 1: Frontera Eficiente ===")

# Escribe tu codigo aqui



# Output esperado:
# === Frontera Eficiente (10,000 simulaciones) ===
# 
# Portafolio de Minima Varianza:
#   Retorno: 7.8% | Volatilidad: 10.2% | Sharpe: 0.47
#   Pesos principales: JNJ 25%, PG 22%, JPM 18%...
# 
# Portafolio de Maximo Sharpe (Tangente):
#   Retorno: 14.5% | Volatilidad: 16.8% | Sharpe: 0.68
#   Pesos principales: NVDA 28%, TSLA 22%, AMZN 18%...
# 
# Equal Weight:
#   Retorno: 11.5% | Volatilidad: 15.2% | Sharpe: 0.56


# ============================================================
# Ejercicio 2: Optimizacion con Restricciones
# Encuentra el MVP y el portafolio de maximo Sharpe usando
# scipy.optimize.minimize con restricciones:
#   - pesos >= 0 (no short-selling)
#   - suma de pesos = 1
# Compara si los pesos son diferentes a la simulacion Monte Carlo.
# ============================================================
print("\\n=== Ejercicio 2: Optimizacion con Restricciones ===")

# Escribe tu codigo aqui



# Output esperado:
# === Optimizacion con SLSQP ===
# 
# Minima Varianza (optimizado):
#   JNJ: 28.5% | PG: 25.2% | JPM: 18.1% | XOM: 12.3% | GOOGL: 8.2% | ...
#   Retorno: 7.8% | Volatilidad: 10.1% | Sharpe: 0.47
# 
# Maximo Sharpe (optimizado):
#   NVDA: 32.1% | TSLA: 28.4% | AMZN: 20.5% | AAPL: 12.0% | MSFT: 7.0% | ...
#   Retorno: 14.8% | Volatilidad: 17.2% | Sharpe: 0.69


# ============================================================
# Ejercicio 3: Capital Market Line (CML)
# Con el portafolio tangente encontrado, calcula la CML.
# Para un inversionista que desea:
#   (a) 10% de retorno: ¿que % en rf y % en tangente?
#   (b) 15% de retorno: ¿que combinacion?
#   (c) ¿Que volatilidad tiene cada combinacion?
# Grafica los puntos sobre la CML.
# ============================================================
print("\\n=== Ejercicio 3: Capital Market Line ===")

# Escribe tu codigo aqui



# Output esperado:
# === Capital Market Line ===
# Portafolio Tangente: ret=14.8%, vol=17.2%, Sharpe=0.69
# Tasa libre de riesgo: 3.0%
# 
# Para retorno objetivo 10.0%:
#   Peso en rf: 38.1% | Peso en tangente: 61.9%
#   Volatilidad: 10.7% | Sharpe (CML): 0.65
# 
# Para retorno objetivo 15.0%:
#   Peso en rf: -1.7% (apalancamiento) | Peso en tangente: 101.7%
#   Volatilidad: 17.5%
#   Nota: Peso negativo en rf implica pedir prestado a la tasa libre.


# ============================================================
# Ejercicio 4: Analisis de Robustez
# Perturba los retornos esperados con ruido normal (sigma=0.5%)
# 100 veces y recalcula los pesos del portafolio tangente.
# ¿Cuanto varian los pesos? ¿Que activos son mas sensibles?
# Reporta el "tracking error" de los pesos (desviacion estandar).
# ============================================================
print("\\n=== Ejercicio 4: Analisis de Robustez ===")

# Escribe tu codigo aqui



# Output esperado:
# === Robustez de Markowitz (100 perturbaciones, sigma=0.5%) ===
# 
# Volatilidad de los pesos del portafolio tangente:
#   NVDA: 8.2% | TSLA: 7.5% | AMZN: 6.1% | AAPL: 5.2%
#   MSFT: 4.8% | GOOGL: 4.5% | JPM: 0.8% | XOM: 0.5%
#   JNJ: 0.3% | PG: 0.2%
# 
# Activos mas sensibles: NVDA, TSLA, AMZN (alto retorno y vol)
# La optimizacion "persigue" pequenios cambios en retornos esperados
# -> Error maximization de Markowitz


# ============================================================
# Ejercicio 5: Comparacion Equal Weight vs Optimizado (10 anios)
# Simula 10 anios (2520 dias) de retornos diarios para los 10
# activos usando los parametros dados. Compara 3 estrategias:
#   - Equal Weight
#   - Minima Varianza
#   - Maximo Sharpe
# Reporta: retorno anualizado, volatilidad, Sharpe, max drawdown.
# ============================================================
print("\\n=== Ejercicio 5: Comparacion de Estrategias ===")

# Escribe tu codigo aqui



# Output esperado:
# === Simulacion 10 Anios (2520 dias) ===
# 
# Estrategia       Ret Anual   Vol Anual   Sharpe   Max Drawdown
# Equal Weight      11.2%       15.3%      0.53       -38.2%
# Min Variance       7.9%       10.5%      0.47       -22.1%
# Max Sharpe        14.1%       17.8%      0.62       -45.5%
# 
# Max Sharpe tiene mayor retorno pero peor drawdown.
# Min Variance es la mas defensiva (menor volatilidad y drawdown).
# Equal Weight es el mejor balance Sharpe vs Drawdown.
```

---

> [📥 Descargar archivo .py](U29_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 7](index.md)
