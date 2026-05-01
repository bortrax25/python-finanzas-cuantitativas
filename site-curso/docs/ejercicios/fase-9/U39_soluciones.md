# ✅ Soluciones: U39 — Fase 9

> [← Volver a ejercicios Fase 9](index.md) | [📥 Descargar .py](U39_soluciones)

---

```python
# U39: SOLUCIONES — Algorithmic Trading: Estrategias y Backtesting

# ============================================================
# Clase Backtester (misma que en teoría)
# ============================================================
import numpy as np
import pandas as pd

class Backtester:
    def __init__(self, precios, tasa_libre_riesgo=0.02):
        self.precios = precios
        self.retornos = precios.pct_change()
        self.rf = tasa_libre_riesgo
        self.rf_diaria = (1 + tasa_libre_riesgo) ** (1 / 252) - 1
    
    def ejecutar(self, posiciones, costos=0.001, capital_inicial=100000):
        if isinstance(posiciones, np.ndarray):
            posiciones = pd.Series(posiciones, index=self.precios.index)
        
        idx_comun = self.retornos.index.intersection(posiciones.index)
        ret = self.retornos.loc[idx_comun]
        pos = posiciones.loc[idx_comun]
        
        retornos_estrategia = pos.shift(1) * ret
        cambios = pos.diff().abs()
        costos_trans = cambios * costos
        retornos_netos = retornos_estrategia - costos_trans
        
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
        ret = self.resultados['retornos_netos'].dropna()
        eq = self.resultados['equity'].dropna()
        
        n_dias = len(ret)
        ret_total = eq.iloc[-1] / eq.iloc[0] - 1
        ret_anual = (1 + ret_total) ** (252 / n_dias) - 1
        vol_anual = ret.std() * np.sqrt(252)
        sharpe = (ret_anual - self.rf) / vol_anual if vol_anual > 0 else 0
        
        ret_negativos = ret[ret < 0]
        vol_downside = ret_negativos.std() * np.sqrt(252) if len(ret_negativos) > 0 else 0
        sortino = (ret_anual - self.rf) / vol_downside if vol_downside > 0 else 0
        
        peak = eq.expanding().max()
        drawdown = (eq - peak) / peak
        max_dd = drawdown.min()
        calmar = ret_anual / abs(max_dd) if max_dd != 0 else 0
        win_rate = (ret > 0).mean()
        
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
        }

def print_metricas(nombre, metricas):
    print(f"\\n{nombre}:")
    print(f"  Retorno Total:    {metricas['Retorno Total']:+.2%}")
    print(f"  Sharpe Ratio:      {metricas['Sharpe Ratio']:.2f}")
    print(f"  Max Drawdown:     {metricas['Max Drawdown']:+.2%}")


# ============================================================
# Ejercicio 1: Momentum con backtester
# ============================================================
np.random.seed(42)
dias = 1260
retornos_sim = np.random.normal(0.0004, 0.012, dias)
precios = 100 * np.exp(np.cumsum(retornos_sim))
precios_serie = pd.Series(precios, index=pd.date_range('2020-01-01', periods=dias, freq='B'), name='activo')

print("=== Ejercicio 1: Momentum con Backtester ===")

# Estrategia de momentum
ventana = 60
retorno_ventana = precios_serie / precios_serie.shift(ventana) - 1
senal = np.where(retorno_ventana > 0, 1, -1)
posiciones_mom = pd.Series(senal, index=precios_serie.index)

bt_mom = Backtester(pd.DataFrame({'activo': precios_serie}))
bt_mom.ejecutar(posiciones_mom, costos=0.001)
print_metricas("Estrategia Momentum", bt_mom.metricas())

# Buy and hold
posiciones_bh = pd.Series(1, index=precios_serie.index)
bt_bh = Backtester(pd.DataFrame({'activo': precios_serie}))
bt_bh.ejecutar(posiciones_bh, costos=0.0)
print_metricas("Buy-and-Hold", bt_bh.metricas())


# ============================================================
# Ejercicio 2: Comparación de 3 estrategias
# ============================================================
print("\\n=== Ejercicio 2: Comparación de 3 Estrategias ===")

precios_df = pd.DataFrame({'activo': precios_serie})

# (a) Momentum
ret_mom = precios_serie / precios_serie.shift(60) - 1
pos_mom = pd.Series(np.where(ret_mom > 0, 1, -1), index=precios_serie.index)

# (b) Mean Reversion (Bollinger)
sma20 = precios_serie.rolling(20).mean()
std20 = precios_serie.rolling(20).std()
pos_mr = pd.Series(np.where(precios_serie < sma20 - 2 * std20, 1,
                   np.where(precios_serie > sma20 + 2 * std20, -1, 0)), index=precios_serie.index)

# (c) Cruce SMA 20/50
sma20_c = precios_serie.rolling(20).mean()
sma50_c = precios_serie.rolling(50).mean()
pos_sma = pd.Series(np.where(sma20_c > sma50_c, 1, -1), index=precios_serie.index)

estrategias = [
    ('Momentum', pos_mom),
    ('Mean Reversion', pos_mr),
    ('Cruce SMA', pos_sma),
]

print(f"{'Estrategia':<16} | {'Sharpe':<8} | {'Sortino':<8} | {'Max DD':<8}")
print("-" * 46)

bt_compare = Backtester(precios_df)
for nombre, pos in estrategias:
    bt_compare.ejecutar(pos, costos=0.001)
    m = bt_compare.metricas()
    print(f"{nombre:<16} | {m['Sharpe Ratio']:<8.2f} | {m['Sortino Ratio']:<8.2f} | {m['Max Drawdown']:>+7.1%}")


# ============================================================
# Ejercicio 3: Pairs Trading
# ============================================================
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm

print("\\n=== Ejercicio 3: Pairs Trading ===")

np.random.seed(42)
n = 1260
ruido_a = np.random.normal(0.0002, 0.01, n)
precio_a = 100 * np.exp(np.cumsum(ruido_a))

# B cointegrado con A
ruido_b = np.random.normal(0, 0.005, n)
precio_b = 0.8 * precio_a + ruido_b + 50  # relación lineal

idx = pd.date_range('2020-01-01', periods=n, freq='B')
p_a = pd.Series(precio_a, index=idx, name='A')
p_b = pd.Series(precio_b, index=idx, name='B')

# Test cointegración
coint_t, p_valor, _ = coint(p_a, p_b)
print(f"Test de cointegración: p-value = {p_valor:.4f} {'(COINTEGRADOS)' if p_valor < 0.05 else '(NO cointegrados)'}")

# Hedge ratio
X = sm.add_constant(p_b.values)
hedge_ratio = sm.OLS(p_a.values, X).fit().params[1]
print(f"Hedge ratio: {hedge_ratio:.4f}")

# Pairs trading con z-score
spread = p_a - hedge_ratio * p_b
spread_media = spread.rolling(60).mean()
spread_std = spread.rolling(60).std()
z_score = (spread - spread_media) / spread_std

posicion = pd.Series(0, index=idx)
en_posicion = False
for i in range(60, len(spread)):
    z = z_score.iloc[i]
    if not en_posicion:
        if z > 2.0:
            posicion.iloc[i] = -1
            en_posicion = True
        elif z < -2.0:
            posicion.iloc[i] = 1
            en_posicion = True
    else:
        if abs(z) < 0.5:
            en_posicion = False
        else:
            posicion.iloc[i] = posicion.iloc[i - 1]

# Retorno del par = pos * (retorno_A - hedge_ratio * retorno_B)
ret_a = p_a.pct_change()
ret_b = p_b.pct_change()
ret_pairs = posicion.shift(1) * (ret_a - hedge_ratio * ret_b)

bt_pairs = Backtester(pd.DataFrame({'activo': p_a}))
bt_pairs.resultados = {
    'retornos_netos': ret_pairs,
    'equity': 100000 * (1 + ret_pairs).cumprod(),
}

m_pairs = bt_pairs.metricas()
print_metricas("Pairs Trading", m_pairs)

bt_bh_a = Backtester(pd.DataFrame({'activo': p_a}))
bt_bh_a.ejecutar(pd.Series(1, index=idx), costos=0)
print_metricas("Buy-and-Hold A", bt_bh_a.metricas())

bt_bh_b = Backtester(pd.DataFrame({'activo': p_b}))
bt_bh_b.ejecutar(pd.Series(1, index=idx), costos=0)
print_metricas("Buy-and-Hold B", bt_bh_b.metricas())


# ============================================================
# Ejercicio 4: Walk-forward optimization
# ============================================================
print("\\n=== Ejercicio 4: Walk-Forward Optimization ===")

ventanas_prueba = [20, 40, 60, 80, 100]
ventana_train = 504   # 2 años
ventana_test = 126    # 6 meses
paso = 63             # 3 meses

resultados_wf = []
inicio = ventana_train

while inicio + ventana_test <= len(precios_serie):
    train = precios_serie.iloc[inicio - ventana_train:inicio]
    test = precios_serie.iloc[inicio:inicio + ventana_test]
    
    mejor_sharpe = -np.inf
    mejor_ventana = None
    
    for v in ventanas_prueba:
        ret_v = train / train.shift(v) - 1
        pos_v = pd.Series(np.where(ret_v > 0, 1, -1), index=train.index)
        ret_estr = pos_v.shift(1) * train.pct_change()
        sharpe_v = ret_estr.mean() / ret_estr.std() * np.sqrt(252) if ret_estr.std() > 0 else 0
        
        if sharpe_v > mejor_sharpe:
            mejor_sharpe = sharpe_v
            mejor_ventana = v
    
    # Aplicar en test
    ret_test = test / test.shift(mejor_ventana) - 1
    pos_test = pd.Series(np.where(ret_test > 0, 1, -1), index=test.index)
    ret_estr_test = pos_test.shift(1) * test.pct_change()
    sharpe_test = ret_estr_test.mean() / ret_estr_test.std() * np.sqrt(252) if ret_estr_test.std() > 0 else 0
    
    resultados_wf.append({
        'train_ini': train.index[0].strftime('%Y-%m'),
        'test_ini': test.index[0].strftime('%Y-%m'),
        'param_opt': mejor_ventana,
        'sharpe_oos': sharpe_test,
    })
    
    inicio += paso

# Reporte
print(f"{'#':<4} | {'Train':<12} | {'Test':<12} | {'Param ópt':<12} | {'Sharpe OOS':<12}")
print("-" * 60)
for i, r in enumerate(resultados_wf):
    print(f"{i+1:<4} | {r['train_ini']:<12} | {r['test_ini']:<12} | {r['param_opt']:<12} | {r['sharpe_oos']:<12.2f}")

sharpe_wf = np.mean([r['sharpe_oos'] for r in resultados_wf])

# Naive (ventana fija = 60)
ret_naive = precios_serie / precios_serie.shift(60) - 1
pos_naive = pd.Series(np.where(ret_naive > 0, 1, -1), index=precios_serie.index)
ret_naive_estr = pos_naive.shift(1) * precios_serie.pct_change()
sharpe_naive = ret_naive_estr.mean() / ret_naive_estr.std() * np.sqrt(252)

print(f"\\nWalk-forward Sharpe acumulado: {sharpe_wf:.2f}")
print(f"Naive (ventana=60) Sharpe:     {sharpe_naive:.2f}")
if sharpe_wf > sharpe_naive:
    mejora = (sharpe_wf - sharpe_naive) / abs(sharpe_naive) * 100
    print(f"Mejora walk-forward: +{mejora:.1f}%")
else:
    print(f"Walk-forward no supera al naive en este período")
```

---

> [📥 Descargar archivo .py](U39_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 9](index.md)
