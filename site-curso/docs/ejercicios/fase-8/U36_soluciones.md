# ✅ Soluciones: U36 — Fase 8

> [← Volver a ejercicios Fase 8](index.md) | [📥 Descargar .py](U36_soluciones)

---

```python
# U36: SOLUCIONES — SQL para Datos Financieros

# ============================================================
# Ejercicio 1: Base de datos de precios y queries básicas
# ============================================================
import sqlite3
import pandas as pd
import numpy as np

print("=== Ejercicio 1: Base de datos de precios ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Crear tabla
cursor.execute("""
    CREATE TABLE precios (
        fecha TEXT,
        ticker TEXT,
        cierre REAL,
        volumen INTEGER
    )
""")

# Insertar datos
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM', 'V', 'JNJ', 'WMT']
fechas = pd.date_range('2022-01-03', '2024-12-31', freq='B').strftime('%Y-%m-%d').tolist()

for ticker in tickers:
    precio_base = np.random.uniform(50, 300)
    precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.015, len(fechas))))
    for fecha, precio in zip(fechas, precios):
        cursor.execute(
            "INSERT INTO precios VALUES (?, ?, ?, ?)",
            (fecha, ticker, round(precio, 2), int(np.random.uniform(1e6, 10e6)))
        )

# (a) Último precio de cada ticker
query_a = """
    SELECT ticker, cierre
    FROM precios
    WHERE fecha = (SELECT MAX(fecha) FROM precios)
    ORDER BY cierre DESC
"""
print("Último precio de cada ticker:")
for row in cursor.execute(query_a):
    print(f"  {row[0]}: {row[1]:.2f}")
conexion.commit()

# (b) Mayor rendimiento en 2023
query_b = """
    SELECT ticker,
           ROUND((MAX(CASE WHEN fecha = '2023-12-29' THEN cierre END) /
                  MAX(CASE WHEN fecha = '2023-01-03' THEN cierre END) - 1) * 100, 2) as rendimiento_2023
    FROM precios
    GROUP BY ticker
    ORDER BY rendimiento_2023 DESC
    LIMIT 1
"""
cursor.execute(query_b)
mejor = cursor.fetchone()
print(f"\\nMayor rendimiento 2023: {mejor[0]} ({mejor[1]:+.1f}%)")

# (c) Volatilidad anualizada
query_c = """
    SELECT ticker,
           ROUND(SQRT(AVG(ret * ret) * 252.0) * 100, 1) as vol_anualizada
    FROM (
        SELECT ticker,
               cierre / LAG(cierre) OVER (PARTITION BY ticker ORDER BY fecha) - 1 as ret
        FROM precios
    )
    WHERE ret IS NOT NULL
    GROUP BY ticker
    ORDER BY vol_anualizada DESC
"""
print(f"\\nVolatilidad anualizada:")
for row in cursor.execute(query_c):
    print(f"  {row[0]}: {row[1]:.1f}%")

conexion.close()


# ============================================================
# Ejercicio 2: Portafolios de momentum con window functions
# ============================================================
print("\\n=== Ejercicio 2: Portafolios de Momentum ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Crear tabla e insertar datos (simplificado)
cursor.execute("""
    CREATE TABLE precios (fecha TEXT, ticker TEXT, cierre REAL, volumen INTEGER)
""")

np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM', 'V']
fechas = pd.date_range('2024-01-02', '2024-12-31', freq='B').strftime('%Y-%m-%d').tolist()

for ticker in tickers:
    precio_base = np.random.uniform(80, 350)
    retornos = np.random.normal(0.0003, 0.012, len(fechas))
    precios = precio_base * np.exp(np.cumsum(retornos))
    for fecha, precio in zip(fechas, precios):
        cursor.execute(
            "INSERT INTO precios VALUES (?, ?, ?, ?)",
            (fecha, ticker, round(precio, 2), int(np.random.uniform(1e6, 10e6)))
        )
conexion.commit()

# Calcular momentum 3 meses en la última fecha
ultima_fecha = fechas[-1]
indice_3m_antes = max(0, len(fechas) - 63 - 1)
fecha_3m_antes = fechas[indice_3m_antes]

query = f"""
    SELECT ticker,
           ROUND((MAX(CASE WHEN fecha = '{ultima_fecha}' THEN cierre END) /
                  MAX(CASE WHEN fecha = '{fecha_3m_antes}' THEN cierre END) - 1) * 100, 2) as mom_3m
    FROM precios
    GROUP BY ticker
    ORDER BY mom_3m DESC
"""
cursor.execute(query)
resultados = cursor.fetchall()

print(f"Fecha rebalanceo: {ultima_fecha}")
print(f"Momentum 3 meses:")
print(f"  Top 3:    {resultados[0][0]} ({resultados[0][1]:+.1f}%), {resultados[1][0]} ({resultados[1][1]:+.1f}%), {resultados[2][0]} ({resultados[2][1]:+.1f}%)")
print(f"  Bottom 3: {resultados[-1][0]} ({resultados[-1][1]:+.1f}%), {resultados[-2][0]} ({resultados[-2][1]:+.1f}%), {resultados[-3][0]} ({resultados[-3][1]:+.1f}%)")

conexion.close()


# ============================================================
# Ejercicio 3: Factor sorts con quintiles
# ============================================================
print("\\n=== Ejercicio 3: Factor Sorts ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Crear tablas
cursor.execute("""
    CREATE TABLE precios (fecha TEXT, ticker TEXT, cierre REAL)
""")
cursor.execute("""
    CREATE TABLE fundamentales (ticker TEXT PRIMARY KEY, market_cap REAL)
""")

np.random.seed(42)
tickers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
fechas = pd.date_range('2024-01-02', '2024-12-31', freq='B').strftime('%Y-%m-%d').tolist()

# Insertar precios
for ticker in tickers:
    precio_base = np.random.uniform(50, 200)
    precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.012, len(fechas))))
    for fecha, precio in zip(fechas, precios):
        cursor.execute("INSERT INTO precios VALUES (?, ?, ?)", (fecha, ticker, round(precio, 2)))

# Insertar market caps
market_caps = {t: np.random.uniform(5e9, 500e9) for t in tickers}
for t, mc in market_caps.items():
    cursor.execute("INSERT INTO fundamentales VALUES (?, ?)", (t, round(mc, 0)))
conexion.commit()

# Quintiles basados en market_cap
cursor.execute("""
    WITH quintiles AS (
        SELECT p.ticker, p.fecha,
               cierre / LAG(cierre) OVER (PARTITION BY p.ticker ORDER BY p.fecha) - 1 as retorno,
               NTILE(5) OVER (ORDER BY f.market_cap) as quintil_mc
        FROM precios p
        JOIN fundamentales f ON p.ticker = f.ticker
    ),
    retornos_siguientes AS (
        SELECT quintil_mc, fecha, retorno,
               LEAD(retorno) OVER (PARTITION BY ticker ORDER BY fecha) as ret_siguiente
        FROM quintiles
    )
    SELECT quintil_mc, ROUND(AVG(ret_siguiente) * 100, 2) as retorno_medio
    FROM retornos_siguientes
    WHERE ret_siguiente IS NOT NULL
    GROUP BY quintil_mc
    ORDER BY quintil_mc
""")
resultados = cursor.fetchall()

print("Quintil (market_cap) | Retorno medio siguiente mes")
for q, r in resultados:
    etiqueta = "Q5 (large caps)" if q == 5 else "Q1 (small caps)" if q == 1 else f"Q{q}"
    print(f"{etiqueta:<21} | {r:+.2f}%")

if len(resultados) >= 2:
    premium = resultados[0][1] - resultados[-1][1]
    print(f"Size premium (Q1 - Q5): {premium:.2f}% mensual")

conexion.close()


# ============================================================
# Ejercicio 4: Pipeline de datos automatizado
# ============================================================
print("\\n=== Ejercicio 4: Pipeline de Datos Automatizado ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# (a) Crear tablas
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS precios (
        fecha TEXT, ticker TEXT, cierre REAL, volumen INTEGER,
        UNIQUE(fecha, ticker)
    );
    CREATE TABLE IF NOT EXISTS fundamentales (
        ticker TEXT PRIMARY KEY, sector TEXT, pe REAL
    );
    CREATE TABLE IF NOT EXISTS senales (
        fecha TEXT, ticker TEXT, momentum_3m REAL, senal TEXT,
        UNIQUE(fecha, ticker)
    );
""")
print("Tablas creadas: precios, fundamentales, senales")

# (b) Insertar datos sin duplicados
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']
fechas = pd.date_range('2023-01-02', '2024-12-31', freq='B').strftime('%Y-%m-%d').tolist()

for ticker in tickers:
    precio_base = np.random.uniform(60, 300)
    precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.012, len(fechas))))
    for fecha, precio in zip(fechas, precios):
        cursor.execute(
            "INSERT OR IGNORE INTO precios VALUES (?, ?, ?, ?)",
            (fecha, ticker, round(precio, 2), int(np.random.uniform(1e6, 10e6)))
        )

# Fundamentales
fund = [
    ('AAPL', 'Tecnología', 28.5), ('MSFT', 'Tecnología', 32.1),
    ('GOOGL', 'Tecnología', 24.3), ('TSLA', 'Automotriz', 55.2),
    ('JPM', 'Financiero', 12.0)
]
for f in fund:
    cursor.execute("INSERT OR IGNORE INTO fundamentales VALUES (?, ?, ?)", f)

print(f"Datos insertados: {len(tickers)} tickers, ~{len(fechas)} días cada uno")
conexion.commit()

# (c) Calcular señales
cursor.execute("""
    INSERT OR REPLACE INTO senales (fecha, ticker, momentum_3m, senal)
    SELECT
        fecha,
        ticker,
        momentum,
        CASE
            WHEN momentum > 5.0 THEN 'COMPRA'
            WHEN momentum < -5.0 THEN 'VENTA'
            ELSE 'NEUTRAL'
        END as senal
    FROM (
        SELECT
            fecha,
            ticker,
            ROUND((cierre / LAG(cierre, 63) OVER (PARTITION BY ticker ORDER BY fecha) - 1) * 100, 2) as momentum
        FROM precios
    )
    WHERE momentum IS NOT NULL
""")
conexion.commit()

# Contar señales
cursor.execute("SELECT senal, COUNT(*) FROM senales GROUP BY senal")
conteos = cursor.fetchall()
for senal, cuenta in conteos:
    print(f"Tabla de señales: {cuenta} señales de {senal}")

# (d) Reporte de señales de COMPRA en última fecha
ultima = fechas[-1]
query_reporte = f"""
    SELECT s.ticker, s.momentum_3m, s.senal
    FROM senales s
    WHERE s.fecha = '{ultima}' AND s.senal = 'COMPRA'
    ORDER BY s.momentum_3m DESC
"""
print(f"\\nSeñales de COMPRA en última fecha ({ultima}):")
cursor.execute(query_reporte)
for row in cursor.fetchall():
    print(f"  {row[0]:<6} | momentum_3m={row[1]:+.1f}%  | {row[2]}")

conexion.close()
```

---

> [📥 Descargar archivo .py](U36_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 8](index.md)
