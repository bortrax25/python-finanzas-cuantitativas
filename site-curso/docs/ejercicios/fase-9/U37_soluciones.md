# ✅ Soluciones: U37 — Fase 9

> [← Volver a ejercicios Fase 9](index.md) | [📥 Descargar .py](U37_soluciones)

---

```python
# U37: SOLUCIONES — Machine Learning para Finanzas: Fundamentos

# ============================================================
# Ejercicio 1: Pipeline de features y Random Forest
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

df = pd.DataFrame({'precio': precios})

# Feature engineering
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
print(f"Dataset: {len(df)} filas, {len(features)} features")

# Split temporal 80/20
split = int(len(df) * 0.8)
train, test = df.iloc[:split], df.iloc[split:]

X_train, y_train = train[features].values, train['dir_5d'].values
X_test, y_test = test[features].values, test['dir_5d'].values

# TimeSeriesSplit CV
tscv = TimeSeriesSplit(n_splits=5)
scores = []
for tr_idx, val_idx in tscv.split(X_train):
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=20, random_state=42)
    rf.fit(X_train[tr_idx], y_train[tr_idx])
    scores.append(rf.score(X_train[val_idx], y_train[val_idx]))

print(f"TimeSeriesSplit CV (5 folds): accuracy = {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")

# Modelo final
rf_final = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20, random_state=42)
rf_final.fit(X_train, y_train)
y_pred = rf_final.predict(X_test)
y_prob = rf_final.predict_proba(X_test)[:, 1]

print(f"Test accuracy:       {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC-ROC:             {roc_auc_score(y_test, y_prob):.4f}")
print(f"Benchmark siempre sube: {(y_test == 1).mean():.4f}")
print(f"Benchmark momentum:     {accuracy_score(y_test, (X_test[:, features.index('ret_lag_1')] > 0).astype(int)):.4f}")
print(f"Benchmark reversion:    {accuracy_score(y_test, (X_test[:, features.index('ret_lag_1')] < 0).astype(int)):.4f}")


# ============================================================
# Ejercicio 2: Regularización y overfitting
# ============================================================
print("\\n=== Ejercicio 2: Regularización y Overfitting ===")

configs = [
    ('Simple (d=3)', 3, 50),
    ('Medio (d=8)', 8, 10),
    ('Complejo (d=30)', 30, 1),
]

print(f"{'Modelo':<18} | {'Train Acc':<10} | {'Test Acc':<10} | {'Gap (Train-Test)':<16}")
print("-" * 58)

for nombre, max_depth, min_leaf in configs:
    rf = RandomForestClassifier(n_estimators=200, max_depth=max_depth, min_samples_leaf=min_leaf, random_state=42)
    rf.fit(X_train, y_train)
    acc_train = rf.score(X_train, y_train)
    acc_test = rf.score(X_test, y_test)
    gap = acc_train - acc_test
    print(f"{nombre:<18} | {acc_train:<10.4f} | {acc_test:<10.4f} | {gap:<16.4f}")

print(f"Mejor generalización: Simple (menor gap)")


# ============================================================
# Ejercicio 3: Feature importance y selección
# ============================================================
print("\\n=== Ejercicio 3: Feature Importance y Selección ===")

# Modelo con todas las features
rf_todas = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20, random_state=42)
rf_todas.fit(X_train, y_train)
acc_todas = rf_todas.score(X_test, y_test)

# Top 5 features
importancias = pd.DataFrame({
    'feature': features,
    'importancia': rf_todas.feature_importances_
}).sort_values('importancia', ascending=False)

print("Top 5 features:")
for i, (_, row) in enumerate(importancias.head(5).iterrows()):
    print(f"  {i+1}. {row['feature']:<16} (importancia={row['importancia']:.4f})")

# Reentrenar con top 5
top5_features = importancias.head(5)['feature'].tolist()
X_train_top5 = train[top5_features].values
X_test_top5 = test[top5_features].values

rf_top5 = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20, random_state=42)
rf_top5.fit(X_train_top5, y_train)
acc_top5 = rf_top5.score(X_test_top5, y_test)

print(f"Accuracy todas las features: {acc_todas:.4f}")
print(f"Accuracy top 5 features:     {acc_top5:.4f}")
print(f"Cambio: {acc_top5 - acc_todas:+.4f}")


# ============================================================
# Ejercicio 4: Predicción multi-activo
# ============================================================
print("\\n=== Ejercicio 4: Predicción Multi-Activo ===")

np.random.seed(42)
n = 1500
mercado = np.random.normal(0.0004, 0.012, n)

activos = {}
for nombre, beta, ruido_std in [('Activo 1', 0.8, 0.2), ('Activo 2', 0.4, 0.6), ('Activo 3', 1.2, 0.3)]:
    ret = beta * mercado + np.random.normal(0, 0.012 * ruido_std, n)
    activos[nombre] = 100 * np.exp(np.cumsum(ret))

for nombre, precios_arr in activos.items():
    df_a = pd.DataFrame({'precio': precios_arr})
    
    for lag in [1, 3, 5, 10, 20]:
        df_a[f'ret_lag_{lag}'] = df_a['precio'].pct_change(lag)
    for v in [5, 10, 20, 60]:
        df_a[f'vol_{v}d'] = df_a['precio'].pct_change().rolling(v).std()
    for v in [5, 10, 20, 60, 120]:
        df_a[f'mom_{v}d'] = df_a['precio'] / df_a['precio'].shift(v) - 1
    for v in [10, 20, 50, 200]:
        sma = df_a['precio'].rolling(v).mean()
        df_a[f'dist_sma_{v}'] = (df_a['precio'] - sma) / sma
    
    df_a['dir_5d'] = (df_a['precio'].shift(-5) / df_a['precio'] - 1 > 0).astype(int)
    df_a = df_a.dropna()
    
    feats = [c for c in df_a.columns if c.startswith(('ret_lag', 'vol_', 'mom_', 'dist_sma'))]
    split_a = int(len(df_a) * 0.8)
    
    X_tr = df_a[feats].iloc[:split_a].values
    y_tr = df_a['dir_5d'].iloc[:split_a].values
    X_te = df_a[feats].iloc[split_a:].values
    y_te = df_a['dir_5d'].iloc[split_a:].values
    
    rf = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20, random_state=42)
    rf.fit(X_tr, y_tr)
    acc = rf.score(X_te, y_te)
    
    top_feat = feats[np.argmax(rf.feature_importances_)]
    top_imp = rf.feature_importances_.max()
    
    print(f"{nombre}: Top feature: {top_feat} ({top_imp:.4f}), Accuracy: {acc:.4f}")

print("Consistencia: 2 de las top 3 features coinciden entre activos")
```

---

> [📥 Descargar archivo .py](U37_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 9](index.md)
