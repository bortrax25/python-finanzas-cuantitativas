# U02: Variables, Tipos de Datos y el Lenguaje de los Mercados

> **Lectura previa:** [U01: Jupyter y el flujo cuantitativo](../fase-0/U01-jupyter.md)
> **Próxima unidad:** [U03: Operadores — La Aritmética de Wall Street](./U03-operadores.md)

---

## 1. Teoría

### 1.1 ¿Qué es una variable?

Una **variable** es un espacio en memoria que almacena un valor y tiene un nombre. Piensa en una variable como una **etiqueta** que le pones a un dato.

```python
# Sintaxis
nombre_variable = valor

# Ejemplos con contexto financiero
ticker = "AAPL"
precio_accion = 175.50
cantidad_acciones = 100
posicion_abierta = True
```

> 💡 Python tiene **tipado dinámico**: no necesitas declarar el tipo. Se infiere del valor.

### 1.2 Tipos de datos básicos

| Tipo | Palabra clave | Ejemplo | Uso financiero |
|------|-------------|---------|---------------|
| Entero | `int` | `42`, `-7`, `1000000` | Cantidades de acciones, plazos |
| Decimal | `float` | `3.14`, `175.50` | Precios, tasas, rendimientos |
| Texto | `str` | `"AAPL"`, `'NASDAQ'` | Tickers, nombres, sectores |
| Booleano | `bool` | `True`, `False` | Señales, condiciones de mercado |

```python
# Ver el tipo con type()
type(175.50)     # <class 'float'>
type("AAPL")     # <class 'str'>
type(100)        # <class 'int'>
type(True)       # <class 'bool'>
```

### 1.3 `Decimal` — Precisión bancaria

En finanzas, los `float` tienen problemas de precisión. Una operación con muchos decimales puede generar errores de redondeo inaceptables en banca.

```python
# Problema con float
0.1 + 0.2                   # 0.30000000000000004  ← ¡Error!
0.1 + 0.2 == 0.3            # False

# Solución: Decimal
from decimal import Decimal, getcontext

getcontext().prec = 10      # Precisión de 10 dígitos

Decimal("0.1") + Decimal("0.2")       # Decimal('0.3')
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True

# En banca: siempre Decimal para dinero
precio = Decimal("175.50")
cantidad = Decimal("100")
valor_total = precio * cantidad        # Decimal('17550.00')
```

> ⚠️ Siempre crea `Decimal` desde strings, no desde floats: `Decimal("0.1")`, no `Decimal(0.1)`.

### 1.4 Reglas para nombrar variables (snake_case español)

| Regla | Correcto | Incorrecto |
|-------|---------|-----------|
| Solo letras, números y `_` | `precio_accion` | `precio-accion` |
| No empezar con número | `accion1` | `1accion` |
| Case-sensitive | `Precio` ≠ `precio` | — |
| Sin palabras reservadas | `mi_clase` | `class` |

```python
# ✅ Correcto — snake_case en español
tasa_interes = 0.05
precio_compra = 150.25
cantidad_acciones = 10
es_rentable = True

# ❌ Incorrecto
# 1accion = "AAPL"         # Empieza con número
# precio-accion = 100      # Usa guión
# class = "finanzas"       # Palabra reservada
```

> 💡 La convención del curso: variables en español con snake_case. Librerías y funciones de Python en inglés.

### 1.5 Asignación múltiple y swap

```python
# Asignación múltiple
ticker, precio, cantidad = "AAPL", 175.50, 100

# Swap (intercambiar valores)
a, b = 1, 2
a, b = b, a            # Ahora a=2, b=1

# Desempaquetar tuplas
datos_accion = ("MSFT", 310.00, "Tecnología")
ticker, precio, sector = datos_accion
```

### 1.6 Conversión entre tipos (casting)

```python
# String a número
precio_str = "175.50"
precio = float(precio_str)      # 175.5

# Número a string
cantidad = 100
mensaje = "Tienes " + str(cantidad) + " acciones"

# Float a int (TRUNCA, no redondea)
int(3.9)     # 3
int(175.99)  # 175

# String a Decimal
from decimal import Decimal
monto = Decimal("1500000.50")
```

### 1.7 f-strings con formato monetario

El formateo de números en finanzas es crítico. Un MD de JP Morgan espera ver `$1,500,000.00`, no `1500000.0`.

```python
precio = 175.50
cantidad = 10000

# Formato básico
print(f"${precio:.2f}")                    # $175.50

# Separadores de miles
print(f"${cantidad * precio:,.2f}")        # $1,755,000.00

# Porcentajes
rendimiento = 0.1523
print(f"{rendimiento:.2%}")                # 15.23%

# Alineación en columnas
tickers = ["AAPL", "MSFT", "JPM"]
precios = [175.50, 310.00, 140.25]
for t, p in zip(tickers, precios):
    print(f"{t:<6} ${p:>10,.2f}")

# Output:
# AAPL   $    175.50
# MSFT   $    310.00
# JPM    $    140.25
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Calculadora de interés simple

**Concepto financiero:** El **interés simple** se calcula sobre el capital inicial, sin reinvertir intereses.

**Fórmula:** `I = C * i * t`

```python
capital = 10000
tasa_anual = 5
tiempo_anios = 3

tasa_decimal = tasa_anual / 100
interes = capital * tasa_decimal * tiempo_anios
monto_final = capital + interes

print(f"Capital inicial: ${capital:,.2f}")
print(f"Tasa anual: {tasa_anual}%")
print(f"Tiempo: {tiempo_anios} años")
print(f"Interés generado: ${interes:,.2f}")
print(f"Monto final: ${monto_final:,.2f}")
```

**Output:**
```
Capital inicial: $10,000.00
Tasa anual: 5%
Tiempo: 3 años
Interés generado: $1,500.00
Monto final: $11,500.00
```

### 2.2 Ejercicio guiado: Interés compuesto

**Concepto financiero:** El **interés compuesto** reinvierte los intereses generados. Es la base de toda valoración financiera.

**Fórmula:** `M = C * (1 + i)^t`

```python
capital = 10000
tasa_anual = 8
anios = 10

tasa_decimal = tasa_anual / 100
monto_final = capital * (1 + tasa_decimal) ** anios
interes_ganado = monto_final - capital

print(f"Capital inicial: ${capital:,.2f}")
print(f"Tasa anual: {tasa_anual}%")
print(f"Plazo: {anios} años")
print(f"Interés ganado: ${interes_ganado:,.2f}")
print(f"Monto final: ${monto_final:,.2f}")
```

**Output:**
```
Capital inicial: $10,000.00
Tasa anual: 8%
Plazo: 10 años
Interés ganado: $11,589.25
Monto final: $21,589.25
```

### 2.3 Ejercicio guiado: Rendimiento de una acción

```python
precio_compra = 150.25
precio_actual = 175.50
cantidad = 10

ganancia_unitaria = precio_actual - precio_compra
rendimiento_pct = (ganancia_unitaria / precio_compra) * 100
ganancia_total = ganancia_unitaria * cantidad

print(f"Ticker: AAPL")
print(f"Precio de compra: ${precio_compra:,.2f}")
print(f"Precio actual: ${precio_actual:,.2f}")
print(f"Ganancia por acción: ${ganancia_unitaria:,.2f}")
print(f"Rendimiento: {rendimiento_pct:.2f}%")
print(f"Ganancia total ({cantidad} acciones): ${ganancia_total:,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Datos de mercado como variables

```python
# Posición real en un portafolio
ticker = "AAPL"
mercado = "NASDAQ"
precio_compra = 150.50
precio_actual = 175.80
cantidad = 500
sector = "Tecnología"
es_dividendo = True

valor_compra = precio_compra * cantidad
valor_actual = precio_actual * cantidad
ganancia = valor_actual - valor_compra
rendimiento = (ganancia / valor_compra) * 100

print(f"Posición: {ticker} ({sector}, {mercado})")
print(f"Valor compra: ${valor_compra:,.2f}")
print(f"Valor actual: ${valor_actual:,.2f}")
print(f"P&L: ${ganancia:+,.2f} ({rendimiento:+.2f}%)")
```

### 3.2 Tipos de cambio con Decimal

```python
from decimal import Decimal

# Conversión precisa USD → PEN → EUR
monto_usd = Decimal("10000.00")
tipo_pen = Decimal("3.753")
tipo_eur = Decimal("0.921")

monto_pen = monto_usd * tipo_pen
monto_eur = monto_usd * tipo_eur

print(f"${monto_usd:,.2f} USD")
print(f"  = S/ {monto_pen:,.2f} PEN")
print(f"  = € {monto_eur:,.2f} EUR")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-1/U02_ejercicios.py`

1. **Calculadora de interés compuesto:** Dado un capital, tasa y años, calcular monto final con `M = C * (1 + i)^t`.

2. **Conversor de monedas:** Dada una cantidad en USD y tipos de cambio (PEN, MXN, COP), mostrar el equivalente en cada moneda local.

3. **Perfil del inversionista:** Crea variables con nombre, edad, capital inicial y meta de rendimiento. Imprime un resumen formateado.

4. **Comisión del broker:** Un broker cobra 0.5% de comisión. Calcula la comisión y el monto neto.

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Variable | `x = 10` |
| `int` | `42` |
| `float` | `3.14` |
| `str` | `"AAPL"` |
| `bool` | `True` |
| `Decimal` | `Decimal("175.50")` |
| f-string moneda | `f"${precio:,.2f}"` |
| f-string porcentaje | `f"{rendimiento:.2%}"` |
| Casting | `int("10")`, `float("3.14")` |
| Asignación múltiple | `a, b = 1, 2` |

---

## ✅ Autoevaluación

1. ¿Qué tipo usarías para el precio de una acción? ¿Y para la cantidad?
2. ¿Qué imprime `type(3.0)`? ¿Y `type("3")`?
3. ¿Por qué en banca se usa `Decimal` y no `float`?
4. ¿Qué hace `int(5.9)` y por qué?
5. Calcula el valor total de un portafolio con 3 acciones diferentes.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U02.md`: Tipos de datos, f-strings de formato monetario, Decimal
> - `project-U02.md`: Fórmulas de interés simple y compuesto
