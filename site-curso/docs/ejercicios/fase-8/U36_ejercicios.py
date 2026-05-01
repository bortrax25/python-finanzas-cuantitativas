# U36: EJERCICIOS — SQL para Datos Financieros

# ============================================================
# Ejercicio 1: Base de datos de precios y queries básicas
# Crea una BD SQLite en memoria con una tabla 'precios' que tenga:
#   fecha TEXT, ticker TEXT, cierre REAL, volumen INTEGER
# Inserta 3 años de precios simulados para 8 tickers.
# Escribe queries para:
#   (a) Último precio de cierre de cada ticker
#   (b) Ticker con mayor rendimiento en 2023 (último día / primer día - 1)
#   (c) Volatilidad anualizada de cada ticker (std * sqrt(252))
# ============================================================
import sqlite3
import pandas as pd
import numpy as np

print("=== Ejercicio 1: Base de datos de precios ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Base de datos de precios ===
# Último precio de cada ticker:
#   AAPL: 178.50
#   MSFT: 312.30
#   ...
# Mayor rendimiento 2023: MSFT (+15.4%)
# Volatilidad anualizada:
#   AAPL: 22.3%
#   MSFT: 19.8%
#   ...

conexion.close()


# ============================================================
# Ejercicio 2: Portafolios de momentum con window functions
# Usando la misma BD, calcula el retorno de momentum
# (1 mes, 3 meses, 6 meses, 12 meses) para cada ticker
# en cada fecha, usando LAG() window function.
# Crea un ranking por momentum trimestral:
#   - Cada 63 días de trading (~trimestre), selecciona top 3 y bottom 3
#   - Muestra el ranking de la fecha más reciente
# ============================================================
print("\n=== Ejercicio 2: Portafolios de Momentum ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Portafolios de Momentum ===
# Fecha rebalanceo: 2024-12-31
# Momentum 3 meses:
#   Top 3:    MSFT (+12.3%), AAPL (+8.7%), GOOGL (+5.4%)
#   Bottom 3: TSLA (-3.2%), JPM (-1.8%), V (+0.5%)

conexion.close()


# ============================================================
# Ejercicio 3: Factor sorts con quintiles
# Crea tablas adicionales: 'fundamentales' (ticker, market_cap, book_to_market)
# y 'factores' (fecha, retorno_mercado, smb, hml).
# Para cada mes, clasifica los tickers en quintiles basados en market_cap.
# Para cada quintil, calcula el rendimiento promedio del MES SIGUIENTE
# usando LEAD() window function sobre los retornos.
# Compara el retorno del quintil más bajo (small caps) vs más alto (large caps).
# ¿Hay una prima de tamaño (size premium)?
# ============================================================
print("\n=== Ejercicio 3: Factor Sorts ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Factor Sorts ===
# Quintil (market_cap) | Retorno medio siguiente mes
# Q1 (small caps)      | +0.82%
# Q2                   | +0.65%
# Q3                   | +0.58%
# Q4                   | +0.51%
# Q5 (large caps)      | +0.44%
# Size premium (Q1 - Q5): 0.38% mensual

conexion.close()


# ============================================================
# Ejercicio 4: Pipeline de datos automatizado
# Escribe un script que:
#   (a) Cree las tablas 'precios', 'fundamentales' y 'senales'
#       si no existen (CREATE TABLE IF NOT EXISTS)
#   (b) Inserta 5 tickers nuevos con datos simulados,
#       pero SIN duplicar fechas (usa INSERT OR IGNORE)
#   (c) Crea una tabla 'senales' calculando:
#       - momentum_3m: retorno de los últimos 63 días
#       - rsi_14: simplificado (usa cambio neto de 14 días)
#       - senal: 'COMPRA' si momentum_3m > 5%, 'VENTA' si < -5%
#   (d) Genera un reporte con los tickers que tienen señal de COMPRA
#       en la última fecha, mostrando ticker, momentum, y señal.
# ============================================================
print("\n=== Ejercicio 4: Pipeline de Datos Automatizado ===")

conexion = sqlite3.connect(':memory:')
cursor = conexion.cursor()

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Pipeline de Datos Automatizado ===
# Tablas creadas: precios, fundamentales, senales
# Datos insertados: 5 tickers, ~1260 días cada uno
# Tabla de señales poblada: XX señales de COMPRA, YY de VENTA
# Señales de COMPRA en última fecha:
#   MSFT   | momentum_3m=+8.2%  | COMPRA
#   AAPL   | momentum_3m=+5.7%  | COMPRA

conexion.close()
