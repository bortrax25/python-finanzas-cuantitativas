# ✅ Soluciones: U04 — Fase 1

> [← Volver a ejercicios Fase 1](index.md) | [📥 Descargar .py](U04_soluciones)

---

```python
# U04: SOLUCIONES — Entrada, Salida y Manejo de Errores

# ============================================================
# Ejercicio 1: Perfil de riesgo
# ============================================================
print("=== Ejercicio 1: Perfil de Riesgo ===")

nombre = "Ana López"
edad = 32
ingresos = 5000.00
ahorros = 25000.00
tolerancia = 7

print("=" * 42)
print("PERFIL DEL INVERSIONISTA")
print("=" * 42)
print(f"{'Nombre:':<20} {nombre}")
print(f"{'Edad:':<20} {edad} años")
print(f"{'Ingresos:':<20} ${ingresos:,.2f}/mes")
print(f"{'Ahorros:':<20} ${ahorros:,.2f}")
print(f"{'Tolerancia:':<20} {tolerancia}/10 (Moderado-Alto)")
print("=" * 42)


# ============================================================
# Ejercicio 2: Calculadora DCA
# ============================================================
print("\\n=== Ejercicio 2: Calculadora DCA ===")

compras = [(100, 10), (90, 12), (110, 8)]

total_invertido = 0
total_acciones = 0

for i, (precio, cantidad) in enumerate(compras, start=1):
    subtotal = precio * cantidad
    total_invertido += subtotal
    total_acciones += cantidad
    print(f"Compra {i} - Precio: ${precio} | Cantidad: {cantidad} → ${subtotal:,.2f}")

precio_promedio = total_invertido / total_acciones

print("-" * 41)
print(f"Total invertido: ${total_invertido:,.2f}")
print(f"Total acciones: {total_acciones}")
print(f"Precio promedio: ${precio_promedio:,.2f}")


# ============================================================
# Ejercicio 3: Depuración — 5 errores corregidos
# ============================================================
print("\\n=== Ejercicio 3: Depuración ===")

# ERROR 1: input() retorna str, hay que convertir a float
# ERROR 2: Falta cerrar paréntesis en float(input(...))
# ERROR 3: Error de sintaxis: input"Tiempo" → input("Tiempo")
# ERROR 4: capital es str, no se puede multiplicar por float
# ERROR 5: print(str + float) → usar f-string

capital = 10000.0
tasa = 5.0 / 100
tiempo = 3.0
interes = capital * tasa * tiempo
print(f"Interés ganado: ${interes:,.2f}")

print("\\nErrores encontrados:")
print("1. input() no se convertía a float")
print("2. Faltaba cerrar paréntesis en float(input(...))")
print("3. Error sintaxis: input\\"Tiempo\\" → input(\\"Tiempo\\")")
print("4. capital (str) multiplicado por tasa (float)")
print("5. print(str + float) → usar f-string")


# ============================================================
# Ejercicio 4: Conversor de monedas interactivo
# ============================================================
print("\\n=== Ejercicio 4: Conversor Interactivo ===")

monto_usd = 1000.00
tipo_pen = 3.75
tipo_eur = 0.92

assert tipo_pen > 0, "El tipo de cambio PEN debe ser positivo"
assert tipo_eur > 0, "El tipo de cambio EUR debe ser positivo"

monto_pen = monto_usd * tipo_pen
monto_eur = monto_usd * tipo_eur

print("=" * 36)
print("CONVERSIÓN DE MONEDA")
print("=" * 36)
print(f"{'USD:':<8} ${monto_usd:>25,.2f}")
print(f"{'PEN:':<8} S/ {monto_pen:>24,.2f}")
print(f"{'EUR:':<8} € {monto_eur:>25,.2f}")
print("=" * 36)
```

---

> [📥 Descargar archivo .py](U04_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 1](index.md)
