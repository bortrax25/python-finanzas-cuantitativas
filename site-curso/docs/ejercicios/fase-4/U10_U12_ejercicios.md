# 📝 Ejercicios: U10 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U10_U12_ejercicios)

---

```python
# U10: EJERCICIOS — Listas y Tuplas / U11: Diccionarios / U12: CSV
# Ejercicios combinados FASE 4

# ============================================================
# U10 - Ejercicio 1: Rastreador de portafolio con listas
# Mantén una lista de (ticker, cantidad, precio_compra).
# Calcula el valor actual usando precios_actuales.
# ============================================================
print("=== U10: Rastreador de Portafolio ===")
portafolio = [
    ("AAPL", 10, 150.00),
    ("MSFT", 5, 280.00),
    ("TSLA", 3, 900.00),
]
precios_actuales = {"AAPL": 175.00, "MSFT": 310.00, "TSLA": 820.00}

# Escribe tu código aquí



# Output esperado:
# AAPL: 10 × $150.00 → Actual: $175.00 | P&L: $250.00 (16.67%)
# MSFT: 5 × $280.00 → Actual: $310.00 | P&L: $150.00 (10.71%)
# TSLA: 3 × $900.00 → Actual: $820.00 | P&L: -$240.00 (-8.89%)
# P&L Total: $160.00


# ============================================================
# U10 - Ejercicio 2: List comprehension + filtro
# Filtra acciones con PER < 15 y crecimiento > 10%
# ============================================================
print("\\n=== U10: Filtro de Oportunidades ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
]
# (ticker, PER, crecimiento %)

# Escribe tu código aquí



# Output esperado:
# Oportunidades (PER<15, Crec>10%): [('XOM', 10, 15), ('JPM', 9, 12), ('CVX', 11, 18)]


# ============================================================
# U11 - Ejercicio 1: Agrupador por sector
# Agrupa el portafolio por sector usando un defaultdict
# ============================================================
print("\\n=== U11: Agrupador por Sector ===")
from collections import defaultdict

portafolio = {
    "AAPL": {"cantidad": 10, "precio": 175, "sector": "Tecnología"},
    "MSFT": {"cantidad": 5, "precio": 310, "sector": "Tecnología"},
    "XOM": {"cantidad": 20, "precio": 85, "sector": "Energía"},
    "JPM": {"cantidad": 15, "precio": 140, "sector": "Finanzas"},
    "CVX": {"cantidad": 10, "precio": 150, "sector": "Energía"},
}

# Escribe tu código aquí



# Output esperado:
# Tecnología: $3,300.00
# Energía: $3,200.00
# Finanzas: $2,100.00


# ============================================================
# U12 - Ejercicio: Leer CSV y generar reporte
# ============================================================
print("\\n=== U12: Reporte desde CSV ===")
import csv, io

csv_data = """Date,Ticker,Type,Quantity,Price
2024-01-15,AAPL,BUY,10,150.50
2024-02-20,AAPL,BUY,5,155.00
2024-03-10,AAPL,SELL,8,175.00
2024-03-15,MSFT,BUY,4,305.00
2024-04-01,MSFT,SELL,4,320.00
"""

# Escribe tu código aquí



# Output esperado:
# AAPL: Compras $2,280.00 | Ventas $1,400.00 | P&L -$880.00
# MSFT: Compras $1,220.00 | Ventas $1,280.00 | P&L $60.00
```

---

> [📥 Descargar archivo .py](U10_U12_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
