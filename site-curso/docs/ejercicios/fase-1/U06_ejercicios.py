# U06: EJERCICIOS — Bucles: Iterando sobre Series de Tiempo

# ============================================================
# Ejercicio 1: SMA 20 y detección de cruces dorados
# Dada una lista de 50 precios, calcula:
# - SMA de 5 días (ventana corta)
# - SMA de 20 días (ventana larga, si hay suficientes datos)
# Detecta el primer día en que la SMA corta cruza POR ENCIMA de la larga
# (Golden Cross). Si no hay cruce en los datos, indica "Sin cruce".
# ============================================================
print("=== Ejercicio 1: SMA y Golden Cross ===")
import random
random.seed(101)

precios = [100.0]
for _ in range(49):
    precios.append(precios[-1] * (1 + random.gauss(0.0003, 0.012)))

ventana_corta = 5
ventana_larga = 20

# Escribe tu código aquí



# Output esperado:
# SMA corta y larga calculadas.
# Primer Golden Cross detectado en día XX (o "Sin cruce")


# ============================================================
# Ejercicio 2: TIR por bisección
# Calcula la TIR de los flujos [-2000, 600, 700, 800, 900]
# Busca entre 0% y 100% con tolerancia 0.0001.
# Verifica que el VPN a la TIR sea ≈ 0.
# ============================================================
print("\n=== Ejercicio 2: TIR por Bisección ===")
flujos = [-2000, 600, 700, 800, 900]
tasa_min = 0.0
tasa_max = 1.0
tolerancia = 0.0001

# Escribe tu código aquí



# Output esperado:
# TIR encontrada: XX.XX%
# VPN a la TIR: $0.00


# ============================================================
# Ejercicio 3: Ruina del jugador (Gambler's Ruin)
# Empiezas con $1,000. Cada trade ganas o pierdes $100 con 50% de prob.
# Simula hasta duplicar ($2,000) o perder todo ($0).
# Muestra el número de trades y el resultado final.
# Usa while con break.
# ============================================================
print("\n=== Ejercicio 3: Ruina del Jugador ===")
import random
random.seed(42)

capital = 1000
objetivo_ganar = 2000
apuesta = 100
trades = 0

# Escribe tu código aquí



# Output esperado (con seed=42):
# Trade 1: Perdiste → $900
# Trade 2: Ganaste → $1000
# ...
# Trade X: Resultado → $XXXX
# Resultado: GANASTE/PERDISTE en X trades


# ============================================================
# Ejercicio 4: Máximo drawdown
# Encuentra la máxima caída porcentual desde un pico en esta serie.
# drawdown = (pico - precio_actual) / pico * 100
# Muestra el precio pico, el precio valle y el drawdown máximo.
# ============================================================
print("\n=== Ejercicio 4: Máximo Drawdown ===")
precios = [100, 105, 98, 92, 96, 88, 94, 85, 90, 82, 87, 95]

# Escribe tu código aquí



# Output esperado:
# Máximo drawdown: XX.XX%
# Pico: $XXX en posición X
# Valle: $XX en posición X
