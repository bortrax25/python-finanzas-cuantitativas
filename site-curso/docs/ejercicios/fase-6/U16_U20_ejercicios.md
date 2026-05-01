# 📝 Ejercicios: U16 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U16_U20_ejercicios)

---

```python
# FASE 6: EJERCICIOS FINALES — Aplicaciones Financieras

# ============================================================
# U16 - Ejercicio: Análisis con NumPy/Pandas
# ============================================================
print("=== U16: Estadísticas de Mercado ===")
import numpy as np

np.random.seed(42)
precios = 100 * (1 + np.random.randn(252).cumsum() * 0.02)
rendimientos = np.diff(precios) / precios[:-1]

ret_anual = np.mean(rendimientos) * 252
vol_anual = np.std(rendimientos, ddof=1) * np.sqrt(252)
sharpe = (ret_anual - 0.04) / vol_anual

print(f"Retorno anualizado: {ret_anual:.2%}")
print(f"Volatilidad anualizada: {vol_anual:.2%}")
print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Max Drawdown: {(np.max(np.maximum.accumulate(precios)) - precios[-1]) / np.max(np.maximum.accumulate(precios)) * 100:.2f}%")


# ============================================================
# U17 - Ejercicio: TIR por iteración
# ============================================================
print("\\n=== U17: TIR ===")
def calcular_tir(flujos, tolerancia=0.0001):
    r_min, r_max = -0.99, 1.0
    while r_max - r_min > tolerancia:
        r = (r_min + r_max) / 2
        vpn = sum(f / (1+r)**t for t, f in enumerate(flujos))
        if vpn > 0:
            r_min = r
        else:
            r_max = r
    return (r_min + r_max) / 2

flujos_proyecto = [-10000, 3000, 4000, 5000, 6000]
tir_resultado = calcular_tir(flujos_proyecto)
print(f"TIR del proyecto: {tir_resultado:.2%}")


# ============================================================
# U18 - Ejercicio: Valoración de bono
# ============================================================
print("\\n=== U18: Precio de Bono ===")
def precio_bono(valor_nominal, cupon_pct, ytm, anios):
    cupon = valor_nominal * (cupon_pct / 100)
    vp_cupones = sum(cupon / (1 + ytm/100)**t for t in range(1, anios + 1))
    vp_nominal = valor_nominal / (1 + ytm/100)**anios
    return vp_cupones + vp_nominal

precio = precio_bono(1000, 5, 4, 10)
print(f"Bono $1,000, cupón 5%, YTM 4%, 10 años: ${precio:,.2f}")

# Tabla de precios para diferentes YTMs
print("\\nYTM → Precio:")
for y in [2, 4, 6, 8, 10]:
    p = precio_bono(1000, 5, y, 10)
    print(f"  {y}% → ${p:,.2f}")


# ============================================================
# U19 - Ejercicio: Monte Carlo VaR
# ============================================================
print("\\n=== U19: Monte Carlo VaR ===")
np.random.seed(123)
s0 = 100.0
mu = 0.08
sigma = 0.20
T = 1.0 / 252  # 1 día
n_sims = 10000

z = np.random.randn(n_sims)
st = s0 * np.exp((mu - 0.5*sigma**2)*T + sigma*np.sqrt(T)*z)
retornos_sim = (st - s0) / s0

var_95_mc = np.percentile(retornos_sim, 5)
var_99_mc = np.percentile(retornos_sim, 1)
cvar_95 = retornos_sim[retornos_sim <= var_95_mc].mean()

print(f"VaR 95% (MC): {var_95_mc:.4%}")
print(f"VaR 99% (MC): {var_99_mc:.4%}")
print(f"CVaR 95% (MC): {cvar_95:.4%}")


# ============================================================
# U20 - Proyecto: Reporte integrado
# ============================================================
print("\\n=== U20: Reporte Integrado ===")
print("=" * 50)
print("ANÁLISIS DE PORTAFOLIO")
print("=" * 50)

# Datos simulados de 3 activos
activos = ["AAPL", "MSFT", "TSLA"]
pesos = [0.40, 0.35, 0.25]
ret_anuales = [0.15, 0.18, 0.12]
vol_anuales = [0.20, 0.22, 0.35]

# Rendimiento del portafolio
port_ret = sum(w * r for w, r in zip(pesos, ret_anuales))
port_vol = np.sqrt(sum((w * v)**2 for w, v in zip(pesos, vol_anuales)))
sharpe_port = (port_ret - 0.04) / port_vol

print(f"{'Activo':<10} {'Peso':>6} {'Ret':>8} {'Vol':>8}")
print("-" * 35)
for a, w, r, v in zip(activos, pesos, ret_anuales, vol_anuales):
    print(f"{a:<10} {w:>6.1%} {r:>7.1%} {v:>7.1%}")
print("-" * 35)
print(f"{'Portafolio':<10} {'100%':>6} {port_ret:>7.1%} {port_vol:>7.1%}")
print()
print(f"Sharpe Ratio (rf=4%): {sharpe_port:.2f}")
print(f"VaR 95% Portafolio: {-(port_ret - 1.645 * port_vol):.2%}")
print("=" * 50)
```

---

> [📥 Descargar archivo .py](U16_U20_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
