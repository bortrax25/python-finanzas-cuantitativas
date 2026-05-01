# 📝 Ejercicios: U10 — Fase 2

> [← Volver a ejercicios Fase 2](index.md) | [📥 Descargar .py](U10_ejercicios)

---

```python
# U10: EJERCICIOS — Archivos y Datos: CSV, JSON y Datos de Mercado

# ============================================================
# Ejercicio 1: Lectura y estadísticas de CSV
# Lee el contenido CSV simulado y calcula:
# - Precio máximo de cierre y su fecha
# - Precio mínimo de cierre y su fecha
# - Precio promedio de cierre
# - Volumen total negociado
# ============================================================
print("=== Ejercicio 1: Estadísticas de CSV ===")
import csv, io

csv_datos = """Date,Open,High,Low,Close,Volume
2024-01-02,150.00,152.50,149.00,151.00,50000000
2024-01-03,151.00,153.00,150.00,152.50,45000000
2024-01-04,152.50,154.00,150.00,150.00,48000000
2024-01-05,150.00,153.50,149.50,153.00,52000000
2024-01-08,153.00,155.00,152.00,155.00,51000000
"""

# Escribe tu código aquí



# Output esperado:
# Máximo cierre: $155.00 (2024-01-08)
# Mínimo cierre: $150.00 (2024-01-04)
# Promedio cierre: $152.30
# Volumen total: 246,000,000


# ============================================================
# Ejercicio 2: Filtro y exportación de transacciones
# Dado un CSV de transacciones, filtra solo las del ticker indicado
# y exporta el resultado a un nuevo CSV.
# ============================================================
print("\\n=== Ejercicio 2: Filtro de Transacciones ===")

transacciones_csv = """Date,Ticker,Type,Quantity,Price
2024-01-15,AAPL,BUY,10,150.50
2024-02-20,MSFT,BUY,5,305.00
2024-03-10,AAPL,SELL,8,175.00
2024-03-15,MSFT,BUY,4,308.00
2024-04-01,MSFT,SELL,4,320.00
2024-05-20,AAPL,BUY,15,180.00
"""

# Filtra solo transacciones de AAPL y exporta a CSV
ticker_objetivo = "AAPL"

# Escribe tu código aquí



# Output esperado (en el CSV filtrado):
# Date,Ticker,Type,Quantity,Price
# 2024-01-15,AAPL,BUY,10,150.50
# 2024-03-10,AAPL,SELL,8,175.00
# 2024-05-20,AAPL,BUY,15,180.00


# ============================================================
# Ejercicio 3: CSV → JSON con pathlib
# Lee el CSV de precios, calcula estadísticas, y guarda en JSON
# usando pathlib para las rutas.
# ============================================================
print("\\n=== Ejercicio 3: CSV → JSON ===")
import json
from pathlib import Path

precios_csv = """Date,Close
2024-01-02,100.00
2024-01-03,102.00
2024-01-04,101.00
2024-01-05,105.00
2024-01-08,103.00
2024-01-09,108.00
2024-01-10,110.00
2024-01-11,107.00
2024-01-12,112.00
"""

# Escribe tu código aquí



# Output esperado (archivo JSON):
# {
#   "periodo": "2024-01-02 a 2024-01-12",
#   "dias": 9,
#   "precio_max": 112.00,
#   "precio_min": 100.00,
#   "precio_promedio": 105.33,
#   "retorno_total_pct": 12.00,
#   "volatilidad_diaria_pct": X.XX
# }


# ============================================================
# Ejercicio 4: Pipeline completo
# 1. Lee el CSV de precios (usa io.StringIO)
# 2. Calcula retornos diarios
# 3. Guarda las estadísticas en un archivo JSON
# 4. Guarda los retornos diarios en un archivo CSV
# ============================================================
print("\\n=== Ejercicio 4: Pipeline Completo ===")

datos = """Date,Open,High,Low,Close,Volume
2024-01-02,150.50,152.00,149.50,151.00,50100000
2024-01-03,151.00,153.50,150.00,152.50,45200000
2024-01-04,152.50,154.00,151.00,151.50,48300000
2024-01-05,151.50,153.00,150.50,152.80,49500000
2024-01-08,152.80,155.00,152.00,154.50,51200000
"""

# Escribe tu código aquí



# Output esperado:
# === Estadísticas ===
# Precio inicial: $151.00
# Precio final: $154.50
# Retorno total: 2.32%
# Volatilidad diaria: X.XX%
#
# Archivos generados:
# - /tmp/estadisticas.json
# - /tmp/retornos_diarios.csv
```

---

> [📥 Descargar archivo .py](U10_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 2](index.md)
