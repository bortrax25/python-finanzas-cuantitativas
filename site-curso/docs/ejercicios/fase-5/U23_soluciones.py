# U23: SOLUCIONES — APIs y Datos Financieros

import pandas as pd
import numpy as np
import time

# ============================================================
# Ejercicio 1: Descarga y análisis de un ticker
# ============================================================
print("=== Ejercicio 1: Análisis de AAPL ===")

np.random.seed(42)
fechas_2y = pd.date_range("2022-01-03", "2023-12-29", freq="B")
retornos_sim = np.random.normal(0.0004, 0.015, len(fechas_2y))
retornos_sim[0] = 0
precios_aapl = pd.Series(180 * np.cumprod(1 + retornos_sim), index=fechas_2y, name="AAPL")

info_aapl = {
    "longName": "Apple Inc.",
    "sector": "Technology",
    "marketCap": 2_800_000_000_000,
    "trailingPE": 28.5,
    "beta": 1.25,
}

precio_inicial = precios_aapl.iloc[0]
precio_final = precios_aapl.iloc[-1]
retorno_total = (precio_final / precio_inicial - 1) * 100

retornos = precios_aapl.pct_change().dropna()
vol_anualizada = retornos.std() * np.sqrt(252) * 100

pico = precios_aapl.cummax()
max_drawdown = (precios_aapl / pico - 1).min() * 100
dias_positivos = (retornos > 0).mean() * 100

market_cap_b = info_aapl["marketCap"] / 1_000_000_000

print(f"AAPL: {info_aapl['longName']}")
print(f"Sector: {info_aapl['sector']} | "
      f"Market Cap: ${market_cap_b:,.2f}B | "
      f"PER: {info_aapl['trailingPE']} | "
      f"Beta: {info_aapl['beta']}")
print(f"Precio inicial ({precios_aapl.index[0].date()}): ${precio_inicial:,.2f}")
print(f"Precio final ({precios_aapl.index[-1].date()}): ${precio_final:,.2f}")
print(f"Retorno total: {retorno_total:.2f}%")
print(f"Volatilidad anualizada: {vol_anualizada:.2f}%")
print(f"Máximo Drawdown: {max_drawdown:.2f}%")
print(f"Días positivos: {dias_positivos:.1f}%")

# ============================================================
# Ejercicio 2: Screening de múltiples tickers
# ============================================================
print("\n=== Ejercicio 2: Screening de 10 tickers ===")

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

retornos_sc = df_sc.pct_change().dropna()
retorno_total = (df_sc.iloc[-1] / df_sc.iloc[0] - 1) * 100
retorno_anual = retornos_sc.mean() * 252 * 100
vol_anual = retornos_sc.std() * np.sqrt(252) * 100
tasa_libre = 0.03
sharpe = (retorno_anual / 100 - tasa_libre) / (vol_anual / 100)

resumen = pd.DataFrame({
    "Ret. Total (%)": retorno_total.round(2),
    "Ret. Anual (%)": retorno_anual.round(2),
    "Vol. Anual (%)": vol_anual.round(2),
    "Sharpe": sharpe.round(2),
}).sort_values("Sharpe", ascending=False)

print("Ranking por Sharpe Ratio (top 3 + bottom 3):")
print(f"{'Ticker':<10} {'Ret. Total':>12} {'Ret. Anual':>12} {'Vol. Anual':>12} {'Sharpe':>8}")
print("-" * 58)
for i, (ticker, fila) in enumerate(resumen.iterrows()):
    if i < 3 or i >= len(resumen) - 3:
        marker = "..." if i == 3 else ""
        if marker:
            print(f"{'...':<10}")
            continue
        print(f"{ticker:<10} {fila['Ret. Total (%)']:>10.2f}% "
              f"{fila['Ret. Anual (%)']:>10.2f}% "
              f"{fila['Vol. Anual (%)']:>10.2f}% {fila['Sharpe']:>8.2f}")

# ============================================================
# Ejercicio 3: Cliente para API REST con rate limiting
# ============================================================
print("\n=== Ejercicio 3: API Client con rate limiting ===")


class BaseAPIClient:
    def __init__(self, api_key: str, base_url: str, rate_limit: float = 0.5):
        self.api_key = api_key
        self.base_url = base_url
        self.rate_limit = rate_limit

    def get(self, endpoint: str, params: dict = None) -> dict:
        time.sleep(self.rate_limit)
        return {}


class PrecioClient(BaseAPIClient):
    def __init__(self, api_key: str = "demo_key", rate_limit: float = 0.5):
        super().__init__(api_key, "https://api.precios-simulada.com/v1", rate_limit)

    def get(self, endpoint: str, params: dict = None) -> dict:
        time.sleep(self.rate_limit)
        ticker = params.get("ticker", "UNKNOWN")
        np.random.seed(hash(ticker) % 2**31)
        precios = list(np.round(np.cumprod(1 + np.random.normal(0.0005, 0.012, 5)) * 100, 2))
        print(f"[PrecioClient] {ticker}: {len(precios)} precios descargados")
        return {"ticker": ticker, "precios": precios, "moneda": "USD"}

    def precio_diario(self, ticker: str) -> dict:
        return self.get("daily", {"ticker": ticker, "outputsize": "compact"})


inicio = time.perf_counter()
client = PrecioClient(rate_limit=0.5)

for ticker in ["AAPL", "MSFT", "TSLA"]:
    datos = client.precio_diario(ticker)
    assert "ticker" in datos and "precios" in datos

tiempo_total = time.perf_counter() - inicio
tiempo_esperado = 0.5 * 3  # 3 llamadas × 0.5s
rate_ok = tiempo_total >= tiempo_esperado - 0.05

print(f"Tiempo total: {tiempo_total:.2f}s (esperado >= {tiempo_esperado:.1f}s con rate_limit=0.5)")
print(f"Rate limit respetado: {rate_ok}")

# ============================================================
# Ejercicio 4: Pipeline datos macro + acciones
# ============================================================
print("\n=== Ejercicio 4: Pipeline datos macro + acciones ===")

np.random.seed(42)
fechas_2023 = pd.date_range("2023-01-03", "2023-12-29", freq="B")
retornos_sp = np.random.normal(0.0003, 0.010, len(fechas_2023))
retornos_sp[0] = 0
spx = pd.Series(3800 * np.cumprod(1 + retornos_sp), index=fechas_2023, name="SPX")

# Tasa de fondos federales simulada (aumenta gradualmente)
fechas_mensuales = pd.date_range("2023-01-01", "2023-12-01", freq="MS")
tasas_mensuales = [4.25, 4.50, 4.75, 5.00, 5.00, 5.25, 5.25, 5.25, 5.50, 5.50, 5.50, 5.50]
fedfunds = pd.Series(tasas_mensuales, index=fechas_mensuales, name="FEDFUNDS")

fedfunds_diario = fedfunds.reindex(fechas_2023, method="ffill")

# Alinear al final (último día hábil)
spx_retornos = spx.pct_change().dropna()
fedfunds_retornos = fedfunds_diario.pct_change().dropna()  # NaN los días sin cambio

comun = spx_retornos.index.intersection(fedfunds_retornos.index)
correlacion = spx_retornos[comun].corr(fedfunds_retornos[comun])

# Meses con alza vs sin cambio
cambios_mensuales = fedfunds.resample("ME").last().diff()
meses_alza = cambios_mensuales[cambios_mensuales > 0].index
meses_estable = cambios_mensuales[cambios_mensuales == 0].index

spx_mensual = spx.resample("ME").last().pct_change() * 100
ret_alza = spx_mensual[spx_mensual.index.isin(meses_alza)].mean()
ret_estable = spx_mensual[spx_mensual.index.isin(meses_estable)].mean()

print(f"Datos S&P 500: {len(spx)} días (2023)")
print(f"Datos FEDFUNDS: {len(fedfunds)} meses → {len(fedfunds_diario)} días (forward filled)")
print(f"Correlación retornos S&P vs Δ tasa: {correlacion:.2f}")
print(f"Meses con alza de tasa ({len(meses_alza)} meses):")
print(f"  Retorno S&P promedio: {ret_alza:+.2f}%")
print(f"Meses sin cambio de tasa ({len(meses_estable)} meses):")
print(f"  Retorno S&P promedio: {ret_estable:+.2f}%")
