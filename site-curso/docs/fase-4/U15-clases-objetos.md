# U15: Clases y Objetos — Modelando Instrumentos Financieros

> **Lectura previa:** [U14: Manejo de Errores y Logging Profesional](../fase-3/U14-errores-logging.md)
> **Próxima unidad:** [U16: Herencia y Polimorfismo](./U16-herencia.md)

---

## 1. Teoría

### 1.1 ¿Por qué programación orientada a objetos en finanzas?

En un banco de inversión o un hedge fund, todo es un **instrumento financiero**: acciones, bonos, opciones, swaps, futuros. Cada uno tiene atributos (ticker, precio, vencimiento) y comportamientos (calcular valor, generar flujos, valorizarse). La POO permite modelar estas entidades de forma natural.

```python
# Sin POO — datos y funciones separados, difícil de mantener
ticker = "AAPL"
precio = 175.50
cantidad = 100

def valor_posicion(ticker, precio, cantidad):
    return precio * cantidad

# Con POO — datos y comportamiento encapsulados
class Accion:
    def __init__(self, ticker: str, precio: float, cantidad: int):
        self.ticker = ticker
        self.precio = precio
        self.cantidad = cantidad

    def valor(self) -> float:
        return self.precio * self.cantidad

posicion = Accion("AAPL", 175.50, 100)
print(posicion.valor())  # 17550.0
```

> ⚠️ **Principio clave:** La POO no es obligatoria, pero en finanzas donde los objetos son naturales (un bono, una acción, un portafolio), el código se lee como el negocio mismo.

### 1.2 La clase: el plano de un instrumento

Una **clase** es una plantilla. Un **objeto** (o instancia) es una copia concreta de esa plantilla.

```python
class Bono:
    """Representa un bono bullet (paga cupón periódico, principal al vencimiento)."""

    # Atributo de clase (compartido por todas las instancias)
    tipo_instrumento = "Renta Fija"

    def __init__(self, valor_nominal: float, tasa_cupon: float,
                 vencimiento: int, frecuencia_cupon: int = 2):
        # Atributos de instancia (cada bono tiene los suyos)
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon          # anual, ej: 0.05 = 5%
        self.vencimiento = vencimiento         # años hasta madurez
        self.frecuencia_cupon = frecuencia_cupon  # pagos por año

    def cupon_por_periodo(self) -> float:
        """Calcula el cupón que paga en cada periodo."""
        return self.valor_nominal * self.tasa_cupon / self.frecuencia_cupon

    def total_cupones(self) -> float:
        """Total de cupones durante la vida del bono."""
        return self.cupon_por_periodo() * self.vencimiento * self.frecuencia_cupon

# Instanciar objetos
bono_usa = Bono(valor_nominal=1000, tasa_cupon=0.05, vencimiento=10, frecuencia_cupon=2)
bono_corp = Bono(valor_nominal=5000, tasa_cupon=0.07, vencimiento=5, frecuencia_cupon=4)

print(bono_usa.tipo_instrumento)       # Renta Fija
print(bono_usa.cupon_por_periodo())    # 25.0
print(bono_corp.cupon_por_periodo())   # 87.5
print(bono_usa.total_cupones())        # 500.0
```

> 💡 **Tip:** En un desk de fixed income, cada bono tiene un ISIN, un emisor, una curva de descuento asociada. Modelarlos como objetos facilita asignarles todos esos atributos.

### 1.3 Métodos: el comportamiento del instrumento

Los métodos son funciones dentro de la clase. El primer parámetro siempre es `self`, que referencia a la instancia.

```python
class Accion:
    bolsa = "NYSE"  # atributo de clase

    def __init__(self, ticker: str, precio_compra: float, cantidad: int):
        self.ticker = ticker.upper()
        self.precio_compra = precio_compra
        self.cantidad = cantidad
        self.precio_actual = precio_compra  # inicia igual a la compra

    def actualizar_precio(self, nuevo_precio: float):
        """Actualiza el precio de mercado del activo."""
        self.precio_actual = nuevo_precio

    def valor_mercado(self) -> float:
        """Valor actual de la posición a precio de mercado."""
        return self.cantidad * self.precio_actual

    def costo(self) -> float:
        """Costo total de adquisición."""
        return self.cantidad * self.precio_compra

    def ganancia_perdida(self) -> float:
        """P&L (profit and loss) no realizada."""
        return self.valor_mercado() - self.costo()

    def rendimiento(self) -> float:
        """Retorno porcentual no realizado."""
        if self.costo() == 0:
            return 0.0
        return (self.precio_actual / self.precio_compra - 1) * 100

aapl = Accion("aapl", 150.0, 100)
aapl.actualizar_precio(175.0)
print(f"Valor mercado: ${aapl.valor_mercado():,.2f}")
print(f"Ganancia: ${aapl.ganancia_perdida():,.2f}")
print(f"Rendimiento: {aapl.rendimiento():.2f}%")
```

### 1.4 Properties: atributos calculados como si fueran simples

`@property` convierte un método en un atributo de solo lectura. Ideal para métricas que se derivan de otros datos.

```python
class Bono:
    def __init__(self, valor_nominal: float, tasa_cupon: float,
                 precio_mercado: float, vencimiento: int):
        self.valor_nominal = valor_nominal
        self.tasa_cupon = tasa_cupon
        self.precio_mercado = precio_mercado
        self.vencimiento = vencimiento

    @property
    def rendimiento_actual(self) -> float:
        """Current yield: cupón anual / precio de mercado."""
        cupon_anual = self.valor_nominal * self.tasa_cupon
        return (cupon_anual / self.precio_mercado) * 100

    @property
    def prima_descuento(self) -> str:
        """Indica si el bono cotiza sobre par, a par, o bajo par."""
        if self.precio_mercado > self.valor_nominal:
            return "Sobre par (prima)"
        elif self.precio_mercado < self.valor_nominal:
            return "Bajo par (descuento)"
        else:
            return "A la par"

bono = Bono(1000, 0.06, 950, 10)
print(bono.rendimiento_actual)  # 6.32 — accedido como atributo
print(bono.prima_descuento)     # Bajo par (descuento)
```

> 💡 **Tip:** Usa `@property` cuando quieras que una métrica se calcule dinámicamente sin necesidad de paréntesis. Es la forma idiomática en Python para getters.

### 1.5 Métodos especiales: `__repr__` y `__str__`

Controlan cómo se imprime el objeto. En finanzas, son clave para logs y debugging.

| Método | Propósito | Audiencia |
|--------|-----------|-----------|
| `__repr__` | Representación técnica, idealmente ejecutable | Desarrolladores, debugging |
| `__str__` | Representación legible para humanos | Usuarios, reportes |

```python
class Accion:
    def __init__(self, ticker: str, precio: float, cantidad: int):
        self.ticker = ticker
        self.precio = precio
        self.cantidad = cantidad

    def __repr__(self):
        return f"Accion(ticker='{self.ticker}', precio={self.precio}, cantidad={self.cantidad})"

    def __str__(self):
        valor = self.precio * self.cantidad
        return f"{self.ticker}: {self.cantidad} acciones × ${self.precio:.2f} = ${valor:,.2f}"

aapl = Accion("AAPL", 175.50, 100)
print(repr(aapl))  # Accion(ticker='AAPL', precio=175.5, cantidad=100)
print(str(aapl))   # AAPL: 100 acciones × $175.50 = $17,550.00
print(aapl)        # AAPL: 100 acciones × $175.50 = $17,550.00  (usa __str__)
```

### 1.6 Atributos de clase vs instancia

```python
class Operacion:
    comision_fija = 1.00          # atributo de clase — igual para todas
    comision_variable = 0.001     # 0.1% del monto

    def __init__(self, ticker: str, cantidad: int, precio: float):
        self.ticker = ticker
        self.cantidad = cantidad
        self.precio = precio

    def monto_bruto(self) -> float:
        return self.cantidad * self.precio

    def comision_total(self) -> float:
        return self.comision_fija + self.monto_bruto() * self.comision_variable

    def monto_neto(self) -> float:
        return self.monto_bruto() - self.comision_total()

op = Operacion("MSFT", 50, 310.0)
print(f"Bruto: ${op.monto_bruto():,.2f}")
print(f"Comisión: ${op.comision_total():,.2f}")
print(f"Neto: ${op.monto_neto():,.2f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Clase Portafolio

**Concepto financiero:** Un portafolio es un conjunto de posiciones. Su valor total es la suma del valor de mercado de cada posición.

**Código:**

```python
class Portafolio:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.activos = {}   # ticker -> objeto Accion

    def agregar(self, accion: 'Accion'):
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

    def __str__(self):
        resumen = f"Portafolio: {self.nombre}\n"
        resumen += f"{'Ticker':<8} {'Cant':>6} {'Precio':>10} {'Valor':>12} {'P&L':>10}\n"
        resumen += "-" * 50 + "\n"
        for a in self.activos.values():
            resumen += f"{a.ticker:<8} {a.cantidad:>6} ${a.precio_actual:>9.2f} "
            resumen += f"${a.valor_mercado():>11,.2f} ${a.ganancia_perdida():>9,.2f}\n"
        resumen += f"\nValor Total: ${self.valor_total():,.2f} | P&L: ${self.pnl_total():,.2f}"
        return resumen

# Uso
pf = Portafolio("Growth")
pf.agregar(Accion("AAPL", 150.0, 100))
pf.agregar(Accion("MSFT", 280.0, 50))
pf.activos["AAPL"].actualizar_precio(175.0)
pf.activos["MSFT"].actualizar_precio(310.0)
print(pf)
```

**Output:**

```
Portafolio: Growth
Ticker    Cant      Precio        Valor        P&L
--------------------------------------------------
AAPL        100 $   175.00 $   17,500.00 $   2,500.00
MSFT         50 $   310.00 $   15,500.00 $   1,500.00

Valor Total: $33,000.00 | P&L: $4,000.00
```

---

## 3. Aplicación en Finanzas 💰

En JP Morgan IBD, los analistas construyen modelos donde cada empresa es un objeto con sus estados financieros, proyecciones, y múltiplos. El `Portafolio` puede contener empresas en lugar de acciones, y métodos como `valorar_por_dcf()` o `comparables()`.

En Citadel, los sistemas de trading manejan miles de instancias de `Order`, `Fill`, `Position` por minuto. La POO permite que cada orden tenga su propio estado (`PENDING → FILLED → CANCELLED`) y que el sistema sea mantenible a escala.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-4/U15_ejercicios.py`

1. **Clase `Accion` con P&L:** Crear la clase `Accion` completa con `__init__`, `actualizar_precio`, `valor_mercado`, `costo`, `ganancia_perdida`, `rendimiento`, `__str__`.
2. **Clase `Bono` con cupones:** Crear la clase `Bono` con `__init__`, `cupon_por_periodo`, `total_cupones`, `rendimiento_actual` (property), `prima_descuento` (property), `__repr__`.
3. **Clase `Portafolio` con estadísticas:** Implementar `Portafolio` con `agregar`, `eliminar`, `valor_total`, `pnl_total`, `rendimiento_ponderado`, `concentracion_maxima` (activo de mayor peso).
4. **Clase `Prestamo` con tabla de amortización:** Crear `Prestamo` con `__init__` (capital, tasa_anual, plazo_años), método `cuota_mensual()` (sistema francés), `tabla_amortizacion()` que retorne lista de dicts con periodo, cuota, interes, amortizacion, saldo.

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| `class` | `class Accion:` |
| `__init__` | `def __init__(self, ticker, precio):` |
| Atributo de instancia | `self.ticker = ticker` |
| Atributo de clase | `tipo = "Renta Variable"` |
| Método | `def valor(self): return self.precio * self.cantidad` |
| `@property` | `@property` sobre `def rendimiento(self):` |
| `__repr__` | `f"Accion('{self.ticker}', {self.precio})"` |
| `__str__` | `f"{self.ticker}: ${self.valor():,.2f}"` |

---

## ✅ Autoevaluación

1. ¿Qué diferencia hay entre un atributo de clase y uno de instancia?
2. ¿Cuándo usarías `@property` en lugar de un método normal?
3. ¿Para qué sirve `__repr__` y en qué se diferencia de `__str__`?
4. ¿Por qué en finanzas conviene modelar instrumentos como objetos?
5. ¿Qué método especial se llama cuando usamos `print(objeto)`?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - La POO modela instrumentos financieros como entidades con datos + comportamiento
> - `@property` para métricas calculadas, `__repr__` para debugging, `__str__` para reportes
> - Patrón: cada clase representa un concepto del dominio financiero (Accion, Bono, Portafolio)
