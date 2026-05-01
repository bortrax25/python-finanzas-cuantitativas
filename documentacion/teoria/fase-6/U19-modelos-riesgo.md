# U19: Modelos de Riesgo (VaR, Monte Carlo)

> **Lectura previa:** [U18: Valoración de bonos](./U18-valoracion-bonos.md)
> **Próxima unidad:** [U20: Proyecto final](./U20-proyecto-final.md)

## 1. Value at Risk (VaR)

El **VaR** estima la máxima pérdida esperada en un horizonte dado con un nivel de confianza.

### 1.1 VaR Histórico

```python
import numpy as np

def var_historico(rendimientos, confianza=95):
    """VaR por método histórico."""
    return np.percentile(rendimientos, 100 - confianza)

# Ejemplo: 252 días de rendimientos diarios
rets = np.random.randn(252) * 0.02  # Simulados
var_95 = var_historico(rets, 95)
print(f"VaR 95% histórico: {var_95:.4%}")
```

### 1.2 VaR Paramétrico (varianza-covarianza)

```python
from scipy import stats

def var_parametrico(rendimientos, confianza=95):
    """VaR asumiendo distribución normal."""
    mu = np.mean(rendimientos)
    sigma = np.std(rendimientos, ddof=1)
    z = stats.norm.ppf(1 - confianza / 100)
    return mu + z * sigma  # z es negativo

var_95p = var_parametrico(rets, 95)
print(f"VaR 95% paramétrico: {var_95p:.4%}")
```

### 1.3 VaR de Portafolio

```python
def var_portafolio(pesos, rendimientos_activos, confianza=95):
    """VaR paramétrico para un portafolio."""
    mu = np.dot(pesos, rendimientos_activos.mean(axis=0))
    cov = np.cov(rendimientos_activos.T)
    var_port = np.dot(pesos.T, np.dot(cov, pesos))
    sigma = np.sqrt(var_port)
    z = stats.norm.ppf(1 - confianza / 100)
    return mu + z * sigma

# 3 activos, 252 días
rets_3 = np.random.randn(252, 3) * np.array([0.02, 0.015, 0.025])
pesos = np.array([0.4, 0.35, 0.25])
print(f"VaR portafolio 95%: {var_portafolio(pesos, rets_3):.4%}")
```

## 2. Simulación Monte Carlo

### 2.1 Movimiento Browniano Geométrico

```python
def simular_gbm(s0, mu, sigma, T, pasos=252, n_sims=1000):
    """Simula precios con Movimiento Browniano Geométrico."""
    dt = T / pasos
    precios = np.zeros((pasos + 1, n_sims))
    precios[0] = s0
    for t in range(1, pasos + 1):
        z = np.random.randn(n_sims)
        precios[t] = precios[t-1] * np.exp((mu - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*z)
    return precios

# Simular 1 año de precios, 1000 escenarios
sims = simular_gbm(100, 0.08, 0.20, 1.0, 252, 1000)
precio_final = sims[-1]
print(f"Precio esperado: ${np.mean(precio_final):.2f}")
print(f"VaR 95% Monte Carlo: ${np.percentile(precio_final, 5):.2f}")
```

### 2.2 Monte Carlo para opciones

```python
def precio_call_europea_mc(s0, k, r, sigma, T, n_sims=100000):
    """Precio de call europea por Monte Carlo."""
    z = np.random.randn(n_sims)
    st = s0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*z)
    payoff = np.maximum(st - k, 0)
    return np.exp(-r * T) * np.mean(payoff)

precio_call = precio_call_europea_mc(100, 105, 0.04, 0.20, 1.0)
print(f"Call europea (MC): ${precio_call:.2f}")
```

## 3. Backtesting de VaR

```python
def backtest_var(rendimientos, var, confianza=95):
    """Cuenta violaciones del VaR."""
    violaciones = (rendimientos < var).sum()
    total = len(rendimientos)
    pct = violaciones / total * 100
    esperado = (100 - confianza)
    print(f"Violaciones: {violaciones}/{total} ({pct:.2f}%)")
    print(f"Esperado: {esperado}%")
```

## 4. Ejercicios Propuestos

1. Implementa CVaR (Expected Shortfall) — promedio de pérdidas que exceden el VaR.
2. Simula 10,000 escenarios de portafolio con 3 activos correlacionados.
3. Calcula VaR por los tres métodos (histórico, paramétrico, Monte Carlo) y compara.
