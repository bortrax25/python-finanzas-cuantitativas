# U08: Bucle while y Control de Flujo

> **Lectura previa:** [U07: Bucle for y range()](./U07-for-range.md)
> **Próxima unidad:** [U09: Bucles for anidados](./U09-for-anidados.md)

---

## 1. Teoría

### 1.1 `while` — Repetir mientras una condición sea verdadera

A diferencia de `for` (que itera sobre una secuencia conocida), `while` repite **mientras** una condición sea `True`.

```python
# Sintaxis
while condicion:
    # código se repite mientras condición sea True

# Ejemplo: cuenta regresiva
contador = 5
while contador > 0:
    print(f"T-{contador}...")
    contador -= 1
print("¡Ejecutado!")
```

> ⚠️ **Cuidado con bucles infinitos:** asegúrate de que la condición eventualmente se vuelva `False`.

### 1.2 `while` vs `for`

| Característica | `for` | `while` |
|---------------|-------|---------|
| Número de iteraciones | Conocido | Desconocido |
| Condición de parada | Fin de secuencia | Expresión booleana |
| Uso típico | Recorrer listas, rangos | Esperar evento, convergencia |

```python
# for: sabes cuántas iteraciones
for mes in range(1, 13):
    print(f"Mes {mes}")

# while: no sabes cuántas iteraciones
saldo = 10000
objetivo = 50000
mes = 0
while saldo < objetivo:
    mes += 1
    saldo *= 1.005
print(f"Se necesitan {mes} meses")
```

### 1.3 `while True` + `break` (menú interactivo)

Patrón para programas que se ejecutan hasta que el usuario decide salir:

```python
while True:
    print("\n--- MENÚ ---")
    print("1. Calcular interés")
    print("2. Convertir moneda")
    print("3. Salir")

    opcion = input("Elige (1-3): ")

    if opcion == "1":
        capital = float(input("Capital: $"))
        tasa = float(input("Tasa anual (%): "))
        tiempo = float(input("Años: "))
        monto = capital * (1 + tasa/100) ** tiempo
        print(f"Monto final: ${monto:,.2f}")
    elif opcion == "2":
        usd = float(input("USD: $"))
        tasa = float(input("Tipo de cambio: "))
        print(f"${usd} → ${usd * tasa:,.2f}")
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida")
```

### 1.4 `continue` en `while`

Saltar iteraciones también funciona en `while`:

```python
# Procesar transacciones saltando montos cero
transacciones = [150, 0, -80, 0, 200, -50]
i = 0
while i < len(transacciones):
    if transacciones[i] == 0:
        i += 1
        continue          # Salta transacciones vacías
    print(f"Transacción {i+1}: ${transacciones[i]:+.0f}")
    i += 1
```

### 1.5 Validación de entrada con `while`

Patrón para forzar al usuario a ingresar datos válidos:

```python
# Pedir un número positivo
while True:
    try:
        edad = int(input("Edad: "))
        if edad > 0:
            break
        print("Error: la edad debe ser positiva")
    except ValueError:
        print("Error: ingresa un número válido")

# Pedir una opción dentro de un rango
while True:
    opcion = input("Riesgo (bajo/medio/alto): ").lower()
    if opcion in ("bajo", "medio", "alto"):
        break
    print("Error: ingresa 'bajo', 'medio' o 'alto'")
```

### 1.6 Convergencia con `while`

En finanzas, muchos cálculos iteran hasta converger (ej: TIR, YTM).

```python
# Aproximar raíz cuadrada (método Newton-Raphson simplificado)
numero = 25
estimacion = numero / 2
tolerancia = 0.0001
iteraciones = 0

while abs(estimacion * estimacion - numero) > tolerancia:
    estimacion = (estimacion + numero / estimacion) / 2
    iteraciones += 1

print(f"√{numero} ≈ {estimacion:.4f} ({iteraciones} iteraciones)")
```

```python
# Encontrar TIR por iteración (método de bisección básico)
flujos = [-1000, 300, 400, 500, 600]  # Inversión, luego retornos
tasa_min = 0.0
tasa_max = 1.0
tolerancia = 0.0001

while (tasa_max - tasa_min) > tolerancia:
    tasa_media = (tasa_min + tasa_max) / 2
    vpn = sum(flujo / (1 + tasa_media) ** t for t, flujo in enumerate(flujos))
    if vpn > 0:
        tasa_min = tasa_media
    else:
        tasa_max = tasa_media

tir = (tasa_min + tasa_max) / 2
print(f"TIR aproximada: {tir:.4%}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Ahorro para la jubilación

```python
capital_actual = float(input("Capital actual: $"))
aporte_mensual = float(input("Aporte mensual: $"))
tasa_anual = float(input("Tasa anual esperada (%): "))
meta = float(input("Meta de jubilación: $"))

tasa_mensual = (tasa_anual / 100) / 12
meses = 0

print(f"\nSimulando... Meta: ${meta:,.2f}")
while capital_actual < meta:
    meses += 1
    capital_actual = capital_actual * (1 + tasa_mensual) + aporte_mensual
    if meses % 12 == 0:
        print(f"Año {meses//12}: ${capital_actual:,.2f}")

anios = meses / 12
print(f"\nMeta alcanzada en {meses} meses ({anios:.1f} años)")
```

### 2.2 Ejercicio guiado: Calculadora de plazo de deuda

```python
# ¿Cuántos meses toma pagar una deuda con cuotas fijas?
deuda = float(input("Deuda total: $"))
cuota = float(input("Cuota mensual: $"))
tasa_anual = float(input("Tasa anual (%): "))
tasa_mensual = (tasa_anual / 100) / 12

mes = 0
while deuda > 0:
    mes += 1
    interes = deuda * tasa_mensual
    pago_capital = min(cuota - interes, deuda)
    if pago_capital <= 0:
        print(f"⚠️ La cuota no cubre ni el interés en el mes {mes}")
        print(f"Interés mensual: ${interes:.2f} > Cuota: ${cuota:.2f}")
        break
    deuda -= pago_capital
    print(f"Mes {mes}: Interés ${interes:.2f} | Capital ${pago_capital:.2f} | Saldo ${deuda:.2f}")
else:
    print(f"\nDeuda pagada en {mes} meses")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Simulación de Monte Carlo (versión introductoria)

```python
import random

capital_inicial = 10000
tasa_anual = 8
volatilidad = 15
anios = 10
simulaciones = 5

print("Simulando escenarios...")
for sim in range(simulaciones):
    capital = capital_inicial
    for _ in range(anios):
        rendimiento = random.gauss(tasa_anual, volatilidad) / 100
        capital *= (1 + rendimiento)
    print(f"Escenario {sim+1}: ${capital:,.2f}")
```

> 💡 `random.gauss(media, desviacion)` genera un número aleatorio con distribución normal.

### 3.2 Años para duplicar (Regla del 72 exacta)

```python
capital = 1000
tasa_anual = 7
objetivo = capital * 2
anios = 0

while capital < objetivo:
    anios += 1
    capital *= (1 + tasa_anual / 100)

print(f"Capital duplicado en {anios} años (exacto)")
print(f"Regla del 72: ~{72/tasa_anual:.1f} años (aproximado)")
```

---

## 4. Ejercicios Propuestos

1. **Simulador de ruina del jugador:** Empiezas con $1,000. Cada "trade" ganas o pierdes 10% con 50% de probabilidad. Simula hasta duplicar o perder todo.

2. **Calculadora de intereses de tarjeta de crédito:** Dada una deuda, pago mínimo (3%) y tasa (24% anual), calcula cuántos meses toma pagar.

3. **Validador de menú interactivo:** Crea un menú con 4 opciones financieras. Valida que la opción ingresada sea válida y permite salir.

4. **Convergencia de cuota:** Encuentra la cuota mensual exacta para pagar un préstamo en N meses usando bisección con `while`.

---

## 5. Resumen

| Patrón | Uso |
|--------|-----|
| `while condicion:` | Repetir mientras se cumpla |
| `while True:` + `break` | Menú interactivo |
| `while` + validación | Forzar entrada válida |
| `while` + convergencia | Métodos iterativos financieros |
| `for` | Número conocido de iteraciones |

---

## ✅ Autoevaluación

1. ¿Cuándo usas `while` en vez de `for`?
2. ¿Qué pasa si escribes `while True:` sin un `break` dentro?
3. ¿Cómo validas que un usuario ingrese un número positivo?
4. Escribe un `while` que calcule cuántos años toma triplicar un capital al 6% anual.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U08.md`: Patrones while: menú, validación, convergencia
> - `project-U08.md`: Simulador de jubilación y calculadora de plazo de deuda
