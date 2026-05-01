# U22: Visualización Financiera con Matplotlib y Plotly

> **Lectura previa:** [U21: Pandas Avanzado](../fase-5/U21-pandas-avanzado.md)
> **Próxima unidad:** [U23: APIs y Datos](../fase-5/U23-apis-datos.md)

---

## 1. Teoría

### 1.1 Matplotlib: la base de toda visualización en Python

Matplotlib es la librería fundamental. Todo lo demás (seaborn, plotly, mplfinance) se construye sobre sus conceptos.

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Datos
fechas = pd.date_range("2024-01-02", periods=252, freq="B")
precios = pd.Series(100 * np.cumprod(1 + np.random.normal(0.0005, 0.012, 252)),
                     index=fechas)

# Gráfico de línea básico
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(precios.index, precios.values, linewidth=1.5, color="#1f77b4", label="Precio")
ax.set_title("Evolución del Precio — Activo Simulado", fontsize=14, fontweight="bold")
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio ($)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### 1.2 Subplots: paneles múltiples

El patrón estándar en finanzas es precio arriba, volumen/indicador abajo.

```python
volumen = pd.Series(np.random.randint(500_000, 5_000_000, 252), index=fechas)
retornos = precios.pct_change().dropna()
sma_20 = precios.rolling(20).mean()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True,
                                      gridspec_kw={'height_ratios': [3, 1, 1]})

# Panel 1: Precio + SMA
ax1.plot(precios.index, precios, linewidth=1.2, color="#1f77b4", label="Precio")
ax1.plot(sma_20.index, sma_20, linewidth=1.0, color="#ff7f0e", label="SMA 20")
ax1.set_title("Precio y Media Móvil 20 días", fontweight="bold")
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)

# Panel 2: Volumen (barras)
colores = ["#2ca02c" if retornos.get(fecha, 0) >= 0 else "#d62728"
           for fecha in volumen.index]
ax2.bar(volumen.index, volumen.values / 1_000_000, color=colores, alpha=0.7, width=1)
ax2.set_ylabel("Volumen (M)")
ax2.grid(True, alpha=0.3)

# Panel 3: Retornos diarios
ax3.fill_between(retornos.index, retornos.values * 100, 0,
                 where=retornos.values >= 0, color="#2ca02c", alpha=0.5, label="Positivo")
ax3.fill_between(retornos.index, retornos.values * 100, 0,
                 where=retornos.values < 0, color="#d62728", alpha=0.5, label="Negativo")
ax3.set_ylabel("Retorno (%)")
ax3.axhline(y=0, color="black", linewidth=0.5)
ax3.legend(loc="upper left")

plt.tight_layout()
plt.show()
```

### 1.3 Ejes duales: precio e indicador en el mismo gráfico

```python
rsi_14 = 100 - (100 / (1 + (
    precios.diff().clip(lower=0).ewm(alpha=1/14, adjust=False).mean() /
    (-precios.diff()).clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
)))

fig, ax1 = plt.subplots(figsize=(12, 5))

# Eje izquierdo: precio
ax1.plot(precios.index, precios, color="#1f77b4", linewidth=1.5, label="Precio")
ax1.set_ylabel("Precio ($)", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")

# Eje derecho: RSI
ax2 = ax1.twinx()
ax2.plot(rsi_14.index, rsi_14, color="#9467bd", linewidth=1.0, alpha=0.7, label="RSI(14)")
ax2.axhline(y=70, color="red", linestyle="--", alpha=0.5, linewidth=0.8)
ax2.axhline(y=30, color="green", linestyle="--", alpha=0.5, linewidth=0.8)
ax2.set_ylabel("RSI", color="#9467bd")
ax2.tick_params(axis="y", labelcolor="#9467bd")
ax2.set_ylim(0, 100)

ax1.set_title("Precio y RSI(14)", fontweight="bold")
fig.tight_layout()
plt.show()
```

### 1.4 Candlestick / OHLC con mplfinance

`mplfinance` es la librería estándar para gráficos de velas japonesas en Python.

```python
import mplfinance as mpf

# Preparar datos OHLC
np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=60, freq="B")
precios_base = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.015, 60))

df_ohlc = pd.DataFrame({
    "Open": precios_base * np.random.uniform(0.99, 1.01, 60),
    "High": precios_base * np.random.uniform(1.00, 1.03, 60),
    "Low": precios_base * np.random.uniform(0.97, 1.00, 60),
    "Close": precios_base,
    "Volume": np.random.randint(1_000_000, 10_000_000, 60),
}, index=fechas)

# Gráfico de velas con volumen
mpf.plot(df_ohlc, type="candle", volume=True, style="charles",
         title="AAPL — Velas Japonesas", figsize=(12, 6),
         warn_too_much_data=100)
```

### 1.5 Heatmap de correlación con Seaborn

```python
import seaborn as sns

# Matriz de correlación de 8 sectores
sectores = ["Tec", "Fin", "Energ", "Salud", "Indust", "Consumo", "Util", "RE"]
np.random.seed(42)
retornos_sectores = np.random.normal(0.0003, 0.010, (252, 8))
corr_sectores = np.corrcoef(retornos_sectores.T)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_sectores, annot=True, fmt=".2f", cmap="RdYlBu",
            center=0, vmin=-1, vmax=1, square=True,
            xticklabels=sectores, yticklabels=sectores,
            ax=ax, cbar_kws={"shrink": 0.8, "label": "Correlación"})
ax.set_title("Matriz de Correlación entre Sectores", fontweight="bold", fontsize=14)
plt.tight_layout()
plt.show()
```

### 1.6 Gráficos interactivos con Plotly

Plotly permite zoom, hover y exportación. Ideal para dashboards y reportes.

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Datos para el candlestick
fechas_plotly = pd.date_range("2024-01-02", periods=90, freq="B")
np.random.seed(42)
precios_plotly = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.015, 90))

df_candle = pd.DataFrame({
    "Open": precios_plotly * np.random.uniform(0.99, 1.01, 90),
    "High": precios_plotly * np.random.uniform(1.00, 1.03, 90),
    "Low": precios_plotly * np.random.uniform(0.97, 1.00, 90),
    "Close": precios_plotly,
    "Volume": np.random.randint(1_000_000, 10_000_000, 90),
    "SMA20": pd.Series(precios_plotly).rolling(20).mean(),
}, index=fechas_plotly)

# Subplots interactivos
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.5, 0.25, 0.25],
    subplot_titles=("Precio + SMA 20", "Volumen", "RSI(14)")
)

# Candlestick
fig.add_trace(
    go.Candlestick(
        x=df_candle.index, open=df_candle["Open"], high=df_candle["High"],
        low=df_candle["Low"], close=df_candle["Close"], name="OHLC",
        increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
    ), row=1, col=1
)
fig.add_trace(
    go.Scatter(x=df_candle.index, y=df_candle["SMA20"],
               mode="lines", name="SMA 20", line=dict(color="orange", width=1.5)),
    row=1, col=1
)

# Volumen
colores_vol = ["#26a69a" if df_candle["Close"].iloc[i] >= df_candle["Open"].iloc[i]
               else "#ef5350" for i in range(len(df_candle))]
fig.add_trace(
    go.Bar(x=df_candle.index, y=df_candle["Volume"], name="Volumen",
           marker_color=colores_vol, opacity=0.7),
    row=2, col=1
)

# RSI
delta = df_candle["Close"].diff()
rsi = 100 - (100 / (1 + (delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean() /
                          (-delta).clip(lower=0).ewm(alpha=1/14, adjust=False).mean())))
fig.add_trace(
    go.Scatter(x=df_candle.index, y=rsi, mode="lines", name="RSI",
               line=dict(color="purple", width=1.5)),
    row=3, col=1
)
fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

fig.update_layout(
    title="Dashboard Interactivo — AAPL",
    xaxis_rangeslider_visible=False,
    height=800,
    template="plotly_white",
)
fig.show()
```

### 1.7 Equity curve y drawdown

```python
# Simular estrategia de trading
np.random.seed(42)
retornos_estrategia = np.random.normal(0.0006, 0.012, 252)
equity_curve = 10_000 * np.cumprod(1 + retornos_estrategia)

# Drawdown
pico = np.maximum.accumulate(equity_curve)
drawdown = (equity_curve / pico - 1) * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True,
                                gridspec_kw={'height_ratios': [3, 1]})

# Equity curve
ax1.plot(equity_curve, color="#1f77b4", linewidth=1.5, label="Equity Curve")
ax1.fill_between(range(len(equity_curve)), 10_000, equity_curve,
                 where=equity_curve >= 10_000, color="#2ca02c", alpha=0.15)
ax1.fill_between(range(len(equity_curve)), equity_curve, 10_000,
                 where=equity_curve < 10_000, color="#d62728", alpha=0.15)
ax1.axhline(y=10_000, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
ax1.set_ylabel("Capital ($)")
ax1.set_title("Equity Curve — Estrategia de Trading", fontweight="bold")
ax1.legend()

# Drawdown
ax2.fill_between(range(len(drawdown)), drawdown, 0,
                 color="#d62728", alpha=0.5, label="Drawdown")
ax2.set_ylabel("Drawdown (%)")
ax2.set_xlabel("Días de Trading")
ax2.axhline(y=0, color="black", linewidth=0.5)
ax2.legend()

plt.tight_layout()
plt.show()
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Reporte visual de análisis técnico

**Concepto financiero:** Un trader técnico necesita ver precio, volumen, SMA, Bollinger Bands y RSI en un solo dashboard.

**Código:**

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=120, freq="B")
precios = pd.Series(100 * np.cumprod(1 + np.random.normal(0.0005, 0.015, 120)), index=fechas)

sma_20 = precios.rolling(20).mean()
std_20 = precios.rolling(20).std()
bb_sup = sma_20 + 2 * std_20
bb_inf = sma_20 - 2 * std_20

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                gridspec_kw={'height_ratios': [3, 1]})

# Panel 1: Precio + Bollinger
ax1.plot(precios.index, precios, color="#1f77b4", linewidth=1.2, label="Precio")
ax1.plot(sma_20.index, sma_20, color="#ff7f0e", linewidth=1.0, label="SMA 20")
ax1.fill_between(bb_sup.dropna().index, bb_sup.dropna(), bb_inf.dropna(),
                 color="#ff7f0e", alpha=0.15, label="Bollinger Bands (±2σ)")
ax1.set_title("Análisis Técnico — Precio con Bollinger Bands", fontweight="bold")
ax1.set_ylabel("Precio ($)")
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)

# Panel 2: RSI
delta = precios.diff()
rsi_14 = 100 - (100 / (1 + (delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean() /
                             (-delta).clip(lower=0).ewm(alpha=1/14, adjust=False).mean())))
ax2.plot(rsi_14.dropna().index, rsi_14.dropna(), color="#9467bd", linewidth=1.2)
ax2.axhline(y=70, color="red", linestyle="--", alpha=0.5)
ax2.axhline(y=30, color="green", linestyle="--", alpha=0.5)
ax2.fill_between(rsi_14.dropna().index, 70, rsi_14.dropna(),
                 where=rsi_14.dropna() >= 70, color="red", alpha=0.2)
ax2.fill_between(rsi_14.dropna().index, rsi_14.dropna(), 30,
                 where=rsi_14.dropna() <= 30, color="green", alpha=0.2)
ax2.set_ylabel("RSI(14)")
ax2.set_ylim(0, 100)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 3. Aplicación en Finanzas 💰

En **JP Morgan**, los pitch books para clientes incluyen gráficos de velas, heatmaps sectoriales y equity curves generados con matplotlib + seaborn, exportados a PDF de alta calidad.

En **Citadel**, los dashboards de monitoreo de riesgo en tiempo real usan Plotly Dash con gráficos interactivos que se actualizan cada segundo con websockets.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-5/U22_ejercicios.py`

1. **Gráfico de línea con retornos acumulados:** Comparar equity curve de 3 activos en un solo gráfico.
2. **Subplots: precio + volumen + drawdown:** Tres paneles verticales con sharex.
3. **Heatmap de correlación sectorial:** Matriz 6×6 con seaborn, anotaciones y escala RdYlBu.
4. **Dashboard interactivo con Plotly:** Candlestick + volumen + RSI con make_subplots.

---

## 5. Resumen

| Librería | Uso principal | Método clave |
|---------|---------------|--------------|
| `matplotlib` | Gráficos base, subplots, anotaciones | `plt.subplots()`, `ax.plot()` |
| `mplfinance` | Velas japonesas (OHLC) | `mpf.plot(type="candle")` |
| `seaborn` | Heatmaps, distribuciones | `sns.heatmap(annot=True)` |
| `plotly` | Interactivos, dashboards | `go.Candlestick()`, `make_subplots()` |

---

## ✅ Autoevaluación

1. ¿Cómo creas un gráfico con dos ejes Y (precio + RSI)?
2. ¿Qué librería usas para un heatmap de correlación con anotaciones?
3. ¿Cómo agregas volumen abajo de un candlestick en mplfinance?
4. ¿Qué ventaja tiene Plotly sobre Matplotlib para reportes?
5. ¿Cómo calculas y graficas el drawdown de una equity curve?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `plt.subplots(n, 1, sharex=True)` es el patrón estándar para dashboards multi-panel
> - `mplfinance` para velas japonesas, `seaborn` para heatmaps de correlación, `plotly` para interactividad
> - Ejes duales: `ax1.twinx()` para precio + RSI en el mismo gráfico
> - Drawdown = `(precio / precio.cummax() - 1) * 100`
