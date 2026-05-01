# U02: Operadores en Python

> **Lectura previa:** [U01: Variables y tipos de datos](./U01-variables-tipos.md)
> **Próxima unidad:** [U03: Entrada, salida y debugging](./U03-entrada-salida.md)

---

## 1. Teoría

### 1.1 Operadores aritméticos

Realizan operaciones matemáticas entre valores.

| Operador | Nombre | Ejemplo | Resultado |
|----------|--------|---------|-----------|
| `+` | Suma | `5 + 3` | `8` |
| `-` | Resta | `5 - 3` | `2` |
| `*` | Multiplicación | `5 * 3` | `15` |
| `/` | División (siempre float) | `5 / 2` | `2.5` |
| `//` | División entera | `5 // 2` | `2` |
| `%` | Módulo (residuo) | `5 % 2` | `1` |
| `**` | Potencia | `5 ** 3` | `125` |

```python
# Ejemplos con datos financieros
precio = 150
cantidad = 10
inversion = precio * cantidad          # 1500
promedio = inversion / cantidad        # 150.0
residuo = inversion % 3               # 0 (1500 divisible entre 3)
cuota_diaria = 365 // 12              # 30 (días, división entera)
rendimiento = (1 + 0.08) ** 5         # 1.469... (interés compuesto)
```

### 1.2 Operadores relacionales (comparación)

Comparan dos valores. El resultado siempre es `True` o `False` (`bool`).

| Operador | Significado | Ejemplo | Resultado |
|----------|------------|---------|-----------|
| `==` | Igual a | `5 == 5` | `True` |
| `!=` | Distinto de | `5 != 3` | `True` |
| `>` | Mayor que | `5 > 3` | `True` |
| `<` | Menor que | `5 < 3` | `False` |
| `>=` | Mayor o igual | `5 >= 5` | `True` |
| `<=` | Menor o igual | `3 <= 5` | `True` |

```python
# Comparaciones financieras
precio_actual = 175
precio_compra = 150
meta = 200

hay_ganancia = precio_actual > precio_compra   # True
alcanzo_meta = precio_actual >= meta            # False
es_igual = precio_actual == precio_compra       # False
```

### 1.3 Operadores lógicos

Combinan expresiones booleanas.

| Operador | Significado | Descripción |
|----------|------------|------------|
| `and` | Y lógico | `True` si **ambas** son `True` |
| `or` | O lógico | `True` si **al menos una** es `True` |
| `not` | Negación | Invierte el valor booleano |

```python
# Tabla de verdad en finanzas
capital_disponible = True
precio_bajo = False

puedo_comprar = capital_disponible and precio_bajo   # False
debo_invertir = capital_disponible or precio_bajo     # True
no_puedo = not capital_disponible                     # False
```

### 1.4 Precedencia de operadores

Cuando hay múltiples operadores, Python los evalúa en este orden:

| Prioridad | Operadores |
|-----------|-----------|
| 1 (mayor) | `()` paréntesis |
| 2 | `**` potencia |
| 3 | `*`, `/`, `//`, `%` |
| 4 | `+`, `-` |
| 5 | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| 6 | `not` |
| 7 | `and` |
| 8 (menor) | `or` |

```python
# Sin paréntesis
resultado = 10 + 5 * 2        # 20 (multiplicación primero)

# Con paréntesis
resultado = (10 + 5) * 2      # 30 (paréntesis primero)

# Combinado
condicion = 5 > 3 and 10 < 20  # True
```

### 1.5 Operadores de asignación compuesta

Acortan operaciones comunes combinando asignación y operación.

| Operador | Equivalente a |
|----------|--------------|
| `x += y` | `x = x + y` |
| `x -= y` | `x = x - y` |
| `x *= y` | `x = x * y` |
| `x /= y` | `x = x / y` |
| `x //= y` | `x = x // y` |
| `x %= y` | `x = x % y` |
| `x **= y` | `x = x ** y` |

```python
# Ejemplo: acumular ganancias diarias
capital = 10000
capital += 250     # capital = 10250 (ganancia día 1)
capital -= 100     # capital = 10150 (pérdida día 2)
capital *= 1.02    # capital = 10353 (rendimiento 2%)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Rendimiento de portafolio

```python
# Datos de 3 acciones
acciones_aapl = 10
precio_compra_aapl = 150.00
precio_actual_aapl = 175.00

acciones_msft = 5
precio_compra_msft = 280.00
precio_actual_msft = 310.00

acciones_tsla = 3
precio_compra_tsla = 900.00
precio_actual_tsla = 820.00

# Calcular inversión total y valor actual
inversion = (acciones_aapl * precio_compra_aapl +
             acciones_msft * precio_compra_msft +
             acciones_tsla * precio_compra_tsla)

valor_actual = (acciones_aapl * precio_actual_aapl +
                acciones_msft * precio_actual_msft +
                acciones_tsla * precio_actual_tsla)

# Rendimiento del portafolio
ganancia = valor_actual - inversion
rendimiento_pct = (ganancia / inversion) * 100
hay_ganancia = ganancia > 0

print(f"Inversión total: ${inversion:,.2f}")
print(f"Valor actual: ${valor_actual:,.2f}")
print(f"Ganancia: ${ganancia:,.2f}")
print(f"Rendimiento: {rendimiento_pct:.2f}%")
print(f"¿Hay ganancia? {hay_ganancia}")
```

### 2.2 Ejercicio guiado: Cálculo de cuota de préstamo (método francés)

```python
# Préstamo: método francés (cuota fija)
monto = 10000
tasa_anual = 12
plazo_meses = 12

tasa_mensual = (tasa_anual / 100) / 12

# Cuota fija mensual (fórmula simplificada para practicar operadores)
# cuota = monto * (tasa_mensual * (1 + tasa_mensual)**plazo) / ((1 + tasa_mensual)**plazo - 1)
factor = (1 + tasa_mensual) ** plazo_meses
cuota = monto * (tasa_mensual * factor) / (factor - 1)
total_pagar = cuota * plazo_meses
interes_total = total_pagar - monto

print(f"Préstamo: ${monto:,.2f}")
print(f"Cuota mensual: ${cuota:,.2f}")
print(f"Total a pagar: ${total_pagar:,.2f}")
print(f"Interés total: ${interes_total:,.2f}")
```

---

## 3. Aplicación en Finanzas 💰

Los operadores son la base de todo cálculo financiero:

```python
# CAGR (Compound Annual Growth Rate)
# CAGR = (VF/VI)^(1/n) - 1
valor_inicial = 1000
valor_final = 2500
anios = 5
cagr = (valor_final / valor_inicial) ** (1 / anios) - 1
# CAGR = 0.2011... → 20.11% anual

# Sharpe Ratio simplificado
# Sharpe = (Rendimiento_portafolio - Tasa_libre_riesgo) / Volatilidad
rendimiento = 0.15
tasa_libre_riesgo = 0.05
volatilidad = 0.20
sharpe = (rendimiento - tasa_libre_riesgo) / volatilidad
# Sharpe = 0.5
```

---

## 4. Ejercicios Propuestos

1. **Cálculo de precio promedio:** Tienes 3 compras de una acción a diferentes precios. Calcula el precio promedio ponderado por cantidad.

2. **Verificador de stop-loss:** Dado un precio de entrada y un porcentaje de stop-loss, verifica si el precio actual activó el stop-loss (`precio_actual <= precio_entrada * (1 - stop_loss)`).

3. **CAGR de una acción:** Calcula la tasa de crecimiento anual compuesta dados precio inicial, precio final y años.

4. **Calculadora de hipoteca:** Calcula la cuota mensual de una hipoteca usando la fórmula del sistema francés.

---

## 5. Resumen

| Categoría | Operadores |
|-----------|-----------|
| Aritméticos | `+`, `-`, `*`, `/`, `//`, `%`, `**` |
| Relacionales | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Lógicos | `and`, `or`, `not` |
| Asignación compuesta | `+=`, `-=`, `*=`, `/=`, `//=`, `**=` |

---

## ✅ Autoevaluación

1. ¿Qué diferencia hay entre `10 / 3` y `10 // 3`?
2. ¿Qué resultado da `True and False or True`?
3. ¿Cuál es el resultado de `2 ** 3 ** 2`? (piensa en precedencia)
4. ¿Qué hace `x += 5` cuando `x = 10`?
5. Calcula el CAGR de una inversión que pasó de $5,000 a $12,000 en 8 años.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U02.md`: Tabla de precedencia de operadores
> - `project-U02.md`: Fórmulas CAGR, cuota de préstamo y Sharpe simplificado
