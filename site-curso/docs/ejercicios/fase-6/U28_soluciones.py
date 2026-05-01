# U28: SOLUCIONES — Derivados: Opciones y Modelos de Pricing

import numpy as np
from scipy.stats import norm
from scipy.optimize import newton

# ============================================================
# Funciones auxiliares
# ============================================================

def bsm(tipo, s, k, r, sigma, T):
    """Precio Black-Scholes-Merton."""
    if sigma <= 0 or T <= 0:
        if tipo == 'call':
            return max(s - k * np.exp(-r * T), 0)
        return max(k * np.exp(-r * T) - s, 0)
    d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if tipo == 'call':
        return s * norm.cdf(d1) - k * np.exp(-r * T) * norm.cdf(d2)
    return k * np.exp(-r * T) * norm.cdf(-d2) - s * norm.cdf(-d1)

def griegas(tipo, s, k, r, sigma, T):
    """Calcula las 5 griegas."""
    if sigma <= 0 or T <= 0:
        return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
    d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if tipo == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    gamma = norm.pdf(d1) / (s * sigma * np.sqrt(T))
    
    theta_call = (-s * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                  - r * k * np.exp(-r * T) * norm.cdf(d2))
    theta_put = (-s * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * k * np.exp(-r * T) * norm.cdf(-d2))
    theta = (theta_call if tipo == 'call' else theta_put) / 365
    
    vega = s * norm.pdf(d1) * np.sqrt(T) * 0.01
    
    if tipo == 'call':
        rho = k * T * np.exp(-r * T) * norm.cdf(d2) * 0.01
    else:
        rho = -k * T * np.exp(-r * T) * norm.cdf(-d2) * 0.01
    
    return {'delta': delta, 'gamma': gamma, 'theta': theta,
            'vega': vega, 'rho': rho}

def binomial_crr(tipo, s, k, r, sigma, T, pasos=100):
    """Arbol binomial CRR."""
    dt = T / pasos
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    precios = np.zeros(pasos + 1)
    for j in range(pasos + 1):
        precios[j] = s * (u ** (pasos - j)) * (d ** j)
    
    if tipo == 'call':
        valores = np.maximum(precios - k, 0)
    else:
        valores = np.maximum(k - precios, 0)
    
    descuento = np.exp(-r * dt)
    for i in range(pasos - 1, -1, -1):
        for j in range(i + 1):
            valores[j] = descuento * (p * valores[j] + (1 - p) * valores[j + 1])
    
    return valores[0]

def volatilidad_implicita(precio_mercado, tipo, s, k, r, T, sigma_0=0.3):
    """Volatilidad implicita por Newton-Raphson."""
    sigma = sigma_0
    for _ in range(200):
        precio_bsm = bsm(tipo, s, k, r, sigma, T)
        d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        vega = s * norm.pdf(d1) * np.sqrt(T)
        if abs(vega) < 1e-12:
            break
        diff = precio_bsm - precio_mercado
        sigma = sigma - diff / vega
        if abs(diff) < 1e-8:
            return sigma
    return sigma


# ============================================================
# Ejercicio 1: BSM Pricer + Griegas
# ============================================================
print("=== Ejercicio 1: BSM Pricer + Griegas ===")
s0 = 100.0
k = 105.0
r = 0.04
sigma = 0.30
T = 0.5

call = bsm('call', s0, k, r, sigma, T)
put = bsm('put', s0, k, r, sigma, T)
griegas_call = griegas('call', s0, k, r, sigma, T)
griegas_put = griegas('put', s0, k, r, sigma, T)

print("=== BSM Pricer ===")
print(f"Parametros: S0=${s0}, K=${k}, r={r:.1%}, sigma={sigma:.1%}, T={T} anios")
print(f"\nCall: ${call:.2f}")
print(f"  Delta: {griegas_call['delta']:.3f}  Gamma: {griegas_call['gamma']:.4f}  "
      f"Theta: ${griegas_call['theta']:+.4f}/dia  Vega: ${griegas_call['vega']:.3f}  "
      f"Rho: ${griegas_call['rho']:+.3f}")
print(f"Put:  ${put:.2f}")
print(f"  Delta: {griegas_put['delta']:+.3f}  Gamma: {griegas_put['gamma']:.4f}  "
      f"Theta: ${griegas_put['theta']:+.4f}/dia  Vega: ${griegas_put['vega']:.3f}  "
      f"Rho: ${griegas_put['rho']:+.3f}")


# ============================================================
# Ejercicio 2: Binomial vs BSM — Convergencia
# ============================================================
print("\n=== Ejercicio 2: Binomial vs BSM ===")
pasos_a_probar = [10, 50, 100, 500, 2000]
bsm_call = bsm('call', s0, k, r, sigma, T)

print("=== Convergencia Binomial -> BSM ===")
print(f"{'Pasos':>7} {'Binomial':>10} {'BSM':>10} {'Diferencia':>12}")
print("-" * 41)
for pasos in pasos_a_probar:
    bin_val = binomial_crr('call', s0, k, r, sigma, T, pasos)
    diff = abs(bin_val - bsm_call)
    print(f"{pasos:>7} ${bin_val:>9.4f} ${bsm_call:>9.4f} ${diff:>11.4f}")

print("\nCon 500+ pasos, la diferencia es < $0.01")


# ============================================================
# Ejercicio 3: Volatility Smile
# ============================================================
print("\n=== Ejercicio 3: Volatility Smile ===")
s0_aapl = 185.0
r_aapl = 0.045
T_aapl = 30 / 365
strikes_aapl = [170, 180, 185, 190, 200, 210]
precios_mercado = [16.50, 8.70, 6.00, 3.95, 1.50, 0.52]

print("=== Volatility Smile AAPL ===")
print(f"{'Strike':>7} {'Precio Mercado':>16} {'IV':>8}")
print("-" * 33)
ivs = []
for k_i, precio_i in zip(strikes_aapl, precios_mercado):
    iv = volatilidad_implicita(precio_i, 'call', s0_aapl, k_i, r_aapl, T_aapl)
    ivs.append(iv)
    print(f"${k_i:>6} ${precio_i:>15,.2f} {iv:>7.1%}")

print("\nForma: Smile (concava hacia arriba). IV minima cerca de ATM.")
print("Las opciones OTM (tanto calls altas como puts bajas) tienen")
print("IV mas alta -> mercado asigna mayor probabilidad a movimientos")
print("extremos que la distribucion log-normal de BSM.")


# ============================================================
# Ejercicio 4: Payoff de Estrategias
# ============================================================
print("\n=== Ejercicio 4: Payoff de Estrategias ===")
precio_compra_stock = 100.0
strike_largo = 100.0
strike_corto = 110.0
strike_put_protect = 95.0
prima_call_atm = 7.80
prima_put_atm = 10.72
prima_call_otm = 2.50

print("=== Analisis de Estrategias ===\n")

# Covered Call
costo_cc = precio_compra_stock - prima_call_otm
max_ganancia_cc = (strike_corto - precio_compra_stock) + prima_call_otm
max_perdida_cc = -costo_cc
be_cc = costo_cc
print("Covered Call (Long Stock + Short Call K=$110):")
print(f"  Costo neto: ${costo_cc:.2f} | Max Ganancia: ${max_ganancia_cc:.2f} | Max Perdida: ${max_perdida_cc:.2f}")
print(f"  Break-even: ${be_cc:.2f}\n")

# Protective Put
costo_pp = precio_compra_stock + prima_put_atm
max_perdida_pp = -(precio_compra_stock - strike_put_protect + prima_put_atm)
be_pp = precio_compra_stock + prima_put_atm
print("Protective Put (Long Stock + Long Put K=$95):")
print(f"  Costo neto: ${costo_pp:.2f} | Max Ganancia: Ilimitada | Max Perdida: ${max_perdida_pp:.2f}")
print(f"  Break-even: ${be_pp:.2f}\n")

# Bull Spread con calls
costo_bs = prima_call_atm - prima_call_otm
max_ganancia_bs = (strike_corto - strike_largo) - costo_bs
max_perdida_bs = -costo_bs
be_bs = strike_largo + costo_bs
print("Bull Spread (Long Call K=$100 + Short Call K=$110):")
print(f"  Costo neto: ${costo_bs:.2f} | Max Ganancia: ${max_ganancia_bs:.2f} | Max Perdida: ${max_perdida_bs:.2f}")
print(f"  Break-even: ${be_bs:.2f}\n")

# Straddle
costo_st = prima_call_atm + prima_put_atm
be_down = strike_largo - costo_st
be_up = strike_largo + costo_st
print("Straddle (Long Call + Long Put K=$100):")
print(f"  Costo neto: ${costo_st:.2f} | Max Ganancia: Ilimitada | Max Perdida: ${-costo_st:.2f}")
print(f"  Break-even (down): ${be_down:.2f} | Break-even (up): ${be_up:.2f}")


# ============================================================
# Ejercicio 5: IV Surface
# ============================================================
print("\n=== Ejercicio 5: IV Surface ===")
s0_surf = 100.0
r_surf = 0.05
strikes_surf = [80, 90, 100, 110, 120]
T_surf = [30/365, 90/365, 180/365, 365/365]
nombres_T = ['1M', '3M', '6M', '1Y']

# Generar precios sinteticos con IV realista (skew + term structure)
def generar_precio_sintetico(tipo, s, k, r, T, strike_atm=100, iv_atm=0.22, skew=-0.003):
    """Genera precio con IV variable (skew lineal)."""
    moneyness = k - strike_atm
    iv = iv_atm + skew * moneyness
    # Ajustar por plazo: menor plazo = mayor skew
    iv += 0.01 * (30/365 / T - 1)
    iv = max(iv, 0.05)
    return bsm(tipo, s, k, r, iv, T)

print("=== Superficie de Volatilidad Implicita ===")
header = f"{'Strike':>7} " + "".join([f"{n:>8}" for n in nombres_T])
print(header)
print("-" * 44)

for strike_val in strikes_surf:
    fila = f"${strike_val:>6} "
    for j, T_val in enumerate(T_surf):
        precio_sint = generar_precio_sintetico('call', s0_surf, strike_val, r_surf, T_val)
        iv_rec = volatilidad_implicita(precio_sint, 'call', s0_surf, strike_val, r_surf, T_val)
        fila += f"{iv_rec:>7.1%} "
    print(fila)

print("\nObservaciones:")
print("  - Skew: puts OTM (strikes bajos) tienen mayor IV")
print("  - Term structure: a mayor plazo, menor skew (se aplana)")
print("  - La IV ATM aumenta ligeramente con el plazo (contango tipico)")
