# U07: Bucle for y range()

> **Lectura previa:** [U06: Condicionales anidados](../fase-2/U06-condicionales-anidados.md)
> **Próxima unidad:** [U08: Bucle while y control de flujo](./U08-while-control.md)

---

## 1. Teoría

### 1.1 ¿Qué es un bucle `for`?

Un bucle `for` ejecuta un bloque de código **para cada elemento** de una secuencia (lista, string, rango, etc.).

```python
# Sintaxis
for variable in secuencia:
    # código que se repite

# Ejemplo
acciones = ["AAPL", "MSFT", "TSLA"]
for ticker in acciones:
    print(f"Analizando {ticker}")
```

### 1.2 `range()` — Generador de secuencias numéricas

`range()` es la herramienta principal para generar secuencias de números.

| Forma | Descripción | Secuencia |
|-------|------------|-----------|
| `range(n)` | 0 a n-1 | `0, 1, 2, ..., n-1` |
| `range(inicio, fin)` | inicio a fin-1 | `inicio, inicio+1, ..., fin-1` |
| `range(inicio, fin, paso)` | inicio a fin-1 con paso | `inicio, inicio+paso, ...` |

```python
# range(stop)
for i in range(5):
    print(i, end=" ")           # 0 1 2 3 4

# range(start, stop)
for i in range(1, 6):
    print(i, end=" ")           # 1 2 3 4 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i, end=" ")           # 0 2 4 6 8

# Paso negativo (cuenta regresiva)
for i in range(5, 0, -1):
    print(i, end=" ")           # 5 4 3 2 1
```

### 1.3 `enumerate()` — Índice + valor

`enumerate()` te da el índice y el valor simultáneamente:

```python
acciones = ["AAPL", "MSFT", "TSLA"]

for indice, ticker in enumerate(acciones):
    print(f"{indice}: {ticker}")

for dia, ticker in enumerate(acciones, start=1):
    print(f"Día {dia}: {ticker}")
```

### 1.4 Recorrer strings

Los strings son secuencias de caracteres, así que `for` los recorre letra por letra:

```python
ticker = "AAPL"
for letra in ticker:
    print(letra, end=" ")    # A A P L

# Contar mayúsculas
texto = "Python Finanzas"
mayusculas = 0
for caracter in texto:
    if caracter.isupper():
        mayusculas += 1
print(f"Mayúsculas: {mayusculas}")
```

### 1.5 Acumuladores con `for`

Patrón común: acumular un resultado iteración a iteración.

```python
# Suma de rendimientos
rendimientos = [5.2, -2.1, 3.8, -0.5, 4.2]
suma = 0
for r in rendimientos:
    suma += r
promedio = suma / len(rendimientos)
print(f"Suma: {suma:.1f}%, Promedio: {promedio:.1f}%")

# Producto acumulado (interés compuesto)
capital = 1000
tasas = [0.02, 0.015, 0.03, -0.01]
for tasa in tasas:
    capital *= (1 + tasa)
    print(f"Capital: ${capital:.2f}")
```

### 1.6 `for` con `else` y `zip()`

```python
# zip() empareja listas
precios = [150, 280, 900]
cantidades = [10, 5, 3]
tickers = ["AAPL", "MSFT", "TSLA"]

for ticker, precio, cantidad in zip(tickers, precios, cantidades):
    valor = precio * cantidad
    print(f"{ticker}: {cantidad} × ${precio} = ${valor:,.2f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Rendimiento acumulado de portafolio

```python
# Datos diarios de rendimiento (%)
rendimientos = [1.2, -0.5, 2.1, -0.8, 1.5, 0.3, -1.2, 2.8]

rendimiento_acumulado = 0
ganancias = 0
perdidas = 0

for r in rendimientos:
    rendimiento_acumulado += r
    if r > 0:
        ganancias += 1
    else:
        perdidas += 1

promedio = rendimiento_acumulado / len(rendimientos)
print(f"Días totales: {len(rendimientos)}")
print(f"Días positivos: {ganancias} | Días negativos: {perdidas}")
print(f"Rendimiento acumulado: {rendimiento_acumulado:+.2f}%")
print(f"Rendimiento promedio diario: {promedio:+.2f}%")
```

### 2.2 Ejercicio guiado: Proyección de inversión

```python
capital = 10000
tasa_anual = 8
anios = 10

print(f"Año | Capital")
print("-" * 20)
print(f"{0:>3} | ${capital:>10,.2f}")

for anio in range(1, anios + 1):
    capital *= (1 + tasa_anual / 100)
    print(f"{anio:>3} | ${capital:>10,.2f}")
```

### 2.3 Ejercicio guiado: Tabla de amortización

```python
monto = 10000
tasa_anual = 12
plazo_meses = 12

tasa_mensual = (tasa_anual / 100) / 12
cuota = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo_meses) / ((1 + tasa_mensual) ** plazo_meses - 1)

saldo = monto
print(f"Cuota mensual: ${cuota:.2f}")
print(f"\n{'Mes':<5} {'Cuota':<12} {'Interés':<12} {'Capital':<12} {'Saldo':<12}")

for mes in range(1, plazo_meses + 1):
    interes = saldo * tasa_mensual
    capital_pagado = cuota - interes
    saldo -= capital_pagado
    print(f"{mes:<5} ${cuota:<11.2f} ${interes:<11.2f} ${capital_pagado:<11.2f} ${saldo:<11.2f}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Cálculo de beta de una acción

```python
# Rendimientos de la acción y del mercado (simulados)
rendimientos_accion = [1.5, -0.8, 2.1, -1.2, 0.5, 1.8, -0.3, 2.5]
rendimientos_mercado = [1.0, -0.5, 1.8, -0.9, 0.3, 1.2, -0.2, 1.6]

suma_xy = sum(x * y for x, y in zip(rendimientos_accion, rendimientos_mercado))
suma_xx = sum(x * x for x in rendimientos_mercado)
beta = suma_xy / suma_xx
print(f"Beta de la acción: {beta:.2f}")
```

### 3.2 Volatilidad histórica

```python
precios = [100, 102, 101, 105, 103, 108, 110, 107, 112]
rendimientos = []

for i in range(1, len(precios)):
    r = (precios[i] - precios[i-1]) / precios[i-1] * 100
    rendimientos.append(r)

promedio = sum(rendimientos) / len(rendimientos)
suma_cuadrados = sum((r - promedio) ** 2 for r in rendimientos)
volatilidad = (suma_cuadrados / (len(rendimientos) - 1)) ** 0.5
print(f"Volatilidad: {volatilidad:.2f}%")
```

---

## 4. Ejercicios Propuestos

1. **Promedio móvil simple:** Calcula la media móvil de 3 días para una serie de precios.

2. **Calculadora de drawdown:** Encuentra la máxima caída desde un pico en una serie de precios.

3. **Tabla de multiplicar de tasas:** Genera una tabla que muestre cuánto crece $1 a diferentes tasas (5%, 10%, 15%) en 1-10 años.

4. **Conteo de velas:** Clasifica días como "vela verde" (cierre > apertura) o "vela roja" y cuenta cuántos de cada uno.

---

## 5. Resumen

| Función | Uso |
|---------|-----|
| `range(n)` | 0, 1, ..., n-1 |
| `range(a, b)` | a, a+1, ..., b-1 |
| `range(a, b, s)` | a, a+s, ..., hasta b-1 |
| `enumerate(lista)` | (índice, valor) |
| `zip(a, b)` | Emparejar secuencias |
| Acumulador | `total += valor` |

---

## ✅ Autoevaluación

1. ¿Qué imprime `for i in range(3): print(i)`?
2. ¿Qué hace `enumerate()` que no hace un `for` normal?
3. ¿Cómo recorres 10 años del 2024 al 2033 con un `for`?
4. Calcula la suma de todos los múltiplos de 3 menores a 100.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U07.md`: Variantes de range() y funciones enumerate/zip
> - `project-U07.md`: Tabla de amortización y cálculo de beta simplificado
