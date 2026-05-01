# U06: EJERCICIOS — Condicionales Anidados y Operadores Lógicos

# ============================================================
# Ejercicio 1: Calculadora de hipoteca 2.0 (con LTV)
# LTV = monto_solicitado / valor_propiedad * 100
# Reglas:
#   LTV <= 80% → Aprobado sin seguro
#   LTV > 80% y score >= 650 → Aprobado CON seguro hipotecario
#   LTV > 80% y score < 650 → Rechazado
#   LTV > 95% → Rechazado (independiente del score)
# ============================================================
print("=== Ejercicio 1: Hipoteca con LTV ===")
valor_propiedad = 200000
monto_solicitado = 180000
score_crediticio = 680

# Escribe tu código aquí



# Output esperado:
# LTV: 90.00%
# Score: 680
# ✅ APROBADO con seguro hipotecario


# ============================================================
# Ejercicio 2: Sistema de alertas de portafolio
# Datos:
#   AAPL: peso 30%, cambio -6.5%
#   MSFT: peso 25%, cambio -3.2%
#   TSLA: peso 15%, cambio -8.0%
#   JPM: peso 20%, cambio 1.5%
#   VIX: peso 10%, cambio 15.0%
# Reglas:
#   Si cae > 5% Y peso > 20% → 🔴 ALERTA ROJA
#   Si solo cae > 5% → 🟡 ALERTA AMARILLA
#   Otro → ✅ NORMAL
# ============================================================
print("\n=== Ejercicio 2: Alertas de Portafolio ===")
acciones = [
    ("AAPL", 30, -6.5),
    ("MSFT", 25, -3.2),
    ("TSLA", 15, -8.0),
    ("JPM", 20, 1.5),
    ("VIX", 10, 15.0),
]

# Escribe tu código aquí



# Output esperado:
# AAPL: -6.5% (peso 30%) → 🔴 ALERTA ROJA
# MSFT: -3.2% (peso 25%) → ✅ NORMAL
# TSLA: -8.0% (peso 15%) → 🟡 ALERTA AMARILLA
# JPM: 1.5% (peso 20%) → ✅ NORMAL
# VIX: 15.0% (peso 10%) → ✅ NORMAL


# ============================================================
# Ejercicio 3: Validador de orden de trading
# Valida estos campos:
#   tipo: "market" o "limit" (string)
#   cantidad: debe ser un entero positivo
#   precio_limite: requerido SOLO si tipo == "limit"
#   Si tipo == "market" y cantidad > 0 → "Orden válida"
#   Si tipo == "limit" y cantidad > 0 y precio > 0 → "Orden válida"
#   Otro caso → "Orden inválida: <razón>"
# ============================================================
print("\n=== Ejercicio 3: Validador de Orden ===")
tipo = "limit"
cantidad = 100
precio_limite = 0

# Escribe tu código aquí



# Output esperado:
# Orden inválida: Precio límite debe ser positivo


# ============================================================
# Ejercicio 4: Impuesto sobre dividendos
# Reglas:
#   Acción nacional (ticker no termina en .L, .DE, .HK):
#     Dividendo <= $1,000 → exento
#     Dividendo > $1,000 → 10% sobre el excedente
#   Acción extranjera:
#     Siempre paga 30% (sin mínimo exento)
# Muestra el dividendo neto (después de impuestos)
# ============================================================
print("\n=== Ejercicio 4: Impuesto Dividendos ===")
ticker = "AAPL"
dividendo_bruto = 1500.00

# Escribe tu código aquí



# Output esperado:
# AAPL (Nacional) | Dividendo bruto: $1,500.00
# Exento: $1,000.00 | Base imponible: $500.00
# Impuesto (10%): $50.00
# Dividendo neto: $1,450.00
