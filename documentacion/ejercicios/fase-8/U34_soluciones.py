# U34: SOLUCIONES — Series de Tiempo: ARIMA y Volatilidad

# ============================================================
# Ejercicio 1: Estacionariedad y transformaciones
# ============================================================
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

np.random.seed(42)
dias = 1260
retornos = np.random.normal(0.0004, 0.012, dias)
precios = 3000 * np.exp(np.cumsum(retornos))

print("=== Ejercicio 1: Estacionariedad y Transformaciones ===")

serie_precios = pd.Series(precios)
serie_ret_simple = serie_precios.pct_change().dropna()
serie_ret_log = np.log(serie_precios).diff().dropna()
serie_diff = serie_precios.diff().dropna()

series = {
    'Precios': serie_precios,
    'Retornos simples': serie_ret_simple,
    'Retornos log': serie_ret_log,
    'Primeras diferencias': serie_diff,
}

print(f"{'Serie':<22} | {'ADF p-value':<12} | {'KPSS p-value':<12} | Estacionaria?")
print("-" * 65)

for nombre, serie in series.items():
    adf_stat, adf_p, *_ = adfuller(serie.dropna())
    kpss_stat, kpss_p, *_ = kpss(serie.dropna(), regression='c', nlags='auto')
    es_estacionaria = adf_p < 0.05 and kpss_p > 0.05
    print(f"{nombre:<22} | {adf_p:<12.4f} | {kpss_p:<12.4f} | {'SÍ' if es_estacionaria else 'NO'}")


# ============================================================
# Ejercicio 2: ARIMA para pronóstico de retornos
# ============================================================
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error

print("\n=== Ejercicio 2: ARIMA para pronóstico ===")

retornos_serie = pd.Series(retornos)
n_train = int(len(retornos_serie) * 0.8)
train = retornos_serie[:n_train]
test = retornos_serie[n_train:]

# Auto-ARIMA en train
modelo = auto_arima(
    train,
    start_p=0, start_q=0,
    max_p=5, max_q=5,
    seasonal=False,
    trace=False,
    error_action='ignore',
    suppress_warnings=True,
    stepwise=True,
)

print(f"Mejor modelo ARIMA: ARIMA{modelo.order}")

# Pronóstico
pronostico, conf_int = modelo.predict(n_periods=len(test), return_conf_int=True)
pronostico_serie = pd.Series(pronostico, index=test.index)

rmse_arima = np.sqrt(mean_squared_error(test, pronostico_serie))
rmse_naive = np.sqrt(mean_squared_error(test, np.full(len(test), train.mean())))

print(f"RMSE ARIMA:          {rmse_arima:.6f}")
print(f"RMSE Naive (media):  {rmse_naive:.6f}")
mejora = (rmse_naive - rmse_arima) / rmse_naive * 100
print(f"Mejora: {mejora:.1f}%")


# ============================================================
# Ejercicio 3: GARCH vs Volatilidad Realizada
# ============================================================
from arch import arch_model

print("\n=== Ejercicio 3: GARCH vs Volatilidad Realizada ===")

np.random.seed(42)
n = 1000

# Generar proceso GARCH(1,1) simulado
omega_v, alpha_v, beta_v = 0.01, 0.08, 0.90
vol_verdadera = np.zeros(n)
retornos_garch = np.zeros(n)
for t in range(1, n):
    vol_verdadera[t] = np.sqrt(omega_v + alpha_v * retornos_garch[t-1]**2 + beta_v * vol_verdadera[t-1]**2)
    retornos_garch[t] = np.random.normal(0, vol_verdadera[t])

retornos_serie = pd.Series(retornos_garch)

# Ajustar GARCH(1,1)
modelo_g11 = arch_model(retornos_serie * 100, vol='Garch', p=1, q=1, dist='normal')
res_g11 = modelo_g11.fit(disp='off')
vol_g11 = res_g11.conditional_volatility / 100

# Ajustar GARCH(2,1)
modelo_g21 = arch_model(retornos_serie * 100, vol='Garch', p=2, q=1, dist='normal')
res_g21 = modelo_g21.fit(disp='off')
vol_g21 = res_g21.conditional_volatility / 100

# Volatilidad realizada
vol_r10 = retornos_serie.rolling(10).std()
vol_r20 = retornos_serie.rolling(20).std()
vol_r60 = retornos_serie.rolling(60).std()

# Correlaciones
print("Correlaciones con volatilidad realizada:")
print(f"{'Modelo':<14} | {'Vol rolling 10d':<16} | {'20d':<8} | {'60d':<8}")
print("-" * 52)

for nombre, vol_cond in [('GARCH(1,1)', vol_g11), ('GARCH(2,1)', vol_g21)]:
    c10 = vol_cond.corr(vol_r10)
    c20 = vol_cond.corr(vol_r20)
    c60 = vol_cond.corr(vol_r60)
    print(f"{nombre:<14} | {c10:<16.4f} | {c20:<8.4f} | {c60:<8.4f}")

mejor_corr = max(
    (vol_g11.corr(vol_r10), 'GARCH(1,1)', '10d'),
    (vol_g11.corr(vol_r20), 'GARCH(1,1)', '20d'),
    (vol_g11.corr(vol_r60), 'GARCH(1,1)', '60d'),
    (vol_g21.corr(vol_r10), 'GARCH(2,1)', '10d'),
    (vol_g21.corr(vol_r20), 'GARCH(2,1)', '20d'),
    (vol_g21.corr(vol_r60), 'GARCH(2,1)', '60d'),
)
print(f"Mejor combinación: {mejor_corr[1]} + vol rolling {mejor_corr[2]} (r={mejor_corr[0]:.4f})")


# ============================================================
# Ejercicio 4: Comparación GARCH/EGARCH y efecto apalancamiento
# ============================================================
print("\n=== Ejercicio 4: GARCH vs EGARCH ===")

# GARCH(1,1) con t
modelo_garch_t = arch_model(retornos_serie * 100, vol='Garch', p=1, q=1, dist='t')
res_garch_t = modelo_garch_t.fit(disp='off')

# EGARCH(1,1) con t
modelo_egarch_t = arch_model(retornos_serie * 100, vol='EGARCH', p=1, q=1, dist='t')
res_egarch_t = modelo_egarch_t.fit(disp='off')

print(f"GARCH(1,1)  — AIC: {res_garch_t.aic:.2f}, BIC: {res_garch_t.bic:.2f}")
print(f"EGARCH(1,1) — AIC: {res_egarch_t.aic:.2f}, BIC: {res_egarch_t.bic:.2f}")
mejor = 'EGARCH' if res_egarch_t.aic < res_garch_t.aic else 'GARCH'
print(f"Mejor modelo: {mejor} (menor AIC)")

# Parámetro de asimetría de EGARCH
if 'gamma[1]' in res_egarch_t.params:
    gamma_val = res_egarch_t.params['gamma[1]']
    gamma_pval = res_egarch_t.pvalues['gamma[1]']
    print(f"Parámetro de asimetría EGARCH: {gamma_val:.4f} (p-value: {gamma_pval:.4f})")
    if gamma_val < 0 and gamma_pval < 0.05:
        print("Conclusión: Efecto apalancamiento SIGNIFICATIVO")
        print("  → Las caídas del mercado generan más volatilidad que las subidas")
    elif gamma_val < 0:
        print("Conclusión: Efecto apalancamiento presente pero NO significativo")
    else:
        print("Conclusión: No se detecta efecto apalancamiento")
else:
    print("Parámetro de asimetría no encontrado en el modelo")
