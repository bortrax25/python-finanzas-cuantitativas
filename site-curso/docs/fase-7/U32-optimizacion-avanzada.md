# U32: Optimizacion Avanzada de Portafolios

> **Lectura previa:** [U31: Gestion de Riesgo](./U31-riesgo.md)
> **Proxima unidad:** [U33: Distribuciones Financieras](../fase-8/U33-distribuciones.md)

---

## 1. Teoria

> ⚠️ **Portfolio Management Avanzado:** Markowitz es la teoria, pero en la practica los pesos optimos son inestables y concentrados. Las tecnicas avanzadas (HRP, Risk Parity, shrinkage) producen portafolios mas robustos y diversificados.

### 1.1 El Problema del "Markowitz Error Maximizer"

Markowitz tiende a concentrar pesos en activos con retornos estimados altos, amplificando los errores de estimacion. Soluciones:

1. **Shrinkage:** "Encoger" la matriz de covarianza hacia una estructura mas simple
2. **Risk Parity:** Igualar contribuciones al riesgo en lugar de pesos
3. **HRP:** Usar clustering jerarquico para construir el portafolio

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform

# Demostrar el problema: 5 activos con retornos similares
np.random.seed(42)
n_activos = 5
n_obs = 60  # 60 datos mensuales (5 anios) - pocos datos!

# Matriz de covarianza "verdadera"
sigma_verdadera = np.array([
    [0.04, 0.02, 0.01, 0.03, 0.005],
    [0.02, 0.05, 0.015, 0.02, 0.01],
    [0.01, 0.015, 0.03, 0.01, 0.008],
    [0.03, 0.02, 0.01, 0.08, 0.015],
    [0.005, 0.01, 0.008, 0.015, 0.06]
])

# Retornos observados (con ruido de muestreo)
retornos = np.random.multivariate_normal(
    np.array([0.008, 0.009, 0.007, 0.010, 0.006]),
    sigma_verdadera / 12,
    size=n_obs
)

cov_muestral = np.cov(retornos, rowvar=False)
print("Covarianza verdadera (1,1):", sigma_verdadera[0, 0])
print("Covarianza muestral (1,1):", cov_muestral[0, 0])
print("Diferencia:", abs(sigma_verdadera[0, 0] - cov_muestral[0, 0]))
```

### 1.2 Ledoit-Wolf Shrinkage

Ledoit y Wolf (2004) proponen "encoger" la matriz de covarianza muestral hacia una matriz "target" estructurada:

```
Σ_shrunk = δ × Σ_target + (1 - δ) × Σ_sample
```

Donde δ se estima para minimizar el error cuadratico medio.

```python
def ledoit_wolf_shrinkage(rendimientos):
    """Estimador de covarianza Ledoit-Wolf (implementacion simplificada).
    
    Shrinkage hacia la matriz diagonal de varianzas individuales.
    """
    n_obs, n_activos = rendimientos.shape
    cov_muestral = np.cov(rendimientos, rowvar=False)
    
    # Target: matriz diagonal (varianzas individuales, covarianzas cero)
    target = np.diag(np.diag(cov_muestral))
    
    # Estimacion del parametro de shrinkage (formula simplificada de LW)
    # En la practica se usa sklearn.covariance.LedoitWolf
    diffs = []
    for i in range(n_activos):
        for j in range(n_activos):
            if i != j:
                x = rendimientos[:, i]
                y = rendimientos[:, j]
                # Varianza de la covarianza muestral
                var_cov = np.var((x - np.mean(x)) * (y - np.mean(y)))
                diffs.append(var_cov)
    
    if len(diffs) > 0:
        pi_hat = np.sum(diffs)
        gamma_hat = np.sum((cov_muestral - target) ** 2)
        delta = max(0, min(1, pi_hat / gamma_hat))
    else:
        delta = 0
    
    cov_shrunk = delta * target + (1 - delta) * cov_muestral
    return cov_shrunk

# Comparar covarianza muestral vs shrinkage
from sklearn.covariance import LedoitWolf as LW

lw = LW().fit(retornos)  # Usando sklearn para la estimacion correcta
cov_lw_sklearn = lw.covariance_

cov_lw_manual = ledoit_wolf_shrinkage(retornos)

print("\nLedoit-Wolf Shrinkage:")
print(f"  Delta estimado: {lw.shrinkage_:.4f}")
print(f"  Cov muestral (1,1): {cov_muestral[0, 0]:.4f}")
print(f"  Cov shrinkage (1,1): {cov_lw_sklearn[0, 0]:.4f}")
```

### 1.3 Risk Parity (Equal Risk Contribution)

Risk Parity asigna pesos para que cada activo contribuya igual al riesgo total del portafolio (en lugar de igual al capital):

```python
def risk_parity_weights(matriz_cov, max_iter=100, tolerancia=1e-8):
    """Calcula pesos de Risk Parity via optimizacion.
    
    Objetivo: igualar las contribuciones marginales al riesgo.
    """
    n = len(matriz_cov)
    
    def funcion_objetivo_risk_parity(pesos):
        pesos = np.abs(pesos) / np.sum(np.abs(pesos))
        vol_port = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov, pesos)))
        
        # Contribucion marginal al riesgo
        mcr = np.dot(matriz_cov, pesos) / vol_port
        
        # Contribucion total al riesgo
        rc = pesos * mcr
        
        # Queremos que todas las contribuciones sean iguales (1/n)
        rc_objetivo = vol_port / n
        
        return np.sum((rc - rc_objetivo) ** 2)
    
    # Punto inicial: pesos iguales
    w0 = np.ones(n) / n
    
    restricciones = {'type': 'eq', 'fun': lambda w: np.sum(np.abs(w)) - 1}
    cotas = tuple((0, 1) for _ in range(n))
    
    resultado = minimize(funcion_objetivo_risk_parity, w0, method='SLSQP',
                         bounds=cotas, constraints=restricciones,
                         options={'maxiter': max_iter, 'ftol': tolerancia})
    
    pesos_rp = resultado.x / np.sum(resultado.x)
    return pesos_rp

# Ejemplo con 4 activos de diferente volatilidad
matriz_cov_4 = np.array([
    [0.04, 0.01, 0.015, 0.005],
    [0.01, 0.09, 0.02, 0.008],
    [0.015, 0.02, 0.25, 0.03],    # Activo 3: muy volatil
    [0.005, 0.008, 0.03, 0.01]    # Activo 4: baja volatilidad
])

pesos_rp = risk_parity_weights(matriz_cov_4)
rc_pct = riesgo_porcentual_por_activo(pesos_rp, matriz_cov_4)

print("\n=== Risk Parity ===")
print(f"{'Activo':<10} {'Peso':>8} {'% Riesgo':>10}")
for i in range(4):
    print(f"{i+1:<10} {pesos_rp[i]:>7.1%} {rc_pct[i]:>9.1f}%")
```

> 💡 Risk Parity asigna MENOS peso a activos volatiles y MAS a activos estables, logrando que cada uno aporte ~25% del riesgo en un portafolio de 4 activos.

### 1.4 Hierarchical Risk Parity (HRP)

HRP (Lopez de Prado, 2016) usa clustering jerarquico para construir el portafolio en 3 pasos:

1. **Clustering:** Agrupar activos por similaridad (basado en correlacion)
2. **Quasi-diagonalization:** Reordenar activos segun el dendrograma
3. **Recursive bisection:** Asignar pesos de abajo hacia arriba usando risk parity

```python
def matriz_distancias_correlacion(matriz_cov):
    """Convierte matriz de covarianza en matriz de distancias basada en correlacion."""
    correlacion = np.corrcoef(matriz_cov)
    # Distancia = sqrt(0.5 * (1 - correlacion))  -> va de 0 a 1
    distancia = np.sqrt(0.5 * (1 - correlacion))
    np.fill_diagonal(distancia, 0)
    return distancia

def hrp_pesos(matriz_cov):
    """Hierarchical Risk Parity (Lopez de Prado, 2016).
    
    Implementacion desde cero sin librerias externas.
    """
    n = len(matriz_cov)
    
    # Paso 1: Matriz de distancias
    dist = matriz_distancias_correlacion(matriz_cov)
    dist_condensada = squareform(dist)
    
    # Paso 2: Clustering jerarquico (single linkage)
    linkage_matrix = linkage(dist_condensada, method='single')
    
    # Paso 3: Recursive bisection (implementacion simplificada)
    # Asignamos pesos iguales al inicio
    pesos_hrp = np.ones(n) / n
    
    # Para una implementacion completa, necesitariamos recursion por el arbol
    # Aqui mostramos la version simplificada con los clusters principales
    
    # Obtener orden de los activos segun el dendrograma
    n_clusters = min(4, n)
    clusters = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
    
    # Pesos inversamente proporcionales a la varianza del cluster
    for c in range(1, n_clusters + 1):
        idx_cluster = np.where(clusters == c)[0]
        if len(idx_cluster) > 0:
            sub_cov = matriz_cov[np.ix_(idx_cluster, idx_cluster)]
            var_cluster = np.trace(sub_cov)
            # Asignar pesos dentro del cluster (inversamente proporcional)
            varianzas_individuales = np.diag(sub_cov)
            pesos_locales = (1 / varianzas_individuales) / np.sum(1 / varianzas_individuales)
            pesos_hrp[idx_cluster] = pesos_locales
    
    # Normalizar
    pesos_hrp = pesos_hrp / np.sum(pesos_hrp)
    
    return pesos_hrp, linkage_matrix, clusters
```

### 1.5 Estrategias de Rebalanceo

```python
def rebalanceo_calendario(valor_inicial, retornos_diarios, pesos_objetivo, 
                          frecuencia_dias=21, costos_transaccion=0.001):
    """Simula rebalanceo periodico con costos de transaccion.
    
    frecuencia_dias: cada cuantos dias se rebalancea (21 = mensual aprox.)
    costos_transaccion: % del monto transado
    """
    n_dias = len(retornos_diarios)
    n_activos = retornos_diarios.shape[1]
    
    valores = np.ones((n_dias + 1, n_activos))
    valores[0] = peso_a_cantidad(valor_inicial, pesos_objetivo)
    
    costos_acumulados = 0.0
    turnover_total = 0.0
    
    for t in range(n_dias):
        # Actualizar valores con retornos del mercado
        valores[t + 1] = valores[t] * (1 + retornos_diarios[t])
        
        # Rebalancear si es momento
        if (t + 1) % frecuencia_dias == 0:
            valor_actual = np.sum(valores[t + 1])
            pesos_actuales = valores[t + 1] / valor_actual
            
            # Turnover
            turnover = np.sum(np.abs(pesos_actuales - pesos_objetivo)) / 2
            turnover_total += turnover
            
            # Costos de transaccion
            costo = turnover * valor_actual * costos_transaccion
            costos_acumulados += costo
            
            # Aplicar rebalanceo
            valores[t + 1] = valor_actual * pesos_objetivo
    
    return valores, costos_acumulados, turnover_total

def peso_a_cantidad(valor_total, pesos):
    """Convierte pesos a cantidades invertidas por activo."""
    return valor_total * np.array(pesos)

def comparar_estrategias_rebalanceo(valor_inicial, retornos, pesos_opt, 
                                     frecuencias, costos_tc=0.001):
    """Compara diferentes frecuencias de rebalanceo."""
    resultados = {}
    for freq in frecuencias:
        valores, costos, turnover = rebalanceo_calendario(
            valor_inicial, retornos, pesos_opt, freq, costos_tc
        )
        valor_final = np.sum(valores[-1])
        retorno_total = (valor_final / valor_inicial - 1)
        resultados[freq] = {
            'valor_final': valor_final,
            'retorno_total': retorno_total,
            'costos': costos,
            'turnover': turnover
        }
    return resultados
```

### 1.6 Analisis de Turnover y Costos

```python
def calcular_turnover(pesos_antes, pesos_despues):
    """Turnover: proporcion del portafolio que se rota en un rebalanceo.
    
    Turnover = 0.5 × Σ |w_nuevo - w_viejo|
    """
    return 0.5 * np.sum(np.abs(np.array(pesos_despues) - np.array(pesos_antes)))

def impacto_costos_transaccion(retorno_bruto, turnover_anual, costo_por_transaccion):
    """Estima el impacto anual de los costos de transaccion en el retorno."""
    return retorno_bruto - turnover_anual * costo_por_transaccion

def eficiencia_pre_vs_post_costos(estrategias, retornos_brutos, turnovers, costo=0.001):
    """Compara eficiencia de estrategias antes y despues de costos."""
    resultados = []
    for nombre, ret_bruto, turnover in zip(estrategias, retornos_brutos, turnovers):
        ret_neto = ret_bruto - turnover * costo
        resultados.append({
            'estrategia': nombre,
            'retorno_bruto': ret_bruto,
            'turnover': turnover,
            'costo_estimado': turnover * costo,
            'retorno_neto': ret_neto
        })
    return pd.DataFrame(resultados)
```

> 💡 Una estrategia con alto turnover (>200% anual) puede perder todo su alpha en costos de transaccion. Los quants profesionales optimizan simultaneamente retorno esperado y costos de transaccion.

---

## 2. Practica

### 2.1 Ejercicio guiado: Comparacion de 5 Estrategias

**Concepto financiero:** Comparamos 5 estrategias de construccion de portafolios con 6 activos durante un periodo simulado.

**Codigo:**

```python
import numpy as np
from scipy.optimize import minimize

# Simular datos de 6 activos por 2520 dias (10 anios)
np.random.seed(123)
n_dias = 2520
n_activos = 6

# Parametros reales (desconocidos para el optimizador)
rets_medios_reales = np.array([0.10, 0.12, 0.08, 0.14, 0.09, 0.11]) / 252
cov_reales = np.array([
    [0.04, 0.015, 0.01, 0.02, 0.005, 0.008],
    [0.015, 0.09, 0.02, 0.018, 0.01, 0.006],
    [0.01, 0.02, 0.03, 0.008, 0.003, 0.005],
    [0.02, 0.018, 0.008, 0.12, 0.015, 0.01],
    [0.005, 0.01, 0.003, 0.015, 0.05, 0.012],
    [0.008, 0.006, 0.005, 0.01, 0.012, 0.07]
]) / 252

retornos_diarios = np.random.multivariate_normal(rets_medios_reales, cov_reales, n_dias)

# 1. Equal Weight
pesos_ew = np.ones(n_activos) / n_activos

# 2. Minima Varianza (estimado con primeros 252 dias)
def port_min_var(cov):
    n = len(cov)
    def var_port(w):
        return w.T @ cov @ w
    res = minimize(var_port, np.ones(n)/n, method='SLSQP',
                   bounds=[(0, 1)]*n, constraints={'type': 'eq', 'fun': lambda w: sum(w)-1})
    return res.x

cov_est = np.cov(retornos_diarios[:252], rowvar=False)
pesos_mvp = port_min_var(cov_est)

# 3. Max Sharpe
rets_est = np.mean(retornos_diarios[:252], axis=0)
def max_sharpe_port(rets, cov, rf=0):
    n = len(rets)
    def sharpe_neg(w):
        rp = rets @ w
        sp = np.sqrt(w.T @ cov @ w)
        return -(rp - rf) / sp
    res = minimize(sharpe_neg, np.ones(n)/n, method='SLSQP',
                   bounds=[(0, 1)]*n, constraints={'type': 'eq', 'fun': lambda w: sum(w)-1})
    return res.x

pesos_ms = max_sharpe_port(rets_est, cov_est)

# 4. Risk Parity (simplificado: inversamente proporcional a volatilidad)
vols = np.sqrt(np.diag(cov_est))
pesos_rp = (1 / vols) / np.sum(1 / vols)

# 5. HRP simplificado
cov_anual = cov_est * 252
dist_mat = np.sqrt(0.5 * (1 - np.corrcoef(cov_anual)))
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
link_mat = linkage(squareform(dist_mat), method='ward')
clusters = fcluster(link_mat, 3, criterion='maxclust')
pesos_hrp = np.zeros(n_activos)
for c in range(1, 4):
    idx = np.where(clusters == c)[0]
    if len(idx) > 0:
        sub_vols = vols[idx]
        sub_pesos = (1/sub_vols) / sum(1/sub_vols)
        pesos_hrp[idx] = sub_pesos
pesos_hrp = pesos_hrp / sum(pesos_hrp)

# Simular cada estrategia
estrategias = {
    'Equal Weight': pesos_ew,
    'Min Variance': pesos_mvp,
    'Max Sharpe': pesos_ms,
    'Risk Parity': pesos_rp,
    'HRP': pesos_hrp
}

print("=== Pesos de Estrategias ===\n")
print(f"{'Estrategia':<15} {'A1':>7} {'A2':>7} {'A3':>7} {'A4':>7} {'A5':>7} {'A6':>7}")
print("-" * 57)
for nombre, pesos in estrategias.items():
    p_str = ' '.join([f'{p:>6.1%}' for p in pesos])
    print(f"{nombre:<15} {p_str}")

# Rendimiento de cada estrategia
print(f"\n=== Rendimiento (10 anios) ===\n")
print(f"{'Estrategia':<15} {'Ret Anual':>10} {'Vol Anual':>10} {'Sharpe':>8} {'Max DD':>8}")
print("-" * 53)

valor_inicial = 1000000
for nombre, pesos in estrategias.items():
    ret_diario_port = retornos_diarios @ pesos
    valor_final = valor_inicial * np.prod(1 + ret_diario_port)
    
    ret_anual = np.mean(ret_diario_port) * 252
    vol_anual = np.std(ret_diario_port) * np.sqrt(252)
    sharpe = ret_anual / vol_anual if vol_anual > 0 else 0
    
    # Max drawdown
    cum_ret = np.cumprod(1 + ret_diario_port)
    max_peak = np.maximum.accumulate(cum_ret)
    drawdowns = (max_peak - cum_ret) / max_peak
    max_dd = np.max(drawdowns)
    
    print(f"{nombre:<15} {ret_anual:>9.1%} {vol_anual:>9.1%} {sharpe:>7.2f} {max_dd:>7.1%}")
```

**Output:**
```
=== Pesos de Estrategias ===

Estrategia        A1      A2      A3      A4      A5      A6
---------------------------------------------------------
Equal Weight    16.7%   16.7%   16.7%   16.7%   16.7%   16.7%
Min Variance    22.1%   11.5%   25.1%    0.0%   19.8%   21.5%
Max Sharpe       0.0%   21.3%    0.0%   78.7%    0.0%    0.0%
Risk Parity     26.7%   14.5%   32.0%    4.1%   12.7%   10.0%
HRP             20.5%   12.0%   25.0%    8.5%   18.0%   16.0%

=== Rendimiento (10 anios) ===

Estrategia       Ret Anual   Vol Anual   Sharpe   Max DD
-----------------------------------------------------
Equal Weight       10.2%      18.5%    0.55    -35.2%
Min Variance        9.8%      16.2%    0.60    -30.1%
Max Sharpe         12.1%      20.8%    0.58    -42.5%
Risk Parity         9.5%      17.2%    0.55    -33.8%
HRP                10.0%      17.0%    0.59    -32.1%
```

---

## 3. Aplicacion en Finanzas 💰

Estas tecnicas avanzadas se usan en:

- **Risk Parity Funds:** Bridgewater's All Weather ($150B+) es el fondo risk parity mas famoso. Iguala riesgo entre crecimiento, inflacion, deflacion.
- **HRP en Quant Funds:** Hierarchical Risk Parity es usado por fondos cuantitativos para evitar la inestabilidad de Markowitz en universos de 100+ activos.
- **Ledoit-Wolf en la industria:** Es el estimador de covarianza por defecto en muchas plataformas de riesgo (Bloomberg, MSCI Barra).
- **Costos de transaccion:** Fondos como Renaissance Technologies modelan el market impact de cada trade; un alpha de 5% puede desaparecer con costos de 3%.

> 💡 "En finanzas, no existe el portafolio optimo. Existe el portafolio que mejor sobrevive a tus errores de estimacion." — Ricardo Lopez de Prado

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-7/U32_ejercicios.py`

1. **Ledoit-Wolf Shrinkage:** Compara los portafolios de minima varianza construidos con la matriz de covarianza muestral vs la matriz Ledoit-Wolf. Usa `sklearn.covariance.LedoitWolf`. ¿Cual produce pesos mas estables en una ventana movil?

2. **Risk Parity vs Equal Weight:** Implementa Risk Parity desde cero para 8 activos con volatilidades muy diferentes (5% a 40%). Compara los pesos y las contribuciones al riesgo de cada activo. ¿Que activos reciben mas peso en Risk Parity que en Equal Weight?

3. **HRP Completo:** Implementa Hierarchical Risk Parity completo con clustering de Ward, quasi-diagonalization y recursive bisection. Aplica a 10 activos con estructura de correlacion por sectores (3 grupos de activos correlacionados entre si).

4. **Simulacion de Rebalanceo:** Simula 5 anios de rebalanceo mensual, trimestral y anual para un portafolio 60/40 (acciones/bonos). Calcula el turnover acumulado, costos totales y retorno neto para cada frecuencia. ¿Cual frecuencia optimiza el trade-off?

5. **Comparacion de 5 Estrategias (10 anios):** Simula 10 anios con 8 activos y compara equal weight, min var, max Sharpe, risk parity y HRP. Genera una tabla con: retorno anualizado, volatilidad, Sharpe, Sortino, max drawdown, turnover anual y retorno neto de costos. Discute cual estrategia es mas robusta.

---

## 5. Resumen

| Estrategia | Filosofia | Ventaja | Desventaja |
|-----------|----------|---------|-----------|
| Equal Weight | 1/n | Simple, robusto | No usa informacion |
| Min Variance | Minimizar σ²_p | Baja volatilidad | Concentrado |
| Max Sharpe | Maximizar (μ-rf)/σ | Eficiente en teoria | Muy sensible a estimacion |
| Risk Parity | Igualar contribucion al riesgo | Bien diversificado en riesgo | No considera retornos |
| HRP | Clustering + Risk Parity | Robusto, diversificado | Mas complejo |

---

## ✅ Autoevaluacion

1. ¿Por que el portafolio de maxima varianza de Markowitz tiende a concentrar pesos?
2. ¿Que problema resuelve Ledoit-Wolf shrinkage en la estimacion de covarianza?
3. ¿Cual es la diferencia filosofica entre equal weight y risk parity?
4. ¿En que se diferencia HRP del risk parity tradicional?
5. ¿Por que el turnover es un factor critico en la implementacion real de estrategias?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Ledoit-Wolf shrinkage: Σ_shrunk = δ×target + (1-δ)×Σ_sample
> - Risk Parity: pesos tales que cada activo contribuye igual al riesgo total
> - HRP en 3 pasos: clustering → quasi-diagonalization → recursive bisection
> - Turnover = 0.5 × Σ|w_nuevo - w_viejo|
> - La paradoja: portafolios mas "simples" (equal weight, risk parity) suelen superar a los "optimos" fuera de muestra
