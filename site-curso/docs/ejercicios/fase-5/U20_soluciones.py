# U20: SOLUCIONES — Pandas Fundamentos

import pandas as pd
import numpy as np

# ============================================================
# Ejercicio 1: Serie de precios con DatetimeIndex
# ============================================================
print("=== Ejercicio 1: Serie de precios ===")

np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=252, freq="B")
retornos = np.random.normal(0.0004, 0.012, 252)
retornos[0] = 0
precios = pd.Series(1000 * np.cumprod(1 + retornos), index=fechas, name="SPX")

primer_precio = precios.iloc[0]
ultimo_precio = precios.iloc[-1]
retorno_acumulado = (ultimo_precio / primer_precio - 1) * 100

ret_diarios = precios.pct_change().dropna()
mejor_dia_idx = ret_diarios.idxmax()
peor_dia_idx = ret_diarios.idxmin()
vol_anualizada = ret_diarios.std() * np.sqrt(252) * 100

print(f"Primer precio ({precios.index[0].date()}): ${primer_precio:,.2f}")
print(f"Último precio ({precios.index[-1].date()}): ${ultimo_precio:,.2f}")
print(f"Retorno acumulado: {retorno_acumulado:.2f}%")
print(f"Mejor día: {mejor_dia_idx.date()} (+{ret_diarios.max()*100:.2f}%)")
print(f"Peor día: {peor_dia_idx.date()} ({ret_diarios.min()*100:.2f}%)")
print(f"Volatilidad anualizada: {vol_anualizada:.2f}%")

# ============================================================
# Ejercicio 2: DataFrame de múltiples tickers con estadísticas
# ============================================================
print("\n=== Ejercicio 2: Múltiples tickers ===")

np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=252, freq="B")

precios_iniciales = {"AAPL": 150.0, "MSFT": 310.0, "TSLA": 250.0}
tickers = list(precios_iniciales.keys())

df_precios = pd.DataFrame(index=fechas)
for ticker in tickers:
    retornos_t = np.random.normal(0.0005, 0.015, 252)
    retornos_t[0] = 0
    df_precios[ticker] = precios_iniciales[ticker] * np.cumprod(1 + retornos_t)

retornos = df_precios.pct_change().dropna()

vol_anualizada = {}
for ticker in tickers:
    vol = retornos[ticker].std() * np.sqrt(252) * 100
    vol_anualizada[ticker] = vol

print("Volatilidad anualizada:")
for ticker, vol in vol_anualizada.items():
    print(f"{ticker}: {vol:.2f}%")

corr_matrix = retornos.corr()
print("Matriz de correlación:")
print(corr_matrix.round(3))

suben_juntos = ((retornos["AAPL"] > 0) & (retornos["MSFT"] > 0)).mean() * 100
print(f"Días AAPL y MSFT suben juntos: {suben_juntos:.1f}%")

retorno_acum = {}
for ticker in tickers:
    ret = (df_precios[ticker].iloc[-1] / df_precios[ticker].iloc[0] - 1) * 100
    retorno_acum[ticker] = ret

mejor_ticker = max(retorno_acum, key=retorno_acum.get)
print(f"Ticker con mayor retorno acumulado: {mejor_ticker} ({retorno_acum[mejor_ticker]:.2f}%)")

# ============================================================
# Ejercicio 3: Resampleo y agregación temporal
# ============================================================
print("\n=== Ejercicio 3: Resampleo temporal ===")

# OHLC semanal de AAPL
aapl = df_precios["AAPL"]
ohlc_semanal = aapl.resample("W-FRI").ohlc()
print("OHLC Semanal AAPL (primeras 4 semanas):")
print(ohlc_semanal.head(4))

# Retornos mensuales
mensual = df_precios.resample("ME").last()
retornos_mensuales = mensual.pct_change().dropna()

print("Mejor/Peor mes por ticker:")
for ticker in tickers:
    mejor_mes = retornos_mensuales[ticker].idxmax()
    peor_mes = retornos_mensuales[ticker].idxmin()
    print(f"Mejor mes {ticker}: {mejor_mes.strftime('%Y-%m')} (+{retornos_mensuales[ticker].max()*100:.2f}%)")
    print(f"Peor mes {ticker}: {peor_mes.strftime('%Y-%m')} ({retornos_mensuales[ticker].min()*100:.2f}%)")

# ============================================================
# Ejercicio 4: Drawdown y métricas de riesgo
# ============================================================
print("\n=== Ejercicio 4: Drawdown y métricas de riesgo ===")

np.random.seed(42)
fechas_5y = pd.date_range("2019-01-02", "2023-12-29", freq="B")
retornos_5y = np.random.normal(0.0003, 0.010, len(fechas_5y))
retornos_5y[0] = 0
spx = pd.Series(2500 * np.cumprod(1 + retornos_5y), index=fechas_5y, name="SPX")

precio_inicial = spx.iloc[0]
precio_final = spx.iloc[-1]

# Drawdown
precio_maximo_historico = spx.cummax()
drawdown = spx / precio_maximo_historico - 1

max_dd = drawdown.min()
fecha_max_dd = drawdown.idxmin()

# Duración del peor drawdown
drawdown_periodo = drawdown[drawdown < 0]
pico_idx = drawdown[:fecha_max_dd][drawdown[:fecha_max_dd] == 0].index[-1] if len(drawdown[:fecha_max_dd][drawdown[:fecha_max_dd] == 0]) > 0 else drawdown.index[0]
recuperacion = drawdown[fecha_max_dd:][drawdown[fecha_max_dd:] == 0]
if len(recuperacion) > 0:
    fecha_recuperacion = recuperacion.index[0]
    duracion_dd = (fecha_recuperacion - pico_idx).days
else:
    duracion_dd = (drawdown.index[-1] - pico_idx).days

# Calmar Ratio
años = (fechas_5y[-1] - fechas_5y[0]).days / 365.25
retorno_anualizado = (precio_final / precio_inicial) ** (1 / años) - 1
calmar = retorno_anualizado / abs(max_dd) if max_dd != 0 else 0

dias_dd_5pct = (drawdown < -0.05).sum()

print(f"Precio inicial (2019-01-02): ${precio_inicial:,.2f}")
print(f"Precio final (2023-12-29): ${precio_final:,.2f}")
print(f"Máximo Drawdown: {max_dd:.2%} en {fecha_max_dd.date()}")
print(f"Duración del peor drawdown: {duracion_dd} días")
print(f"Retorno anualizado: {retorno_anualizado:.2%}")
print(f"Calmar Ratio: {calmar:.2f}")
print(f"Días en drawdown > 5%: {dias_dd_5pct} días")
