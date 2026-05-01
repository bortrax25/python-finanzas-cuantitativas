# U16: NumPy y Pandas para Finanzas

> **Lectura previa:** [U15: Módulos, paquetes e intro a Jupyter](../fase-5/U15-modulos-jupyter.md)
> **Próxima unidad:** [U17: Cálculos financieros fundamentales](./U17-calculos-financieros.md)

## 1. NumPy — Cómputo numérico eficiente

```python
import numpy as np

# Arrays (más rápidos que listas)
precios = np.array([100, 102, 105, 103, 108])
rendimientos = np.diff(precios) / precios[:-1] * 100

# Operaciones vectorizadas (sin bucles)
rendimiento_total = (precios[-1] / precios[0] - 1) * 100
volatilidad = np.std(rendimientos, ddof=1)

# Funciones estadísticas
media = np.mean(precios)
mediana = np.median(precios)
maximo = np.max(precios)

# Generar números aleatorios
np.random.seed(42)
simulaciones = 100 * (1 + np.random.randn(1000) * 0.02).cumprod()
```

## 2. Pandas — Análisis de datos tabulares

```python
import pandas as pd

# Crear DataFrame desde diccionario
datos = {
    "Ticker": ["AAPL", "MSFT", "TSLA", "GOOGL"],
    "Precio": [175.50, 310.00, 250.00, 140.00],
    "PER": [28, 32, 65, 22],
    "Sector": ["Tec", "Tec", "Auto", "Tec"]
}
df = pd.DataFrame(datos)

# Operaciones básicas
print(df.head())
print(df.describe())
print(df["Sector"].value_counts())

# Filtrado
tecnologicas = df[df["Sector"] == "Tec"]
baratas = df[df["PER"] < 25]

# Agrupación
por_sector = df.groupby("Sector")["Precio"].mean()

# Leer/Escribir CSV
df.to_csv("acciones.csv", index=False)
df_leido = pd.read_csv("acciones.csv")

# Fechas
fechas = pd.date_range("2024-01-01", periods=100, freq="B")  # Días hábiles
df_tiempo = pd.DataFrame({"Precio": precios}, index=fechas)
print(df_tiempo.resample("W").last())  # Semanal
```

## 3. Finanzas con NumPy y Pandas

```python
# Rendimientos logarítmicos
precios = np.array([100, 102, 101, 105, 103, 108])
log_returns = np.diff(np.log(precios))

# Matriz de covarianza
rendimientos = np.random.randn(100, 3) * 0.02  # 100 días, 3 activos
cov_matrix = np.cov(rendimientos.T)

# Correlación
corr_matrix = np.corrcoef(rendimientos.T)

# Estadísticas del portafolio
pesos = np.array([0.4, 0.35, 0.25])
port_ret = np.dot(pesos, rendimientos.mean(axis=0)) * 252  # Anualizado
port_vol = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix * 252, pesos)))
sharpe = (port_ret - 0.04) / port_vol
```

## 4. Ejercicios Propuestos

1. Simula 1000 escenarios de precio con Monte Carlo y calcula VaR al 95%.
2. Carga un CSV de precios con Pandas y calcula medias móviles de 20 y 50 días.
3. Calcula la matriz de correlación de 4 activos y encuentra el par menos correlacionado.
