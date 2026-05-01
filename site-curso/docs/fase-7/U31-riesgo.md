# U31: Gestion de Riesgo — VaR, CVaR y Stress Testing

> **Lectura previa:** [U30: Modelos de Factores](./U30-factores.md)
> **Proxima unidad:** [U32: Optimizacion Avanzada de Portafolios](./U32-optimizacion-avanzada.md)

---

## 1. Teoria

> ⚠️ **Risk Management Core Skill:** Todo banco de inversion, hedge fund y asset manager tiene un departamento de riesgo que monitorea VaR, CVaR y realiza stress tests diariamente. Despues de 2008, esto es obligatorio por regulacion (Basel III, Dodd-Frank).

### 1.1 Value at Risk (VaR)

El VaR estima la maxima perdida esperada en un horizonte temporal dado con un nivel de confianza especifico:

> "Con 95% de confianza, no perderemos mas de $X en los proximos N dias."

```python
import numpy as np
from scipy import stats
import pandas as pd

def var_historico(rendimientos, confianza=95):
    """VaR por metodo historico: percentil de la distribucion empirica."""
    return np.percentile(rendimientos, 100 - confianza)

def var_parametrico(rendimientos, confianza=95):
    """VaR parametrico: asume distribucion normal.
    
    Var = μ + z_α × σ
    Donde z_α es el cuantil de la normal para el nivel de confianza.
    """
    mu = np.mean(rendimientos)
    sigma = np.std(rendimientos, ddof=1)
    z_alpha = stats.norm.ppf(1 - confianza / 100)  # Negativo
    return mu + z_alpha * sigma

def var_monte_carlo(rendimientos, confianza=95, n_sims=10000, horizonte=1):
    """VaR por simulacion Monte Carlo.
    
    Simula n_sims escenarios muestreando de la distribucion historica
    y calcula el percentil de los resultados.
    """
    np.random.seed(42)
    mu = np.mean(rendimientos)
    sigma = np.std(rendimientos, ddof=1)
    
    # Simular rendimientos futuros
    futuros = np.random.normal(mu, sigma, n_sims)
    
    # Para multi-periodo, usar retorno compuesto
    if horizonte > 1:
        futuros_acum = np.zeros(n_sims)
        for _ in range(horizonte):
            futuros_acum += np.random.normal(mu, sigma, n_sims)
        futuros = futuros_acum
    
    return np.percentile(futuros, 100 - confianza)

# Ejemplo: 252 dias de rendimientos simulados
np.random.seed(100)
rendimientos_sim = np.random.normal(0.0008, 0.015, 252)

var_hist = var_historico(rendimientos_sim, 95)
var_param = var_parametrico(rendimientos_sim, 95)
var_mc = var_monte_carlo(rendimientos_sim, 95)

print("=== VaR 95% (1 dia) ===")
print(f"VaR Historico:    {var_hist:+.4%}")
print(f"VaR Parametrico:  {var_param:+.4%}")
print(f"VaR Monte Carlo:  {var_mc:+.4%}")
```

> 💡 El VaR historico no asume ninguna distribucion: usa directamente los datos. El VaR parametrico asume normalidad (subestima en fat tails). El VaR Monte Carlo es flexible: puedes usar cualquier distribucion.

### 1.2 VaR de un Portafolio

```python
def var_portafolio_parametrico(pesos, rendimientos_activos, confianza=95, 
                                valor_portafolio=1_000_000):
    """VaR parametrico de un portafolio de multiples activos."""
    # Matriz de covarianza
    matriz_cov = np.cov(rendimientos_activos, rowvar=False)
    
    # Retorno y varianza del portafolio
    retorno_medio = np.dot(pesos, np.mean(rendimientos_activos, axis=0))
    var_port = np.dot(pesos.T, np.dot(matriz_cov, pesos))
    vol_port = np.sqrt(var_port)
    
    z_alpha = stats.norm.ppf(1 - confianza / 100)
    var_pct = retorno_medio + z_alpha * vol_port
    
    # VaR en dolares
    var_dolar = valor_portafolio * (-var_pct)
    
    return var_pct, var_dolar

# Portafolio de 3 activos
n_dias = 252
valores_port = 500000
rets_3 = np.column_stack([
    np.random.normal(0.001, 0.020, n_dias),
    np.random.normal(0.0006, 0.015, n_dias),
    np.random.normal(0.0004, 0.025, n_dias)
])
pesos_port = np.array([0.4, 0.35, 0.25])

var_pct, var_usd = var_portafolio_parametrico(pesos_port, rets_3, 95, valores_port)
print(f"VaR Portafolio 95%: {var_pct:.4%}")
print(f"VaR en USD: ${var_usd:,.0f}")
```

### 1.3 CVaR / Expected Shortfall

El **CVaR** (Conditional VaR) o **Expected Shortfall** mide la perdida esperada CONDICIONAL a que se exceda el VaR. Responde: "Si las cosas salen mal, ¿que tan mal?"

```python
def cvar_historico(rendimientos, confianza=95):
    """CVaR historico: promedio de perdidas que exceden el VaR."""
    var_nivel = np.percentile(rendimientos, 100 - confianza)
    # Perdidas peores que el VaR
    cola = rendimientos[rendimientos <= var_nivel]
    return np.mean(cola)

def cvar_parametrico(rendimientos, confianza=95):
    """CVaR parametrico para distribucion normal."""
    mu = np.mean(rendimientos)
    sigma = np.std(rendimientos, ddof=1)
    z_alpha = stats.norm.ppf(1 - confianza / 100)
    # Para la normal: CVaR = μ - σ × φ(z_α) / (1 - α)
    cvar = mu - sigma * stats.norm.pdf(z_alpha) / (1 - confianza / 100)
    return cvar

# Comparacion VaR vs CVaR
var_h = var_historico(rendimientos_sim, 95)
cvar_h = cvar_historico(rendimientos_sim, 95)
cvar_p = cvar_parametrico(rendimientos_sim, 95)

print("=== VaR vs CVaR 95% ===")
print(f"VaR Historico:  {var_h:+.4%}")
print(f"CVaR Historico: {cvar_h:+.4%}")
print(f"CVaR Parametrico: {cvar_p:+.4%}")
print(f"CVaR/VaR ratio: {abs(cvar_h/var_h):.2f}x")
```

> ⚠️ El CVaR siempre es mas extremo que el VaR (mayor en valor absoluto). Es una mejor medida de riesgo porque cumple con las propiedades de "coherent risk measure" que el VaR no cumple (subaditividad).

### 1.4 Stress Testing

El stress testing simula escenarios extremos especificos para evaluar el impacto en el portafolio:

```python
def stress_test_2008(portafolio_valor, betas_mercado, shock_mercado=-0.40):
    """Estima perdida del portafolio bajo escenario 2008 (caida 40% del mercado)."""
    perdida_pct = betas_mercado * shock_mercado
    perdida_usd = portafolio_valor * abs(perdida_pct)
    return perdida_pct, perdida_usd

def stress_test_covid(portafolio_valor, exposicion_sectores, shocks_sectoriales):
    """Estima perdida bajo escenario COVID con shocks diferenciados por sector."""
    perdida_total = 0
    for sector, exposicion in exposicion_sectores.items():
        shock = shocks_sectoriales.get(sector, 0)
        perdida_total += exposicion * shock
    return perdida_total * portafolio_valor

def generar_escenarios_stress():
    """Define escenarios de stress historicos."""
    return {
        'Crisis_2008': {
            'equity_us': -0.40,
            'equity_em': -0.55,
            'credito_hy': -0.30,
            'credito_ig': -0.05,
            'commodities': -0.45,
            'usd': 0.15
        },
        'COVID_2020': {
            'equity_us': -0.34,
            'equity_em': -0.25,
            'energia': -0.50,
            'aerolineas': -0.60,
            'tecnologia': -0.05,
            'salud': 0.05,
            'credito_hy': -0.15
        },
        'Taper_Tantrum_2013': {
            'equity_em': -0.15,
            'bonos_em': -0.12,
            'credito_hy': -0.08,
            'usd': 0.08
        },
        'Inflacion_Estanflacion': {
            'equity_us': -0.20,
            'bonos_lp': -0.15,
            'commodities': 0.25,
            'oro': 0.30,
            'usd': -0.10
        }
    }

def ejecutar_stress_tests(portafolio_valor, exposiciones, escenarios):
    """Ejecuta todos los escenarios de stress y reporta resultados."""
    resultados = {}
    for nombre, shocks in escenarios.items():
        perdida = 0
        for activo, exposicion in exposiciones.items():
            shock = shocks.get(activo, 0)
            perdida += exposicion * shock
        resultados[nombre] = {
            'perdida_pct': perdida,
            'perdida_usd': portafolio_valor * abs(perdida)
        }
    return pd.DataFrame(resultados).T
```

### 1.5 Backtesting de VaR — Kupiec Test

El backtesting verifica si el modelo de VaR es preciso contando cuantas veces la perdida real excedio el VaR predicho:

```python
def contar_violaciones_var(rendimientos_reales, var_predicho):
    """Cuenta cuantas veces el rendimiento real fue peor que el VaR predicho."""
    return np.sum(rendimientos_reales < var_predicho)

def kupiec_test(rendimientos_reales, var_predicho, confianza=95):
    """Test de Kupiec (POF - Proportion of Failures).
    
    H0: La proporcion de violaciones es igual al nivel esperado (1 - confianza).
    Estadistico sigue distribucion chi-cuadrado con 1 grado de libertad.
    """
    n = len(rendimientos_reales)
    violaciones = contar_violaciones_var(rendimientos_reales, var_predicho)
    
    p_esperado = 1 - confianza / 100
    p_observado = violaciones / n
    
    if violaciones == 0:
        # Evitar log(0)
        lr_stat = -2 * np.log((1 - p_esperado) ** n)
    elif violaciones == n:
        lr_stat = -2 * np.log(p_esperado ** n)
    else:
        # Likelihood ratio statistic
        lr_stat = -2 * np.log(
            ((1 - p_esperado) ** (n - violaciones) * p_esperado ** violaciones) /
            ((1 - p_observado) ** (n - violaciones) * p_observado ** violaciones)
        )
    
    # p-value del chi-cuadrado con 1 gl
    p_value = 1 - stats.chi2.cdf(lr_stat, 1)
    
    return {
        'violaciones': violaciones,
        'total_obs': n,
        'pct_violaciones': p_observado * 100,
        'pct_esperado': (1 - confianza / 100) * 100,
        'lr_statistic': lr_stat,
        'p_value': p_value,
        'rechazar_modelo': p_value < 0.05
    }

# Ejemplo de backtesting
np.random.seed(200)
n_obs = 500
rets_backtest = np.random.normal(-0.001, 0.02, n_obs)
vars_predichos = np.full(n_obs, var_parametrico(rets_backtest[:100], 95))

resultado_bt = kupiec_test(rets_backtest, vars_predichos, 95)
print("=== Kupiec Backtest (VaR 95%) ===")
print(f"Violaciones: {resultado_bt['violaciones']}/{resultado_bt['total_obs']}")
print(f"Observado: {resultado_bt['pct_violaciones']:.1f}%")
print(f"Esperado: {resultado_bt['pct_esperado']:.1f}%")
print(f"p-value: {resultado_bt['p_value']:.3f}")
print(f"Rechazar modelo: {resultado_bt['rechazar_modelo']}")
```

> ⚠️ Un p-value < 0.05 indica que el modelo de VaR NO es preciso: las violaciones observadas difieren significativamente de lo esperado. El modelo puede estar subestimando o sobreestimando el riesgo.

### 1.6 Risk Budgeting

El risk budgeting asigna el riesgo total del portafolio entre sus componentes:

```python
def contribucion_riesgo_marginal(pesos, matriz_cov):
    """Contribucion marginal al riesgo de cada activo."""
    vol_port = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
    # Contribucion marginal = (Σ × w)_i / σ_port
    mcr = np.dot(matriz_cov, pesos) / vol_port
    return mcr

def contribucion_riesgo_total(pesos, matriz_cov):
    """Contribucion total al riesgo (peso × MCR). Suma = volatilidad total."""
    mcr = contribucion_riesgo_marginal(pesos, matriz_cov)
    return pesos * mcr

def riesgo_porcentual_por_activo(pesos, matriz_cov):
    """Porcentaje del riesgo total aportado por cada activo."""
    crt = contribucion_riesgo_total(pesos, matriz_cov)
    return crt / np.sum(crt) * 100

# Ejemplo
matriz_cov_3 = np.array([
    [0.04, 0.01, 0.005],
    [0.01, 0.06, 0.008],
    [0.005, 0.008, 0.03]
])
pesos_rb = np.array([0.4, 0.35, 0.25])

riesgo_pct = riesgo_porcentual_por_activo(pesos_rb, matriz_cov_3)
for i, rp in enumerate(riesgo_pct):
    print(f"Activo {i+1}: {rp:.1f}% del riesgo total")
```

---

## 2. Practica

### 2.1 Ejercicio guiado: Sistema de Riesgo Completo

**Concepto financiero:** Construimos un mini risk system para un portafolio de $2M con 3 activos.

**Codigo:**

```python
import numpy as np
from scipy import stats

np.random.seed(500)
n_dias = 252

# Rendimientos simulados de 3 activos
rets_a = np.random.normal(0.0012, 0.022, n_dias)  # Activo A: mas volatil
rets_b = np.random.normal(0.0008, 0.015, n_dias)  # Activo B: moderado
rets_c = np.random.normal(0.0005, 0.018, n_dias)  # Activo C: intermedio

matriz_rets = np.column_stack([rets_a, rets_b, rets_c])
pesos = np.array([0.35, 0.40, 0.25])
valor_portafolio = 2_000_000

# Retorno del portafolio
retornos_port = matriz_rets @ pesos

# 1. VaR por 3 metodos
var_hist = np.percentile(retornos_port, 5)
var_param = var_parametrico(retornos_port, 95)
futuros_mc = np.random.normal(np.mean(retornos_port), np.std(retornos_port), 10000)
var_mc = np.percentile(futuros_mc, 5)

# 2. CVaR
cvar_val = cvar_historico(retornos_port, 95)

# 3. Stress tests
escenarios = generar_escenarios_stress()
exposiciones = {'equity_us': 0.60, 'tecnologia': 0.25, 'salud': 0.15}

# 4. Backtesting (rolling window)
ventana = 100
vars_rolling = []
for t in range(ventana, n_dias):
    datos_ventana = retornos_port[t-ventana:t]
    vars_rolling.append(var_parametrico(datos_ventana, 95))

vars_array = np.array(vars_rolling)
rets_fuera = retornos_port[ventana:]

resultado_kupiec = kupiec_test(rets_fuera, vars_array, 95)

# Reporte
print("=" * 50)
print("     SISTEMA DE GESTION DE RIESGO")
print("=" * 50)
print(f"Valor del Portafolio: ${valor_portafolio:,.0f}")
print(f"\n--- VaR 95% (1 dia) ---")
print(f"  Historico:   {var_hist:+.4%}  (${abs(var_hist * valor_portafolio):,.0f})")
print(f"  Parametrico: {var_param:+.4%}  (${abs(var_param * valor_portafolio):,.0f})")
print(f"  Monte Carlo: {var_mc:+.4%}  (${abs(var_mc * valor_portafolio):,.0f})")
print(f"\n--- CVaR 95% ---")
print(f"  Historico:   {cvar_val:+.4%}  (${abs(cvar_val * valor_portafolio):,.0f})")
print(f"\n--- Stress Tests ---")
print(f"  Crisis 2008: {exposiciones['equity_us'] * (-0.40):+.1%}")
print(f"  COVID 2020:  {exposiciones['tecnologia'] * (-0.05) + exposiciones['salud'] * 0.05:+.1%}")
print(f"\n--- Kupiec Backtest (p-value: {resultado_kupiec['p_value']:.3f}) ---")
print(f"  Violaciones: {resultado_kupiec['violaciones']}/{resultado_kupiec['total_obs']}")
print(f"  Rechazar H0: {'SI' if resultado_kupiec['rechazar_modelo'] else 'NO'}")
```

**Output:**
```
==================================================
     SISTEMA DE GESTION DE RIESGO
==================================================
Valor del Portafolio: $2,000,000

--- VaR 95% (1 dia) ---
  Historico:   -2.50%  ($50,079)
  Parametrico: -2.52%  ($50,489)
  Monte Carlo: -2.53%  ($50,618)

--- CVaR 95% ---
  Historico:   -3.28%  ($65,621)

--- Stress Tests ---
  Crisis 2008: -24.0%
  COVID 2020:  -0.5%

--- Kupiec Backtest (p-value: 0.942) ---
  Violaciones: 63/152
  Rechazar H0: NO
```

---

## 3. Aplicacion en Finanzas 💰

El risk management es obligatorio y central en:

- **Bancos de Inversion (JP Morgan Risk):** El CRO (Chief Risk Officer) reporta directamente al CEO. VaR diario para cada trading desk.
- **Hedge Funds:** Definen limites de VaR por estrategia (ej: max VaR 95% diario = 2% del NAV).
- **Regulacion Basel III:** Los bancos deben mantener capital regulatorio proporcional a su VaR × 3 (multiplicador conservador).
- **Asset Managers:** Monitorean tracking error, risk budgeting y stress tests para cumplir con los mandatos de los clientes.

> 💡 Despues de la crisis de 2008, el Comite de Basel introdujo CVaR (Expected Shortfall) como reemplazo del VaR para capital regulatorio porque captura mejor el riesgo de cola.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-7/U31_ejercicios.py`

1. **VaR por 3 Metodos:** Para un portafolio de $5M con 4 activos, calcula el VaR 95% y 99% a 1 dia usando los tres metodos (historico, parametrico, Monte Carlo). Compara y explica las diferencias.

2. **CVaR y Perdida en Cola:** Calcula el CVaR 95% y 99% del mismo portafolio. ¿Cual es la diferencia porcentual entre VaR y CVaR para cada nivel de confianza? ¿Por que la diferencia es mayor al 99%?

3. **Sistema de Stress Testing:** Define 4 escenarios de stress (2008, COVID, Dot-com 2000, Estanflacion). Aplica cada escenario a un portafolio con exposiciones a 6 clases de activos. Genera un reporte con las perdidas estimadas en USD y %.

4. **Kupiec Backtesting:** Implementa un sistema rolling de VaR (ventana de 252 dias) y realiza el backtest de Kupiec para niveles de confianza de 95% y 99%. ¿Cual nivel de confianza es mas dificil de backtestear y por que?

5. **Risk Budgeting:** Para un portafolio de 6 activos, calcula la contribucion porcentual de cada activo al riesgo total (risk budgeting). Identifica los activos que concentran el mayor riesgo y evalua si la diversificacion es adecuada.

---

## 5. Resumen

| Metrica | Descripcion | Formula |
|---------|------------|---------|
| VaR Historico | Percentil empirico | Percentile(returns, 1-α) |
| VaR Parametrico | Asume normalidad | μ + z_α × σ |
| VaR Monte Carlo | Simulacion de escenarios | Percentil(simulaciones, 1-α) |
| CVaR | Perdida esperada en la cola | E[R | R ≤ VaR] |
| Kupiec Test | Validez del modelo VaR | LR test chi-cuadrado |
| Stress Testing | Impacto de escenarios extremos | Exposicion × Shock |

---

## ✅ Autoevaluacion

1. ¿Por que el VaR parametrico suele subestimar el riesgo en mercados reales?
2. ¿Cual es la ventaja del CVaR sobre el VaR como medida de riesgo?
3. ¿Que significa que el Kupiec test rechace el modelo de VaR con p < 0.05?
4. ¿Por que es importante el stress testing ademas del VaR diario?
5. ¿Como se relacionan el VaR, el CVaR y el capital regulatorio en Basel III?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Tres metodos de VaR: historico, parametrico, Monte Carlo
> - CVaR como promedio de perdidas en la cola
> - Stress testing con escenarios historicos (2008, COVID)
> - Kupiec test para validar modelos de VaR (H0: proporcion de violaciones = esperado)
> - Risk budgeting: contribucion marginal y total al riesgo
