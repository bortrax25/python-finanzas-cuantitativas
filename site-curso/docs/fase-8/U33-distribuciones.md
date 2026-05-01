# U33: Probabilidad, Estadística y Distribuciones Financieras

> **Lectura previa:** [U32: Optimización Avanzada de Portafolios](../fase-7/U32-optimizacion-avanzada.md)
> **Próxima unidad:** [U34: Series de Tiempo — ARIMA y Volatilidad](./U34-series-tiempo.md)

---

## 1. Teoría

### 1.1 Por qué las distribuciones importan en finanzas

En finanzas cuantitativas, los retornos de los activos NO siguen una distribución normal perfecta. Tienen **colas gruesas** (fat tails): eventos extremos ocurren con más frecuencia de lo que la normal predice. Entender qué distribución sigue tu activo es crítico para:

- Calcular VaR (Value at Risk) correctamente
- Preciar opciones fuera del dinero
- Simular escenarios de estrés con Monte Carlo
- Construir portafolios robustos a eventos extremos

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Simulemos retornos de un activo con fat tails
np.random.seed(42)
retornos_normales = np.random.normal(0.001, 0.02, 1000)        # Normal
retornos_colas = np.random.standard_t(df=3, size=1000) * 0.01  # t-Student (colas gruesas)

print(f"Normal: skew={stats.skew(retornos_normales):.3f}, kurt={stats.kurtosis(retornos_normales):.3f}")
print(f"t(3):   skew={stats.skew(retornos_colas):.3f}, kurt={stats.kurtosis(retornos_colas):.3f}")
```

> 💡 **Dato curioso:** En octubre de 1987, el S&P 500 cayó 20.5% en un día. Bajo una distribución normal, esto debería ocurrir una vez cada varios miles de millones de años. Claramente, los mercados no son normales.

### 1.2 Distribuciones clave en finanzas

#### Distribución Normal (Gaussiana)

La base de la teoría moderna de portafolios, Black-Scholes y VaR paramétrico. Se define por su media `μ` y desviación estándar `σ`.

```python
from scipy.stats import norm

mu, sigma = 0.001, 0.02  # 0.1% retorno diario, 2% volatilidad

# PDF, CDF, generación de muestras
x = np.linspace(-0.06, 0.06, 100)
densidad = norm.pdf(x, mu, sigma)
probabilidad = norm.cdf(0, mu, sigma)  # P(retorno < 0)
cuantil_5 = norm.ppf(0.05, mu, sigma)  # VaR al 95%

print(f"Probabilidad de retorno negativo: {probabilidad:.4f}")
print(f"VaR 95% paramétrico: {cuantil_5:.4f}")
```

#### Distribución Log-Normal

Los precios de activos se modelan como log-normales (el logaritmo del precio es normal). Esto evita precios negativos, algo imposible en la realidad.

```python
from scipy.stats import lognorm

# Si el log-rendimiento diario ~ N(mu, sigma), el multiplicador de precio es log-normal
s = sigma       # parámetro de forma
scale = np.exp(mu)  # escala

precio_simulado = lognorm.rvs(s=s, scale=scale, size=1000)
print(f"Precio relativo medio: {precio_simulado.mean():.4f}")
print(f"Probabilidad precio < 1 (pérdida): {(precio_simulado < 1).mean():.3f}")
```

#### Distribución t-Student

Captura las colas gruesas de los retornos financieros. A menor `df` (grados de libertad), más gruesas son las colas.

```python
from scipy.stats import t

# Ajustar t-Student a retornos reales
retornos_reales = np.array([0.003, -0.012, 0.008, -0.025, 0.015, -0.001, 0.022, -0.018])
parametros_t = t.fit(retornos_reales)
df_ajustado, loc_ajustado, scale_ajustado = parametros_t

print(f"t-Student ajustada: df={df_ajustado:.2f}, loc={loc_ajustado:.4f}, scale={scale_ajustado:.4f}")
print(f"Colas: df bajo (~3) = colas muy gruesas; df > 30 = se aproxima a normal")
```

> ⚠️ **Error común:** Usar la distribución normal para modelar retornos diarios de criptomonedas o acciones de pequeña capitalización. Siempre verifica con tests de normalidad antes de asumir normalidad.

### 1.3 Tests de normalidad

Para decidir si puedes usar modelos basados en normalidad, aplica estos tests:

```python
from scipy.stats import jarque_bera, shapiro, kstest, probplot

# 1. Jarque-Bera (basado en skewness y kurtosis)
jb_stat, jb_pvalue = jarque_bera(retornos_reales)
print(f"Jarque-Bera: estadístico={jb_stat:.3f}, p-value={jb_pvalue:.4f}")

# 2. Shapiro-Wilk (más potente en muestras pequeñas)
sh_stat, sh_pvalue = shapiro(retornos_reales)
print(f"Shapiro-Wilk: estadístico={sh_stat:.3f}, p-value={sh_pvalue:.4f}")

# 3. Kolmogorov-Smirnov (compara con normal teórica)
ks_stat, ks_pvalue = kstest(retornos_reales, 'norm', args=(retornos_reales.mean(), retornos_reales.std(ddof=1)))
print(f"Kolmogorov-Smirnov: estadístico={ks_stat:.3f}, p-value={ks_pvalue:.4f}")

# Interpretación: si p-value < 0.05, rechazamos normalidad al 95% de confianza
```

#### Q-Q Plot (gráfico cuantil-cuantil)

Visualiza si los datos siguen una distribución de referencia.

```python
import scipy.stats as stats
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Datos normales
datos_normales = np.random.normal(0, 1, 200)
stats.probplot(datos_normales, dist="norm", plot=ax[0])
ax[0].set_title("Q-Q Plot: Datos normales")

# Datos con colas gruesas
datos_colas = np.random.standard_t(df=4, size=200)
stats.probplot(datos_colas, dist="norm", plot=ax[1])
ax[1].set_title("Q-Q Plot: Datos t-Student (colas gruesas)")

plt.tight_layout()
# plt.show()  # Descomentar en Jupyter
```

> 💡 **Interpretación del Q-Q Plot:** Si los puntos se alinean con la recta diagonal, los datos siguen la distribución de referencia. Desviaciones en los extremos (cola izquierda/derecha) indican fat tails o asimetría.

### 1.4 Bootstrap para intervalos de confianza

Cuando no conocemos la distribución subyacente, el bootstrap nos permite estimar intervalos de confianza sin asumir normalidad. Es intensivo computacionalmente pero muy robusto.

```python
def bootstrap_intervalo(datos, estadistico=np.mean, n_bootstrap=10000, alpha=0.05):
    """
    Intervalo de confianza por bootstrap percentil.
    
    Parámetros:
        datos: array-like de observaciones
        estadistico: función que calcula el estadístico (por defecto media)
        n_bootstrap: número de remuestreos
        alpha: nivel de significancia (0.05 = intervalo al 95%)
    """
    np.random.seed(42)
    estimaciones = np.zeros(n_bootstrap)
    n = len(datos)
    
    for i in range(n_bootstrap):
        muestra = np.random.choice(datos, size=n, replace=True)
        estimaciones[i] = estadistico(muestra)
    
    limite_inferior = np.percentile(estimaciones, alpha / 2 * 100)
    limite_superior = np.percentile(estimaciones, (1 - alpha / 2) * 100)
    
    return limite_inferior, limite_superior, estimaciones

# Ejemplo: IC para la media de retornos del S&P 500
sp500_retornos = np.random.normal(0.0004, 0.012, 500)  # Simulado
li, ls, _ = bootstrap_intervalo(sp500_retornos)

print(f"Media observada: {sp500_retornos.mean():.6f}")
print(f"IC 95% bootstrap: [{li:.6f}, {ls:.6f}]")
```

### 1.5 Random Walk y Movimiento Browniano Geométrico (GBM)

El GBM es el modelo estándar para simular precios de activos:

```
dS_t = μ·S_t·dt + σ·S_t·dW_t
```

Donde `dW_t` es un proceso de Wiener (incrementos normales independientes).

```python
def simular_gbm(precio_inicial, mu, sigma, dias, n_simulaciones, seed=42):
    """
    Simula trayectorias de precios con Movimiento Browniano Geométrico.
    
    Parámetros:
        precio_inicial: S_0
        mu: retorno esperado anualizado (drift)
        sigma: volatilidad anualizada
        dias: horizonte en días
        n_simulaciones: número de trayectorias
    """
    np.random.seed(seed)
    dt = 1 / 252  # un día de trading
    t = np.arange(0, dias)
    
    # Ecuación discretizada: S_{t+1} = S_t * exp((mu - sigma^2/2)*dt + sigma*sqrt(dt)*Z)
    precios = np.zeros((dias, n_simulaciones))
    precios[0, :] = precio_inicial
    
    for i in range(1, dias):
        z = np.random.standard_normal(n_simulaciones)
        precios[i, :] = precios[i - 1, :] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
        )
    
    return precios

# Simular 5 trayectorias de AAPL a 252 días
trayectorias = simular_gbm(precio_inicial=100, mu=0.10, sigma=0.25, dias=252, n_simulaciones=5)

precios_finales = trayectorias[-1, :]
print(f"Precios finales: media={precios_finales.mean():.2f}, std={precios_finales.std():.2f}")
print(f"Retorno medio: {(precios_finales.mean() / 100 - 1) * 100:.2f}%")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Análisis de distribución de retornos de una acción

**Concepto financiero:** Antes de aplicar cualquier modelo cuantitativo (VaR, opciones, optimización), debemos conocer la distribución de los retornos.

**Código:**

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Datos simulados de retornos diarios de AAPL (1 año)
np.random.seed(42)
# Simulamos con t-Student para tener colas gruesas
retornos = np.random.standard_t(df=4, size=252) * 0.005 + 0.001

# 1. Estadísticas descriptivas
print("=== Estadísticas descriptivas ===")
print(f"Media:            {retornos.mean():.6f}")
print(f"Desv. estándar:   {retornos.std():.6f}")
print(f"Skewness:         {stats.skew(retornos):.4f}")
print(f"Kurtosis (exceso):{stats.kurtosis(retornos):.4f}")
print(f"Mínimo:           {retornos.min():.6f}")
print(f"Máximo:           {retornos.max():.6f}")

# 2. Tests de normalidad
jb_stat, jb_p = stats.jarque_bera(retornos)
sh_stat, sh_p = stats.shapiro(retornos)
print(f"\n=== Tests de normalidad ===")
print(f"Jarque-Bera:  estadístico={jb_stat:.2f}, p-value={jb_p:.6f}")
print(f"Shapiro-Wilk: estadístico={sh_stat:.4f}, p-value={sh_p:.6f}")
print(f"Conclusión: {'Normal' if sh_p > 0.05 else 'NO normal'} al 95% de confianza")

# 3. Ajustar distribución t-Student
df_t, loc_t, scale_t = stats.t.fit(retornos)
print(f"\n=== Ajuste t-Student ===")
print(f"Grados de libertad (df): {df_t:.2f}")
print(f"Parámetro de escala:     {scale_t:.6f}")
print(f"Interpretación: df bajos (< 10) indican colas muy gruesas")

# 4. Calcular VaR histórico vs VaR paramétrico (normal) vs VaR t-Student
var_95_historico = np.percentile(retornos, 5)
var_95_normal = stats.norm.ppf(0.05, loc=retornos.mean(), scale=retornos.std())
var_95_tstudent = stats.t.ppf(0.05, df=df_t, loc=loc_t, scale=scale_t)

print(f"\n=== Value at Risk (95%) ===")
print(f"VaR Histórico:   {var_95_historico:.4%}")
print(f"VaR Normal:      {var_95_normal:.4%}")
print(f"VaR t-Student:   {var_95_tstudent:.4%}")
```

**Output:**
```
=== Estadísticas descriptivas ===
Media:            0.001243
Desv. estándar:   0.007546
Skewness:         0.1044
Kurtosis (exceso):1.3644
Mínimo:           -0.023801
Máximo:           0.027627

=== Tests de normalidad ===
Jarque-Bera:  estadístico=20.02, p-value=0.000045
Shapiro-Wilk: estadístico=0.9739, p-value=0.000120
Conclusión: NO normal al 95% de confianza

=== Ajuste t-Student ===
Grados de libertad (df): 4.34
Parámetro de escala:     0.005587
Interpretación: df bajos (< 10) indican colas muy gruesas

=== Value at Risk (95%) ===
VaR Histórico:   -1.0045%
VaR Normal:      -1.0991%
VaR t-Student:   -1.1438%
```

---

## 3. Aplicación en Finanzas 💰

En Citadel, Jane Street y Renaissance Technologies, el análisis de distribuciones de retornos es **la primera tarea** antes de cualquier modelado:

1. **Risk Management:** Si asumes normalidad cuando los retornos tienen colas gruesas, tu VaR subestimará el riesgo real. Después de 2008, los reguladores exigen CVaR (Expected Shortfall) precisamente por esto.

2. **Options Pricing:** El volatility smile (sonrisa de volatilidad) existe porque el mercado le asigna un precio a las fat tails. Un modelo de Black-Scholes ingenuo no captura esto.

3. **Factor Investing:** Los retornos de estrategias long-short (momentum, value, quality) tampoco son normales. Analizar su distribución es clave para entender los riesgos no lineales del portafolio.

4. **Monte Carlo en Asset Management:** Cuando proyectas 30 años de retiros en un portafolio de jubilación, NO uses retornos normales. Usa distribuciones con colas gruesas o bootstrapping histórico.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-8/U33_ejercicios.py`

1. **Estadísticas y tests de normalidad:** Dado un array de retornos de 50 activos del S&P 500, calcular media, volatilidad, skewness, kurtosis para cada uno. Identificar cuáles rechazan normalidad.

2. **Ajuste de distribución y VaR:** Ajustar distribución t-Student a los retornos de AAPL. Comparar VaR al 95% y 99% con tres metodologías: histórico, paramétrico normal y paramétrico t-Student.

3. **Simulación GBM y bootstrap:** Generar 1000 trayectorias GBM para el S&P 500 a 1 año. Calcular la distribución de precios finales y comparar los percentiles con simulación histórica bootstrap.

4. **Validación de supuestos para un portafolio:** Descargar retornos de 5 activos. Verificar normalidad para cada uno. Si alguno no es normal, comparar la matriz de covarianza muestral con una estimada por bootstrap. ¿Qué impacto tiene en la optimización de portafolio?

---

## 5. Resumen

| Concepto | Ejemplo / Código |
|----------|-----------------|
| Normal fit | `stats.norm.fit(datos)` |
| Log-normal | `lognorm.rvs(s=sigma, scale=np.exp(mu), size=n)` |
| t-Student fit | `stats.t.fit(datos)` devuelve (df, loc, scale) |
| Jarque-Bera | `stats.jarque_bera(datos)` → (stat, p-value) |
| Q-Q Plot | `stats.probplot(datos, dist="norm", plot=ax)` |
| Bootstrap IC | `np.random.choice(datos, size=n, replace=True)` repetido N veces |
| GBM simulación | `S_t * exp((mu - 0.5*σ²)*dt + σ*√dt*Z)` |
| Skewness | `stats.skew(datos)` |
| Kurtosis (exceso) | `stats.kurtosis(datos)` — normal = 0 |
| VaR percentil | `np.percentile(datos, alpha * 100)` |

---

## ✅ Autoevaluación

1. ¿Por qué los retornos financieros NO siguen una distribución normal en la práctica?
2. ¿Qué indican grados de libertad bajos (df < 5) en una distribución t-Student ajustada a retornos?
3. Explica la diferencia entre VaR histórico, VaR paramétrico normal y VaR paramétrico t-Student. ¿Cuál es más conservador y por qué?
4. ¿Qué hace el bootstrap y por qué es útil cuando no conocemos la distribución subyacente?
5. Escribe la ecuación del Movimiento Browniano Geométrico discretizada para simular un paso de precio.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Las tres distribuciones clave: Normal (base teórica), Log-normal (precios), t-Student (retornos reales)
> - Los tests de normalidad y sus diferencias (Jarque-Bera usa skew/kurt, Shapiro-Wilk es más potente en muestras < 50)
> - El código para simular GBM: siempre incluye la corrección de Itô `(mu - 0.5*sigma**2)*dt`
> - El bootstrap es tu herramienta cuando no puedes asumir una distribución paramétrica
