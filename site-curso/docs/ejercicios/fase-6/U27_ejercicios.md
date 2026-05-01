# 📝 Ejercicios: U27 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U27_ejercicios)

---

```python
# U27: EJERCICIOS — Modelo LBO y Private Equity

import numpy as np

# ============================================================
# Ejercicio 1: LBO Base — RetailCo
# Construye un LBO completo para RetailCo:
#   EBITDA inicial: $100M, Precio compra: 8x EBITDA
#   Financiamiento: 60% deuda senior (Kd=5%), 40% equity
#   Proyeccion 5 anios: crecimiento ingresos 6% anual,
#   margen EBITDA 25%, D&A 4% ingresos, CAPEX 5% ingresos,
#   WC 8% ingresos, tasa impositiva 21%
#   Salida: 8x EBITDA anio 5
# Calcula: IRR del sponsor y MOIC
# ============================================================
print("=== Ejercicio 1: LBO Base ===")
ebitda_inicial = 100.0
multiplo_entrada = 8.0
deuda_pct = 0.60
equity_pct = 0.40
tasa_deuda = 0.05
tasa_impositiva = 0.21
crecimiento_ingresos = 0.06
margen_ebitda = 0.25
d_a_pct = 0.04
capex_pct = 0.05
wc_pct = 0.08
multiplo_salida = 8.0
anios_proyeccion = 5

ingreso_inicial = ebitda_inicial / margen_ebitda
precio_compra = ebitda_inicial * multiplo_entrada
deuda_inicial = precio_compra * deuda_pct
equity_inicial = precio_compra * equity_pct

# Escribe tu codigo aqui



# Output esperado:
# === LBO RetailCo ===
# Precio compra: $800.0M | Deuda: $480.0M | Equity: $320.0M
# 
# Anio  EBITDA    Intereses  Utilidad Neta  FCF      Saldo Deuda
#   1   100.0      24.0       53.6          28.8     451.2
#   2   106.0      22.6       56.8          30.5     420.7
#   3   112.4      21.0       60.2          32.3     388.4
#   4   119.1      19.4       63.8          34.2     354.2
#   5   126.2      17.7       67.6          36.3     317.9
# 
# EBITDA salida (anio 5): $126.2M
# EV salida: $1,010.0M | Deuda remanente: $317.9M
# Equity salida: $692.1M
# 
# IRR sponsor: 16.7%
# MOIC: 2.23x


# ============================================================
# Ejercicio 2: Debt Schedule Detallado
# Agrega al LBO del ejercicio 1:
#   (a) Amortizacion obligatoria de 5% anual sobre saldo inicial
#   (b) Cash sweep del 100% del FCF excedente
# Muestra la tabla de evolucion de deuda anio a anio.
# ============================================================
print("\\n=== Ejercicio 2: Debt Schedule Detallado ===")
amortizacion_obligatoria = 0.05

# Escribe tu codigo aqui



# Output esperado:
# === Debt Schedule Detallado ===
# Anio  Saldo_Ini  Int   Amort_Oblig  Cash_Sweep  Amort_Total  Saldo_Fin
#   1   480.0     24.0     24.0         4.8         28.8        451.2
#   2   451.2     22.6     22.6         4.5         27.1        424.1
#   3   424.1     21.2     21.2         4.2         25.4        398.7
#   4   398.7     19.9     19.9         4.0         23.9        374.7
#   5   374.7     18.7     18.7         3.7         22.5        352.2
# 
# IRR con debt schedule: 17.1%
# MOIC con debt schedule: 2.31x


# ============================================================
# Ejercicio 3: Sensibilidad 3x3 — Multiplos Entrada vs Salida
# Genera una tabla de sensibilidad 3x3 para el LBO base:
#   - Multiplos de entrada: 7x, 8x, 9x
#   - Multiplos de salida: 7x, 8x, 9x
# Reporta IRR para cada combinacion. ¿Que escenarios generan
# IRR < 15% (target minimo tipico de PE)?
# ============================================================
print("\\n=== Ejercicio 3: Sensibilidad 3x3 ===")
multiplos_entrada = [7.0, 8.0, 9.0]
multiplos_salida = [7.0, 8.0, 9.0]

# Escribe tu codigo aqui



# Output esperado:
# === Sensibilidad IRR: Entrada x Salida ===
#           Salida 7x  Salida 8x  Salida 9x
# Entrada 7x   22.5%     28.7%     34.3%
# Entrada 8x  [10.8%]    16.7%     22.1%
# Entrada 9x   -2.5%      5.3%     10.8%
# 
# Escenarios con IRR < 15%:
#   - Entrada 9x con Salida 7x: -2.5%
#   - Entrada 9x con Salida 8x: 5.3%
#   - Entrada 8x con Salida 7x: 10.8%
#   - Entrada 9x con Salida 9x: 10.8%
# 
# Conclusion: Comprar a 9x EBITDA es arriesgado, solo genera
# retorno aceptable si la salida es >= 9x (multiple expansion).


# ============================================================
# Ejercicio 4: Estructura de Deuda en Capas
# Modela el LBO base pero con deuda en dos tramos:
#   - Senior: 4x EBITDA ($400M), tasa 5%
#   - Subordinada: 2x EBITDA ($200M), tasa 9%
# La cascada de pagos paga primero intereses y principal de la
# deuda senior. Si sobra FCF, paga subordinada.
# Equity sponsor: el resto ($200M, 25%)
# Compara IRR y MOIC con el LBO base de una sola capa.
# ============================================================
print("\\n=== Ejercicio 4: Estructura de Deuda en Capas ===")
deuda_senior_x = 4.0
tasa_senior = 0.05
deuda_sub_x = 2.0
tasa_sub = 0.09

# Escribe tu codigo aqui



# Output esperado:
# === LBO con Deuda en Capas ===
# Deuda Senior: $400.0M (5.0%) | Subordinada: $200.0M (9.0%)
# Equity Sponsor: $200.0M (25%)
# 
# Anio  Saldo_Senior  Saldo_Sub  FCF_Sponsor
#   1      376.2       195.3        2.5
#   2      351.9       189.8        3.1
#   3      326.7       183.4        3.7
#   4      300.5       176.0        4.0
#   5      273.1       167.4        4.5
# 
# Equity salida: $567.6M | FCF acumulado sponsor: $17.8M
# IRR: 23.2% | MOIC: 2.93x
# 
# Comparacion:
#   LBO 1 capa (60% deuda):  IRR 16.7%, MOIC 2.23x
#   LBO 2 capas (75% deuda): IRR 23.2%, MOIC 2.93x
# 
# Mayor apalancamiento aumenta retorno pero tambien riesgo de default.


# ============================================================
# Ejercicio 5: Sensibilidad Avanzada 5x5
# Genera una matriz de sensibilidad con 5 niveles de crecimiento
# de EBITDA (-2%, 0%, 2%, 4%, 6%) vs 5 niveles de multiplo de
# salida (6x, 7x, 8x, 9x, 10x) usando el LBO de 2 capas.
# Grafica la matriz como tabla de IRR. ¿Que celdas generan
# IRR > 25% (target agresivo de PE)?
# ============================================================
print("\\n=== Ejercicio 5: Sensibilidad Avanzada 5x5 ===")
crecimientos_ebitda = [-0.02, 0.00, 0.02, 0.04, 0.06]
multiplos_salida_5 = [6.0, 7.0, 8.0, 9.0, 10.0]

# Escribe tu codigo aqui



# Output esperado:
# === Sensibilidad Avanzada: IRR por Crecimiento y Exit Multiple ===
# Crec\\Exit     6x      7x      8x      9x     10x
#   -2%       -5.2%    2.1%    8.5%   14.2%   19.3%
#    0%        0.8%    8.1%   14.5%   20.2%   25.5%*
#    2%        6.7%   14.1%   20.5%   26.3%*  31.8%*
#    4%       12.7%   20.1%   26.7%*  32.8%*  38.6%*
#    6%       18.6%   26.2%*  33.2%*  39.5%*  45.5%*
# 
# * IRR > 25% (target agresivo PE)
# 
# Conclusión: Para alcanzar IRR > 25% se requiere:
#   - Crecimiento >= 2% + Exit Multiple >= 9x, o
#   - Crecimiento >= 4% + Exit Multiple >= 8x, o
#   - Crecimiento >= 6% + Exit Multiple >= 7x
```

---

> [📥 Descargar archivo .py](U27_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
