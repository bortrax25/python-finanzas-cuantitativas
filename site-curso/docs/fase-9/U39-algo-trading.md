# U39: Algorithmic Trading — Estrategias y Backtesting

> **Lectura previa:** [U38: Machine Learning Avanzado — Métodos Cuantitativos](./U38-ml-avanzado.md)
> **Próxima unidad:** [U40: Infraestructura y Producción](./U40-infraestructura.md)

---

## 1. Teoría

### 1.1 ¿Qué es el trading algorítmico?

El trading algorítmico ejecuta estrategias de inversión de forma sistemática, basada en reglas cuantitativas predefinidas. Un sistema algorítmico típico tiene 4 componentes:

1. **Señales (alpha):** Reglas que generan predicciones de compra/venta
2. **Ejecución:** Traducción de señales a órdenes (posiciones, tamaños)
3. **Gestión de riesgo:** Límites de exposición, stop-loss, position sizing
4. **Backtesting:** Simulación histórica para validar la estrategia

En esta unidad construiremos un **framework de backtesting vectorizado desde cero**, sin depender de librerías externas como Backtrader o Zipline. El objetivo es que entiendas cada componente.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### 1.2 Estrategia 1: Momentum

El momentum es la tendencia: activos que han subido tienden a seguir subiendo en el corto-mediano plazo (3-12 meses).

```python
def estrategia_momentum(precios, ventana_retorno=60, ventana_vol=20, umbral=0.0):
    """
    Estrategia de momentum: compra si el retorno de los últimos N días
    supera un umbral, con position sizing inverso a la volatilidad.
    
    Retorna un DataFrame de posiciones (-1, 0, 1) para cada día.
    """
    retornos = precios.pct_change()
    retorno_acum = precios / precios.shift(ventana_retorno) - 1
    volatilidad = retornos.rolling(ventana_vol).std()
    
    # Señal: long si momentum > umbral, short si < -umbral
    senal = np.where(retorno_acum > umbral, 1, np.where(retorno_acum < -umbral, -1, 0))
    
    # Position sizing: 1/volatilidad para targeting de riesgo constante
    with np.errstate(divide='ignore', invalid='ignore'):
        posicion = senal / volatilidad
        posicion = np.where(np.isfinite(posicion), posicion, 0)
    
    return pd.DataFrame({
        'posicion': posicion.flatten() if posicion.ndim > 1 else posicion,
        'senal': senal.flatten() if senal.ndim > 1 else senal,
    }, index=precios.index)

# Ejemplo: precios simulados
np.random.seed(42)
dias = 252 * 5  # 5 años
retornos_sim = np.random.normal(0.0004, 0.012, dias)
precios_sim = 100 * np.exp(np.cumsum(retornos_sim))
precios_serie = pd.Series(precios_sim, name='precio')
```

### 1.3 Estrategia 2: Mean Reversion

La reversión a la media asume que los precios oscilan alrededor de un valor "justo" y tienden a volver a él.

```python
def estrategia_mean_reversion(precios, ventana_media=20, n_desviaciones=2.0):
    """
    Estrategia de mean reversion con Bollinger Bands.
    
    Vende cuando el precio supera la banda superior (sobrecomprado).
    Compra cuando cae por debajo de la banda inferior (sobrevendido).
    """
    media_movil = precios.rolling(ventana_media).mean()
    desviacion = precios.rolling(ventana_media).std()
    
    banda_superior = media_movil + n_desviaciones * desviacion
    banda_inferior = media_movil - n_desviaciones * desviacion
    
    # Señal: +1 (compra) si precio < banda inferior, -1 (vende) si > banda superior
    senal = np.where(
        precios < banda_inferior, 1,
        np.where(precios > banda_superior, -1, 0)
    )
    
    return pd.DataFrame({
        'senal': senal,
        'media_movil': media_movil,
        'banda_superior': banda_superior,
        'banda_inferior': banda_inferior,
    }, index=precios.index)
```

### 1.4 Estrategia 3: Pairs Trading (Cointegración)

Dos activos cointegrados comparten una relación de largo plazo. Cuando el spread entre ellos se desvía, apostamos a que volverá.

```python
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

def encontrar_pares_cointegrados(precios_df, p_value_umbral=0.05):
    """
    Identifica pares de activos cointegrados.
    Retorna los pares con p-value < umbral y su ratio de hedge.
    """
    tickers = precios_df.columns
    pares = []
    
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            score, p_value, _ = coint(precios_df[tickers[i]], precios_df[tickers[j]])
            
            if p_value < p_value_umbral:
                # Calcular ratio de hedge
                y = precios_df[tickers[i]].values
                X = sm.add_constant(precios_df[tickers[j]].values)
                hedge_ratio = OLS(y, X).fit().params[1]
                
                pares.append({
                    'activo_1': tickers[i],
                    'activo_2': tickers[j],
                    'p_value': p_value,
                    'hedge_ratio': hedge_ratio,
                })
    
    return pares

def estrategia_pairs_trading(precio_1, precio_2, hedge_ratio, ventana_zscore=60, entrada=2.0, salida=0.5):
    """
    Estrategia de pairs trading.
    
    Calcula el spread normalizado (z-score). 
    Entra cuando |z-score| > entrada, sale cuando |z-score| < salida.
    """
    spread = precio_1 - hedge_ratio * precio_2
    spread_media = spread.rolling(ventana_zscore).mean()
    spread_std = spread.rolling(ventana_zscore).std()
    z_score = (spread - spread_media) / spread_std
    
    posicion = np.zeros(len(spread))
    en_posicion = False
    
    for i in range(ventana_zscore, len(spread)):
        z = z_score.iloc[i]
        
        if not en_posicion:
            if z > entrada:
                posicion[i] = -1  # Spread muy alto → short spread (corto activo 1, largo activo 2)
                en_posicion = True
            elif z < -entrada:
                posicion[i] = 1   # Spread muy bajo → long spread
                en_posicion = True
        else:
            if abs(z) < salida:
                en_posicion = False  # Cerrar posición
            else:
                posicion[i] = posicion[i - 1]  # Mantener
    
    return pd.Series(posicion, index=precio_1.index, name='posicion')
```

### 1.5 Framework de Backtesting Vectorizado

```python
class Backtester:
    """
    Framework de backtesting vectorizado desde cero.
    Soporta múltiples estrategias, costos de transacción y métricas avanzadas.
    """
    
    def __init__(self, precios, tasa_libre_riesgo=0.02):
        """
        Parámetros:
            precios: DataFrame con precios (filas=fechas, columnas=activos)
            tasa_libre_riesgo: tasa anual libre de riesgo
        """
        self.precios = precios
        self.retornos = precios.pct_change()
        self.rf = tasa_libre_riesgo
        self.rf_diaria = (1 + tasa_libre_riesgo) ** (1 / 252) - 1
    
    def ejecutar(self, posiciones, costos=0.001, capital_inicial=100000):
        """
        Ejecuta el backtest.
        
        Parámetros:
            posiciones: DataFrame con posiciones objetivo (mismo índice que precios)
            costos: costo de transacción (0.001 = 10 bps)
            capital_inicial: capital inicial del portafolio
        """
        # Alinear índices
        idx_comun = self.retornos.index.intersection(posiciones.index)
        ret = self.retornos.loc[idx_comun]
        pos = posiciones.loc[idx_comun]
        
        # Retornos de la estrategia (sin costos)
        retornos_estrategia = (pos * ret).sum(axis=1)
        
        # Costos de transacción
        cambios = pos.diff().abs().sum(axis=1)
        costos_trans = cambios * costos
        
        # Retornos netos
        retornos_netos = retornos_estrategia - costos_trans
        
        # Equity curve
        equity = capital_inicial * (1 + retornos_netos).cumprod()
        
        self.resultados = {
            'equity': equity,
            'retornos_netos': retornos_netos,
            'retornos_brutos': retornos_estrategia,
            'costos_transaccion': costos_trans,
            'cambios': cambios,
        }
        
        return self.resultados
    
    def metricas(self):
        """Calcula métricas de rendimiento."""
        ret = self.resultados['retornos_netos'].dropna()
        eq = self.resultados['equity'].dropna()
        
        n_dias = len(ret)
        ret_total = eq.iloc[-1] / eq.iloc[0] - 1
        ret_anual = (1 + ret_total) ** (252 / n_dias) - 1
        vol_anual = ret.std() * np.sqrt(252)
        sharpe = (ret_anual - self.rf) / vol_anual if vol_anual > 0 else 0
        
        # Sortino (solo penaliza volatilidad a la baja)
        ret_negativos = ret[ret < 0]
        vol_downside = ret_negativos.std() * np.sqrt(252) if len(ret_negativos) > 0 else 0
        sortino = (ret_anual - self.rf) / vol_downside if vol_downside > 0 else 0
        
        # Max drawdown
        peak = eq.expanding().max()
        drawdown = (eq - peak) / peak
        max_dd = drawdown.min()
        
        # Calmar ratio
        calmar = ret_anual / abs(max_dd) if max_dd != 0 else 0
        
        # Win rate
        win_rate = (ret > 0).mean()
        
        # Profit factor
        ganancias = ret[ret > 0].sum()
        perdidas = abs(ret[ret < 0].sum())
        profit_factor = ganancias / perdidas if perdidas > 0 else np.inf
        
        return {
            'Retorno Total': ret_total,
            'Retorno Anualizado': ret_anual,
            'Volatilidad Anual': vol_anual,
            'Sharpe Ratio': sharpe,
            'Sortino Ratio': sortino,
            'Max Drawdown': max_dd,
            'Calmar Ratio': calmar,
            'Win Rate': win_rate,
            'Profit Factor': profit_factor,
            'Días Trading': n_dias,
        }
    
    def resumen(self):
        """Imprime resumen de métricas formateado."""
        m = self.metricas()
        print("=" * 45)
        print(f"{'MÉTRICAS DE BACKTEST':^45}")
        print("=" * 45)
        print(f"Retorno Total:       {m['Retorno Total']:>8.2%}")
        print(f"Retorno Anualizado:  {m['Retorno Anualizado']:>8.2%}")
        print(f"Volatilidad Anual:    {m['Volatilidad Anual']:>8.2%}")
        print(f"Sharpe Ratio:        {m['Sharpe Ratio']:>8.2f}")
        print(f"Sortino Ratio:       {m['Sortino Ratio']:>8.2f}")
        print(f"Max Drawdown:        {m['Max Drawdown']:>8.2%}")
        print(f"Calmar Ratio:        {m['Calmar Ratio']:>8.2f}")
        print(f"Win Rate:            {m['Win Rate']:>8.2%}")
        print(f"Profit Factor:       {m['Profit Factor']:>8.2f}")
        print(f"Días Trading:        {m['Días Trading']:>8}")
        print("=" * 45)
```

### 1.6 Walk-Forward Optimization

La optimización walk-forward evita el overfitting al re-optimizar parámetros periódicamente con datos solo del pasado reciente.

```python
def walk_forward_backtest(precios, funcion_estrategia, rango_param,
                          ventana_train=504, ventana_test=126, paso=63):
    """
    Walk-forward backtest.
    
    Parámetros:
        precios: DataFrame de precios
        funcion_estrategia: función(posiciones, param) → DataFrame de posiciones
        rango_param: lista de parámetros a probar
        ventana_train: días para optimizar (2 años)
        ventana_test: días para testear out-of-sample
        paso: días de avance entre ventanas
    """
    resultados_wf = []
    inicio = ventana_train
    
    while inicio + ventana_test <= len(precios):
        train = precios.iloc[inicio - ventana_train:inicio]
        test = precios.iloc[inicio:inicio + ventana_test]
        
        # Optimizar parámetro en train
        mejores_metricas = {'sharpe': -np.inf, 'param': None}
        
        for param in rango_param:
            pos_train = funcion_estrategia(train, param)
            ret = (pos_train['posicion'] * train.pct_change()).iloc[:, 0]
            sharpe = ret.mean() / ret.std() * np.sqrt(252) if ret.std() > 0 else 0
            
            if sharpe > mejores_metricas['sharpe']:
                mejores_metricas = {'sharpe': sharpe, 'param': param}
        
        # Aplicar mejor parámetro en test
        pos_test = funcion_estrategia(test, mejores_metricas['param'])
        ret_test = (pos_test['posicion'] * test.pct_change()).iloc[:, 0]
        
        resultados_wf.append({
            'inicio': test.index[0],
            'fin': test.index[-1],
            'param_optimo': mejores_metricas['param'],
            'sharpe_train': mejores_metricas['sharpe'],
            'sharpe_test': ret_test.mean() / ret_test.std() * np.sqrt(252),
        })
        
        inicio += paso
    
    return pd.DataFrame(resultados_wf)
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Backtest completo de momentum

**Concepto financiero:** Las estrategias de momentum cross-sectional (comprar ganadores, vender perdedores) han generado retornos anormales históricamente.

**Código:**

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simular precios de 10 activos (5 años)
np.random.seed(42)
n_dias, n_activos = 1260, 10
retornos = np.random.normal(0.0003, 0.012, (n_dias, n_activos))
precios = 100 * np.exp(np.cumsum(retornos, axis=0))
precios_df = pd.DataFrame(
    precios,
    index=pd.date_range('2020-01-01', periods=n_dias, freq='B'),
    columns=[f'Activo_{i}' for i in range(n_activos)]
)

# Estrategia momentum cross-sectional:
# Cada mes, comprar el top 3 con mejor momentum (3 meses), short el bottom 3
# Rebalanceo mensual (cada 21 días)
ventana_mom = 63   # 3 meses
ventana_reb = 21   # mensual

posiciones = pd.DataFrame(0, index=precios_df.index, columns=precios_df.columns)

for i in range(ventana_mom, len(precios_df), ventana_reb):
    mom = precios_df.iloc[i] / precios_df.iloc[i - ventana_mom] - 1
    mom_sorted = mom.sort_values(ascending=False)
    long_tickers = mom_sorted.head(3).index
    short_tickers = mom_sorted.tail(3).index
    
    # Asignar posiciones: +1/3 long, -1/3 short (portafolio beta-neutral)
    fin_ventana = min(i + ventana_reb, len(precios_df))
    posiciones.loc[precios_df.index[i:fin_ventana], long_tickers] = 1 / 3
    posiciones.loc[precios_df.index[i:fin_ventana], short_tickers] = -1 / 3

# Backtest
bt = Backtester(precios_df)
resultados = bt.ejecutar(posiciones, costos=0.001)
bt.resumen()

# Gráfico
fig, axes = plt.subplots(2, 1, figsize=(12, 8))
equity = resultados['equity']
axes[0].plot(equity.index, equity.values)
axes[0].set_title('Equity Curve — Momentum Cross-Sectional')
axes[0].set_ylabel('Capital ($)')
axes[0].grid(True, alpha=0.3)

dd = equity / equity.expanding().max() - 1
axes[1].fill_between(dd.index, 0, dd.values * 100, color='red', alpha=0.3)
axes[1].set_title('Drawdown')
axes[1].set_ylabel('Drawdown (%)')
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
# plt.show()
```

**Output:**
```
=============================================
          MÉTRICAS DE BACKTEST
=============================================
Retorno Total:           28.45%
Retorno Anualizado:       5.13%
Volatilidad Anual:        8.92%
Sharpe Ratio:              0.35
Sortino Ratio:             0.52
Max Drawdown:            -15.23%
Calmar Ratio:              0.34
Win Rate:                 52.34%
Profit Factor:             1.34
Días Trading:              1260
=============================================
```

---

## 3. Aplicación en Finanzas 💰

**AQR Capital Management:** Gestiona más de $100B usando estrategias sistemáticas basadas en momentum, value, y carry. Su "Managed Futures" fund es un ejemplo de momentum puro aplicado a futuros de commodities, FX y bonos.

**Renaissance Technologies:** Su Medallion Fund (mejor track record de la historia: ~66% anual antes de fees) usa una combinación de cientos de señales, incluyendo momentum, mean reversion, y patrones estadísticos.

**Pairs Trading en Market Neutral:** Pioneros como Ed Thorp y Gerry Bamberger en Morgan Stanley en los 80s hicieron del pairs trading la base de las estrategias "statistical arbitrage" que hoy dominan el mercado.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-9/U39_ejercicios.py`

1. **Momentum con backtester:** Implementar estrategia de momentum para un solo activo. Usar el Backtester para evaluar Sharpe, Sortino, max drawdown. Probar con y sin costos de transacción.

2. **Comparación de estrategias:** Implementar momentum, mean reversion (Bollinger) y cruce de medias móviles (SMA 20/50). Backtestear las 3 con los mismos datos. Graficar las 3 equity curves en un mismo plot.

3. **Pairs trading:** Generar 2 series de precios cointegradas. Implementar la estrategia de pairs trading con z-score. Calcular Sharpe y comparar con buy-and-hold de cada activo.

4. **Walk-forward optimization:** Aplicar walk-forward al parámetro de ventana de momentum (20, 40, 60, 80, 100 días). Comparar el Sharpe out-of-sample con el Sharpe de un parámetro fijo naive (ventana=60).

---

## 5. Resumen

| Concepto | Código / Fórmula |
|----------|-----------------|
| Momentum | `precio / precio.shift(N) - 1 > umbral` |
| Mean Reversion | `precio - media > N * desviacion` |
| Pairs Trading | `z_score = (spread - media) / std`, entrada en ±2.0 |
| Backtester | `retornos_estrategia = pos * retornos` |
| Costos transacción | `|cambio_posicion| * tasa_comision` |
| Sharpe Ratio | `(ret_anual - rf) / vol_anual` |
| Sortino Ratio | `(ret_anual - rf) / vol_downside` |
| Max Drawdown | `min((equity / peak) - 1)` |
| Calmar Ratio | `ret_anual / |max_drawdown|` |
| Walk-Forward | optimizar en train, validar en test out-of-sample |

---

## ✅ Autoevaluación

1. ¿Qué diferencia hay entre Sortino y Sharpe? ¿Cuándo es preferible Sortino?
2. Explica la cointegración y por qué es la base del pairs trading.
3. ¿Por qué los costos de transacción son críticos en estrategias de alta frecuencia pero menos en estrategias mensuales?
4. ¿Qué es el walk-forward optimization y por qué es superior a una optimización única en todo el histórico?
5. ¿Cómo interpretas un profit factor de 1.5? ¿Y uno de 0.8?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Retorno de estrategia = posiciones × retornos - costos de transacción
> - Métricas clave: Sharpe (riesgo total), Sortino (riesgo a la baja), max drawdown (peor escenario histórico)
> - Pairs trading se basa en cointegración, no correlación (la correlación es de corto plazo, la cointegración de largo plazo)
> - Walk-forward: la única forma honesta de optimizar parámetros sin data snooping
> - Siempre incluye costos de transacción (10-50 bps por trade). Sin costos, cualquier estrategia parece buena.
