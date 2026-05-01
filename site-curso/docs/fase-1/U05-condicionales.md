# U05: Condicionales — Reglas de Negocio y Señales de Trading

> **Lectura previa:** [U04: Entrada, salida y manejo de errores](./U04-io-errores.md)
> **Próxima unidad:** [U06: Bucles — Iterando sobre Series de Tiempo](./U06-bucles.md)

---

## 1. Teoría

### 1.1 `if/elif/else` — Decisiones en cascada

```python
rendimiento = 8.5

if rendimiento > 20:
    print("Rendimiento excepcional")
elif rendimiento > 10:
    print("Buen rendimiento")
elif rendimiento > 0:
    print("Rendimiento positivo")       # ← se ejecuta esto
elif rendimiento > -5:
    print("Ligera pérdida")
else:
    print("Pérdida significativa")
```

> ⚠️ Python usa 4 espacios de indentación para delimitar bloques.

### 1.2 Operador ternario (if en una línea)

```python
# Sintaxis: valor_si_verdadero if condicion else valor_si_falso

rendimiento = 5.2
estado = "ganancia" if rendimiento > 0 else "pérdida"

# Equivalente a 4 líneas con if/else
```

### 1.3 `match/case` (Python 3.10+) — Pattern matching

El `match/case` es un switch moderno que permite matching por valor y por estructura:

```python
# Clasificación de orden de trading
orden = "limit"

match orden:
    case "market":
        comision_pct = 0.001
    case "limit":
        comision_pct = 0.002
    case "stop":
        comision_pct = 0.003
    case _:
        comision_pct = 0.005

print(f"Comisión: {comision_pct:.1%}")

# Matching con guardas (condiciones)
score = 720
match score:
    case s if s >= 750:
        rating = "AAA"
    case s if s >= 650:
        rating = "BBB"
    case s if s >= 550:
        rating = "CCC"
    case _:
        rating = "D"
```

### 1.4 Condicionales anidados

```python
precio = 85
tendencia = "alcista"

if precio < 100:                        # Primer filtro
    if tendencia == "alcista":          # Segundo filtro
        print("COMPRAR — precio bajo + tendencia alcista")
    else:
        print("ESPERAR — precio bajo pero tendencia bajista")
else:
    print("NO COMPRAR — precio elevado")
```

> 💡 Más de 2-3 niveles de anidación es difícil de leer. Refactoriza con `and`/`or`.

### 1.5 Cortocircuito lógico

Python evalúa de izquierda a derecha y para en cuanto conoce el resultado:

```python
# and: si la primera es False, la segunda NUNCA se evalúa
cuenta_activa = False
saldo = 1000000
if cuenta_activa and saldo > 1000:    # saldo > 1000 no se evalúa
    print("Puedes retirar")

# or: si la primera es True, la segunda NUNCA se evalúa
es_premium = True
if es_premium or verificar_saldo():     # verificar_saldo() no se llama
    print("Acceso permitido")

# Precedencia lógica: NOT > AND > OR
# Usa paréntesis para claridad
resultado = (a and b) or c    # Claro
resultado = a and b or c      # Ambigüo
```

### 1.6 Truthy/Falsy y comparaciones encadenadas

```python
# Valores que se evalúan como False: 0, 0.0, "", [], {}, None
acciones = ["AAPL", "MSFT"]
if acciones:
    print("Portafolio con posiciones")

# Comparaciones encadenadas
precio = 150
if 100 <= precio <= 200:
    print("Precio en rango esperado")   # Más legible que precio >= 100 and precio <= 200
```

### 1.7 Validación de entrada con condicionales

```python
entrada = input("Edad: ")

if entrada.isdigit():
    edad = int(entrada)
    if edad >= 18:
        print("Acceso permitido")
    else:
        print("Debes ser mayor de edad")
else:
    print("Error: ingresa un número válido")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Scoring de inversión (3 criterios)

```python
liquidez = float(input("Ratio de liquidez (>1 bueno): "))
endeudamiento = float(input("Ratio de endeudamiento (<0.5 bueno): "))
crecimiento = float(input("Crecimiento de ventas (%): "))

puntaje = 0

puntaje += 3 if liquidez > 2 else (2 if liquidez > 1 else 0)
puntaje += 3 if endeudamiento < 0.3 else (2 if endeudamiento < 0.5 else 0)
puntaje += 4 if crecimiento > 20 else (2 if crecimiento > 10 else 1)

print(f"Puntaje total: {puntaje}/10")
if puntaje >= 7:
    print("INVERTIR")
elif puntaje >= 4:
    print("ANALIZAR MÁS")
else:
    print("DESCARTAR")
```

### 2.2 Ejercicio guiado: Señal de trading con medias móviles

```python
precio_actual = 155.00
media_corta = 152.00    # MA20
media_larga = 148.00    # MA50

# Señal de cruce
if media_corta > media_larga:
    senal = "COMPRA (Golden Cross)"
elif media_corta < media_larga:
    senal = "VENTA (Death Cross)"
else:
    senal = "INDEFINIDO"

# Tendencia del precio
if precio_actual > media_corta and precio_actual > media_larga:
    tendencia = "ALCISTA"
elif precio_actual < media_corta and precio_actual < media_larga:
    tendencia = "BAJISTA"
else:
    tendencia = "LATERAL"

print(f"Precio: ${precio_actual:.2f} | MA20: ${media_corta:.2f} | MA50: ${media_larga:.2f}")
print(f"Señal: {senal}")
print(f"Tendencia: {tendencia}")
```

**Output:**
```
Precio: $155.00 | MA20: $152.00 | MA50: $148.00
Señal: COMPRA (Golden Cross)
Tendencia: ALCISTA
```

### 2.3 Ejercicio guiado: Aprobación de crédito (lógica bancaria real)

```python
ingresos = float(input("Ingresos mensuales: $"))
score = int(input("Score crediticio: "))
deuda = float(input("Deuda actual: $"))
monto = float(input("Monto solicitado: $"))

relacion_deuda = deuda / ingresos if ingresos > 0 else 999

if score >= 700 and relacion_deuda <= 0.4 and monto <= ingresos * 6:
    print("CRÉDITO APROBADO")
elif score >= 650 and relacion_deuda <= 0.35:
    print("APROBADO con tasa mayor")
elif score >= 600 and relacion_deuda <= 0.3:
    print("APROBADO con garantía")
else:
    if score < 600:
        print("RECHAZADO: Score insuficiente")
    elif relacion_deuda > 0.4:
        print("RECHAZADO: Relación deuda/ingreso alta")
    else:
        print("RECHAZADO: Monto excede capacidad")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Sistema de alertas de trading

```python
# Integrar alertas con múltiples criterios
precio_entrada = 150.00
precio_actual = 175.00
stop_loss_pct = 7
take_profit_pct = 15
volatilidad = 25

precio_stop = precio_entrada * (1 - stop_loss_pct / 100)
precio_take = precio_entrada * (1 + take_profit_pct / 100)

if precio_actual >= precio_take:
    print(f"TAKE-PROFIT: +{(precio_actual/precio_entrada - 1)*100:.1f}%")
elif precio_actual <= precio_stop:
    print(f"STOP-LOSS: {(precio_actual/precio_entrada - 1)*100:.1f}%")
elif volatilidad > 30:
    print("ALERTA: Reducir posición (alta volatilidad)")
else:
    ganancia = (precio_actual / precio_entrada - 1) * 100
    print(f"Mantener posición ({ganancia:+.1f}%)")
```

### 3.2 Clasificación crediticia institucional

```python
# Ratings de S&P / Moody's traducidos a umbrales numéricos
def clasificar_bono(ytm_spread, leverage_ratio, coverage_ratio):
    """
    ytm_spread: spread sobre Treasuries (puntos básicos)
    leverage_ratio: Deuda/EBITDA
    coverage_ratio: EBITDA/Intereses
    """
    if ytm_spread < 100 and leverage_ratio < 2 and coverage_ratio > 5:
        return "AAA/AA (Investment Grade)"
    elif ytm_spread < 200 and leverage_ratio < 3 and coverage_ratio > 3:
        return "A/BBB (Investment Grade)"
    elif ytm_spread < 400 and leverage_ratio < 4 and coverage_ratio > 1.5:
        return "BB (High Yield)"
    elif ytm_spread < 700:
        return "B (Speculative)"
    else:
        return "CCC/Default (Distressed)"

print(clasificar_bono(150, 2.5, 4.0))  # A/BBB (Investment Grade)
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-1/U05_ejercicios.py`

1. **Calculadora de impuesto a la renta:** Tramos progresivos (10%, 15%, 20%, 25%).

2. **Score crediticio:** Clasifica 750+ Excelente, 650-749 Bueno, 550-649 Regular, <550 Malo.

3. **Señal de medias móviles:** MA20 vs MA50 → Golden Cross / Death Cross + tendencia.

4. **Alerta de portafolio:** Si cae >5% Y peso >20% → alerta roja. Si solo cae >5% → amarilla.

---

## 5. Resumen

| Concepto | Sintaxis |
|---------|---------|
| if/elif/else | `if cond: ... elif cond: ... else: ...` |
| Ternario | `x if cond else y` |
| match/case | `match var: case patrón: ... case _: ...` |
| Anidados | `if a: if b: ...` (máx. 2-3 niveles) |
| Cortocircuito | `False and x` → no evalúa x |
| Encadenado | `10 <= x <= 20` |

---

## ✅ Autoevaluación

1. ¿Cuántos `elif` puede tener un bloque `if`?
2. Convierte a ternario: `if precio > 100: estado = "caro" else: estado = "barato"`
3. ¿Qué imprime `print(False and 1/0)`? ¿Por qué?
4. ¿Cuándo usarías `match/case` en vez de `if/elif`?
5. Clasifica un score de 720 con match/case y guardas.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U05.md`: if/elif/else, ternario, match/case, cortocircuito
> - `project-U05.md`: Scoring de inversión, señal de trading, aprobación de crédito
