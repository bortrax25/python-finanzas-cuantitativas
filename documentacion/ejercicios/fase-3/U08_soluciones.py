# U08: SOLUCIONES — Bucle while y Control de Flujo

# ============================================================
# Ejercicio 1: Ruina del jugador
# ============================================================
print("=== Ejercicio 1: Ruina del Jugador ===")
import random

capital = 1000
objetivo_ganar = 2000
apuesta = 100
trades = 0
random.seed(42)  # Para reproducibilidad

while capital > 0 and capital < objetivo_ganar:
    trades += 1
    if random.random() < 0.5:
        capital += apuesta
        print(f"Trade {trades}: Ganaste → ${capital}")
    else:
        capital -= apuesta
        print(f"Trade {trades}: Perdiste → ${capital}")

resultado = "GANASTE" if capital >= objetivo_ganar else "PERDISTE"
print(f"Resultado: {resultado} en {trades} trades")


# ============================================================
# Ejercicio 2: Tarjeta de crédito
# ============================================================
print("\n=== Ejercicio 2: Tarjeta de Crédito ===")
deuda = 5000.00
tasa_anual = 36
tasa_mensual = (tasa_anual / 100) / 12
pago_minimo_pct = 0.05
mes = 0
total_intereses = 0

while deuda > 0:
    mes += 1
    interes = deuda * tasa_mensual
    total_intereses += interes
    deuda += interes
    pago = deuda * pago_minimo_pct
    if pago > deuda:
        pago = deuda
    deuda -= pago
    if mes % 12 == 0:
        print(f"Año {mes//12}: Deuda ${deuda:,.2f}")

print(f"\nDeuda pagada en {mes} meses")
print(f"Total intereses pagados: ${total_intereses:,.2f}")


# ============================================================
# Ejercicio 3: Menú financiero
# ============================================================
print("\n=== Ejercicio 3: Menú Financiero ===")
print("(Demostración sin input — en tu código usarías input())")

def menu_financiero():
    pass  # Este ejercicio usa input(), se ejecuta interactivamente

print("Estructura del menú:")
print("while True:")
print("    opcion = input('Elige (1-4): ')")
print("    if opcion == '1': calcular_interes()")
print("    elif opcion == '2': convertir_moneda()")
print("    elif opcion == '3': calcular_cagr()")
print("    elif opcion == '4': break")


# ============================================================
# Ejercicio 4: Encontrar tasa por bisección
# ============================================================
print("\n=== Ejercicio 4: Tasa por Bisección ===")
monto = 10000
cuota = 888.49
plazo = 12
tasa_min = 0.0
tasa_max = 0.05
tolerancia = 0.0001

while (tasa_max - tasa_min) > tolerancia:
    tasa_media = (tasa_min + tasa_max) / 2
    vpn = -monto
    for t in range(1, plazo + 1):
        vpn += cuota / (1 + tasa_media) ** t
    if vpn > 0:
        tasa_min = tasa_media
    else:
        tasa_max = tasa_media

tasa_encontrada = (tasa_min + tasa_max) / 2
print(f"Tasa mensual encontrada: {tasa_encontrada:.4%}")
