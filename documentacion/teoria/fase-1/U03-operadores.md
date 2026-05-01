# U03: Operadores — La Aritmética de Wall Street

> **Lectura previa:** [U02: Variables y tipos de datos](./U02-variables-tipos.md)
> **Próxima unidad:** [U04: Entrada, salida y manejo de errores](./U04-io-errores.md)

---

## 1. Teoría

### 1.1 Operadores aritméticos

| Operador | Nombre | Ejemplo | Resultado | Uso financiero |
|----------|--------|---------|-----------|---------------|
| `+` | Suma | `5 + 3` | `8` | Sumar flujos, P&L |
| `-` | Resta | `5 - 3` | `2` | Ganancia/pérdida |
| `*` | Multiplicación | `5 * 3` | `15` | Valor posición = precio × cantidad |
| `/` | División (siempre float) | `5 / 2` | `2.5` | Ratios financieros |
| `//` | División entera | `5 // 2` | `2` | Lotes de acciones |
| `%` | Módulo (residuo) | `5 % 2` | `1` | Días hábiles, ciclos |
| `**` | Potencia | `5 ** 3` | `125` | Interés compuesto |

```python
# Contexto financiero
precio = 150
cantidad = 10
inversion = precio * cantidad           # 1500
promedio = inversion / cantidad         # 150.0
lotes_completos = 1000 // 150           # 6 (acciones que puedes comprar con $1000)
rendimiento = (1 + 0.08) ** 5           # 1.469... (interés compuesto 5 años al 8%)
```

### 1.2 Operadores relacionales (comparación)

| Operador | Significado | Ejemplo | Resultado |
|----------|------------|---------|-----------|
| `==` | Igual a | `5 == 5` | `True` |
| `!=` | Distinto de | `5 != 3` | `True` |
| `>` | Mayor que | `5 > 3` | `True` |
| `<` | Menor que | `5 < 3` | `False` |
| `>=` | Mayor o igual | `5 >= 5` | `True` |
| `<=` | Menor o igual | `3 <= 5` | `True` |

```python
precio_actual = 175
precio_compra = 150
meta = 200

hay_ganancia = precio_actual > precio_compra    # True
alcanzo_meta = precio_actual >= meta             # False
es_igual = precio_actual == precio_compra        # False
```

### 1.3 Operadores lógicos

| Operador | Significado | Descripción |
|----------|------------|------------|
| `and` | Y lógico | `True` si **ambas** son `True` |
| `or` | O lógico | `True` si **al menos una** es `True` |
| `not` | Negación | Invierte el valor booleano |

```python
capital_disponible = True
precio_bajo = False

puedo_comprar = capital_disponible and precio_bajo    # False
debo_invertir = capital_disponible or precio_bajo      # True
no_puedo = not capital_disponible                      # False
```

### 1.4 Rendimiento simple vs logarítmico

En finanzas hay dos formas de medir rendimientos:

**Rendimiento simple (aritmético):**
```
R_simple = (Pf - Pi) / Pi = Pf / Pi - 1
```

**Rendimiento logarítmico (continuo):**
```
R_log = ln(Pf / Pi)
```

Los quants prefieren el rendimiento logarítmico porque:
- Son aditivos en el tiempo: `R_log_total = R1 + R2 + R3`
- Se distribuyen normalmente (más fácil de modelar)
- Simétricos: +10% y -10% logarítmico son simétricos

```python
import math

precio_inicial = 100
precio_final = 112

# Rendimiento simple
r_simple = (precio_final - precio_inicial) / precio_inicial
print(f"R. Simple: {r_simple:.2%}")           # 12.00%

# Rendimiento logarítmico
r_log = math.log(precio_final / precio_inicial)
print(f"R. Log:    {r_log:.4%}")              # 11.33%

# El logarítmico siempre es menor (compounding continuo)
```

### 1.5 Spread bid-ask

El **bid-ask spread** es la diferencia entre el precio de compra (bid) y venta (ask). Es el costo implícito de transar.

```python
precio_bid = 150.00     # Precio al que puedes VENDER
precio_ask = 150.30     # Precio al que puedes COMPRAR

spread = precio_ask - precio_bid                    # $0.30
spread_pct = (spread / precio_ask) * 100            # ~0.20%
precio_medio = (precio_bid + precio_ask) / 2        # $150.15

print(f"Bid: ${precio_bid:.2f} | Ask: ${precio_ask:.2f}")
print(f"Spread: ${spread:.2f} ({spread_pct:.2f}%)")
print(f"Mid-price: ${precio_medio:.2f}")
```

### 1.6 CAGR (Tasa de Crecimiento Anual Compuesta)

El CAGR mide el rendimiento anualizado de una inversión, suavizando la volatilidad.

```
CAGR = (VF / VI)^(1/n) - 1
```

```python
valor_inicial = 10000
valor_final = 25000
anios = 5

cagr = (valor_final / valor_inicial) ** (1 / anios) - 1
print(f"CAGR: {cagr:.2%}")          # 20.11% anual

# Verificación: ¿$10,000 al 20.11% por 5 años llega a $25,000?
monto = valor_inicial * (1 + cagr) ** anios
print(f"Verificación: ${monto:,.2f}")  # $25,000.00
```

### 1.7 Precedencia de operadores

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
# Sin paréntesis: multiplicación primero
resultado = 10 + 5 * 2            # 20

# Con paréntesis
resultado = (10 + 5) * 2          # 30

# Combinado en finanzas
condicion = 5 > 3 and 10 < 20     # True
```

### 1.8 Asignación compuesta

| Operador | Equivalente | Uso financiero |
|----------|------------|---------------|
| `x += y` | `x = x + y` | Acumular P&L diario |
| `x -= y` | `x = x - y` | Restar comisiones |
| `x *= y` | `x = x * y` | Aplicar rendimiento compuesto |
| `x /= y` | `x = x / y` | Normalizar |
| `x **= y` | `x = x ** y` | Interés compuesto iterativo |

```python
# Acumular ganancias diarias
capital = 10000
capital += 250      # Día 1: $10,250
capital -= 100      # Día 2: $10,150
capital *= 1.02     # Día 3: rendimiento 2% → $10,353
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Rendimiento de portafolio

```python
# 3 acciones con cantidades y precios
acciones = [
    ("AAPL", 10, 150.00, 175.00),
    ("MSFT", 5, 280.00, 310.00),
    ("TSLA", 3, 900.00, 820.00),
]

inversion_total = 0
valor_actual_total = 0

for ticker, cant, p_compra, p_actual in acciones:
    inversion = cant * p_compra
    valor_actual = cant * p_actual
    inversion_total += inversion
    valor_actual_total += valor_actual
    pl = valor_actual - inversion
    pl_pct = (pl / inversion) * 100
    print(f"{ticker}: Inversión ${inversion:,.2f} → Actual ${valor_actual:,.2f} | P&L {pl_pct:+.2f}%")

pl_total = valor_actual_total - inversion_total
rendimiento_total = (pl_total / inversion_total) * 100
print(f"\nTotal: Inv ${inversion_total:,.2f} → ${valor_actual_total:,.2f} | {rendimiento_total:+.2f}%")
```

### 2.2 Ejercicio guiado: Cuota de préstamo (sistema francés)

```python
monto = 10000
tasa_anual = 12
plazo_meses = 12

tasa_mensual = (tasa_anual / 100) / 12

factor = (1 + tasa_mensual) ** plazo_meses
cuota = monto * (tasa_mensual * factor) / (factor - 1)

total_pagar = cuota * plazo_meses
interes_total = total_pagar - monto

print(f"Préstamo: ${monto:,.2f}")
print(f"Cuota mensual: ${cuota:,.2f}")
print(f"Total a pagar: ${total_pagar:,.2f}")
print(f"Interés total: ${interes_total:,.2f}")
```

**Output:**
```
Préstamo: $10,000.00
Cuota mensual: $888.49
Total a pagar: $10,661.88
Interés total: $661.88
```

### 2.3 Ejercicio guiado: Rendimiento logarítmico de una serie

```python
import math

precios = [100, 102, 99, 105, 108, 110]

rendimientos_simples = []
rendimientos_log = []

for i in range(1, len(precios)):
    r_simple = (precios[i] - precios[i-1]) / precios[i-1]
    r_log = math.log(precios[i] / precios[i-1])
    rendimientos_simples.append(r_simple)
    rendimientos_log.append(r_log)
    print(f"Día {i}: Simple {r_simple:+.2%} | Log {r_log:+.4%}")

# Suma de logarítmicos = log del retorno total
r_log_total = sum(rendimientos_log)
r_simple_total = (precios[-1] - precios[0]) / precios[0]
print(f"\nR. Simple total: {r_simple_total:.2%}")
print(f"R. Log total:     {r_log_total:.4%} (equivale a {math.exp(r_log_total) - 1:.2%})")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Sharpe Ratio simplificado

```python
# Sharpe = (Rp - Rf) / σp
rendimiento_portafolio = 0.15      # 15% anual
tasa_libre_riesgo = 0.05           # 5% (bonos del Tesoro US)
volatilidad = 0.20                 # 20% anual

sharpe = (rendimiento_portafolio - tasa_libre_riesgo) / volatilidad
print(f"Sharpe Ratio: {sharpe:.2f}")

# Interpretación:
# Sharpe > 1.0 → Excelente
# Sharpe > 0.5 → Bueno
# Sharpe > 0.0 → Positivo (mejor que tasa libre de riesgo)
# Sharpe < 0.0 → PEOR que tasa libre de riesgo
```

### 3.2 Interés compuesto continuo

```python
import math

# Capitalización continua: M = C * e^(r*t)
capital = 10000
tasa_continua = 0.08
anios = 5

monto = capital * math.exp(tasa_continua * anios)
print(f"Capitalización continua: ${monto:,.2f}")

# Comparar con capitalización anual
monto_anual = capital * (1 + tasa_continua) ** anios
print(f"Capitalización anual:     ${monto_anual:,.2f}")
print(f"Diferencia: ${monto - monto_anual:,.2f}")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-1/U03_ejercicios.py`

1. **Precio promedio ponderado:** 3 compras a diferentes precios y cantidades. Calcula PAPP.

2. **Stop-loss:** Verifica si el precio actual activó el stop-loss (`precio_actual <= precio_entrada * (1 - stop_loss/100)`).

3. **CAGR:** Calcula la tasa de crecimiento anual compuesta dados VI, VF y años.

4. **Calculadora de hipoteca:** Cuota mensual de una hipoteca con sistema francés.

---

## 5. Resumen

| Categoría | Operadores |
|-----------|-----------|
| Aritméticos | `+`, `-`, `*`, `/`, `//`, `%`, `**` |
| Relacionales | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Lógicos | `and`, `or`, `not` |
| Asignación compuesta | `+=`, `-=`, `*=`, `/=`, `**=` |
| Rendimiento simple | `(Pf - Pi) / Pi` |
| Rendimiento log | `ln(Pf / Pi)` |
| CAGR | `(VF / VI)^(1/n) - 1` |
| Bid-Ask spread | `ask - bid` |

---

## ✅ Autoevaluación

1. ¿Qué diferencia hay entre `10 / 3` y `10 // 3`?
2. ¿Por qué los quants usan rendimientos logarítmicos en lugar de simples?
3. ¿Cuál es el resultado de `2 ** 3 ** 2`? (piensa en precedencia)
4. ¿Qué es el bid-ask spread y por qué importa al trader?
5. Calcula el CAGR de una inversión que pasó de $5,000 a $12,000 en 8 años.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U03.md`: Tabla de precedencia, fórmulas rendimiento simple vs log
> - `project-U03.md`: CAGR, Sharpe simplificado, cuota de préstamo (sistema francés)
