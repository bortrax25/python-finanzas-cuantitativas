# U13: Funciones Básicas y Parámetros

> **Lectura previa:** [U12: Manejo de archivos CSV](../fase-4/U12-archivos-csv.md)
> **Próxima unidad:** [U14: args, kwargs, lambda y scope](./U14-avanzado-funciones.md)

---

## 1. Teoría

### 1.1 ¿Qué es una función?

Una **función** es un bloque de código reutilizable que realiza una tarea específica. Se define con `def`.

```python
# Sintaxis
def nombre_funcion(parametros):
    """Docstring: describe qué hace la función."""
    # código
    return resultado

# Ejemplo mínimo
def saludar(nombre):
    return f"Hola, {nombre}"

print(saludar("Carlos"))  # Hola, Carlos
```

### 1.2 Parámetros y argumentos

```python
# Parámetros posicionales
def calcular_interes(capital, tasa, tiempo):
    return capital * (tasa / 100) * tiempo

interes = calcular_interes(10000, 5, 3)   # 1500.0

# Parámetros con valor por defecto
def valor_futuro(capital, tasa=8, tiempo=5):
    return capital * (1 + tasa/100) ** tiempo

print(valor_futuro(10000))              # Usa defaults: 8%, 5 años
print(valor_futuro(10000, 10, 3))       # Sobrescribe
print(valor_futuro(10000, tiempo=10))   # Argumentos nombrados
```

### 1.3 `return` — Retornar valores

```python
# Retorno simple
def rendimiento(precio_inicial, precio_final):
    return (precio_final - precio_inicial) / precio_inicial * 100

# Retorno múltiple (tupla)
def analizar_accion(precio, cantidad):
    valor = precio * cantidad
    return valor, precio, cantidad

total, precio, cant = analizar_accion(150, 10)

# Sin return → retorna None
def mostrar_precio(ticker, precio):
    print(f"{ticker}: ${precio}")

resultado = mostrar_precio("AAPL", 175)   # None
```

### 1.4 Docstrings y type hints

```python
def sharpe_ratio(rendimiento: float, tasa_libre_riesgo: float, volatilidad: float) -> float:
    """
    Calcula el Sharpe Ratio de un activo o portafolio.

    Args:
        rendimiento: Rendimiento anualizado (%).
        tasa_libre_riesgo: Tasa libre de riesgo (%).
        volatilidad: Volatilidad anualizada (%).

    Returns:
        float: Sharpe Ratio.
    """
    return (rendimiento - tasa_libre_riesgo) / volatilidad

help(sharpe_ratio)
```

### 1.5 Funciones como bloques de construcción

```python
# Pequeñas funciones que se combinan
def rendimiento_diario(precios):
    return [(precios[i] - precios[i-1]) / precios[i-1] * 100
            for i in range(1, len(precios))]

def promedio(lista):
    return sum(lista) / len(lista) if lista else 0

def volatilidad(rendimientos):
    prom = promedio(rendimientos)
    varianza = sum((r - prom) ** 2 for r in rendimientos) / (len(rendimientos) - 1)
    return varianza ** 0.5

# Uso combinado
precios = [100, 102, 105, 103, 108]
rets = rendimiento_diario(precios)
print(f"Volatilidad: {volatilidad(rets):.2f}%")
```

---

## 2. Práctica

### 2.1 Módulo financiero personal

```python
def interes_compuesto(capital, tasa_anual, anios):
    """Calcula monto final con interés compuesto."""
    return capital * (1 + tasa_anual / 100) ** anios

def cagr(vi, vf, anios):
    """Tasa de crecimiento anual compuesta."""
    return ((vf / vi) ** (1 / anios) - 1) * 100

def cuota_prestamo(monto, tasa_anual, plazo_meses):
    """Calcula cuota fija mensual (sistema francés)."""
    i = (tasa_anual / 100) / 12
    return monto * (i * (1 + i) ** plazo_meses) / ((1 + i) ** plazo_meses - 1)

# Probar
print(f"Interés compuesto: ${interes_compuesto(10000, 8, 10):,.2f}")
print(f"CAGR: {cagr(5000, 12000, 8):.2f}%")
print(f"Cuota: ${cuota_prestamo(200000, 10, 240):,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

```python
def valoracion_bono(valor_nominal, cupon_pct, tasa_mercado, anios):
    """Valor presente de un bono (bullet)."""
    cupon = valor_nominal * (cupon_pct / 100)
    tasa = tasa_mercado / 100
    vp_cupones = sum(cupon / (1 + tasa) ** t for t in range(1, anios + 1))
    vp_nominal = valor_nominal / (1 + tasa) ** anios
    return vp_cupones + vp_nominal

precio = valoracion_bono(1000, 5, 4, 10)
print(f"Precio del bono: ${precio:,.2f}")
```

---

## 4. Ejercicios Propuestos

1. Escribe una función `payback(inversion, flujos)` que retorne el número de períodos para recuperar la inversión.
2. Crea `tir_aproximada(flujos)` que estime la TIR por iteración.
3. Implementa `diversificacion(correlaciones)` que determine si un portafolio está bien diversificado (promedio correlación < 0.5).

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre parámetro y argumento?
2. ¿Qué retorna una función sin `return`?
3. ¿Qué hacen los type hints y por qué son útiles?
4. Escribe una función que calcule el valor presente neto (VPN) de una serie de flujos.

---

> 📝 **Knowledge Wiki:** Guarda `reference-U13.md` (sintaxis def, parámetros default) y `project-U13.md` (módulo financiero personal).
