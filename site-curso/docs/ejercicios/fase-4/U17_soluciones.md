# ✅ Soluciones: U17 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U17_soluciones)

---

```python
# U17: SOLUCIONES — Métodos Especiales y Data Classes

# ============================================================
# Ejercicio 1: Dataclass Operacion y clase Posicion
# ============================================================
print("=== Ejercicio 1: Dataclass Operacion y Posicion ===")

from dataclasses import dataclass


@dataclass
class Operacion:
    ticker: str
    lado: str
    cantidad: int
    precio: float
    comision: float = 1.00

    @property
    def monto(self) -> float:
        return self.cantidad * self.precio

    @property
    def monto_neto(self) -> float:
        return self.monto - self.comision


@dataclass
class Posicion:
    ticker: str
    cantidad: int = 0
    costo_promedio: float = 0.0

    def actualizar(self, op: Operacion):
        if op.lado == "COMPRA":
            costo_total_anterior = self.cantidad * self.costo_promedio
            costo_total_nuevo = costo_total_anterior + op.monto
            self.cantidad += op.cantidad
            self.costo_promedio = costo_total_nuevo / self.cantidad if self.cantidad > 0 else 0
        else:
            self.cantidad -= op.cantidad

    @property
    def costo_total(self) -> float:
        return self.cantidad * self.costo_promedio

    def valor_mercado(self, precio_actual: float) -> float:
        return self.cantidad * precio_actual

    def pnl(self, precio_actual: float) -> float:
        return self.valor_mercado(precio_actual) - self.costo_total


# Simulación
compras = [
    Operacion("AAPL", "COMPRA", 100, 150.0),
    Operacion("AAPL", "COMPRA", 50, 160.0),
    Operacion("AAPL", "VENTA", 30, 155.0),
    Operacion("AAPL", "COMPRA", 80, 170.0),
]

pos = Posicion("AAPL")
for op in compras:
    print(f"{op.lado} {op.ticker}: {op.cantidad} × ${op.precio:.2f} = ${op.monto:,.2f} | Neto: ${op.monto_neto:,.2f}")
    pos.actualizar(op)

precio_final = 175.0
print(f"Posición final: {pos.cantidad} acciones | "
      f"Costo prom: ${pos.costo_promedio:.2f} | "
      f"Valor @ ${precio_final:.2f}: ${pos.valor_mercado(precio_final):,.2f} | "
      f"P&L: ${pos.pnl(precio_final):,.2f}")

# ============================================================
# Ejercicio 2: OrderBook completo con dunders
# ============================================================
print("\\n=== Ejercicio 2: OrderBook completo ===")


@dataclass
class Orden:
    id_orden: str
    lado: str
    cantidad: int
    precio: float


class OrderBook:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ordenes: list[Orden] = []

    def agregar(self, orden: Orden):
        self.ordenes.append(orden)

    def __getitem__(self, indice):
        return self.ordenes[indice]

    def __len__(self):
        return len(self.ordenes)

    def __iter__(self):
        return iter(self.ordenes)

    def __add__(self, otro: 'OrderBook') -> 'OrderBook':
        nuevo = OrderBook(f"{self.ticker}+{otro.ticker}")
        nuevo.ordenes = self.ordenes + otro.ordenes
        return nuevo

    def __contains__(self, id_orden: str):
        return any(o.id_orden == id_orden for o in self.ordenes)

    def mejor_precio(self, lado: str) -> float:
        try:
            if lado == "compra":
                return max(o.precio for o in self.ordenes if o.lado == lado)
            else:
                return min(o.precio for o in self.ordenes if o.lado == lado)
        except ValueError:
            return 0.0

    def volumen_por_lado(self, lado: str) -> int:
        return sum(o.cantidad for o in self.ordenes if o.lado == lado)

    def spread(self) -> float:
        mejor_compra = self.mejor_precio("compra")
        mejor_venta = self.mejor_precio("venta")
        if mejor_compra == 0 or mejor_venta == 0:
            return 0.0
        return mejor_venta - mejor_compra

    def resumen(self) -> str:
        return (
            f"{self.ticker}: {len(self)} órdenes | "
            f"Vol compra: {self.volumen_por_lado('compra')} | "
            f"Vol venta: {self.volumen_por_lado('venta')} | "
            f"Spread: ${self.spread():.2f}"
        )


book = OrderBook("MSFT")
book.agregar(Orden("O01", "compra", 100, 309.00))
book.agregar(Orden("O02", "compra", 200, 308.00))
book.agregar(Orden("O03", "compra", 150, 308.50))
book.agregar(Orden("O04", "venta", 200, 309.50))
book.agregar(Orden("O05", "venta", 100, 310.00))
book.agregar(Orden("O06", "compra", 50, 308.50))

print(book.resumen())
print(f"Mejor compra: ${book.mejor_precio('compra'):.2f} | Mejor venta: ${book.mejor_precio('venta'):.2f}")
print(f"Primera orden: {book[0]}")
print("Últimas 3 órdenes:")
for orden in book[-3:]:
    print(f"  {orden.id_orden}: {orden.lado} {orden.cantidad} @ ${orden.precio:.2f}")
print(f"¿Contiene O03? {'O03' in book}")

# ============================================================
# Ejercicio 3: Ranking por Sharpe Ratio
# ============================================================
print("\\n=== Ejercicio 3: Ranking por Sharpe Ratio ===")

from functools import total_ordering


@total_ordering
@dataclass
class ActivoRentable:
    ticker: str
    retorno_anual: float
    volatilidad_anual: float
    tasa_libre_riesgo: float = 0.03

    @property
    def sharpe_ratio(self) -> float:
        if self.volatilidad_anual == 0:
            return 0.0
        return (self.retorno_anual - self.tasa_libre_riesgo) / self.volatilidad_anual

    def __eq__(self, otro):
        if not isinstance(otro, ActivoRentable):
            return NotImplemented
        return self.ticker == otro.ticker

    def __lt__(self, otro):
        if not isinstance(otro, ActivoRentable):
            return NotImplemented
        return self.sharpe_ratio > otro.sharpe_ratio  # invertido: mayor Sharpe = menor

    def __hash__(self):
        return hash(self.ticker)


activos = [
    ActivoRentable("AAPL", 0.25, 0.18),
    ActivoRentable("MSFT", 0.20, 0.17),
    ActivoRentable("NVDA", 0.35, 0.30),
    ActivoRentable("XOM", 0.10, 0.20),
    ActivoRentable("JPM", 0.15, 0.22),
]

activos_ordenados = sorted(activos)
print("Ranking por Sharpe Ratio:")
for i, a in enumerate(activos_ordenados, 1):
    print(f"{i}. {a.ticker:<6} | Ret: {a.retorno_anual*100:.2f}% | "
          f"Vol: {a.volatilidad_anual*100:.2f}% | Sharpe: {a.sharpe_ratio:.2f}")

mejor = activos_ordenados[0]
print(f"Mejor activo: {mejor.ticker} (Sharpe: {mejor.sharpe_ratio:.2f})")
print(f"¿AAPL en top 3? {'AAPL' in {a.ticker for a in activos_ordenados[:3]}}")

# ============================================================
# Ejercicio 4: Fusión de portafolios con __add__
# ============================================================
print("\\n=== Ejercicio 4: Fusión de portafolios ===")


class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.activos = {}  # {ticker: {"cantidad": int, "precio_compra": float}}

    def agregar(self, ticker: str, cantidad: int, precio_compra: float):
        self.activos[ticker] = {"cantidad": cantidad, "precio_compra": precio_compra}

    def valor_total(self, precios_actuales: dict = None) -> float:
        if precios_actuales is None:
            return sum(d["cantidad"] * d["precio_compra"] for d in self.activos.values())
        return sum(d["cantidad"] * precios_actuales.get(t, d["precio_compra"])
                   for t, d in self.activos.items())

    def __add__(self, otro: 'Portafolio') -> 'Portafolio':
        combinado = {}
        for ticker, datos in self.activos.items():
            combinado[ticker] = datos.copy()
        for ticker, datos in otro.activos.items():
            if ticker in combinado:
                cant1 = combinado[ticker]["cantidad"]
                prec1 = combinado[ticker]["precio_compra"]
                cant2 = datos["cantidad"]
                prec2 = datos["precio_compra"]
                cant_total = cant1 + cant2
                precio_prom = (cant1 * prec1 + cant2 * prec2) / cant_total
                combinado[ticker] = {"cantidad": cant_total, "precio_compra": round(precio_prom, 4)}
            else:
                combinado[ticker] = datos.copy()
        nuevo = Portafolio(f"{self.nombre}+{otro.nombre}")
        nuevo.activos = combinado
        return nuevo

    def __len__(self):
        return len(self.activos)

    def __str__(self):
        precio_actual = {t: d["precio_compra"] for t, d in self.activos.items()}
        lineas = [f"Portafolio {self.nombre}: {len(self)} activos | Valor: ${self.valor_total():,.2f}"]
        for ticker, datos in self.activos.items():
            valor = datos["cantidad"] * datos["precio_compra"]
            lineas.append(f"  {ticker}: {datos['cantidad']} × ${datos['precio_compra']:.2f} = ${valor:,.2f}")
        return "\\n".join(lineas)


pf_a = Portafolio("A")
pf_a.agregar("AAPL", 100, 150.00)
pf_a.agregar("MSFT", 50, 330.00)

pf_b = Portafolio("B")
pf_b.agregar("AAPL", 30, 160.00)
pf_b.agregar("TSLA", 30, 240.00)

print(pf_a)
print(pf_b)

pf_fusion = pf_a + pf_b
print(pf_fusion)
```

---

> [📥 Descargar archivo .py](U17_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
