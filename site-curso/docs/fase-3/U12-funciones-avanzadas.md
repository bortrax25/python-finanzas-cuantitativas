# U12: Funciones Avanzadas — Lambda, Decoradores y Closures

> **Lectura previa:** [U11: Funciones — Librería Financiera](./U11-funciones.md)
> **Próxima unidad:** [U13: Módulos, Paquetes y Arquitectura de Proyecto](./U13-modulos-paquetes.md)

---

## 1. Teoría

### 1.1 Funciones lambda (anónimas)

```python
# lambda argumentos: expresion
cuadrado = lambda x: x ** 2

# En finanzas: clave para sorted(), map(), filter()
acciones = [("AAPL", 28, 8), ("XOM", 10, 15), ("JPM", 9, 12)]

# Ordenar por PER (índice 1) ascendente
por_per = sorted(acciones, key=lambda x: x[1])
print(por_per)  # [('JPM', 9, 12), ('XOM', 10, 15), ('AAPL', 28, 8)]

# Ordenar por crecimiento (índice 2) descendente
por_crec = sorted(acciones, key=lambda x: x[2], reverse=True)

# Filtrar con filter()
rendimientos = [5.2, -2.1, 3.8, -0.5, 4.2]
positivos = list(filter(lambda r: r > 0, rendimientos))  # [5.2, 3.8, 4.2]

# Transformar con map()
comisiones = list(map(lambda r: r * 0.005, rendimientos))  # 0.5% de comisión
```

### 1.2 Closures — Funciones que recuerdan su entorno

```python
def crear_calculadora_impuesto(porcentaje):
    """Factory de calculadoras de impuesto."""
    def calcular(monto):
        return monto * (porcentaje / 100)
    return calcular

impuesto_renta = crear_calculadora_impuesto(20)
impuesto_iva = crear_calculadora_impuesto(15)

print(impuesto_renta(50000))  # 10000 (20%)
print(impuesto_iva(50000))    # 7500 (15%)

# Closure financiero: descuento por tasa
def crear_descontador(tasa):
    import math
    def valor_presente(flujo, periodo):
        return flujo / math.exp(tasa * periodo)
    return valor_presente

descontar_5pct = crear_descontador(0.05)
print(descontar_5pct(1000, 5))  # 778.80
```

### 1.3 Decoradores

Un decorador es una función que envuelve a otra para extender su comportamiento sin modificarla.

```python
import time
from functools import wraps

def medir_tiempo(func):
    """Decorador que mide tiempo de ejecución."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fin = time.perf_counter()
        print(f"{func.__name__} tardó {fin - inicio:.4f}s")
        return resultado
    return wrapper

@medir_tiempo
def calcular_var_historico(rendimientos, confianza=0.95):
    """VaR histórico: percentil de la distribución de pérdidas."""
    ordenados = sorted(rendimientos)
    indice = int(len(ordenados) * (1 - confianza))
    return -ordenados[indice]

# Usar
retornos = [1.2, -0.5, 2.1, -3.8, 0.9, -1.2, 2.5, -0.8]
var_95 = calcular_var_historico(retornos)
print(f"VaR 95%: {var_95:.2f}%")
```

### 1.4 Decorador `@registrar_operacion` (log de trades)

```python
def registrar_operacion(func):
    """Registra cada trade con timestamp."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__}({args}, {kwargs})")
        resultado = func(*args, **kwargs)
        print(f"[{timestamp}] Resultado: {resultado}")
        return resultado
    return wrapper

@registrar_operacion
def ejecutar_trade(ticker, tipo, cantidad, precio):
    return {"ticker": ticker, "tipo": tipo, "total": cantidad * precio}

ejecutar_trade("AAPL", "compra", 100, 175.50)
```

### 1.5 Decorador `@validar_positivo`

```python
def validar_positivo(func):
    """Asegura que todos los argumentos numéricos sean positivos."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Argumento inválido: {arg} debe ser positivo")
        for k, v in kwargs.items():
            if isinstance(v, (int, float)) and v <= 0:
                raise ValueError(f"Argumento {k}={v} debe ser positivo")
        return func(*args, **kwargs)
    return wrapper

@validar_positivo
def calcular_precio_bono(valor_nominal, cupon, tasa, anios):
    cupon_anual = valor_nominal * cupon
    return sum(cupon_anual / (1 + tasa) ** t for t in range(1, anios+1)) + valor_nominal / (1 + tasa) ** anios

print(calcular_precio_bono(1000, 0.05, 0.04, 10))  # OK
# calcular_precio_bono(-1000, 0.05, 0.04, 10)        # ValueError
```

### 1.6 `functools` — Herramientas funcionales

```python
from functools import partial, reduce, lru_cache

# partial: fijar argumentos de una función
def calcular_interes(capital, tasa_anual, tiempo, capitalizacion=1):
    return capital * (1 + tasa_anual / capitalizacion) ** (tiempo * capitalizacion)

interes_anual = partial(calcular_interes, capitalizacion=1)
interes_mensual = partial(calcular_interes, capitalizacion=12)

print(interes_anual(10000, 0.08, 5))     # $14,693.28
print(interes_mensual(10000, 0.08, 5))   # $14,898.46

# reduce: acumular valores
retornos = [1.02, 1.015, 0.98, 1.03]
capital_final = reduce(lambda acc, r: acc * r, retornos, 10000)
print(f"Capital final: ${capital_final:,.2f}")

# lru_cache: cachear resultados de funciones costosas
@lru_cache(maxsize=128)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Pipeline de procesamiento con lambda

```python
# Datos: (ticker, precio, cambio_pct)
datos = [
    ("AAPL", 175.50, 2.1),
    ("MSFT", 310.25, -0.5),
    ("TSLA", 820.00, -3.2),
    ("JPM", 142.80, 1.8),
    ("XOM", 85.30, 0.3),
]

# Filtrar: solo acciones que subieron
subieron = list(filter(lambda x: x[2] > 0, datos))

# Ordenar por cambio porcentual (mayor a menor)
ranking = sorted(subieron, key=lambda x: x[2], reverse=True)

# Transformar: capitalizar tickers
caps = list(map(lambda x: (x[0].upper(), x[1], x[2]), ranking))

for ticker, precio, cambio in caps:
    print(f"{ticker}: ${precio:.2f} ({cambio:+.1f}%)")
```

### 2.2 Ejercicio guiado: Decoradores aplicados a pricing

```python
import time
from functools import wraps

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion = time.perf_counter() - inicio
        print(f"[TIMER] {func.__name__}: {duracion:.6f}s")
        return resultado
    return wrapper

def validar_parametros(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Argumento {i} negativo: {arg}")
        return func(*args, **kwargs)
    return wrapper

@medir_tiempo
@validar_parametros
def black_scholes_call(S, K, T, r, sigma):
    """Precio de una opción CALL con Black-Scholes."""
    import math
    d1 = (math.log(S/K) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    # Usamos aproximación simple de N(x) para no importar scipy
    def N(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return S * N(d1) - K * math.exp(-r * T) * N(d2)

precio = black_scholes_call(S=100, K=105, T=1, r=0.05, sigma=0.2)
print(f"Precio CALL: ${precio:.2f}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Filtrado de activos por criterios

```python
acciones = [
    {"ticker": "AAPL", "per": 28, "crecimiento": 8, "dividendo": 0.5},
    {"ticker": "XOM", "per": 10, "crecimiento": 15, "dividendo": 3.5},
    {"ticker": "JPM", "per": 9, "crecimiento": 12, "dividendo": 2.8},
    {"ticker": "TSLA", "per": 65, "crecimiento": 25, "dividendo": 0},
    {"ticker": "CVX", "per": 11, "crecimiento": 18, "dividendo": 3.2},
]

# Value: PER < 15
value = list(filter(lambda a: a["per"] < 15, acciones))

# Growth: Crecimiento > 10%
growth = list(filter(lambda a: a["crecimiento"] > 10, acciones))

# Dividend: Dividendo > 2%
dividend = list(filter(lambda a: a["dividendo"] > 2, acciones))

# Top 3 por combinación (PER bajo + crecimiento alto)
ranking = sorted(acciones, key=lambda a: a["per"] - a["crecimiento"])

print("Top 3 Value+Growth:")
for a in ranking[:3]:
    print(f"  {a['ticker']}: PER={a['per']}, Crec={a['crecimiento']}%")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-3/U12_ejercicios.py`

1. **Filtro con lambda:** Filtra acciones por PER < 15 y Crecimiento > 10% usando filter+lambda.

2. **Ordenamiento con lambda:** Ordena acciones por Sharpe ratio de mayor a menor.

3. **Decorador @medir_tiempo:** Aplica a una función que calcule VaR histórico.

4. **Decorador @registrar_operacion:** Crea un decorador que registre cada trade ejecutado con timestamp.

---

## 5. Resumen

| Herramienta | Uso financiero |
|------------|---------------|
| `lambda` | Filtros rápidos, keys de sorted |
| `map()` | Transformar datos (comisiones, fx) |
| `filter()` | Screening de activos |
| `sorted(key=lambda)` | Rankings, top performers |
| Closure | Factory de calculadoras (impuestos, descuentos) |
| `@decorator` | Timing, logging, validación |
| `functools.partial` | Fijar parámetros (capitalización) |
| `functools.reduce` | Acumular rendimientos compuestos |
| `functools.lru_cache` | Cachear cálculos costosos |

---

## ✅ Autoevaluación

1. ¿Qué hace `sorted(lista, key=lambda x: x[1])`?
2. ¿Cuál es la diferencia entre un closure y una función normal?
3. ¿Qué problema resuelve un decorador en una librería financiera?
4. Crea un decorador `@log_trade` que imprima el ticker, precio y timestamp de cada trade.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U12.md`: lambda, closures, decoradores, functools (partial, lru_cache, reduce)
> - `project-U12.md`: Decoradores @medir_tiempo, @registrar_operacion, @validar_positivo
