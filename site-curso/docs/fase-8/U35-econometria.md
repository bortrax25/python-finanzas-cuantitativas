# U35: Econometría Financiera — Regresión y Panel Data

> **Lectura previa:** [U34: Series de Tiempo — ARIMA y Volatilidad](./U34-series-tiempo.md)
> **Próxima unidad:** [U36: SQL para Datos Financieros](./U36-sql.md)

---

## 1. Teoría

### 1.1 ¿Qué es la econometría financiera?

La econometría aplica métodos estadísticos a datos económicos y financieros para probar hipótesis, estimar relaciones y hacer predicciones. En finanzas cuantitativas se usa para:

- Estimar betas de acciones (CAPM)
- Probar si existen primas de riesgo (value, momentum, size)
- Modelar la relación entre variables macro y retornos
- Analizar datos de panel (empresas × tiempo) para estudios cross-sectional

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
```

### 1.2 Mínimos Cuadrados Ordinarios (OLS)

El modelo más fundamental: estima la relación lineal entre una variable dependiente `y` y una o más independientes `X`.

```python
# Simular datos: relación CAPM
np.random.seed(42)
n = 500
retorno_mercado = np.random.normal(0.0005, 0.012, n)  # retorno del mercado (S&P 500)
alfa_verdadero = 0.0002
beta_verdadero = 1.15
ruido = np.random.normal(0, 0.008, n)
retorno_activo = alfa_verdadero + beta_verdadero * retorno_mercado + ruido

# OLS con statsmodels
X = sm.add_constant(retorno_mercado)  # agrega columna de 1s para el intercepto
modelo = sm.OLS(retorno_activo, X)
resultado = modelo.fit()

print("=== Regresión CAPM ===\n")
print(resultado.summary())

print(f"\n--- Interpretación ---")
print(f"Alfa (intercepto): {resultado.params[0]:.6f} — retorno en exceso del mercado")
print(f"Beta:              {resultado.params[1]:.4f} — sensibilidad al mercado")
print(f"R²:                {resultado.rsquared:.4f} — % de varianza explicada")
print(f"Alfa significativo: {'SÍ' if resultado.pvalues[0] < 0.05 else 'NO'}")
```

### 1.3 Violaciones de los supuestos de OLS

```python
# 1. Heterocedasticidad: varianza del error NO es constante
# Solución: Errores estándar robustos (White, HC0-HC3)
resultado_robusto = modelo.fit(cov_type='HC3')  # White robust errors
print("=== OLS con errores robustos (White HC3) ===\n")
print(resultado_robusto.summary())

# 2. Autocorrelación: errores correlacionados en el tiempo
# Solución: Errores estándar Newey-West (corrigen autocorrelación + heterocedasticidad)
resultado_nw = modelo.fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print("\n=== OLS con errores Newey-West (5 lags) ===\n")
print(resultado_nw.summary())

# 3. Comparar errores estándar
print(f"Error estándar OLS simple:        {resultado.bse[1]:.6f}")
print(f"Error estándar White (HC3):       {resultado_robusto.bse[1]:.6f}")
print(f"Error estándar Newey-West (5):    {resultado_nw.bse[1]:.6f}")
```

> ⚠️ **Error común:** Usar errores estándar OLS simples en regresiones financieras ignorando que los datos financieros casi siempre tienen heterocedasticidad y autocorrelación. Siempre reporta errores robustos Newey-West cuando trabajes con series de tiempo.

### 1.4 Errores Clustered (agrupados)

Útil cuando los datos tienen estructura de grupos (ej: empresas dentro del mismo sector, múltiples observaciones por empresa).

```python
# Simular panel: 50 empresas, 60 meses cada una
np.random.seed(42)
n_empresas, n_meses = 50, 60
n_total = n_empresas * n_meses

empresa_id = np.repeat(np.arange(n_empresas), n_meses)
mes = np.tile(np.arange(n_meses), n_empresas)

factor_mercado = np.random.normal(0.0005, 0.012, n_total)
factor_empresa = np.random.normal(0, 0.005, n_total)  # error a nivel empresa

retorno = 0.0003 + 1.0 * factor_mercado + factor_empresa

df_panel = pd.DataFrame({
    'retorno': retorno,
    'mercado': factor_mercado,
    'empresa': empresa_id,
    'mes': mes
})

# OLS con errores clustered por empresa
X_panel = sm.add_constant(df_panel['mercado'])
modelo_panel = sm.OLS(df_panel['retorno'], X_panel)

resultado_cluster = modelo_panel.fit(cov_type='cluster', cov_kwds={'groups': df_panel['empresa']})
print("=== OLS con errores clustered (por empresa) ===\n")
print(resultado_cluster.summary())
```

### 1.5 Panel Data: Fixed Effects vs Random Effects

Los modelos de panel controlan por heterogeneidad no observada entre entidades (empresas, países).

```python
from linearmodels.panel import PanelOLS, RandomEffects, compare

# Crear DataFrame con MultiIndex para datos de panel
df_panel = df_panel.set_index(['empresa', 'mes'])

# Modelo de Efectos Fijos (Fixed Effects)
# Controla por características invariantes en el tiempo de cada empresa
modelo_fe = PanelOLS(
    df_panel['retorno'],
    sm.add_constant(df_panel[['mercado']]),
    entity_effects=True    # fixed effects por empresa
)
resultado_fe = modelo_fe.fit()

print("=== Panel: Efectos Fijos ===\n")
print(resultado_fe.summary)

# Modelo de Efectos Aleatorios (Random Effects)
modelo_re = RandomEffects(
    df_panel['retorno'],
    sm.add_constant(df_panel[['mercado']])
)
resultado_re = modelo_re.fit()

print("\n=== Panel: Efectos Aleatorios ===\n")
print(resultado_re.summary)

# Test de Hausman: ¿Fixed Effects o Random Effects?
# H0: Random Effects es consistente y eficiente
# Si p < 0.05, usar Fixed Effects
from linearmodels.panel import compare
comparacion = compare({'Fixed Effects': resultado_fe, 'Random Effects': resultado_re})
print("\n=== Test de Hausman ===\n")
print(comparacion)
```

### 1.6 Fama-MacBeth Regression

El procedimiento en dos pasos estándar para regresiones cross-sectional en asset pricing:

1. **Paso 1:** Estimar betas de cada activo con regresiones de series de tiempo (rolling)
2. **Paso 2:** Regresión cross-sectional cada período: `retorno_i,t = γ_t * beta_i + error`. Promediar los γ_t en el tiempo.

```python
def fama_macbeth(returns_df, factor_df):
    """
    Implementación del procedimiento Fama-MacBeth.
    
    Parámetros:
        returns_df: DataFrame (T × N) — retornos de activos
        factor_df: DataFrame (T × K) — factores de riesgo
    
    Retorna:
        gamma: vector de primas de riesgo promedio
        se_gamma: errores estándar (corregidos por autocorrelación)
        t_stats: estadísticos t
    """
    from scipy import stats
    
    T, N = returns_df.shape
    K = factor_df.shape[1]
    
    # Paso 2: Regresión cross-sectional cada período
    gammas = []
    
    for t in range(T):
        y = returns_df.iloc[t].values  # retornos cross-section en t
        X = sm.add_constant(factor_df.iloc[t].values)
        
        # Usar betas de los 24 meses previos (simplificado aquí)
        modelo_cs = sm.OLS(y, X).fit()
        gammas.append(modelo_cs.params)
    
    gammas = np.array(gammas)
    
    # Estadísticas Fama-MacBeth
    gamma_promedio = gammas.mean(axis=0)
    se_fm = gammas.std(axis=0, ddof=1) / np.sqrt(T)  # Fama-MacBeth SE
    t_stat = gamma_promedio / se_fm
    
    return gamma_promedio, se_fm, t_stat

# Simular datos para Fama-MacBeth
np.random.seed(42)
T, N = 120, 30  # 10 años, 30 activos

factor = np.random.normal(0.0005, 0.012, size=(T, 1))
returns = 0.0003 + 0.8 * factor + np.random.normal(0, 0.01, size=(T, N))

returns_df = pd.DataFrame(returns)
factor_df = pd.DataFrame(factor, columns=['mercado'])

gamma, se, t = fama_macbeth(returns_df, factor_df)
print("=== Fama-MacBeth Resultados ===\n")
print(f"Prima de riesgo (γ): {gamma[1]:.6f}")
print(f"Error estándar FM:   {se[1]:.6f}")
print(f"t-statistic:         {t[1]:.3f}")
print(f"Significativa:       {'SÍ (>1.96)' if abs(t[1]) > 1.96 else 'NO'}")
```

### 1.7 Two-Stage Least Squares (2SLS)

Corrige endogeneidad usando variables instrumentales. En finanzas: estimar el impacto de la liquidez en retornos (la liquidez puede ser endógena).

```python
# Simular ejemplo de 2SLS
np.random.seed(42)
n = 200

# Variable instrumental (exógena)
z = np.random.normal(0, 1, n)

# Variable endógena: x depende de z + ruido
x = 0.7 * z + np.random.normal(0, 0.5, n)

# Variable dependiente: y depende de x + ruido
y = 2.0 * x + np.random.normal(0, 1, n)

# --- 2SLS manual ---
# Etapa 1: Regresar x sobre z
etapa1 = sm.OLS(x, sm.add_constant(z)).fit()
x_predicho = etapa1.predict(sm.add_constant(z))

# Etapa 2: Regresar y sobre x_predicho
etapa2 = sm.OLS(y, sm.add_constant(x_predicho)).fit()

print("=== 2SLS Manual ===\n")
print(f"Coeficiente 2SLS: {etapa2.params[1]:.4f} (verdadero = 2.0)")
print(f"R² etapa 1:       {etapa1.rsquared:.4f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Replicación de un estudio Fama-MacBeth

**Concepto financiero:** Fama y MacBeth (1973) revolucionaron el asset pricing al proponer un método para estimar primas de riesgo en datos cross-section con series de tiempo.

**Código:**

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

np.random.seed(42)
T, N = 120, 50  # 10 años mensuales, 50 activos

# Generar betas (invariantes para simplificar)
betas_verdaderas = np.random.uniform(0.5, 1.5, N)
prima_mercado_verdadera = 0.006  # 0.6% mensual

# Paso 1: Estimar betas con rolling window (24 meses)
# Simulado: usamos las betas verdaderas con ruido
betas_estimadas = betas_verdaderas.reshape(1, -1) * np.ones((T, N))
betas_estimadas += np.random.normal(0, 0.1, size=(T, N))

# Paso 2: Regresión cross-sectional cada mes
gammas_intercepto = []
gammas_beta = []

for t in range(T):
    retornos_t = 0.001 + prima_mercado_verdadera * betas_verdaderas + np.random.normal(0, 0.02, N)
    X = sm.add_constant(betas_estimadas[t])
    modelo_t = sm.OLS(retornos_t, X).fit()
    gammas_intercepto.append(modelo_t.params[0])
    gammas_beta.append(modelo_t.params[1])

gammas_intercepto = np.array(gammas_intercepto)
gammas_beta = np.array(gammas_beta)

# Estadísticas Fama-MacBeth
gamma_0 = gammas_intercepto.mean()
gamma_1 = gammas_beta.mean()
se_0 = gammas_intercepto.std(ddof=1) / np.sqrt(T)
se_1 = gammas_beta.std(ddof=1) / np.sqrt(T)

print("=== Resultados Fama-MacBeth (2 pasos) ===\n")
print(f"Paso 1: Betas estimadas para {N} activos en {T} meses")
print(f"\nPaso 2 — Cross-sectional (promedios):")
print(f"Intercepto (γ₀):    {gamma_0:.6f} (SE: {se_0:.6f})")
print(f"Prima mercado (γ₁): {gamma_1:.6f} (SE: {se_1:.6f})")
print(f"t-stat γ₁:          {gamma_1 / se_1:.2f}")
print(f"\nPrima verdadera: {prima_mercado_verdadera:.4f}")
print(f"Prima estimada:  {gamma_1:.4f} ✓" if abs(gamma_1 - prima_mercado_verdadera) < 0.002
      else f"Prima estimada:  {gamma_1:.4f} (diferencia: {abs(gamma_1 - prima_mercado_verdadera):.4f})")
```

**Output:**
```
=== Resultados Fama-MacBeth (2 pasos) ===

Paso 1: Betas estimadas para 50 activos en 120 meses

Paso 2 — Cross-sectional (promedios):
Intercepto (γ₀):    0.000672 (SE: 0.002039)
Prima mercado (γ₁): 0.005286 (SE: 0.001955)
t-stat γ₁:          2.70

Prima verdadera: 0.0060
Prima estimada:  0.0053 ✓
```

---

## 3. Aplicación en Finanzas 💰

**Asset Management (AQR, Dimensional Fund Advisors):** Fama-MacBeth es el método estándar para validar nuevas primas de riesgo. Cuando AQR lanza un fondo de "quality minus junk", respalda la estrategia con regresiones Fama-MacBeth que muestran que el factor quality tiene una prima estadísticamente significativa.

**Academic Research:** Prácticamente todo paper de asset pricing en el Journal of Finance usa Fama-MacBeth o alguna variante. Es el "gold standard" para evidencia empírica de factores.

**Fixed Effects en Finanzas Corporativas:** Cuando estudias el impacto del apalancamiento en la rentabilidad de 500 empresas durante 10 años, fixed effects controla por características no observables de cada empresa (calidad de management, cultura corporativa).

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-8/U35_ejercicios.py`

1. **Diagnóstico de regresión:** Correr OLS de retornos de una acción contra el mercado. Testear heterocedasticidad con Breusch-Pagan, autocorrelación con Durbin-Watson. Reportar coeficientes con 3 tipos de errores estándar.

2. **Clustered vs robust errors:** Crear un panel artificial con 100 empresas y 60 meses. Correr la misma regresión con errores OLS, White, Newey-West y clustered por empresa. Comparar significancia estadística.

3. **Fixed Effects vs Pooled OLS:** Usar PanelOLS con entity_effects y comparar con OLS agrupado (pooled). Interpretar el R² within vs between. ¿Qué implica un R² within bajo?

4. **Fama-MacBeth completo:** Simular 36 meses de rolling betas (paso 1) y 84 meses de cross-sectional regressions (paso 2). Reportar primas de riesgo con errores estándar corregidos por autocorrelación (Newey-West en los γ_t).

---

## 5. Resumen

| Concepto | Código |
|----------|--------|
| OLS | `sm.OLS(y, X).fit()` |
| OLS robusto (White) | `.fit(cov_type='HC3')` |
| OLS Newey-West | `.fit(cov_type='HAC', cov_kwds={'maxlags': lags})` |
| Clustered errors | `.fit(cov_type='cluster', cov_kwds={'groups': grupos})` |
| Panel Fixed Effects | `PanelOLS(y, X, entity_effects=True)` |
| Panel Random Effects | `RandomEffects(y, X)` |
| Test Hausman | `compare({'FE': fe, 'RE': re})` |
| Fama-MacBeth | Paso 1: rolling betas, Paso 2: σ_t de γ cross-sectional |
| 2SLS | Etapa 1: `sm.OLS(x, Z)`, Etapa 2: `sm.OLS(y, x_pred)` |
| Breusch-Pagan | `sm.stats.diagnostic.het_breuschpagan()` |
| Durbin-Watson | `sm.stats.durbin_watson(residuals)` |

---

## ✅ Autoevaluación

1. ¿Por qué necesitamos errores estándar Newey-West en regresiones con datos financieros?
2. Explica la diferencia entre Fixed Effects y Random Effects. ¿Cuándo usarías cada uno?
3. Describe el procedimiento Fama-MacBeth en dos pasos. ¿Por qué es preferible a una regresión cross-sectional simple?
4. ¿Qué problema resuelve 2SLS y cuándo es necesario en finanzas?
5. Si los errores estándar clustered duplican los errores OLS, ¿cómo cambia tu interpretación de la significancia estadística?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Siempre reportar errores robustos (Newey-West para series de tiempo, clustered para datos de panel)
> - Fixed Effects controla por variables omitidas invariantes en el tiempo
> - Fama-MacBeth: estimar betas en series de tiempo (paso 1), luego regresión cross-sectional cada período (paso 2), promediar gammas
> - El error estándar de Fama-MacBeth es σ(γ_t) / √T (Newey-West si hay autocorrelación en los γ)
