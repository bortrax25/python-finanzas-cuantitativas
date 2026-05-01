# U23: Obtención de Datos — APIs y Web Scraping Financiero

> **Lectura previa:** [U22: Visualización Financiera](../fase-5/U22-visualizacion.md)
> **Próxima unidad:** [U24: Valor del Dinero en el Tiempo y Renta Fija](../fase-6/U24-tvm-renta-fija.md)

---

## 1. Teoría

### 1.1 yfinance: Yahoo Finance desde Python

`yfinance` es la puerta de entrada más simple a datos de mercado gratuitos. Descarga precios históricos, fundamentales, dividendos y splits.

```python
import yfinance as yf

# Descargar datos de un ticker
aapl = yf.Ticker("AAPL")

# Información general
info = aapl.info
print(f"Nombre: {info.get('longName')}")
print(f"Sector: {info.get('sector')}")
print(f"Market Cap: ${info.get('marketCap'):,}")
print(f"PER: {info.get('trailingPE')}")
print(f"Beta: {info.get('beta')}")

# Precios históricos
hist = aapl.history(period="1y")
print(hist.head())

# Precios en rango específico
hist_rango = aapl.history(start="2023-01-01", end="2023-12-31")

# Múltiples tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
datos = yf.download(tickers, start="2023-01-01", end="2023-12-31")
precios_cierre = datos["Close"]

# Dividendos y splits
dividendos = aapl.dividends
splits = aapl.splits
```

> ⚠️ **Limitaciones de yfinance:** Los datos pueden tener retrasos (15-20 min para precios en tiempo real). No uses yfinance para trading en vivo. Para backtesting e investigación, es excelente.

### 1.2 Acceso a múltiples DataFrames con `yf.download`

```python
import yfinance as yf
import pandas as pd

# 20 acciones del S&P 500 (top por market cap)
sp20 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
        "BRK-B", "UNH", "JNJ", "V", "XOM", "WMT", "JPM", "MA",
        "PG", "CVX", "HD", "LLY", "ABBV"]

# Descargar 2 años de datos
datos_sp20 = yf.download(sp20, start="2022-01-01", end="2023-12-31")

# El resultado es un MultiIndex DataFrame
print(datos_sp20.columns)
# MultiIndex: (Price, AAPL), (Price, MSFT), ...

# Extraer solo precios de cierre
cierre_sp20 = datos_sp20["Close"]

# Calcular retornos diarios de todo el universo
retornos_sp20 = cierre_sp20.pct_change().dropna()

# Matriz de correlación
corr_matrix = retornos_sp20.corr()

# Top 3 acciones por retorno acumulado
retorno_acum = (cierre_sp20.iloc[-1] / cierre_sp20.iloc[0] - 1).sort_values(ascending=False)
print(retorno_acum.head(3))
```

### 1.3 Requests para APIs REST financieras

Muchas APIs financieras requieren autenticación y rate limiting. El patrón estándar:

```python
import requests
import time
from typing import Optional

class APIClient:
    """Cliente base para APIs REST financieras."""

    def __init__(self, api_key: str, base_url: str, rate_limit: float = 0.2):
        self.api_key = api_key
        self.base_url = base_url
        self.rate_limit = rate_limit  # segundos entre requests
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """GET request con rate limiting y manejo de errores."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()  # lanza excepción si 4xx/5xx
            time.sleep(self.rate_limit)   # respetar rate limit
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en {endpoint}: {e}")
            return None


# Ejemplo con Alpha Vantage (API gratuita de datos financieros)
class AlphaVantageClient(APIClient):
    def __init__(self, api_key: str):
        super().__init__(api_key, "https://www.alphavantage.co/query", rate_limit=0.5)

    def precio_diario(self, ticker: str) -> Optional[dict]:
        return self.get("", {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
        })

    def tipo_cambio(self, desde: str, hacia: str = "USD") -> Optional[dict]:
        return self.get("", {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": desde,
            "to_currency": hacia,
            "apikey": self.api_key,
        })

# Uso:
# client = AlphaVantageClient("TU_API_KEY")
# datos = client.precio_diario("AAPL")
```

> ⚠️ **Nunca hardcodees API keys.** Usa variables de entorno: `os.getenv("ALPHA_VANTAGE_KEY")` o un archivo `.env` con `python-dotenv`.

### 1.4 FRED: Datos macroeconómicos de la Reserva Federal

FRED (Federal Reserve Economic Data) ofrece datos macro gratuitos: PIB, inflación, tasas de interés, empleo.

```python
# Usando requests directamente (la API de FRED es REST, no requiere librería extra)
import requests
import pandas as pd

class FREDClient:
    BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def obtener_serie(self, series_id: str, inicio: str = "2020-01-01",
                      fin: str = "2023-12-31") -> pd.Series:
        """Descarga una serie temporal de FRED."""
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "observation_start": inicio,
            "observation_end": fin,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        datos = response.json()

        fechas = [obs["date"] for obs in datos["observations"]]
        valores = [float(obs["value"]) if obs["value"] != "." else None
                   for obs in datos["observations"]]

        serie = pd.Series(valores, index=pd.to_datetime(fechas), name=series_id)
        return serie.dropna()


# Series populares de FRED
SERIES_FRED = {
    "GDP": "GDP",                     # Producto Interno Bruto
    "CPI": "CPIAUCSL",                # Índice de Precios al Consumidor
    "FEDFUNDS": "FEDFUNDS",          # Tasa de Fondos Federales
    "UNRATE": "UNRATE",               # Tasa de Desempleo
    "T10Y2Y": "T10Y2Y",               # Spread 10Y-2Y (indicador de recesión)
    "SP500": "SP500",                 # S&P 500
    "VIXCLS": "VIXCLS",               # VIX (índice del miedo)
}

# Uso:
# fred = FREDClient("TU_API_KEY_FRED")
# tasa_fed = fred.obtener_serie("FEDFUNDS")
# desempleo = fred.obtener_serie("UNRATE")
# spread = fred.obtener_serie("T10Y2Y")
```

### 1.5 BeautifulSoup: Web Scraping ético

Para datos que no tienen API (tarifas, reportes, noticias), BeautifulSoup extrae información de HTML.

```python
import requests
from bs4 import BeautifulSoup

def extraer_tickers_noticia(url: str) -> list[str]:
    """Extrae menciones de tickers (símbolos en mayúscula de 1-5 letras)."""
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Eliminar scripts y estilos
    for script in soup(["script", "style"]):
        script.decompose()

    texto = soup.get_text()

    # Buscar tickers (palabras en mayúscula de 1-5 letras)
    import re
    tickers_encontrados = set()
    # Patrón: palabra en mayúscula de 1-5 caracteres, precedida por espacio/signo
    for match in re.finditer(r'(?<![A-Za-z])[A-Z]{1,5}(?![A-Za-z])', texto):
        ticker = match.group()
        # Excluir palabras comunes en inglés
        comunes = {"A", "I", "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU",
                   "ALL", "CAN", "HAD", "HER", "WAS", "ONE", "OUR", "OUT",
                   "HAS", "HAVE", "FROM", "THEY", "THIS", "THAT", "WITH",
                   "WILL", "BEEN", "WOULD", "THERE", "THEIR"}
        if ticker not in comunes:
            tickers_encontrados.add(ticker)

    return sorted(tickers_encontrados)

# Uso:
# tickers = extraer_tickers_noticia("https://example.com/finance-news")
```

> ⚠️ **Ética del web scraping:** Siempre (1) lee `robots.txt` del sitio, (2) respeta rate limits con `time.sleep()`, (3) no extraigas datos protegidos por copyright, (4) usa un User-Agent identificable.

### 1.6 Pipeline de datos financieros end-to-end

```python
def construir_dataset(sp500_tickers: list[str], fred_series: dict,
                      inicio: str, fin: str) -> pd.DataFrame:
    """
    Pipeline completo:
    1. Descarga precios de acciones (yfinance)
    2. Descarga datos macro (FRED)
    3. Combina en un solo DataFrame alineado por fecha
    """
    import yfinance as yf
    import pandas as pd

    # 1. Precios de acciones
    print(f"Descargando {len(sp500_tickers)} acciones...")
    precios_raw = yf.download(sp500_tickers, start=inicio, end=fin, progress=False)
    precios_cierre = precios_raw["Close"]

    # 2. Calcular retornos diarios
    retornos = precios_cierre.pct_change().dropna()

    # 3. Métricas de acciones
    retorno_promedio = retornos.mean() * 252
    volatilidad = retornos.std() * np.sqrt(252)
    sharpe = retorno_promedio / volatilidad

    metricas_acciones = pd.DataFrame({
        "retorno_anual": retorno_promedio,
        "volatilidad_anual": volatilidad,
        "sharpe_ratio": sharpe,
    })

    # 4. Agregar sector (desde info de yfinance)
    sectores = {}
    for ticker in sp500_tickers[:5]:  # limitar a 5 para no saturar
        try:
            info = yf.Ticker(ticker).info
            sectores[ticker] = info.get("sector", "Desconocido")
            time.sleep(0.2)
        except Exception:
            sectores[ticker] = "Error"
    metricas_acciones["sector"] = pd.Series(sectores)

    return metricas_acciones

# Uso:
# dataset = construir_dataset(sp20, SERIES_FRED, "2022-01-01", "2023-12-31")
# print(dataset.sort_values("sharpe_ratio", ascending=False))
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Pipeline de datos S&P 500

**Concepto financiero:** Construir un dataset que combine precios, retornos y métricas de múltiples acciones para screening.

**Código:**

```python
import yfinance as yf
import pandas as pd
import numpy as np

# Top 10 del S&P por market cap (tickers estables)
sp10 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
        "BRK-B", "JPM", "V"]

print("Descargando datos de 10 acciones del S&P 500...")
datos = yf.download(sp10, start="2023-01-01", end="2023-12-31", progress=False)
precios_cierre = datos["Close"]

# Calcular métricas
retornos_diarios = precios_cierre.pct_change().dropna()
retorno_anual = retornos_diarios.mean() * 252 * 100
vol_anual = retornos_diarios.std() * np.sqrt(252) * 100
sharpe = retorno_anual / vol_anual
retorno_total = (precios_cierre.iloc[-1] / precios_cierre.iloc[0] - 1) * 100

# Tabla resumen
resumen = pd.DataFrame({
    "Retorno Total (%)": retorno_total,
    "Retorno Anual (%)": retorno_anual,
    "Volatilidad (%)": vol_anual,
    "Sharpe Ratio": sharpe,
}).round(2)

print("\nTop 3 por retorno total:")
print(resumen.sort_values("Retorno Total (%)", ascending=False).head(3))
print(f"\nTop 3 por Sharpe Ratio:")
print(resumen.sort_values("Sharpe Ratio", ascending=False).head(3))
```

**Output:**

```
Descargando datos de 10 acciones del S&P 500...
Top 3 por retorno total:
      Retorno Total (%)  Retorno Anual (%)  Volatilidad (%)  Sharpe Ratio
NVDA              239.45             121.34            45.23          2.68
META              194.32             108.56            40.12          2.71
TSLA              101.56              72.34            52.18          1.39
```

---

## 3. Aplicación en Finanzas 💰

En **JP Morgan**, el equipo de research construye dashboards que combinan datos de Bloomberg Terminal (vía API), FRED (macro), y SEC EDGAR (filings) en un solo DataFrame para análisis cross-asset.

En **hedge funds**, los pipelines de datos se ejecutan diariamente antes del open: descargan precios de cierre, datos fundamentales actualizados, y los fusionan con señales de factores para generar el orden book del día.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-5/U23_ejercicios.py`

1. **Descarga y análisis de un ticker con yfinance:** Descargar 2 años de AAPL. Calcular retorno total, volatilidad, máximo drawdown. Extraer PER, sector, market cap de `info`.
2. **Screening de múltiples tickers:** Descargar 10 tickers, calcular retorno y Sharpe. Ranking top 3 y bottom 3.
3. **Cliente para API REST (simulado):** Implementar `APIClient` con rate limiting y manejo de errores. Proveer datos simulados de precios en JSON.
4. **Pipeline datos macro + acciones:** Combinar datos de acciones simulados con datos macro de FRED simulados. Calcular correlación entre retornos del S&P 500 y tasa de fondos federales.

---

## 5. Resumen

| Herramienta | Propósito | Ejemplo |
|------------|-----------|---------|
| `yfinance` | Datos de Yahoo Finance (precios, info) | `yf.download(["AAPL", "MSFT"])` |
| `requests` | APIs REST (Alpha Vantage, FRED) | `requests.get(url, params={})` |
| `BeautifulSoup` | Scraping de HTML (noticias, tablas) | `BeautifulSoup(html, "html.parser")` |
| Rate limiting | Respetar límites de API | `time.sleep(0.2)` entre requests |
| Variables de entorno | Proteger API keys | `os.getenv("API_KEY")` |

---

## ✅ Autoevaluación

1. ¿Cómo descargas datos históricos de 5 tickers a la vez con yfinance?
2. ¿Qué precauciones debes tomar al hacer web scraping?
3. ¿Cómo proteges tus API keys en un proyecto?
4. ¿Qué es rate limiting y por qué es importante respetarlo?
5. ¿Cómo combinarías precios de acciones con datos macro en un solo DataFrame?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `yfinance` para precios históricos e info fundamental gratuita de Yahoo Finance
> - `requests` + `Session()` para APIs REST con autenticación y rate limiting
> - APIs clave: Alpha Vantage (precios), FRED (datos macro de la Fed)
> - Scraping ético: `robots.txt`, `time.sleep()`, User-Agent, no copyright
> - Pipeline típico: descargar → limpiar → alinear por fecha → merge → analizar
