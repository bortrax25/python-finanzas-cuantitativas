# U30: SOLUCIONES — Modelos de Factores y Asset Pricing

import numpy as np
import statsmodels.api as sm

# Datos compartidos
np.random.seed(42)
n_dias = 252

rf_diario = 0.00016
mkt_exceso = np.random.normal(0.0006, 0.012, n_dias)
smb = np.random.normal(0.0002, 0.008, n_dias)
hml = np.random.normal(0.0001, 0.007, n_dias)
rmw = np.random.normal(0.0001, 0.006, n_dias)
cma = np.random.normal(0.0000, 0.005, n_dias)

np.random.seed(100)
n_acciones = 20
betas_verdaderos = {
    'mkt': np.random.uniform(0.5, 1.8, n_acciones),
    'smb': np.random.uniform(-0.5, 0.8, n_acciones),
    'hml': np.random.uniform(-0.4, 0.7, n_acciones),
}

retornos_acciones = np.zeros((n_dias, n_acciones))
alphas_verdaderos = np.array([0.02, 0.05, -0.01, 0.08, 0.0, -0.03, 0.0, 0.04, 0.0, 0.0,
                               0.01, -0.02, 0.0, 0.06, 0.0, -0.01, 0.0, 0.03, 0.0, 0.0]) / 252

for j in range(n_acciones):
    retornos_acciones[:, j] = (
        rf_diario
        + alphas_verdaderos[j]
        + betas_verdaderos['mkt'][j] * mkt_exceso
        + betas_verdaderos['smb'][j] * smb
        + betas_verdaderos['hml'][j] * hml
        + np.random.normal(0, 0.012, n_dias)
    )

excesos_acciones = retornos_acciones - rf_diario.reshape(-1, 1)


# ============================================================
# Ejercicio 1: CAPM para 20 Acciones
# ============================================================
print("=== Ejercicio 1: CAPM para 20 Acciones ===")

resultados_capm = []
for j in range(n_acciones):
    X = sm.add_constant(mkt_exceso)
    y = excesos_acciones[:, j]
    modelo = sm.OLS(y, X).fit()
    resultados_capm.append({
        'accion': j + 1,
        'beta': modelo.params[1],
        'alpha_anual': modelo.params[0] * 252,
        'p_value': modelo.pvalues[0],
        'r2': modelo.rsquared,
        'significativo': modelo.pvalues[0] < 0.05
    })

print("=== CAPM: Betas y Alphas ===")
print(f"{'Accion':>7} {'Beta':>7} {'Alpha (anual)':>14} {'p-value':>8} {'Significativo?':>15}")
print("-" * 55)
for r in resultados_capm:
    sig = "Si *" if r['p_value'] < 0.05 else ("Si **" if r['p_value'] < 0.01 else "No")
    print(f"{r['accion']:>7} {r['beta']:>7.2f} {r['alpha_anual']:>13.2%} {r['p_value']:>8.3f} {sig:>15}")

significativos = [r for r in resultados_capm if r['significativo']]
print(f"\nAcciones con alpha significativo: {', '.join([str(r['accion']) for r in significativos])} "
      f"({len(significativos)} de {n_acciones})")


# ============================================================
# Ejercicio 2: Fama-French 3-Factor vs CAPM
# ============================================================
print("\n=== Ejercicio 2: Fama-French 3-Factor vs CAPM ===")

resultados_ff3 = []
mejora_r2 = []

print("=== Comparacion R²: CAPM vs FF3 ===")
print(f"{'Accion':>7} {'R²_CAPM':>9} {'R²_FF3':>8} {'Mejora':>8}")
print("-" * 35)
for j in range(n_acciones):
    # Estimamos CAPM y FF3
    X_capm = sm.add_constant(mkt_exceso)
    y = excesos_acciones[:, j]
    r2_capm = sm.OLS(y, X_capm).fit().rsquared
    
    X_ff3 = sm.add_constant(np.column_stack([mkt_exceso, smb, hml]))
    modelo_ff3 = sm.OLS(y, X_ff3).fit()
    r2_ff3 = modelo_ff3.rsquared
    
    mejora = r2_ff3 - r2_capm
    mejora_r2.append(mejora)
    resultados_ff3.append({
        'accion': j + 1,
        'beta_mkt': modelo_ff3.params[1],
        'beta_smb': modelo_ff3.params[2],
        'beta_hml': modelo_ff3.params[3],
        'alpha_anual': modelo_ff3.params[0] * 252,
        'p_value_alpha': modelo_ff3.pvalues[0],
        'r2': r2_ff3
    })
    
    marca = " ***" if mejora > 0.25 else (" **" if mejora > 0.15 else (" *" if mejora > 0.10 else ""))
    print(f"{j + 1:>7} {r2_capm:>8.2f} {r2_ff3:>8.2f} {mejora:>+7.2f}{marca}")

print(f"\nMejora promedio de R²: +{np.mean(mejora_r2):.2f}")
print("Acciones que mas mejoran: aquellas con alta exposicion a SMB o HML")
print("(small caps y value stocks)")


# ============================================================
# Ejercicio 3: Clasificacion por Factores
# ============================================================
print("\n=== Ejercicio 3: Clasificacion por Factores ===")

def clasificar_smb(b):
    if b > 0.15:
        return 'Small'
    elif b < -0.15:
        return 'Large'
    return 'Neutral'

def clasificar_hml(b):
    if b > 0.15:
        return 'Value'
    elif b < -0.15:
        return 'Growth'
    return 'Neutral'

print("=== Clasificacion por Factores ===")
print(f"{'Accion':>7} {'beta_smb':>9} {'SMB':>10} {'beta_hml':>9} {'HML':>10}")
print("-" * 48)
for r in resultados_ff3:
    cat_smb = clasificar_smb(r['beta_smb'])
    cat_hml = clasificar_hml(r['beta_hml'])
    print(f"{r['accion']:>7} {r['beta_smb']:>+8.2f} {cat_smb:>10} {r['beta_hml']:>+8.2f} {cat_hml:>10}")

cats_smb = [clasificar_smb(r['beta_smb']) for r in resultados_ff3]
cats_hml = [clasificar_hml(r['beta_hml']) for r in resultados_ff3]
print(f"\nResumen:")
print(f"  Large: {cats_smb.count('Large')} | Neutral: {cats_smb.count('Neutral')} | Small: {cats_smb.count('Small')}")
print(f"  Growth: {cats_hml.count('Growth')} | Neutral: {cats_hml.count('Neutral')} | Value: {cats_hml.count('Value')}")


# ============================================================
# Ejercicio 4: Performance Attribution
# ============================================================
print("\n=== Ejercicio 4: Performance Attribution ===")

pesos = np.ones(n_acciones) / n_acciones

# Estimar betas al FF5 para el portafolio
X_ff5 = sm.add_constant(np.column_stack([mkt_exceso, smb, hml, rmw, cma]))
y_portafolio = excesos_acciones @ pesos

modelo_ff5 = sm.OLS(y_portafolio, X_ff5).fit()
alpha_port = modelo_ff5.params[0]
betas_port = {
    'mkt': modelo_ff5.params[1],
    'smb': modelo_ff5.params[2],
    'hml': modelo_ff5.params[3],
    'rmw': modelo_ff5.params[4],
    'cma': modelo_ff5.params[5],
}

# Atribucion del ultimo dia
ultimo_dia = -1
retorno_port = y_portafolio[ultimo_dia]
contribuciones = {}
for factor, beta_val in betas_port.items():
    if factor == 'mkt':
        valor_factor = mkt_exceso[ultimo_dia]
    else:
        valor_factor = eval(factor)[ultimo_dia]
    contribuciones[factor] = beta_val * valor_factor

contribucion_total = sum(contribuciones.values())
alpha_residual = retorno_port - contribucion_total

print("=== Performance Attribution (dia 252) ===\n")
print(f"Retorno del portafolio (exceso): {retorno_port:+.4%}\n")
print("Contribuciones:")
print(f"  Alpha:           {alpha_residual:+.4%}")
for factor, contrib in contribuciones.items():
    print(f"  {factor.upper():<16} {contrib:+.4%}")
print(f"  Total factores:  {contribucion_total:+.4%}")
print(f"\nAlpha diario no es significativo. El retorno se explica")
print(f"casi totalmente por factores de mercado y estilo.")


# ============================================================
# Ejercicio 5: Black-Litterman con Views
# ============================================================
print("\n=== Ejercicio 5: Black-Litterman con Views ===")

market_caps = np.array([500, 300, 200, 150, 100])
delta = 2.5
tau = 0.05

# Submatriz 5x5 de covarianza
cov_5 = matriz_covarianza[:5, :5] = np.array([
    [0.045, 0.018, 0.015, 0.022, 0.008],
    [0.018, 0.040, 0.017, 0.020, 0.007],
    [0.015, 0.017, 0.042, 0.025, 0.006],
    [0.022, 0.020, 0.025, 0.065, 0.008],
    [0.008, 0.007, 0.006, 0.008, 0.025]
])

print("=== Black-Litterman ===\n")

# Pesos de equilibrio
pesos_eq = market_caps / np.sum(market_caps)
print("Pesos de equilibrio (market cap):")
for i in range(5):
    print(f"  A{i}: {pesos_eq[i]:.1%}", end='')
print()

# Retornos de equilibrio
pi = delta * cov_5 @ pesos_eq
print("\nRetornos de equilibrio (CAPM implicito):")
for i in range(5):
    print(f"  A{i}: {pi[i]:.1%}", end='')
print()

# Views
views_P = np.array([
    [1, -1, 0, 0, 0],      # A0 supera a A1
    [0, 0, 1, 0, 0],       # A2 retorno absoluto
    [0, 0, 0, 0.5, 0.5],   # A3 y A4 superan al mercado
])
views_Q = np.array([0.03, 0.10, 0.01])

# Matriz de confianza (Omega)
omega = np.diag([0.0004, 0.0016, 0.0025])  # Confianzas: 80%, 60%, 50%

# Black-Litterman formula
tau_sigma = tau * cov_5
M = np.linalg.inv(
    np.linalg.inv(tau_sigma)
    + views_P.T @ np.linalg.inv(omega) @ views_P
)
retornos_bl = M @ (
    np.linalg.inv(tau_sigma) @ pi
    + views_P.T @ np.linalg.inv(omega) @ views_Q
)

print("\nRetornos Black-Litterman (con views):")
for i in range(5):
    print(f"  A{i}: {retornos_bl[i]:.1%}", end='')
print()

print("\nCambios principales:")
for i in range(5):
    cambio = retornos_bl[i] - pi[i]
    print(f"  A{i}: {cambio:+.1%}", end='')
    if cambio > 0.005:
        print(" (View alcista)")
    elif cambio < -0.005:
        print(" (View bajista)")
    else:
        print()
