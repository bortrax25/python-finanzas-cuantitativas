# U13-U15: EJERCICIOS — Funciones y Módulos

# ============================================================
# U13 - Ejercicio 1: Payback
# Escribe una función payback(inversion, flujos) que retorne el número de años
# ============================================================
print("=== U13: Payback ===")

# Escribe tu función aquí



# Prueba
print(payback(50000, [12000, 15000, 18000, 20000, 22000]))  # Debe retornar 4


# ============================================================
# U13 - Ejercicio 2: VPN (Valor Presente Neto)
# vpn = sum(flujo / (1 + tasa)^t ) - inversion_inicial
# ============================================================
print("\n=== U13: VPN ===")

# Escribe tu función aquí



print(vpn(10000, 0.10, [3000, 4000, 5000, 6000]))  # Esperado: ~$3,597


# ============================================================
# U14 - Ejercicio 1: Función con *args
# Escribe una función que reciba N rendimientos y retorne (promedio, max, min)
# ============================================================
print("\n=== U14: Estadísticas con *args ===")

# Escribe tu función aquí



print(estadisticas(5.2, -2.1, 3.8, -0.5, 4.2))  # (2.12, 5.2, -2.1)


# ============================================================
# U14 - Ejercicio 2: Ordenar con lambda
# Dada una lista de acciones (ticker, PER, crecimiento), ordena por:
# 1. PER ascendente (menor mejor)
# 2. Crecimiento descendente (mayor mejor)
# ============================================================
print("\n=== U14: Ordenar con lambda ===")
acciones = [("AAPL", 28, 8), ("XOM", 10, 15), ("JPM", 9, 12), ("TSLA", 65, 25)]

# Escribe tu código aquí



# Output esperado:
# Por PER: [('JPM', 9, 12), ('XOM', 10, 15), ('AAPL', 28, 8), ('TSLA', 65, 25)]
# Por Crecimiento: [('TSLA', 65, 25), ('XOM', 10, 15), ('JPM', 9, 12), ('AAPL', 28, 8)]


# ============================================================
# U15 - Ejercicio: Crear módulo financiero
# Crea una función que use datetime para calcular edad de una inversión
# ============================================================
print("\n=== U15: Edad de inversión ===")
from datetime import date

# Escribe tu función aquí



print(edad_inversion(2020, 1, 15))  # Años transcurridos desde 2020-01-15
