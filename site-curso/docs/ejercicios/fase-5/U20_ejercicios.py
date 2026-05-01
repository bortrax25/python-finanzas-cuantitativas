# U20: EJERCICIOS — Pandas Fundamentos

import pandas as pd
import numpy as np

# ============================================================
# Ejercicio 1: Serie de precios con DatetimeIndex
# Crea una Serie de pandas con:
#   - 252 días hábiles desde 2024-01-02 (freq="B")
#   - Precios simulados: empieza en 1000 y aplica retornos diarios N(0.0004, 0.012)
#   - Usa np.random.seed(42) para reproducibilidad
# Calcula e imprime:
#   - Primer y último precio
#   - Retorno acumulado total (último / primero - 1)
#   - Mejor día (fecha y retorno %)
#   - Peor día (fecha y retorno %)
#   - Volatilidad anualizada (std diaria * sqrt(252))
# ============================================================
print("=== Ejercicio 1: Serie de precios ===")

# Escribe tu código aquí



# Output esperado:
# Primer precio (2024-01-02): $1,000.00
# Último precio (2024-12-31): $1,1XX.XX
# Retorno acumulado: 1X.XX%
# Mejor día: 2024-XX-XX (+X.XX%)
# Peor día: 2024-XX-XX (-X.XX%)
# Volatilidad anualizada: 1X.XX%


# ============================================================
# Ejercicio 2: DataFrame de múltiples tickers con estadísticas
# Crea un DataFrame con 252 días (desde 2024-01-02) y 3 tickers:
#   AAPL, MSFT, TSLA — cada uno con precios simulados desde 150, 310, 250
#   usando np.random.seed(42), retornos N(0.0005, 0.015)
# Calcula:
#   - Retornos diarios de cada ticker
#   - Volatilidad anualizada de cada uno
#   - Matriz de correlación entre los 3 tickers
#   - Días en que AAPL y MSFT subieron simultáneamente (%)
#   - Ticker con mayor retorno acumulado
# ============================================================
print("\n=== Ejercicio 2: Múltiples tickers ===")

# Escribe tu código aquí



# Output esperado:
# Volatilidad anualizada:
# AAPL: 2X.XX%
# MSFT: 2X.XX%
# TSLA: 2X.XX%
# Matriz de correlación:
#        AAPL   MSFT   TSLA
# AAPL  1.000  0.XXX  0.XXX
# MSFT  0.XXX  1.000  0.XXX
# TSLA  0.XXX  0.XXX  1.000
# Días AAPL y MSFT suben juntos: 2X.X%
# Ticker con mayor retorno acumulado: XXXX (1X.XX%)


# ============================================================
# Ejercicio 3: Resampleo y agregación temporal
# Usando el DataFrame del ejercicio anterior (3 tickers, 252 días):
#   - Calcula OHLC semanal (W-FRI) para AAPL
#   - Calcula retorno mensual (ME) para cada ticker
#   - Encuentra el mejor y peor mes de cada ticker (por retorno mensual)
#   - Calcula volumen promedio mensual simulado (usa np.random.randint)
#   - Muestra el resumen mensual de AAPL con columnas: retorno, vol_promedio, max, min
# ============================================================
print("\n=== Ejercicio 3: Resampleo temporal ===")

# Escribe tu código aquí



# Output esperado:
# OHLC Semanal AAPL (primeras 4 semanas):
#               open    high    low     close
# 2024-01-05    ...
# 2024-01-12    ...
# 2024-01-19    ...
# 2024-01-26    ...
# Mejor mes AAPL: 2024-XX (+X.XX%)
# Peor mes AAPL: 2024-XX (-X.XX%)
# Mejor mes MSFT: 2024-XX (+X.XX%)
# Peor mes TSLA: 2024-XX (-X.XX%)


# ============================================================
# Ejercicio 4: Drawdown y métricas de riesgo
# Con la serie de precios del S&P 500 simulada:
#   - Crea una serie de 5 años (2019-01-02 a 2023-12-29) de precios empezando en 2500
#     con retornos diarios N(0.0003, 0.010) y seed=42
#   - Calcula el drawdown diario: (precio / precio_maximo_historico - 1)
#   - Encuentra el máximo drawdown (valor y fecha)
#   - Encuentra la duración del peor drawdown en días (desde pico hasta recuperación)
#   - Calcula el Calmar Ratio: retorno_anualizado / abs(max_drawdown)
#     donde retorno_anualizado = (precio_final / precio_inicial)^(1/años) - 1
#   - Calcula cuántos días estuvo en drawdown > 5%
# ============================================================
print("\n=== Ejercicio 4: Drawdown y métricas de riesgo ===")

# Escribe tu código aquí



# Output esperado:
# Precio inicial (2019-01-02): $2,500.00
# Precio final (2023-12-29): $X,XXX.XX
# Máximo Drawdown: -XX.XX% en 2020-XX-XX
# Duración del peor drawdown: XXX días
# Retorno anualizado: X.XX%
# Calmar Ratio: X.XX
# Días en drawdown > 5%: XXX días
