# U37: Machine Learning para Finanzas — Fundamentos

> **Lectura previa:** [U36: SQL para Datos Financieros](../fase-8/U36-sql.md)
> **Próxima unidad:** [U38: Machine Learning Avanzado — Métodos Cuantitativos](./U38-ml-avanzado.md)

---

## 1. Teoría

### 1.1 ¿Por qué ML en finanzas?

El machine learning complementa (no reemplaza) la econometría tradicional. En finanzas cuantitativas, ML se usa para:

- **Predicción de retornos:** ¿Subirá o bajará el mercado esta semana?
- **Clasificación de regímenes:** ¿Estamos en bull, bear o sideways?
- **Feature engineering:** Crear variables predictivas a partir de datos crudos
- **Modelos no lineales:** Capturar relaciones que OLS no puede modelar

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
```

> ⚠️ **Advertencia fundamental:** En finanzas NO puedes usar cross-validation aleatorio (KFold). Los datos tienen estructura temporal. Si mezclas pasado con futuro, tu modelo "aprende del futuro" y los resultados en paper son espectaculares pero en producción pierdes dinero. **Siempre TimeSeriesSplit.**

### 1.2 Feature Engineering Financiero

Las features (variables predictoras) son lo que realmente hace la diferencia. Un random forest con buenas features supera a XGBoost con features malas.

```python
np.random.seed(42)
fechas = pd.date_range('2020-01-01', '2024-12-31', freq='B')
n = len(fechas)

# Simular precios
retornos = np.random.normal(0.0004, 0.012, n)
precios = 100 * np.exp(np.cumsum(retornos))
df = pd.DataFrame({'precio': precios}, index=fechas)

# --- Feature engineering financiero ---

# 1. Retornos rezagados (lagged returns)
for lag in [1, 2, 3, 5, 10, 20]:
    df[f'retorno_lag_{lag}'] = df['precio'].pct_change(lag)

# 2. Volatilidad histórica (rolling std)
for ventana in [5, 10, 20, 60]:
    df[f'volatilidad_{ventana}d'] = df['precio'].pct_change().rolling(ventana).std()

# 3. Momentum (tasas de cambio)
for ventana in [5, 10, 20, 60, 120]:
    df[f'momentum_{ventana}d'] = df['precio'] / df['precio'].shift(ventana) - 1

# 4. Medias móviles y distancia a la media
for ventana in [10, 20, 50, 200]:
    sma = df['precio'].rolling(ventana).mean()
    df[f'dist_sma_{ventana}'] = (df['precio'] - sma) / sma

# 5. Target: dirección del mercado a 5 días (1 semana)
df['retorno_futuro_5d'] = df['precio'].shift(-5) / df['precio'] - 1
df['direccion_5d'] = (df['retorno_futuro_5d'] > 0).astype(int)

# 6. Variables de volumen (si tuviéramos)
# df['volumen_ratio'] = df['volumen'] / df['volumen'].rolling(20).mean()

# Limpiar NaN
df = df.dropna()

print(f"Dataset: {len(df)} filas, {len(df.columns)} columnas")
print(f"Features creadas: {[c for c in df.columns if c not in ['precio', 'retorno_futuro_5d', 'direccion_5d']]}")
print(f"Target: {df['direccion_5d'].value_counts().to_dict()}")
```

> 💡 **Dato curioso:** Renaissance Technologies usa miles de features para sus modelos. Muchas son transformaciones de datos de mercado aparentemente simples (rezagos, ratios, volatilidades) combinadas de formas no lineales.

### 1.3 Train/Test Split Temporal

La regla de oro: **nunca entrenes con datos futuros y pruebes con datos pasados.**

```python
# Split temporal: entrenar con los primeros 80%, testear con los últimos 20%
split_idx = int(len(df) * 0.8)
train = df.iloc[:split_idx]
test = df.iloc[split_idx:]

print(f"Train: {train.index[0].date()} → {train.index[-1].date()} ({len(train)} días)")
print(f"Test:  {test.index[0].date()} → {test.index[-1].date()} ({len(test)} días)")

# TimeSeriesSplit para validación cruzada temporal
tscv = TimeSeriesSplit(n_splits=5)

feature_cols = [c for c in df.columns if c.startswith(('retorno_lag', 'volatilidad', 'momentum', 'dist_sma'))]
X = df[feature_cols].values
y = df['direccion_5d'].values

for i, (train_idx, val_idx) in enumerate(tscv.split(X)):
    print(f"Fold {i}: train={train_idx[0]}:{train_idx[-1]}, val={val_idx[0]}:{val_idx[-1]}")
```

### 1.4 Random Forest para Clasificación Financiera

Random Forest es un excelente primer modelo para predicción financiera: maneja no linealidades, es robusto a outliers, y da feature importance "gratis".

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Pipeline con scaling + modelo
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(
        n_estimators=200,
        max_depth=5,          # limitar profundidad para evitar overfitting
        min_samples_leaf=20,  # mínimo de muestras por hoja
        random_state=42,
        n_jobs=-1
    ))
])

# Entrenar
X_train = train[feature_cols].values
y_train = train['direccion_5d'].values
X_test = test[feature_cols].values
y_test = test['direccion_5d'].values

pipeline.fit(X_train, y_train)

# Predecir
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

# Métricas
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC-ROC:  {roc_auc_score(y_test, y_prob):.4f}")
print(f"\nMatriz de confusión:\n{confusion_matrix(y_test, y_pred)}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
```

### 1.5 Feature Importance

```python
# Importancia de features
rf_model = pipeline.named_steps['rf']
importancias = pd.DataFrame({
    'feature': feature_cols,
    'importancia': rf_model.feature_importances_
}).sort_values('importancia', ascending=False)

print("=== Top 10 Features por Importancia ===\n")
print(importancias.head(10).to_string(index=False))
```

### 1.6 Overfitting y Regularización

El overfitting es el enemigo #1 en ML financiero. Señales de overfitting:

- Accuracy en train >> accuracy en test (gap grande)
- El modelo "memoriza" ruido en lugar de aprender patrones
- Performance en backtest espectacular, en producción real desastrosa

```python
# Técnicas de regularización en Random Forest:
# 1. max_depth: limita la profundidad del árbol
# 2. min_samples_split: mínimo de muestras para dividir un nodo
# 3. min_samples_leaf: mínimo de muestras en hoja
# 4. max_features: fracción de features usadas en cada split
# 5. n_estimators: más árboles = más estable (pero más lento)

# Comparar modelo simple vs complejo
modelo_simple = RandomForestClassifier(n_estimators=100, max_depth=3, min_samples_leaf=50, random_state=42)
modelo_complejo = RandomForestClassifier(n_estimators=500, max_depth=20, min_samples_leaf=1, random_state=42)

for nombre, modelo in [('Simple', modelo_simple), ('Complejo', modelo_complejo)]:
    modelo.fit(X_train, y_train)
    acc_train = modelo.score(X_train, y_train)
    acc_test = modelo.score(X_test, y_test)
    print(f"{nombre}: Train acc={acc_train:.4f}, Test acc={acc_test:.4f}, Gap={acc_train - acc_test:.4f}")
```

### 1.7 Comparación con Benchmark

En finanzas, el benchmark NO es accuracy = 50% (random guess). El benchmark es:

1. **Naive:** ¿Sube o baja? Predecir siempre la clase mayoritaria
2. **Momentum:** Si el retorno de ayer fue positivo → predecir subida
3. **Mean reversion:** Si el retorno de ayer fue positivo → predecir bajada

```python
# Benchmark 1: Siempre predecir subida
acc_siempre_sube = (y_test == 1).mean()
print(f"Benchmark 'siempre sube': {acc_siempre_sube:.4f}")

# Benchmark 2: Seguir la tendencia (momentum naive)
# Si retorno_lag_1 > 0, predecir subida
pred_momentum = (X_test[:, feature_cols.index('retorno_lag_1')] > 0).astype(int)
acc_momentum = accuracy_score(y_test, pred_momentum)
print(f"Benchmark momentum: {acc_momentum:.4f}")

# Benchmark 3: Mean reversion
pred_reversion = (X_test[:, feature_cols.index('retorno_lag_1')] < 0).astype(int)
acc_reversion = accuracy_score(y_test, pred_reversion)
print(f"Benchmark reversion: {acc_reversion:.4f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Predecir dirección semanal del mercado

**Concepto financiero:** Predecir si el mercado subirá o bajará la próxima semana es una señal base para estrategias de market timing.

**Código:**

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# 1. Generar datos
np.random.seed(42)
n = 1500
retornos = np.random.normal(0.0004, 0.012, n)
precios = 100 * np.exp(np.cumsum(retornos))
df = pd.DataFrame({
    'precio': precios,
}, index=pd.date_range('2019-01-01', periods=n, freq='B'))

# 2. Feature engineering
for lag in [1, 3, 5, 10, 20]:
    df[f'ret_lag_{lag}'] = df['precio'].pct_change(lag)
for v in [5, 10, 20, 60]:
    df[f'vol_{v}d'] = df['precio'].pct_change().rolling(v).std()
for v in [5, 20, 60, 120]:
    df[f'mom_{v}d'] = df['precio'] / df['precio'].shift(v) - 1

# Target: dirección a 5 días
df['dir_5d'] = (df['precio'].shift(-5) / df['precio'] - 1 > 0).astype(int)
df = df.dropna()

# 3. Split temporal
split = int(len(df) * 0.8)
train, test = df.iloc[:split], df.iloc[split:]

features = [c for c in df.columns if any(c.startswith(p) for p in ['ret_lag', 'vol_', 'mom_'])]
X_train, y_train = train[features].values, train['dir_5d'].values
X_test, y_test = test[features].values, test['dir_5d'].values

# 4. TimeSeriesSplit CV
tscv = TimeSeriesSplit(n_splits=5)
print("=== Validación cruzada temporal ===\n")
fold_scores = []
for i, (tr_idx, val_idx) in enumerate(tscv.split(X_train)):
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, min_samples_leaf=20, random_state=42)
    rf.fit(X_train[tr_idx], y_train[tr_idx])
    acc = rf.score(X_train[val_idx], y_train[val_idx])
    fold_scores.append(acc)
    print(f"Fold {i+1}: Accuracy = {acc:.4f}")
print(f"\nCV Accuracy promedio: {np.mean(fold_scores):.4f} (+/- {np.std(fold_scores):.4f})")

# 5. Modelo final
rf_final = RandomForestClassifier(n_estimators=200, max_depth=5, min_samples_leaf=20, random_state=42)
rf_final.fit(X_train, y_train)
y_pred = rf_final.predict(X_test)
y_prob = rf_final.predict_proba(X_test)[:, 1]

print(f"\n=== Resultados en Test ===\n")
print(f"Accuracy:        {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC-ROC:         {roc_auc_score(y_test, y_prob):.4f}")
print(f"Siempre sube:    {(y_test == 1).mean():.4f} (benchmark)")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Baja', 'Sube']))
```

**Output:**
```
=== Validación cruzada temporal ===

Fold 1: Accuracy = 0.5423
Fold 2: Accuracy = 0.5381
Fold 3: Accuracy = 0.5512
Fold 4: Accuracy = 0.5298
Fold 5: Accuracy = 0.5456

CV Accuracy promedio: 0.5414 (+/- 0.0072)

=== Resultados en Test ===

Accuracy:        0.5345
AUC-ROC:         0.5512
Siempre sube:    0.5189 (benchmark)
```

---

## 3. Aplicación en Finanzas 💰

**Two Sigma y Renaissance Technologies:** Estos fondos usan random forests y gradient boosting como parte de ensembles más grandes. Un random forest típico en producción tiene cientos de features y se reentrena diariamente con nuevos datos.

**Predicción de defaults (JP Morgan):** Los modelos de credit scoring usan variantes de random forest para predecir probabilidad de default. La feature importance ayuda a los oficiales de crédito a entender qué variables pesan más.

**Market making (Citadel):** Los modelos de ML predicen la dirección del flujo de órdenes en los próximos segundos/minutos. Un accuracy de 52-53% sostenido, con suficientes transacciones, genera retornos significativos.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-9/U37_ejercicios.py`

1. **Pipeline de features:** Crear 15+ features financieras (retornos rezagados, volatilidad, momentum, distancia a SMA). Entrenar random forest con TimeSeriesSplit. Comparar con baseline naive.

2. **Regularización y overfitting:** Entrenar 3 modelos con distinta complejidad (max_depth=3, 10, 30) y comparar performance en train vs test. Graficar accuracy vs profundidad.

3. **Feature importance y selección:** Entrenar modelo con todas las features, rankear por importancia, reentrenar solo con las top 5. ¿Mejora o empeora la performance?

4. **Predicción multi-activo:** Simular datos de 3 activos correlacionados. Entrenar modelos separados para cada uno. Comparar la estabilidad de feature importance entre activos.

---

## 5. Resumen

| Concepto | Código |
|----------|--------|
| TimeSeriesSplit | `TimeSeriesSplit(n_splits=5)` |
| Feature engineering | `pct_change(lag)`, `rolling(w).std()` |
| RandomForest | `RandomForestClassifier(n_estimators=200, max_depth=5)` |
| Pipeline | `Pipeline([('scaler', StandardScaler()), ('rf', RF())])` |
| Accuracy | `accuracy_score(y_test, y_pred)` |
| AUC-ROC | `roc_auc_score(y_test, y_prob)` |
| Feature importance | `rf.feature_importances_` |
| Regularización | `max_depth`, `min_samples_leaf`, `min_samples_split` |

---

## ✅ Autoevaluación

1. ¿Por qué NO podemos usar KFold cross-validation en datos financieros?
2. ¿Qué ventaja tiene Random Forest sobre una regresión logística para predicción financiera?
3. Explica qué es el overfitting en el contexto de predicción de retornos y cómo detectarlo.
4. ¿Qué métrica es más importante en un problema de predicción de dirección de mercado: accuracy o AUC-ROC? ¿Por qué?
5. Si tu modelo tiene accuracy = 51% en test, ¿es bueno o malo? ¿Comparado con qué benchmark?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - NUNCA uses KFold en finanzas. Siempre TimeSeriesSplit.
> - Feature engineering > elección de modelo. Dedica 80% del tiempo a crear buenas features.
> - Overfitting es letal: train acc >> test acc. Regulariza con max_depth, min_samples_leaf.
> - Accuracy 51-53% sostenido en predicción de dirección puede ser muy rentable con suficientes transacciones.
> - Siempre compara contra benchmarks naive: "siempre sube", tendencia, mean reversion.
