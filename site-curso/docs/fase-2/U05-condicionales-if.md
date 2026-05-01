# U05: Condicionales if/elif/else

> **Lectura previa:** [U04: Estructuras de control](../fase-1/U04-estructuras-control.md)
> **Próxima unidad:** [U06: Condicionales anidados y operadores lógicos](./U06-condicionales-anidados.md)

---

## 1. Teoría

### 1.1 `if` — Tomar decisiones

`if` ejecuta un bloque de código **solo si una condición es verdadera**.

```python
# Sintaxis
if condicion:
    # código si la condición es True

# Ejemplo
precio = 150
if precio > 100:
    print("La acción está cara")
```

> ⚠️ **Indentación:** Python usa 4 espacios para delimitar bloques. Si olvidas la indentación, obtienes `IndentationError`.

### 1.2 `if/else` — Dos caminos

`else` ejecuta un bloque alternativo cuando la condición `if` es falsa.

```python
precio = 80
if precio > 100:
    print("Acción cara")
else:
    print("Precio razonable")   # ← se ejecuta esto
```

### 1.3 `if/elif/else` — Múltiples condiciones

`elif` (else if) permite verificar condiciones adicionales. Se evalúan **en orden** y solo se ejecuta el primer bloque verdadero.

```python
rendimiento = 8.5

if rendimiento > 20:
    print("Rendimiento excepcional")
elif rendimiento > 10:
    print("Buen rendimiento")
elif rendimiento > 0:
    print("Rendimiento positivo")     # ← se ejecuta esto
elif rendimiento > -5:
    print("Ligera pérdida")
else:
    print("Pérdida significativa")
```

### 1.4 Condiciones simplificadas (Truthy/Falsy)

Python evalúa ciertos valores como `True` o `False` en contextos booleanos:

| Valor | Se evalúa como |
|-------|---------------|
| `0`, `0.0` | `False` |
| `""`, `[]`, `{}` | `False` |
| `None` | `False` |
| Cualquier otro valor | `True` |

```python
# Verificar si una lista tiene elementos
acciones = ["AAPL", "MSFT"]
if acciones:
    print("Hay acciones en el portafolio")  # se ejecuta
else:
    print("Portafolio vacío")

# Verificar saldo
saldo = 0
if not saldo:
    print("Saldo en cero")  # se ejecuta
```

### 1.5 Operador ternario (if en una línea)

Para condiciones simples, Python tiene una sintaxis compacta:

```python
# Sintaxis: valor_si_verdadero if condicion else valor_si_falso

rendimiento = 5.2
estado = "ganancia" if rendimiento > 0 else "pérdida"
print(f"Resultado: {estado}")  # Resultado: ganancia

# Equivalente a:
if rendimiento > 0:
    estado = "ganancia"
else:
    estado = "pérdida"
```

### 1.6 Comparaciones encadenadas

Python permite encadenar comparaciones de forma natural:

```python
# Comparación encadenada
precio = 150
if 100 <= precio <= 200:
    print("Precio en rango esperado")

# Equivalente a:
if precio >= 100 and precio <= 200:
    print("Precio en rango esperado")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Clasificador de rendimientos

```python
rendimiento = float(input("Rendimiento del portafolio (%): "))

if rendimiento > 20:
    categoria = "EXCEPCIONAL"
elif rendimiento > 10:
    categoria = "BUENO"
elif rendimiento > 0:
    categoria = "POSITIVO"
elif rendimiento > -10:
    categoria = "PÉRDIDA MODERADA"
else:
    categoria = "PÉRDIDA SEVERA"

print(f"Categoría: {categoria} ({rendimiento:+.2f}%)")
```

### 2.2 Ejercicio guiado: Señal de trading simple

```python
precio_actual = 175.00
precio_entrada = 150.00
precio_stop = 140.00
precio_take = 180.00

if precio_actual >= precio_take:
    print("✅ Señal: CERRAR (TAKE-PROFIT)")
elif precio_actual <= precio_stop:
    print("🛑 Señal: CERRAR (STOP-LOSS)")
else:
    ganancia = precio_actual - precio_entrada
    ganancia_pct = (ganancia / precio_entrada) * 100
    print(f"MANTENER (Ganancia: {ganancia_pct:+.2f}%)")
```

### 2.3 Ejercicio guiado: Clasificador de perfil de riesgo

```python
edad = int(input("Edad: "))
ingresos = float(input("Ingresos mensuales: $"))
ahorros = float(input("Ahorros totales: $"))

if edad < 30 and ingresos > 3000:
    perfil = "Agresivo (joven con ingresos)"
elif edad < 50 and ahorros > 50000:
    perfil = "Moderado (mediana edad con ahorros)"
elif edad >= 60:
    perfil = "Conservador (próximo a jubilación)"
else:
    perfil = "Balanceado"

print(f"Perfil recomendado: {perfil}")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Clasificación de activos por capitalización de mercado

```python
# Market Cap en billones de USD
market_cap = float(input("Market Cap (billones USD): "))

if market_cap > 200:
    categoria = "Mega-cap"
elif market_cap > 10:
    categoria = "Large-cap"
elif market_cap > 2:
    categoria = "Mid-cap"
elif market_cap > 0.3:
    categoria = "Small-cap"
else:
    categoria = "Micro-cap"

print(f"Clasificación: {categoria}")
```

### 3.2 Indicador RSI simplificado

```python
rsi = float(input("Valor RSI: "))

if rsi > 70:
    print("⚠️ Sobrecompra — posible corrección")
elif rsi < 30:
    print("💡 Sobreventa — posible rebote")
else:
    print(f"Zona neutral (RSI: {rsi:.1f})")
```

---

## 4. Ejercicios Propuestos

1. **Calculadora de impuesto a la renta:** Según el ingreso anual, calcula el impuesto con tramos progresivos (10%, 15%, 20%).

2. **Clasificador de IMC con interpretación financiera:** Clasifica el "riesgo de crédito" basado en score crediticio.

3. **Señal de cruce de medias móviles:** Dado un precio, media corta y media larga, determina la señal.

4. **Verificador de arbitraje:** Dado un precio en NYSE y otro en LSE convertido, determina si hay oportunidad de arbitraje.

---

## 5. Resumen

| Estructura | Uso |
|-----------|-----|
| `if` | Ejecutar código si una condición es True |
| `if/else` | Dos caminos posibles |
| `if/elif/else` | Múltiples condiciones en cascada |
| Operador ternario | `x if cond else y` |
| Truthy/Falsy | `if variable:` (verifica si no es vacío/cero/None) |

---

## ✅ Autoevaluación

1. ¿Cuántos `elif` puede tener un bloque `if`?
2. ¿Qué imprime esto?
```python
x = 5
if x > 10:
    print("A")
elif x > 3:
    print("B")
elif x > 0:
    print("C")
```

3. Convierte a ternario:
```python
if precio > 100:
    estado = "caro"
else:
    estado = "barato"
```

4. Escribe un programa que clasifique un score crediticio:
   - 750+ → Excelente
   - 650-749 → Bueno
   - 550-649 → Regular
   - < 550 → Malo

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U05.md`: Estructura if/elif/else y operador ternario
> - `project-U05.md`: Clasificación por market cap y señal de trading
