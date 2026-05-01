# U10_U12: SOLUCIONES — FASE 4

# ============================================================
# U10 - Ejercicio 1: Rastreador de Portafolio
# ============================================================
print("=== U10: Rastreador de Portafolio ===")
portafolio = [
    ("AAPL", 10, 150.00),
    ("MSFT", 5, 280.00),
    ("TSLA", 3, 900.00),
]
precios_actuales = {"AAPL": 175.00, "MSFT": 310.00, "TSLA": 820.00}

pl_total = 0
for ticker, cantidad, precio_compra in portafolio:
    precio_actual = precios_actuales[ticker]
    valor_compra = cantidad * precio_compra
    valor_actual = cantidad * precio_actual
    pl = valor_actual - valor_compra
    pl_pct = (pl / valor_compra) * 100
    pl_total += pl
    print(f"{ticker}: {cantidad} × ${precio_compra:.2f} → Actual: ${precio_actual:.2f} | P&L: ${pl:+,.2f} ({pl_pct:+.2f}%)")

print(f"P&L Total: ${pl_total:+,.2f}")


# ============================================================
# U10 - Ejercicio 2: List comprehension + filtro
# ============================================================
print("\n=== U10: Filtro de Oportunidades ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
]

oportunidades = [a for a in acciones if a[1] < 15 and a[2] > 10]
print(f"Oportunidades (PER<15, Crec>10%): {oportunidades}")


# ============================================================
# U11 - Ejercicio 1: Agrupador por sector
# ============================================================
print("\n=== U11: Agrupador por Sector ===")
from collections import defaultdict

portafolio = {
    "AAPL": {"cantidad": 10, "precio": 175, "sector": "Tecnología"},
    "MSFT": {"cantidad": 5, "precio": 310, "sector": "Tecnología"},
    "XOM": {"cantidad": 20, "precio": 85, "sector": "Energía"},
    "JPM": {"cantidad": 15, "precio": 140, "sector": "Finanzas"},
    "CVX": {"cantidad": 10, "precio": 150, "sector": "Energía"},
}

por_sector = defaultdict(float)
for ticker, datos in portafolio.items():
    valor = datos["cantidad"] * datos["precio"]
    por_sector[datos["sector"]] += valor

for sector, valor in sorted(por_sector.items()):
    print(f"{sector}: ${valor:,.2f}")


# ============================================================
# U12 - Ejercicio: Reporte desde CSV
# ============================================================
print("\n=== U12: Reporte desde CSV ===")
import csv, io

csv_data = """Date,Ticker,Type,Quantity,Price
2024-01-15,AAPL,BUY,10,150.50
2024-02-20,AAPL,BUY,5,155.00
2024-03-10,AAPL,SELL,8,175.00
2024-03-15,MSFT,BUY,4,305.00
2024-04-01,MSFT,SELL,4,320.00
"""

reader = csv.DictReader(io.StringIO(csv_data))
compras = defaultdict(float)
ventas = defaultdict(float)

for fila in reader:
    ticker = fila["Ticker"]
    monto = int(fila["Quantity"]) * float(fila["Price"])
    if fila["Type"] == "BUY":
        compras[ticker] += monto
    else:
        ventas[ticker] += monto

todos_tickers = set(compras.keys()) | set(ventas.keys())
for ticker in sorted(todos_tickers):
    cmp = compras.get(ticker, 0)
    vta = ventas.get(ticker, 0)
    pl = vta - cmp
    print(f"{ticker}: Compras ${cmp:,.2f} | Ventas ${vta:,.2f} | P&L ${pl:+,.2f}")
