# U23: EJERCICIOS — APIs y Datos Financieros

import json
import time
import pandas as pd
import numpy as np

# ============================================================
# Ejercicio 1: Descarga y análisis de un ticker con yfinance
# Descarga 2 años de datos de AAPL usando yfinance (start="2022-01-01", end="2023-12-31").
# NOTA: Si no tienes internet, usa el bloque de datos simulados comentado abajo.
# Calcula:
#   - Precio inicial y final
#   - Retorno total (%)
#   - Volatilidad anualizada (%)
#   - Máximo drawdown (%)
#   - Días positivos (%)
# Extrae de ticker.info: nombre largo, sector, marketCap, trailingPE, beta.
# ============================================================
print("=== Ejercicio 1: Análisis de AAPL ===")

# ---- BLOQUE SIMULADO (usar si no hay internet) ----
# Simula 2 años de precios de AAPL (~504 días hábiles)
np.random.seed(42)
fechas_2y = pd.date_range("2022-01-03", "2023-12-29", freq="B")
retornos_sim = np.random.normal(0.0004, 0.015, len(fechas_2y))
retornos_sim[0] = 0
precios_aapl = pd.Series(180 * np.cumprod(1 + retornos_sim), index=fechas_2y, name="AAPL")
# Info simulada
info_aapl = {
    "longName": "Apple Inc.",
    "sector": "Technology",
    "marketCap": 2_800_000_000_000,
    "trailingPE": 28.5,
    "beta": 1.25,
}
# Descomenta la línea siguiente para usar datos reales de yfinance:
# import yfinance as yf
# aapl = yf.Ticker("AAPL")
# precios_aapl = aapl.history(start="2022-01-01", end="2023-12-31")["Close"]
# info_aapl = aapl.info
# ------------------------------------------------

# Escribe tu código aquí



# Output esperado:
# AAPL: Apple Inc.
# Sector: Technology | Market Cap: $2,800.00B | PER: 28.5 | Beta: 1.25
# Precio inicial (2022-01-03): $180.00
# Precio final (2023-12-29): $2XX.XX
# Retorno total: XX.XX%
# Volatilidad anualizada: 2X.XX%
# Máximo Drawdown: -XX.XX%
# Días positivos: 5X.X%


# ============================================================
# Ejercicio 2: Screening de múltiples tickers
# Dados 10 tickers con precios simulados (ver abajo), calcula:
#   - Retorno total de cada uno (último / primero - 1)
#   - Volatilidad anualizada de cada uno
#   - Sharpe Ratio (retorno_anual / vol_anual, con tasa libre=0.03)
#   - Ranking top 3 y bottom 3 por Sharpe Ratio
# Muestra tabla resumen ordenada por Sharpe descendente.
# ============================================================
print("\n=== Ejercicio 2: Screening de 10 tickers ===")

# Datos simulados de 10 tickers
np.random.seed(123)
fechas_sc = pd.date_range("2023-01-03", "2023-12-29", freq="B")
tickers_sc = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
              "META", "TSLA", "JPM", "XOM", "WMT"]
spots_sc = [150, 310, 140, 100, 250, 300, 200, 140, 110, 150]
sigmas_sc = [0.22, 0.20, 0.25, 0.28, 0.40, 0.35, 0.50, 0.22, 0.24, 0.15]
mus_sc = [0.10, 0.12, 0.08, 0.05, 0.30, 0.25, -0.05, 0.09, 0.07, 0.06]

df_sc = pd.DataFrame(index=fechas_sc)
for i, ticker in enumerate(tickers_sc):
    ret = np.random.normal(mus_sc[i] / 252, sigmas_sc[i] / np.sqrt(252), len(fechas_sc))
    ret[0] = 0
    df_sc[ticker] = spots_sc[i] * np.cumprod(1 + ret)

# Escribe tu código aquí



# Output esperado:
# Ranking por Sharpe Ratio (top 3 + bottom 3):
# Ticker    Ret. Total    Ret. Anual    Vol. Anual    Sharpe
# NVDA      XX.XX%        XX.XX%        XX.XX%        X.XX
# META      XX.XX%        XX.XX%        XX.XX%        X.XX
# MSFT      XX.XX%        XX.XX%        XX.XX%        X.XX
# ...
# AMZN      XX.XX%        XX.XX%        XX.XX%        X.XX
# XOM       XX.XX%        XX.XX%        XX.XX%        X.XX
# TSLA      XX.XX%        XX.XX%        XX.XX%        X.XX


# ============================================================
# Ejercicio 3: Cliente para API REST con rate limiting
# Implementa:
#   - Clase BaseAPIClient con:
#       __init__(self, api_key, base_url, rate_limit=0.5)
#       get(self, endpoint, params) -> dict (con manejo de errores y rate limiting)
#   - Clase PrecioClient(BaseAPIClient) que herede y sobrescriba get
#     para simular respuestas de una API de precios.
#   - Método precio_diario(ticker) que retorne un dict con:
#       {"ticker": ticker, "precios": [lista de 5 precios], "moneda": "USD"}
# Simula llamadas a 3 tickers diferentes respetando rate limiting.
# Mide el tiempo total y verifica que se respetó el rate limit.
# ============================================================
print("\n=== Ejercicio 3: API Client con rate limiting ===")

# Escribe tu código aquí



# Output esperado:
# [PrecioClient] AAPL: 5 precios descargados
# [PrecioClient] MSFT: 5 precios descargados
# [PrecioClient] TSLA: 5 precios descargados
# Tiempo total: X.XXs (esperado ≈ 1.5s con rate_limit=0.5)
# Rate limit respetado: True


# ============================================================
# Ejercicio 4: Pipeline de datos macro + acciones
# Simula dos fuentes de datos y combínalas:
#   Fuente 1: Precios diarios del S&P 500 (252 días, 2023, seed=42)
#   Fuente 2: Tasa de Fondos Federales (FRED FEDFUNDS) — datos mensuales simulados
#             que aumentan de 4.25% a 5.50% durante 2023
# Tareas:
#   - Alinear los datos: resamplear la tasa mensual a frecuencia diaria (forward fill)
#   - Calcular la correlación entre retornos diarios del S&P y cambios en la tasa
#   - Calcular retorno del S&P en meses donde la tasa subió vs meses donde se mantuvo
#   - Mostrar un resumen comparativo
# ============================================================
print("\n=== Ejercicio 4: Pipeline datos macro + acciones ===")

# Escribe tu código aquí



# Output esperado:
# Datos S&P 500: 252 días (2023)
# Datos FEDFUNDS: 12 meses → 252 días (forward filled)
# Correlación retornos S&P vs Δ tasa: -0.XX
# Meses con alza de tasa (X meses):
#   Retorno S&P promedio: +X.XX%
# Meses sin cambio de tasa (X meses):
#   Retorno S&P promedio: +X.XX%
