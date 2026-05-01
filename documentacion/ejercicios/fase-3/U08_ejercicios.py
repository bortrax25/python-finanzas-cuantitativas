# U08: EJERCICIOS — Bucle while y Control de Flujo

# ============================================================
# Ejercicio 1: Ruina del jugador
# Empiezas con $1,000. Cada trade ganas o pierdes $100 (50/50).
# Simula hasta duplicar ($2,000) o perder todo ($0).
# Muestra el número de trades, el resultado final y si "GANASTE" o "PERDISTE"
# ============================================================
print("=== Ejercicio 1: Ruina del Jugador ===")
import random

capital = 1000
objetivo_ganar = 2000
apuesta = 100
trades = 0

# Escribe tu código aquí



# Output esperado (varía por aleatoriedad):
# Trade 1: Perdiste → $900
# Trade 2: Ganaste → $1000
# ...
# Trade 24: Ganaste → $2000
# Resultado: GANASTE en 24 trades


# ============================================================
# Ejercicio 2: Intereses de tarjeta de crédito
# Deuda: $5,000 | Tasa anual: 36% | Pago mínimo: 5% de la deuda
# Calcula cuántos meses toma pagar asumiendo que SIEMPRE pagas el mínimo
# Muestra resumen anual
# ============================================================
print("\n=== Ejercicio 2: Tarjeta de Crédito ===")
deuda = 5000.00
tasa_anual = 36
tasa_mensual = (tasa_anual / 100) / 12
pago_minimo_pct = 0.05
mes = 0

# Escribe tu código aquí



# Output esperado (resumen):
# Mes 1: Deuda $5,000.00 | Interés $150.00 | Pago $250.00 | Nueva deuda $4,900.00
# ...
# Año 1: Deuda $X,XXX.XX
# Año 2: Deuda $X,XXX.XX
# ...
# Deuda pagada en X meses | Total intereses: $X,XXX.XX


# ============================================================
# Ejercicio 3: Menú financiero
# Crea un menú interactivo con while True:
#   1. Calcular interés compuesto
#   2. Convertir moneda (USD → PEN)
#   3. Calcular CAGR
#   4. Salir
# Valida que la opción sea 1-4. Usa funciones vacías con pass.
# ============================================================
print("\n=== Ejercicio 3: Menú Financiero ===")

# Escribe tu código aquí



# (Este ejercicio requiere input() del usuario)


# ============================================================
# Ejercicio 4: Encontrar tasa por bisección
# Encuentra la tasa mensual que hace que el VPN de un préstamo sea 0
# Datos: préstamo de $10,000, 12 cuotas fijas de $888.49
# Busca entre 0% y 5% mensual con tolerancia 0.0001
# ============================================================
print("\n=== Ejercicio 4: Tasa por Bisección ===")
monto = 10000
cuota = 888.49
plazo = 12
tasa_min = 0.0
tasa_max = 0.05
tolerancia = 0.0001

# Escribe tu código aquí



# Output esperado:
# Tasa mensual encontrada: 1.0000%
