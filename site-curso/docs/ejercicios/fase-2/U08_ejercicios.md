# 📝 Ejercicios: U08 — Fase 2

> [← Volver a ejercicios Fase 2](index.md) | [📥 Descargar .py](U08_ejercicios)

---

```python
# U08: EJERCICIOS — Diccionarios: Portafolios y Datos Estructurados

# ============================================================
# Ejercicio 1: Portafolio de 5 activos
# Dado un dict de cantidades y precios actuales, calcula:
# - Valor total del portafolio
# - Peso (%) de cada activo
# - Rendimiento ponderado (usando precios de compra vs actuales)
# ============================================================
print("=== Ejercicio 1: Portafolio de 5 Activos ===")
cantidades = {"AAPL": 10, "MSFT": 5, "TSLA": 3, "JPM": 20, "XOM": 15}
precios_compra = {"AAPL": 150, "MSFT": 280, "TSLA": 900, "JPM": 135, "XOM": 85}
precios_actuales = {"AAPL": 175, "MSFT": 310, "TSLA": 820, "JPM": 142, "XOM": 90}

# Escribe tu código aquí



# Output esperado:
# Activo    Cant     Precio     Valor       Peso   Rendimiento
# AAPL      10       $175.00    $1,750.00   14.8%  +16.67%
# MSFT      5        $310.00    $1,550.00   13.1%  +10.71%
# TSLA      3        $820.00    $2,460.00   20.8%  -8.89%
# JPM       20       $142.00    $2,840.00   24.0%  +5.19%
# XOM       15       $90.00     $1,350.00   11.4%  +5.88%
# -------------------------------------------------------
# Total: $11,950.00 | Rend. ponderado: +3.42%


# ============================================================
# Ejercicio 2: Agrupador por sector (defaultdict)
# Agrupa el valor del portafolio por sector.
# Calcula el valor total y el peso de cada sector.
# ============================================================
print("\\n=== Ejercicio 2: Agrupador por Sector ===")
from collections import defaultdict

portafolio = {
    "AAPL": {"cantidad": 10, "precio": 175, "sector": "Tecnología"},
    "MSFT": {"cantidad": 5, "precio": 310, "sector": "Tecnología"},
    "GOOGL": {"cantidad": 8, "precio": 140, "sector": "Tecnología"},
    "XOM": {"cantidad": 20, "precio": 85, "sector": "Energía"},
    "JPM": {"cantidad": 15, "precio": 142, "sector": "Finanzas"},
    "CVX": {"cantidad": 10, "precio": 150, "sector": "Energía"},
    "GS": {"cantidad": 5, "precio": 380, "sector": "Finanzas"},
}

# Escribe tu código aquí



# Output esperado:
# Sector       Valor        Peso
# Tecnología   $4,420.00    37.4%
# Energía      $3,200.00    27.1%
# Finanzas     $4,030.00    34.1%
# ------------------------------
# Total: $11,650.00


# ============================================================
# Ejercicio 3: Contador de transacciones (Counter)
# Cuenta las transacciones por tipo (compra/venta) y por ticker.
# Muestra los 3 tickers más transados.
# ============================================================
print("\\n=== Ejercicio 3: Contador de Transacciones ===")
from collections import Counter

transacciones = [
    ("AAPL", "compra"), ("MSFT", "compra"), ("AAPL", "venta"),
    ("TSLA", "compra"), ("MSFT", "venta"), ("AAPL", "compra"),
    ("JPM", "compra"), ("TSLA", "venta"), ("AAPL", "venta"),
    ("MSFT", "compra"), ("TSLA", "compra"), ("JPM", "venta"),
    ("AAPL", "compra"), ("XOM", "compra"), ("MSFT", "venta"),
]

# Escribe tu código aquí



# Output esperado:
# Tipos de orden: Counter({'compra': 9, 'venta': 6})
# Tickers más transados: [('AAPL', 5), ('MSFT', 4), ('TSLA', 3)]


# ============================================================
# Ejercicio 4: Ratios financieros con dicts anidados
# Con los estados financieros de 3 empresas, calcula:
# - Ratio de liquidez (activos_corrientes / pasivos_corrientes)
# - Ratio de endeudamiento (pasivos_totales / activos_totales)
# - ROE aproximado (patrimonio / activos_totales)
# ============================================================
print("\\n=== Ejercicio 4: Ratios Financieros ===")
balances = {
    "AAPL": {"activos_corrientes": 143, "activos_totales": 352, "pasivos_corrientes": 145, "pasivos_totales": 302, "patrimonio": 50},
    "MSFT": {"activos_corrientes": 169, "activos_totales": 364, "pasivos_corrientes": 95, "pasivos_totales": 198, "patrimonio": 166},
    "JPM": {"activos_corrientes": 1200, "activos_totales": 3800, "pasivos_corrientes": 900, "pasivos_totales": 3500, "patrimonio": 300},
}
# (valores en miles de millones USD)

# Escribe tu código aquí



# Output esperado:
# Ticker  Liquidez  Endeudam.  ROE aprox
# AAPL    0.99      85.8%      14.2%
# MSFT    1.78      54.4%      45.6%
# JPM     1.33      92.1%      7.9%
```

---

> [📥 Descargar archivo .py](U08_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 2](index.md)
