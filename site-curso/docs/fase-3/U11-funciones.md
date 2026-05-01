# U11: Funciones — Construyendo tu Librería Financiera

> **Lectura previa:** [U10: Archivos y Datos — CSV, JSON](../fase-2/U10-archivos.md)
> **Próxima unidad:** [U12: Funciones Avanzadas — Lambda, Decoradores y Closures](./U12-funciones-avanzadas.md)

---

## 1. Teoría

### 1.1 ¿Qué es una función?

Una **función** es un bloque de código reutilizable que realiza una tarea específica.

```python
def nombre_funcion(parametros):
    """Docstring: describe qué hace la función."""
    # código
    return resultado
```

### 1.2 Parámetros y argumentos

```python
# Posicionales
def calcular_interes(capital, tasa, tiempo):
    return capital * (tasa / 100) * tiempo

# Con valores por defecto
def valor_futuro(capital, tasa=8, tiempo=5):
    return capital * (1 + tasa / 100) ** tiempo

# Argumentos nombrados (keyword arguments)
monto = valor_futuro(10000, tasa=10, tiempo=3)
monto = valor_futuro(10000, tiempo=10)  # tasa usa default=8
```

### 1.3 Return — Simple y múltiple

```python
# Retorno simple
def rendimiento(precio_inicial, precio_final):
    return (precio_final - precio_inicial) / precio_inicial * 100

# Retorno múltiple (tupla)
def analizar_posicion(precio, cantidad):
    valor = precio * cantidad
    return valor, precio, cantidad

total, p, c = analizar_posicion(150, 10)

# Sin return → retorna None
def log_precio(ticker, precio):
    print(f"{ticker}: ${precio}")
```

### 1.4 Type hints (anotaciones de tipo)

En finanzas, los type hints evitan errores costosos. No afectan la ejecución pero sí la legibilidad y el autocompletado.

```python
def sharpe_ratio(
    rendimiento: float,
    tasa_libre_riesgo: float,
    volatilidad: float
) -> float:
    """Calcula el Sharpe Ratio."""
    return (rendimiento - tasa_libre_riesgo) / volatilidad

def valor_presente_neto(
    flujos: list[float],
    tasa: float,
    inversion_inicial: float = 0
) -> float:
    """VPN de una serie de flujos."""
    return sum(f / (1 + tasa) ** (t + 1) for t, f in enumerate(flujos)) - inversion_inicial
```

### 1.5 Docstrings estilo NumPy

```python
def calcular_tir(flujos: list[float], tolerancia: float = 1e-6, max_iter: int = 1000) -> float:
    """
    Calcula la Tasa Interna de Retorno por bisección.

    Parameters
    ----------
    flujos : list[float]
        Lista de flujos de caja. El primer elemento debe ser negativo (inversión).
    tolerancia : float, default 1e-6
        Precisión deseada para la convergencia.
    max_iter : int, default 1000
        Máximo de iteraciones permitidas.

    Returns
    -------
    float
        TIR expresada como decimal (ej. 0.15 = 15%).

    Raises
    ------
    ValueError
        Si la TIR no converge en max_iter iteraciones o si los flujos son inválidos.
    """
    if not flujos or flujos[0] >= 0:
        raise ValueError("El primer flujo debe ser negativo (inversión)")

    tasa_min, tasa_max = 0.0, 1.0
    
    for _ in range(max_iter):
        tasa_media = (tasa_min + tasa_max) / 2
        vpn = sum(f / (1 + tasa_media) ** t for t, f in enumerate(flujos))
        if abs(vpn) < tolerancia:
            return tasa_media
        if vpn > 0:
            tasa_min = tasa_media
        else:
            tasa_max = tasa_media
    
    raise ValueError(f"TIR no convergió en {max_iter} iteraciones")
```

### 1.6 `*args` y `**kwargs`

```python
# *args: N argumentos posicionales → tupla
def rendimiento_promedio(*rendimientos: float) -> float:
    if not rendimientos:
        return 0.0
    return sum(rendimientos) / len(rendimientos)

print(rendimiento_promedio(5.2, -2.1, 3.8, 0.5))  # 1.85

# **kwargs: N argumentos nombrados → dict
def crear_portafolio(**activos: float) -> dict:
    total = sum(activos.values())
    return {ticker: valor / total for ticker, valor in activos.items()}

pesos = crear_portafolio(AAPL=3500, MSFT=6200, TSLA=5300)
print(pesos)  # {'AAPL': 0.233, 'MSFT': 0.413, 'TSLA': 0.353}
```

### 1.7 Desempaquetado con `*` y `**`

```python
def sharpe(rendimiento, tasa_libre, volatilidad):
    return (rendimiento - tasa_libre) / volatilidad

# Desempaquetar lista → argumentos posicionales
datos = [15, 4, 18]
print(sharpe(*datos))  # sharpe(15, 4, 18)

# Desempaquetar dict → argumentos nombrados
params = {"rendimiento": 15, "tasa_libre": 4, "volatilidad": 18}
print(sharpe(**params))  # sharpe(rendimiento=15, tasa_libre=4, volatilidad=18)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Módulo `finanzas_basicas.py`

```python
# ============================================
# finanzas_basicas.py — Librería de funciones financieras
# ============================================

def valor_futuro(capital: float, tasa_anual: float, anios: int) -> float:
    """Calcula el valor futuro con interés compuesto anual."""
    return capital * (1 + tasa_anual / 100) ** anios

def valor_presente(valor_futuro: float, tasa_anual: float, anios: int) -> float:
    """Calcula el valor presente descontando a tasa anual."""
    return valor_futuro / (1 + tasa_anual / 100) ** anios

def cagr(valor_inicial: float, valor_final: float, anios: int) -> float:
    """Tasa de Crecimiento Anual Compuesta (en %)."""
    return ((valor_final / valor_inicial) ** (1 / anios) - 1) * 100

def cuota_prestamo(monto: float, tasa_anual: float, plazo_meses: int) -> float:
    """Cuota fija mensual (sistema francés)."""
    i = (tasa_anual / 100) / 12
    return monto * (i * (1 + i) ** plazo_meses) / ((1 + i) ** plazo_meses - 1)

def sharpe_ratio(rendimiento: float, tasa_libre: float, volatilidad: float) -> float:
    """Sharpe Ratio: exceso de retorno sobre riesgo."""
    return (rendimiento - tasa_libre) / volatilidad

def rendimiento_diario(precios: list[float]) -> list[float]:
    """Lista de rendimientos diarios porcentuales."""
    return [(precios[i] - precios[i-1]) / precios[i-1] * 100
            for i in range(1, len(precios))]

def volatilidad_anualizada(rendimientos_diarios: list[float]) -> float:
    """Volatilidad anualizada desde rendimientos diarios porcentuales."""
    n = len(rendimientos_diarios)
    media = sum(rendimientos_diarios) / n
    varianza = sum((r - media) ** 2 for r in rendimientos_diarios) / (n - 1)
    return (varianza ** 0.5) * (252 ** 0.5)

def payback(inversion: float, flujos: list[float]) -> int | None:
    """Años para recuperar la inversión. Retorna None si no se recupera."""
    acumulado = 0.0
    for i, flujo in enumerate(flujos, start=1):
        acumulado += flujo
        if acumulado >= inversion:
            return i
    return None

def vpn(inversion: float, tasa: float, flujos: list[float]) -> float:
    """Valor Presente Neto."""
    return sum(f / (1 + tasa) ** (i + 1) for i, f in enumerate(flujos)) - inversion

def max_drawdown(precios: list[float]) -> float:
    """Máximo drawdown porcentual desde un pico."""
    pico = precios[0]
    max_dd = 0.0
    for precio in precios:
        if precio > pico:
            pico = precio
        dd = (pico - precio) / pico * 100
        max_dd = max(max_dd, dd)
    return max_dd


# Pruebas rápidas
if __name__ == "__main__":
    print(f"VF $10,000 al 8% por 10 años: ${valor_futuro(10000, 8, 10):,.2f}")
    print(f"CAGR $5,000 → $12,000 en 8 años: {cagr(5000, 12000, 8):.2f}%")
    print(f"Cuota préstamo $200K al 10% a 20 años: ${cuota_prestamo(200000, 10, 240):,.2f}")
    print(f"VPN: ${vpn(10000, 0.10, [3000, 4000, 5000, 6000]):,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Funciones que se usan en un desk real

```python
def valoracion_bono(valor_nominal: float, cupon_pct: float,
                    tasa_mercado: float, anios: int) -> float:
    """Valor presente de un bono bullet."""
    cupon = valor_nominal * (cupon_pct / 100)
    tasa = tasa_mercado / 100
    vp_cupones = sum(cupon / (1 + tasa) ** t for t in range(1, anios + 1))
    vp_nominal = valor_nominal / (1 + tasa) ** anios
    return vp_cupones + vp_nominal

def beta_accion(rendimientos_accion: list[float],
                rendimientos_mercado: list[float]) -> float:
    """Beta por regresión simple (mínimos cuadrados manual)."""
    n = len(rendimientos_accion)
    media_a = sum(rendimientos_accion) / n
    media_m = sum(rendimientos_mercado) / n
    cov = sum((a - media_a) * (m - media_m) for a, m in zip(rendimientos_accion, rendimientos_mercado))
    var_m = sum((m - media_m) ** 2 for m in rendimientos_mercado)
    return cov / var_m if var_m != 0 else 0.0
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-3/U11_ejercicios.py`

1. **payback:** Función que calcula años para recuperar inversión.

2. **VPN:** Función de valor presente neto con type hints y docstring.

3. **Estadísticas con *args:** Función que recibe N rendimientos y retorna (promedio, max, min).

4. **CAGR y volatilidad:** Implementa CAGR y volatilidad anualizada como funciones con type hints.

---

## 5. Resumen

| Concepto | Sintaxis |
|---------|---------|
| Función | `def nombre(params): return valor` |
| Parámetros default | `def f(x, y=10):` |
| Type hints | `def f(x: float) -> float:` |
| Docstring NumPy | Parameters / Returns / Raises |
| `*args` | Argumentos posicionales variables |
| `**kwargs` | Argumentos nombrados variables |
| `*` unpack | `func(*lista)` |
| `**` unpack | `func(**dict)` |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre parámetro y argumento?
2. ¿Qué ventaja ofrecen los type hints en finanzas?
3. ¿Qué retorna una función sin `return`?
4. Escribe una función que calcule el VPN de una serie de flujos con type hints.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U11.md`: def, parámetros, type hints, docstrings NumPy, *args, **kwargs
> - `project-U11.md`: Módulo finanzas_basicas.py con 10+ funciones
