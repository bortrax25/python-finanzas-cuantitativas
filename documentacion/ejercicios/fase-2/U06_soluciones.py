# U06: SOLUCIONES — Condicionales Anidados y Operadores Lógicos

# ============================================================
# Ejercicio 1: Hipoteca con LTV
# ============================================================
print("=== Ejercicio 1: Hipoteca con LTV ===")
valor_propiedad = 200000
monto_solicitado = 180000
score_crediticio = 680

ltv = (monto_solicitado / valor_propiedad) * 100

print(f"LTV: {ltv:.2f}%")
print(f"Score: {score_crediticio}")

if ltv > 95:
    print("❌ RECHAZADO — LTV superior al 95%")
elif ltv > 80:
    if score_crediticio >= 650:
        print("✅ APROBADO con seguro hipotecario")
    else:
        print("❌ RECHAZADO — Score insuficiente para LTV > 80%")
else:
    print("✅ APROBADO sin seguro hipotecario")


# ============================================================
# Ejercicio 2: Alertas de Portafolio
# ============================================================
print("\n=== Ejercicio 2: Alertas de Portafolio ===")
acciones = [
    ("AAPL", 30, -6.5),
    ("MSFT", 25, -3.2),
    ("TSLA", 15, -8.0),
    ("JPM", 20, 1.5),
    ("VIX", 10, 15.0),
]

for ticker, peso, cambio in acciones:
    if cambio < -5 and peso > 20:
        alerta = "🔴 ALERTA ROJA"
    elif cambio < -5:
        alerta = "🟡 ALERTA AMARILLA"
    else:
        alerta = "✅ NORMAL"
    print(f"{ticker}: {cambio:+.1f}% (peso {peso}%) → {alerta}")


# ============================================================
# Ejercicio 3: Validador de Orden
# ============================================================
print("\n=== Ejercicio 3: Validador de Orden ===")
tipo = "limit"
cantidad = 100
precio_limite = 0

if tipo not in ("market", "limit"):
    print("Orden inválida: Tipo debe ser 'market' o 'limit'")
elif cantidad <= 0:
    print("Orden inválida: Cantidad debe ser positiva")
elif tipo == "limit" and precio_limite <= 0:
    print("Orden inválida: Precio límite debe ser positivo")
else:
    print(f"✅ Orden válida: {tipo.upper()} {cantidad} acciones" +
          (f" @ ${precio_limite:.2f}" if tipo == "limit" else ""))


# ============================================================
# Ejercicio 4: Impuesto sobre dividendos
# ============================================================
print("\n=== Ejercicio 4: Impuesto Dividendos ===")
ticker = "AAPL"
dividendo_bruto = 1500.00

extranjeros = (".L", ".DE", ".HK", ".JP", ".HK")
es_extranjera = ticker.endswith(extranjeros)

print(f"{ticker} ({'Extranjera' if es_extranjera else 'Nacional'}) | Dividendo bruto: ${dividendo_bruto:,.2f}")

if es_extranjera:
    impuesto = dividendo_bruto * 0.30
    print(f"Impuesto (30%): ${impuesto:,.2f}")
else:
    exento = 1000.00
    base_imponible = max(0, dividendo_bruto - exento)
    impuesto = base_imponible * 0.10
    print(f"Exento: ${exento:,.2f} | Base imponible: ${base_imponible:,.2f}")
    print(f"Impuesto (10%): ${impuesto:,.2f}")

dividendo_neto = dividendo_bruto - impuesto
print(f"Dividendo neto: ${dividendo_neto:,.2f}")
