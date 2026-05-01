# U17: Métodos Especiales y Data Classes — Operaciones Financieras Elegantes

> **Lectura previa:** [U16: Herencia y Polimorfismo](../fase-4/U16-herencia.md)
> **Próxima unidad:** [U18: Patrones de Diseño en Finanzas](./U18-patrones-diseno.md)

---

## 1. Teoría

### 1.1 Dunder methods: operadores para tus objetos financieros

Los **métodos dunder** (double underscore) permiten que tus objetos respondan a operadores de Python (`+`, `==`, `<`, `len()`, `[]`). En finanzas esto significa sumar portafolios, comparar trades y acceder a elementos por índice.

```python
class Portafolio:
    def __init__(self, nombre: str, activos: dict = None):
        self.nombre = nombre
        self.activos = activos or {}

    def valor_total(self) -> float:
        return sum(act["cantidad"] * act["precio"] for act in self.activos.values())

    # ----- DUNDER METHODS -----

    def __add__(self, otro: 'Portafolio') -> 'Portafolio':
        """Suma dos portafolios: combina activos."""
        combinado = {}
        for ticker, datos in self.activos.items():
            combinado[ticker] = datos.copy()
        for ticker, datos in otro.activos.items():
            if ticker in combinado:
                cant_total = combinado[ticker]["cantidad"] + datos["cantidad"]
                precio_prom = (
                    (combinado[ticker]["cantidad"] * combinado[ticker]["precio"] +
                     datos["cantidad"] * datos["precio"]) / cant_total
                )
                combinado[ticker] = {"cantidad": cant_total, "precio": precio_prom}
            else:
                combinado[ticker] = datos.copy()
        return Portafolio(f"{self.nombre}+{otro.nombre}", combinado)

    def __eq__(self, otro: 'Portafolio') -> bool:
        """Dos portafolios son iguales si tienen el mismo valor total."""
        return abs(self.valor_total() - otro.valor_total()) < 0.01

    def __lt__(self, otro: 'Portafolio') -> bool:
        return self.valor_total() < otro.valor_total()

    def __len__(self) -> int:
        """Número de tickers distintos en el portafolio."""
        return len(self.activos)

    def __contains__(self, ticker: str) -> bool:
        return ticker in self.activos

    def __str__(self):
        return f"{self.nombre}: {len(self)} activos | ${self.valor_total():,.2f}"


pf1 = Portafolio("Growth", {"AAPL": {"cantidad": 100, "precio": 175}})
pf2 = Portafolio("Value", {"MSFT": {"cantidad": 50, "precio": 310}, "AAPL": {"cantidad": 50, "precio": 180}})

pf3 = pf1 + pf2                          # __add__
print(pf3)                               # Growth+Value: 2 activos | $41,500.00
print(pf1 > pf2)                         # __lt__ → True
print("AAPL" in pf3)                     # __contains__ → True
print(f"Cantidad de tickers: {len(pf3)}") # __len__ → 2
```

> 💡 **Tip:** `__add__` hace que `port_a + port_b` sea sintaxis natural. En un sistema real, esto podría representar la fusión de dos fondos.

### 1.2 `__getitem__` y `__iter__`: portafolios como colecciones

```python
class OrderBook:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ordenes = []  # lista de dicts: {id, lado, cantidad, precio}

    def agregar(self, id_orden: str, lado: str, cantidad: int, precio: float):
        self.ordenes.append({"id": id_orden, "lado": lado,
                             "cantidad": cantidad, "precio": precio})

    def __getitem__(self, indice):
        """Permite slicing y acceso por índice: book[0], book[:5]"""
        return self.ordenes[indice]

    def __iter__(self):
        """Permite iterar: for orden in book:"""
        return iter(self.ordenes)

    def __len__(self):
        return len(self.ordenes)

    def __bool__(self):
        """Book vacío = False."""
        return len(self.ordenes) > 0

    def mejor_precio(self, lado: str) -> float | None:
        ordenes_lado = [o for o in self.ordenes if o["lado"] == lado]
        if not ordenes_lado:
            return None
        if lado == "compra":
            return max(o["precio"] for o in ordenes_lado)
        else:
            return min(o["precio"] for o in ordenes_lado)


book = OrderBook("AAPL")
book.agregar("O001", "compra", 100, 174.50)
book.agregar("O002", "compra", 200, 174.00)
book.agregar("O003", "venta", 150, 175.00)
book.agregar("O004", "venta", 100, 175.50)

print(f"Total órdenes: {len(book)}")
print(f"Primera orden: {book[0]['id']}")

for orden in book[:3]:  # slicing
    print(f"  {orden['id']}: {orden['lado']} {orden['cantidad']} @ ${orden['precio']:.2f}")

print(f"Mejor compra: ${book.mejor_precio('compra'):.2f}")
print(f"Mejor venta: ${book.mejor_precio('venta'):.2f}")
```

### 1.3 `@dataclass`: menos boilerplate para registros financieros

Las dataclasses (Python 3.7+) eliminan la necesidad de escribir `__init__`, `__repr__`, `__eq__` manualmente. Ideales para registros de trades, órdenes y datos tabulares.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Operacion:
    """Un trade ejecutado."""
    ticker: str
    lado: str              # "COMPRA" o "VENTA"
    cantidad: int
    precio: float
    fecha: datetime = field(default_factory=datetime.now)
    comision: float = 1.00

    @property
    def monto(self) -> float:
        return self.cantidad * self.precio

    @property
    def monto_neto(self) -> float:
        return self.monto - self.comision


@dataclass
class Posicion:
    """Estado acumulado de un ticker."""
    ticker: str
    cantidad: int = 0
    costo_promedio: float = 0.0

    def actualizar(self, operacion: Operacion):
        if operacion.lado == "COMPRA":
            costo_total = self.cantidad * self.costo_promedio + operacion.monto
            self.cantidad += operacion.cantidad
            self.costo_promedio = costo_total / self.cantidad if self.cantidad > 0 else 0
        else:
            self.cantidad -= operacion.cantidad

    @property
    def valor_mercado(self, precio_actual: float) -> float:
        return self.cantidad * precio_actual

    def pnl(self, precio_actual: float) -> float:
        return self.valor_mercado(precio_actual) - self.cantidad * self.costo_promedio


# Uso
trade1 = Operacion("AAPL", "COMPRA", 100, 150.0)
trade2 = Operacion("AAPL", "COMPRA", 50, 160.0)

print(trade1)  # Operacion(ticker='AAPL', lado='COMPRA', cantidad=100, ...)
print(f"Monto neto: ${trade2.monto_neto:,.2f}")

pos = Posicion("AAPL")
pos.actualizar(trade1)
pos.actualizar(trade2)
print(f"Cantidad: {pos.cantidad}, Costo prom: ${pos.costo_promedio:.2f}")
print(f"P&L a $175: ${pos.pnl(175.0):,.2f}")
```

> ⚠️ **Cuidado con mutabilidad:** Por defecto `@dataclass` hace las instancias mutables. Para inmutabilidad, usa `@dataclass(frozen=True)`. Para tipos de dato simples, `NamedTuple` es más ligero.

### 1.4 `NamedTuple`: registros inmutables y ligeros

```python
from typing import NamedTuple

class Cotizacion(NamedTuple):
    """Un snapshot de precios en un instante. Inmutable por diseño."""
    ticker: str
    apertura: float
    maximo: float
    minimo: float
    cierre: float
    volumen: int

    def rango_diario(self) -> float:
        return self.maximo - self.minimo

    def rendimiento(self) -> float:
        return ((self.cierre / self.apertura) - 1) * 100

    def volatilidad_intradiaria(self) -> float:
        return (self.rango_diario() / self.apertura) * 100


cot = Cotizacion("AAPL", 175.0, 178.5, 173.2, 177.0, 45_000_000)
print(f"Rango: ${cot.rango_diario():.2f}")
print(f"Rendimiento: {cot.rendimiento():.2f}%")

# cot.cierre = 180  # AttributeError: NamedTuple es inmutable
```

### 1.5 `__slots__`: ahorro de memoria para millones de objetos

En sistemas de trading de alta frecuencia, se crean millones de objetos `Orden`. `__slots__` reduce el uso de memoria entre 40-50% eliminando el `__dict__` interno.

```python
class OrdenHFT:
    __slots__ = ("id_orden", "ticker", "lado", "cantidad", "precio", "timestamp")

    def __init__(self, id_orden: str, ticker: str, lado: str,
                 cantidad: int, precio: float, timestamp: float):
        self.id_orden = id_orden
        self.ticker = ticker
        self.lado = lado
        self.cantidad = cantidad
        self.precio = precio
        self.timestamp = timestamp

    def valor(self) -> float:
        return self.cantidad * self.precio

    def __repr__(self):
        return f"OrdenHFT({self.id_orden}, {self.lado} {self.cantidad}@{self.precio})"


# Comparación de memoria (aproximada)
from dataclasses import dataclass

@dataclass
class OrdenDataclass:
    id_orden: str
    ticker: str
    lado: str
    cantidad: int
    precio: float
    timestamp: float

# OrdenDataclass usa ~56 bytes más por instancia que OrdenHFT
```

> 💡 **Tip:** Usa `__slots__` solo cuando tengas MILLONES de instancias y la memoria sea crítica. Para casos normales, `@dataclass` es más legible y mantenible.

### 1.6 Comparaciones personalizadas para instrumentos

```python
from functools import total_ordering

@total_ordering
@dataclass
class Activo:
    ticker: str
    precio: float
    capitalizacion: float  # market cap en miles de millones

    def __eq__(self, otro):
        if not isinstance(otro, Activo):
            return NotImplemented
        return self.ticker == otro.ticker

    def __lt__(self, otro):
        if not isinstance(otro, Activo):
            return NotImplemented
        return self.precio < otro.precio

    def __hash__(self):
        return hash(self.ticker)


activos = [
    Activo("AAPL", 175.0, 2800),
    Activo("MSFT", 310.0, 2300),
    Activo("TSLA", 250.0, 800),
]

activos_ordenados = sorted(activos)  # por precio
print([a.ticker for a in activos_ordenados])  # ['AAPL', 'TSLA', 'MSFT']
```

> ⚠️ **`@total_ordering`** del módulo `functools` genera automáticamente `__le__`, `__gt__`, `__ge__` a partir de `__eq__` y `__lt__`.

---

## 2. Práctica

### 2.1 Ejercicio guiado: OrderBook con dataclasses y dunders

**Concepto financiero:** Un libro de órdenes muestra la profundidad de mercado. Los traders lo usan para evaluar liquidez y decidir ejecución.

**Código:**

```python
from dataclasses import dataclass

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

    def volumen_por_lado(self, lado: str) -> int:
        return sum(o.cantidad for o in self.ordenes if o.lado == lado)

    def spread(self) -> float:
        compras = [o.precio for o in self.ordenes if o.lado == "compra"]
        ventas = [o.precio for o in self.ordenes if o.lado == "venta"]
        if not compras or not ventas:
            return 0.0
        return min(ventas) - max(compras)

    def resumen(self) -> str:
        return (f"{self.ticker}: {len(self)} órdenes | "
                f"Vol compra: {self.volumen_por_lado('compra')} | "
                f"Vol venta: {self.volumen_por_lado('venta')} | "
                f"Spread: ${self.spread():.2f}")


book1 = OrderBook("AAPL")
book1.agregar(Orden("O01", "compra", 100, 174.50))
book1.agregar(Orden("O02", "compra", 200, 174.00))
book1.agregar(Orden("O03", "venta", 150, 175.00))

print(book1.resumen())
print(f"Primera orden: {book1[0]}")

for orden in book1:
    print(f"  {orden.id_orden}: {orden.lado} {orden.cantidad} @ ${orden.precio}")
```

---

## 3. Aplicación en Finanzas 💰

En un **exchange electrónico** (NASDAQ, BATS), el order book se reconstruye en tiempo real con dataclasses inmutables y `__slots__` para minimizar latencia. Cada `Orden` tiene ~50 nanosegundos de vida en memoria antes de ser matcheada o descartada.

En **risk management**, los operadores suman portafolios con `__add__` para consolidar exposición global de un desk completo en un solo comando.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-4/U17_ejercicios.py`

1. **`@dataclass Operacion` y `Posicion`:** Dataclass `Operacion` (ticker, lado, cantidad, precio, comision) y clase `Posicion` que acumule trades y calcule costo promedio y P&L.
2. **`OrderBook` completo con dunders:** `__getitem__`, `__len__`, `__iter__`, `__add__`, `__contains__`, método `spread()`, `mejor_precio()`.
3. **Comparación y ordenamiento de `Activo`:** `__eq__`, `__lt__`, `__hash__` para ordenar por ratio de Sharpe descendente.
4. **Fusión de portafolios con `__add__`:** Dos `Portafolio` que al sumarse combinan posiciones promediando precios de compra.

---

## 5. Resumen

| Concepto | Sintaxis | Uso financiero |
|---------|----------|----------------|
| `__add__` | `def __add__(self, otro):` | `pf_total = pf1 + pf2` |
| `__eq__` | `def __eq__(self, otro):` | Comparar portafolios |
| `__lt__` | `def __lt__(self, otro):` | Ordenar activos |
| `__getitem__` | `def __getitem__(self, i):` | `book[0]` |
| `__iter__` | `def __iter__(self):` | `for orden in book:` |
| `@dataclass` | `@dataclass class Orden:` | Trades, órdenes |
| `NamedTuple` | `class Cotizacion(NamedTuple):` | Snapshot inmutable |
| `__slots__` | `__slots__ = ("id", "precio")` | HFT, millones de órdenes |

---

## ✅ Autoevaluación

1. ¿Qué método dunder permite sumar dos portafolios con el operador `+`?
2. ¿Cuándo usarías `@dataclass` vs `NamedTuple`?
3. ¿Qué ventaja tiene `__slots__` y cuándo no deberías usarlo?
4. ¿Cómo habilitas el operador `in` para tu clase?
5. ¿Qué generas con `functools.total_ordering`?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Dunders = operadores Python para tus objetos. `__add__` suma portafolios, `__getitem__` indexa órdenes
> - `@dataclass` elimina boilerplate para registros financieros (trades, cotizaciones)
> - `NamedTuple` = inmutable y ligero; `__slots__` = máxima eficiencia de memoria para HFT
