# U18: Patrones de Diseño en Finanzas Cuantitativas

> **Lectura previa:** [U17: Métodos Especiales y Data Classes](../fase-4/U17-dunders-dataclasses.md)
> **Próxima unidad:** [U19: NumPy](../fase-5/U19-numpy.md)

---

## 1. Teoría

### 1.1 Strategy Pattern: motor de pricing intercambiable

En un banco, el mismo derivado puede valorarse con Black-Scholes, árbol binomial o Monte Carlo. El **Strategy Pattern** permite cambiar el algoritmo de pricing en tiempo de ejecución sin modificar el instrumento.

```python
from abc import ABC, abstractmethod
from math import exp, log, sqrt

class EstrategiaPricing(ABC):
    """Interfaz común para todas las estrategias de pricing."""

    @abstractmethod
    def calcular(self, spot: float, strike: float, plazo: float,
                 tasa: float, volatilidad: float, tipo: str = "CALL") -> float:
        pass


class BlackScholes(EstrategiaPricing):
    """Pricing de opciones europeas con el modelo Black-Scholes-Merton."""

    def calcular(self, spot: float, strike: float, plazo: float,
                 tasa: float, volatilidad: float, tipo: str = "CALL") -> float:
        from statistics import NormalDist
        N = NormalDist().cdf
        d1 = (log(spot / strike) + (tasa + volatilidad**2 / 2) * plazo) / (volatilidad * sqrt(plazo))
        d2 = d1 - volatilidad * sqrt(plazo)
        if tipo == "CALL":
            return spot * N(d1) - strike * exp(-tasa * plazo) * N(d2)
        else:
            return strike * exp(-tasa * plazo) * N(-d2) - spot * N(-d1)


class Binomial(EstrategiaPricing):
    """Árbol binomial de Cox-Ross-Rubinstein."""

    def calcular(self, spot: float, strike: float, plazo: float,
                 tasa: float, volatilidad: float, tipo: str = "CALL",
                 pasos: int = 100) -> float:
        dt = plazo / pasos
        u = exp(volatilidad * sqrt(dt))
        d = 1 / u
        p = (exp(tasa * dt) - d) / (u - d)
        descuento = exp(-tasa * dt)

        precios = [spot * u**j * d**(pasos - j) for j in range(pasos + 1)]
        if tipo == "CALL":
            valores = [max(0, s - strike) for s in precios]
        else:
            valores = [max(0, strike - s) for s in precios]

        for i in range(pasos - 1, -1, -1):
            valores = [descuento * (p * valores[j + 1] + (1 - p) * valores[j])
                       for j in range(i + 1)]
        return valores[0]


class MonteCarlo(EstrategiaPricing):
    """Simulación Monte Carlo para opciones europeas."""

    def calcular(self, spot: float, strike: float, plazo: float,
                 tasa: float, volatilidad: float, tipo: str = "CALL",
                 simulaciones: int = 100_000) -> float:
        import numpy as np
        np.random.seed(42)
        Z = np.random.standard_normal(simulaciones)
        ST = spot * np.exp((tasa - volatilidad**2 / 2) * plazo + volatilidad * sqrt(plazo) * Z)
        if tipo == "CALL":
            payoff = np.maximum(ST - strike, 0)
        else:
            payoff = np.maximum(strike - ST, 0)
        return exp(-tasa * plazo) * payoff.mean()


class MotorPrecios:
    """Contexto que usa una estrategia de pricing."""

    def __init__(self, estrategia: EstrategiaPricing):
        self.estrategia = estrategia

    def cambiar_estrategia(self, nueva: EstrategiaPricing):
        self.estrategia = nueva

    def valorar(self, spot, strike, plazo, tasa, vol, tipo="CALL") -> float:
        return self.estrategia.calcular(spot, strike, plazo, tasa, vol, tipo)


motor = MotorPrecios(BlackScholes())
print(f"BSM Call: ${motor.valorar(100, 105, 0.5, 0.05, 0.20):.4f}")

motor.cambiar_estrategia(Binomial())
print(f"Binomial Call: ${motor.valorar(100, 105, 0.5, 0.05, 0.20):.4f}")

motor.cambiar_estrategia(MonteCarlo())
print(f"Monte Carlo Call: ${motor.valorar(100, 105, 0.5, 0.05, 0.20):.4f}")
```

> 💡 **Tip:** En un entorno de producción, el Strategy Pattern permite hacer A/B testing de modelos de pricing: ejecutas ambos en paralelo y comparas P&L.

### 1.2 Factory Pattern: creando instrumentos desde archivos

El **Factory Pattern** centraliza la creación de objetos. En finanzas, los datos vienen de CSV, JSON o APIs, y cada formato requiere una lógica de parsing distinta.

```python
from abc import ABC, abstractmethod
import json
import csv
from io import StringIO

class Instrumento:
    def __init__(self, ticker: str, tipo: str, **kwargs):
        self.ticker = ticker
        self.tipo = tipo
        self.atributos = kwargs

    def __repr__(self):
        return f"Instrumento({self.ticker}, {self.tipo}, {self.atributos})"


class FabricaInstrumento(ABC):
    @abstractmethod
    def desde_dict(self, datos: dict) -> Instrumento:
        pass

    def desde_json(self, ruta: str) -> list[Instrumento]:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return [self.desde_dict(d) for d in datos]

    def desde_csv(self, ruta: str) -> list[Instrumento]:
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [self.desde_dict(fila) for fila in reader]


class FabricaAccion(FabricaInstrumento):
    def desde_dict(self, datos: dict) -> Instrumento:
        return Instrumento(
            ticker=datos["ticker"],
            tipo="Accion",
            precio=float(datos["precio"]),
            cantidad=int(datos["cantidad"]),
            sector=datos.get("sector", "N/A"),
        )


class FabricaBono(FabricaInstrumento):
    def desde_dict(self, datos: dict) -> Instrumento:
        return Instrumento(
            ticker=datos["ticker"],
            tipo="Bono",
            valor_nominal=float(datos["valor_nominal"]),
            cupon=float(datos["cupon"]),
            vencimiento=int(datos["vencimiento"]),
        )


def crear_fabrica(tipo: str) -> FabricaInstrumento:
    """Factory de factories: selecciona la fábrica según el tipo."""
    fabricas = {
        "accion": FabricaAccion,
        "bono": FabricaBono,
    }
    clase = fabricas.get(tipo)
    if clase is None:
        raise ValueError(f"Tipo de instrumento no soportado: {tipo}")
    return clase()


# Uso
fabrica = crear_fabrica("accion")
inst = fabrica.desde_dict({"ticker": "AAPL", "precio": "175", "cantidad": "100"})
print(inst)  # Instrumento(AAPL, Accion, {'precio': 175.0, 'cantidad': 100, 'sector': 'N/A'})
```

> ⚠️ **Separación de responsabilidades:** La fábrica solo crea objetos. No hace cálculos, no valida reglas de negocio. Eso es responsabilidad de los objetos creados.

### 1.3 Observer Pattern: reaccionando a eventos de mercado

El **Observer Pattern** es fundamental en trading algorítmico: cuando el precio cambia, múltiples componentes (risk engine, signal generator, order manager) deben reaccionar.

```python
from abc import ABC, abstractmethod

class Observador(ABC):
    @abstractmethod
    def actualizar(self, ticker: str, precio: float):
        pass


class Sujeto:
    """El market data feed — notifica a sus observadores."""

    def __init__(self):
        self._observadores: list[Observador] = []
        self._precios: dict[str, float] = {}

    def registrar(self, observador: Observador):
        self._observadores.append(observador)

    def eliminar(self, observador: Observador):
        self._observadores.remove(observador)

    def notificar(self, ticker: str, precio: float):
        for obs in self._observadores:
            obs.actualizar(ticker, precio)

    def actualizar_precio(self, ticker: str, precio: float):
        self._precios[ticker] = precio
        self.notificar(ticker, precio)


class AlertaPrecio(Observador):
    """Dispara alertas cuando un precio cruza un umbral."""

    def __init__(self, ticker: str, umbral_superior: float, umbral_inferior: float):
        self.ticker = ticker
        self.umbral_superior = umbral_superior
        self.umbral_inferior = umbral_inferior

    def actualizar(self, ticker: str, precio: float):
        if ticker != self.ticker:
            return
        if precio >= self.umbral_superior:
            print(f"🚨 {ticker} superó ${self.umbral_superior:.2f} → VENDER señal")
        elif precio <= self.umbral_inferior:
            print(f"🚨 {ticker} cayó bajo ${self.umbral_inferior:.2f} → COMPRAR señal")


class RegistroPrecios(Observador):
    """Guarda historial de precios para backtesting."""

    def __init__(self):
        self.historial: dict[str, list[float]] = {}

    def actualizar(self, ticker: str, precio: float):
        if ticker not in self.historial:
            self.historial[ticker] = []
        self.historial[ticker].append(precio)
        print(f"📊 {ticker}: precio registrado ${precio:.2f}")


class CalculadorPnL(Observador):
    """Calcula P&L en tiempo real para una posición."""

    def __init__(self, ticker: str, precio_compra: float, cantidad: int):
        self.ticker = ticker
        self.precio_compra = precio_compra
        self.cantidad = cantidad

    def actualizar(self, ticker: str, precio: float):
        if ticker != self.ticker:
            return
        pnl = (precio - self.precio_compra) * self.cantidad
        signo = "+" if pnl >= 0 else ""
        print(f"💰 P&L {ticker}: {signo}${pnl:,.2f}")


# Simular market data
feed = Sujeto()
feed.registrar(AlertaPrecio("AAPL", 180.0, 160.0))
feed.registrar(RegistroPrecios())
feed.registrar(CalculadorPnL("AAPL", 170.0, 100))

# Flujo de precios
for precio in [172, 175, 178, 181, 176, 159]:
    print(f"\n--- Nuevo precio AAPL: ${precio:.2f} ---")
    feed.actualizar_precio("AAPL", precio)
```

### 1.4 Singleton: una sola conexión a la base de datos

En sistemas financieros, ciertos recursos (conexión a DB, logger, configuración global) deben existir una sola vez.

```python
class ConfiguracionGlobal:
    """Singleton: configuración única para todo el sistema."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.parametros = {
            "tasa_libre_riesgo": 0.05,
            "horizonte_var": 10,
            "confianza_var": 0.99,
            "comision_fija": 1.00,
            "comision_variable": 0.001,
        }

    def obtener(self, clave: str, default=None):
        return self.parametros.get(clave, default)

    def establecer(self, clave: str, valor):
        self.parametros[clave] = valor


cfg1 = ConfiguracionGlobal()
cfg2 = ConfiguracionGlobal()
print(cfg1 is cfg2)                               # True — misma instancia
print(cfg1.obtener("tasa_libre_riesgo"))           # 0.05
cfg2.establecer("tasa_libre_riesgo", 0.045)
print(cfg1.obtener("tasa_libre_riesgo"))           # 0.045 — compartido
```

> ⚠️ **Singletons son controvertidos:** Dificultan el testing (estado global oculto). Úsalos solo cuando realmente necesites UNA instancia (conexiones costosas, logs).

### 1.5 Generadores (`yield`): streaming de datos de mercado

Los generadores producen valores bajo demanda sin cargar todo en memoria. Ideales para procesar streams de ticks en tiempo real.

```python
def generar_precios_gbm(spot: float, mu: float, sigma: float,
                        dias: int, dt: float = 1/252):
    """Generador de trayectoria de precios con Movimiento Browniano Geométrico."""
    import numpy as np
    np.random.seed(42)
    precio = spot
    yield precio
    for _ in range(dias - 1):
        shock = np.random.normal(0, 1)
        precio *= np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shock)
        yield precio


def detectar_cruces_medias(precios, ventana_corta=5, ventana_larga=20):
    """Generador que emite señales cuando las medias se cruzan."""
    from collections import deque

    historial = []
    for precio in precios:
        historial.append(precio)
        if len(historial) < ventana_larga:
            yield None
            continue

        sma_corta = sum(historial[-ventana_corta:]) / ventana_corta
        sma_larga = sum(historial[-ventana_larga:]) / ventana_larga
        sma_corta_ant = sum(historial[-ventana_corta-1:-1]) / ventana_corta
        sma_larga_ant = sum(historial[-ventana_larga-1:-1]) / ventana_larga

        if sma_corta_ant <= sma_larga_ant and sma_corta > sma_larga:
            yield "GOLDEN CROSS (COMPRA)"
        elif sma_corta_ant >= sma_larga_ant and sma_corta < sma_larga:
            yield "DEATH CROSS (VENTA)"
        else:
            yield None


# Stream de precios con señales
precios_stream = generar_precios_gbm(100, 0.08, 0.20, 40)
senales = detectar_cruces_medias(precios_stream)

for dia, senal in enumerate(senales, 1):
    if senal:
        print(f"Día {dia}: {senal}")
```

> 💡 **Tip:** Los generadores son la base de `asyncio` y procesamiento de streams en Python. En un sistema de trading real, serían `async def` que yield-ean ticks del exchange.

---

## 2. Práctica

### 2.1 Ejercicio guiado: Pricing Engine con Strategy Pattern

**Concepto financiero:** Un desk de derivados necesita valorar opciones con el modelo que mejor se ajuste al mercado (BSM para opciones líquidas, Monte Carlo para exóticas).

**Código:**

```python
from abc import ABC, abstractmethod

class EstrategiaPrecio(ABC):
    @abstractmethod
    def precio(self, spot, strike, plazo, tasa, vol, tipo="CALL") -> float:
        pass


class BSM(EstrategiaPrecio):
    def precio(self, spot, strike, plazo, tasa, vol, tipo="CALL") -> float:
        from math import exp, log, sqrt
        from statistics import NormalDist
        N = NormalDist().cdf
        d1 = (log(spot / strike) + (tasa + vol**2/2) * plazo) / (vol * sqrt(plazo))
        d2 = d1 - vol * sqrt(plazo)
        if tipo == "CALL":
            return spot * N(d1) - strike * exp(-tasa * plazo) * N(d2)
        else:
            return strike * exp(-tasa * plazo) * N(-d2) - spot * N(-d1)


class Pricer:
    def __init__(self, estrategia: EstrategiaPrecio):
        self.estrategia = estrategia

    def valorar(self, **params) -> float:
        return self.estrategia.precio(**params)


pricer = Pricer(BSM())
print(f"Call ATM: ${pricer.valorar(spot=100, strike=100, plazo=1, tasa=0.05, vol=0.20):.4f}")
print(f"Put OTM: ${pricer.valorar(spot=100, strike=90, plazo=1, tasa=0.05, vol=0.20, tipo='PUT'):.4f}")
```

**Output:**

```
Call ATM: $10.4506
Put OTM: $4.4803
```

---

## 3. Aplicación en Finanzas 💰

En **Citadel Securities**, el Strategy Pattern se usa para market making: el mismo `OrderRouter` puede ejecutar con estrategia `agresiva` (cruzar spread) o `pasiva` (postear en el book) según condiciones de mercado.

En **JP Morgan**, el Factory Pattern crea instrumentos desde feeds de Bloomberg, Reuters, y datos internos, cada uno con su parser. El Observer Pattern monitorea límites de riesgo en tiempo real en todos los desks.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-4/U18_ejercicios.py`

1. **Pricing Engine con Strategy:** Implementar `EstrategiaPrecio` abstracta, `BSM`, `Binomial`, `MonteCarlo`. Motor que tome cualquier estrategia y valores opciones.
2. **Factory de Instrumentos desde JSON:** Crear `FabricaInstrumento` abstracta, `FabricaAccion`, `FabricaBono`, `FabricaOpcion`. Parsear un JSON simulado con instrumentos mixtos y crear la lista.
3. **Observer para Stop Loss y Take Profit:** `MarketDataFeed` (Sujeto), `StopLoss` (Observador), `TakeProfit` (Observador). Simular ticks de precio y verificar disparo de órdenes.
4. **Generador de señales RSI:** Crear generador que reciba stream de precios y emita señales de sobrecompra (RSI>70) y sobreventa (RSI<30).

---

## 5. Resumen

| Patrón | Propósito | Uso financiero |
|--------|-----------|----------------|
| Strategy | Intercambiar algoritmos | Pricing de opciones (BSM/binomial/MC) |
| Factory | Crear objetos desde distintas fuentes | Cargar instrumentos desde JSON/CSV/API |
| Observer | Notificar cambios a múltiples componentes | Alertas, risk limits, P&L en tiempo real |
| Singleton | Garantizar una sola instancia | Configuración global, conexión a DB |
| Generator | Producir secuencias bajo demanda | Streams de precios, señales de trading |

---

## ✅ Autoevaluación

1. ¿Qué problema resuelve el Strategy Pattern en un sistema de pricing?
2. ¿Cuál es la diferencia entre Factory Pattern y un simple constructor?
3. ¿Cómo implementarías un Observer para que un risk engine detenga el trading si el VaR excede un límite?
4. ¿Por qué los Singletons son controvertidos en testing?
5. ¿Qué ventaja tiene un generador sobre una lista para procesar ticks de mercado?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Strategy = motor de pricing con modelos intercambiables (BSM ↔ Binomial ↔ MC)
> - Factory = crear instrumentos desde múltiples formatos (CSV, JSON, API)
> - Observer = market data feed notifica a alertas, risk, P&L (arquitectura event-driven)
> - Generadores (`yield`) = procesar streams de datos financieros sin cargar todo en memoria
