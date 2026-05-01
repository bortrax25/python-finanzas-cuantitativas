# ✅ Soluciones: U22 — Fase 5

> [← Volver a ejercicios Fase 5](index.md) | [📥 Descargar .py](U22_soluciones)

---

```python
# U22: SOLUCIONES — Visualización Financiera

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Directorio de salida
salida = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Datos compartidos
np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=180, freq="B")

activos_cfg = {
    "AAPL": {"spot": 150, "mu": 0.10, "sigma": 0.22},
    "MSFT": {"spot": 310, "mu": 0.08, "sigma": 0.18},
    "TSLA": {"spot": 250, "mu": 0.12, "sigma": 0.35},
}

df_precios = pd.DataFrame(index=fechas)
for ticker, params in activos_cfg.items():
    ret = np.random.normal(params["mu"] / 252, params["sigma"] / np.sqrt(252), 180)
    ret[0] = 0
    df_precios[ticker] = params["spot"] * np.cumprod(1 + ret)

df_retornos = df_precios.pct_change().dropna()

# ============================================================
# Ejercicio 1: Equity curve de 3 activos
# ============================================================
print("=== Ejercicio 1: Equity curves ===")

normalizado = df_precios / df_precios.iloc[0] * 100

fig, ax = plt.subplots(figsize=(12, 6))
colores = {"AAPL": "#1f77b4", "MSFT": "#ff7f0e", "TSLA": "#2ca02c"}

for ticker in ["AAPL", "MSFT", "TSLA"]:
    ax.plot(normalizado.index, normalizado[ticker], linewidth=1.5,
            color=colores[ticker], label=ticker)

ax.axhline(y=100, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
ax.set_title("Retorno Acumulado — Comparación de Activos", fontsize=14, fontweight="bold")
ax.set_xlabel("Fecha")
ax.set_ylabel("Retorno Acumulado (base 100)")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)

ruta1 = os.path.join(salida, "U22_ej1_equity_curves.png")
fig.savefig(ruta1, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Gráfico guardado en: {ruta1}")

# ============================================================
# Ejercicio 2: Subplots — Precio + Volumen + Drawdown
# ============================================================
print("\\n=== Ejercicio 2: Subplots precio/volumen/drawdown ===")

aapl = df_precios["AAPL"]
ret_aap = df_retornos["AAPL"]
volumen = pd.Series(np.random.randint(1_000_000, 8_000_000, 179), index=df_retornos.index)

# Drawdown
pico_aapl = aapl.cummax()
drawdown = (aapl / pico_aapl - 1) * 100

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True,
                                     gridspec_kw={'height_ratios': [3, 1, 1]})

# Panel 1: Precio
ax1.plot(aapl.index, aapl, color="#1f77b4", linewidth=1.5, label="AAPL")
ax1.fill_between(aapl.index, aapl.min(), aapl, color="#1f77b4", alpha=0.1)
ax1.set_title("AAPL — Precio", fontweight="bold", fontsize=13)
ax1.set_ylabel("Precio ($)")
ax1.legend(loc="upper left")
ax1.grid(True, alpha=0.3)

# Panel 2: Volumen
colores_vol = ["#2ca02c" if ret >= 0 else "#d62728" for ret in ret_aap]
ax2.bar(volumen.index, volumen.values / 1_000_000, color=colores_vol,
        alpha=0.7, width=1)
ax2.set_ylabel("Volumen (M)")
ax2.set_title("Volumen Diario", fontweight="bold", fontsize=11)
ax2.grid(True, alpha=0.3)

# Panel 3: Drawdown
ax3.fill_between(drawdown.index, drawdown, 0, color="#d62728", alpha=0.4)
ax3.set_ylabel("Drawdown (%)")
ax3.set_xlabel("Fecha")
ax3.set_title("Drawdown Diario", fontweight="bold", fontsize=11)
ax3.axhline(y=0, color="black", linewidth=0.5)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
ruta2 = os.path.join(salida, "U22_ej2_subplots.png")
fig.savefig(ruta2, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Gráfico guardado en: {ruta2}")

# ============================================================
# Ejercicio 3: Heatmap de correlación sectorial
# ============================================================
print("\\n=== Ejercicio 3: Heatmap de correlación ===")

sectores = ["Tecnología", "Finanzas", "Energía", "Salud", "Industrial", "Consumo"]

# Correlación inducida con Cholesky
corr_base = np.array([
    [1.0, 0.5, 0.3, 0.4, 0.6, 0.2],
    [0.5, 1.0, 0.4, 0.3, 0.5, 0.3],
    [0.3, 0.4, 1.0, 0.1, 0.3, 0.2],
    [0.4, 0.3, 0.1, 1.0, 0.4, 0.5],
    [0.6, 0.5, 0.3, 0.4, 1.0, 0.3],
    [0.2, 0.3, 0.2, 0.5, 0.3, 1.0],
])
sigmas_sectores = np.array([0.22, 0.18, 0.25, 0.15, 0.20, 0.12])
cov = np.outer(sigmas_sectores, sigmas_sectores) * corr_base
L = np.linalg.cholesky(cov)

np.random.seed(42)
Z = np.random.standard_normal((252, 6))
retornos_sectores = Z @ L.T

matriz_corr = np.corrcoef(retornos_sectores.T)

import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap="RdYlBu",
            center=0, vmin=-1, vmax=1, square=True,
            xticklabels=sectores, yticklabels=sectores,
            ax=ax, cbar_kws={"shrink": 0.8, "label": "Correlación"})
ax.set_title("Matriz de Correlación Sectorial", fontsize=14, fontweight="bold")
plt.tight_layout()

ruta3 = os.path.join(salida, "U22_ej3_heatmap.png")
fig.savefig(ruta3, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Gráfico guardado en: {ruta3}")

# ============================================================
# Ejercicio 4: Dashboard interactivo con Plotly
# ============================================================
print("\\n=== Ejercicio 4: Dashboard Plotly interactivo ===")

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Preparar datos OHLC (60 días)
np.random.seed(42)
fechas_60 = pd.date_range("2024-01-02", periods=60, freq="B")
precios_base = 150 * np.cumprod(1 + np.random.normal(0.10/252, 0.22/np.sqrt(252), 60))

df_candle = pd.DataFrame({
    "Open": precios_base * np.random.uniform(0.99, 1.01, 60),
    "High": precios_base * np.random.uniform(1.00, 1.03, 60),
    "Low": precios_base * np.random.uniform(0.97, 1.00, 60),
    "Close": precios_base,
    "Volume": np.random.randint(1_000_000, 10_000_000, 60),
    "SMA20": pd.Series(precios_base).rolling(20).mean(),
}, index=fechas_60)

# RSI
delta = df_candle["Close"].diff()
ganancia = delta.clip(lower=0)
perdida = (-delta).clip(lower=0)
rsi_vals = 100 - (100 / (1 + (
    ganancia.ewm(alpha=1/14, adjust=False).mean() /
    perdida.ewm(alpha=1/14, adjust=False).mean()
)))

fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.5, 0.25, 0.25],
    subplot_titles=("AAPL — Precio + SMA 20", "Volumen", "RSI(14)")
)

# Panel 1: Candlestick + SMA
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

# Panel 2: Volumen
colores_vol_plotly = [
    "#26a69a" if df_candle["Close"].iloc[i] >= df_candle["Open"].iloc[i]
    else "#ef5350" for i in range(len(df_candle))
]
fig.add_trace(
    go.Bar(x=df_candle.index, y=df_candle["Volume"], name="Volumen",
           marker_color=colores_vol_plotly, opacity=0.7),
    row=2, col=1
)

# Panel 3: RSI
fig.add_trace(
    go.Scatter(x=df_candle.index, y=rsi_vals, mode="lines", name="RSI(14)",
               line=dict(color="purple", width=1.5)),
    row=3, col=1
)
fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1, opacity=0.5)
fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1, opacity=0.5)

fig.update_layout(
    title="Dashboard Interactivo — AAPL (60 días)",
    xaxis_rangeslider_visible=False,
    height=800,
    template="plotly_white",
)

ruta4 = os.path.join(salida, "U22_ej4_dashboard.html")
fig.write_html(ruta4)
print(f"Dashboard interactivo guardado en: {ruta4}")
print("(Abrir en navegador: candlestick + volumen + RSI con zoom y hover)")
```

---

> [📥 Descargar archivo .py](U22_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 5](index.md)
