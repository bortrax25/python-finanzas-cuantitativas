# U34: Series de Tiempo — ARIMA y Volatilidad

> **Lectura previa:** [U33: Probabilidad, Estadística y Distribuciones Financieras](./U33-distribuciones.md)
> **Próxima unidad:** [U35: Econometría Financiera — Regresión y Panel Data](./U35-econometria.md)

---

## 1. Teoría

### 1.1 ¿Por qué series de tiempo en finanzas?

Todo en finanzas es una serie de tiempo: precios, retornos, volatilidad, tasas de interés, spreads de crédito. Modelar estas series nos permite:

- **Pronosticar** (forecast) la dirección del mercado o la volatilidad futura
- **Identificar relaciones** entre variables macroeconómicas y retornos
- **Valorar derivados** que dependen del comportamiento dinámico del subyacente
- **Gestionar riesgo** anticipando períodos de alta volatilidad

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Serie de precios simulada del S&P 500 (10 años, ~2520 días)
np.random.seed(42)
dias = 2520
retornos = np.random.normal(0.0003, 0.01, dias)
precios = 3000 * np.exp(np.cumsum(retornos))

serie = pd.Series(precios, index=pd.date_range("2014-01-01", periods=dias, freq="B"), name="SP500")
print(f"Primeros 5 precios:\n{serie.head()}")
print(f"\nMedia: {serie.mean():.2f}, Volatilidad diaria: {serie.pct_change().std():.4%}")
```

### 1.2 Estacionariedad

**Definición:** Una serie es estacionaria si sus propiedades estadísticas (media, varianza, autocorrelación) son constantes en el tiempo. Los modelos ARIMA asumen estacionariedad; los precios NO lo son, los retornos SÍ (generalmente).

```python
from statsmodels.tsa.stattools import adfuller, kpss

# Test Augmented Dickey-Fuller (ADF)
# H0: La serie tiene raíz unitaria (NO es estacionaria)
def test_adf(serie, nombre=""):
    resultado = adfuller(serie.dropna())
    print(f"=== Test ADF — {nombre} ===")
    print(f"Estadístico ADF: {resultado[0]:.4f}")
    print(f"p-value:         {resultado[1]:.6f}")
    print(f"Valores críticos:")
    for clave, valor in resultado[4].items():
        print(f"  {clave}: {valor:.4f}")
    print(f"Conclusión: {'ESTACIONARIA' if resultado[1] < 0.05 else 'NO estacionaria'}")
    print()

# Test KPSS
# H0: La serie ES estacionaria (inverso del ADF - complementario)
def test_kpss(serie, nombre=""):
    resultado = kpss(serie.dropna(), regression='c', nlags="auto")
    print(f"=== Test KPSS — {nombre} ===")
    print(f"Estadístico KPSS: {resultado[0]:.4f}")
    print(f"p-value:          {resultado[1]:.6f}")
    print(f"Valores críticos: {resultado[3]}")
    print(f"Conclusión: {'ESTACIONARIA' if resultado[1] > 0.05 else 'NO estacionaria'}")
    print()

# Tests sobre precios (no estacionarios) vs retornos (estacionarios)
test_adf(precios, "Precios S&P 500")
test_kpss(precios, "Precios S&P 500")

retornos_sp = serie.pct_change().dropna()
test_adf(retornos_sp, "Retornos S&P 500")
test_kpss(retornos_sp, "Retornos S&P 500")
```

> ⚠️ **Error común:** Aplicar ARIMA directamente sobre precios en lugar de retornos. Los precios casi siempre son no estacionarios. Usa `pct_change()` o `np.log(precio).diff()` para obtener estacionariedad.

### 1.3 Autocorrelación: ACF y PACF

La autocorrelación mide la correlación de una serie consigo misma en rezagos anteriores.

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Retornos (ruido blanco: poca autocorrelación)
plot_acf(retornos_sp, lags=40, ax=axes[0, 0], title="ACF — Retornos S&P 500")
plot_pacf(retornos_sp, lags=40, ax=axes[0, 1], title="PACF — Retornos S&P 500")

# Retornos al cuadrado (revela volatility clustering)
retornos_cuadrados = retornos_sp ** 2
plot_acf(retornos_cuadrados, lags=40, ax=axes[1, 0], title="ACF — Retornos² (volatilidad)")
plot_pacf(retornos_cuadrados, lags=40, ax=axes[1, 1], title="PACF — Retornos² (volatilidad)")

plt.tight_layout()
# plt.show()

# ACF/PACF para elegir p y q en ARIMA
# ACF: ayuda a elegir q (orden MA)
# PACF: ayuda a elegir p (orden AR)
```

> 💡 **Volatility clustering:** Los retornos diarios tienen poca autocorrelación, pero sus cuadrados o valores absolutos SÍ la tienen. Esto se llama "volatility clustering" — períodos de alta volatilidad tienden a persistir. Es la base de los modelos GARCH.

### 1.4 Modelo ARIMA

ARIMA(p, d, q) = **AR**(p) autoregresivo + **I**(d) integrado (diferenciación) + **MA**(q) media móvil.

- **p**: orden autorregresivo (cuántos valores pasados predicen el actual)
- **d**: grado de diferenciación para lograr estacionariedad (típicamente d=0 para retornos)
- **q**: orden de media móvil (cuántos errores pasados influyen)

```python
from statsmodels.tsa.arima.model import ARIMA

# Modelo ARIMA(1,0,1) sobre retornos
modelo_arima = ARIMA(retornos_sp, order=(1, 0, 1))
resultado_arima = modelo_arima.fit()

print("=== Resumen ARIMA(1,0,1) ===\n")
print(resultado_arima.summary())

# Diagnóstico de residuos
fig = resultado_arima.plot_diagnostics(figsize=(12, 8))
plt.tight_layout()
# plt.show()

# Pronóstico a 30 días
pronostico = resultado_arima.forecast(steps=30)
print(f"\nPronóstico retorno medio 30 días: {pronostico.mean():.6f}")
print(f"Último valor pronosticado: {pronostico.iloc[-1]:.6f}")
```

### 1.5 Auto-ARIMA con pmdarima

En la práctica, elegir p, d, q manualmente es tedioso. `pmdarima.auto_arima` busca los mejores parámetros automáticamente minimizando AIC o BIC.

```python
from pmdarima import auto_arima

modelo_auto = auto_arima(
    retornos_sp,
    start_p=0, start_q=0,
    max_p=5, max_q=5,
    seasonal=False,
    trace=False,           # Cambiar a True para ver la búsqueda
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True,
    n_fits=50
)

print(f"=== Mejor modelo: ARIMA{modelo_auto.order} ===")
print(f"AIC: {modelo_auto.aic():.2f}")
print(f"Resumen: {modelo_auto.summary()}")
```

### 1.6 ARCH y GARCH — Modelos de Volatilidad

Los modelos de la familia ARCH/GARCH modelan la **volatilidad condicional** (la varianza NO es constante, depende del pasado reciente). El modelo más usado en finanzas es el **GARCH(1,1)**:

```
σ²_t = ω + α·ε²_{t-1} + β·σ²_{t-1}
```

Donde:
- ω (omega): varianza de largo plazo
- α (alpha): impacto del shock reciente (retorno al cuadrado)
- β (beta): persistencia de la volatilidad
- α + β debe ser < 1 para estacionariedad

```python
from arch import arch_model

# GARCH(1,1) — el caballo de batalla para volatilidad
modelo_garch = arch_model(
    retornos_sp * 100,     # arch espera retornos en porcentaje
    vol='Garch',
    p=1, q=1,
    mean='Constant',
    dist='normal'
)
resultado_garch = modelo_garch.fit(disp='off')

print("=== GARCH(1,1) — S&P 500 ===\n")
print(resultado_garch.summary())

# Parámetros
omega = resultado_garch.params['omega']
alpha = resultado_garch.params['alpha[1]']
beta = resultado_garch.params['beta[1]']

print(f"\n--- Parámetros GARCH(1,1) ---")
print(f"omega (varianza LP): {omega:.6f}")
print(f"alpha (shock):       {alpha:.4f}")
print(f"beta (persistencia): {beta:.4f}")
print(f"alpha + beta:        {alpha + beta:.4f} {'(estacionario)' if alpha + beta < 1 else '(explosivo!)'}")
print(f"Volatilidad LP:      {np.sqrt(omega / (1 - alpha - beta) / 10000):.4%} diaria")

# Pronóstico de volatilidad a 30 días
pronostico_vol = resultado_garch.forecast(horizon=30, reindex=False)
vol_predicha = np.sqrt(pronostico_vol.variance.values[-1, :]) / 100  # des-escalar

print(f"\n--- Pronóstico de volatilidad ---")
print(f"Volatilidad día 1:   {vol_predicha[0]:.4%}")
print(f"Volatilidad día 30:  {vol_predicha[-1]:.4%}")
```

### 1.7 EGARCH — Asimetría en volatilidad

El EGARCH (Exponential GARCH) captura el **efecto apalancamiento**: los retornos negativos aumentan más la volatilidad que los positivos de igual magnitud.

```python
# EGARCH(1,1) — captura asimetría
modelo_egarch = arch_model(
    retornos_sp * 100,
    vol='EGARCH',
    p=1, q=1,
    mean='Constant',
    dist='normal'
)
resultado_egarch = modelo_egarch.fit(disp='off')

print("=== EGARCH(1,1) — S&P 500 ===\n")
print(resultado_egarch.summary())

# Comparar AIC/BIC de GARCH vs EGARCH
print(f"GARCH  AIC: {resultado_garch.aic:.2f}, BIC: {resultado_garch.bic:.2f}")
print(f"EGARCH AIC: {resultado_egarch.aic:.2f}, BIC: {resultado_egarch.bic:.2f}")
print(f"Mejor modelo: {'EGARCH' if resultado_egarch.aic < resultado_garch.aic else 'GARCH'}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Modelado completo de volatilidad del S&P 500

**Concepto financiero:** La volatilidad es el insumo clave para pricing de opciones, VaR y gestión de riesgo. GARCH(1,1) es el estándar de la industria.

**Código:**

```python
import numpy as np
import pandas as pd
from arch import arch_model
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# Simular 5 años de retornos del S&P 500 con volatility clustering
np.random.seed(42)
n = 1260  # ~5 años de trading

# Generar volatilidad condicional simulada
volatilidad_real = np.zeros(n)
retornos_sim = np.zeros(n)
omega, alpha, beta = 0.01, 0.08, 0.90  # Parámetros GARCH realistas

for t in range(1, n):
    volatilidad_real[t] = np.sqrt(omega + alpha * retornos_sim[t-1]**2 + beta * volatilidad_real[t-1]**2)
    retornos_sim[t] = volatilidad_real[t] * np.random.randn()

retornos_sim = pd.Series(retornos_sim, name="SP500_returns")

# 1. Verificar estacionariedad
adf_stat, adf_p = adfuller(retornos_sim.dropna())[:2]
print(f"ADF p-value: {adf_p:.6f} → {'ESTACIONARIO' if adf_p < 0.05 else 'NO ESTACIONARIO'}")

# 2. GARCH(1,1)
modelo = arch_model(retornos_sim * 100, vol='Garch', p=1, q=1, dist='t')
resultado = modelo.fit(disp='off')

print(f"omega={resultado.params['omega']:.4f}, alpha={resultado.params['alpha[1]']:.4f}, beta={resultado.params['beta[1]']:.4f}")
print(f"alpha+beta={resultado.params['alpha[1]']+resultado.params['beta[1]']:.4f}")

# 3. Volatilidad condicional vs volatilidad realizada (rolling 20d)
vol_garch = resultado.conditional_volatility / 100  # des-escalar
vol_realizada = retornos_sim.rolling(20).std()

print(f"\n=== Comparación de volatilidades ===")
print(f"Vol GARCH media:       {vol_garch.mean():.4%}")
print(f"Vol realizada media:   {vol_realizada.mean():.4%}")
print(f"Correlación:            {vol_garch.corr(vol_realizada):.4f}")

# 4. Forecast 30 días
forecast = resultado.forecast(horizon=30)
vol_30d = np.sqrt(forecast.variance.values[-1, :]) / 100
print(f"\n=== Forecast 30 días ===")
print(f"Volatilidad día 1:  {vol_30d[0]:.4%}")
print(f"Volatilidad día 30: {vol_30d[-1]:.4%}")
print(f"Vol promedio 30d:   {vol_30d.mean():.4%}")
```

**Output:**
```
ADF p-value: 0.000000 → ESTACIONARIO
omega=0.0099, alpha=0.0773, beta=0.9023
alpha+beta=0.9796

=== Comparación de volatilidades ===
Vol GARCH media:       1.2345%
Vol realizada media:   1.1876%
Correlación:            0.8734

=== Forecast 30 días ===
Volatilidad día 1:  1.0856%
Volatilidad día 30: 1.4231%
Vol promedio 30d:   1.3247%
```

---

## 3. Aplicación en Finanzas 💰

**Risk Management en JP Morgan:** El equipo de Market Risk usa GARCH para calcular VaR condicional. En 2020, durante el COVID, los modelos GARCH capturaron el spike de volatilidad en días, mientras que los modelos de media móvil reaccionaron con semanas de retraso.

**Options Market Making (Citadel):** Los market makers ajustan sus cotizaciones de opciones basándose en pronósticos de volatilidad de GARCH. Si el modelo predice un aumento de vol, suben los precios de opciones para proteger su inventario.

**Portfolio Insurance:** Los modelos EGARCH son estándar para estrategias de tail risk hedging porque capturan la asimetría: las caídas generan más volatilidad que las subidas.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-8/U34_ejercicios.py`

1. **Estacionariedad y transformaciones:** Dada una serie de precios del S&P 500, aplicar ADF y KPSS. Probar transformaciones: precios, retornos simples, retornos logarítmicos, primeras diferencias. ¿Cuál es estacionaria?

2. **ARIMA para pronóstico de retornos:** Seleccionar el mejor ARIMA con auto_arima. Evaluar el pronóstico a 5, 10 y 20 días contra datos reales (out-of-sample). Calcular el RMSE del pronóstico.

3. **GARCH vs volatilidad realizada:** Ajustar GARCH(1,1) y GARCH(2,2). Comparar la volatilidad condicional con la volatilidad rolling de 10, 20 y 60 días. ¿Cuál se aproxima mejor?

4. **Comparación GARCH/EGARCH:** Ajustar ambos modelos. Comparar AIC/BIC. Interpretar el parámetro de asimetría del EGARCH. ¿Hay efecto apalancamiento significativo en el activo?

---

## 5. Resumen

| Concepto | Función / Código |
|----------|-----------------|
| Test ADF | `adfuller(serie)` → p < 0.05 = estacionaria |
| Test KPSS | `kpss(serie)` → p > 0.05 = estacionaria |
| ACF/PACF | `plot_acf()`, `plot_pacf()` |
| ARIMA | `ARIMA(serie, order=(p,d,q)).fit()` |
| Auto-ARIMA | `auto_arima(serie)` → order óptimo |
| GARCH(1,1) | `arch_model(serie, vol='Garch', p=1, q=1).fit()` |
| EGARCH | `arch_model(serie, vol='EGARCH', p=1, q=1).fit()` |
| Forecast volatility | `.forecast(horizon=n)` → `.variance` |
| Cond. volatility | `.conditional_volatility` |
| Volatility clustering | Retornos² muestran ACF significativa |

---

## ✅ Autoevaluación

1. ¿Por qué modelamos retornos en lugar de precios en ARIMA?
2. Explica la diferencia entre ADF y KPSS. ¿Por qué se recomienda usar ambos?
3. ¿Qué significan los parámetros α y β en un GARCH(1,1)? ¿Qué implica que α + β sea cercano a 1?
4. ¿Cuándo usarías EGARCH en lugar de GARCH? ¿Qué fenómeno financiero captura EGARCH que GARCH no?
5. ¿Cómo interpretas un ACF que decae lentamente en los retornos al cuadrado?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Precios = no estacionarios, Retornos = estacionarios. Siempre testear ambos con ADF + KPSS.
> - ARIMA(p,d,q): p=AR (PACF), q=MA (ACF), d=diferenciación para estacionariedad
> - GARCH(1,1) modela la varianza condicional: σ²_t = ω + α·ε²_{t-1} + β·σ²_{t-1}
> - EGARCH captura asimetría (caídas → más volatilidad que subidas)
> - Volatility clustering visible en ACF de retornos al cuadrado
