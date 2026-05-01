# U07: Listas y Tuplas — Series de Precios y Registros Financieros

> **Lectura previa:** [U06: Bucles — Iterando sobre Series de Tiempo](../fase-1/U06-bucles.md)
> **Próxima unidad:** [U08: Diccionarios — Portafolios y Datos Estructurados](./U08-diccionarios.md)

---

## 1. Teoría

### 1.1 Listas — Colecciones ordenadas y mutables

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

| Método | Descripción | Ejemplo |
|--------|------------|---------|
| `append(x)` | Agrega al final | `lista.append(4)` |
| `insert(i, x)` | Inserta en posición i | `lista.insert(1, 5)` |
| `remove(x)` | Elimina primera ocurrencia | `lista.remove(5)` |
| `pop(i)` | Elimina y retorna | `lista.pop()` |
| `len(lista)` | Longitud | `len([1,2,3])` → `3` |
| `sort()` | Ordena in-place | `lista.sort()` |
| `reverse()` | Invierte in-place | `lista.reverse()` |
| `index(x)` | Posición de primera ocurrencia | `lista.index(5)` |
| `count(x)` | Número de ocurrencias | `lista.count(5)` |

```python
portafolio = ["AAPL", "MSFT"]
portafolio.append("TSLA")       # ["AAPL", "MSFT", "TSLA"]
portafolio.insert(0, "GOOGL")   # ["GOOGL", "AAPL", "MSFT", "TSLA"]
portafolio.remove("MSFT")       # ["GOOGL", "AAPL", "TSLA"]
ultimo = portafolio.pop()        # "TSLA"
```

### 1.3 Slicing de listas

```python
precios = [100, 102, 105, 108, 110, 107, 112]

precios[0:3]     # [100, 102, 105] — primeros 3
precios[:3]      # [100, 102, 105]
precios[3:]      # [108, 110, 107, 112]
precios[-3:]     # [110, 107, 112] — últimos 3
precios[::2]     # [100, 105, 110, 112] — cada 2
precios[::-1]    # [112, 107, 110, ...] — invertida
```

### 1.4 Datos OHLCV como tuplas

En finanzas, los datos OHLCV (Open, High, Low, Close, Volume) son perfectos para tuplas por su inmutabilidad:

```python
# Cada día es una tupla inmutable (fecha, open, high, low, close, volume)
datos_aapl = [
    ("2024-01-02", 185.50, 186.75, 184.20, 185.90, 45230100),
    ("2024-01-03", 185.90, 187.10, 185.00, 186.50, 38920500),
    ("2024-01-04", 186.50, 187.80, 185.50, 187.20, 42100800),
]

for fecha, apertura, maximo, minimo, cierre, volumen in datos_aapl:
    rango = maximo - minimo
    print(f"{fecha}: Cierre ${cierre:.2f} | Rango ${rango:.2f} | Vol {volumen:,}")
```

### 1.5 Tuplas — Colecciones inmutables

```python
# Creación
coordenadas = (10, 20)
punto = 150, 200        # Paréntesis opcionales
un_elemento = (42,)     # ¡La coma es necesaria!

# Acceso (igual que listas)
print(coordenadas[0])   # 10

# Inmutabilidad
# coordenadas[0] = 5    # TypeError: 'tuple' no soporta asignación

# Desempaquetado
ticker, sector, mercado = ("AAPL", "Tecnología", "NASDAQ")
```

**¿Cuándo usar tuplas?** Datos que no deben cambiar: registros OHLCV, claves de diccionarios, retornos múltiples.

### 1.6 Rolling windows manuales

Antes de usar pandas, entiende cómo funcionan las ventanas móviles:

```python
precios = [100, 102, 101, 105, 103, 108, 110, 107, 112, 115]
ventana = 3

sma = []
for i in range(len(precios) - ventana + 1):
    promedio = sum(precios[i:i+ventana]) / ventana
    sma.append(promedio)
    print(f"Días {i+1}-{i+ventana}: SMA = {promedio:.2f}")

# Misma operación con list comprehension
sma_comp = [sum(precios[i:i+3])/3 for i in range(len(precios)-2)]
```

### 1.7 Funciones built-in sobre secuencias

```python
numeros = [3, 1, 4, 1, 5, 9]

sum(numeros)            # 23
max(numeros)            # 9
min(numeros)            # 1
sorted(numeros)         # [1, 1, 3, 4, 5, 9] — nuevo, no modifica
sorted(numeros, reverse=True)  # [9, 5, 4, 3, 1, 1]
any([False, True])      # True (al menos uno True)
all([True, True])       # True (todos True)
list(reversed(numeros)) # [9, 5, 1, 4, 1, 3]
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Gestor de portafolio con listas

```python
portafolio = [
    ("AAPL", 10, 150.00),
    ("MSFT", 5, 280.00),
    ("TSLA", 3, 900.00),
]
precios_actuales = {"AAPL": 175.00, "MSFT": 310.00, "TSLA": 820.00}

pl_total = 0
for ticker, cantidad, precio_compra in portafolio:
    precio_actual = precios_actuales[ticker]
    valor_compra = cantidad * precio_compra
    valor_actual = cantidad * precio_actual
    pl = valor_actual - valor_compra
    pl_pct = (pl / valor_compra) * 100
    pl_total += pl
    print(f"{ticker}: {cantidad} × ${precio_compra:.2f} → ${precio_actual:.2f} | P&L: ${pl:+,.2f} ({pl_pct:+.2f}%)")

print(f"\nP&L Total: ${pl_total:+,.2f}")
```

### 2.2 Ejercicio guiado: Rentabilidades con list comprehension

```python
compras = [("AAPL", 150, 175), ("MSFT", 280, 310), ("TSLA", 900, 820)]

rentabilidades = [(ticker, (vta - cmp) / cmp * 100) for ticker, cmp, vta in compras]

for ticker, rent in rentabilidades:
    print(f"{ticker}: {rent:+.2f}%")

ganadoras = [t for t, r in rentabilidades if r > 0]
print(f"Ganadoras: {ganadoras}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Media, varianza y desviación estándar a mano

```python
def media(datos):
    return sum(datos) / len(datos)

def varianza(datos):
    prom = media(datos)
    return sum((x - prom) ** 2 for x in datos) / (len(datos) - 1)

def desviacion_estandar(datos):
    return varianza(datos) ** 0.5

def max_drawdown(precios):
    pico = precios[0]
    max_dd = 0
    for precio in precios:
        if precio > pico:
            pico = precio
        dd = (pico - precio) / pico * 100
        max_dd = max(max_dd, dd)
    return max_dd

# Datos de ejemplo
precios = [100, 102, 105, 98, 103, 108, 95, 102, 110, 105]
retornos = [(precios[i]-precios[i-1])/precios[i-1]*100 for i in range(1, len(precios))]

print(f"Media: {media(retornos):.2f}%")
print(f"Volatilidad: {desviacion_estandar(retornos):.2f}%")
print(f"Max Drawdown: {max_drawdown(precios):.2f}%")
```

### 3.2 Cesta de monedas

```python
cesta = [
    ("EUR", 0.92, 0.40),
    ("GBP", 0.79, 0.25),
    ("JPY", 150.50, 0.20),
    ("CHF", 0.90, 0.15),
]

inversion = 100000
for moneda, tasa, peso in cesta:
    monto_usd = inversion * peso
    monto_moneda = monto_usd * tasa
    print(f"{moneda}: ${monto_usd:,.2f} → {monto_moneda:,.2f} {moneda}")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-2/U07_ejercicios.py`

1. **Rastreador de portafolio:** Lista de (ticker, cantidad, precio_compra). Calcula P&L total.

2. **Filtro de oportunidades:** Con list comprehension, filtra acciones con PER < 15 y crecimiento > 10%.

3. **SMA con slicing:** Calcula media móvil de 5 días usando slicing en listas.

4. **Estadísticas financieras:** Calcula media, varianza, desviación estándar y max drawdown usando solo listas.

---

## 5. Resumen

| Característica | Lista | Tupla |
|---------------|-------|-------|
| Sintaxis | `[1, 2, 3]` | `(1, 2, 3)` |
| Mutable | Sí | No |
| Métodos | append, pop, sort... | count, index |
| Uso financiero | Series de precios | Registros OHLCV |

---

## ✅ Autoevaluación

1. ¿Cómo agregas un elemento al final de una lista?
2. ¿Qué diferencia hay entre `lista.sort()` y `sorted(lista)`?
3. ¿Por qué usarías tuplas para datos OHLCV en vez de listas?
4. Crea con list comprehension una lista de cuadrados de números pares del 1 al 20.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U07.md`: Slicing, métodos de listas, tuplas, rolling windows
> - `project-U07.md`: Gestor de portafolio, estadísticas sin librerías externas
