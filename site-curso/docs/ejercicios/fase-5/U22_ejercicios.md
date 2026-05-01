# 📝 Ejercicios: U22 — Fase 5

> [← Volver a ejercicios Fase 5](index.md) | [📥 Descargar .py](U22_ejercicios)

---

```python
# U22: EJERCICIOS — Visualización Financiera

import matplotlib
matplotlib.use("Agg")  # modo no interactivo para scripts
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Datos compartidos
np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=180, freq="B")

# 3 activos con distinta volatilidad
activos = {
    "AAPL": {"spot": 150, "mu": 0.10, "sigma": 0.22},
    "MSFT": {"spot": 310, "mu": 0.08, "sigma": 0.18},
    "TSLA": {"spot": 250, "mu": 0.12, "sigma": 0.35},
}

df_precios = pd.DataFrame(index=fechas)
for ticker, params in activos.items():
    ret = np.random.normal(params["mu"] / 252, params["sigma"] / np.sqrt(252), 180)
    ret[0] = 0
    df_precios[ticker] = params["spot"] * np.cumprod(1 + ret)

df_retornos = df_precios.pct_change().dropna()

# ============================================================
# Ejercicio 1: Equity curve de 3 activos (línea)
# Crea un gráfico de línea con los 3 activos normalizados
# (precio / precio_inicial * 100, para que todos partan de 100).
# Incluye:
#   - Título: "Retorno Acumulado — Comparación de Activos"
#   - Etiquetas en ejes
#   - Leyenda
#   - Grid
#   - Línea horizontal en 100 (punto de partida)
# Guarda el gráfico como "U22_ej1_equity_curves.png"
# ============================================================
print("=== Ejercicio 1: Equity curves ===")

# Escribe tu código aquí



# Output esperado:
# Gráfico guardado en: U22_ej1_equity_curves.png
# (Ver archivo: 3 líneas de colores partiendo de 100, linea punteada en 100)


# ============================================================
# Ejercicio 2: Subplots — Precio + Volumen + Drawdown
# Crea una figura con 3 subplots (sharex=True):
#   Panel 1 (60% altura): Precio de AAPL con línea y fill_between desde el mínimo
#   Panel 2 (20% altura): Volumen simulado (np.random.randint) como barras,
#                          verdes si el retorno diario >= 0, rojas si < 0
#   Panel 3 (20% altura): Drawdown diario de AAPL como fill_between rojo
# Incluye títulos en cada panel, etiquetas, grid.
# Guarda como "U22_ej2_subplots.png"
# ============================================================
print("\\n=== Ejercicio 2: Subplots precio/volumen/drawdown ===")

# Escribe tu código aquí



# Output esperado:
# Gráfico guardado en: U22_ej2_subplots.png
# (Ver archivo: 3 paneles verticales con precio, volumen coloreado, drawdown)


# ============================================================
# Ejercicio 3: Heatmap de correlación sectorial con Seaborn
# Dada una matriz de correlación de 6 sectores:
#   sectores = ["Tecnología", "Finanzas", "Energía", "Salud", "Industrial", "Consumo"]
# Genera retornos sintéticos para 6 sectores (252 días) con correlación inducida
# (usa np.random.multivariate_normal o construye manualmente con Cholesky).
# Crea un heatmap con:
#   - seaborn.heatmap
#   - annot=True, fmt=".2f"
#   - cmap="RdYlBu", center=0, vmin=-1, vmax=1
#   - Título
# Guarda como "U22_ej3_heatmap.png"
# ============================================================
print("\\n=== Ejercicio 3: Heatmap de correlación ===")

# Escribe tu código aquí



# Output esperado:
# Gráfico guardado en: U22_ej3_heatmap.png
# (Ver archivo: heatmap 6×6 con colores RdYlBu y valores anotados)


# ============================================================
# Ejercicio 4: Dashboard interactivo con Plotly
# Usando plotly.graph_objects y make_subplots:
# Crea un dashboard de 3 paneles para AAPL (60 días de datos):
#   Panel 1: Candlestick (Open, High, Low, Close) + SMA 20 como línea naranja
#   Panel 2: Volumen como barras (verde si cierre >= apertura, rojo si no)
#   Panel 3: RSI(14) como línea púrpura + líneas horizontales en 70 (roja) y 30 (verde)
# Configura:
#   - shared_xaxes=True
#   - height=800
#   - template="plotly_white"
#   - xaxis_rangeslider_visible=False
# Guarda como archivo HTML: "U22_ej4_dashboard.html"
# ============================================================
print("\\n=== Ejercicio 4: Dashboard Plotly interactivo ===")

# Escribe tu código aquí



# Output esperado:
# Dashboard interactivo guardado en: U22_ej4_dashboard.html
# (Abrir en navegador: candlestick + volumen + RSI con zoom y hover)
```

---

> [📥 Descargar archivo .py](U22_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 5](index.md)
