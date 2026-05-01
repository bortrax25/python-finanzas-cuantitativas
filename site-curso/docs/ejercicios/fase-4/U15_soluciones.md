# ✅ Soluciones: U15 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U15_soluciones)

---

```python
# U15: SOLUCIONES — Clases y Objetos: Modelando Instrumentos Financieros

# ============================================================
# Ejercicio 1: Clase Accion con P&L
# ============================================================
print("=== Ejercicio 1: Clase Accion ===")


class Accion:
    def __init__(self, ticker: str, precio_compra: float, cantidad: int):
        self.ticker = ticker.upper()
        self.precio_compra = precio_compra
        self.cantidad = cantidad
        self.precio_actual = precio_compra

    def actualizar_precio(self, nuevo_precio: float):
        self.precio_actual = nuevo_precio

    def valor_mercado(self) -> float:
        return self.cantidad * self.precio_actual

    def costo(self) -> float:
        return self.cantidad * self.precio_compra

    def ganancia_perdida(self) -> float:
        return self.valor_mercado() - self.costo()

    def rendimiento(self) -> float:
        if self.costo() == 0:
            return 0.0
        return (self.precio_actual / self.precio_compra - 1) * 100

    def __str__(self):
        return (
            f"{self.ticker}: {self.cantidad} × ${self.precio_actual:.2f} = "
            f"${self.valor_mercado():,.2f} | "
            f"P&L: ${self.ganancia_perdida():,.2f} "
            f"({self.rendimiento():.2f}%)"
        )


aapl = Accion("AAPL", 150.00, 100)
aapl.actualizar_precio(175.00)
print(aapl)

# ============================================================
# Ejercicio 2: Clase Bono con cupones y properties
# ============================================================
print("\\n=== Ejercicio 2: Clase Bono ===")


class Bono:
    def __init__(self, valor_nominal: float, tasa_cupon: float,
                 precio_mercado: float, vencimiento: int, frecuencia: int = 2):
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon
        self.precio_mercado = precio_mercado
        self.vencimiento = vencimiento
        self.frecuencia = frecuencia

    def cupon_por_periodo(self) -> float:
        return self.valor_nominal * self.tasa_cupon / self.frecuencia

    def total_cupones(self) -> float:
        return self.cupon_por_periodo() * self.vencimiento * self.frecuencia

    @property
    def rendimiento_actual(self) -> float:
        cupon_anual = self.valor_nominal * self.tasa_cupon
        return (cupon_anual / self.precio_mercado) * 100

    @property
    def prima_descuento(self) -> str:
        if self.precio_mercado > self.valor_nominal:
            return "Sobre par (prima)"
        elif self.precio_mercado < self.valor_nominal:
            return "Bajo par (descuento)"
        else:
            return "A la par"

    def __repr__(self):
        return (
            f"Bono(VN={self.valor_nominal}, cupon={self.tasa_cupon*100}%, "
            f"venc={self.vencimiento}, precio={self.precio_mercado})"
        )


bono = Bono(1000, 0.06, 950, 10)
print(repr(bono))
print(f"Cupón por periodo: ${bono.cupon_por_periodo():.2f}")
print(f"Total cupones: ${bono.total_cupones():.2f}")
print(f"Rendimiento actual: {bono.rendimiento_actual:.2f}%")
print(f"Clasificación: {bono.prima_descuento}")

# ============================================================
# Ejercicio 3: Clase Portafolio con estadísticas avanzadas
# ============================================================
print("\\n=== Ejercicio 3: Clase Portafolio ===")


class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.activos = {}

    def agregar(self, accion: Accion):
        self.activos[accion.ticker] = accion

    def eliminar(self, ticker: str):
        if ticker in self.activos:
            del self.activos[ticker]

    def valor_total(self) -> float:
        return sum(a.valor_mercado() for a in self.activos.values())

    def costo_total(self) -> float:
        return sum(a.costo() for a in self.activos.values())

    def pnl_total(self) -> float:
        return self.valor_total() - self.costo_total()

    def rendimiento_ponderado(self) -> float:
        if self.costo_total() == 0:
            return 0.0
        return (self.pnl_total() / self.costo_total()) * 100

    def concentracion_maxima(self) -> tuple:
        if not self.activos:
            return ("N/A", 0.0)
        total = self.valor_total()
        max_ticker = max(self.activos, key=lambda t: self.activos[t].valor_mercado())
        peso = (self.activos[max_ticker].valor_mercado() / total) * 100
        return (max_ticker, peso)

    def resumen(self) -> str:
        lineas = [f"Portafolio: {self.nombre}"]
        lineas.append(f"{'Ticker':<8} {'Cant':>6} {'Precio':>10} {'Valor':>12} {'P&L':>10} {'Peso':>8}")
        lineas.append("-" * 64)
        total = self.valor_total()
        for a in self.activos.values():
            peso = (a.valor_mercado() / total) * 100 if total > 0 else 0
            lineas.append(
                f"{a.ticker:<8} {a.cantidad:>6} ${a.precio_actual:>9.2f} "
                f"${a.valor_mercado():>11,.2f} ${a.ganancia_perdida():>9,.2f} {peso:>7.2f}%"
            )
        lineas.append("-" * 64)
        lineas.append(
            f"Valor Total: ${self.valor_total():,.2f} | P&L: ${self.pnl_total():,.2f} | "
            f"Rend: {self.rendimiento_ponderado():.2f}%"
        )
        ticker, peso = self.concentracion_maxima()
        lineas.append(f"Concentración máxima: {ticker} ({peso:.2f}%)")
        return "\\n".join(lineas)


pf = Portafolio("Mi Fondo")
pf.agregar(Accion("AAPL", 150.00, 150))
pf.agregar(Accion("MSFT", 290.00, 80))
pf.agregar(Accion("TSLA", 300.00, 40))
pf.activos["AAPL"].actualizar_precio(180.00)
pf.activos["MSFT"].actualizar_precio(340.00)
pf.activos["TSLA"].actualizar_precio(295.00)
print(pf.resumen())

# ============================================================
# Ejercicio 4: Clase Prestamo con tabla de amortización
# ============================================================
print("\\n=== Ejercicio 4: Clase Prestamo ===")


class Prestamo:
    def __init__(self, capital: float, tasa_anual: float, plazo_años: int):
        self.capital = capital
        self.tasa_anual = tasa_anual
        self.plazo_años = plazo_años

    @property
    def tasa_mensual(self) -> float:
        return self.tasa_anual / 12

    @property
    def numero_cuotas(self) -> int:
        return self.plazo_años * 12

    def cuota_mensual(self) -> float:
        r = self.tasa_mensual
        n = self.numero_cuotas
        if r == 0:
            return self.capital / n
        return self.capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    def tabla_amortizacion(self, mostrar: int = 5) -> list:
        saldo = self.capital
        cuota = self.cuota_mensual()
        tabla = []

        for periodo in range(1, self.numero_cuotas + 1):
            interes = saldo * self.tasa_mensual
            amortizacion = cuota - interes
            saldo -= amortizacion
            if periodo <= mostrar or periodo == self.numero_cuotas:
                tabla.append({
                    "periodo": periodo,
                    "cuota": round(cuota, 2),
                    "interes": round(interes, 2),
                    "amortizacion": round(amortizacion, 2),
                    "saldo": round(max(saldo, 0), 2),
                })
        return tabla


prestamo = Prestamo(200000, 0.08, 20)
print(f"Préstamo: ${prestamo.capital:,.2f} | Tasa: {prestamo.tasa_anual*100:.2f}% | Plazo: {prestamo.plazo_años} años")
print(f"Cuota mensual: ${prestamo.cuota_mensual():,.2f}")
print(f"{'Periodo':<10} {'Cuota':>12} {'Interés':>12} {'Amortización':>14} {'Saldo':>12}")
print("-" * 60)
tabla = prestamo.tabla_amortizacion()
for i, fila in enumerate(tabla):
    if i == len(tabla) - 2:
        print("...")
    print(
        f"{fila['periodo']:<10} ${fila['cuota']:>11,.2f} "
        f"${fila['interes']:>11,.2f} ${fila['amortizacion']:>13,.2f} "
        f"${fila['saldo']:>11,.2f}"
    )
```

---

> [📥 Descargar archivo .py](U15_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
