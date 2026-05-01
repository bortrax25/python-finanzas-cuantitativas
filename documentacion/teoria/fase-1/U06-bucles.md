# U06: Bucles — Iterando sobre Series de Tiempo

> **Lectura previa:** [U05: Condicionales](./U05-condicionales.md)
> **Próxima unidad:** [U07: Listas y Tuplas — Series de Precios](../fase-2/U07-listas-tuplas.md)

---

## 1. Teoría

### 1.1 Bucle `for` — Iterar sobre secuencias

```python
acciones = ["AAPL", "MSFT", "TSLA"]
for ticker in acciones:
    print(f"Analizando {ticker}")
```

### 1.2 `range()` — Generador de secuencias numéricas

| Forma | Descripción | Secuencia |
|-------|------------|-----------|
| `range(n)` | 0 a n-1 | `0, 1, ..., n-1` |
| `range(inicio, fin)` | inicio a fin-1 | `inicio, ..., fin-1` |
| `range(inicio, fin, paso)` | con paso | inicio, inicio+paso, ... |

```python
for i in range(5):          # 0 1 2 3 4
    print(i, end=" ")

for i in range(1, 6):       # 1 2 3 4 5
    print(i, end=" ")

for i in range(5, 0, -1):   # 5 4 3 2 1 (cuenta regresiva)
    print(i, end=" ")
```

### 1.3 `enumerate()` y `zip()`

```python
# enumerate: índice + valor
acciones = ["AAPL", "MSFT", "TSLA"]
for dia, ticker in enumerate(acciones, start=1):
    print(f"Día {dia}: {ticker}")

# zip: emparejar secuencias
precios = [150, 280, 900]
cantidades = [10, 5, 3]
for ticker, precio, cantidad in zip(acciones, precios, cantidades):
    valor = precio * cantidad
    print(f"{ticker}: {cantidad} × ${precio} = ${valor:,.2f}")
```

### 1.4 `while` — Repetir mientras condición sea True

```python
# Años para duplicar capital
capital = 10000
meta = 20000
tasa = 0.08
anios = 0

while capital < meta:
    anios += 1
    capital *= (1 + tasa)

print(f"Duplicado en {anios} años (exacto)")
print(f"Regla del 72: ~{72/8:.1f} años (aproximado)")
```

### 1.5 `while True` + `break` — Menú interactivo

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
        print(f"${usd} → S/ {usd * tasa:,.2f}")
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida")
```

### 1.6 `break`, `continue`, `pass`

| Comando | Efecto | Cuándo usarlo |
|---------|--------|--------------|
| `break` | Detiene el bucle | Encontraste lo que buscabas |
| `continue` | Salta a siguiente iteración | Ignorar ciertos casos |
| `pass` | No hace nada | Placeholder |

```python
# break: buscar primera acción rentable
rendimientos = [-2.1, 3.5, -0.8, 5.2, -1.3]
for i, r in enumerate(rendimientos):
    if r > 0:
        print(f"Primera rentable: índice {i}, rendimiento {r}%")
        break

# continue: procesar solo ganancias
resultados = [150, -80, 200, -50, 300]
total = 0
for resultado in resultados:
    if resultado < 0:
        continue
    total += resultado
print(f"Total ganancias: ${total}")

# pass: función pendiente
def calcular_var():
    pass    # "Lo implementaré después"
```

### 1.7 `else` en bucles

```python
# for...else: se ejecuta si NO hubo break
precios = [95, 88, 102, 97]
limite = 100
for precio in precios:
    if precio < limite:
        print(f"Oportunidad: ${precio}")
        break
else:
    print("Ningún activo por debajo del límite")
```

### 1.8 Bucles anidados y matrices

```python
# Matriz: filas = activos, columnas = días
precios = [
    [150, 152, 149, 153, 155],   # AAPL
    [280, 282, 279, 285, 290],   # MSFT
]

# Búsqueda 2D: encontrar precio máximo
max_precio = 0
activo_max = dia_max = -1
activos = ["AAPL", "MSFT"]

for i, fila in enumerate(precios):
    for j, precio in enumerate(fila):
        if precio > max_precio:
            max_precio = precio
            activo_max = i
            dia_max = j

print(f"Precio máximo: ${max_precio} ({activos[activo_max]}, día {dia_max + 1})")
```

### 1.9 List comprehensions

```python
# Tradicional
cuadrados = []
for i in range(10):
    cuadrados.append(i ** 2)

# List comprehension (más rápido y compacto)
cuadrados = [i ** 2 for i in range(10)]

# Con filtro
pares = [i for i in range(20) if i % 2 == 0]

# Con transformación financiera
rendimientos = [1.2, -0.5, 2.1, -0.8, 0.3]
positivos = [r for r in rendimientos if r > 0]
absolutos = [abs(r) for r in rendimientos]

# Anidada
matriz_3x3 = [[i * 3 + j for j in range(3)] for i in range(3)]
```

### 1.10 Validación de entrada con `while`

```python
# Pedir número positivo
while True:
    try:
        valor = float(input("Monto: $"))
        if valor > 0:
            break
        print("Error: debe ser positivo")
    except ValueError:
        print("Error: ingresa un número válido")

# Pedir opción dentro de un rango
while True:
    opcion = input("Riesgo (bajo/medio/alto): ").lower()
    if opcion in ("bajo", "medio", "alto"):
        break
    print("Error: opción inválida")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: SMA 20 y SMA 50 + Golden/Death Cross

```python
# Serie de precios (50 días simulados)
import random
random.seed(42)
precio = 100
precios = [precio]
for _ in range(49):
    precio *= (1 + random.gauss(0.0005, 0.015))
    precios.append(precio)

# Calcular SMA 20 y SMA 50
sma20 = []
sma50 = []

for i in range(len(precios)):
    if i >= 19:
        sma20.append(sum(precios[i-19:i+1]) / 20)
    else:
        sma20.append(None)

    if i >= 49:
        sma50.append(sum(precios[i-49:i+1]) / 50)
    else:
        sma50.append(None)

# Detectar cruces (desde que ambas SMAs existen, día 49 en adelante)
for dia in range(49, len(precios)):
    if sma20[dia] is None or sma50[dia] is None:
        continue
    if sma20[dia-1] <= sma50[dia-1] and sma20[dia] > sma50[dia]:
        print(f"Día {dia+1}: GOLDEN CROSS (COMPRA) | ${precios[dia]:.2f}")
    elif sma20[dia-1] >= sma50[dia-1] and sma20[dia] < sma50[dia]:
        print(f"Día {dia+1}: DEATH CROSS (VENTA) | ${precios[dia]:.2f}")
```

### 2.2 Ejercicio guiado: TIR por bisección

**Concepto financiero:** La TIR (Tasa Interna de Retorno) es la tasa que hace el VPN = 0.

```python
# Flujos: inversión inicial negativa, luego retornos positivos
flujos = [-1000, 300, 400, 500, 600]

print("Cálculo de TIR por bisección:")
print(f"Flujos: {flujos}")

tasa_min = 0.0
tasa_max = 1.0     # 100% (límite superior)
tolerancia = 0.0001

while (tasa_max - tasa_min) > tolerancia:
    tasa_media = (tasa_min + tasa_max) / 2
    vpn = sum(flujo / (1 + tasa_media) ** t for t, flujo in enumerate(flujos))
    if vpn > 0:
        tasa_min = tasa_media
    else:
        tasa_max = tasa_media

tir = (tasa_min + tasa_max) / 2
print(f"TIR: {tir:.4%}")

# Validación
vpn_final = sum(flujo / (1 + tir) ** t for t, flujo in enumerate(flujos))
print(f"VPN a la TIR: ${vpn_final:,.2f} (debe ser ≈ $0)")
```

### 2.3 Ejercicio guiado: Ahorro para la jubilación con while

```python
capital = 10000
aporte_mensual = 500
tasa_anual = 8
meta = 100000

tasa_mensual = (tasa_anual / 100) / 12
meses = 0

while capital < meta:
    meses += 1
    capital = capital * (1 + tasa_mensual) + aporte_mensual
    if meses % 12 == 0:
        print(f"Año {meses//12}: ${capital:,.2f}")

anios = meses / 12
print(f"\nMeta de ${meta:,.0f} alcanzada en {meses} meses ({anios:.1f} años)")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Payback (período de recuperación)

```python
inversion = 50000
flujos = [12000, 15000, 18000, 20000, 22000]

acumulado = 0
for i, flujo in enumerate(flujos, start=1):
    acumulado += flujo
    pendiente = inversion - acumulado
    print(f"Año {i}: Flujo ${flujo:,} | Acum ${acumulado:,} | Pend ${pendiente:,}")
    if acumulado >= inversion:
        print(f"Payback alcanzado en año {i}")
        break
```

### 3.2 Optimización de portafolio por grilla

```python
# 2 activos: buscamos la combinación que maximiza Sharpe
ret_a, vol_a = 12, 18    # %
ret_b, vol_b = 8, 10
corr = 0.3
rf = 4  # tasa libre de riesgo

mejor_sharpe = -1
mejor_w = 0

for w in range(0, 101):
    wa = w / 100
    wb = 1 - wa
    rp = wa * ret_a + wb * ret_b
    var = (wa * vol_a) ** 2 + (wb * vol_b) ** 2 + 2 * wa * wb * corr * vol_a * vol_b
    riesgo = var ** 0.5
    sharpe = (rp - rf) / riesgo
    if sharpe > mejor_sharpe:
        mejor_sharpe = sharpe
        mejor_w = w

print(f"Mejor asignación: {mejor_w}% A, {100-mejor_w}% B")
print(f"Sharpe máximo: {mejor_sharpe:.2f}")
```

### 3.3 Stop-loss dinámico con break

```python
precio_entrada = 100.00
stop_pct = 5
take_pct = 10

precio_stop = precio_entrada * (1 - stop_pct / 100)
precio_take = precio_entrada * (1 + take_pct / 100)
precios_diarios = [102, 104, 99, 97, 105, 112, 94, 108]

for dia, precio in enumerate(precios_diarios, start=1):
    if precio <= precio_stop:
        print(f"Día {dia}: ${precio} → STOP-LOSS ACTIVADO")
        break
    elif precio >= precio_take:
        print(f"Día {dia}: ${precio} → TAKE-PROFIT ACTIVADO")
        break
    print(f"Día {dia}: ${precio} — manteniendo")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-1/U06_ejercicios.py`

1. **SMA 20 y cruce de medias:** Calcula SMA 20 y SMA 50 para una lista de 60 precios. Detecta cruces dorados y de muerte.

2. **TIR por bisección:** Encuentra la TIR de los flujos [-2000, 600, 700, 800, 900] usando bisección con while.

3. **Simulador de ruina del jugador:** Empiezas con $1,000. Cada trade ganas o pierdes $100 (50/50). Simula hasta $2,000 o $0.

4. **Máximo drawdown con for:** Encuentra la máxima caída desde un pico en una serie de precios.

---

## 5. Resumen

| Herramienta | Uso principal |
|------------|--------------|
| `for item in secuencia:` | Recorrer listas, rangos |
| `range(n)`, `range(a,b,s)` | Secuencias numéricas |
| `while condicion:` | Iterar hasta que se cumpla condición |
| `while True:` + `break` | Menú interactivo |
| `break` | Detener bucle |
| `continue` | Saltar iteración |
| `pass` | Placeholder |
| `for...else` | Código si no hubo break |
| Bucles anidados | Matrices, grillas, tablas |
| `[expr for x in seq if cond]` | List comprehension |

---

## ✅ Autoevaluación

1. ¿Cuándo usas `while` en vez de `for`?
2. ¿Qué imprime `for i in range(3): print(i)`?
3. ¿Qué hace `break` en un bucle anidado?
4. ¿Qué patrón usas para un menú interactivo?
5. Calcula el SMA de 3 días para [100, 102, 101, 105, 103].

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U06.md`: range(), enumerate(), zip(), break/continue/pass, list comprehensions
> - `project-U06.md`: SMA + cruces, TIR por bisección, optimización por grilla
