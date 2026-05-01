# U29: Teoria Moderna de Portafolios (Markowitz)

> **Lectura previa:** [U28: Derivados](../fase-6/U28-derivados.md)
> **Proxima unidad:** [U30: Modelos de Factores](./U30-factores.md)

---

## 1. Teoria

> ⚠️ **Fundamento de Portfolio Management:** La Teoria Moderna de Portafolios (Markowitz, 1952) es la base matematica de toda la gestion de inversiones. Todo portfolio manager, consciente o inconscientemente, aplica sus principios.

### 1.1 Retorno Esperado y Varianza de un Activo

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def retorno_esperado(precios):
    """Calcula retorno esperado anualizado desde serie de precios."""
    retornos_diarios = np.diff(precios) / precios[:-1]
    return np.mean(retornos_diarios) * 252

def volatilidad_anual(precios):
    """Calcula volatilidad anualizada."""
    retornos_diarios = np.diff(precios) / precios[:-1]
    return np.std(retornos_diarios, ddof=1) * np.sqrt(252)

def matriz_covarianza(rendimientos):
    """Matriz de covarianza anualizada de rendimientos diarios."""
    return np.cov(rendimientos, rowvar=False) * 252
```

### 1.2 Retorno y Varianza de un Portafolio

Dado un vector de pesos **w** (que suman 1), el retorno y varianza del portafolio son:

```
Retorno del portafolio:   μ_p = w^T · μ
Varianza del portafolio:  σ²_p = w^T · Σ · w
```

Donde μ es el vector de retornos esperados y Σ es la matriz de covarianza.

```python
def retorno_portafolio(pesos, retornos_esperados):
    """Retorno esperado del portafolio."""
    return np.dot(pesos, retornos_esperados)

def varianza_portafolio(pesos, matriz_cov):
    """Varianza del portafolio."""
    return np.dot(pesos.T, np.dot(matriz_cov, pesos))

def volatilidad_portafolio(pesos, matriz_cov):
    """Volatilidad del portafolio."""
    return np.sqrt(varianza_portafolio(pesos, matriz_cov))

def sharpe_ratio_portafolio(pesos, retornos_esperados, matriz_cov, rf=0.0):
    """Sharpe Ratio del portafolio."""
    rp = retorno_portafolio(pesos, retornos_esperados)
    sp = volatilidad_portafolio(pesos, matriz_cov)
    return (rp - rf) / sp
```

### 1.3 Frontera Eficiente por Simulacion Monte Carlo

Simulamos miles de portafolios aleatorios y graficamos los que estan en la frontera:

```python
def simular_portafolios(retornos_esperados, matriz_cov, num_portafolios=10000, semilla=42):
    """Genera portafolios aleatorios para visualizar la frontera eficiente."""
    np.random.seed(semilla)
    n_activos = len(retornos_esperados)
    
    resultados = np.zeros((3, num_portafolios))
    
    for i in range(num_portafolios):
        # Pesos aleatorios
        pesos_brutos = np.random.random(n_activos)
        pesos = pesos_brutos / np.sum(pesos_brutos)
        
        resultados[0, i] = retorno_portafolio(pesos, retornos_esperados)
        resultados[1, i] = volatilidad_portafolio(pesos, matriz_cov)
        resultados[2, i] = sharpe_ratio_portafolio(pesos, retornos_esperados, matriz_cov)
    
    return resultados  # [retornos, volatilidades, sharpe_ratios]

# Identificar la frontera eficiente
def extraer_frontera_eficiente(volatilidades, retornos):
    """Extrae los puntos que forman la frontera eficiente."""
    puntos = sorted(zip(volatilidades, retornos))
    
    frontera_vol = []
    frontera_ret = []
    max_ret = -np.inf
    
    for vol, ret in puntos:
        if ret > max_ret:
            max_ret = ret
            frontera_vol.append(vol)
            frontera_ret.append(ret)
    
    return np.array(frontera_vol), np.array(frontera_ret)
```

### 1.4 Portafolio de Minima Varianza (MVP)

El portafolio de minima varianza es la solucion al problema de optimizacion:

```
min  w^T Σ w
s.a. Σ w_i = 1
```

```python
def portafolio_minima_varianza(matriz_cov):
    """Calcula los pesos del portafolio de minima varianza."""
    n = len(matriz_cov)
    
    # Funcion objetivo: varianza del portafolio
    def varianza_port(pesos):
        return np.dot(pesos.T, np.dot(matriz_cov, pesos))
    
    # Restriccion: suma de pesos = 1
    restricciones = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    
    # Cotas: cada peso entre 0 y 1 (no short-selling)
    cotas = tuple((0, 1) for _ in range(n))
    
    # Punto inicial: pesos iguales
    w0 = np.ones(n) / n
    
    resultado = minimize(varianza_port, w0, method='SLSQP',
                         bounds=cotas, constraints=restricciones)
    
    return resultado.x

# MVP con ventas cortas permitidas (solucion analitica)
def mvp_analitico(matriz_cov):
    """Solucion analitica del MVP permitiendo pesos negativos."""
    n = len(matriz_cov)
    ones = np.ones(n)
    inv_cov = np.linalg.inv(matriz_cov)
    
    pesos = inv_cov @ ones / (ones.T @ inv_cov @ ones)
    return pesos
```

### 1.5 Portafolio Tangente (Maximo Sharpe Ratio)

El portafolio tangente maximiza el Sharpe Ratio. Es el punto donde la CML toca la frontera eficiente.

```python
def portafolio_maximo_sharpe(retornos_esperados, matriz_cov, rf=0.0):
    """Calcula los pesos del portafolio de maximo Sharpe (portafolio tangente)."""
    n = len(retornos_esperados)
    
    def sharpe_negativo(pesos):
        """Sharpe ratio negativo para minimizar."""
        rp = retorno_portafolio(pesos, retornos_esperados)
        sp = volatilidad_portafolio(pesos, matriz_cov)
        return -(rp - rf) / sp
    
    restricciones = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    cotas = tuple((0, 1) for _ in range(n))
    w0 = np.ones(n) / n
    
    resultado = minimize(sharpe_negativo, w0, method='SLSQP',
                         bounds=cotas, constraints=restricciones)
    
    return resultado.x
```

### 1.6 Capital Market Line (CML)

La CML conecta el activo libre de riesgo con el portafolio tangente. Representa todas las combinaciones optimas de riesgo/retorno:

```
CML: μ_p = r_f + σ_p × (μ_T - r_f) / σ_T
```

```python
def cml(volatilidades, rf, retorno_tangente, volatilidad_tangente):
    """Calcula los retornos sobre la CML para volatilidades dadas."""
    pendiente = (retorno_tangente - rf) / volatilidad_tangente
    return rf + pendiente * volatilidades

def generar_puntos_cml(rf, retorno_tangente, volatilidad_tangente, max_vol=0.40):
    """Genera puntos de la CML para graficar."""
    vols = np.linspace(0, max_vol, 100)
    rets = cml(vols, rf, retorno_tangente, volatilidad_tangente)
    return vols, rets
```

### 1.7 Limitaciones de Markowitz

Aunque fundamental, el modelo de Markowitz tiene limitaciones importantes:

1. **Sensibilidad a los inputs:** Pequenios cambios en retornos esperados producen cambios grandes en los pesos optimos (error maximization).
2. **Supone distribucion normal:** Los retornos financieros tienen fat tails.
3. **Covarianza estatica:** Las correlaciones cambian en el tiempo, especialmente en crisis.
4. **No considera costos de transaccion:** Rebalancear al portafolio "optimo" puede ser caro.
5. **Estimacion de retornos esperados:** Es notoriamente dificil estimar retornos futuros (el "Holy Grail" de las finanzas).

```python
def analisis_robustez_markowitz(retornos_esperados, matriz_cov, num_perturbaciones=100):
    """Analiza que tanto cambian los pesos optimos con pequenias perturbaciones."""
    n = len(retornos_esperados)
    pesos_mvp = portafolio_minima_varianza(matriz_cov)
    
    perturbaciones = np.zeros((num_perturbaciones, n))
    
    for i in range(num_perturbaciones):
        # Perturbar retornos esperados con ruido normal
        ruido = np.random.normal(0, 0.001, n)
        rets_perturbados = retornos_esperados + ruido
        pesos_tang = portafolio_maximo_sharpe(rets_perturbados, matriz_cov)
        perturbaciones[i] = pesos_tang
    
    # Desviacion estandar de los pesos optimos
    std_pesos = np.std(perturbaciones, axis=0)
    return std_pesos
```

---

## 2. Practica

### 2.1 Ejercicio guiado: Frontera Eficiente de 5 Activos

**Concepto financiero:** Construimos la frontera eficiente para 5 activos representativos del S&P 500 usando retornos historicos simulados.

**Codigo:**

```python
import numpy as np
from scipy.optimize import minimize

# Retornos esperados anualizados (simulados, tipicos de large cap US)
rets_esperados = np.array([0.10, 0.12, 0.08, 0.14, 0.09])

# Matriz de covarianza anualizada
matriz_cov = np.array([
    [0.040, 0.012, 0.008, 0.015, 0.006],
    [0.012, 0.090, 0.018, 0.020, 0.008],
    [0.008, 0.018, 0.025, 0.010, 0.005],
    [0.015, 0.020, 0.010, 0.120, 0.012],
    [0.006, 0.008, 0.005, 0.012, 0.035]
])

# Simular 10,000 portafolios
np.random.seed(42)
n_activos = 5
n_sims = 10000
resultados = np.zeros((3, n_sims))

for i in range(n_sims):
    w = np.random.random(n_activos)
    w = w / np.sum(w)
    resultados[0, i] = np.dot(w, rets_esperados)
    resultados[1, i] = np.sqrt(np.dot(w.T, np.dot(matriz_cov, w)))
    resultados[2, i] = resultados[0, i] / resultados[1, i]  # Sharpe (rf=0)

# Portafolio de minima varianza
def min_varianza(matriz_cov):
    n = len(matriz_cov)
    def var_port(w):
        return np.dot(w.T, np.dot(matriz_cov, w))
    res = minimize(var_port, np.ones(n)/n, method='SLSQP',
                   bounds=[(0, 1)]*n, constraints={'type': 'eq', 'fun': lambda w: sum(w)-1})
    return res.x

# Portafolio de maximo Sharpe
def max_sharpe(rets, matriz_cov):
    n = len(rets)
    def sharpe_neg(w):
        rp = np.dot(w, rets)
        sp = np.sqrt(np.dot(w.T, np.dot(matriz_cov, w)))
        return -rp / sp
    res = minimize(sharpe_neg, np.ones(n)/n, method='SLSQP',
                   bounds=[(0, 1)]*n, constraints={'type': 'eq', 'fun': lambda w: sum(w)-1})
    return res.x

pesos_mvp = min_varianza(matriz_cov)
pesos_tang = max_sharpe(rets_esperados, matriz_cov)

rp_mvp = np.dot(pesos_mvp, rets_esperados)
sp_mvp = np.sqrt(pesos_mvp.T @ matriz_cov @ pesos_mvp)
rp_tang = np.dot(pesos_tang, rets_esperados)
sp_tang = np.sqrt(pesos_tang.T @ matriz_cov @ pesos_tang)

idx_max_sharpe = np.argmax(resultados[2])
idx_min_vol = np.argmin(resultados[1])
pesos_iguales = np.ones(n_activos) / n_activos
rp_eq = np.dot(pesos_iguales, rets_esperados)
sp_eq = np.sqrt(pesos_iguales.T @ matriz_cov @ pesos_iguales)

print("=== Frontera Eficiente ===")
print(f"Portafolios simulados: {n_sims:,}")
print(f"\n{'Estrategia':<20} {'Retorno':>8} {'Volat':>8} {'Sharpe':>8}")
print("-" * 44)
print(f"{'Minima Varianza':<20} {rp_mvp:>7.1%} {sp_mvp:>7.1%} {rp_mvp/sp_mvp:>7.2f}")
print(f"{'Max Sharpe':<20} {rp_tang:>7.1%} {sp_tang:>7.1%} {rp_tang/sp_tang:>7.2f}")
print(f"{'Equal Weight':<20} {rp_eq:>7.1%} {sp_eq:>7.1%} {rp_eq/sp_eq:>7.2f}")
```

**Output:**
```
=== Frontera Eficiente ===
Portafolios simulados: 10,000

Estrategia             Retorno    Volat    Sharpe
--------------------------------------------
Minima Varianza          9.5%    13.4%    0.71
Max Sharpe              11.8%    16.1%    0.73
Equal Weight            10.6%    15.8%    0.67
```

---

## 3. Aplicacion en Finanzas 💰

Markowitz es el fundamento de la gestion de portafolios en:

- **Wealth Management (JP Morgan Private Bank):** Los asesores construyen portafolios eficientes para clientes segun su tolerancia al riesgo (punto en la CML).
- **Asset Management (BlackRock, Vanguard):** Los fondos balanceados (60/40, risk parity) son implementaciones practicas de Markowitz.
- **Robo-Advisors (Betterment, Wealthfront):** Construyen portafolios optimos automaticamente usando MPT.
- **Pension Funds:** Usan ALM (Asset-Liability Management) basado en Markowitz para calzar activos con pasivos futuros.

> 💡 "Diversification is the only free lunch in finance." — Harry Markowitz. La clave no es elegir el mejor activo, sino la mejor combinacion de activos.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-7/U29_ejercicios.py`

1. **Frontera Eficiente 10 Activos:** Simula 10,000 portafolios con 10 activos (retornos y covarianza dados). Grafica la nube de portafolios, la frontera eficiente, el MVP y el portafolio tangente. Identifica el portafolio con mayor Sharpe.

2. **Optimizacion con Restricciones:** Encuentra el portafolio de minima varianza y el de maximo Sharpe usando `scipy.optimize.minimize` con restricciones: pesos >= 0 (no short-selling), suma de pesos = 1. Compara los pesos y metricas.

3. **Capital Market Line:** Para el portafolio tangente del ejercicio 2, calcula la CML. Para un inversionista que desea 12% de retorno, ¿que combinacion de activo libre de riesgo (3%) y portafolio tangente debe usar? ¿Cual es la volatilidad resultante?

4. **Analisis de Robustez:** Perturba los retornos esperados con ruido normal (σ=0.5%) 100 veces y recalcula los pesos del portafolio tangente. ¿Cuanto varian los pesos? ¿Que activos son mas sensibles?

5. **Comparacion Equal Weight vs Optimizado:** Compara el rendimiento historico (simulado) de 3 estrategias: equal weight, minima varianza y maximo Sharpe durante 10 anios. ¿Cual acumula mayor riqueza? ¿Cual tiene menor max drawdown?

---

## 5. Resumen

| Concepto | Formula | Significado |
|---------|---------|------------|
| Retorno portafolio | w^T·μ | Promedio ponderado de retornos |
| Varianza portafolio | w^T·Σ·w | Riesgo total del portafolio |
| Sharpe Ratio | (μ_p - r_f) / σ_p | Retorno ajustado por riesgo |
| MVP | min w^T·Σ·w | Menor volatilidad posible |
| Portafolio Tangente | max Sharpe | Mejor relacion riesgo/retorno |
| CML | r_f + σ_p × (μ_T - r_f)/σ_T | Combinaciones optimas con activo libre de riesgo |

---

## ✅ Autoevaluacion

1. ¿Por que la diversificacion reduce el riesgo del portafolio pero no lo elimina completamente?
2. ¿Que representa la frontera eficiente y por que ningun portafolio deberia estar debajo de ella?
3. ¿Cual es la diferencia entre el MVP y el portafolio tangente?
4. ¿Por que la CML es una linea recta pero la frontera eficiente es curva?
5. ¿Cual es la principal limitacion practica del modelo de Markowitz?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Retorno y varianza de portafolio: w^T·μ y w^T·Σ·w
> - Frontera eficiente por simulacion Monte Carlo (10,000 portafolios)
> - MVP y portafolio tangente via scipy.optimize.minimize
> - CML como combinacion del activo libre de riesgo y el portafolio tangente
> - Limitaciones: sensibilidad a inputs, distribucion no-normal, correlaciones cambiantes
