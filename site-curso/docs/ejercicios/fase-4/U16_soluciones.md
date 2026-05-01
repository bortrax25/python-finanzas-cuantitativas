# ✅ Soluciones: U16 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U16_soluciones)

---

```python
# U16: SOLUCIONES — Herencia y Polimorfismo

# ============================================================
# Ejercicio 1: Jerarquía de instrumentos financieros
# ============================================================
print("=== Ejercicio 1: Jerarquía de instrumentos ===")

from abc import ABC, abstractmethod


class Instrumento(ABC):
    def __init__(self, ticker: str, nombre: str):
        self.ticker = ticker
        self.nombre = nombre

    @abstractmethod
    def valorar(self) -> float:
        pass

    @abstractmethod
    def tipo_instrumento(self) -> str:
        pass

    def resumen(self) -> str:
        return f"{self.ticker} | {self.tipo_instrumento()} | Valor: ${self.valorar():,.2f}"


class Accion(Instrumento):
    def __init__(self, ticker: str, nombre: str, precio: float, cantidad: int):
        super().__init__(ticker, nombre)
        self.precio = precio
        self.cantidad = cantidad

    def tipo_instrumento(self) -> str:
        return "Renta Variable"

    def valorar(self) -> float:
        return self.precio * self.cantidad


class Bono(Instrumento):
    def __init__(self, ticker: str, nombre: str, valor_nominal: float,
                 cupon: float, vencimiento: int, tasa_descuento: float):
        super().__init__(ticker, nombre)
        self.valor_nominal = valor_nominal
        self.cupon = cupon
        self.vencimiento = vencimiento
        self.tasa_descuento = tasa_descuento

    def tipo_instrumento(self) -> str:
        return "Renta Fija"

    def valorar(self) -> float:
        flujos = [self.valor_nominal * self.cupon] * self.vencimiento
        flujos[-1] += self.valor_nominal
        return sum(f / (1 + self.tasa_descuento) ** (t + 1) for t, f in enumerate(flujos))


class Opcion(Instrumento):
    def __init__(self, ticker: str, nombre: str, tipo: str, strike: float,
                 spot: float, plazo: float, tasa: float, volatilidad: float):
        super().__init__(ticker, nombre)
        self.tipo = tipo
        self.strike = strike
        self.spot = spot
        self.plazo = plazo
        self.tasa = tasa
        self.volatilidad = volatilidad

    def tipo_instrumento(self) -> str:
        return "Derivado"

    def valorar(self) -> float:
        if self.tipo == "CALL":
            return max(0, self.spot - self.strike) * 100
        else:
            return max(0, self.strike - self.spot) * 100


accion = Accion("AAPL", "Apple Inc.", 175.0, 100)
bono = Bono("UST10Y", "US Treasury 10Y", 1000, 0.05, 10, 0.04)
opcion = Opcion("AAPL200C", "Apple Call 200", "CALL", 200, 175, 0.5, 0.05, 0.25)

print(accion.resumen())
print(bono.resumen())
print(opcion.resumen())

# ============================================================
# Ejercicio 2: Portafolio polimórfico
# ============================================================
print("\\n=== Ejercicio 2: Portafolio polimórfico ===")


class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.instrumentos: list[Instrumento] = []

    def agregar(self, instrumento: Instrumento):
        self.instrumentos.append(instrumento)

    def valor_total(self) -> float:
        return sum(inst.valorar() for inst in self.instrumentos)

    def composicion_por_tipo(self) -> dict:
        composicion = {}
        for inst in self.instrumentos:
            tipo = inst.__class__.__name__
            composicion[tipo] = composicion.get(tipo, 0) + inst.valorar()
        return composicion

    def instrumento_mayor_valor(self) -> Instrumento:
        if not self.instrumentos:
            return None
        return max(self.instrumentos, key=lambda i: i.valorar())

    def __str__(self):
        lineas = [f"Portafolio: {self.nombre}"]
        lineas.append(f"{'Ticker':<12} {'Tipo':<18} {'Valor':>12}")
        lineas.append("-" * 42)
        for inst in self.instrumentos:
            lineas.append(f"{inst.ticker:<12} {inst.tipo_instrumento():<18} ${inst.valorar():>11,.2f}")
        lineas.append("-" * 42)
        lineas.append(f"Valor Total: ${self.valor_total():,.2f}")
        mayor = self.instrumento_mayor_valor()
        lineas.append(f"Mayor posición: {mayor.ticker} (${mayor.valorar():,.2f})")
        comp = self.composicion_por_tipo()
        lineas.append(f"Composición: {comp}")
        return "\\n".join(lineas)


pf = Portafolio("Multi-Asset")
pf.agregar(Accion("AAPL", "Apple Inc.", 175.0, 100))
pf.agregar(Accion("MSFT", "Microsoft Corp.", 310.0, 50))
pf.agregar(Bono("UST10Y", "US Treasury 10Y", 1000, 0.05, 10, 0.04))
pf.agregar(Bono("CORP5Y", "Corporate 5Y", 1000, 0.06, 5, 0.05))
pf.agregar(Opcion("AAPL200C", "Apple Call 200", "CALL", 200, 175, 0.5, 0.05, 0.25))
print(pf)

# ============================================================
# Ejercicio 3: Mixin Auditable
# ============================================================
print("\\n=== Ejercicio 3: Mixin Auditable ===")

from datetime import datetime


class AuditableMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.historial = []

    def auditar(self, evento: str, valor):
        entrada = {
            "tipo": self.tipo_instrumento(),
            "ticker": self.ticker,
            "evento": evento,
            "valor": valor,
            "timestamp": datetime.now().isoformat(),
        }
        self.historial.append(entrada)
        print(f"[{entrada['timestamp']}] {entrada['tipo']} {entrada['ticker']} | {evento} | {valor}")

    def reporte_auditoria(self):
        print(f"Total eventos auditados: {len(self.historial)}")


class AccionAuditable(AuditableMixin, Accion):
    def valorar(self) -> float:
        resultado = super().valorar()
        self.auditar("valoracion", f"${resultado:,.2f}")
        return resultado

    def actualizar_precio(self, nuevo_precio: float):
        self.auditar("actualizacion", f"nuevo_precio={nuevo_precio}")
        self.precio = nuevo_precio


class BonoAuditable(AuditableMixin, Bono):
    def valorar(self) -> float:
        resultado = super().valorar()
        self.auditar("valoracion", f"${resultado:,.2f}")
        return resultado


aapl = AccionAuditable("AAPL", "Apple Inc.", 175.0, 100)
bono = BonoAuditable("UST10Y", "US Treasury 10Y", 1000, 0.05, 10, 0.04)

aapl.valorar()
bono.valorar()
aapl.actualizar_precio(180.0)
aapl.reporte_auditoria()

# ============================================================
# Ejercicio 4: Sistema de pricing por composición
# ============================================================
print("\\n=== Ejercicio 4: Sistema de pricing por composición ===")


class ModeloPrecio:
    def calcular(self, instrumento: Instrumento) -> float:
        raise NotImplementedError


class ModeloLineal(ModeloPrecio):
    def calcular(self, instrumento: Instrumento) -> float:
        return instrumento.precio * instrumento.cantidad


class ModeloFlujoDescontado(ModeloPrecio):
    def calcular(self, instrumento: Instrumento) -> float:
        flujos = [instrumento.valor_nominal * instrumento.cupon] * instrumento.vencimiento
        flujos[-1] += instrumento.valor_nominal
        return sum(f / (1 + instrumento.tasa_descuento) ** (t + 1) for t, f in enumerate(flujos))


class MotorPrecios:
    def __init__(self, modelo: ModeloPrecio):
        self.modelo = modelo

    def valorar(self, instrumento: Instrumento) -> float:
        return self.modelo.calcular(instrumento)

    def cambiar_modelo(self, nuevo_modelo: ModeloPrecio):
        self.modelo = nuevo_modelo


accion1 = Accion("AAPL", "Apple Inc.", 175.0, 100)
accion2 = Accion("MSFT", "Microsoft Corp.", 180.0, 50)
bono1 = Bono("UST10Y", "US Treasury 10Y", 1000, 0.05, 10, 0.04)
bono2 = Bono("CORP5Y", "Corporate 5Y", 1000, 0.06, 5, 0.05)

motor = MotorPrecios(ModeloLineal())
print(f"Motor con ModeloLineal → AAPL: ${motor.valorar(accion1):,.2f}")
print(f"Motor con ModeloLineal → MSFT: ${motor.valorar(accion2):,.2f}")

motor.cambiar_modelo(ModeloFlujoDescontado())
print(f"Motor con ModeloFlujoDescontado → UST10Y: ${motor.valorar(bono1):,.2f}")
print(f"Motor con ModeloFlujoDescontado → CORP5Y: ${motor.valorar(bono2):,.2f}")
```

---

> [📥 Descargar archivo .py](U16_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
