# U16: Herencia y Polimorfismo — Jerarquía de Instrumentos Financieros

> **Lectura previa:** [U15: Clases y Objetos](../fase-4/U15-clases-objetos.md)
> **Próxima unidad:** [U17: Métodos Especiales y Data Classes](./U17-dunders-dataclasses.md)

---

## 1. Teoría

### 1.1 Herencia: el "es un" financiero

En finanzas, una **acción** es un **instrumento financiero**. Un **bono** es un **instrumento financiero**. Una **opción** es un **instrumento financiero**. La herencia modela esta relación natural.

```python
class Instrumento:
    """Clase base para todo instrumento financiero."""

    def __init__(self, ticker: str, nombre: str):
        self.ticker = ticker
        self.nombre = nombre

    def tipo(self) -> str:
        return "Instrumento genérico"

    def __repr__(self):
        return f"{self.__class__.__name__}(ticker='{self.ticker}')"


class Accion(Instrumento):
    """Una acción hereda de Instrumento."""

    def __init__(self, ticker: str, nombre: str, precio: float, cantidad: int):
        super().__init__(ticker, nombre)  # llama al __init__ del padre
        self.precio = precio
        self.cantidad = cantidad

    def tipo(self) -> str:
        return "Renta Variable"

    def valor_mercado(self) -> float:
        return self.precio * self.cantidad


class Bono(Instrumento):
    """Un bono también hereda de Instrumento."""

    def __init__(self, ticker: str, nombre: str, valor_nominal: float,
                 tasa_cupon: float, vencimiento: int):
        super().__init__(ticker, nombre)
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon
        self.vencimiento = vencimiento

    def tipo(self) -> str:
        return "Renta Fija"

    def valor_mercado(self) -> float:
        return self.valor_nominal * (1 + self.tasa_cupon * self.vencimiento)


aapl = Accion("AAPL", "Apple Inc.", 175.0, 100)
bono_usa = Bono("UST10Y", "US Treasury 10Y", 1000, 0.05, 10)

print(aapl)              # Accion(ticker='AAPL')
print(aapl.tipo())       # Renta Variable
print(aapl.valor_mercado())  # 17500.0
print(bono_usa.tipo())   # Renta Fija
```

> 💡 **Tip:** `super().__init__()` llama al constructor de la clase padre. Esto evita duplicar la inicialización de `ticker` y `nombre` en cada subclase.

### 1.2 Clases Abstractas: el contrato financiero

Una **clase abstracta** define un contrato: todas las subclases DEBEN implementar ciertos métodos. En finanzas esto garantiza que todo instrumento tenga, por ejemplo, un método `valorar()`.

```python
from abc import ABC, abstractmethod

class Instrumento(ABC):
    """Clase abstracta: no se puede instanciar directamente."""

    def __init__(self, ticker: str, nombre: str):
        self.ticker = ticker
        self.nombre = nombre

    @abstractmethod
    def valorar(self) -> float:
        """Todo instrumento debe saber valorizarse."""
        pass

    @abstractmethod
    def riesgo(self) -> str:
        """Todo instrumento debe reportar su nivel de riesgo."""
        pass

    def resumen(self) -> str:
        """Método concreto: usa los abstractos."""
        return f"{self.ticker} | Valor: ${self.valorar():,.2f} | Riesgo: {self.riesgo()}"


class Accion(Instrumento):
    def __init__(self, ticker: str, nombre: str, precio: float, cantidad: int):
        super().__init__(ticker, nombre)
        self.precio = precio
        self.cantidad = cantidad

    def valorar(self) -> float:
        return self.precio * self.cantidad

    def riesgo(self) -> str:
        return "Alto" if self.precio > 200 else "Moderado"


class Bono(Instrumento):
    def __init__(self, ticker: str, nombre: str, valor_nominal: float,
                 tasa_cupon: float, vencimiento: int, calificacion: str):
        super().__init__(ticker, nombre)
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon
        self.vencimiento = vencimiento
        self.calificacion = calificacion

    def valorar(self) -> float:
        # Valor presente simplificado: nominal + cupones descontados
        return self.valor_nominal * (1 + self.tasa_cupon * self.vencimiento)

    def riesgo(self) -> str:
        if self.calificacion in ("AAA", "AA"):
            return "Bajo"
        elif self.calificacion in ("A", "BBB"):
            return "Moderado"
        else:
            return "Alto (High Yield)"


# instrumento = Instrumento("X", "Y")  # TypeError: no se puede instanciar ABC
accion = Accion("AAPL", "Apple", 175.0, 100)
bono = Bono("UST10Y", "US Treasury", 1000, 0.05, 10, "AAA")

print(accion.resumen())
print(bono.resumen())
```

> ⚠️ **Importante:** Si una subclase no implementa un `@abstractmethod`, Python lanza `TypeError` al intentar instanciarla. Esto fuerza el contrato en tiempo de ejecución.

### 1.3 Polimorfismo: mismo mensaje, distinto comportamiento

El polimorfismo permite tratar objetos de distintas clases de manera uniforme. Un `Portafolio` no necesita saber si contiene acciones o bonos; solo necesita llamar a `valorar()`.

```python
class Opcion(Instrumento):
    def __init__(self, ticker: str, subyacente: str, tipo_opcion: str,
                 precio_strike: float, precio_subyacente: float, cantidad: int):
        super().__init__(ticker, f"Opción {tipo_opcion} sobre {subyacente}")
        self.subyacente = subyacente
        self.tipo_opcion = tipo_opcion  # "CALL" o "PUT"
        self.precio_strike = precio_strike
        self.precio_subyacente = precio_subyacente
        self.cantidad = cantidad

    def valorar(self) -> float:
        if self.tipo_opcion == "CALL":
            valor_intrinseco = max(0, self.precio_subyacente - self.precio_strike)
        else:
            valor_intrinseco = max(0, self.precio_strike - self.precio_subyacente)
        return valor_intrinseco * self.cantidad * 100

    def riesgo(self) -> str:
        return "Muy Alto (derivado)"


class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.instrumentos: list[Instrumento] = []

    def agregar(self, instrumento: Instrumento):
        self.instrumentos.append(instrumento)

    def valor_total(self) -> float:
        # POLIMORFISMO: mismo método valorar(), distinto resultado
        return sum(inst.valorar() for inst in self.instrumentos)

    def resumen_por_tipo(self) -> dict:
        resumen = {}
        for inst in self.instrumentos:
            tipo = inst.__class__.__name__
            resumen[tipo] = resumen.get(tipo, 0) + inst.valorar()
        return resumen

    def __str__(self):
        partes = [f"Portafolio: {self.nombre}"]
        for inst in self.instrumentos:
            partes.append(f"  {inst.resumen()}")
        partes.append(f"  VALOR TOTAL: ${self.valor_total():,.2f}")
        return "\n".join(partes)


pf = Portafolio("Multi-Asset")
pf.agregar(Accion("AAPL", "Apple", 175.0, 100))
pf.agregar(Bono("UST10Y", "US Treasury", 10000, 0.05, 10, "AAA"))
pf.agregar(Opcion("AAPL250C", "AAPL", "CALL", 170.0, 175.0, 5))
print(pf)
```

### 1.4 Composición vs Herencia

| Característica | Herencia ("es un") | Composición ("tiene un") |
|---------------|-------------------|-------------------------|
| Relación | `Accion` es un `Instrumento` | `Portafolio` tiene `Instrumento`s |
| Acoplamiento | Alto | Bajo |
| Flexibilidad | Menor | Mayor |
| Cuándo usarlo | Jerarquías naturales | Relaciones "parte de" |

```python
# Composición: un Portafolio no ES un Instrumento, TIENE Instrumentos
class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.instrumentos = []  # COMPOSICIÓN: contiene instrumentos

# Composición: un OrderBook tiene Orders
class Orden:
    def __init__(self, id_orden: str, ticker: str, lado: str, cantidad: int, precio: float):
        self.id_orden = id_orden
        self.ticker = ticker
        self.lado = lado
        self.cantidad = cantidad
        self.precio = precio

class OrderBook:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ordenes_compra = []   # COMPOSICIÓN
        self.ordenes_venta = []    # COMPOSICIÓN
```

### 1.5 Mixins: comportamiento transversal

Un mixin es una clase que aporta funcionalidad sin ser una entidad principal. Se usa con herencia múltiple.

```python
import time
import json

class LoggingMixin:
    """Agrega logging a cualquier instrumento."""

    def registrar_operacion(self, operacion: str, detalle: dict):
        entrada = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "clase": self.__class__.__name__,
            "ticker": self.ticker,
            "operacion": operacion,
            "detalle": detalle,
        }
        print(f"[LOG] {json.dumps(entrada)}")


class AccionConLog(Accion, LoggingMixin):
    """Acción que hereda de Accion y LoggingMixin."""

    def vender(self, cantidad: int, precio: float):
        self.registrar_operacion("VENTA", {"cantidad": cantidad, "precio": precio})


accion = AccionConLog("MSFT", "Microsoft", 310.0, 50)
accion.vender(10, 320.0)
```

> ⚠️ **Cuidado con la herencia múltiple:** Python usa MRO (Method Resolution Order) para decidir qué método se ejecuta. Con mixins, coloca siempre el mixin a la izquierda para que sus métodos tengan prioridad.

---

## 2. Práctica

### 2.1 Ejercicio guiado: Jerarquía de Valoración

**Concepto financiero:** Cada tipo de instrumento se valora de forma distinta, pero todos comparten la interfaz `valorar()`.

**Código:**

```python
from abc import ABC, abstractmethod

class Instrumento(ABC):
    def __init__(self, ticker: str):
        self.ticker = ticker

    @abstractmethod
    def valorar(self, **kwargs) -> float:
        pass


class Accion(Instrumento):
    def __init__(self, ticker: str, precio: float, cantidad: int):
        super().__init__(ticker)
        self.precio = precio
        self.cantidad = cantidad

    def valorar(self, **kwargs) -> float:
        return self.precio * self.cantidad


class Bono(Instrumento):
    def __init__(self, ticker: str, valor_nominal: float, cupon: float,
                 vencimiento: int, tasa_descuento: float):
        super().__init__(ticker)
        self.valor_nominal = valor_nominal
        self.cupon = cupon
        self.vencimiento = vencimiento
        self.tasa_descuento = tasa_descuento

    def valorar(self, **kwargs) -> float:
        # VP de cupones + VP del nominal
        flujos = [self.valor_nominal * self.cupon] * self.vencimiento
        flujos[-1] += self.valor_nominal
        vp = sum(f / (1 + self.tasa_descuento) ** (t + 1) for t, f in enumerate(flujos))
        return vp


class Opcion(Instrumento):
    def __init__(self, ticker: str, tipo: str, strike: float, spot: float,
                 plazo: float, tasa: float, volatilidad: float, cantidad: int = 1):
        super().__init__(ticker)
        self.tipo = tipo
        self.strike = strike
        self.spot = spot
        self.plazo = plazo
        self.tasa = tasa
        self.volatilidad = volatilidad
        self.cantidad = cantidad

    def valorar(self, **kwargs) -> float:
        # Black-Scholes simplificado (para CALL)
        from math import exp, log, sqrt
        from statistics import NormalDist
        d1 = (log(self.spot / self.strike) + (self.tasa + self.volatilidad**2/2) * self.plazo) / (self.volatilidad * sqrt(self.plazo))
        d2 = d1 - self.volatilidad * sqrt(self.plazo)
        N = NormalDist().cdf
        precio = self.spot * N(d1) - self.strike * exp(-self.tasa * self.plazo) * N(d2)
        return precio * self.cantidad * 100


# Polimorfismo en acción
instrumentos = [
    Accion("AAPL", 175.0, 100),
    Bono("UST10Y", 1000, 0.05, 10, 0.04),
    Opcion("AAPL180C", "CALL", 180, 175, 0.5, 0.05, 0.25, 5),
]

for inst in instrumentos:
    print(f"{inst.ticker}: ${inst.valorar():,.2f}")
```

**Output:**

```
AAPL: $17,500.00
UST10Y: $1,081.11
AAPL180C: $575.30
```

---

## 3. Aplicación en Finanzas 💰

En un banco, el **middle office** valida el riesgo de miles de instrumentos distintos. Gracias al polimorfismo, un solo loop puede calcular VaR para todos:

```python
for instrumento in libro_trading:
    pnl_escenarios.append(instrumento.valorar(escenario=esc))
```

Sin POO, esto requeriría `if isinstance(inst, Accion): ... elif isinstance(inst, Bono): ...` — inmantenible con 50 tipos de derivados.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-4/U16_ejercicios.py`

1. **Jerarquía `Instrumento` → `Accion`, `Bono`, `Opcion`:** Crear la clase abstracta `Instrumento` con `@abstractmethod valorar()` y 3 subclases concretas.
2. **`Portafolio` polimórfico:** Portafolio que acepte cualquier `Instrumento` y calcule valor_total y composicion_por_tipo.
3. **Mixin `Auditable`:** Crear mixin que registre cada llamada a `valorar()` con timestamp e implementarlo en `Accion` y `Bono`.
4. **Sistema de pricing con composición:** Un `MotorPrecios` que reciba `Instrumento` y aplique un `ModeloPrecio` (composición: el motor tiene un modelo).

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Herencia | `class Accion(Instrumento):` |
| `super()` | `super().__init__(ticker, nombre)` |
| ABC + abstractmethod | `@abstractmethod` sobre `def valorar(self):` |
| Polimorfismo | `for inst in lista: inst.valorar()` |
| Composición | `self.instrumentos = []` |
| Mixin | `class AccionConLog(Accion, LoggingMixin):` |

---

## ✅ Autoevaluación

1. ¿Qué ventaja tiene usar `ABC` y `@abstractmethod` en lugar de una clase base normal?
2. ¿En qué situaciones conviene composición sobre herencia?
3. ¿Cómo permite el polimorfismo simplificar un sistema de pricing?
4. ¿Qué pasa si una subclase no implementa un método abstracto?
5. ¿Para qué sirve `super()` en el constructor de una subclase?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Herencia modela jerarquías "es un": Accion es un Instrumento
> - `ABC` + `@abstractmethod` fuerzan un contrato que todas las subclases deben cumplir
> - Polimorfismo = mismo método, distinto comportamiento según la clase concreta
> - Composición ("tiene un") es más flexible que herencia para relaciones no jerárquicas
