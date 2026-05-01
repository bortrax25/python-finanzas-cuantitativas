# U21: Pandas Avanzado — Análisis Técnico de Series Financieras

> **Lectura previa:** [U20: Pandas Fundamentos](../fase-5/U20-pandas-fundamentos.md)
> **Próxima unidad:** [U22: Visualización Financiera](../fase-5/U22-visualizacion.md)

---

## 1. Teoría

### 1.1 Ventanas móviles: `rolling()` y `ewm()`

Las ventanas móviles son la base del análisis técnico. `rolling()` aplica funciones sobre una ventana fija de observaciones pasadas.

```python
import pandas as pd
import numpy as np

# Datos de ejemplo
fechas = pd.date_range("2024-01-02", periods=120, freq="B")
precios = pd.Series(100 * np.cumprod(1 + np.random.normal(0.0005, 0.012, 120)),
                     index=fechas, name="precio")
retornos = precios.pct_change().dropna()

# Medias móviles (SMA)
sma_20 = precios.rolling(window=20).mean()
sma_50 = precios.rolling(window=50).mean()
sma_200 = precios.rolling(window=200).mean()

# Desviación estándar móvil (volatilidad rolling)
vol_rolling_20 = retornos.rolling(window=20).std()

# Mínimo, máximo, suma en ventana
max_20d = precios.rolling(window=20).max()
min_20d = precios.rolling(window=20).min()
suma_vol = retornos.rolling(window=20).sum()

# EMA — Exponential Moving Average (más peso a datos recientes)
ema_12 = precios.ewm(span=12, adjust=False).mean()
ema_26 = precios.ewm(span=26, adjust=False).mean()

# Volatilidad con EWMA (RiskMetrics)
vol_ewma = retornos.ewm(span=20).std()
```

> 💡 **Tip:** `span` en `ewm` define el centro de masa. `span=20` equivale aproximadamente a `alpha = 2/(span+1)`. `adjust=False` usa la fórmula recursiva moderna (más rápida).

### 1.2 Bollinger Bands

Las Bandas de Bollinger miden la dispersión alrededor de una media móvil. Precio fuera de bandas → posible reversión a la media.

```python
def calcular_bollinger(precios: pd.Series, ventana: int = 20, num_std: float = 2.0):
    sma = precios.rolling(window=ventana).mean()
    std = precios.rolling(window=ventana).std()
    banda_superior = sma + num_std * std
    banda_inferior = sma - num_std * std
    ancho_banda = (banda_superior - banda_inferior) / sma * 100  # %B width
    posicion_b = (precios - banda_inferior) / (banda_superior - banda_inferior)  # %B
    return pd.DataFrame({
        "sma": sma,
        "superior": banda_superior,
        "inferior": banda_inferior,
        "ancho_banda": ancho_banda,
        "posicion_b": posicion_b,
    })

bb = calcular_bollinger(precios)
senal_compra = bb["posicion_b"] < 0   # precio bajo banda inferior → oversold
senal_venta = bb["posicion_b"] > 1    # precio sobre banda superior → overbought
```

### 1.3 RSI — Relative Strength Index

El RSI (Wilder, 1978) mide la velocidad y magnitud de los cambios de precio. Valores > 70 = sobrecompra, < 30 = sobreventa.

```python
def calcular_rsi(precios: pd.Series, periodo: int = 14) -> pd.Series:
    delta = precios.diff()
    ganancia = delta.clip(lower=0)
    perdida = (-delta).clip(lower=0)

    ganancia_media = ganancia.ewm(alpha=1/periodo, adjust=False).mean()
    perdida_media = perdida.ewm(alpha=1/periodo, adjust=False).mean()

    rs = ganancia_media / perdida_media
    rsi = 100 - (100 / (1 + rs))
    return rsi

rsi_14 = calcular_rsi(precios)
sobrecompra = rsi_14 > 70
sobreventa = rsi_14 < 30
```

> ⚠️ **Wilder smoothing usa `alpha=1/periodo`**, a diferencia del `span` de `ewm`. La fórmula original de Wilder usa una media móvil exponencial modificada.

### 1.4 MACD — Moving Average Convergence Divergence

El MACD (Appel, 1979) es un indicador de tendencia que combina dos EMAs. La señal se genera cuando la línea MACD cruza la línea de señal.

```python
def calcular_macd(precios: pd.Series, rapida: int = 12, lenta: int = 26, senal: int = 9):
    ema_rapida = precios.ewm(span=rapida, adjust=False).mean()
    ema_lenta = precios.ewm(span=lenta, adjust=False).mean()

    macd_line = ema_rapida - ema_lenta
    senal_line = macd_line.ewm(span=senal, adjust=False).mean()
    histograma = macd_line - senal_line

    # Detección de cruces
    cruce_alcista = (macd_line > senal_line) & (macd_line.shift(1) <= senal_line.shift(1))
    cruce_bajista = (macd_line < senal_line) & (macd_line.shift(1) >= senal_line.shift(1))

    return pd.DataFrame({
        "macd": macd_line,
        "senal": senal_line,
        "histograma": histograma,
        "cruce_alcista": cruce_alcista,
        "cruce_bajista": cruce_bajista,
    })

macd = calcular_macd(precios)
print(f"Cruces alcistas detectados: {macd['cruce_alcista'].sum()}")
print(f"Cruces bajistas detectados: {macd['cruce_bajista'].sum()}")
```

### 1.5 VWAP — Volume Weighted Average Price

El VWAP es el precio promedio ponderado por volumen. Es el benchmark estándar para ejecución institucional.

```python
def calcular_vwap(precios: pd.Series, volumen: pd.Series) -> pd.Series:
    """VWAP acumulado desde el inicio de la serie."""
    pv_acum = (precios * volumen).cumsum()
    vol_acum = volumen.cumsum()
    return pv_acum / vol_acum

# VWAP intradiario (resetea cada día)
def vwap_diario(df: pd.DataFrame) -> pd.Series:
    """df debe tener columnas: precio, volumen y un DatetimeIndex."""
    pv = (df["precio"] * df["volumen"]).groupby(df.index.date).cumsum()
    vol = df["volumen"].groupby(df.index.date).cumsum()
    return pv / vol
```

### 1.6 Métricas de performance con `rolling()` y `ewm()`

```python
# Sharpe Ratio móvil (ventana de 60 días)
retornos = precios.pct_change().dropna()
sharpe_rolling = (retornos.rolling(60).mean() / retornos.rolling(60).std()) * np.sqrt(252)

# Sortino Ratio (solo penaliza volatilidad negativa)
retornos_negativos = retornos.clip(upper=0)  # solo valores <= 0
downside_std = retornos_negativos.rolling(60).std()
sortino_rolling = (retornos.rolling(60).mean() / downside_std) * np.sqrt(252)

# Maximum drawdown en ventana móvil
def max_drawdown_rolling(precios: pd.Series, ventana: int = 60) -> pd.Series:
    pico_rolling = precios.rolling(ventana, min_periods=1).max()
    return (precios / pico_rolling - 1)

drawdown_rolling = max_drawdown_rolling(precios)
```

### 1.7 MultiIndex, `pipe()`, datos faltantes y performance

```python
# MultiIndex: panel de datos (ticker × fecha)
fechas = pd.date_range("2024-01-02", periods=30, freq="B")
tickers = ["AAPL", "MSFT", "TSLA"]
idx = pd.MultiIndex.from_product([fechas, tickers], names=["fecha", "ticker"])
datos = pd.DataFrame({
    "precio": np.random.uniform(100, 350, 90),
    "volumen": np.random.randint(500_000, 5_000_000, 90),
}, index=idx)

# Acceso con MultiIndex
print(datos.loc[(slice(None), "AAPL"), :])  # todos los días de AAPL
print(datos.xs("AAPL", level="ticker"))     # cross-section de AAPL

# pipe(): encadenar operaciones
resultado = (datos
    .query("volumen > 1_000_000")        # filtro rápido (eval)
    .pipe(lambda df: df.assign(retorno=df.groupby("ticker")["precio"].pct_change()))
    .dropna()
)

# fillna e interpolate
precios_con_huecos = precios.copy()
precios_con_huecos.iloc[[10, 20, 50]] = np.nan

# Rellenar con último valor conocido (forward fill)
precios_ffill = precios_con_huecos.fillna(method="ffill")

# Interpolar linealmente
precios_interp = precios_con_huecos.interpolate(method="linear")

# eval() y query() — más rápidos que la sintaxis normal
condicion = datos.eval("precio > 200 and volumen > 2_000_000")
seleccion = datos.query("ticker == 'AAPL' and precio > 150")
```

> 💡 **Tip:** `eval()` y `query()` usan el motor numexpr internamente y son más rápidos en DataFrames grandes (>100k filas). Para datos chicos, la sintaxis normal de Python es igual de rápida.

### 1.8 Dtypes categóricos: eficiencia en memoria

```python
# Sectores como categorías (ahorra memoria y acelera groupby)
datos_panel = pd.DataFrame({
    "ticker": np.random.choice(["AAPL", "MSFT", "TSLA", "JPM", "XOM"], 10_000),
    "sector": np.random.choice(["Tecnologia", "Finanzas", "Energia"], 10_000),
    "precio": np.random.uniform(50, 350, 10_000),
})

# Convertir a categoría
datos_panel["ticker"] = datos_panel["ticker"].astype("category")
datos_panel["sector"] = datos_panel["sector"].astype("category")

print(f"Memoria ticker: {datos_panel['ticker'].memory_usage(deep=True):,} bytes")
# ~1,000 bytes vs ~80,000 bytes como string

# Groupby en categorías es más rápido
resultado = datos_panel.groupby(["sector", "ticker"], observed=True).agg(
    precio_medio=("precio", "mean"),
    count=("precio", "count"),
)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Dashboard de indicadores técnicos

**Concepto financiero:** Combinar SMA, Bollinger, RSI y MACD en un solo DataFrame para generar señales de trading.

**Código:**

```python
import pandas as pd
import numpy as np

np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=200, freq="B")
precios = pd.Series(100 * np.cumprod(1 + np.random.normal(0.0005, 0.015, 200)), index=fechas)

# Calcular todos los indicadores
sma_20 = precios.rolling(20).mean()
std_20 = precios.rolling(20).std()
bb_superior = sma_20 + 2 * std_20
bb_inferior = sma_20 - 2 * std_20

delta = precios.diff()
rsi_14 = 100 - (100 / (1 + (delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean() /
                            (-delta).clip(lower=0).ewm(alpha=1/14, adjust=False).mean())))

ema_12 = precios.ewm(span=12, adjust=False).mean()
ema_26 = precios.ewm(span=26, adjust=False).mean()
macd_line = ema_12 - ema_26
senal_line = macd_line.ewm(span=9, adjust=False).mean()

# Dataframe de señales
dashboard = pd.DataFrame({
    "precio": precios,
    "sma_20": sma_20,
    "bb_superior": bb_superior,
    "bb_inferior": bb_inferior,
    "rsi_14": rsi_14,
    "macd": macd_line,
    "senal_macd": senal_line,
    "senal_sobreventa": (precios < bb_inferior) & (rsi_14 < 30),
    "senal_sobrecompra": (precios > bb_superior) & (rsi_14 > 70),
}).dropna()

señales = dashboard[dashboard["senal_sobreventa"] | dashboard["senal_sobrecompra"]]
print(f"Señales detectadas: {len(señales)}")
print(señales[["precio", "rsi_14"]].round(2))
```

---

## 3. Aplicación en Finanzas 💰

En **hedge funds sistemáticos** (Renaissance Technologies, Two Sigma), los indicadores técnicos se calculan sobre miles de activos en tiempo real con `rolling().apply()` optimizado. El 80% de las estrategias CTA (Commodity Trading Advisors) usan combinaciones de SMA, MACD y Bollinger como features de entrada para modelos de ML.

En **mesas de ejecución**, el VWAP es el benchmark: si llenas una orden a mejor precio que el VWAP, generaste alpha de ejecución.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-5/U21_ejercicios.py`

1. **SMA, EMA y Golden/Death Cross:** Calcular SMA 20/50 y EMA 12/26. Detectar golden cross y death cross en una serie de 252 días.
2. **Bollinger Bands con señales:** Calcular BB(20,2). Identificar rupturas sobre la banda superior y bajo la banda inferior. Contar frecuencia de reversiones.
3. **RSI y detección de divergencias:** Calcular RSI(14). Detectar sobrecompra/sobreventa. Bonus: detectar divergencias precio-RSI (precio hace mínimo más bajo pero RSI hace mínimo más alto).
4. **MACD completo con señal y backtest rápido:** MACD con cruces. Estrategia simple: comprar en cruce alcista, vender en cruce bajista. Calcular P&L acumulado en el período.

---

## 5. Resumen

| Indicador | Cálculo | Señal |
|-----------|---------|-------|
| SMA | `precios.rolling(N).mean()` | Cruces corto/largo |
| EMA | `precios.ewm(span=N, adjust=False).mean()` | Tendencia |
| Bollinger | `SMA ± K × rolling_std` | Ruptura de bandas |
| RSI | `100 - 100/(1 + RS)` con EWMA | >70 sobrecompra, <30 sobreventa |
| MACD | `EMA12 - EMA26` con línea de señal EMA9 | Cruce MACD/señal |
| VWAP | `∑(P×V) / ∑V` acumulado | Benchmark de ejecución |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre `rolling()` y `ewm()`?
2. ¿Por qué `adjust=False` en `ewm()`?
3. ¿Cómo detectas un golden cross sin bucles?
4. ¿Qué significa un RSI de 85 en términos de trading?
5. ¿Cómo calcularías el máximo drawdown en una ventana móvil de 60 días?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `rolling()` = ventana fija, `ewm()` = decaimiento exponencial (más peso a lo reciente)
> - Bollinger = `SMA ± 2σ`; RSI > 70 = sobrecompra; MACD = `EMA12 - EMA26`
> - Señales sin bucles: comparar valores actuales con `shift(1)` para detectar cruces
> - `pipe()`, `eval()`, `query()` para código más limpio y rápido en DataFrames grandes
