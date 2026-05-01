# U14: args, kwargs, lambda y Scope

> **Lectura previa:** [U13: Funciones básicas](./U13-funciones-basicas.md)
> **Próxima unidad:** [U15: Módulos, paquetes e intro a Jupyter](./U15-modulos-jupyter.md)

---

## 1. Teoría

### 1.1 `*args` — Múltiples argumentos posicionales

`*args` permite recibir un número variable de argumentos como tupla.

```python
def rendimiento_promedio(*rendimientos):
    """Calcula el promedio de N rendimientos."""
    if not rendimientos:
        return 0
    return sum(rendimientos) / len(rendimientos)

print(rendimiento_promedio(5.2, -2.1, 3.8))
print(rendimiento_promedio(1.2, -0.5, 2.1, -0.8, 0.3))

def calcular_valor_total(*posiciones):
    """Suma el valor de N posiciones (cantidad, precio)."""
    total = 0
    for cantidad, precio in posiciones:
        total += cantidad * precio
    return total

total = calcular_valor_total((10, 150), (5, 280), (3, 900))
print(f"Total: ${total:,.2f}")
```

### 1.2 `**kwargs` — Múltiples argumentos nombrados

`**kwargs` permite recibir un número variable de argumentos con nombre como diccionario.

```python
def crear_activo(ticker, **detalles):
    """Crea un diccionario de activo con detalles adicionales."""
    activo = {"ticker": ticker}
    activo.update(detalles)
    return activo

aapl = crear_activo("AAPL", precio=175.50, sector="Tecnología", pe=28)
print(aapl)

def resumen_portafolio(**activos):
    """Muestra resumen de portafolio con kwargs."""
    total = sum(activos.values())
    for ticker, valor in activos.items():
        print(f"{ticker}: ${valor:,.2f} ({valor/total*100:.1f}%)")

resumen_portafolio(AAPL=3500, MSFT=6200, TSLA=5300)
```

### 1.3 Desempaquetado con `*` y `**`

```python
# Desempaquetar lista en argumentos posicionales
def sharpe(rendimiento, tasa_libre, volatilidad):
    return (rendimiento - tasa_libre) / volatilidad

datos = [15, 4, 18]
print(sharpe(*datos))  # sharpe(15, 4, 18)

# Desempaquetar dict en argumentos nombrados
params = {"rendimiento": 15, "tasa_libre": 4, "volatilidad": 18}
print(sharpe(**params))
```

### 1.4 Funciones lambda (anónimas)

Función de una línea sin nombre. Ideal para operaciones simples.

```python
# Sintaxis: lambda argumentos: expresion

cuadrado = lambda x: x ** 2
print(cuadrado(5))  # 25

# Muy útil con sorted(), map(), filter()
rendimientos = [5.2, -2.1, 3.8, -0.5, 4.2]

# Ordenar por valor absoluto
ordenados = sorted(rendimientos, key=lambda r: abs(r))

# Filtrar positivos
positivos = list(filter(lambda r: r > 0, rendimientos))

# Transformar a porcentaje * 100
porcentajes = list(map(lambda r: r * 100, rendimientos))

# Ejemplo financiero: ordenar acciones por ratio
acciones = [("AAPL", 28, 8), ("XOM", 10, 15), ("JPM", 9, 12)]
acciones.sort(key=lambda x: x[1])  # Ordenar por PER
```

### 1.5 Scope (alcance de variables)

| Tipo | Definición | Accesible desde |
|------|-----------|----------------|
| **Local** | Dentro de función | Solo dentro de la función |
| **Global** | Fuera de toda función | Todo el archivo |
| **nonlocal** | En función anidada | Modifica variable del enclosing scope |

```python
tasa_global = 8          # Variable global

def calcular_monto(capital):
    tasa_local = 5       # Variable local
    return capital * (1 + tasa_local/100) ** 2

def usar_global(capital):
    global tasa_global   # Indica que modificamos la global
    tasa_global = 10
    return capital * (1 + tasa_global/100)

print(calcular_monto(10000))
print(usar_global(10000))
print(tasa_global)       # 10 (fue modificada)
```

---

## 2. Práctica

```python
# Pipeline de procesamiento con lambda
precios = [150, 280, 900, 175, 310]
cantidades = [10, 5, 3, 8, 4]

# Calcular valor de cada posición en una línea
valores = list(map(lambda p, q: p * q, precios, cantidades))

# Solo posiciones > $2,000
grandes = list(filter(lambda v: v > 2000, valores))

# Ordenar descendentemente
grandes.sort(reverse=True)
print(f"Posiciones grandes: {grandes}")
```

---

## 5. Resumen

| Concepto | Uso |
|---------|-----|
| `*args` | N args posicionales → tupla |
| `**kwargs` | N args nombrados → dict |
| `*` unpack | `func(*lista)` |
| `**` unpack | `func(**dict)` |
| `lambda` | `lambda x: x*2` |
| `global` | Modificar variable global |

---

## ✅ Autoevaluación

1. ¿Qué tipo de dato es `args` dentro de `def f(*args)`?
2. ¿Qué hace `sorted(lista, key=lambda x: x[1])`?
3. ¿Cuándo usarías `global`?
4. Escribe una función que acepte cualquier número de rendimientos y retorne (promedio, máximo, mínimo).

---

> 📝 **Knowledge Wiki:** Guarda `reference-U14.md` (*args, **kwargs, lambda, scope).
