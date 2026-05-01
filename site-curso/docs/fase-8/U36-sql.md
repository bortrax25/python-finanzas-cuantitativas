# U36: SQL para Datos Financieros

> **Lectura previa:** [U35: Econometría Financiera — Regresión y Panel Data](./U35-econometria.md)
> **Próxima unidad:** [U37: Machine Learning para Finanzas — Fundamentos](../fase-9/U37-ml-fundamentos.md)

---

## 1. Teoría

### 1.1 ¿Por qué SQL en finanzas cuantitativas?

En un desk de trading real, los datos NO viven en archivos CSV sueltos. Viven en bases de datos relacionales (PostgreSQL en Citadel, KDB+ en desks de high-frequency, SQLite para investigación local). SQL te permite:

- Consultar eficientemente millones de registros de precios
- Unir precios con datos fundamentales y factores
- Calcular métricas agregadas sin cargar todo en memoria
- Crear pipelines de datos reproducibles

```python
import sqlite3
import pandas as pd
import numpy as np

# SQLite es perfecto para datos locales (sin servidor)
conexion = sqlite3.connect(':memory:')  # o 'mis_datos.db' para persistente

print("Base de datos SQLite creada en memoria")
```

### 1.2 SELECT, WHERE, JOIN, GROUP BY — Lo esencial

```python
# Creamos tablas de ejemplo
cursor = conexion.cursor()

# Tabla de precios diarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS precios (
        fecha DATE,
        ticker TEXT,
        precio_cierre REAL,
        volumen INTEGER
    )
""")

# Tabla de información fundamental
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fundamentales (
        ticker TEXT PRIMARY KEY,
        sector TEXT,
        market_cap REAL,
        per_ratio REAL,
        roe REAL
    )
""")

# Tabla de factores (Fama-French)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS factores (
        fecha DATE,
        mercado REAL,
        smb REAL,
        hml REAL
    )
""")

# Insertar datos de ejemplo
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM', 'V', 'JNJ', 'WMT']
fechas = pd.date_range('2020-01-02', '2024-12-31', freq='B').strftime('%Y-%m-%d').tolist()

for fecha in fechas:
    for ticker in tickers:
        precio = 100 + np.cumsum(np.random.normal(0, 0.5, 1))[0]
        volumen = int(np.random.uniform(1e6, 10e6))
        cursor.execute("INSERT INTO precios VALUES (?, ?, ?, ?)",
                       (fecha, ticker, max(precio, 10), volumen))

# Fundamentales
datos_fund = [
    ('AAPL', 'Tecnología', 3e12, 28.5, 0.45),
    ('MSFT', 'Tecnología', 2.8e12, 32.1, 0.40),
    ('GOOGL', 'Tecnología', 1.8e12, 24.3, 0.30),
    ('TSLA', 'Automotriz', 800e9, 55.2, 0.20),
    ('JPM', 'Financiero', 500e9, 12.0, 0.15),
    ('V', 'Financiero', 560e9, 30.5, 0.48),
    ('JNJ', 'Salud', 450e9, 16.8, 0.28),
    ('WMT', 'Consumo', 420e9, 25.0, 0.22),
]
cursor.executemany("INSERT INTO fundamentales VALUES (?, ?, ?, ?, ?)", datos_fund)

# Factores Fama-French diarios (simulados)
for fecha in fechas:
    cursor.execute("INSERT INTO factores VALUES (?, ?, ?, ?)",
                   (fecha, np.random.normal(0.0003, 0.012),
                    np.random.normal(0.0001, 0.005),
                    np.random.normal(0.0002, 0.004)))

conexion.commit()

# SELECT básico
consulta = """
    SELECT ticker, fecha, precio_cierre
    FROM precios
    WHERE ticker = 'AAPL'
    ORDER BY fecha DESC
    LIMIT 5
"""
df_aapl = pd.read_sql(consulta, conexion)
print(f"Últimos 5 precios de AAPL:\n{df_aapl}\n")

# JOIN: precios + fundamentales
consulta = """
    SELECT p.fecha, p.ticker, p.precio_cierre, f.sector, f.per_ratio
    FROM precios p
    JOIN fundamentales f ON p.ticker = f.ticker
    WHERE p.fecha = (SELECT MAX(fecha) FROM precios)
    ORDER BY f.market_cap DESC
"""
df_join = pd.read_sql(consulta, conexion)
print(f"Precios + fundamentales (último día):\n{df_join}\n")

# GROUP BY y agregaciones
consulta = """
    SELECT
        ticker,
        ROUND(AVG(precio_cierre), 2) as precio_promedio,
        ROUND(MAX(precio_cierre), 2) as precio_maximo,
        ROUND(MIN(precio_cierre), 2) as precio_minimo,
        ROUND(MAX(precio_cierre) / MIN(precio_cierre) - 1, 4) * 100 as rango_pct
    FROM precios
    GROUP BY ticker
    ORDER BY rango_pct DESC
"""
df_agregado = pd.read_sql(consulta, conexion)
print(f"Estadísticas por ticker:\n{df_agregado}\n")
```

### 1.3 Window Functions (Funciones de Ventana)

Las window functions son el superpoder de SQL para finanzas. Permiten cálculos rolling sin sacar datos de la base.

```python
# LAG: precio del día anterior
consulta = """
    SELECT
        ticker,
        fecha,
        precio_cierre,
        LAG(precio_cierre, 1) OVER (PARTITION BY ticker ORDER BY fecha) as precio_anterior,
        ROUND((precio_cierre / LAG(precio_cierre, 1) OVER (PARTITION BY ticker ORDER BY fecha) - 1) * 100, 4) as retorno_pct
    FROM precios
    WHERE ticker IN ('AAPL', 'MSFT')
    ORDER BY ticker, fecha DESC
    LIMIT 10
"""
df_lag = pd.read_sql(consulta, conexion)
print(f"Retornos diarios con LAG:\n{df_lag}\n")

# RANK y ROW_NUMBER: ranking de desempeño
consulta = """
    SELECT
        ticker,
        fecha,
        precio_cierre,
        RANK() OVER (PARTITION BY fecha ORDER BY precio_cierre DESC) as ranking
    FROM precios
    WHERE fecha IN ('2024-12-30', '2024-12-31')
    ORDER BY fecha, ranking
"""
df_rank = pd.read_sql(consulta, conexion)
print(f"Ranking de precios por día:\n{df_rank}\n")

# Media móvil con window function
consulta = """
    SELECT DISTINCT
        ticker,
        fecha,
        precio_cierre,
        ROUND(AVG(precio_cierre) OVER (
            PARTITION BY ticker
            ORDER BY fecha
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
        ), 2) as sma_20
    FROM precios
    WHERE ticker = 'AAPL'
    ORDER BY fecha DESC
    LIMIT 10
"""
df_sma = pd.read_sql(consulta, conexion)
print(f"SMA 20 de AAPL (últimos 10 días):\n{df_sma}\n")
```

### 1.4 CTEs (Common Table Expressions) y Subconsultas

Las CTEs (`WITH`) hacen consultas complejas más legibles. Subconsultas anidadas son útiles para filtrar basado en agregaciones.

```python
# CTE para calcular retornos y luego filtrar
consulta = """
    WITH retornos_diarios AS (
        SELECT
            ticker,
            fecha,
            (precio_cierre / LAG(precio_cierre) OVER (PARTITION BY ticker ORDER BY fecha) - 1) * 100 as retorno
        FROM precios
    ),
    estadisticas_retornos AS (
        SELECT
            ticker,
            COUNT(retorno) as n_dias,
            ROUND(AVG(retorno), 6) as retorno_medio,
            ROUND(AVG(retorno * retorno), 8) as retorno_cuad_medio
        FROM retornos_diarios
        WHERE retorno IS NOT NULL
        GROUP BY ticker
    )
    SELECT
        ticker,
        retorno_medio,
        ROUND(SQRT(n_dias / (n_dias - 1.0) * (retorno_cuad_medio - retorno_medio * retorno_medio)), 6) as volatilidad
    FROM estadisticas_retornos
    ORDER BY volatilidad DESC
"""
df_cte = pd.read_sql(consulta, conexion)
print(f"Retorno medio y volatilidad por ticker (CTE):\n{df_cte}\n")

# Subconsulta para top performers del último mes
consulta = """
    SELECT ticker, ROUND(rendimiento, 2) as rendimiento_pct
    FROM (
        SELECT
            ticker,
            (MAX(CASE WHEN fecha = ultimo.dia THEN precio_cierre END) /
             MAX(CASE WHEN fecha = ultimo.inicio_mes THEN precio_cierre END) - 1) * 100 as rendimiento
        FROM precios,
             (SELECT MAX(fecha) as dia, DATE(MAX(fecha), '-21 days') as inicio_mes FROM precios) as ultimo
        WHERE fecha IN (ultimo.dia, ultimo.inicio_mes)
        GROUP BY ticker
    )
    ORDER BY rendimiento DESC
"""
df_top = pd.read_sql(consulta, conexion)
print(f"Top performers (último mes):\n{df_top}\n")
```

### 1.5 Indexación y rendimiento en SQLite

```python
# Crear índices para consultas frecuentes
conexion.execute("CREATE INDEX IF NOT EXISTS idx_precios_ticker ON precios(ticker)")
conexion.execute("CREATE INDEX IF NOT EXISTS idx_precios_fecha ON precios(fecha)")
conexion.execute("CREATE INDEX IF NOT EXISTS idx_precios_ticker_fecha ON precios(ticker, fecha)")

# Explicar plan de consulta
plan = pd.read_sql("EXPLAIN QUERY PLAN SELECT * FROM precios WHERE ticker = 'AAPL' AND fecha > '2024-01-01'", conexion)
print(f"Plan de consulta:\n{plan}\n")
```

### 1.6 SQLAlchemy — ORM para producción

SQLAlchemy permite trabajar con bases de datos usando objetos Python en lugar de SQL crudo.

```python
from sqlalchemy import create_engine, text

# Engine para SQLite
engine = create_engine('sqlite:///:memory:', echo=False)

# También funciona con PostgreSQL:
# engine = create_engine('postgresql://user:pass@localhost:5432/finanzas')

# Copiar DataFrame a SQL
df_precios = pd.DataFrame({
    'fecha': fechas[:100],
    'ticker': 'AAPL',
    'precio_cierre': np.random.normal(150, 2, 100)
})
df_precios.to_sql('precios', engine, index=False, if_exists='replace')

# Leer con SQLAlchemy
with engine.connect() as conn:
    resultado = conn.execute(text("SELECT COUNT(*) FROM precios"))
    print(f"Filas en tabla precios: {resultado.scalar()}")

# Pandas + SQLAlchemy
df = pd.read_sql("SELECT fecha, precio_cierre FROM precios ORDER BY fecha DESC LIMIT 5", engine)
print(f"\nÚltimos 5 precios desde SQLAlchemy:\n{df}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Base de datos de portafolio cuantitativo

**Concepto financiero:** Un quant necesita consultar rápidamente precios, calcular señales de momentum, y unir con datos fundamentales para construir portafolios.

**Código:**

```python
import sqlite3
import pandas as pd
import numpy as np

# Crear base de datos
conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Tablas
cursor.executescript("""
    CREATE TABLE precios (fecha TEXT, ticker TEXT, cierre REAL, volumen INTEGER);
    CREATE TABLE fundamentales (ticker TEXT PRIMARY KEY, sector TEXT, pe REAL, roe REAL, deuda_ebitda REAL);
""")

# Datos
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']
fechas = pd.date_range('2023-01-01', '2023-12-31', freq='B').strftime('%Y-%m-%d')

for ticker in tickers:
    precio_base = np.random.uniform(50, 300)
    precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.015, len(fechas))))
    for i, (fecha, precio) in enumerate(zip(fechas, precios)):
        cursor.execute("INSERT INTO precios VALUES (?, ?, ?, ?)",
                       (fecha, ticker, round(precio, 2), int(np.random.uniform(5e6, 20e6))))

# Fundamentales
fund_data = [
    ('AAPL', 'Tech', 28.5, 0.45, 1.2), ('MSFT', 'Tech', 32.1, 0.40, 0.8),
    ('GOOGL', 'Tech', 24.3, 0.30, 0.3), ('TSLA', 'Auto', 55.2, 0.20, 2.1),
    ('JPM', 'Fin', 12.0, 0.15, 3.5)
]
cursor.executemany("INSERT INTO fundamentales VALUES (?, ?, ?, ?, ?)", fund_data)
conexion.commit()

# Query 1: Top performers (momentum 3 meses)
query_momentum = """
    WITH retorno_3m AS (
        SELECT ticker,
            MAX(CASE WHEN fecha = '2023-12-29' THEN cierre END) as precio_fin,
            MAX(CASE WHEN fecha = '2023-09-29' THEN cierre END) as precio_ini
        FROM precios
        GROUP BY ticker
    )
    SELECT ticker, ROUND((precio_fin / precio_ini - 1) * 100, 2) as momentum_3m_pct
    FROM retorno_3m
    ORDER BY momentum_3m_pct DESC
"""
print("=== Momentum 3 meses ===\n")
print(pd.read_sql(query_momentum, conexion))

# Query 2: Value + Quality screen (bajo P/E + alto ROE)
query_value = """
    SELECT p.ticker, f.pe, f.roe, f.deuda_ebitda,
           ROUND(AVG(p.cierre), 2) as precio_promedio
    FROM precios p
    JOIN fundamentales f ON p.ticker = f.ticker
    WHERE f.pe < 30 AND f.roe > 0.20 AND f.deuda_ebitda < 2.0
    GROUP BY p.ticker
    ORDER BY f.pe ASC
"""
print("\n=== Value + Quality Screen ===\n")
print(pd.read_sql(query_value, conexion))

conexion.close()
```

**Output:**
```
=== Momentum 3 meses ===
  ticker  momentum_3m_pct
0   TSFT             8.75
1   GOOGL             5.21
2   AAPL             2.13
3     JPM            -1.45
4    TSLA            -3.89

=== Value + Quality Screen ===
  ticker    pe   roe  deuda_ebitda  precio_promedio
0   MSFT  32.1  0.40           0.8           290.45
1   AAPL  28.5  0.45           1.2           175.30
```

---

## 3. Aplicación en Finanzas 💰

**Hedge Funds (Renaissance Technologies):** Mantienen petabytes de datos en bases de datos relacionales. Cada analista escribe queries SQL para probar hipótesis antes de implementar en C++. SQL es la "primera línea" de investigación.

**Asset Management (BlackRock):** Aladdin, su plataforma de riesgo, usa SQL internamente para agregar riesgos a través de miles de portafolios. Los analistas de riesgo escriben queries para identificar concentraciones de riesgo.

**Banca de Inversión:** Las bases de datos de comps (comparables) se consultan con SQL para filtrar empresas por sector, rango de EV/EBITDA, crecimiento de revenue, etc.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-8/U36_ejercicios.py`

1. **Base de datos de precios:** Crear una BD SQLite con 5 años de precios para 10 tickers. Escribir queries para: (a) precio de cierre más reciente de cada ticker, (b) ticker con mayor rendimiento en 2024, (c) volatilidad anualizada de cada ticker.

2. **Portafolios de momentum:** Usando window functions, calcular retornos de 1, 3, 6 y 12 meses para cada ticker. Crear un ranking de momentum y seleccionar el top 3 y bottom 3 en cada fecha de rebalanceo trimestral.

3. **Factor sorts:** Unir precios con una tabla de factores (market_cap, book_to_market). Crear quintiles basados en estos factores. Para cada quintil, calcular el retorno promedio del mes siguiente (usar LEAD).

4. **Pipeline de datos automatizado:** Escribir un script que: (a) cree las tablas si no existen, (b) inserte nuevos precios evitando duplicados, (c) calcule y almacene señales en una tabla `señales`, (d) genere un reporte de los tickers con señales de compra.

---

## 5. Resumen

| Concepto | SQL / Python |
|----------|-------------|
| SELECT básico | `SELECT col FROM tabla WHERE cond` |
| JOIN | `FROM t1 JOIN t2 ON t1.key = t2.key` |
| GROUP BY | `GROUP BY ticker` con `AVG()`, `MAX()`, `COUNT()` |
| Window LAG | `LAG(precio, 1) OVER (PARTITION BY ticker ORDER BY fecha)` |
| Window RANK | `RANK() OVER (ORDER BY rendimiento DESC)` |
| Rolling window | `AVG() OVER (ROWS BETWEEN 19 PRECEDING AND CURRENT ROW)` |
| CTE | `WITH nombre AS (...) SELECT * FROM nombre` |
| Subconsulta | `WHERE ticker IN (SELECT ...)` |
| Conexión SQLite | `sqlite3.connect('db.sqlite')` |
| Leer en pandas | `pd.read_sql(query, conexion)` |
| SQLAlchemy engine | `create_engine('sqlite:///ruta')` |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre `WHERE` y `HAVING` en SQL?
2. ¿Para qué sirve `PARTITION BY` en una window function? Da un ejemplo financiero.
3. Explica la diferencia entre `RANK()` y `ROW_NUMBER()`. ¿Cuándo usarías cada una?
4. ¿Qué ventaja tiene usar una CTE (`WITH`) en lugar de subconsultas anidadas?
5. ¿Por qué los índices (`CREATE INDEX`) son importantes en bases de datos financieras grandes?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `PARTITION BY ticker ORDER BY fecha` es el patrón universal para cálculos por activo en series de tiempo
> - Window functions permiten cálculos rolling, LAG/LEAD, y rankings sin sacar datos de la BD
> - Las CTEs (`WITH`) hacen consultas complejas mantenibles y legibles
> - SQLite es suficiente para research local; PostgreSQL para producción multi-usuario
> - `pd.read_sql()` es la forma más rápida de traer resultados de SQL a un DataFrame
