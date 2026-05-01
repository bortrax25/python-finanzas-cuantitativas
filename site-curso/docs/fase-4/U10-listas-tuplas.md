# U10: Listas y Tuplas

> **Lectura previa:** [U09: Bucles for anidados](../fase-3/U09-for-anidados.md)
> **Próxima unidad:** [U11: Diccionarios y conjuntos](./U11-diccionarios-sets.md)

---

## 1. Teoría

### 1.1 Listas — Colecciones ordenadas y mutables

Una **lista** es una colección de elementos ordenados, modificables y que permiten duplicados.

```python
# Creación
acciones = ["AAPL", "MSFT", "TSLA"]
precios = [150.25, 280.50, 900.00]
mixta = ["AAPL", 150, True]

# Acceso por índice (base 0)
print(acciones[0])       # AAPL
print(acciones[-1])      # TSLA (último)
print(acciones[1:3])     # ['MSFT', 'TSLA'] (slice)
```

### 1.2 Operaciones con listas

| Operación | Ejemplo | Resultado |
|-----------|---------|-----------|
| `append(x)` | `lista.append(4)` | Agrega al final |
| `insert(i, x)` | `lista.insert(1, 5)` | Inserta en posición i |
| `remove(x)` | `lista.remove(5)` | Elimina primera ocurrencia |
| `pop(i)` | `lista.pop()` | Elimina y retorna último |
| `len(lista)` | `len([1,2,3])` | `3` |
| `sort()` | `lista.sort()` | Ordena in-place |
| `reverse()` | `lista.reverse()` | Invierte in-place |

```python
portafolio = ["AAPL", "MSFT"]
portafolio.append("TSLA")       # ["AAPL", "MSFT", "TSLA"]
portafolio.insert(0, "GOOGL")   # ["GOOGL", "AAPL", "MSFT", "TSLA"]
portafolio.remove("MSFT")       # ["GOOGL", "AAPL", "TSLA"]
ultimo = portafolio.pop()        # "TSLA", lista queda ["GOOGL", "AAPL"]
print(len(portafolio))          # 2
```

### 1.3 Slicing de listas

```python
precios = [100, 102, 105, 108, 110, 107, 112]

# Sintaxis: lista[inicio:fin:paso]
precios[0:3]     # [100, 102, 105] — primeros 3
precios[:3]      # [100, 102, 105] — desde el inicio
precios[3:]      # [108, 110, 107, 112] — desde 3 al final
precios[-3:]     # [110, 107, 112] — últimos 3
precios[::2]     # [100, 105, 110, 112] — cada 2
precios[::-1]    # [112, 107, 110, 108, 105, 102, 100] — invertida
```

### 1.4 List comprehension

Sintaxis compacta para crear listas:

```python
# Tradicional
cuadrados = []
for i in range(5):
    cuadrados.append(i ** 2)

# List comprehension
cuadrados = [i ** 2 for i in range(5)]        # [0, 1, 4, 9, 16]

# Con filtro
pares = [i for i in range(10) if i % 2 == 0]   # [0, 2, 4, 6, 8]

# Con transformación
rendimientos = [1.2, -0.5, 2.1, -0.8, 0.3]
positivos = [r for r in rendimientos if r > 0]  # [1.2, 2.1, 0.3]
```

### 1.5 Tuplas — Colecciones inmutables

Las tuplas son como listas pero **no se pueden modificar** después de creadas.

```python
# Creación
coordenadas = (10, 20)
punto = 150, 200        # Los paréntesis son opcionales
vacia = ()
un_elemento = (42,)     # ¡La coma es necesaria!

# Acceso (igual que listas)
print(coordenadas[0])   # 10

# Inmutabilidad
# coordenadas[0] = 5    # ❌ TypeError: 'tuple' object does not support item assignment
```

**¿Cuándo usar tuplas?**
- Datos que no deben cambiar (ej: configuración)
- Claves de diccionarios (las listas no pueden ser claves)
- Retorno de múltiples valores en funciones

```python
# Datos de un activo que no cambian
activo = ("AAPL", "Tecnología", "NASDAQ")

# Desempaquetado
ticker, sector, mercado = activo
```

### 1.6 Funciones útiles con listas y tuplas

```python
numeros = [3, 1, 4, 1, 5, 9]

sum(numeros)           # 23
max(numeros)           # 9
min(numeros)           # 1
sorted(numeros)        # [1, 1, 3, 4, 5, 9] — nuevo
list(reversed(numeros))# [9, 5, 1, 4, 1, 3]
any([False, True])     # True (al menos uno)
all([True, True])      # True (todos)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Gestor de portafolio con listas

```python
portafolio = []

# Agregar posiciones
portafolio.append(("AAPL", 10, 150.00))
portafolio.append(("MSFT", 5, 280.00))
portafolio.append(("TSLA", 3, 900.00))

# Calcular valor total
valor_total = 0
for ticker, cantidad, precio in portafolio:
    valor_posicion = cantidad * precio
    valor_total += valor_posicion
    print(f"{ticker}: {cantidad} × ${precio} = ${valor_posicion:,.2f}")

print(f"Valor total: ${valor_total:,.2f}")

# Encontrar posición más valiosa
max_valor = 0
max_ticker = ""
for ticker, cantidad, precio in portafolio:
    valor = cantidad * precio
    if valor > max_valor:
        max_valor = valor
        max_ticker = ticker
print(f"Mayor posición: {max_ticker} (${max_valor:,.2f})")

# Usando list comprehension + max
valores = [cant * prec for _, cant, prec in portafolio]
print(f"Posiciones: {valores}")
```

### 2.2 Ejercicio guiado: Rentabilidades con list comprehension

```python
compras = [
    ("AAPL", 150, 175),
    ("MSFT", 280, 310),
    ("TSLA", 900, 820),
]

# Calcular rentabilidad de cada posición
rentabilidades = [(ticker, (vta - cmp) / cmp * 100)
                  for ticker, cmp, vta in compras]

for ticker, rent in rentabilidades:
    print(f"{ticker}: {rent:+.2f}%")

# Filtrar solo las ganadoras
ganadoras = [t for t, r in rentabilidades if r > 0]
print(f"Ganadoras: {ganadoras}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Precios históricos y retornos diarios

```python
precios_aapl = [150, 152, 149, 153, 155, 158, 156, 160]

# Calcular retornos diarios con slicing
retornos = [(precios_aapl[i] - precios_aapl[i-1]) / precios_aapl[i-1] * 100
            for i in range(1, len(precios_aapl))]

print("Retornos diarios:")
for dia, r in enumerate(retornos, start=2):
    print(f"Día {dia}: {r:+.2f}%")
```

### 3.2 Cesta de monedas

```python
# Datos: (moneda, tasa vs USD, peso en portafolio)
cesta = [
    ("EUR", 0.92, 0.40),
    ("GBP", 0.79, 0.25),
    ("JPY", 150.50, 0.20),
    ("CHF", 0.90, 0.15),
]

# Valor de la cesta en USD (asumiendo 100,000 USD)
inversion = 100000
for moneda, tasa, peso in cesta:
    monto_usd = inversion * peso
    monto_moneda = monto_usd * tasa
    print(f"{moneda}: ${monto_usd:,.2f} → {monto_moneda:,.2f} {moneda}")
```

---

## 4. Ejercicios Propuestos

1. **Rastreador de portafolio:** Mantén una lista de (ticker, cantidad, precio_compra). Implementa agregar, eliminar y calcular P&L total.

2. **Filtro de oportunidades:** Dada una lista de (ticker, PER, crecimiento), filtra las que tienen PER < 15 y crecimiento > 10% usando list comprehension.

3. **Media móvil con slicing:** Calcula SMA de 5 días usando slicing y list comprehension.

4. **Rebalanceo de portafolio:** Simula el rebalanceo trimestral de un portafolio de 3 activos para mantener pesos objetivo.

---

## 5. Resumen

| Característica | Lista | Tupla |
|---------------|-------|-------|
| Sintaxis | `[1, 2, 3]` | `(1, 2, 3)` |
| Mutable | Sí | No |
| Métodos | append, pop, sort... | count, index |
| Uso | Datos que cambian | Datos fijos, claves |

---

## ✅ Autoevaluación

1. ¿Cómo agregas un elemento al final de una lista?
2. ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)`?
3. ¿Por qué usarías una tupla en vez de una lista?
4. Crea con list comprehension una lista de los cuadrados de los números del 1 al 10 que sean pares.

---

> 📝 **Knowledge Wiki:** Guarda `reference-U10.md` (slicing, list comprehension) y `project-U10.md` (gestor de portafolio).
