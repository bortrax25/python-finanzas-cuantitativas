# U04: Estructuras de Control — break, continue, pass

> **Lectura previa:** [U03: Entrada, salida y debugging](./U03-entrada-salida.md)
> **Próxima unidad:** [U05: Condicionales if/elif/else](../fase-2/U05-condicionales-if.md)

---

## 1. Teoría

### 1.1 `break` — Interrumpir un bucle

`break` detiene la ejecución del bucle **por completo**, sin importar si quedaban iteraciones pendientes.

```python
# Sin break: itera todos los elementos
for i in range(10):
    print(i, end=" ")          # 0 1 2 3 4 5 6 7 8 9

# Con break: se detiene al cumplir la condición
for i in range(10):
    if i == 5:
        break                   # Se detiene cuando i = 5
    print(i, end=" ")           # 0 1 2 3 4
```

**Analogía financiera:** Buscar la primera acción rentable en una lista y detenerse al encontrarla.

```python
rendimientos = [-2.1, 3.5, -0.8, 5.2, -1.3, 7.8]

print("Buscando primera acción rentable...")
for rendimiento in rendimientos:
    if rendimiento > 0:
        print(f"¡Encontrada! Rendimiento: {rendimiento}%")
        break
    print(f"  {rendimiento}% — no rentable")
```

### 1.2 `continue` — Saltar a la siguiente iteración

`continue` omite el resto del código de la iteración actual y **pasa a la siguiente** iteración del bucle.

```python
# Sin continue
for i in range(1, 6):
    print(i, end=" ")          # 1 2 3 4 5

# Con continue: salta los pares
for i in range(1, 6):
    if i % 2 == 0:
        continue                # Salta números pares
    print(i, end=" ")           # 1 3 5
```

**Analogía financiera:** Procesar solo los días con ganancias, ignorando pérdidas.

```python
resultados_diarios = [150, -80, 200, -50, 300, -120]
total_ganancias = 0

for resultado in resultados_diarios:
    if resultado < 0:
        continue                # Ignora pérdidas
    total_ganancias += resultado

print(f"Total ganancias: ${total_ganancias}")     # $650
```

### 1.3 `pass` — Marcador de posición

`pass` no hace nada. Se usa como **placeholder** para código que escribirás después.

```python
# Sin pass: SyntaxError
# def calcular_riesgo():
#                      ← vacío, error de sintaxis

# Con pass: código válido (pendiente de implementar)
def calcular_riesgo():
    pass                    # "Después escribo esto"

# También en condicionales
if condicion:
    pass                    # "Ya lo implementaré"
else:
    print("Caso manejado")
```

### 1.4 Comparativa visual

```python
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# break: se detiene en el 5
print("break:")
for n in numeros:
    if n == 5:
        break
    print(n, end=" ")        # 1 2 3 4
print()

# continue: salta el 5
print("continue:")
for n in numeros:
    if n == 5:
        continue
    print(n, end=" ")        # 1 2 3 4 6 7 8 9 10
print()

# pass: no hace nada, imprime todo
print("pass:")
for n in numeros:
    if n == 5:
        pass
    print(n, end=" ")        # 1 2 3 4 5 6 7 8 9 10
```

### 1.5 Combinando `break` y `continue`

Ambos funcionan en `for` y `while`:

```python
# for con break y continue
precios = [100, 0, 150, -1, 200, 0, 175]

for precio in precios:
    if precio == 0:
        continue             # Salta datos inválidos
    if precio < 0:
        break                 # Se detiene al encontrar precio negativo
    print(f"Procesando: ${precio}")
    # Procesando: $100
    # Procesando: $150
```

### 1.6 `while True` + `break` (bucle infinito controlado)

Un patrón muy común: bucle que se ejecuta hasta que el usuario decide salir.

```python
# Calculadora financiera interactiva
while True:
    monto = float(input("\nMonto ($): "))
    tasa = float(input("Tasa anual (%): "))
    tiempo = float(input("Años: "))

    monto_final = monto * (1 + tasa/100) ** tiempo
    print(f"Monto final: ${monto_final:,.2f}")

    continuar = input("¿Otro cálculo? (s/n): ").lower()
    if continuar != 's':
        print("¡Hasta luego!")
        break
```

### 1.7 `else` en bucles (poco conocido pero útil)

En Python, `for` y `while` pueden tener `else`. Se ejecuta si el bucle terminó **sin `break`**.

```python
# Buscar un activo que cumpla el criterio
precios_objetivo = [95, 88, 102, 97]
precio_limite = 100

for precio in precios_objetivo:
    if precio < precio_limite:
        print(f"Oportunidad encontrada: ${precio}")
        break
else:
    print("Ningún activo por debajo del límite")

# Si se encuentra → imprime y break
# Si no se encuentra → el else se ejecuta
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Stop-loss dinámico

```python
# Simulación: monitorear precio con stop-loss y take-profit
precio_entrada = 100.00
stop_loss_pct = 5     # -5%
take_profit_pct = 10  # +10%

precio_stop = precio_entrada * (1 - stop_loss_pct/100)   # $95.00
precio_take = precio_entrada * (1 + take_profit_pct/100) # $110.00

# Simular precios diarios
precios_diarios = [102, 104, 99, 97, 105, 112, 94, 108]
print(f"Precio entrada: ${precio_entrada}")
print(f"Stop-loss: ${precio_stop} | Take-profit: ${precio_take}")
print()

for dia, precio in enumerate(precios_diarios, start=1):
    if precio <= precio_stop:
        perdida_pct = (precio - precio_entrada) / precio_entrada * 100
        print(f"Día {dia}: ${precio} → STOP-LOSS ACTIVADO ({perdida_pct:+.1f}%)")
        break
    if precio >= precio_take:
        ganancia_pct = (precio - precio_entrada) / precio_entrada * 100
        print(f"Día {dia}: ${precio} → TAKE-PROFIT ACTIVADO ({ganancia_pct:+.1f}%)")
        break
    print(f"Día {dia}: ${precio} — manteniendo posición")
```

### 2.2 Ejercicio guiado: Filtrar datos del mercado

```python
# Datos de acciones: (ticker, sector, rendimiento_ytd)
acciones = [
    ("AAPL", "Tecnología", 15.2),
    ("XOM", "Energía", -3.1),
    ("JPM", "Finanzas", 8.7),
    ("TSLA", "Automotriz", -12.5),
    ("MSFT", "Tecnología", 22.1),
    ("CVX", "Energía", 5.3)
]

print("=== Análisis sector Tecnología ===")
for ticker, sector, rendimiento in acciones:
    if sector != "Tecnología":
        continue        # Solo nos interesa tecnología
    if rendimiento < 0:
        print(f"{ticker}: {rendimiento}% ⚠️")
        continue
    print(f"{ticker}: {rendimiento}% ✅")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Interés compuesto con capitalización

```python
# ¿Cuántos años toma duplicar el capital a una tasa dada?
capital_inicial = 10000
tasa_anual = 8
objetivo = capital_inicial * 2

capital = capital_inicial
anio = 0

while True:
    anio += 1
    capital *= (1 + tasa_anual/100)
    print(f"Año {anio}: ${capital:,.2f}")
    if capital >= objetivo:
        break

print(f"Capital duplicado en {anio} años al {tasa_anual}% anual")
```

### 3.2 Regla del 72 (aproximación)

```python
# La Regla del 72 estima años para duplicar: 72 / tasa
# Validemos contra varias tasas

for tasa in [4, 6, 8, 10, 12]:
    if tasa <= 0:
        continue
    estimacion = 72 / tasa
    print(f"Tasa {tasa}% → duplicar en ~{estimacion:.1f} años (Regla del 72)")
```

---

## 4. Ejercicios Propuestos

1. **Cazador de gangas:** Recorres una lista de precios de acciones. Imprimes solo las que están por debajo de tu precio objetivo. Usa `continue` para saltar las demás.

2. **Simulador de ahorro:** Empiezas con $1,000 y ahorras $200 al mes. Usa `while True` para calcular cuántos meses necesitas para llegar a $10,000 con una tasa mensual del 0.5%.

3. **Validador de tickers:** Dada una lista de tickers, verifica que sean válidos (3-5 letras, todo mayúsculas). Usa `continue` para saltar inválidos y `break` si encuentras un ticker vacío.

4. **Cálculo de período de recuperación (payback):** Inviertes $50,000 en un proyecto que genera flujos anuales. Calcula en qué año recuperas tu inversión.

---

## 5. Resumen

| Comando | Efecto | Cuándo usarlo |
|---------|--------|--------------|
| `break` | Detiene el bucle por completo | Encontraste lo que buscabas |
| `continue` | Salta a la siguiente iteración | Ignorar ciertos casos |
| `pass` | No hace nada | Placeholder para código futuro |
| `while True` + `break` | Bucle hasta condición externa | Menús interactivos |
| `for...else` | Se ejecuta si no hubo `break` | Búsqueda sin resultado |

---

## ✅ Autoevaluación

1. ¿Qué imprime esto?
```python
for i in range(5):
    if i == 2:
        break
    print(i, end=" ")
```

2. ¿Qué imprime esto?
```python
for i in range(5):
    if i == 2:
        continue
    print(i, end=" ")
```

3. ¿Cuándo se ejecuta el `else` de un bucle `for`?

4. Escribe un programa que pida números al usuario indefinidamente (`while True`) y termine cuando ingrese 0. Muestra la suma y el promedio de los números ingresados (excluyendo el 0).

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U04.md`: Patrón `while True` + `break` y tabla comparativa break/continue/pass
> - `project-U04.md`: Stop-loss dinámico y regla del 72
