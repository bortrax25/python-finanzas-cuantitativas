# U05: SOLUCIONES — Condicionales: Reglas de Negocio y Señales de Trading

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
# Ejercicio 2: Score Crediticio
# ============================================================
print("\n=== Ejercicio 2: Score Crediticio ===")
score = 720

match score:
    case s if s >= 750:
        clasificacion = "Excelente (AAA)"
    case s if s >= 650:
        clasificacion = "Bueno (BBB)"
    case s if s >= 550:
        clasificacion = "Regular (CCC)"
    case _:
        clasificacion = "Malo (D)"

print(f"Score: {score} → Clasificación: {clasificacion}")


# ============================================================
# Ejercicio 3: Señal de Trading
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
# Ejercicio 4: Alertas de Portafolio
# ============================================================
print("\n=== Ejercicio 4: Alertas de Portafolio ===")
acciones = [
    ("AAPL", 30, -6.5),
    ("MSFT", 25, -3.2),
    ("TSLA", 15, -8.0),
    ("JPM", 20, 1.5),
    ("VIX", 10, 15.0),
]

for ticker, peso, cambio in acciones:
    if cambio < -5 and peso > 20:
        alerta = "ALERTA ROJA"
    elif cambio < -5:
        alerta = "ALERTA AMARILLA"
    else:
        alerta = "NORMAL"
    print(f"{ticker}: {cambio:+.1f}% (peso {peso}%) → {alerta}")
