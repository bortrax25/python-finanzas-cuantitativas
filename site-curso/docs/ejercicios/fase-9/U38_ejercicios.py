# U38: EJERCICIOS — Machine Learning Avanzado: Métodos Cuantitativos

# ============================================================
# Ejercicio 1: XGBoost vs LightGBM vs Random Forest
# Usa el dataset del ejercicio U37 (mismas features, mismo split).
# Entrena y evalúa 3 modelos:
#   - Random Forest (n_estimators=200, max_depth=5)
#   - XGBoost (n_estimators=200, max_depth=5, learning_rate=0.01)
#   - LightGBM (n_estimators=200, max_depth=5, learning_rate=0.01)
# Para cada uno, reporta: accuracy, AUC-ROC y tiempo de entrenamiento.
# Usa el mismo TimeSeriesSplit para validación.
# ============================================================
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
import time

np.random.seed(42)
n = 1500
retornos = np.random.normal(0.0003, 0.012, n)
precios = 100 * np.exp(np.cumsum(retornos))

print("=== Ejercicio 1: XGBoost vs LightGBM vs Random Forest ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: XGBoost vs LightGBM vs Random Forest ===
# Modelo         | Accuracy | AUC-ROC | Tiempo (s)
# Random Forest  | 0.5345   | 0.5512  | 0.45
# XGBoost        | 0.5412   | 0.5587  | 1.23
# LightGBM       | 0.5389   | 0.5534  | 0.67
# Mejor modelo: XGBoost (mayor AUC-ROC)


# ============================================================
# Ejercicio 2: Clustering de regímenes de mercado
# Genera datos de mercado simulados con 3 regímenes:
#   - Bull: retorno positivo (+0.1% diario), baja vol (1.0%)
#   - Bear: retorno negativo (-0.08% diario), alta vol (2.5%)
#   - Sideways: retorno ~0, vol media (1.5%)
# Features para clustering: retorno_30d, volatilidad_30d, drawdown_60d.
# Usa K-Means con k=3. Encuentra k óptimo con elbow method (probar k=2..6).
# Reporta silhouette score para k=3.
# Etiqueta cada cluster como Bull/Bear/Sideways basado en el retorno medio.
# ============================================================
print("\n=== Ejercicio 2: Clustering de Regímenes ===")

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Clustering de Regímenes ===
# Elbow method: k óptimo = 3 (codo más pronunciado)
# K-Means (k=3), Silhouette Score: 0.4234
# Cluster 0 (Sideways):  920 días, ret_30d=0.023%, vol=1.23%
# Cluster 1 (Bull):       345 días, ret_30d=1.234%, vol=0.87%
# Cluster 2 (Bear):       175 días, ret_30d=-0.876%, vol=2.34%


# ============================================================
# Ejercicio 3: PCA para factores y predicción
# Genera retornos de 20 activos con estructura de factores:
#   - Factor mercado: afecta a todos los activos (carga ~0.8-1.2)
#   - Factor sector: afecta a los primeros 10, no a los últimos 10
#   - Ruido idiosincrático
# Aplica PCA y reporta varianza explicada por los primeros 3 componentes.
# Usa los primeros K componentes como features para predecir
# el retorno futuro del activo 1 (target: ret_lag_1).
# Compara accuracy de predicción usando:
#   (a) Los 20 activos como features
#   (b) Los primeros 3 componentes de PCA
# ============================================================
from sklearn.decomposition import PCA

print("\n=== Ejercicio 3: PCA para Factores y Predicción ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: PCA para Factores y Predicción ===
# Varianza explicada:
#   PC1: 0.4523 (mercado)
#   PC2: 0.2123 (sector)
#   PC3: 0.0834
#   Acumulada 3 PCs: 0.7480
# Accuracy con 20 activos: 0.5389
# Accuracy con 3 PCs:      0.5412
# Conclusión: PCA no solo reduce dimensionalidad sino que
#             puede mejorar predicción al eliminar ruido


# ============================================================
# Ejercicio 4: Autoencoder para reducción de dimensionalidad
# Usa el mismo dataset de 20 activos del ejercicio 3.
# Implementa un autoencoder simple con NumPy (sin PyTorch):
#   - Encoder: Linear(20→8) + ReLU + Linear(8→3)  [3 factores latentes]
#   - Decoder: Linear(3→8) + ReLU + Linear(8→20)
# Entrena minimizando MSE de reconstrucción (usa descenso por gradiente simple).
# Extrae los 3 factores latentes del encoder.
# Compara el MSE de reconstrucción del autoencoder vs PCA (con 3 componentes).
# ¿Cuál reconstruye mejor los datos originales?
# ============================================================
print("\n=== Ejercicio 4: Autoencoder con NumPy ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Autoencoder con NumPy ===
# Autoencoder: MSE reconstrucción = 0.0023
# PCA:         MSE reconstrucción = 0.0034
# Autoencoder reconstruye mejor (MSE menor).
# Los factores latentes del autoencoder son combinaciones NO lineales
# de los retornos, lo que permite capturar patrones que PCA (lineal) pierde.
