# U17: Cálculos Financieros Fundamentales

> **Lectura previa:** [U16: NumPy y Pandas](./U16-numpy-pandas.md)
> **Próxima unidad:** [U18: Valoración de bonos](./U18-valoracion-bonos.md)

## 1. Valor del dinero en el tiempo

```python
import numpy as np

# Valor Futuro
def valor_futuro(vp, tasa, periodos):
    return vp * (1 + tasa) ** periodos

# Valor Presente
def valor_presente(vf, tasa, periodos):
    return vf / (1 + tasa) ** periodos

# Valor Presente Neto (VPN/NPV)
def vpn(inversion, tasa, flujos):
    return np.sum([f / (1 + tasa)**t for t, f in enumerate(flujos, 1)]) - inversion

# Tasa Interna de Retorno (TIR/IRR) — por iteración
def tir(flujos, tolerancia=0.0001):
    """flujos[0] debe ser la inversión (negativo)."""
    r_min, r_max = -0.99, 1.0
    while r_max - r_min > tolerancia:
        r = (r_min + r_max) / 2
        npv = sum(f / (1 + r)**t for t, f in enumerate(flujos))
        if npv > 0:
            r_min = r
        else:
            r_max = r
    return (r_min + r_max) / 2
```

## 2. Rentabilidad y riesgo

```python
# Rentabilidad simple y logarítmica
def rentabilidad_simple(pi, pf):
    return (pf - pi) / pi

def rentabilidad_log(pi, pf):
    return np.log(pf / pi)

# Volatilidad anualizada
def volatilidad_anual(rendimientos_diarios):
    return np.std(rendimientos_diarios, ddof=1) * np.sqrt(252)

# Sharpe Ratio
def sharpe(rendimiento_anual, tasa_libre, volatilidad_anual):
    return (rendimiento_anual - tasa_libre) / volatilidad_anual

# Maximum Drawdown
def max_drawdown(precios):
    pico = np.maximum.accumulate(precios)
    drawdown = (pico - precios) / pico
    return np.max(drawdown) * 100
```

## 3. Análisis de regresión simple

```python
# Beta de una acción vs mercado (mínimos cuadrados simples)
def calcular_beta(rendimientos_accion, rendimientos_mercado):
    cov = np.cov(rendimientos_accion, rendimientos_mercado)[0, 1]
    var_mercado = np.var(rendimientos_mercado)
    return cov / var_mercado

# Alpha de Jensen
def alpha_jensen(rend_accion, rend_mercado, beta, rf):
    return rend_accion - (rf + beta * (rend_mercado - rf))
```

## 4. Ejercicios Propuestos

1. Implementa una función que calcule todas las métricas de un activo a partir de su serie de precios.
2. Calcula la frontera eficiente para 2 activos con diferentes correlaciones.
3. Implementa el modelo de Black-Scholes para valoración de opciones europeas.
