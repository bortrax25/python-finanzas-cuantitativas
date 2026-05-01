# U33: EJERCICIOS — Probabilidad, Estadística y Distribuciones Financieras

# ============================================================
# Ejercicio 1: Estadísticas y tests de normalidad
# Tienes los retornos diarios de 50 activos del S&P 500 (simulados).
# Para cada activo, calcula: media, volatilidad, skewness, kurtosis.
# Identifica cuáles activos rechazan la hipótesis de normalidad
# usando Jarque-Bera al 95% de confianza.
# Reporta: % de activos que NO son normales.
# ============================================================
import numpy as np
import scipy.stats as stats

np.random.seed(42)
# 252 días, 50 activos
retornos = np.random.standard_t(df=5, size=(252, 50)) * 0.005 + 0.0005

print("=== Ejercicio 1: Estadísticas y Tests de Normalidad ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Estadísticas y Tests de Normalidad ===
# Activo 0: media=0.000512, vol=0.007154, skew=0.1234, kurt=1.2345, Normal: False
# Activo 1: media=0.000487, vol=0.007231, skew=-0.2134, kurt=0.8932, Normal: True
# ...
# Total activos: 50
# Activos que rechazan normalidad (JB, 95%): XX / 50 (XX.X%)


# ============================================================
# Ejercicio 2: Ajuste t-Student y comparación de VaR
# Usa los retornos de uno de los activos del Ejercicio 1.
# Ajusta una distribución t-Student con stats.t.fit().
# Calcula VaR al 95% y 99% usando tres metodologías:
#   - VaR histórico (percentil empírico)
#   - VaR paramétrico normal (asumiendo normalidad)
#   - VaR paramétrico t-Student (usando el ajuste)
# Compara los resultados. El VaR histórico es la "verdad".
# ============================================================
print("\n=== Ejercicio 2: Ajuste t-Student y VaR ===")

retornos_activo = retornos[:, 0]  # Retornos del activo 0

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Ajuste t-Student y VaR ===
# Parámetros t-Student: df=4.89, loc=0.0005, scale=0.0061
# VaR 95% Histórico:   -1.0987%
# VaR 95% Normal:       -1.1345%
# VaR 95% t-Student:    -1.1523%
# VaR 99% Histórico:    -1.8734%
# VaR 99% Normal:        -1.6450%
# VaR 99% t-Student:     -1.9845%


# ============================================================
# Ejercicio 3: Simulación GBM y comparación con bootstrap
# Simula el precio del S&P 500 usando GBM:
#   precio_inicial = 4500, mu = 0.09, sigma = 0.18, dias = 252
# Genera 5000 trayectorias.
# Calcula:
#   (a) Distribución de precios finales (percentiles 5, 25, 50, 75, 95)
#   (b) Bootstrap histórico: remuestrea retornos del S&P 500 histórico
#       (simula retornos diarios con np.random.choice) y proyecta 252 días
#       con 5000 trayectorias. Calcula los mismos percentiles.
#   (c) Compara los percentiles. ¿Son similares?
# ============================================================
print("\n=== Ejercicio 3: Simulación GBM vs Bootstrap ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Simulación GBM vs Bootstrap ===
# GBM — Precios finales:
#   P5=3456.12, P25=4123.45, P50=4789.01, P75=5521.34, P95=6234.56
# Bootstrap — Precios finales:
#   P5=3412.78, P25=4089.12, P50=4756.89, P75=5498.23, P95=6198.45
# Diferencia en mediana: 0.67%


# ============================================================
# Ejercicio 4: Validación de supuestos para portafolio
# Tienes retornos simulados de 5 activos (252 días).
# Para cada activo:
#   (a) Test de normalidad Jarque-Bera y Shapiro-Wilk
#   (b) Q-Q plot conceptual (indica si hay desviaciones visibles)
#   (c) Si el activo no es normal, estima la matriz de covarianza por dos métodos:
#       - Método muestral clásico (np.cov)
#       - Bootstrap: remuestrea pares de retornos 1000 veces y promedia las covarianzas
# Compara las dos matrices. ¿Qué implicaciones tiene para la optimización de portafolio?
# ============================================================
print("\n=== Ejercicio 4: Validación de Supuestos para Portafolio ===")

np.random.seed(99)
retornos_5 = np.random.standard_t(df=6, size=(252, 5)) * 0.005 + 0.0004

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Validación de Supuestos para Portafolio ===
# Activo 0: JB p=0.0034, SW p=0.0156 → NO normal
# Activo 1: JB p=0.0021, SW p=0.0089 → NO normal
# Activo 2: JB p=0.0789, SW p=0.1234 → Normal
# Activo 3: JB p=0.0456, SW p=0.0345 → NO normal
# Activo 4: JB p=0.0012, SW p=0.0067 → NO normal
# Cov clásica vs bootstrap — diferencia media: 0.000012
# Las diferencias son pequeñas; el supuesto de normalidad afecta más
# a métricas de cola (VaR, CVaR) que a la covarianza.
