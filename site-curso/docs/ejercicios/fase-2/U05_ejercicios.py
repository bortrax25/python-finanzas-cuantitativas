# U05: EJERCICIOS — Condicionales if/elif/else

# ============================================================
# Ejercicio 1: Calculadora de impuesto a la renta
# Tramos progresivos simplificados:
# Hasta $10,000 → 10%
# De $10,001 a $50,000 → 15%
# De $50,001 a $100,000 → 20%
# Más de $100,000 → 25%
# Muestra el impuesto a pagar y la tasa efectiva
# ============================================================
print("=== Ejercicio 1: Impuesto a la Renta ===")
ingreso_anual = 75000

# Escribe tu código aquí



# Output esperado:
# Ingreso anual: $75,000.00
# Impuesto a pagar: $11,250.00
# Tasa efectiva: 15.00%


# ============================================================
# Ejercicio 2: Score crediticio
# Clasifica el riesgo según score:
# 750+ → "Excelente"
# 650-749 → "Bueno"
# 550-649 → "Regular"
# < 550 → "Malo"
# ============================================================
print("\n=== Ejercicio 2: Score Crediticio ===")
score = 720

# Escribe tu código aquí



# Output esperado:
# Score: 720 → Clasificación: Bueno


# ============================================================
# Ejercicio 3: Señal de medias móviles
# Dado precio_actual, media_corta (MA20) y media_larga (MA50)
# Señales:
#   MA20 cruza por ENCIMA de MA50 → "COMPRA (Golden Cross)"
#   MA20 cruza por DEBAJO de MA50 → "VENTA (Death Cross)"
#   MA20 == MA50 → "INDEFINIDO"
#   Si precio_actual > ambas → Tendencia "ALCISTA"
#   Si precio_actual < ambas → Tendencia "BAJISTA"
#   Otro → "LATERAL"
# ============================================================
print("\n=== Ejercicio 3: Señal de Trading ===")
precio_actual = 155.00
media_corta = 152.00
media_larga = 148.00

# Escribe tu código aquí



# Output esperado:
# Precio: $155.00 | MA20: $152.00 | MA50: $148.00
# Señal: COMPRA (Golden Cross)
# Tendencia: ALCISTA


# ============================================================
# Ejercicio 4: Oportunidad de arbitraje
# Dado precio en NYSE y en LSE (ambos convertidos a USD)
# Si diferencia > 1% y hay oportunidad:
#   Si NYSE < LSE → comprar NYSE, vender LSE
#   Si LSE < NYSE → comprar LSE, vender NYSE
# Sino: "Sin arbitraje"
# ============================================================
print("\n=== Ejercicio 4: Arbitraje ===")
precio_nyse = 150.00
precio_lse = 153.50
umbral_pct = 1.0

# Escribe tu código aquí



# Output esperado:
# NYSE: $150.00 | LSE: $153.50
# Diferencia: 2.33%
# Comprar NYSE → Vender LSE
# Ganancia estimada: 2.33%
