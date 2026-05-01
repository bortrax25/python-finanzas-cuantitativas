# U12: EJERCICIOS — Funciones Avanzadas: Lambda, Decoradores y Closures

# ============================================================
# Ejercicio 1: Filtro y ranking con lambda
# Dada una lista de (ticker, PER, crecimiento %), usa:
# - filter + lambda para acciones con PER < 15 Y crecimiento > 10%
# - sorted + lambda para ordenar por crecimiento descendente
# ============================================================
print("=== Ejercicio 1: Filtro y Ranking con Lambda ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
    ("PFE", 14, 5),
    ("NVDA", 45, 30),
    ("BAC", 8, 9),
]

# Escribe tu código aquí



# Output esperado:
# Value+Growth: [('XOM', 10, 15), ('JPM', 9, 12), ('CVX', 11, 18)]
# Top crecimiento: [('NVDA', 45, 30), ('TSLA', 65, 25), ('CVX', 11, 18), ...]


# ============================================================
# Ejercicio 2: Ordenamiento por Sharpe Ratio
# Dada una lista de dicts con (ticker, retorno, volatilidad),
# calcula el Sharpe Ratio (rf=4%) y ordena de mayor a menor.
# ============================================================
print("\n=== Ejercicio 2: Ranking por Sharpe ===")
rf = 4
activos = [
    {"ticker": "AAPL", "retorno": 15.2, "volatilidad": 22.1},
    {"ticker": "MSFT", "retorno": 18.5, "volatilidad": 20.8},
    {"ticker": "TSLA", "retorno": 25.0, "volatilidad": 45.3},
    {"ticker": "JPM", "retorno": 10.8, "volatilidad": 18.2},
    {"ticker": "XOM", "retorno": 8.5, "volatilidad": 15.5},
    {"ticker": "NVDA", "retorno": 30.0, "volatilidad": 40.0},
]

# Escribe tu código aquí



# Output esperado:
# Ranking por Sharpe (rf=4%):
# 1. MSFT Sharpe=0.70 (ret=18.5%, vol=20.8%)
# 2. JPM Sharpe=0.37 (ret=10.8%, vol=18.2%)
# 3. NVDA Sharpe=0.65 (ret=30.0%, vol=40.0%)
# ...


# ============================================================
# Ejercicio 3: Decorador @medir_tiempo
# Crea un decorador @medir_tiempo que imprima el tiempo de ejecución.
# Aplícalo a una función calcular_var_historico(rendimientos, confianza=0.95).
# El VaR histórico es: ordenar rendimientos, tomar el percentil (1-confianza),
# y retornar el valor absoluto de ese percentil.
# ============================================================
print("\n=== Ejercicio 3: Decorador @medir_tiempo ===")
import time
from functools import wraps

# Escribe tu decorador y función aquí



rendimientos = [1.2, -0.5, 2.1, -3.8, 0.9, -1.2, 2.5, -0.8, 1.5, -2.3,
                0.7, -1.1, 3.2, -0.4, 1.8, -2.0, 0.5, -1.5, 2.8, -0.6]
var_95 = calcular_var_historico(rendimientos, 0.95)
print(f"VaR 95%: {var_95:.2f}%")

# Output esperado:
# [TIMER] calcular_var_historico: X.XXXXXXs
# VaR 95%: X.XX%


# ============================================================
# Ejercicio 4: Decorador @registrar_operacion
# Crea un decorador @registrar_operacion que registre:
# - Timestamp
# - Nombre de la función
# - Argumentos
# - Resultado
# Aplícalo a ejecutar_trade(ticker, tipo, cantidad, precio).
# ============================================================
print("\n=== Ejercicio 4: Decorador @registrar_operacion ===")
from datetime import datetime

# Escribe tu decorador y función aquí



resultado = ejecutar_trade("AAPL", "compra", 100, 175.50)
print(f"Resultado final: {resultado}")

# Output esperado:
# [2024-XX-XX XX:XX:XX] ejecutar_trade('AAPL', 'compra', 100, 175.5)
# [2024-XX-XX XX:XX:XX] Resultado: {'ticker': 'AAPL', 'monto_total': 17550.0}
# Resultado final: {'ticker': 'AAPL', 'monto_total': 17550.0}
