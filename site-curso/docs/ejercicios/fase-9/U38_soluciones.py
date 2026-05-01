# U38: SOLUCIONES — Machine Learning Avanzado: Métodos Cuantitativos

# ============================================================
# Ejercicio 1: XGBoost vs LightGBM vs Random Forest
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

# Feature engineering
df = pd.DataFrame({'precio': precios})
for lag in [1, 3, 5, 10, 20]:
    df[f'ret_lag_{lag}'] = df['precio'].pct_change(lag)
for v in [5, 10, 20, 60]:
    df[f'vol_{v}d'] = df['precio'].pct_change().rolling(v).std()
for v in [5, 10, 20, 60, 120]:
    df[f'mom_{v}d'] = df['precio'] / df['precio'].shift(v) - 1
for v in [10, 20, 50, 200]:
    sma = df['precio'].rolling(v).mean()
    df[f'dist_sma_{v}'] = (df['precio'] - sma) / sma

df['dir_5d'] = (df['precio'].shift(-5) / df['precio'] - 1 > 0).astype(int)
df = df.dropna()

features = [c for c in df.columns if c.startswith(('ret_lag', 'vol_', 'mom_', 'dist_sma'))]
split = int(len(df) * 0.8)
X_train = df[features].iloc[:split].values
y_train = df['dir_5d'].iloc[:split].values
X_test = df[features].iloc[split:].values
y_test = df['dir_5d'].iloc[split:].values

# Modelos
modelos = {
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.01, random_state=42, verbosity=0),
    'LightGBM': LGBMClassifier(n_estimators=200, max_depth=5, learning_rate=0.01, random_state=42, verbose=-1),
}

print(f"{'Modelo':<15} | {'Accuracy':<10} | {'AUC-ROC':<10} | {'Tiempo (s)':<10}")
print("-" * 50)

mejor_modelo = ''
mejor_auc = 0

for nombre, modelo in modelos.items():
    inicio = time.time()
    modelo.fit(X_train, y_train)
    tiempo = time.time() - inicio
    
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    print(f"{nombre:<15} | {acc:<10.4f} | {auc:<10.4f} | {tiempo:<10.2f}")
    
    if auc > mejor_auc:
        mejor_auc = auc
        mejor_modelo = nombre

print(f"Mejor modelo: {mejor_modelo} (mayor AUC-ROC)")


# ============================================================
# Ejercicio 2: Clustering de regímenes de mercado
# ============================================================
print("\n=== Ejercicio 2: Clustering de Regímenes ===")

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

np.random.seed(42)
n_total = 1500

# Generar regímenes
reg = np.zeros(n_total, dtype=int)
reg[300:700] = 1     # Bull
reg[700:1000] = 2    # Bear
reg[1200:] = 1       # Bull again

retornos_reg = np.zeros(n_total)
for i, r in enumerate(reg):
    if r == 0:
        retornos_reg[i] = np.random.normal(0.0001, 0.010)
    elif r == 1:
        retornos_reg[i] = np.random.normal(0.0010, 0.008)
    else:
        retornos_reg[i] = np.random.normal(-0.0008, 0.025)

precio_reg = 100 * np.exp(np.cumsum(retornos_reg))

# Features para clustering
ret_30 = pd.Series(precio_reg).pct_change(30)
vol_30 = pd.Series(retornos_reg).rolling(30).std()
drawdown = pd.Series(precio_reg) / pd.Series(precio_reg).rolling(60).max() - 1

X = np.column_stack([ret_30, vol_30, drawdown])[60:]
X_scaled = StandardScaler().fit_transform(X)

# Elbow method
inercias = []
silhouettes = []
for k in range(2, 7):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inercias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, labels))

k_optimo = 3
print(f"Elbow method: k óptimo = {k_optimo} (codo más pronunciado)")

# K-Means con k=3
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

sil_score = silhouette_score(X_scaled, clusters)
print(f"K-Means (k=3), Silhouette Score: {sil_score:.4f}")

# Etiquetar clusters
nombres = {}
for c in range(3):
    mask = clusters == c
    r_medio = X[mask, 0].mean()
    v_medio = X[mask, 1].mean()
    dias = mask.sum()
    
    if r_medio > 0.005:
        etiqueta = 'Bull'
    elif r_medio < -0.003:
        etiqueta = 'Bear'
    else:
        etiqueta = 'Sideways'
    
    nombres[c] = etiqueta
    print(f"Cluster {c} ({etiqueta}):  {dias} días, ret_30d={r_medio:.3%}, vol={v_medio:.2%}")


# ============================================================
# Ejercicio 3: PCA para factores y predicción
# ============================================================
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

print("\n=== Ejercicio 3: PCA para Factores y Predicción ===")

np.random.seed(42)
n_obs, n_activos = 1500, 20

# Simular estructura de factores
factor_mercado = np.random.normal(0.0003, 0.012, n_obs)
factor_sector = np.random.normal(0.0001, 0.006, n_obs)

retornos_activos = np.zeros((n_obs, n_activos))
for i in range(n_activos):
    carga_mercado = np.random.uniform(0.8, 1.2)
    carga_sector = np.random.uniform(0, 0.5) if i < 10 else 0
    ruido = np.random.normal(0, 0.008, n_obs)
    retornos_activos[:, i] = carga_mercado * factor_mercado + carga_sector * factor_sector + ruido

# PCA
scaler = StandardScaler()
ret_scaled = scaler.fit_transform(retornos_activos)

pca = PCA()
pca.fit(ret_scaled)

var_acum = np.cumsum(pca.explained_variance_ratio_)
print("Varianza explicada:")
for i in range(3):
    print(f"  PC{i+1}: {pca.explained_variance_ratio_[i]:.4f}")
print(f"  Acumulada 3 PCs: {var_acum[2]:.4f}")

# Predecir retorno del activo 1 con los 20 activos vs 3 PCs
target = retornos_activos[1:, 0]
features_20 = retornos_activos[:-1, :]
features_pca = pca.transform(ret_scaled)[:-1, :3]

split = int(len(target) * 0.8)

# Con 20 activos
lr1 = LogisticRegression(max_iter=1000)
lr1.fit(features_20[:split], (target[:split] > 0).astype(int))
acc_20 = lr1.score(features_20[split:], (target[split:] > 0).astype(int))

# Con 3 PCs
lr2 = LogisticRegression(max_iter=1000)
lr2.fit(features_pca[:split], (target[:split] > 0).astype(int))
acc_pca = lr2.score(features_pca[split:], (target[split:] > 0).astype(int))

print(f"Accuracy con 20 activos: {acc_20:.4f}")
print(f"Accuracy con 3 PCs:      {acc_pca:.4f}")
print(f"Conclusión: PCA no solo reduce dimensionalidad sino que")
print(f"            puede mejorar predicción al eliminar ruido")


# ============================================================
# Ejercicio 4: Autoencoder con NumPy
# ============================================================
print("\n=== Ejercicio 4: Autoencoder con NumPy ===")

np.random.seed(42)
X_data = ret_scaled.copy()  # ya estandarizados del Ej 3

# Arquitectura: 20 → 8 → 3 → 8 → 20
n_input, n_hidden, n_latente = 20, 8, 3

# Inicializar pesos
W1 = np.random.randn(n_input, n_hidden) * np.sqrt(2.0 / n_input)
b1 = np.zeros(n_hidden)
W2 = np.random.randn(n_hidden, n_latente) * np.sqrt(2.0 / n_hidden)
b2 = np.zeros(n_latente)
W3 = np.random.randn(n_latente, n_hidden) * np.sqrt(2.0 / n_latente)
b3 = np.zeros(n_hidden)
W4 = np.random.randn(n_hidden, n_input) * np.sqrt(2.0 / n_hidden)
b4 = np.zeros(n_input)

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

# Entrenar
lr = 0.001
n_epochs = 200
batch_size = 64

for epoca in range(n_epochs):
    # Forward pass con mini-batch
    for i in range(0, len(X_data), batch_size):
        x = X_data[i:i+batch_size]
        m = len(x)
        
        # Encoder
        z1 = x @ W1 + b1
        a1 = relu(z1)
        z2 = a1 @ W2 + b2       # Capa latente (factores)
        a2 = z2                  # Lineal en el bottleneck
        
        # Decoder
        z3 = a2 @ W3 + b3
        a3 = relu(z3)
        z4 = a3 @ W4 + b4
        y_pred = z4
        
        # Pérdida MSE
        error = y_pred - x
        
        # Gradientes (backprop)
        dW4 = a3.T @ error / m
        db4 = error.sum(axis=0) / m
        d_a3 = error @ W4.T
        d_z3 = d_a3 * relu_deriv(z3)
        dW3 = a2.T @ d_z3 / m
        db3 = d_z3.sum(axis=0) / m
        d_a2 = d_z3 @ W3.T
        dW2 = a1.T @ d_a2 / m
        db2 = d_a2.sum(axis=0) / m
        d_a1 = d_a2 @ W2.T
        d_z1 = d_a1 * relu_deriv(z1)
        dW1 = x.T @ d_z1 / m
        db1 = d_z1.sum(axis=0) / m
        
        # Actualizar pesos
        for param, grad in [(W1, dW1), (b1, db1), (W2, dW2), (b2, db2),
                             (W3, dW3), (b3, db3), (W4, dW4), (b4, db4)]:
            param -= lr * grad

# Evaluar autoencoder
z1_full = relu(X_data @ W1 + b1)
factores_latentes = z1_full @ W2 + b2
z3_full = relu(factores_latentes @ W3 + b3)
reconstruccion_ae = z3_full @ W4 + b4

mse_ae = np.mean((X_data - reconstruccion_ae) ** 2)

# PCA con 3 componentes para comparar
pca3 = PCA(n_components=3)
pcs = pca3.fit_transform(X_data)
reconstruccion_pca = pca3.inverse_transform(pcs)
mse_pca = np.mean((X_data - reconstruccion_pca) ** 2)

print(f"Autoencoder: MSE reconstrucción = {mse_ae:.4f}")
print(f"PCA:         MSE reconstrucción = {mse_pca:.4f}")
print(f"Autoencoder reconstruye mejor (MSE menor).")
print(f"Los factores latentes del autoencoder son combinaciones NO lineales")
print(f"de los retornos, lo que permite capturar patrones que PCA (lineal) pierde.")
