# U01: EJERCICIOS — Jupyter Notebooks y Flujo de Trabajo Cuantitativo

# ============================================================
# Ejercicio 1: Simulación de precios y gráfico
# Simula 252 precios diarios de una acción que empieza en $150
# usando un retorno diario promedio de 0.05% y volatilidad diaria 1.5%.
# Grafica la evolución del precio con matplotlib.
# ============================================================
print("=== Ejercicio 1: Simulación de Precios ===")
import random

random.seed(123)
precio = 150.00
media_diaria = 0.0005
vol_diaria = 0.015
dias = 252

precios = [precio]

# Escribe tu código aquí



# Output esperado:
# Precio inicial: $150.00
# Precio final: $XXX.XX
# Rendimiento total: XX.XX%
# [Se mostraría un gráfico de línea con los 252 precios]


# ============================================================
# Ejercicio 2: Cálculo de retornos y volatilidad
# Con los precios generados en el Ejercicio 1, calcula:
# - Retorno diario promedio (%)
# - Volatilidad diaria (%)
# - Volatilidad anualizada (diaria * sqrt(252))
# - Retorno total acumulado (%)
# ============================================================
print("\n=== Ejercicio 2: Estadísticas del Activo ===")
# Usa la lista precios del Ejercicio 1

# Escribe tu código aquí



# Output esperado:
# Retorno diario promedio: X.XXXX%
# Volatilidad diaria: X.XXXX%
# Volatilidad anualizada: XX.XX%
# Retorno total acumulado: XX.XX%


# ============================================================
# Ejercicio 3: Reporte de portafolio
# Dado un portafolio de 5 activos con pesos y rendimientos,
# muestra una tabla formateada y un gráfico de torta con matplotlib.
# ============================================================
print("\n=== Ejercicio 3: Reporte de Portafolio ===")
import matplotlib.pyplot as plt

portafolio = [
    ("AAPL", 30.0, 15.2),
    ("MSFT", 25.0, 22.1),
    ("GOOGL", 20.0, 8.5),
    ("AMZN", 15.0, -3.2),
    ("META", 10.0, 12.8),
]
# (ticker, peso %, rendimiento %)

# Escribe tu código aquí



# Output esperado:
# Activo    Peso     Rendimiento
# AAPL      30.0%    +15.20%
# MSFT      25.0%    +22.10%
# GOOGL     20.0%    +8.50%
# AMZN      15.0%    -3.20%
# META      10.0%    +12.80%
# -----------------------------------
# Portafolio: 100.0% | Rend. ponderado: 12.86%
# [Gráfico de torta con los pesos]


# ============================================================
# Ejercicio 4: Sharpe Ratio
# Calcula el Sharpe Ratio de un activo dados sus
# rendimientos diarios simulados.
# Sharpe = (retorno_anual - tasa_libre_riesgo) / volatilidad_anual
# tasa_libre_riesgo = 4% anual
# ============================================================
print("\n=== Ejercicio 4: Sharpe Ratio ===")
rendimientos_diarios = [0.0012, -0.0005, 0.0021, -0.0008, 0.0015,
                         0.0003, -0.0012, 0.0028, -0.0004, 0.0009,
                         0.0018, -0.0015, 0.0007, 0.0025, -0.0003,
                         0.0014, -0.0010, 0.0006, 0.0020, -0.0008]
tasa_libre_riesgo = 0.04

# Escribe tu código aquí



# Output esperado:
# Días: 20
# Retorno promedio diario: 0.0005
# Volatilidad diaria: 0.0013
# Retorno anualizado: 13.10%
# Volatilidad anualizada: 20.61%
# Sharpe Ratio: 0.44
