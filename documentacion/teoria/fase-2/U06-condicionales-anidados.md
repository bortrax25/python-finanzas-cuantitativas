# U06: Condicionales Anidados y Operadores Lógicos

> **Lectura previa:** [U05: Condicionales if/elif/else](./U05-condicionales-if.md)
> **Próxima unidad:** [U07: Bucle for y range()](../fase-3/U07-for-range.md)

---

## 1. Teoría

### 1.1 Condicionales anidados

Un condicional **dentro de otro condicional**. Permite decisiones con múltiples criterios jerárquicos.

```python
# Sintaxis
if condicion_externa:
    if condicion_interna:
        # código
    else:
        # código
else:
    # código
```

```python
# Ejemplo: Decisión de inversión con múltiples criterios
precio = 85
tendencia = "alcista"

if precio < 100:                        # Primer filtro
    if tendencia == "alcista":          # Segundo filtro
        print("✅ COMPRAR — precio bajo + tendencia alcista")
    else:
        print("⏳ ESPERAR — precio bajo pero tendencia bajista")
else:
    print("❌ NO COMPRAR — precio elevado")
```

### 1.2 Operadores lógicos profundizados

| Operador | Significado | Tabla de verdad |
|----------|------------|----------------|
| `and` | Ambas True | `True and True → True` |
| `or` | Al menos una True | `False or True → True` |
| `not` | Negación | `not True → False` |

```python
# and: ambas condiciones deben cumplirse
precio = 85
volumen = 1000000
if precio < 100 and volumen > 500000:
    print("Señal de compra fuerte")

# or: al menos una condición
efectivo = 5000
credito = 10000
if efectivo > 10000 or credito > 5000:
    print("Puedes invertir")

# not: negación
mercado_abierto = False
if not mercado_abierto:
    print("Mercado cerrado, no puedes operar")
```

### 1.3 Cortocircuito lógico (short-circuit evaluation)

Python evalúa de izquierda a derecha y **se detiene en cuanto conoce el resultado**.

```python
# and: si la primera es False, no evalúa la segunda
cuenta_activa = False
saldo = 1000000
if cuenta_activa and saldo > 1000:    # saldo > 1000 NUNCA se evalúa
    print("Puedes retirar")

# or: si la primera es True, no evalúa la segunda
es_premium = True
saldo_minimo = 500
if es_premium or saldo_minimo > 1000:  # saldo_minimo NUNCA se evalúa
    print("Acceso permitido")
```

### 1.4 Combinar `and`, `or`, `not`

Usa paréntesis para clarificar la precedencia:

```python
# Sin paréntesis: ambiguo
if a and b or c:       # ¿(a and b) or c  o  a and (b or c)?

# Con paréntesis: claro
if (a and b) or c:     # Se cumple si (a y b) o solo c
if a and (b or c):     # Se cumple si a y (b o c)
```

```python
# Ejemplo financiero
tiene_capital = True
mercado_alcista = True
conoce_riesgo = False

# Puede invertir si: tiene capital Y (mercado alcista O conoce el riesgo)
if tiene_capital and (mercado_alcista or conoce_riesgo):
    print("Puede invertir")    # True and (True or False) = True
```

### 1.5 Validación de entrada con condicionales

Patrón común para evitar errores con `input()`:

```python
entrada = input("Ingresa tu edad: ")

if entrada.isdigit():               # Verifica que sea número
    edad = int(entrada)
    if edad >= 18:
        print("Acceso permitido")
    else:
        print("Debes ser mayor de edad")
else:
    print("Error: ingresa un número válido")
```

### 1.6 Condicionales anidados vs planos (`elif`)

**Anidado** (legible para jerarquías):
```python
if tipo_cuenta == "premium":
    if saldo >= 10000:
        tasa = 0.05
    else:
        tasa = 0.03
else:
    tasa = 0.01
```

**Plano con `and`** (legible para combinaciones):
```python
if tipo_cuenta == "premium" and saldo >= 10000:
    tasa = 0.05
elif tipo_cuenta == "premium" and saldo < 10000:
    tasa = 0.03
else:
    tasa = 0.01
```

> 💡 Si tienes más de 2 niveles de anidación, replantea la lógica. Código muy anidado es difícil de leer.

---

## 2. Práctica

### 2.1 Ejercicio guiado: Sistema de scoring de inversión

```python
# Tres criterios con pesos
liquidez = float(input("Ratio de liquidez (>1 es bueno): "))
endeudamiento = float(input("Ratio de endeudamiento (<0.5 es bueno): "))
crecimiento = float(input("Crecimiento de ventas (%): "))

puntaje = 0

if liquidez > 2:
    puntaje += 3
elif liquidez > 1:
    puntaje += 2
else:
    puntaje += 0

if endeudamiento < 0.3:
    puntaje += 3
elif endeudamiento < 0.5:
    puntaje += 2
else:
    puntaje += 0

if crecimiento > 20:
    puntaje += 4
elif crecimiento > 10:
    puntaje += 2
else:
    puntaje += 1

print(f"Puntaje total: {puntaje}/10")
if puntaje >= 7:
    print("✅ INVERTIR")
elif puntaje >= 4:
    print("⏳ ANALIZAR MÁS")
else:
    print("❌ DESCARTAR")
```

### 2.2 Ejercicio guiado: Arbitraje entre exchanges

```python
precio_nyse = float(input("Precio en NYSE (USD): $"))
precio_lse = float(input("Precio en LSE (USD): $"))
comision = 0.005  # 0.5% por operación

diferencia = abs(precio_nyse - precio_lse)
costo_operacion = (precio_nyse + precio_lse) * comision / 2

if diferencia > costo_operacion:
    if precio_nyse < precio_lse:
        print(f"Comprar NYSE (${precio_nyse}) → Vender LSE (${precio_lse})")
        ganancia = diferencia - costo_operacion
    else:
        print(f"Comprar LSE (${precio_lse}) → Vender NYSE (${precio_nyse})")
        ganancia = diferencia - costo_operacion
    print(f"Ganancia estimada: ${ganancia:.2f}")
else:
    print("Sin oportunidad de arbitraje (costo > diferencia)")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Aprobación de crédito (lógica real bancaria)

```python
ingresos = float(input("Ingresos mensuales: $"))
score_crediticio = int(input("Score crediticio: "))
deuda_actual = float(input("Deuda actual: $"))
monto_solicitado = float(input("Monto solicitado: $"))

relacion_deuda_ingreso = deuda_actual / ingresos if ingresos > 0 else 999

if score_crediticio >= 700:
    if relacion_deuda_ingreso <= 0.4:
        if monto_solicitado <= ingresos * 6:
            print("✅ CRÉDITO APROBADO")
        else:
            print("❌ Monto excede tu capacidad")
    else:
        print("❌ Relación deuda/ingreso muy alta")
else:
    print("❌ Score crediticio insuficiente")
```

### 3.2 Estrategia de cobertura (hedge)

```python
posicion_actual = "larga"     # larga o corta
volatilidad = 25              # porcentaje
correlacion = -0.7            # con el activo de cobertura

if posicion_actual == "larga":
    if volatilidad > 20 and correlacion < -0.5:
        print("🛡️ Cobertura recomendada: PUT protectora")
    elif volatilidad > 20:
        print("⚠️ Alta volatilidad: reducir posición")
    else:
        print("✅ Posición sin cobertura necesaria")
else:
    print("Posición corta — estrategia diferente requerida")
```

---

## 4. Ejercicios Propuestos

1. **Calculadora de hipoteca 2.0:** Clasifica la hipoteca según LTV (Loan-to-Value). Si LTV > 80%, requiere seguro. Si además el score es < 650, rechazar.

2. **Sistema de alertas de portafolio:** Si una acción cae más del 5% Y representa más del 20% del portafolio, alerta roja. Si solo cae más del 5%, alerta amarilla.

3. **Validador de orden de trading:** Verifica que el tipo de orden (market/limit) sea válido, que la cantidad > 0, y que el precio límite (si aplica) sea positivo.

4. **Calculadora de dividendos con impuestos:** Calcula el dividendo neto según si la acción es nacional (10% impuesto) o extranjera (30% impuesto) y si el monto excede el mínimo exento.

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Anidado | `if ... if ... else ... else` |
| Cortocircuito | `False and x` → no evalúa x |
| Paréntesis lógicos | `(a and b) or c` |
| Validación | `if entrada.isdigit()` |
| Máx. anidación | 2-3 niveles recomendado |

---

## ✅ Autoevaluación

1. ¿Qué imprime `print(False and 1/0)`? ¿Por qué?
2. ¿Qué imprime `print(True or 1/0)`?
3. Simplifica usando `and`/`or`:
```python
if edad >= 18:
    if tiene_licencia:
        print("Puede conducir")
```

4. Escribe un validador de contraseña que requiera: mínimo 8 caracteres, al menos una mayúscula y al menos un número.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U06.md`: Cortocircuito lógico y tabla de verdad and/or/not
> - `project-U06.md`: Sistema de scoring de inversión y aprobación de crédito
