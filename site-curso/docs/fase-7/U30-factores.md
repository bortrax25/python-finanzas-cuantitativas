# U30: Modelos de Factores y Asset Pricing

> **Lectura previa:** [U29: Teoria Moderna de Portafolios](./U29-mpt.md)
> **Proxima unidad:** [U31: Gestion de Riesgo](./U31-riesgo.md)

---

## 1. Teoria

> ⚠️ **Quant Core Skill:** Los modelos de factores son el lenguaje universal de la inversion cuantitativa. Todo quant fund descompone los retornos en factores sistematicos para entender fuentes de riesgo y alpha.

### 1.1 CAPM: Capital Asset Pricing Model

El CAPM (Sharpe, 1964) establece que el retorno esperado de un activo depende solo de su exposicion al riesgo de mercado (beta):

```
E[R_i] = R_f + β_i × (E[R_m] - R_f)

Donde:
β_i = Cov(R_i, R_m) / Var(R_m)  (riesgo sistematico)
α_i = R_i - [R_f + β_i × (R_m - R_f)]  (exceso de retorno no explicado)
```

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

def calcular_beta(rendimientos_activo, rendimientos_mercado):
    """Calcula beta usando covarianza."""
    cov = np.cov(rendimientos_activo, rendimientos_mercado)[0, 1]
    var_mercado = np.var(rendimientos_mercado)
    return cov / var_mercado

def capm_expected_return(rf, beta, prima_mercado):
    """Retorno esperado segun CAPM."""
    return rf + beta * prima_mercado

def estimar_capm_regresion(rendimientos_activo, rendimientos_mercado, rf=0.0):
    """Estima CAPM via regresion OLS: (R_i - Rf) = α + β(R_m - Rf) + ε"""
    exceso_activo = rendimientos_activo - rf
    exceso_mercado = rendimientos_mercado - rf
    
    # Agregar constante para el intercepto (alpha)
    X = sm.add_constant(exceso_mercado)
    modelo = sm.OLS(exceso_activo, X).fit()
    
    return {
        'alpha': modelo.params[0],
        'beta': modelo.params[1],
        'alpha_pvalue': modelo.pvalues[0],
        'r2': modelo.rsquared,
        'resumen': modelo.summary()
    }

# Ejemplo con datos simulados
np.random.seed(42)
n_dias = 252
rm = np.random.normal(0.0008, 0.012, n_dias)  # Mercado: 8 bps diario, 19% vol
eps = np.random.normal(0, 0.015, n_dias)        # Idiosincratico
rf_diario = 0.00016  # ~4% anual

ri = rf_diario + 1.2 * (rm - rf_diario) + eps  # Activo con β=1.2

resultados_capm = estimar_capm_regresion(ri, rm, rf_diario)
print(f"Beta estimado: {resultados_capm['beta']:.3f}")
print(f"Alpha (anualizado): {resultados_capm['alpha'] * 252:.4%}")
print(f"R²: {resultados_capm['r2']:.3f}")
```

### 1.2 Security Market Line (SML)

La SML grafica el CAPM: retorno esperado vs beta. Los activos sobre la SML tienen alpha positivo (estan subvalorados); los que estan debajo tienen alpha negativo.

```python
def calcular_sml(rf, betas, prima_mercado):
    """Calcula retornos esperados sobre la SML para betas dados."""
    return rf + betas * prima_mercado

def clasificar_activos_por_alpha(retornos_activos, retorno_mercado, rf):
    """Calcula alpha para multiples activos y clasifica."""
    n_activos = retornos_activos.shape[1]
    resultados = []
    
    for i in range(n_activos):
        ri = retornos_activos[:, i]
        capm_result = estimar_capm_regresion(ri, retorno_mercado, rf)
        resultados.append({
            'activo': i,
            'alpha': capm_result['alpha'] * 252,
            'beta': capm_result['beta'],
            'alpha_significativo': capm_result['alpha_pvalue'] < 0.05
        })
    
    return pd.DataFrame(resultados)
```

> 💡 Un alpha positivo y estadisticamente significativo (p-value < 0.05) sugiere que el activo genera retornos superiores a los predichos por su beta — algo que en teoria no deberia existir en un mercado eficiente.

### 1.3 Fama-French 3-Factor Model

Fama y French (1993) demostraron que ademas del mercado, dos factores adicionales explican los retornos:

```
R_i - R_f = α + β_m × (R_m - R_f) + β_smb × SMB + β_hml × HML + ε

SMB (Small Minus Big): Empresas pequenias tienden a superar a las grandes
HML (High Minus Low): Empresas "value" (alto B/M) superan a "growth" (bajo B/M)
```

```python
def fama_french_3_regresion(rendimientos_activo, rendimientos_mercado, 
                             smb, hml, rf=0.0):
    """Estima el modelo de 3 factores de Fama-French."""
    exceso_activo = rendimientos_activo - rf
    exceso_mercado = rendimientos_mercado - rf
    
    # Construir matriz de factores
    X = np.column_stack([exceso_mercado, smb, hml])
    X = sm.add_constant(X)
    
    modelo = sm.OLS(exceso_activo, X).fit()
    
    return {
        'alpha': modelo.params[0],
        'beta_mkt': modelo.params[1],
        'beta_smb': modelo.params[2],
        'beta_hml': modelo.params[3],
        'r2': modelo.rsquared,
        'pvalues': modelo.pvalues
    }

# Datos simulados de factores
n_dias = 252
rm_exceso = np.random.normal(0.0006, 0.012, n_dias)  # Mercado en exceso
smb_factor = np.random.normal(0.0002, 0.008, n_dias)  # Small minus big
hml_factor = np.random.normal(0.0001, 0.007, n_dias)  # High minus low

# Simular retorno de un small-cap value
ri_exc = 0.0001 + 0.9 * rm_exceso + 0.6 * smb_factor + 0.4 * hml_factor
ri_exc += np.random.normal(0, 0.012, n_dias)

resultados_ff3 = fama_french_3_regresion(ri_exc + rf_diario, rm_exceso + rf_diario,
                                          smb_factor, hml_factor, rf_diario)
print(f"FF3 Alpha (anual): {resultados_ff3['alpha'] * 252:.4%}")
print(f"β_mkt: {resultados_ff3['beta_mkt']:.3f}")
print(f"β_smb: {resultados_ff3['beta_smb']:.3f}")
print(f"β_hml: {resultados_ff3['beta_hml']:.3f}")
print(f"R²: {resultados_ff3['r2']:.3f}")
```

### 1.4 Fama-French 5-Factor Model

En 2015, Fama y French agregaron dos factores mas:

```
R_i - R_f = α + β_m×(R_m-R_f) + β_smb×SMB + β_hml×HML + β_rmw×RMW + β_cma×CMA + ε

RMW (Robust Minus Weak): Empresas rentables superan a las no rentables
CMA (Conservative Minus Aggressive): Empresas que invierten conservadoramente superan
```

```python
def fama_french_5_regresion(rendimientos_activo, rendimientos_mercado,
                             smb, hml, rmw, cma, rf=0.0):
    """Estima Fama-French 5-factor via OLS."""
    exceso_activo = rendimientos_activo - rf
    exceso_mercado = rendimientos_mercado - rf
    
    X = np.column_stack([exceso_mercado, smb, hml, rmw, cma])
    X = sm.add_constant(X)
    
    modelo = sm.OLS(exceso_activo, X).fit()
    
    return {
        'alpha': modelo.params[0],
        'betas': {
            'mkt': modelo.params[1],
            'smb': modelo.params[2],
            'hml': modelo.params[3],
            'rmw': modelo.params[4],
            'cma': modelo.params[5]
        },
        'r2': modelo.rsquared,
        'pvalues_alpha': modelo.pvalues[0]
    }
```

### 1.5 Performance Attribution

El analisis de atribucion descompone el retorno de un portafolio en sus fuentes:

```python
def performance_attribution(retorno_portafolio, betas, retornos_factores):
    """Descompone el retorno en contribucion de factores y alpha.
    
    Retorno = alpha + Σ (beta_k × factor_k)
    """
    # Contribucion de cada factor
    contribuciones = {}
    for factor, beta in betas.items():
        contribuciones[factor] = beta * retornos_factores[factor]
    
    # Alpha = retorno total - suma de contribuciones
    contribucion_total = sum(contribuciones.values())
    alpha = retorno_portafolio - contribucion_total
    
    return alpha, contribuciones

def reporte_atribucion(alpha, contribuciones):
    """Genera reporte de performance attribution."""
    print("=== Performance Attribution ===")
    print(f"Alpha: {alpha:+.4%}")
    for factor, contrib in contribuciones.items():
        print(f"{factor}: {contrib:+.4%}")
    total = alpha + sum(contribuciones.values())
    print(f"Retorno Total: {total:.4%}")
```

### 1.6 Modelo Black-Litterman

Black-Litterman (1992) combina los retornos de equilibrio del mercado (CAPM) con las "views" subjetivas del inversionista para generar retornos esperados mas robustos:

```python
def black_litterman_returns(market_caps, matriz_cov, delta, views_Q, views_P, 
                             confianza_views=None, tau=0.025):
    """Calcula retornos esperados de Black-Litterman.
    
    Parametros:
        market_caps: capitalizaciones de mercado (para pesos de equilibrio)
        matriz_cov: matriz de covarianza de retornos (Σ)
        delta: coeficiente de aversion al riesgo (≈ Sharpe del mercado)
        views_Q: vector de views (ej: [0.05] = "Activo A supera al B por 5%")
        views_P: matriz de views (cada fila = una view, suma 0)
        confianza_views: matriz diagonal de confianza en las views (Ω)
        tau: parametro de escala (usualmente ~0.025)
    """
    n_activos = len(market_caps)
    
    # Pesos de equilibrio (market cap weight)
    pesos_eq = market_caps / np.sum(market_caps)
    
    # Retornos de equilibrio (implied returns from CAPM reverse optimization)
    pi = delta * matriz_cov @ pesos_eq
    
    # Si no se especifica confianza, usar formula estandar
    if confianza_views is None:
        omega = np.diag(np.diag(tau * views_P @ matriz_cov @ views_P.T))
    else:
        omega = confianza_views
    
    # Formula de Black-Litterman
    tau_sigma = tau * matriz_cov
    M = np.linalg.inv(np.linalg.inv(tau_sigma) + views_P.T @ np.linalg.inv(omega) @ views_P)
    retornos_bl = M @ (np.linalg.inv(tau_sigma) @ pi + views_P.T @ np.linalg.inv(omega) @ views_Q)
    
    return retornos_bl

# Ejemplo: 3 activos, 2 views
market_caps_ej = np.array([500, 300, 200])  # En miles de millones
matriz_cov_ej = np.array([
    [0.04, 0.01, 0.005],
    [0.01, 0.06, 0.008],
    [0.005, 0.008, 0.03]
])

# View 1: Activo 0 superara al Activo 1 por 3%
# View 2: Activo 2 tendra retorno absoluto de 8%
views_P_ej = np.array([
    [1, -1, 0],    # View relativa
    [0, 0, 1]      # View absoluta
])
views_Q_ej = np.array([0.03, 0.08])

rets_bl = black_litterman_returns(market_caps_ej, matriz_cov_ej, delta=2.5,
                                   views_Q=views_Q_ej, views_P=views_P_ej)

print("Retornos Black-Litterman:")
for i, ret in enumerate(rets_bl):
    print(f"  Activo {i}: {ret:.2%}")
```

> 💡 Black-Litterman resuelve el principal problema de Markowitz: en lugar de estimar retornos esperados directamente (lo cual es casi imposible), parte de los retornos de equilibrio y los ajusta con opiniones informadas.

---

## 2. Practica

### 2.1 Ejercicio guiado: Regresion Fama-French Completa

**Concepto financiero:** Analizamos el perfil de riesgo de 5 acciones usando el modelo de 3 factores.

**Codigo:**

```python
import numpy as np
import statsmodels.api as sm
import pandas as pd

# Simular 252 dias de retornos para 5 activos y factores
np.random.seed(123)
n_dias = 252
n_activos = 5

# Factores
rf_daily = 0.00016
mkt_exc = np.random.normal(0.0006, 0.012, n_dias)
smb = np.random.normal(0.0002, 0.008, n_dias)
hml = np.random.normal(0.0001, 0.007, n_dias)

# Betas verdaderos de cada activo (diferentes perfiles)
betas_reales = {
    'Large Growth':  [1.1, -0.2, -0.3],
    'Large Value':   [0.9, -0.1,  0.5],
    'Small Growth':  [1.2,  0.7, -0.2],
    'Small Value':   [1.0,  0.8,  0.6],
    'Market Neutral':[0.0,  0.1,  0.1]
}

activos = {}
retornos_activos = np.zeros((n_dias, n_activos))

for j, (nombre, betas) in enumerate(betas_reales.items()):
    ret = rf_daily + betas[0] * mkt_exc + betas[1] * smb + betas[2] * hml
    ret += np.random.normal(0, 0.01, n_dias)
    retornos_activos[:, j] = ret

# Estimar FF3 para cada activo
print("=== Fama-French 3-Factor Analysis ===\n")
print(f"{'Activo':<18} {'Alpha':>8} {'β_mkt':>7} {'β_smb':>7} {'β_hml':>7} {'R²':>7}")
print("-" * 58)

resultados = []
for j in range(n_activos):
    ff3 = fama_french_3_regresion(retornos_activos[:, j], 
                                    mkt_exc + rf_daily, smb, hml, rf_daily)
    nombre = list(betas_reales.keys())[j]
    alpha_anual = ff3['alpha'] * 252
    print(f"{nombre:<18} {alpha_anual:>7.2%} {ff3['beta_mkt']:>6.2f} "
          f"{ff3['beta_smb']:>6.2f} {ff3['beta_hml']:>6.2f} {ff3['r2']:>6.2f}")
    resultados.append(ff3)

# Identificar activos con alpha significativo
print(f"\nAlphas significativos (p < 0.05):")
for j, ff3 in enumerate(resultados):
    if ff3['pvalues'][0] < 0.05:
        print(f"  {list(betas_reales.keys())[j]}: alpha anual = {ff3['alpha'] * 252:.2%}")
```

**Output:**
```
=== Fama-French 3-Factor Analysis ===

Activo               Alpha   β_mkt   β_smb   β_hml     R²
----------------------------------------------------------
Large Growth         0.18%   1.11   -0.22   -0.31   0.75
Large Value          0.82%   0.92   -0.11    0.49   0.68
Small Growth        -0.05%   1.20    0.72   -0.21   0.79
Small Value          1.21%   0.97    0.82    0.58   0.82
Market Neutral       0.34%   0.02    0.09    0.13   0.04

Alphas significativos (p < 0.05):
  Small Value: alpha anual = 1.21%
```

---

## 3. Aplicacion en Finanzas 💰

Los modelos de factores se usan en:

- **Hedge Funds Quant (Citadel, AQR, Two Sigma):** Todo se modela como factores. Las estrategias son "long factores con alpha positivo, short factores con alpha negativo."
- **Risk Management:** Los risk managers descomponen el riesgo del portafolio en riesgo de factores (sistematico) vs riesgo idiosincratico.
- **Performance Attribution:** ¿El PM genero alpha o simplemente tuvo suerte con el factor momentum?
- **Smart Beta ETFs:** Productos como iShares Value ETF (IVE) o Small-Cap ETF (IJR) son implementaciones pasivas de factores.

> 💡 En una entrevista de quant en Citadel: "Descompon el retorno de este portafolio en Fama-French 5 factores e identificame donde esta el alpha real."

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-7/U30_ejercicios.py`

1. **CAPM para 20 Acciones:** Estima beta y alpha (con p-values) de 20 acciones contra el S&P 500. Datos simulados con diferentes betas (0.5 a 1.8) y alphas (algunos estadisticamente significativos). Identifica cuales generan alpha real.

2. **Fama-French 3-Factor:** Para las mismas 20 acciones, estima el modelo FF3 y compara los R² con el CAPM. ¿Cuanto mejora el poder explicativo al agregar SMB y HML?

3. **Clasificacion por Factores:** Las 20 acciones tienen diferentes cargas factoriales. Clasificalas como Large/Small y Growth/Value segun sus betas a SMB y HML. ¿Concuerda la clasificacion con los nombres?

4. **Performance Attribution:** Tienes un portafolio con pesos conocidos. Calcula los betas del portafolio a los 5 factores FF. Descompone el retorno del ultimo mes en contribuciones de cada factor + alpha.

5. **Black-Litterman con Views:** Implementa el modelo Black-Litterman para 5 activos. Define 3 views: (1) Activo A supera a B por 2%, (2) Activo C tendra retorno 10%, (3) Activos D y E superaran al mercado por 1%. Compara los retornos BL con los retornos de equilibrio CAPM.

---

## 5. Resumen

| Modelo | Factores | Formula |
|--------|---------|---------|
| CAPM | 1 (mercado) | E[R] = Rf + β(Rm - Rf) |
| FF 3-Factor | Mercado + Size + Value | + β_smb×SMB + β_hml×HML |
| FF 5-Factor | + Profitability + Investment | + β_rmw×RMW + β_cma×CMA |
| Black-Litterman | Equilibrium + Views | BL = f(Π, P, Q, Ω) |

---

## ✅ Autoevaluacion

1. ¿Que mide el alpha de Jensen y que significa si es estadisticamente significativo?
2. ¿Por que el CAPM tiene bajo poder explicativo (R² bajo) para acciones individuales?
3. ¿Que interpretacion le darias a un beta de SMB = 0.8 en una accion?
4. ¿Cual es la diferencia entre los factores RMW y HML en FF5?
5. ¿Por que Black-Litterman produce retornos esperados mas "razonables" que Markowitz puro?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - CAPM: regresion OLS para estimar alpha y beta, test de significancia
> - Fama-French 3 y 5 factores: que mide cada factor
> - R² como medida de poder explicativo del modelo
> - Performance attribution: descomposicion retorno = alpha + Σ(beta_k × factor_k)
> - Black-Litterman como solucion al problema de estimacion de retornos esperados
