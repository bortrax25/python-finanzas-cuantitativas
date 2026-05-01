# U05: SOLUCIONES — Condicionales if/elif/else

# ============================================================
# Ejercicio 1: Impuesto a la Renta
# ============================================================
print("=== Ejercicio 1: Impuesto a la Renta ===")
ingreso_anual = 75000

if ingreso_anual <= 10000:
    impuesto = ingreso_anual * 0.10
elif ingreso_anual <= 50000:
    impuesto = 1000 + (ingreso_anual - 10000) * 0.15
elif ingreso_anual <= 100000:
    impuesto = 1000 + 6000 + (ingreso_anual - 50000) * 0.20
else:
    impuesto = 1000 + 6000 + 10000 + (ingreso_anual - 100000) * 0.25

tasa_efectiva = (impuesto / ingreso_anual) * 100

print(f"Ingreso anual: ${ingreso_anual:,.2f}")
print(f"Impuesto a pagar: ${impuesto:,.2f}")
print(f"Tasa efectiva: {tasa_efectiva:.2f}%")


# ============================================================
# Ejercicio 2: Score crediticio
# ============================================================
print("\n=== Ejercicio 2: Score Crediticio ===")
score = 720

if score >= 750:
    clasificacion = "Excelente"
elif score >= 650:
    clasificacion = "Bueno"
elif score >= 550:
    clasificacion = "Regular"
else:
    clasificacion = "Malo"

print(f"Score: {score} → Clasificación: {clasificacion}")


# ============================================================
# Ejercicio 3: Señal de medias móviles
# ============================================================
print("\n=== Ejercicio 3: Señal de Trading ===")
precio_actual = 155.00
media_corta = 152.00
media_larga = 148.00

if media_corta > media_larga:
    senal = "COMPRA (Golden Cross)"
elif media_corta < media_larga:
    senal = "VENTA (Death Cross)"
else:
    senal = "INDEFINIDO"

if precio_actual > media_corta and precio_actual > media_larga:
    tendencia = "ALCISTA"
elif precio_actual < media_corta and precio_actual < media_larga:
    tendencia = "BAJISTA"
else:
    tendencia = "LATERAL"

print(f"Precio: ${precio_actual:.2f} | MA20: ${media_corta:.2f} | MA50: ${media_larga:.2f}")
print(f"Señal: {senal}")
print(f"Tendencia: {tendencia}")


# ============================================================
# Ejercicio 4: Oportunidad de arbitraje
# ============================================================
print("\n=== Ejercicio 4: Arbitraje ===")
precio_nyse = 150.00
precio_lse = 153.50
umbral_pct = 1.0

diferencia_pct = abs(precio_nyse - precio_lse) / min(precio_nyse, precio_lse) * 100

print(f"NYSE: ${precio_nyse:.2f} | LSE: ${precio_lse:.2f}")
print(f"Diferencia: {diferencia_pct:.2f}%")

if diferencia_pct > umbral_pct:
    if precio_nyse < precio_lse:
        print("Comprar NYSE → Vender LSE")
    else:
        print("Comprar LSE → Vender NYSE")
    print(f"Ganancia estimada: {diferencia_pct:.2f}%")
else:
    print("Sin arbitraje")
