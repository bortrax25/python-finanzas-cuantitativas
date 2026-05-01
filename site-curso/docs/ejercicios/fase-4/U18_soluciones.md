# ✅ Soluciones: U18 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U18_soluciones)

---

```python
# U18: SOLUCIONES — Patrones de Diseño en Finanzas Cuantitativas

# ============================================================
# Ejercicio 1: Pricing Engine con Strategy Pattern
# ============================================================
print("=== Ejercicio 1: Pricing Engine con Strategy ===")

from abc import ABC, abstractmethod
from math import exp, log, sqrt


class EstrategiaPrecio(ABC):
    @abstractmethod
    def precio(self, spot: float, strike: float, plazo: float,
               tasa: float, vol: float, tipo: str = "CALL") -> float:
        pass


class BSM(EstrategiaPrecio):
    def precio(self, spot: float, strike: float, plazo: float,
               tasa: float, vol: float, tipo: str = "CALL") -> float:
        from statistics import NormalDist
        N = NormalDist().cdf
        d1 = (log(spot / strike) + (tasa + vol**2 / 2) * plazo) / (vol * sqrt(plazo))
        d2 = d1 - vol * sqrt(plazo)
        if tipo == "CALL":
            return spot * N(d1) - strike * exp(-tasa * plazo) * N(d2)
        else:
            return strike * exp(-tasa * plazo) * N(-d2) - spot * N(-d1)


class Binomial(EstrategiaPrecio):
    def precio(self, spot: float, strike: float, plazo: float,
               tasa: float, vol: float, tipo: str = "CALL", pasos: int = 50) -> float:
        dt = plazo / pasos
        u = exp(vol * sqrt(dt))
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


class MotorPrecios:
    def __init__(self, estrategia: EstrategiaPrecio):
        self.estrategia = estrategia

    def cambiar_estrategia(self, nueva: EstrategiaPrecio):
        self.estrategia = nueva

    def valorar(self, spot, strike, plazo, tasa, vol, tipo="CALL", **kwargs) -> float:
        return self.estrategia.precio(spot, strike, plazo, tasa, vol, tipo, **kwargs)


motor = MotorPrecios(BSM())
precio_bsm = motor.valorar(100, 100, 0.5, 0.05, 0.25)
print(f"BSM      CALL ATM (S=100, K=100, T=0.5): ${precio_bsm:.4f}")

motor.cambiar_estrategia(Binomial())
precio_binom = motor.valorar(100, 100, 0.5, 0.05, 0.25)
print(f"Binomial CALL ATM (S=100, K=100, T=0.5): ${precio_binom:.4f}")
print(f"Diferencia absoluta: ${abs(precio_bsm - precio_binom):.4f}")

# ============================================================
# Ejercicio 2: Factory de Instrumentos desde JSON simulado
# ============================================================
print("\\n=== Ejercicio 2: Factory de Instrumentos ===")

import json


class Instrumento:
    def __init__(self, ticker: str, tipo: str, atributos: dict):
        self.ticker = ticker
        self.tipo = tipo
        self.atributos = atributos

    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.atributos.items())
        return f"Instrumento({self.ticker}, {self.tipo}, {attrs})"


class FabricaInstrumento(ABC):
    @abstractmethod
    def desde_dict(self, datos: dict) -> Instrumento:
        pass

    def desde_json(self, texto_json: str) -> list:
        datos = json.loads(texto_json)
        return [self.desde_dict(d) for d in datos]


class FabricaAccion(FabricaInstrumento):
    def desde_dict(self, datos: dict) -> Instrumento:
        return Instrumento(
            ticker=datos["ticker"],
            tipo="Accion",
            atributos={
                "precio": float(datos["precio"]),
                "cantidad": int(datos["cantidad"]),
                "sector": datos.get("sector", "N/A"),
            },
        )


class FabricaBono(FabricaInstrumento):
    def desde_dict(self, datos: dict) -> Instrumento:
        return Instrumento(
            ticker=datos["ticker"],
            tipo="Bono",
            atributos={
                "valor_nominal": float(datos["valor_nominal"]),
                "cupon": float(datos["cupon"]),
                "vencimiento": int(datos["vencimiento"]),
            },
        )


def crear_fabrica(tipo: str) -> FabricaInstrumento:
    fabricas = {"accion": FabricaAccion, "bono": FabricaBono}
    if tipo not in fabricas:
        raise ValueError(f"Tipo no soportado: {tipo}")
    return fabricas[tipo]()


# JSON simulado con instrumentos mixtos
json_datos = json.dumps([
    {"ticker": "AAPL", "precio": "175", "cantidad": "100", "sector": "Tecnologia"},
    {"ticker": "JPM", "precio": "140", "cantidad": "200", "sector": "Finanzas"},
    {"ticker": "UST10Y", "valor_nominal": "1000", "cupon": "0.05", "vencimiento": "10"},
    {"ticker": "CORP5Y", "valor_nominal": "5000", "cupon": "0.07", "vencimiento": "5"},
])

# Clasificar por tipo
acciones_json = json.loads(json_datos)
instrumentos = []
for item in acciones_json:
    if "precio" in item:
        fab = crear_fabrica("accion")
    else:
        fab = crear_fabrica("bono")
    instrumentos.append(fab.desde_dict(item))

for inst in instrumentos:
    print(inst)
print(f"Total instrumentos creados: {len(instrumentos)}")

# ============================================================
# Ejercicio 3: Observer Pattern — Stop Loss y Take Profit
# ============================================================
print("\\n=== Ejercicio 3: Observer para Stop Loss / Take Profit ===")


class Observador(ABC):
    @abstractmethod
    def actualizar(self, ticker: str, precio: float):
        pass


class MarketDataFeed:
    def __init__(self):
        self._observadores: list[Observador] = []

    def registrar(self, observador: Observador):
        self._observadores.append(observador)

    def eliminar(self, observador: Observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self, ticker: str, precio: float):
        for obs in self._observadores[:]:
            obs.actualizar(ticker, precio)

    def actualizar_precio(self, ticker: str, precio: float):
        print(f"Precio {ticker}: ${precio:.2f}")
        self.notificar(ticker, precio)


class StopLoss(Observador):
    def __init__(self, ticker: str, precio_stop: float, feed: MarketDataFeed):
        self.ticker = ticker
        self.precio_stop = precio_stop
        self.feed = feed

    def actualizar(self, ticker: str, precio: float):
        if ticker != self.ticker:
            return
        if precio <= self.precio_stop:
            print(f"🛑 STOP LOSS {ticker}: Precio ${precio:.2f} <= Stop ${self.precio_stop:.2f} → VENDER")
            self.feed.eliminar(self)


class TakeProfit(Observador):
    def __init__(self, ticker: str, precio_target: float, feed: MarketDataFeed):
        self.ticker = ticker
        self.precio_target = precio_target
        self.feed = feed

    def actualizar(self, ticker: str, precio: float):
        if ticker != self.ticker:
            return
        if precio >= self.precio_target:
            print(f"✅ TAKE PROFIT {ticker}: Precio ${precio:.2f} >= Target ${self.precio_target:.2f} → VENDER")
            self.feed.eliminar(self)


class RegistroPrecios(Observador):
    def __init__(self):
        self.historial = []

    def actualizar(self, ticker: str, precio: float):
        self.historial.append(precio)


feed = MarketDataFeed()
registro = RegistroPrecios()
feed.registrar(registro)
feed.registrar(StopLoss("AAPL", 157.0, feed))
feed.registrar(TakeProfit("AAPL", 170.0, feed))

precios = [150, 155, 162, 158, 168, 165, 172]
for p in precios:
    feed.actualizar_precio("AAPL", p)

print(f"Historial de precios registrados: {registro.historial}")

# ============================================================
# Ejercicio 4: Generador de señales RSI
# ============================================================
print("\\n=== Ejercicio 4: Generador de señales RSI ===")

import random
random.seed(42)


def generar_rsi(precios: list, periodo: int = 14):
    ganancias = []
    perdidas = []
    for i in range(1, len(precios)):
        cambio = precios[i] - precios[i - 1]
        ganancias.append(max(cambio, 0))
        perdidas.append(max(-cambio, 0))

    for dia in range(periodo, len(precios)):
        ganancia_prom = sum(ganancias[dia - periodo:dia]) / periodo
        perdida_prom = sum(perdidas[dia - periodo:dia]) / periodo
        if perdida_prom == 0:
            rsi = 100.0
        else:
            rs = ganancia_prom / perdida_prom
            rsi = 100.0 - (100.0 / (1 + rs))

        if rsi > 70:
            yield (dia + 1, precios[dia], rsi, "SOBRECOMPRA (vender)")
        elif rsi < 30:
            yield (dia + 1, precios[dia], rsi, "SOBREVENTA (comprar)")
        else:
            yield None


# Generar serie de 30 precios sintéticos con tendencia + ruido
precios_base = [100.0]
for i in range(29):
    tendencia = 0.5 * (i % 10)  # tendencia variable
    ruido = random.gauss(0, 2)
    precios_base.append(precios_base[-1] + tendencia + ruido)

print(f"Serie de {len(precios_base)} precios generada")
print("Señales detectadas:")
senales = list(generar_rsi(precios_base))
for senal in senales:
    if senal is not None:
        dia, precio, rsi, mensaje = senal
        print(f"Día {dia}: Precio={precio:.2f} | RSI={rsi:.1f} → {mensaje}")
```

---

> [📥 Descargar archivo .py](U18_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
