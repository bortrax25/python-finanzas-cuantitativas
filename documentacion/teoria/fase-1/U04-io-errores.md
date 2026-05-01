# U04: Entrada, Salida y Manejo de Errores

> **Lectura previa:** [U03: Operadores](./U03-operadores.md)
> **Próxima unidad:** [U05: Condicionales — Reglas de Negocio y Señales de Trading](./U05-condicionales.md)

---

## 1. Teoría

### 1.1 Salida de datos: `print()` avanzado

```python
# Múltiples argumentos
print("Precio:", 150.50, "USD")

# Cambiar separador
print("AAPL", "MSFT", "TSLA", sep=" | ")

# Cambiar final de línea
print("Cargando...", end=" ")
print("¡Listo!")

# Expresiones en f-strings
precio = 175.50
cantidad = 100
print(f"Valor total: ${precio * cantidad:,.2f}")
```

### 1.2 f-strings con formato monetario

```python
accion = "AAPL"
precio = 175.50
cantidad = 10

# Decimales
print(f"Precio: ${precio:.2f}")                      # $175.50

# Separadores de miles
inversion = 1500000
print(f"Inversión: ${inversion:,.2f}")               # $1,500,000.00

# Alineación en columnas
print(f"{'Activo':<10} {'Precio':>10}")
print(f"{accion:<10} ${precio:>9.2f}")

# Porcentajes
rendimiento = 0.1523
print(f"Rendimiento: {rendimiento:.2%}")              # 15.23%

# Signo
pl = -250.50
print(f"P&L: ${pl:+,.2f}")                           # -$250.50
```

### 1.3 Entrada de datos: `input()`

```python
nombre = input("Ingresa tu nombre: ")
print(f"Hola, {nombre}")

# ⚠️ input() siempre retorna str — debes convertir
capital = float(input("Capital inicial: $"))
tasa = float(input("Tasa anual (%): ")) / 100
tiempo = int(input("Años: "))

monto_final = capital * (1 + tasa) ** tiempo
print(f"Monto final: ${monto_final:,.2f}")
```

### 1.4 `try/except` — Manejo de errores

En finanzas, el usuario puede ingresar datos inválidos (tasas negativas, texto en vez de números). `try/except` protege tu programa.

```python
# Capturar errores de conversión
try:
    edad = int(input("Edad: "))
    print(f"Tienes {edad} años")
except ValueError:
    print("Error: Ingresa un número válido")

# Múltiples excepciones
try:
    capital = float(input("Capital: $"))
    tasa = float(input("Tasa anual (%): "))
    tiempo = int(input("Años: "))
    if capital <= 0 or tasa < 0 or tiempo <= 0:
        raise ValueError("Los valores deben ser positivos")
    monto = capital * (1 + tasa/100) ** tiempo
    print(f"Monto final: ${monto:,.2f}")
except ValueError as e:
    print(f"Error de entrada: {e}")
except ZeroDivisionError:
    print("Error: División por cero")
```

### 1.5 `assert` — Validación en desarrollo

`assert` verifica una condición y lanza `AssertionError` si es falsa. Se usa para detectar bugs en desarrollo.

```python
# Validar inputs financieros
def calcular_interes(capital, tasa, tiempo):
    assert capital > 0, "El capital debe ser positivo"
    assert 0 <= tasa <= 100, "La tasa debe estar entre 0 y 100"
    assert tiempo > 0, "El tiempo debe ser positivo"
    return capital * (tasa / 100) * tiempo

calcular_interes(10000, 5, 3)     # OK
# calcular_interes(-1000, 5, 3)    # AssertionError: El capital debe ser positivo

# ⚠️ En producción se desactivan con python -O
```

### 1.6 Errores comunes

| Error | Causa | Ejemplo | Solución |
|-------|-------|---------|---------|
| `SyntaxError` | Escritura incorrecta | `print "hola"` | Revisar sintaxis |
| `NameError` | Variable no definida | `print(precio)` | Definir la variable |
| `TypeError` | Tipo incorrecto | `"precio: " + 150` | `str(150)` |
| `ValueError` | Conversión inválida | `int("abc")` | Validar antes |
| `ZeroDivisionError` | División por cero | `100 / 0` | Validar divisor |

### 1.7 Cómo leer un traceback

```python
capital = 10000
tiempo = "tres"
interes = capital * tiempo

# Traceback:
# Traceback (most recent call last):
#   File "script.py", line 3, in <module>
#     interes = capital * tiempo
# TypeError: can't multiply sequence by non-int of type 'float'
```

**Regla:** Lee de **abajo hacia arriba**. La última línea dice qué error y dónde.

### 1.8 Debugging con VS Code

1. **Breakpoints:** Clic izquierdo en el margen → punto rojo
2. **F5** para empezar a debuggear
3. **Step Over (F10):** ejecutar línea actual
4. **Step Into (F11):** entrar a una función
5. **Variables:** panel izquierdo muestra valores en tiempo real
6. **Watch:** agregar expresiones para monitorear

### 1.9 Validación de inputs financieros

```python
# Patrón robusto para calculadora financiera
def obtener_numero_positivo(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("Error: debe ser un número positivo")
                continue
            return valor
        except ValueError:
            print("Error: ingresa un número válido")

# Uso
capital = obtener_numero_positivo("Capital inicial: $")
tasa = obtener_numero_positivo("Tasa anual (%): ")
tiempo = obtener_numero_positivo("Años: ")

monto = capital * (1 + tasa/100) ** tiempo
print(f"Monto final: ${monto:,.2f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Calculadora financiera interactiva

```python
print("=" * 50)
print("CALCULADORA DE INTERÉS COMPUESTO")
print("=" * 50)

try:
    capital = float(input("Capital inicial ($): "))
    tasa_anual = float(input("Tasa anual (%): "))
    tiempo_anios = float(input("Tiempo (años): "))

    assert capital > 0, "Capital debe ser positivo"
    assert tasa_anual >= 0, "Tasa no puede ser negativa"
    assert tiempo_anios > 0, "Tiempo debe ser positivo"

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
except ValueError:
    print("Error: Debes ingresar valores numéricos")
except AssertionError as e:
    print(f"Error de validación: {e}")
```

### 2.2 Ejercicio guiado: Depuración de un script roto

```python
# Versión con errores:
# capital = input("Capital: ")          # No convertido
# tasa = float(input("Tasa (%): ")      # Falta paréntesis
# tiempo = float(input"Tiempo: "))      # Error sintaxis
# interes = capital * tasa * tiempo      # capital es str
# print("Interés: " + interes)          # str + float

# Versión corregida:
capital = float(input("Capital: "))
tasa = float(input("Tasa (%): ")) / 100
tiempo = float(input("Tiempo: "))
interes = capital * tasa * tiempo
print(f"Interés: ${interes:,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Calculadora de posición con validación

```python
ticker = input("Símbolo: ").upper().strip()
assert ticker.isalpha() and 1 <= len(ticker) <= 5, "Ticker inválido"

precio_entrada = float(input(f"Precio de entrada de {ticker}: $"))
cantidad = int(input(f"Cantidad de {ticker}: "))
precio_actual = float(input(f"Precio actual de {ticker}: $"))

assert precio_entrada > 0 and cantidad > 0 and precio_actual > 0

valor_entrada = precio_entrada * cantidad
valor_actual = precio_actual * cantidad
pl = valor_actual - valor_entrada
pl_pct = (pl / valor_entrada) * 100

print(f"\n--- Resumen de Posición ---")
print(f"{ticker}: {cantidad} acciones")
print(f"P&L: ${pl:+,.2f} ({pl_pct:+.2f}%)")
```

### 3.2 Cuadro de amortización con validación

```python
try:
    monto = float(input("Monto del préstamo: $"))
    tasa_anual = float(input("Tasa anual (%): "))
    plazo_meses = int(input("Plazo (meses): "))

    assert monto > 0 and tasa_anual >= 0 and plazo_meses > 0

    tasa_mensual = (tasa_anual / 100) / 12
    cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)

    saldo = monto
    print(f"\nCuota mensual: ${cuota:,.2f}")
    print(f"{'Mes':<6} {'Cuota':<12} {'Interés':<12} {'Capital':<12} {'Saldo':<12}")

    for mes in range(1, plazo_meses + 1):
        interes = saldo * tasa_mensual
        capital_pagado = cuota - interes
        saldo -= capital_pagado
        print(f"{mes:<6} ${cuota:<11.2f} ${interes:<11.2f} ${capital_pagado:<11.2f} ${saldo:<11.2f}")
except ValueError:
    print("Error: ingresa valores numéricos válidos")
except AssertionError as e:
    print(f"Error: {e}")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-1/U04_ejercicios.py`

1. **Perfil de riesgo:** Pide edad, ingresos, ahorros y tolerancia (1-10). Valida con try/except.

2. **Calculadora DCA:** El usuario ingresa 3 compras periódicas. Calcula precio promedio y total invertido.

3. **Depuración guiada:** Script con 5 errores. Encuéntralos y corrígelos.

4. **Conversor interactivo:** Convierte USD a PEN y EUR con tipos de cambio validados.

---

## 5. Resumen

| Comando / Concepto | Descripción |
|-------------------|------------|
| `print()` | Mostrar en consola |
| `input()` | Leer del usuario (siempre str) |
| f-string | `f"${precio:,.2f}"` |
| `try/except` | Capturar errores |
| `assert` | Validar condiciones en desarrollo |
| Traceback | Leer de abajo hacia arriba |
| VS Code Debugger | Breakpoints, F5, F10, F11 |

---

## ✅ Autoevaluación

1. ¿Qué tipo retorna `input()`?
2. ¿Cómo formateas un float a 2 decimales en un f-string?
3. ¿Qué error produce `"total: " + 100`?
4. ¿Cómo lees un traceback?
5. Escribe un programa que pida monto USD, lo convierta a PEN y EUR, y valide las entradas con try/except.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U04.md`: Especificadores de formato f-string, errores comunes, patrón try/except
> - `project-U04.md`: Validación de inputs financieros, cuadro de amortización
