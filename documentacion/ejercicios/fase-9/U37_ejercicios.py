# U37: EJERCICIOS — Machine Learning para Finanzas: Fundamentos

# ============================================================
# Ejercicio 1: Pipeline de features y Random Forest
# Crea 20+ features financieras para una serie de precios simulada:
#   - Retornos rezagados (1, 3, 5, 10, 20 días)
#   - Volatilidad rolling (5, 10, 20, 60 días)
#   - Momentum (5, 10, 20, 60, 120 días)
#   - Distancia a SMA (10, 20, 50, 200 días)
# Target: dirección del mercado a 5 días (0=baja, 1=sube)
# Split temporal 80/20. Entrena Random Forest con TimeSeriesSplit.
# Compara accuracy vs 3 benchmarks: siempre sube, momentum naive, mean reversion.
# ============================================================
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, roc_auc_score

np.random.seed(42)
n = 1500
retornos = np.random.normal(0.0003, 0.012, n)
precios = 100 * np.exp(np.cumsum(retornos))

print("=== Ejercicio 1: Pipeline de Features y Random Forest ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Pipeline de Features y Random Forest ===
# Dataset: XXXX filas, XX features
# TimeSeriesSplit CV (5 folds): accuracy = 0.XXXX (+/- 0.XXXX)
# Test accuracy:       0.XXXX
# AUC-ROC:             0.XXXX
# Benchmark siempre sube: 0.XXXX
# Benchmark momentum:     0.XXXX
# Benchmark reversion:    0.XXXX


# ============================================================
# Ejercicio 2: Regularización y overfitting
# Usa las mismas features del Ejercicio 1.
# Entrena Random Forest con 3 configuraciones:
#   - Modelo simple: max_depth=3, min_samples_leaf=50
#   - Modelo medio: max_depth=8, min_samples_leaf=10
#   - Modelo complejo: max_depth=30, min_samples_leaf=1
# Para cada modelo, reporta accuracy en train y test.
# ¿Cuál tiene el menor gap (train - test)?
# ¿Qué modelo generaliza mejor?
# ============================================================
print("\n=== Ejercicio 2: Regularización y Overfitting ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Regularización y Overfitting ===
# Modelo           | Train Acc | Test Acc | Gap (Train-Test)
# Simple (d=3)     | 0.5523    | 0.5401   | 0.0122
# Medio (d=8)      | 0.5876    | 0.5356   | 0.0520
# Complejo (d=30)  | 0.8345    | 0.5123   | 0.3222
# Mejor generalización: Simple (menor gap)


# ============================================================
# Ejercicio 3: Feature importance y selección
# Entrena modelo base con todas las features.
# Extrae y rankea feature importance.
# Re-entrena modelo solo con las top 5 features.
# Compara accuracy en test de ambas versiones.
# ¿Eliminar features irrelevantes mejora o empeora?
# ============================================================
print("\n=== Ejercicio 3: Feature Importance y Selección ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Feature Importance y Selección ===
# Top 5 features:
#   1. vol_10d        (importancia=0.1234)
#   2. ret_lag_1      (importancia=0.0987)
#   3. mom_20d        (importancia=0.0876)
#   4. dist_sma_50    (importancia=0.0765)
#   5. vol_20d        (importancia=0.0654)
# Accuracy todas las features: 0.5345
# Accuracy top 5 features:     0.5410
# Cambio: +0.0065


# ============================================================
# Ejercicio 4: Predicción multi-activo
# Simula datos de 3 activos correlacionados:
#   - Retornos del mercado: normal(0.0004, 0.012)
#   - Activo 1: 0.8 * mercado + 0.2 * ruido
#   - Activo 2: 0.4 * mercado + 0.6 * ruido
#   - Activo 3: 1.2 * mercado + 0.3 * ruido
# Crea features para cada activo (mismas que Ej 1).
# Entrena un modelo separado para cada uno.
# Compara feature importance entre los 3 modelos.
# ¿Las features importantes son consistentes entre activos?
# ============================================================
print("\n=== Ejercicio 4: Predicción Multi-Activo ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Predicción Multi-Activo ===
# Activo 1 — Top feature: vol_10d (0.1234), Accuracy: 0.5412
# Activo 2 — Top feature: ret_lag_1 (0.1156), Accuracy: 0.5278
# Activo 3 — Top feature: mom_20d (0.0987), Accuracy: 0.5334
# Consistencia: 2 de las top 3 features coinciden entre activos
