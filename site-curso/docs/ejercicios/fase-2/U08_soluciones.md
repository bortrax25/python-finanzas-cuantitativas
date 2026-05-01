# ✅ Soluciones: U08 — Fase 2

> [← Volver a ejercicios Fase 2](index.md) | [📥 Descargar .py](U08_soluciones)

---

```python
# U08: SOLUCIONES — Diccionarios: Portafolios y Datos Estructurados

# ============================================================
# Ejercicio 1: Portafolio de 5 Activos
# ============================================================
print("=== Ejercicio 1: Portafolio de 5 Activos ===")
cantidades = {"AAPL": 10, "MSFT": 5, "TSLA": 3, "JPM": 20, "XOM": 15}
precios_compra = {"AAPL": 150, "MSFT": 280, "TSLA": 900, "JPM": 135, "XOM": 85}
precios_actuales = {"AAPL": 175, "MSFT": 310, "TSLA": 820, "JPM": 142, "XOM": 90}

valor_total = 0
valores = {}
rendimientos = {}
for ticker in cantidades:
    valor_actual = cantidades[ticker] * precios_actuales[ticker]
    valor_compra = cantidades[ticker] * precios_compra[ticker]
    valores[ticker] = valor_actual
    rendimientos[ticker] = (valor_actual - valor_compra) / valor_compra * 100
    valor_total += valor_actual

print(f"{'Activo':<8} {'Cant':<6} {'Precio':<10} {'Valor':<12} {'Peso':<8} {'Rendimiento':<12}")
rend_ponderado = 0
for ticker in cantidades:
    peso = valores[ticker] / valor_total * 100
    rend_ponderado += peso * rendimientos[ticker] / 100
    print(f"{ticker:<8} {cantidades[ticker]:<6} ${precios_actuales[ticker]:<9,.2f} ${valores[ticker]:<11,.2f} {peso:<7.1f}% {rendimientos[ticker]:+>11.2f}%")

print("-" * 55)
print(f"Total: ${valor_total:,.2f} | Rend. ponderado: {rend_ponderado:+.2f}%")


# ============================================================
# Ejercicio 2: Agrupador por Sector (defaultdict)
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

por_sector = defaultdict(float)
for ticker, datos in portafolio.items():
    valor = datos["cantidad"] * datos["precio"]
    por_sector[datos["sector"]] += valor

total = sum(por_sector.values())

print(f"{'Sector':<12} {'Valor':<12} {'Peso':<8}")
for sector, valor in sorted(por_sector.items()):
    peso = valor / total * 100
    print(f"{sector:<12} ${valor:<11,.2f} {peso:<7.1f}%")

print("-" * 30)
print(f"Total: ${total:,.2f}")


# ============================================================
# Ejercicio 3: Contador de Transacciones
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

tipos = Counter(tipo for _, tipo in transacciones)
tickers = Counter(ticker for ticker, _ in transacciones)

print(f"Tipos de orden: {tipos}")
print(f"Tickers más transados: {tickers.most_common(3)}")


# ============================================================
# Ejercicio 4: Ratios Financieros
# ============================================================
print("\\n=== Ejercicio 4: Ratios Financieros ===")
balances = {
    "AAPL": {"activos_corrientes": 143, "activos_totales": 352, "pasivos_corrientes": 145, "pasivos_totales": 302, "patrimonio": 50},
    "MSFT": {"activos_corrientes": 169, "activos_totales": 364, "pasivos_corrientes": 95, "pasivos_totales": 198, "patrimonio": 166},
    "JPM": {"activos_corrientes": 1200, "activos_totales": 3800, "pasivos_corrientes": 900, "pasivos_totales": 3500, "patrimonio": 300},
}

print(f"{'Ticker':<8} {'Liquidez':<9} {'Endeudam.':<10} {'ROE aprox':<8}")
for ticker, datos in balances.items():
    liquidez = datos["activos_corrientes"] / datos["pasivos_corrientes"]
    endeudamiento = datos["pasivos_totales"] / datos["activos_totales"] * 100
    roe = datos["patrimonio"] / datos["activos_totales"] * 100
    print(f"{ticker:<8} {liquidez:<8.2f} {endeudamiento:<9.1f}% {roe:<7.1f}%")
```

---

> [📥 Descargar archivo .py](U08_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 2](index.md)
