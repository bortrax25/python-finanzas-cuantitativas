# U03: Entrada, Salida y Debugging

> **Lectura previa:** [U02: Operadores en Python](./U02-operadores-python.md)
> **Próxima unidad:** [U04: Estructuras de control](./U04-estructuras-control.md)

---

## 1. Teoría

### 1.1 Salida de datos: `print()`

La función `print()` muestra información en la consola. Es tu principal herramienta para ver resultados.

```python
# Sintaxis básica
print("Hola, finanzas")

# Múltiples argumentos (separados por espacio)
print("Precio:", 150, "USD")             # Precio: 150 USD

# Cambiar separador
print("AAPL", "MSFT", "TSLA", sep=" | ")  # AAPL | MSFT | TSLA

# Cambiar final de línea
print("Cargando...", end=" ")
print("¡Listo!")                          # Cargando... ¡Listo!
```

### 1.2 f-strings (Formateo avanzado)

Los **f-strings** (Python 3.6+) son la forma más legible de formatear texto con variables.

```python
# Sintaxis: f"texto {variable} texto"

accion = "AAPL"
precio = 175.50
cantidad = 10

# Formateo básico
print(f"Acción: {accion}, Precio: ${precio}")

# Especificar decimales
print(f"Precio: ${precio:.2f}")           # Precio: $175.50

# Separadores de miles
inversion = 1500000
print(f"Inversión: ${inversion:,.2f}")    # Inversión: $1,500,000.00

# Alineación y ancho
print(f"{'Activo':<10} {'Precio':>10}")   # Activo          Precio
print(f"{accion:<10} ${precio:>9.2f}")    # AAPL       $175.50

# Porcentajes
rendimiento = 0.1523
print(f"Rendimiento: {rendimiento:.2%}")  # Rendimiento: 15.23%

# Expresiones dentro de f-strings
print(f"Valor total: {precio * cantidad:.2f}")
```

### 1.3 Entrada de datos: `input()`

La función `input()` permite recibir datos del usuario. **Siempre retorna un string.**

```python
# Sintaxis
nombre = input("Ingresa tu nombre: ")
print(f"Hola, {nombre}")

# ⚠️ input() siempre retorna str, DEBES convertir
edad_str = input("Edad: ")     # "25" (string)
edad = int(edad_str)           # 25 (int)

# Forma directa (más común)
capital = float(input("Capital inicial: $"))
tasa = float(input("Tasa anual (%): "))
tiempo = int(input("Años: "))

monto_final = capital * (1 + tasa/100) ** tiempo
print(f"Monto final: ${monto_final:,.2f}")
```

### 1.4 Tipos de errores y debugging

#### 1.4.1 Errores comunes

| Error | Causa | Ejemplo | Solución |
|-------|-------|---------|---------|
| `SyntaxError` | Escritura incorrecta | `print "hola"` | Revisar sintaxis |
| `NameError` | Variable no definida | `print(precio)` cuando no existe | Definir la variable primero |
| `TypeError` | Operación entre tipos incorrectos | `"precio: " + 150` | Convertir: `str(150)` |
| `ValueError` | Conversión inválida | `int("abc")` | Verificar el dato antes de convertir |
| `ZeroDivisionError` | División entre cero | `100 / 0` | Validar divisor ≠ 0 |
| `IndentationError` | Indentación incorrecta | Falta o sobra espacio | 4 espacios por nivel |

```python
# Ejemplos de cada error
# SyntaxError: print "hola"         # Faltan paréntesis
# NameError:   print(precio)         # precio no está definida
# TypeError:   "total: " + 100       # str + int inválido
# ValueError:  int("cien")           # "cien" no es número
# ZeroDivisionError: 100 / 0         # División por cero
```

#### 1.4.2 Cómo leer un traceback

Cuando ocurre un error, Python muestra un **traceback**: la ruta del error.

```python
# Código con error
capital = 10000
tiempo = "tres"
interes = capital * tiempo

# Traceback (de abajo hacia arriba se lee):
# Traceback (most recent call last):
#   File "script.py", line 3, in <module>
#     interes = capital * tiempo
# TypeError: can't multiply sequence by non-int of type 'int'
#         ↑ tipo de error   ↑ mensaje explicativo
```

**Regla para leer tracebacks:** lee desde la **última línea hacia arriba**. La última línea dice qué error ocurrió y dónde.

#### 1.4.3 Debugging con `print()`

La técnica más simple y efectiva: imprimir variables en puntos clave.

```python
# Sin debug — ¿dónde está el error?
capital = float(input("Capital: "))
tasa = float(input("Tasa (%): ")) / 100
tiempo = float(input("Años: "))
print(capital, tasa, tiempo)           # Verifica valores
monto = capital * (1 + tasa) ** tiempo
print(f"Monto calculado: {monto}")     # Verifica resultado
print(f"Monto final: ${monto:,.2f}")
```

#### 1.4.4 Validación de entrada

Siempre que uses `input()`, el usuario puede ingresar datos inválidos:

```python
# Estrategia: try/except (versión simple, se profundiza en U05)
try:
    edad = int(input("Edad: "))
    print(f"Tienes {edad} años")
except ValueError:
    print("⚠️ Error: Ingresa un número válido")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Calculadora financiera interactiva

```python
print("=" * 50)
print("CALCULADORA DE INTERÉS COMPUESTO")
print("=" * 50)

capital = float(input("Capital inicial ($): "))
tasa_anual = float(input("Tasa anual (%): "))
tiempo_anios = float(input("Tiempo (años): "))

tasa_decimal = tasa_anual / 100
monto_final = capital * (1 + tasa_decimal) ** tiempo_anios
interes_ganado = monto_final - capital

print()
print("=" * 50)
print("RESULTADOS")
print("=" * 50)
print(f"Capital inicial:    ${capital:>15,.2f}")
print(f"Tasa anual:         {tasa_anual:>15.2f}%")
print(f"Tiempo:             {tiempo_anios:>15.2f} años")
print(f"-" * 50)
print(f"Interés ganado:     ${interes_ganado:>15,.2f}")
print(f"Monto final:        ${monto_final:>15,.2f}")
```

### 2.2 Ejercicio guiado: Debugging de un script roto

```python
# Este script tiene errores. Encuiéntralos y corrígelos.

# Versión con errores:
capital = input("Capital: ")          # No se convierte a número
tasa = float(input("Tasa (%): ")
tiempo = float(input"Tiempo: "))      # Error de sintaxis
interés = capital * tasa * tiempo      # Error de tipo
print("Interés: " + interes)          # Error de tipo

# Solución corregida:
capital = float(input("Capital: "))
tasa = float(input("Tasa (%): ")) / 100
tiempo = float(input("Tiempo: "))
interes = capital * tasa * tiempo
print(f"Interés: ${interes:,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

En finanzas, leer datos del usuario y mostrar resultados formateados es esencial:

```python
# Calculadora de posición
ticker = input("Símbolo de la acción: ").upper()
precio_entrada = float(input(f"Precio de entrada de {ticker}: $"))
cantidad = int(input(f"Cantidad de acciones de {ticker}: "))
precio_actual = float(input(f"Precio actual de {ticker}: $"))

valor_entrada = precio_entrada * cantidad
valor_actual = precio_actual * cantidad
pl = valor_actual - valor_entrada
pl_pct = (pl / valor_entrada) * 100

print("\n--- Resumen de Posición ---")
print(f"{ticker}: {cantidad} acciones")
print(f"P&L: ${pl:+,.2f} ({pl_pct:+.2f}%)")
```

---

## 4. Ejercicios Propuestos

1. **Perfil de riesgo:** Pide edad, ingresos mensuales, ahorros y tolerancia al riesgo (1-10). Muestra un perfil formateado.

2. **Calculadora de DCA (Dollar Cost Averaging):** El usuario ingresa 3 compras periódicas (cantidad y precio). Calcula precio promedio y total invertido.

3. **Depuración guiada:** Te daré un script con 5 errores. Encuéntralos, corrígelos y explica cada uno.

4. **Conversor avanzado:** Convierte entre PEN, USD y EUR usando tasas ingresadas por el usuario.

---

## 5. Resumen

| Comando | Descripción | Ejemplo |
|---------|------------|---------|
| `print()` | Mostrar en consola | `print("Hola")` |
| `input()` | Leer del usuario (siempre str) | `x = input("Valor: ")` |
| f-string | Formatear texto | `f"${precio:.2f}"` |
| `try/except` | Capturar errores | `try: ... except: ...` |

**Regla de oro del debugging:** si algo falla, imprime las variables para ver qué valor tienen realmente.

---

## ✅ Autoevaluación

1. ¿Qué tipo de dato retorna `input()`?
2. ¿Cómo formateas un float a 2 decimales en un f-string?
3. ¿Qué error produce `"total: " + 100` y cómo lo corrijes?
4. ¿Cómo lees un traceback de Python (de arriba a abajo o de abajo a arriba)?
5. Escribe un programa que pida un monto en USD, lo convierta a 3 monedas diferentes y muestre los resultados en columnas alineadas.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U03.md`: Tabla de especificadores de formato en f-strings
> - `project-U03.md`: Tabla de errores comunes y cómo leer tracebacks
