# 📝 Ejercicios: U35 — Fase 8

> [← Volver a ejercicios Fase 8](index.md) | [📥 Descargar .py](U35_ejercicios)

---

```python
# U35: EJERCICIOS — Econometría Financiera: Regresión y Panel Data

# ============================================================
# Ejercicio 1: Diagnóstico de regresión CAPM
# Simula retornos de una acción contra el mercado:
#   r_accion = alfa + beta * r_mercado + ruido
# con alfa=0.0002, beta=1.2, y ruido con heterocedasticidad
# (la varianza del ruido crece cuando el mercado baja).
# Estima el CAPM con OLS y reporta:
#   (a) Coeficientes con errores OLS estándar
#   (b) Test de Breusch-Pagan para heterocedasticidad
#   (c) Test de Durbin-Watson para autocorrelación
#   (d) Coeficientes con errores White (HC3)
#   (e) Coeficientes con errores Newey-West (5 lags)
# Compara los p-values. ¿Cambia la significancia del alfa?
# ============================================================
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

np.random.seed(42)
n = 500
retorno_mercado = np.random.normal(0.0005, 0.012, n)
alfa_verdadero = 0.0002
beta_verdadero = 1.2

# Ruido heterocedástico: mayor varianza cuando mercado negativo
ruido = np.where(
    retorno_mercado < 0,
    np.random.normal(0, 0.012, n),
    np.random.normal(0, 0.006, n)
)
retorno_accion = alfa_verdadero + beta_verdadero * retorno_mercado + ruido

print("=== Ejercicio 1: Diagnóstico de regresión CAPM ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Diagnóstico de regresión CAPM ===
# OLS: alfa=0.0003 (p=0.456), beta=1.198 (p=0.000)
# Breusch-Pagan: p=0.0001 → Heterocedasticidad DETECTADA
# Durbin-Watson: 2.03 → Sin autocorrelación apreciable
# White (HC3):  alfa=0.0003 (p=0.487), beta=1.198 (p=0.000)
# Newey-West:   alfa=0.0003 (p=0.491), beta=1.198 (p=0.000)
# Conclusión: Significancia del alfa es similar; los SE son ligeramente mayores


# ============================================================
# Ejercicio 2: Errores clustered vs robustos
# Crea un panel artificial con 80 empresas y 60 meses.
# Los retornos de empresas del mismo sector están correlacionados.
# Estima el modelo: r_it = alfa + beta * mercado_t + ruido_it
# Reporta el coeficiente beta con:
#   (a) Errores OLS simples
#   (b) Errores White (HC3)
#   (c) Errores Newey-West (5 lags)
#   (d) Errores clustered por empresa
#   (e) Errores clustered por sector
# Compara los errores estándar. ¿Cuál es el más conservador?
# ============================================================
print("\\n=== Ejercicio 2: Errores Clustered vs Robustos ===")

np.random.seed(42)
n_empresas = 80
n_meses = 60
n_total = n_empresas * n_meses

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Errores Clustered vs Robustos ===
# Error estándar de beta:
# OLS simple:          0.0345
# White (HC3):         0.0387
# Newey-West (5):      0.0392
# Clustered empresa:   0.0521
# Clustered sector:    0.0615
# El clustering por sector es el más conservador


# ============================================================
# Ejercicio 3: Fixed Effects vs Pooled OLS
# Simula datos de panel con efectos fijos por empresa:
#   r_it = alfa_i + beta * x_it + ruido_it
# donde cada empresa tiene su propio intercepto alfa_i.
# Estima dos modelos:
#   (a) Pooled OLS (ignorando efectos fijos)
#   (b) PanelOLS con entity_effects=True (Fixed Effects)
# Compara:
#   - Coeficiente beta estimado
#   - R² within, R² between, R² overall
#   - ¿Por qué el R² within es más bajo?
# ============================================================
from linearmodels.panel import PanelOLS
import pandas as pd

print("\\n=== Ejercicio 3: Fixed Effects vs Pooled OLS ===")

np.random.seed(42)
n_empresas = 30
n_periodos = 40
n_total = n_empresas * n_periodos

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Fixed Effects vs Pooled OLS ===
# Pooled OLS beta:  0.8234
# Fixed Effects beta: 0.9876 (valor verdadero: 1.0)
# R² (Pooled): 0.4523
# R² Within (FE): 0.3124
# R² Between (FE): 0.8912
# El R² within es más bajo porque FE explota solo la variación temporal
# dentro de cada empresa, ignorando diferencias entre empresas


# ============================================================
# Ejercicio 4: Fama-MacBeth
# Simula 30 activos con betas verdaderas invariantes.
# Asume 120 meses: los primeros 36 para estimar betas (rolling),
# los últimos 84 para regresiones cross-sectional (FM paso 2).
# Simplificación: usa las betas verdaderas con ruido aleatorio.
# Paso 1: Para cada activo, estima beta como beta_verdadera + ruido
# Paso 2: Cada mes, regresa los retornos cross-section contra betas
#         y promedia los gammas.
# Reporta:
#   - Prima de riesgo estimada (gamma)
#   - Error estándar Fama-MacBeth
#   - t-statistic
#   - ¿Es la prima estadísticamente significativa?
# ============================================================
print("\\n=== Ejercicio 4: Fama-MacBeth ===")

np.random.seed(42)
T, N, ventana = 120, 30, 36

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Fama-MacBeth ===
# Prima verdadera: 0.0060
# Prima estimada (gamma): 0.0058
# Error estándar FM:      0.0020
# t-statistic:            2.90
# Significativa: SÍ (|t| > 1.96)
```

---

> [📥 Descargar archivo .py](U35_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 8](index.md)
