# U30: EJERCICIOS — Modelos de Factores y Asset Pricing

import numpy as np

# Datos compartidos: Factores Fama-French simulados (252 dias)
np.random.seed(42)
n_dias = 252

rf_diario = 0.00016  # ~4% anual
mkt_exceso = np.random.normal(0.0006, 0.012, n_dias)   # Mercado
smb = np.random.normal(0.0002, 0.008, n_dias)           # Small Minus Big
hml = np.random.normal(0.0001, 0.007, n_dias)           # High Minus Low
rmw = np.random.normal(0.0001, 0.006, n_dias)           # Robust Minus Weak
cma = np.random.normal(0.0000, 0.005, n_dias)           # Conservative Minus Aggressive

# 20 acciones con diferentes betas "verdaderos"
np.random.seed(100)
n_acciones = 20
betas_verdaderos = {
    'mkt': np.random.uniform(0.5, 1.8, n_acciones),
    'smb': np.random.uniform(-0.5, 0.8, n_acciones),
    'hml': np.random.uniform(-0.4, 0.7, n_acciones),
}

# Generar retornos: R_i = rf + beta_mkt * (R_m - rf) + beta_smb * SMB + beta_hml * HML + eps
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

# ============================================================
# Ejercicio 1: CAPM para 20 Acciones
# Estima beta y alpha de cada accion contra el mercado (CAPM).
# Calcula los p-values. Identifica cuales tienen alpha
# estadisticamente significativo (p < 0.05).
# ============================================================
print("=== Ejercicio 1: CAPM para 20 Acciones ===")

# Escribe tu codigo aqui



# Output esperado:
# === CAPM: Betas y Alphas ===
# Accion  Beta    Alpha (anual)  p-value  Significativo?
#     1   1.35      -0.52%       0.389       No
#     2   0.89      +3.78%       0.041       Si *
#     3   1.52      -1.21%       0.215       No
#     4   0.72      +7.12%       0.008       Si **
#     5   1.10      -0.15%       0.852       No
#   ...   ...        ...          ...        ...
# 
# Acciones con alpha significativo: 2, 4, 8, 14, 18 (5 de 20)


# ============================================================
# Ejercicio 2: Fama-French 3-Factor vs CAPM
# Para las mismas 20 acciones, estima FF3 y compara los R²
# con CAPM. ¿Cuanto mejora el poder explicativo promedio?
# ¿Que acciones mejoran mas su R² al agregar SMB y HML?
# ============================================================
print("\n=== Ejercicio 2: Fama-French 3-Factor vs CAPM ===")

# Escribe tu codigo aqui



# Output esperado:
# === Comparacion R²: CAPM vs FF3 ===
# Accion  R²_CAPM  R²_FF3  Mejora
#     1    0.62     0.78    +0.16
#     2    0.45     0.55    +0.10
#     3    0.58     0.72    +0.14
#     4    0.35     0.68    +0.33 ***
#     5    0.55     0.60    +0.05
#   ...     ...      ...     ...
# 
# Mejora promedio de R²: +0.18
# Acciones que mas mejoran: aquellas con alta exposicion a SMB o HML
# (small caps y value stocks)


# ============================================================
# Ejercicio 3: Clasificacion por Factores
# Usando los betas de FF3, clasifica las 20 acciones en
# categorias: Large/Small (basado en beta_smb) y
# Growth/Value (basado en beta_hml).
# Define umbrales: |beta| < 0.15 = neutral.
# ============================================================
print("\n=== Ejercicio 3: Clasificacion por Factores ===")

# Escribe tu codigo aqui



# Output esperado:
# === Clasificacion por Factores ===
# Accion  beta_smb  Categoria SMB    beta_hml  Categoria HML
#     1    +0.45    Small             -0.25    Growth
#     2    -0.12    Neutral           +0.55    Value
#     3    +0.68    Small             +0.10    Neutral
#     4    -0.35    Large             -0.40    Growth
#     5    +0.05    Neutral           +0.30    Value
#   ...     ...      ...               ...      ...
# 
# Resumen:
#   Large: 5 | Neutral: 7 | Small: 8
#   Growth: 6 | Neutral: 6 | Value: 8


# ============================================================
# Ejercicio 4: Performance Attribution
# Para un portafolio con los siguientes pesos (20 acciones):
# pesos = [0.05]*20 (equal weight), descompone el retorno
# del ultimo dia (dia 252) usando FF5:
#   Retorno = alpha + Σ(beta_k * factor_k)
# Reporta la contribucion de cada factor y el alpha diario.
# ============================================================
print("\n=== Ejercicio 4: Performance Attribution ===")

# Escribe tu codigo aqui



# Output esperado:
# === Performance Attribution (dia 252) ===
# 
# Retorno del portafolio: +0.32%
# 
# Contribuciones:
#   Alpha:           -0.01%
#   Mercado (MKT):   +0.18%
#   Size (SMB):      +0.05%
#   Value (HML):     +0.03%
#   Profit (RMW):    +0.04%
#   Investment (CMA):+0.03%
#   Total factores:  +0.33%
# 
# Alpha diario no es significativo. El retorno se explica
# casi totalmente por factores de mercado y estilo.


# ============================================================
# Ejercicio 5: Black-Litterman con Views
# Implementa el modelo Black-Litterman para 5 activos con:
#   Market caps: [500, 300, 200, 150, 100] (miles de M)
#   Matriz cov: usa submatriz 5x5 de los datos
#   delta = 2.5 (aversion al riesgo)
#   tau = 0.05
# 
# Views:
#   View 1: Activo 0 superara al Activo 1 por 3% (confianza 80%)
#   View 2: Activo 2 tendra retorno absoluto de 10% (confianza 60%)
#   View 3: Activos 3 y 4 superaran al mercado por 1% (confianza 50%)
# 
# Compara los retornos BL con los retornos de equilibrio CAPM.
# ============================================================
print("\n=== Ejercicio 5: Black-Litterman con Views ===")

# Escribe tu codigo aqui



# Output esperado:
# === Black-Litterman ===
# 
# Pesos de equilibrio (market cap):
#   A0: 40.0% | A1: 24.0% | A2: 16.0% | A3: 12.0% | A4: 8.0%
# 
# Retornos de equilibrio (CAPM implicito):
#   A0: 8.2% | A1: 9.5% | A2: 7.1% | A3: 10.8% | A4: 9.2%
# 
# Retornos Black-Litterman (con views):
#   A0: 9.1% | A1: 6.5% | A2: 9.4% | A3: 10.2% | A4: 8.8%
# 
# Cambios principales:
#   A0 sube +0.9pp (View 1: supera a A1)
#   A1 baja -3.0pp (View 1: es superado por A0)
#   A2 sube +2.3pp (View 2: retorno absoluto 10%)
