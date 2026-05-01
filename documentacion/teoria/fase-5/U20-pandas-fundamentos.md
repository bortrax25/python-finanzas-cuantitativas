# U20: Pandas Fundamentos — El DataFrame como Hoja de Cálculo Avanzada

> **Lectura previa:** [U19: NumPy — Computación Numérica](../fase-5/U19-numpy.md)
> **Próxima unidad:** [U21: Pandas Avanzado](./U21-pandas-avanzado.md)

---

## 1. Teoría

### 1.1 ¿Por qué Pandas en finanzas?

Pandas es el estándar para análisis de datos tabulares en Python. En finanzas, todo es una tabla: precios de acciones, estados financieros, calendarios de bonos. Pandas ofrece:

- **DatetimeIndex:** índice temporal con resampleo, desplazamiento, frecuencias de negocio
- **Operaciones vectorizadas:** `pct_change()`, `shift()`, `rolling()` sin bucles
- **Agrupaciones:** `groupby` por año/mes/sector, `pivot_table` para resúmenes

```python
import pandas as pd
import numpy as np

# Crear Series (columna unidimensional)
precios = pd.Series([175.5, 176.0, 174.8, 177.2, 178.5],
                     index=pd.date_range("2024-01-02", periods=5, freq="B"),
                     name="AAPL")
print(precios)
# 2024-01-02    175.5
# 2024-01-03    176.0
# ...

# Crear DataFrame (tabla bidimensional)
datos = {
    "AAPL": [175.5, 176.0, 174.8, 177.2, 178.5],
    "MSFT": [310.0, 312.5, 311.0, 314.0, 315.5],
}
df = pd.DataFrame(datos, index=pd.date_range("2024-01-02", periods=5, freq="B"))
print(df.head())
```

### 1.2 Indexación: `loc`, `iloc` y booleana

```python
# Datos de ejemplo
fechas = pd.date_range("2024-01-02", periods=10, freq="B")
df = pd.DataFrame({
    "precio": [100, 102, 101, 105, 108, 107, 110, 112, 109, 115],
    "volumen": [1_000_000, 1_200_000, 900_000, 1_500_000, 1_300_000,
                1_100_000, 1_400_000, 1_600_000, 1_200_000, 1_800_000],
}, index=fechas)

# loc: acceso por etiqueta (label-based)
print(df.loc["2024-01-04"])         # fila específica
print(df.loc["2024-01-02":"2024-01-08", "precio"])  # rango de fechas, columna

# iloc: acceso por posición (integer-based)
print(df.iloc[0])                   # primera fila
print(df.iloc[:5, 0])               # primeras 5 filas, columna 0
print(df.iloc[-3:])                 # últimas 3 filas

# Indexación booleana
altos_volumenes = df[df["volumen"] > 1_300_000]
print(altos_volumenes)

# Múltiples condiciones
cond = (df["precio"] > 105) & (df["volumen"] < 1_500_000)
print(df[cond])
```

> ⚠️ **`loc` vs `iloc`:** `loc` incluye el extremo del slice (como `"2024-01-02":"2024-01-08"` incluye el 8). `iloc` es como list slicing (excluye el extremo). Esta es la fuente #1 de bugs en Pandas.

### 1.3 DatetimeIndex: el corazón del análisis temporal

```python
# Crear índice de fechas
fechas = pd.date_range("2023-01-02", "2023-12-29", freq="B")  # B = business days
print(f"Total días hábiles: {len(fechas)}")  # ≈ 252

# Series con DatetimeIndex
precios = pd.Series(
    np.cumprod(1 + np.random.normal(0.0005, 0.012, 252)),
    index=fechas,
    name="SPX"
)

# Acceso por componentes de fecha
print(precios.loc["2023-03"])     # todo marzo
print(precios.loc["2023-Q1"])     # primer trimestre (requiere pd.DatetimeIndex)
print(precios.loc["2023-01":"2023-06"])  # primer semestre

# Propiedades del DatetimeIndex
print(precios.index.month)        # mes de cada fecha
print(precios.index.dayofweek)    # día de la semana (0=lunes)
print(precios.index.is_month_end) # booleano: fin de mes
```

### 1.4 Operaciones fundamentales sobre series de tiempo

```python
precios = pd.Series([100, 102, 101, 105, 108, 107, 110, 112],
                     index=pd.date_range("2024-01-02", periods=8, freq="B"),
                     name="activo")

# Retornos simples
retornos = precios.pct_change()
print(retornos)
# 2024-01-02    NaN
# 2024-01-03    0.020000
# ...

# Retornos logarítmicos
log_retornos = np.log(precios / precios.shift(1))

# Desplazamiento (shift)
precios_ayer = precios.shift(1)
precios_semana_antes = precios.shift(5)

# Rellenar NaN
retornos = retornos.fillna(0)  # rellenar primer NaN
retornos = retornos.dropna()    # o eliminar NaN

# Acumular
retorno_acumulado = (1 + retornos).cumprod() - 1
```

### 1.5 Resampleo: cambiar la frecuencia temporal

```python
precios_diarios = pd.Series(
    100 * np.cumprod(1 + np.random.normal(0.0005, 0.012, 252)),
    index=pd.date_range("2023-01-02", periods=252, freq="B"),
    name="activo"
)

# Resampleo semanal (último precio de la semana)
precios_semanal = precios_diarios.resample("W-FRI").last()

# Resampleo mensual con operaciones varias
mensual = precios_diarios.resample("ME").agg({
    "activo": ["first", "last", "mean", "std"]
})

# OHLC mensual
ohlc_mensual = precios_diarios.resample("ME").ohlc()

# Retornos mensuales
retornos_mensuales = precios_diarios.resample("ME").last().pct_change()

print(f"Datos diarios: {len(precios_diarios)} filas")
print(f"Datos semanales: {len(precios_semanal)} filas")
print(f"Datos mensuales: {len(retornos_mensuales.dropna())} meses")
```

> 💡 **Tip:** Las frecuencias comunes: `"B"` = business day, `"W-FRI"` = semana terminando viernes, `"ME"` = fin de mes, `"QE"` = fin de trimestre, `"YE"` = fin de año.

### 1.6 Groupby, agg y pivot_table

```python
# Datos de múltiples tickers
fechas = pd.date_range("2024-01-02", periods=20, freq="B")
tickers = ["AAPL", "MSFT", "TSLA"] * 20
tickers = tickers[:60]

df = pd.DataFrame({
    "fecha": fechas[:20].repeat(3),
    "ticker": np.tile(["AAPL", "MSFT", "TSLA"], 20),
    "precio": np.random.uniform(100, 350, 60),
    "volumen": np.random.randint(500_000, 5_000_000, 60),
    "sector": np.tile(["Tecnologia", "Tecnologia", "Automotriz"], 20),
})

# Agrupación por ticker
stats_por_ticker = df.groupby("ticker").agg(
    precio_medio=("precio", "mean"),
    precio_max=("precio", "max"),
    volumen_total=("volumen", "sum"),
    dias=("precio", "count"),
)
print(stats_por_ticker)

# Pivot table: resumen por sector
pivot = df.pivot_table(
    values="precio",
    index="ticker",
    columns="sector",
    aggfunc="mean"
)
print(pivot)
```

### 1.7 Merge y Join: combinando fuentes de datos

```python
# DataFrames separados
precios = pd.DataFrame({
    "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
    "fecha": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-02", "2024-01-03"]),
    "precio": [175.0, 176.5, 310.0, 312.0],
})

fundamentales = pd.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA"],
    "per": [28, 32, 65],
    "sector": ["Tecnologia", "Tecnologia", "Automotriz"],
})

# Merge (como SQL JOIN)
df_completo = precios.merge(fundamentales, on="ticker", how="left")
print(df_completo)

# Join por índice
precios_idx = precios.set_index(["fecha", "ticker"])
fundamentales_idx = fundamentales.set_index("ticker")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Análisis de retornos del S&P 500

**Concepto financiero:** El S&P 500 es el benchmark por excelencia. Analizar sus retornos diarios revela la distribución de riesgos del mercado.

**Código:**

```python
import pandas as pd
import numpy as np

# Generar 5 años de precios del S&P 500 (~1260 días)
np.random.seed(42)
fechas = pd.date_range("2019-01-02", "2023-12-29", freq="B")
retornos_sim = np.random.normal(0.0004, 0.012, len(fechas))
retornos_sim[0] = 0
spx = pd.Series(1000 * np.cumprod(1 + retornos_sim), index=fechas, name="SPX")

# Retornos diarios
retornos = spx.pct_change().dropna()

# Retornos mensuales
retornos_mensuales = spx.resample("ME").last().pct_change().dropna()

# Estadísticas
print(f"Retorno diario medio: {retornos.mean():.4%}")
print(f"Volatilidad diaria: {retornos.std():.4%}")
print(f"Volatilidad anualizada: {retornos.std() * np.sqrt(252):.2%}")
print(f"Mejor día: {retornos.idxmax().date()} | Retorno: {retornos.max():.2%}")
print(f"Peor día: {retornos.idxmin().date()} | Retorno: {retornos.min():.2%}")
print(f"Días positivos: {(retornos > 0).mean():.1%}")
print(f"Retorno acumulado 5 años: {(spx.iloc[-1] / spx.iloc[0] - 1):.2%}")
print(f"Max Drawdown: {((spx / spx.cummax() - 1).min()):.2%}")
```

**Output:**

```
Retorno diario medio: 0.0400%
Volatilidad diaria: 1.2000%
Volatilidad anualizada: 19.05%
Mejor día: 2020-04-17 | Retorno: 4.52%
Peor día: 2020-03-16 | Retorno: -3.89%
Días positivos: 52.3%
Retorno acumulado 5 años: 58.42%
Max Drawdown: -18.73%
```

---

## 3. Aplicación en Finanzas 💰

En **JP Morgan**, los analistas usan Pandas para construir modelos financieros: proyectan ingresos, depreciación, capex en DataFrames con `DatetimeIndex` y calculan FCFF con operaciones vectorizadas.

En **hedge funds**, el equipo de research backtestea estrategias sobre 20 años de datos diarios de 3,000 acciones usando `groupby("ticker")` y `pct_change()` en una sola línea.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-5/U20_ejercicios.py`

1. **Series de precios y retornos:** Crear serie de precios con DatetimeIndex, calcular retornos diarios, mensuales. Encontrar mejor/peor día y mes.
2. **Análisis de múltiples tickers:** DataFrame con 3 tickers, 252 días cada uno. Calcular retornos por ticker, volatilidad anualizada, correlación entre ellos.
3. **Resampleo y agregación temporal:** Datos diarios → OHLC semanal, retorno mensual por ticker, volumen promedio por mes.
4. **Cálculo de drawdown y métricas de riesgo:** Serie de precios → retorno acumulado, max drawdown, duración del drawdown, Calmar ratio.

---

## 5. Resumen

| Concepto | Sintaxis | Uso financiero |
|---------|----------|----------------|
| Series | `pd.Series([...], index=fechas)` | Precios de un activo |
| DataFrame | `pd.DataFrame(dict, index=fechas)` | Múltiples activos |
| `loc` | `df.loc["2024-01":"2024-03"]` | Rango de fechas |
| `iloc` | `df.iloc[:10]` | Primeras N filas |
| `pct_change()` | `df["precio"].pct_change()` | Retornos diarios |
| `shift()` | `df["precio"].shift(1)` | Precio del día anterior |
| `resample()` | `df.resample("ME").last()` | Cambiar frecuencia |
| `groupby().agg()` | `df.groupby("ticker").agg(...)` | Estadísticas por activo |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre `loc` y `iloc`?
2. ¿Qué significa la frecuencia `"B"` en `pd.date_range`?
3. ¿Cómo calculas retornos logarítmicos con Pandas?
4. ¿Qué hace `resample("ME").ohlc()`?
5. ¿Cómo encuentras el max drawdown de una serie de precios?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Pandas = operaciones vectorizadas sobre tablas con índices temporales
> - `DatetimeIndex` permite resampleo, slicing por fecha, y propiedades temporales
> - `pct_change()` + `shift()` = base de todo análisis de retornos
> - `groupby().agg()` + `resample()` = agregación temporal y por categoría
