# U01: Variables y Tipos de Datos en Python

> **Lectura previa:** [U00: Preparando tu entorno](../fase-0/U00-setup.md)
> **Próxima unidad:** [U02: Operadores en Python](./U02-operadores-python.md)

---

## 1. Teoría

### 1.1 ¿Qué es una variable?

Una **variable** es un espacio en la memoria de la computadora que almacena un valor y tiene un nombre asociado. Piensa en una variable como una **etiqueta** que le pones a un dato para poder usarlo después.

```python
# Sintaxis básica
nombre_variable = valor

# Ejemplos
edad = 25
precio = 100.50
nombre = "Carlos"
activo = True
```

> 💡 En Python no necesitas declarar el tipo de la variable. El tipo se infiere automáticamente del valor asignado. Esto se llama **tipado dinámico**.

### 1.2 Tipos de datos en Python

Python tiene 4 tipos de datos básicos que usarás constantemente:

| Tipo | Palabra clave | Ejemplo | ¿Qué almacena? |
|------|-------------|---------|---------------|
| Entero | `int` | `42`, `-7`, `0` | Números sin decimales |
| Decimal | `float` | `3.14`, `-0.5`, `1.0` | Números con decimales |
| Texto | `str` | `"hola"`, `'Python'` | Cadenas de caracteres |
| Booleano | `bool` | `True`, `False` | Verdadero o falso |

```python
# Ver el tipo de una variable
type(42)        # <class 'int'>
type(3.14)      # <class 'float'>
type("hola")    # <class 'str'>
type(True)      # <class 'bool'>
```

### 1.3 Reglas para nombrar variables

| Regla | Correcto | Incorrecto |
|-------|---------|-----------|
| Solo letras, números y `_` | `precio_accion` | `precio-accion` |
| No puede empezar con número | `accion1` | `1accion` |
| Case-sensitive | `Precio` ≠ `precio` | — |
| Sin palabras reservadas | `mi_for` | `for` |

```python
# ✅ Correcto
tasa_interes = 0.05
precioCierre = 150.25
_accion = "AAPL"

# ❌ Incorrecto
# 1variable = 10        # Empieza con número
# precio-accion = 100   # Usa guión
# class = "finanzas"    # Palabra reservada
```

> 💡 La convención en Python es usar **snake_case**: palabras en minúsculas separadas por guiones bajos (`precio_compra`, `tasa_anual`).

### 1.4 Asignación múltiple

Python permite asignar varias variables en una sola línea:

```python
# Asignación múltiple
x, y, z = 10, 20, 30

# Intercambio de valores (swap)
a, b = 1, 2
a, b = b, a          # Ahora a=2, b=1

# Desempaquetado
precio, cantidad = 100.50, 10
```

### 1.5 Conversión entre tipos (casting)

Puedes convertir entre tipos usando las funciones `int()`, `float()`, `str()`, `bool()`:

```python
# String a número
precio_str = "150"
precio = float(precio_str)    # 150.0

# Número a string
cantidad = 10
mensaje = "Tienes " + str(cantidad) + " acciones"

# Float a int (trunca, no redondea)
entero = int(3.9)             # 3
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Calculadora de interés simple

**Concepto financiero:** El **interés simple** se calcula sobre el capital inicial, sin reinvertir intereses.

**Fórmula:** `I = C * i * t` donde:
- `C` = capital inicial
- `i` = tasa de interés (en decimal)
- `t` = tiempo (en años)

**Código:**
```python
# Datos de entrada
capital = 10000          # int
tasa_anual = 5           # int (porcentaje)
tiempo_anios = 3         # int

# Convertir tasa a decimal
tasa_decimal = tasa_anual / 100    # 0.05 (float)

# Calcular interés
interes = capital * tasa_decimal * tiempo_anios      # 1500.0
monto_final = capital + interes                      # 11500.0

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

### 2.2 Ejercicio guiado: Rendimiento de una acción

**Concepto financiero:** El **rendimiento** mide la ganancia o pérdida relativa de una inversión.

**Fórmula:** `rendimiento = (precio_actual - precio_compra) / precio_compra * 100`

```python
precio_compra = 150.25
precio_actual = 175.50

ganancia = precio_actual - precio_compra
rendimiento = (ganancia / precio_compra) * 100

print(f"Precio de compra: ${precio_compra}")
print(f"Precio actual: ${precio_actual}")
print(f"Ganancia por acción: ${ganancia:.2f}")
print(f"Rendimiento: {rendimiento:.2f}%")
```

---

## 3. Aplicación en Finanzas 💰

En el mundo real, las variables y tipos de datos se usan para representar:

```python
# Cartera de inversión
ticker = "AAPL"              # str: símbolo de la acción
precio = 175.50              # float: precio por acción
cantidad = 100               # int: número de acciones
es_ganancia = True           # bool: ¿está en verde?

# Valor total de la posición
valor_posicion = precio * cantidad    # float: $17,550.00
```

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-1/U01_ejercicios.py`

1. **Calculadora de interés compuesto anual simple:** Dado un capital, tasa y años, calcular el monto final con interés compuesto básico (sin bucle aún: `monto = capital * (1 + tasa) ** anios`).

2. **Conversor de monedas:** Dada una cantidad en USD y un tipo de cambio (PEN, MXN, COP), mostrar el equivalente en la moneda local.

3. **Datos personales del inversionista:** Crea variables con tu nombre, edad, capital inicial y meta de rendimiento. Imprime un resumen formateado.

4. **Cálculo de comisión:** Un broker cobra 0.5% de comisión. Dado un monto de transacción, calcula la comisión y el monto neto.

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Variable | `x = 10` |
| `int` | `42` |
| `float` | `3.14` |
| `str` | `"Python"` |
| `bool` | `True` |
| f-string | `f"Valor: {x}"` |
| Casting | `int("10")`, `float("3.14")` |
| Asignación múltiple | `a, b = 1, 2` |

---

## ✅ Autoevaluación

1. ¿Qué tipo de dato usarías para almacenar el precio de una acción? ¿Y la cantidad de acciones?
2. ¿Qué imprime `type(3.0)`? ¿Y `type("3")`? ¿Y `type(True)`?
3. Corrige: `1precio = 100`
4. ¿Qué hace `int(5.9)` y por qué?
5. Escribe un programa que calcule el valor total de tu portafolio con 3 acciones diferentes.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U01.md`: Ruta de los ejercicios de esta unidad y sus soluciones
> - `project-U01.md`: Los 4 tipos de datos básicos y la fórmula de interés simple
