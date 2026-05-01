# 📝 Ejercicios: U26 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U26_ejercicios)

---

```python
# U26: EJERCICIOS — Valoracion de Empresas: DCF y Comparables

import numpy as np

# ============================================================
# Ejercicio 1: DCF Completo — MegaCorp S.A.
# Proyecta 5 anios de FCF para MegaCorp S.A. con:
#   Ingresos iniciales: $8,000M
#   Margen EBITDA: 40%
#   Depreciacion: 6% de ingresos
#   CAPEX: 7% de ingresos
#   Working Capital: 12% de ingresos
#   Tasa impositiva: 21%
#   Crecimiento de ingresos: 15%, 12%, 10%, 8%, 5%
#   WACC: 8.5%
#   Crecimiento perpetuo: 2%
#   Deuda Neta: $2,500M
#   Acciones diluidas: 800M
# Calcula: EV, Equity Value, Precio Implicito por Accion
# ============================================================
print("=== Ejercicio 1: DCF Completo ===")
ingreso_inicial = 8000
margen_ebitda = 0.40
depreciacion_pct = 0.06
capex_pct = 0.07
wc_pct = 0.12
tasa_impositiva = 0.21
tasas_crecimiento = [0.15, 0.12, 0.10, 0.08, 0.05]
wacc_val = 0.085
crecimiento_perpetuo = 0.02
deuda_neta = 2500
acciones = 800

# Escribe tu codigo aqui



# Output esperado:
# === Proyeccion de Flujos ===
# Anio   Ingresos   EBITDA     NOPAT     CAPEX   Delta_WC    FCFF
#    1    9,200.0  3,680.0  2,327.2     644.0      144.0  1,810.0
#    2   10,304.0  4,121.6  2,606.9     721.3      132.5  2,078.3
#    3   11,334.4  4,533.8  2,868.1     793.4      123.1  2,252.4
#    4   12,241.2  4,896.5  3,097.3     856.9      108.8  2,468.9
#    5   12,853.2  5,141.3  3,252.5     901.2       73.4  2,554.0
# 
# Valor Terminal (Gordon): $40,074.4M
# Enterprise Value: $36,753.1M
# Equity Value: $34,253.1M
# Precio Implicito por Accion: $42.82


# ============================================================
# Ejercicio 2: Tabla de Sensibilidad (9x9)
# Con el DCF del ejercicio 1, genera una tabla de sensibilidad
# del precio implicito variando:
#   - WACC: 7.0% a 11.0% (9 niveles)
#   - Crecimiento perpetuo: 1.0% a 5.0% (9 niveles)
# Identifica el rango de precios y el escenario base (WACC=8.5%, g=2%)
# ============================================================
print("\\n=== Ejercicio 2: Tabla de Sensibilidad ===")

# Escribe tu codigo aqui



# Output esperado:
# === Tabla de Sensibilidad: Precio Implicito por Accion ===
#               g=1.0%   g=1.5%   g=2.0%   g=2.5%   g=3.0%   g=3.5%   g=4.0%   g=4.5%   g=5.0%
# WACC=7.0%      55.12    59.84    65.47    72.31    80.78    91.42   105.02   122.76   146.45
# WACC=7.5%      52.34    56.78    62.03    68.37    76.14    85.78    97.95   113.58   134.15
# WACC=8.0%      49.81    53.97    58.90    64.78    71.93    80.74    91.78   105.76   123.90
# WACC=8.5%      47.49    51.41    56.02    61.50  [ 68.12]   76.23    86.31    98.97   115.11
# WACC=9.0%      45.35    49.05    53.38    58.50    64.67    72.18    81.45    92.98   107.58
# WACC=9.5%      43.38    46.86    50.95    55.77    61.55    68.57    77.21    87.92   101.33
# WACC=10.0%     41.56    44.84    48.70    53.25    58.70    65.28    73.35    83.34    95.80
# WACC=10.5%     39.87    42.97    46.62    50.92    56.08    62.28    69.86    79.24    90.88
# WACC=11.0%     38.30    41.23    44.69    48.77    53.66    59.53    66.68    75.51    86.47
# 
# Precio en escenario base (WACC=8.5%, g=2.0%): $56.02
# Rango de precios: $38.30 - $146.45


# ============================================================
# Ejercicio 3: CAPM y WACC Desglosado
# Para MegaCorp, calcula el WACC usando CAPM para el costo de equity:
#   Rf = 4.0%, β = 1.2, Prima de mercado = 5.5%, Kd = 3.5%
#   Estructura de capital: Deuda/Valor Total (D/V) = 25%
# Recalcula el DCF del ejercicio 1 con este WACC mas preciso.
# Compara el precio implicito.
# ============================================================
print("\\n=== Ejercicio 3: CAPM y WACC Desglosado ===")
rf = 0.04
beta_val = 1.2
prima_mercado = 0.055
kd = 0.035
d_sobre_v = 0.25
e_sobre_v = 1 - d_sobre_v
tasa_imp = 0.21

# Escribe tu codigo aqui



# Output esperado:
# Ke (CAPM) = Rf + β * (Rm - Rf) = 4.0% + 1.2 * 5.5% = 10.60%
# WACC = (E/V)*Ke + (D/V)*Kd*(1-t)
#      = 0.75 * 10.60% + 0.25 * 3.5% * 0.79
#      = 7.95% + 0.69% = 8.64%
# 
# === DCF con WACC CAPM ===
# Enterprise Value: $35,712.4M
# Precio Implicito: $41.52
# Diferencia vs WACC 8.5%: -$1.30 (-3.0%)


# ============================================================
# Ejercicio 4: Valor Terminal — Gordon vs Exit Multiple
# Para el DCF del ejercicio 1, compara el valor terminal usando:
#   - Gordon Growth: g = 2%
#   - Exit Multiple: EV/EBITDA = 12x
# ¿Cual metodo da un valor terminal mas alto? ¿Por que?
# Calcula el crecimiento perpetuo IMPLICITO en el exit multiple.
# ============================================================
print("\\n=== Ejercicio 4: Valor Terminal — Gordon vs Exit Multiple ===")

# Escribe tu codigo aqui



# Output esperado:
# === Comparacion Valor Terminal ===
# Gordon Growth (g=2.0%): $40,074.4M
# Exit Multiple (12x EBITDA): $61,695.3M
# Diferencia: $21,620.9M (Exit Multiple es 54% mayor)
# 
# Crecimiento perpetuo implicito en el exit multiple de 12x:
# g_implicito = (EBITDA_n * Multiple * WACC - FCF_{n+1}) / (...)
# g_implicito: ~3.8%
# 
# El Exit Multiple a 12x implica un crecimiento perpetuo
# de ~3.8%, mucho mas agresivo que el 2% de Gordon.
# En la practica, se triangulan ambos metodos.


# ============================================================
# Ejercicio 5: DCF con Analisis de Escenarios
# Para MegaCorp, define 3 escenarios y calcula el precio implicito:
#   - Bull: Crecimiento +3pp en cada anio, WACC -1pp, g perpetuo +0.5pp
#   - Base: Parametros del ejercicio 1
#   - Bear: Crecimiento -3pp, WACC +1pp, g perpetuo -0.5pp
# Reporta los 3 precios y el rango Bull/Bear.
# ============================================================
print("\\n=== Ejercicio 5: DCF con Analisis de Escenarios ===")

# Escribe tu codigo aqui



# Output esperado:
# === Analisis de Escenarios ===
# Escenario  Precio Implicito  vs Base
# Bull            $68.50        +60.0%
# Base            $42.82          0.0%
# Bear            $24.15        -43.6%
# 
# Rango: $24.15 - $68.50
# Football Field: Bear ← | · Base · | → Bull
# Conclusion: Alta sensibilidad a supuestos. Triangulacion
# con comparables necesaria para validar valoracion.
```

---

> [📥 Descargar archivo .py](U26_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
