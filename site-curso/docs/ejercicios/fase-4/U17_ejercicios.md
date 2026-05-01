# 📝 Ejercicios: U17 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U17_ejercicios)

---

```python
# U17: EJERCICIOS — Métodos Especiales y Data Classes

# ============================================================
# Ejercicio 1: Dataclass Operacion y clase Posicion
# Crea:
#   - @dataclass Operacion con campos: ticker, lado (COMPRA/VENTA),
#     cantidad, precio, comision=1.00
#     Propiedad monto: cantidad * precio
#     Propiedad monto_neto: monto - comision
#   - @dataclass Posicion con campos: ticker, cantidad=0, costo_promedio=0.0
#     Método actualizar(self, op: Operacion): ajusta cantidad y costo_promedio
#     Método valor_mercado(self, precio_actual): cantidad * precio_actual
#     Método pnl(self, precio_actual): valor_mercado - costo_total
# Simula 3 compras y 1 venta parcial de AAPL.
# ============================================================
print("=== Ejercicio 1: Dataclass Operacion y Posicion ===")

# Escribe tu código aquí



# Output esperado:
# COMPRA AAPL: 100 × $150.00 = $15,000.00 | Neto: $14,999.00
# COMPRA AAPL: 50 × $160.00 = $8,000.00 | Neto: $7,999.00
# VENTA AAPL: 30 × $155.00 = $4,650.00 | Neto: $4,649.00
# COMPRA AAPL: 80 × $170.00 = $13,600.00 | Neto: $13,599.00
# Posición final: 200 acciones | Costo prom: $155.50 | Valor @ $175.00: $35,000.00 | P&L: $3,900.00


# ============================================================
# Ejercicio 2: OrderBook completo con dunders
# Crea la clase OrderBook con:
#   - __init__(self, ticker)
#   - agregar(self, orden: Orden)
#   - __getitem__(self, indice) → soporta slicing
#   - __len__(self) → número de órdenes
#   - __iter__(self) → iterar sobre órdenes
#   - __add__(self, otro) → combinar dos OrderBook
#   - __contains__(self, id_orden) → buscar por id_orden
#   - spread(self) → mejor venta - mejor compra (0 si no hay)
#   - resumen(self) → str con estadísticas
# Usa @dataclass Orden(id_orden, lado, cantidad, precio).
# Prueba con 6 órdenes en un book de MSFT.
# ============================================================
print("\\n=== Ejercicio 2: OrderBook completo ===")

# Escribe tu código aquí



# Output esperado:
# MSFT: 6 órdenes | Vol compra: 450 | Vol venta: 450 | Spread: $0.50
# Mejor compra: $309.00 | Mejor venta: $309.50
# Primera orden: Orden(id_orden='O01', lado='compra', cantidad=100, precio=309.00)
# Últimas 3 órdenes:
#   O04: venta 200 @ $309.50
#   O05: venta 100 @ $310.00
#   O06: compra 50 @ $308.50
# ¿Contiene O03? True


# ============================================================
# Ejercicio 3: Ordenamiento de activos por Sharpe Ratio
# Crea @dataclass ActivoRentable con:
#   - ticker, retorno_anual, volatilidad_anual, tasa_libre_riesgo=0.03
#   - Propiedad sharpe_ratio: (retorno - tasa_libre) / volatilidad
# Implementa __eq__, __lt__, __hash__ para que:
#   - Dos activos sean iguales si tienen mismo ticker
#   - Orden natural: mayor Sharpe primero
#   - Hash basado en ticker
# Crea 5 activos, ordénalos por Sharpe y muestra ranking.
# ============================================================
print("\\n=== Ejercicio 3: Ranking por Sharpe Ratio ===")

# Escribe tu código aquí



# Output esperado:
# Ranking por Sharpe Ratio:
# 1. AAPL  | Ret: 25.00% | Vol: 18.00% | Sharpe: 1.22
# 2. NVDA  | Ret: 35.00% | Vol: 30.00% | Sharpe: 1.07
# 3. MSFT  | Ret: 20.00% | Vol: 17.00% | Sharpe: 1.00
# 4. JPM   | Ret: 15.00% | Vol: 22.00% | Sharpe: 0.55
# 5. XOM   | Ret: 10.00% | Vol: 20.00% | Sharpe: 0.35
# Mejor activo: AAPL (Sharpe: 1.22)
# ¿AAPL en top 3? True


# ============================================================
# Ejercicio 4: Fusión de portafolios con __add__
# Implementa Portafolio con:
#   - __init__(self, nombre): activos = dict {ticker: {"cantidad", "precio_compra"}}
#   - agregar(self, ticker, cantidad, precio_compra)
#   - valor_total(self, precios_actuales) → float
#   - __add__(self, otro) → combina activos (suma cantidades, promedia precios ponderados)
#   - __len__(self) → número de tickers distintos
#   - __str__(self) → tabla resumen
# Fusiona dos portafolios con solapamiento en AAPL.
# ============================================================
print("\\n=== Ejercicio 4: Fusión de portafolios ===")

# Escribe tu código aquí



# Output esperado:
# Portafolio A: 2 activos | Valor: $31,500.00
#   AAPL: 100 × $150.00 = $15,000.00
#   MSFT: 50 × $330.00 = $16,500.00
# Portafolio B: 2 activos | Valor: $12,000.00
#   AAPL: 30 × $160.00 = $4,800.00
#   TSLA: 30 × $240.00 = $7,200.00
# Fusión A+B: 3 activos | Valor: $43,500.00
#   AAPL: 130 × $152.31 = $19,800.00
#   MSFT: 50 × $330.00 = $16,500.00
#   TSLA: 30 × $240.00 = $7,200.00
```

---

> [📥 Descargar archivo .py](U17_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
