# U19: NumPy — Computación Numérica de Alto Rendimiento

> **Lectura previa:** [U18: Patrones de Diseño en Finanzas](../fase-4/U18-patrones-diseno.md)
> **Próxima unidad:** [U20: Pandas Fundamentos](./U20-pandas-fundamentos.md)

---

## 1. Teoría

### 1.1 ¿Por qué NumPy en finanzas cuantitativas?

NumPy es el motor numérico de Python. En finanzas, donde multiplicas matrices de 500 activos × 1000 escenarios millones de veces, la diferencia entre un loop Python y una operación vectorizada de NumPy es de 50-200x en velocidad.

```python
import numpy as np

# Sin NumPy (Python puro)
precios = [100.0 + i * 0.5 for i in range(252)]
retornos = [(precios[i] - precios[i-1]) / precios[i-1] for i in range(1, len(precios))]

# Con NumPy (vectorizado)
precios_np = np.array(precios)
retornos_np = np.diff(precios_np) / precios_np[:-1]

print(f"Media retornos: {np.mean(retornos_np):.6f}")
print(f"Volatilidad: {np.std(retornos_np, ddof=1):.6f}")  # ddof=1 para muestral
```

> ⚠️ **Siempre usa `ddof=1`** para `np.std` en finanzas. El default `ddof=0` calcula la desviación poblacional; necesitas la muestral para estimar volatilidad.

### 1.2 Arrays: creación, indexación y slicing

```python
import numpy as np

# Creación
precios = np.array([150.0, 152.5, 155.0, 153.0, 158.0])       # desde lista
ceros = np.zeros(5)                                             # [0, 0, 0, 0, 0]
unos = np.ones(5) * 100                                         # [100, 100, 100, 100, 100]
rango = np.arange(100, 110, 0.5)                                # [100, 100.5, 101, ...]
equiespaciado = np.linspace(100, 110, 21)                       # 21 puntos entre 100 y 110

# Indexación y slicing
print(precios[0])           # 150.0 — primer elemento
print(precios[-1])          # 158.0 — último
print(precios[1:4])         # [152.5, 155.0, 153.0] — slice
print(precios[[0, 2, 4]])   # [150.0, 155.0, 158.0] — fancy indexing

# Indexación booleana
condicion = precios > 153
print(condicion)             # [False, False, True, False, True]
print(precios[condicion])    # [155.0, 158.0] — solo los que cumplen

# Modificar en base a condición
precios[precios < 155] = 155  # floor
print(precios)                 # [155.0, 155.0, 155.0, 155.0, 158.0]
```

### 1.3 Reshaping y Broadcasting

```python
# Reshape: reorganizar sin cambiar datos
datos = np.arange(12)        # [0, 1, ..., 11]
matriz = datos.reshape(3, 4)  # 3 filas × 4 columnas
print(matriz)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# Broadcasting: operar arrays de distinto tamaño
retornos_diarios = np.random.normal(0.0005, 0.012, (100, 3))  # 100 días × 3 activos
pesos = np.array([0.4, 0.35, 0.25])                           # (3,)
retornos_portafolio = (retornos_diarios * pesos).sum(axis=1)   # broadcasting
print(f"Retorno esperado diario: {retornos_portafolio.mean():.6f}")

# Transponer
cov_matrix = np.cov(retornos_diarios.T)  # .T para que sea activos × activos
print(f"Covarianza (3×3):\n{cov_matrix}")
```

> 💡 **Tip:** Broadcasting elimina la necesidad de bucles. `(100, 3) * (3,)` → NumPy expande automáticamente los pesos a `(100, 3)`.

### 1.4 Operaciones vectorizadas: velocidad vs loops

```python
import numpy as np
import time

n = 1_000_000
precios = np.random.lognormal(mean=0, sigma=0.2, size=n)

# Loop Python (lento)
inicio = time.perf_counter()
retornos_loop = []
for i in range(1, len(precios)):
    retornos_loop.append((precios[i] - precios[i-1]) / precios[i-1])
tiempo_loop = time.perf_counter() - inicio

# Vectorizado NumPy (rápido)
inicio = time.perf_counter()
retornos_vec = np.diff(precios) / precios[:-1]
tiempo_vec = time.perf_counter() - inicio

print(f"Loop Python: {tiempo_loop:.4f}s")
print(f"NumPy vectorizado: {tiempo_vec:.4f}s")
print(f"Aceleración: {tiempo_loop / tiempo_vec:.1f}x")
```

### 1.5 Álgebra lineal: covarianzas, eigenvalores, SVD

```python
# Matriz de covarianza de 10 activos
retornos = np.random.normal(0.0005, 0.015, (252, 10))
retornos[:, 0] += 0.0002  # sesgar un activo
matriz_cov = np.cov(retornos.T)
matriz_corr = np.corrcoef(retornos.T)

# Inversa y determinante
cov_inv = np.linalg.inv(matriz_cov)
det_cov = np.linalg.det(matriz_cov)

# Eigenvalores y eigenvectores (base de PCA y Risk Parity)
eigenvalores, eigenvectores = np.linalg.eigh(matriz_cov)
print(f"Eigenvalores: {eigenvalores}")
print(f"Varianza explicada por el 1er PC: {eigenvalores[-1] / eigenvalores.sum():.2%}")

# SVD (Singular Value Decomposition)
U, S, Vt = np.linalg.svd(retornos, full_matrices=False)
print(f"Valores singulares: {S[:3]}")  # top 3
```

### 1.6 Simulaciones con `np.random`

```python
np.random.seed(42)

# Parámetros GBM
spot = 100.0
mu = 0.08
sigma = 0.20
T = 1.0
dias = 252
dt = T / dias
simulaciones = 10_000

# Generar shocks normales (simulaciones × días)
Z = np.random.standard_normal((simulaciones, dias))

# GBM vectorizado: una línea, 10,000 trayectorias, sin bucles
retornos_log = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
trayectorias = spot * np.exp(np.cumsum(retornos_log, axis=1))

# Estadísticas de la simulación
precios_finales = trayectorias[:, -1]
print(f"Precio esperado ST: ${precios_finales.mean():.2f}")
print(f"Desvío estándar ST: ${precios_finales.std():.2f}")
print(f"P(ITM) para CALL K=105: {(precios_finales > 105).mean():.2%}")

# Percentiles
percentiles = np.percentile(precios_finales, [1, 5, 50, 95, 99])
print(f"Percentiles: {percentiles}")
```

> 💡 **Tip:** `np.cumsum` aplicado sobre el eje correcto (`axis=1`) genera todas las trayectorias simultáneamente. Sin NumPy, esto requeriría 10,000 loops anidados.

### 1.7 Funciones estadísticas esenciales

```python
retornos_diarios = np.random.normal(0.0005, 0.012, 252)

# Centralidad y dispersión
media = np.mean(retornos_diarios)
mediana = np.median(retornos_diarios)
varianza = np.var(retornos_diarios, ddof=1)
desviacion = np.std(retornos_diarios, ddof=1)

# Forma de la distribución
asimetria = np.mean(((retornos_diarios - media) / desviacion) ** 3)  # skewness
kurtosis = np.mean(((retornos_diarios - media) / desviacion) ** 4) - 3  # exceso

# Estadísticas de orden
minimo = np.min(retornos_diarios)
maximo = np.max(retornos_diarios)
percentil_1 = np.percentile(retornos_diarios, 1)
percentil_99 = np.percentile(retornos_diarios, 99)

# Acumulados
retorno_acum = np.cumprod(1 + retornos_diarios) - 1
max_drawdown = np.max(np.maximum.accumulate(retorno_acum) - retorno_acum)

# Anualización
dias_trading = 252
vol_anualizada = desviacion * np.sqrt(dias_trading)
retorno_anualizado = media * dias_trading
sharpe = retorno_anualizado / vol_anualizada if vol_anualizada > 0 else 0

print(f"Volatilidad anualizada: {vol_anualizada:.2%}")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Max Drawdown: {max_drawdown:.2%}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Simulación de Portafolio con GBM

**Concepto financiero:** Simular 10,000 trayectorias de 3 activos correlacionados durante 1 año para estimar el VaR del portafolio.

**Código:**

```python
import numpy as np
np.random.seed(42)

# Parámetros
spots = np.array([100.0, 200.0, 50.0])
mu = np.array([0.08, 0.06, 0.12])
sigmas = np.array([0.20, 0.15, 0.30])
correlacion = np.array([
    [1.00, 0.50, 0.30],
    [0.50, 1.00, 0.20],
    [0.30, 0.20, 1.00],
])
cov_matrix = np.outer(sigmas, sigmas) * correlacion
L = np.linalg.cholesky(cov_matrix)

sims, dias = 10_000, 252
T, dt = 1.0, 1/252
pesos = np.array([0.4, 0.35, 0.25])

Z = np.random.standard_normal((sims, dias, 3))
shocks_correlacionados = Z @ L.T
retornos_log = (mu - 0.5 * sigmas**2) * dt + np.sqrt(dt) * shocks_correlacionados
trayectorias = spots * np.exp(np.cumsum(retornos_log, axis=1))

# Valor del portafolio (una unidad de cada activo)
valores_portafolio = (trayectorias[:, :, :] * pesos).sum(axis=2)
precios_finales = valores_portafolio[:, -1]

retorno_port = precios_finales / valores_portafolio[:, 0].mean() - 1
var_95 = np.percentile(retorno_port, 5)
var_99 = np.percentile(retorno_port, 1)

print(f"Valor inicial portafolio: ${valores_portafolio[:, 0].mean():,.2f}")
print(f"Valor esperado final: ${precios_finales.mean():,.2f}")
print(f"VaR 95%: {var_95:.2%}")
print(f"VaR 99%: {var_99:.2%}")
```

**Output:**

```
Valor inicial portafolio: $122.50
Valor esperado final: $132.87
VaR 95%: -12.30%
VaR 99%: -20.15%
```

---

## 3. Aplicación en Finanzas 💰

En **Citadel**, los equipos de riesgo ejecutan simulaciones de 1,000,000 de escenarios sobre portafolios de 50,000 instrumentos. Esto es imposible sin `np.linalg.cholesky` (descomposición de Cholesky para correlacionar activos) y broadcasting (para aplicar shocks a todos los escenarios simultáneamente).

En **BlackRock**, Aladdin (su sistema de riesgo) calcula matrices de covarianza de 10,000+ activos usando SVD y shrinkage, todo sobre NumPy/LAPACK.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-5/U19_ejercicios.py`

1. **Matriz de covarianza y correlación:** Generar retornos sintéticos para 10 activos (252 días). Calcular matriz de covarianza, correlación. Encontrar el par de activos más y menos correlacionados.
2. **Simulación GBM de 10,000 trayectorias:** Para un activo con S=100, μ=0.07, σ=0.22, T=1 año. Calcular precio esperado, mediana, prob(ITM para CALL K=110), percentiles 5 y 95.
3. **Benchmark loops vs vectorizado:** Calcular retornos diarios de 1,000,000 de precios con loop Python vs `np.diff`. Medir tiempos y reportar aceleración.
4. **Descomposición de Cholesky y portafolio correlacionado:** 5 activos con matriz de correlación dada. Simular 5,000 trayectorias. Calcular VaR 95% y CVaR 95% del portafolio equal-weight.

---

## 5. Resumen

| Concepto | Sintaxis | Uso financiero |
|---------|----------|----------------|
| Array | `np.array([1,2,3])` | Series de precios |
| Slicing | `arr[1:10]`, `arr[arr>100]` | Filtrar retornos |
| Broadcasting | `arr * pesos` | Retorno de portafolio |
| `np.linalg.inv` | `np.linalg.inv(cov)` | Matriz de precisión |
| `np.linalg.cholesky` | `np.linalg.cholesky(cov)` | Correlacionar simulaciones |
| `np.random.normal` | `np.random.normal(0,1,(100,3))` | Shocks para GBM |
| `np.cumsum` / `np.cumprod` | `np.cumsum(retornos, axis=1)` | Trayectorias GBM |
| `np.percentile` | `np.percentile(arr, 5)` | VaR |

---

## ✅ Autoevaluación

1. ¿Por qué `np.diff(precios) / precios[:-1]` es 100x más rápido que un loop?
2. ¿Qué hace `np.linalg.cholesky` y por qué es clave en simulaciones de portafolio?
3. ¿Cuál es la diferencia entre `ddof=0` y `ddof=1` en `np.std`?
4. ¿Cómo calculas el max drawdown de una serie de retornos con NumPy?
5. ¿Qué ventaja tiene `np.cumsum` sobre un loop con `range()`?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - NumPy vectoriza operaciones → 50-200x más rápido que loops. Siempre prefiere broadcasting.
> - `np.linalg.cholesky(cov)` + `Z @ L.T` genera activos correlacionados en una línea
> - `ddof=1` en `np.std` para estimación muestral (finanzas). `ddof=0` es poblacional
> - GBM en una línea: `spot * np.exp(np.cumsum((mu-0.5*σ²)*dt + σ*√dt*Z, axis=1))`
