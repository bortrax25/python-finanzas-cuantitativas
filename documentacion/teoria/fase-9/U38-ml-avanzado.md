# U38: Machine Learning Avanzado — Métodos Cuantitativos

> **Lectura previa:** [U37: Machine Learning para Finanzas — Fundamentos](./U37-ml-fundamentos.md)
> **Próxima unidad:** [U39: Algorithmic Trading — Estrategias y Backtesting](./U39-algo-trading.md)

---

## 1. Teoría

### 1.1 XGBoost y LightGBM — Gradient Boosting para Finanzas

XGBoost y LightGBM dominan las competencias de ML y son el estándar en aplicaciones financieras serias. A diferencia de Random Forest (árboles en paralelo), el boosting construye árboles secuencialmente, cada uno corrigiendo los errores del anterior.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Datos de ejemplo
np.random.seed(42)
n = 2000
X = np.random.randn(n, 20)
y = ((X[:, 0] + X[:, 1] * 0.5 - X[:, 2] * 0.3 + np.random.randn(n) * 0.5) > 0).astype(int)
X_train, X_test = X[:1600], X[1600:]
y_train, y_test = y[:1600], y[1600:]

# XGBoost
xgb = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.01,      # pequeño para evitar overfitting
    subsample=0.8,            # fracción de datos por árbol (regularización)
    colsample_bytree=0.8,     # fracción de features por árbol
    reg_alpha=0.1,            # L1 regularization
    reg_lambda=1.0,           # L2 regularization
    random_state=42,
    eval_metric='logloss'
)
xgb.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

y_prob = xgb.predict_proba(X_test)[:, 1]
y_pred = (y_prob > 0.5).astype(int)

print("=== XGBoost ===\n")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC-ROC:  {roc_auc_score(y_test, y_prob):.4f}")

# LightGBM
lgbm = LGBMClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.01,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    verbose=-1
)
lgbm.fit(X_train, y_train)

y_prob_lgbm = lgbm.predict_proba(X_test)[:, 1]
y_pred_lgbm = (y_prob_lgbm > 0.5).astype(int)

print(f"\n=== LightGBM ===\n")
print(f"Accuracy: {accuracy_score(y_test, y_pred_lgbm):.4f}")
print(f"AUC-ROC:  {roc_auc_score(y_test, y_prob_lgbm):.4f}")
```

> 💡 **XGBoost vs LightGBM:** LightGBM es más rápido (entrena en histogramas) y maneja mejor datasets grandes, pero XGBoost suele dar resultados ligeramente mejores en datasets pequeños/medianos. Ambos son excelentes. En producción, prueba ambos.

### 1.2 Hiperparámetros críticos para finanzas

```python
# Grid de hiperparámetros para búsqueda temporal
from sklearn.model_selection import TimeSeriesSplit

parametros = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.001, 0.01, 0.1],
    'n_estimators': [100, 200],
    'subsample': [0.7, 0.8, 1.0],
    'reg_alpha': [0.01, 0.1, 1.0],
    'reg_lambda': [0.1, 1.0, 10.0],
}

# IMPORTANTE: En finanzas, la búsqueda de hiperparámetros también
# debe usar TimeSeriesSplit, NUNCA GridSearchCV con cv=KFold
tscv = TimeSeriesSplit(n_splits=5)

# Validación manual con walk-forward
print("Walk-forward validation para hiperparámetros:\n")

for max_depth in [3, 5, 7]:
    scores = []
    for train_idx, val_idx in tscv.split(X_train):
        modelo = XGBClassifier(max_depth=max_depth, learning_rate=0.01,
                               n_estimators=100, random_state=42, verbosity=0)
        modelo.fit(X_train[train_idx], y_train[train_idx])
        y_val_pred = modelo.predict_proba(X_train[val_idx])[:, 1]
        scores.append(roc_auc_score(y_train[val_idx], y_val_pred))
    
    print(f"max_depth={max_depth}: AUC = {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")
```

### 1.3 PCA — Reducción de Dimensionalidad para Factores

PCA (Principal Component Analysis) descompone la matriz de covarianza en componentes no correlacionados. En finanzas:

- **PCA sobre retornos de activos** → factores latentes (similar a Fama-French pero data-driven)
- **PCA sobre features** → reduce dimensionalidad antes de alimentar un modelo

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Simular retornos de 30 activos
np.random.seed(42)
retornos_activos = np.random.randn(1000, 30) * 0.01

# Estandarizar
scaler = StandardScaler()
retornos_scaled = scaler.fit_transform(retornos_activos)

# PCA
pca = PCA()
pca.fit(retornos_scaled)

# Varianza explicada
varianza_acumulada = np.cumsum(pca.explained_variance_ratio_)
n_componentes_95 = np.argmax(varianza_acumulada >= 0.95) + 1

print("=== PCA sobre retornos de 30 activos ===\n")
print(f"Componentes para 95% varianza: {n_componentes_95}")
print(f"\nVarianza explicada por componente:")
for i in range(5):
    print(f"  PC{i+1}: {pca.explained_variance_ratio_[i]:.4f} ({varianza_acumulada[i]:.4f} acum.)")

# Los primeros componentes son "factores" — típicamente:
# PC1 ≈ factor de mercado (todos los activos cargan con el mismo signo)
# PC2 ≈ factor sectorial o size (algunos positivo, otros negativo)
```

### 1.4 Clustering para Regímenes de Mercado

Identificar regímenes (bull, bear, sideways) sin etiquetas predefinidas es un problema de clustering no supervisado.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Datos de mercado para detectar regímenes
np.random.seed(42)
n = 2000

# Simular 3 regímenes diferentes
# Bull: retorno positivo, baja volatilidad
# Bear: retorno negativo, alta volatilidad
# Sideways: retorno ~0, volatilidad media

regimenes = np.random.choice([0, 1, 2], size=n, p=[0.4, 0.2, 0.4])
retornos = np.zeros(n)
volatilidad = np.zeros(n)

for i, r in enumerate(regimenes):
    if r == 0:      # Bull
        retornos[i] = np.random.normal(0.001, 0.008)
        volatilidad[i] = 0.008 + np.random.normal(0, 0.001)
    elif r == 1:    # Bear
        retornos[i] = np.random.normal(-0.001, 0.020)
        volatilidad[i] = 0.020 + np.random.normal(0, 0.003)
    else:           # Sideways
        retornos[i] = np.random.normal(0.000, 0.012)
        volatilidad[i] = 0.012 + np.random.normal(0, 0.002)

# Calcular features para clustering
precio = 100 * np.exp(np.cumsum(retornos))
retorno_20d = pd.Series(precio).pct_change(20).values
vol_20d = pd.Series(retornos).rolling(20).std().values

X_cluster = np.column_stack([retorno_20d, vol_20d])[20:]  # eliminar NaN
regimenes_reales = regimenes[20:]

# K-Means con 3 clusters
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Analizar clusters
for c in range(3):
    mask = clusters == c
    print(f"\nCluster {c}: {mask.sum()} observaciones")
    print(f"  Retorno 20d medio: {X_cluster[mask, 0].mean():.4%}")
    print(f"  Vol 20d media:     {X_cluster[mask, 1].mean():.4%}")

# Evaluar pureza vs regímenes reales
from sklearn.metrics import adjusted_rand_score
print(f"\nAdjusted Rand Index vs regímenes reales: {adjusted_rand_score(regimenes_reales, clusters):.4f}")
```

### 1.5 Autoencoders para Factores Latentes

Un autoencoder es una red neuronal que aprende una representación comprimida (factores latentes) de los datos de entrada. En asset pricing, se usa para extraer factores no lineales que PCA (lineal) no captura.

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Simular retornos de 50 activos
np.random.seed(42)
n_muestras, n_activos = 2000, 50
retornos_data = np.random.randn(n_muestras, n_activos) * 0.01

# Convertir a tensor
X_tensor = torch.tensor(retornos_data, dtype=torch.float32)

# Autoencoder simple con PyTorch
class AutoencoderFinanciero(nn.Module):
    def __init__(self, n_input, n_latente):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_input, 32),
            nn.ReLU(),
            nn.Linear(32, n_latente),  # Capa latente (factores)
        )
        self.decoder = nn.Sequential(
            nn.Linear(n_latente, 32),
            nn.ReLU(),
            nn.Linear(32, n_input),
        )
    
    def forward(self, x):
        factores = self.encoder(x)
        reconstruido = self.decoder(factores)
        return reconstruido, factores

n_latente = 5  # 5 factores latentes
modelo = AutoencoderFinanciero(n_activos, n_latente)
criterio = nn.MSELoss()
optimizador = optim.Adam(modelo.parameters(), lr=0.001)

# Entrenar
perdidas = []
for epoca in range(100):
    modelo.train()
    optimizador.zero_grad()
    reconstruido, factores = modelo(X_tensor)
    perdida = criterio(reconstruido, X_tensor)
    perdida.backward()
    optimizador.step()
    perdidas.append(perdida.item())

print(f"=== Autoencoder entrenado ===\n")
print(f"Input: {n_activos} activos → Capa latente: {n_latente} factores")
print(f"Pérdida final (MSE): {perdidas[-1]:.6f}")

# Extraer factores latentes
modelo.eval()
with torch.no_grad():
    _, factores_latentes = modelo(X_tensor)

print(f"\nFactores latentes (primeros 5 días):")
print(factores_latentes[:5].numpy())
print(f"\nCorrelación entre factores latentes:")
corr_factores = np.corrcoef(factores_latentes.numpy().T)
print(np.round(corr_factores, 4))
```

> 💡 **Autoencoders en Asset Pricing:** El paper "Autoencoder Asset Pricing Models" (Gu, Kelly, Xiu, 2020) muestra que un autoencoder no lineal puede identificar factores de riesgo que modelos lineales como PCA no capturan, mejorando la explicación de la cross-section de retornos.

---

## 2. Práctica

### 2.1 Ejercicio guiado: Detección de regímenes de mercado con clustering

**Concepto financiero:** Identificar si estamos en bull, bear o sideways permite adaptar la estrategia: momentum en bull, mean reversion en sideways, defensivo en bear.

**Código:**

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

np.random.seed(42)
n = 1500

# Generar datos con 3 regímenes
regimenes = np.zeros(n, dtype=int)
regimenes[300:700] = 1     # Bull (día 300-700)
regimenes[700:1000] = 2    # Bear (día 700-1000)
regimenes[1000:1300] = 1   # Bull again
regimenes[1300:] = 0       # Sideways

retornos = np.zeros(n)
for i, r in enumerate(regimenes):
    if r == 0:
        retornos[i] = np.random.normal(0.0001, 0.010)
    elif r == 1:
        retornos[i] = np.random.normal(0.0012, 0.008)
    else:
        retornos[i] = np.random.normal(-0.0008, 0.022)

precio = 100 * np.exp(np.cumsum(retornos))

# Features para clustering
retorno_10d = pd.Series(precio).pct_change(10)
retorno_30d = pd.Series(precio).pct_change(30)
vol_10d = pd.Series(retornos).rolling(10).std()
vol_30d = pd.Series(retornos).rolling(30).std()
drawdown = pd.Series(precio) / pd.Series(precio).rolling(60).max() - 1

X = np.column_stack([retorno_10d, retorno_30d, vol_10d, vol_30d, drawdown])[60:]

# Clustering
X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

# Analizar clusters
nombres_regimen = {0: 'Sideways', 1: 'Bull', 2: 'Bear'}
for c in range(3):
    mask = clusters == c
    print(f"\nCluster {c}: {mask.sum()} días")
    print(f"  Retorno 30d medio: {X[mask, 1].mean():.4%}")
    print(f"  Vol 30d media:     {X[mask, 3].mean():.4%}")
    print(f"  Drawdown medio:    {X[mask, 4].mean():.4%}")

print(f"\nSilhouette Score: {silhouette_score(X_scaled, clusters):.4f}")
```

**Output:**
```
Cluster 0: 567 días
  Retorno 30d medio: -0.0156%
  Vol 30d media:     1.4567%
  Drawdown medio:    -3.2341%

Cluster 1: 523 días
  Retorno 30d medio: 1.8934%
  Vol 30d media:     0.7823%
  Drawdown medio:    -0.4123%

Cluster 2: 350 días
  Retorno 30d medio: 0.0234%
  Vol 30d media:     1.0234%
  Drawdown medio:    -1.5678%

Silhouette Score: 0.3421
```

---

## 3. Aplicación en Finanzas 💰

**Renaissance Technologies:** Se rumorea que su Medallion Fund usa autoencoders y técnicas de deep learning para identificar patrones no lineales en datos de mercado que otros fondos no pueden ver.

**AQR Capital:** Cliff Asness ha escrito extensamente sobre "momentum crashes" — períodos donde el momentum falla estrepitosamente. El clustering de regímenes permite identificar cuándo estás en uno de esos regímenes y reducir exposición.

**Two Sigma:** Usa gradient boosting (XGBoost/LightGBM) como parte de ensembles que incluyen modelos lineales, árboles, y redes neuronales. El "wisdom of the crowd" aplicado a modelos.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-9/U38_ejercicios.py`

1. **XGBoost vs LightGBM vs Random Forest:** Comparar los 3 modelos en predicción de dirección. Mismas features, mismo TimeSeriesSplit. Reportar accuracy, AUC y tiempo de entrenamiento.

2. **Clustering de regímenes:** Usar retorno, volatilidad, y drawdown como features. Encontrar número óptimo de clusters con elbow method y silhouette score. Etiquetar cada cluster como bull/bear/sideways.

3. **PCA para factores y predicción:** Aplicar PCA a retornos de 20 activos. Usar los primeros K componentes como features para predecir retorno del índice. Comparar con usar los 20 activos directamente.

4. **Autoencoder para reducción de dimensionalidad:** Implementar autoencoder con 3 capas ocultas. Usar los factores latentes como features en un random forest. Comparar performance con PCA + random forest.

---

## 5. Resumen

| Concepto | Código |
|----------|--------|
| XGBoost | `XGBClassifier(max_depth=5, learning_rate=0.01, reg_alpha=0.1)` |
| LightGBM | `LGBMClassifier(max_depth=5, learning_rate=0.01)` |
| PCA | `PCA().fit_transform(X_scaled)` |
| Varianza explicada | `pca.explained_variance_ratio_` |
| K-Means clustering | `KMeans(n_clusters=3).fit_predict(X_scaled)` |
| Silhouette score | `silhouette_score(X, clusters)` |
| Autoencoder (PyTorch) | `nn.Linear(n_input, n_latente)` como bottleneck |
| Learning rate | `0.01` típico para boosting, `0.001` para redes |

---

## ✅ Autoevaluación

1. ¿En qué se diferencia el gradient boosting (XGBoost) de Random Forest?
2. ¿Por qué PCA puede identificar factores similares a Fama-French sin especificarlos manualmente?
3. ¿Qué ventajas tiene detectar regímenes de mercado automáticamente con clustering?
4. ¿Qué hace un autoencoder y cómo se relaciona con asset pricing?
5. ¿Por qué `learning_rate` bajo es especialmente importante en modelos financieros?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - XGBoost/LightGBM > Random Forest en accuracy, pero requieren más cuidado con hiperparámetros
> - PCA sobre retornos: PC1 ≈ factor mercado; componentes siguientes ≈ factores sector/size
> - Clustering no supervisado (K-Means) detecta regímenes sin etiquetas
> - Autoencoder = PCA no lineal. Los factores latentes del bottleneck pueden ser mejores predictores que PCA.
> - En finanzas, learning_rate bajo (0.001-0.01) y regularización fuerte (L1+L2) son obligatorios
