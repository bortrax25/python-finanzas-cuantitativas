# U27: SOLUCIONES — Modelo LBO y Private Equity

import numpy as np
from scipy.optimize import newton

# ============================================================
# Ejercicio 1: LBO Base — RetailCo
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

print(f"Precio compra: ${precio_compra:.1f}M | Deuda: ${deuda_inicial:.1f}M | Equity: ${equity_inicial:.1f}M")

# Proyectar ingresos y metrica operativas
ingresos_arr = np.zeros(anios_proyeccion)
ingresos_arr[0] = ingreso_inicial * (1 + crecimiento_ingresos)
for t in range(1, anios_proyeccion):
    ingresos_arr[t] = ingresos_arr[t - 1] * (1 + crecimiento_ingresos)

ebitda_arr = ingresos_arr * margen_ebitda
depreciacion_arr = ingresos_arr * d_a_pct
ebit_arr = ebitda_arr - depreciacion_arr

# Simulacion LBO
saldo_deuda = deuda_inicial
flujos_sponsor = []

print(f"\n{'Anio':>5} {'EBITDA':>8} {'Intereses':>10} {'Utilidad Neta':>14} {'FCF':>8} {'Saldo Deuda':>12}")
print("-" * 60)
for t in range(anios_proyeccion):
    intereses = saldo_deuda * tasa_deuda
    ebt_anio = ebit_arr[t] - intereses
    impuestos = max(0, ebt_anio * tasa_impositiva)
    utilidad_neta = ebt_anio - impuestos
    
    capex = ingresos_arr[t] * capex_pct
    wc_val = ingresos_arr[t] * wc_pct
    delta_wc = wc_val - (ingresos_arr[t - 1] * wc_pct if t > 0 else ingreso_inicial * wc_pct)
    
    fcf = utilidad_neta + depreciacion_arr[t] - capex - delta_wc
    
    # Pagar deuda con FCF
    pago_deuda = min(fcf, saldo_deuda)
    saldo_deuda -= pago_deuda
    
    remanente = max(0, fcf - pago_deuda)
    flujos_sponsor.append(remanente)
    
    print(f"{t + 1:>5} {ebitda_arr[t]:>8.1f} {intereses:>10.1f} {utilidad_neta:>14.1f} {fcf:>8.1f} {saldo_deuda:>12.1f}")

# Salida
ebitda_salida = ebitda_arr[-1]
ev_salida = ebitda_salida * multiplo_salida
equity_salida = ev_salida - saldo_deuda

print(f"\nEBITDA salida (anio 5): ${ebitda_salida:.1f}M")
print(f"EV salida: ${ev_salida:,.1f}M | Deuda remanente: ${saldo_deuda:.1f}M")
print(f"Equity salida: ${equity_salida:,.1f}M")

# IRR
flujos_totales = [-equity_inicial] + flujos_sponsor + [equity_salida]

def vpn_irr(r):
    return sum(f / (1 + r) ** t for t, f in enumerate(flujos_totales))

tir_result = newton(vpn_irr, 0.15)
moic_result = (sum(flujos_sponsor) + equity_salida) / equity_inicial

print(f"\nIRR sponsor: {tir_result:.1%}")
print(f"MOIC: {moic_result:.2f}x")


# ============================================================
# Ejercicio 2: Debt Schedule Detallado
# ============================================================
print("\n=== Ejercicio 2: Debt Schedule Detallado ===")
amortizacion_obligatoria = 0.05

saldo_deuda_ds = deuda_inicial
flujos_sponsor_ds = []

print(f"{'Anio':>5} {'Saldo_Ini':>10} {'Int':>8} {'Amort_Oblig':>12} {'Cash_Sweep':>11} {'Amort_Total':>12} {'Saldo_Fin':>10}")
print("-" * 70)
for t in range(anios_proyeccion):
    saldo_inicial_t = saldo_deuda_ds
    intereses_t = saldo_deuda_ds * tasa_deuda
    amort_oblig = saldo_deuda_ds * amortizacion_obligatoria
    
    ebt_anio = ebit_arr[t] - intereses_t
    impuestos = max(0, ebt_anio * tasa_impositiva)
    utilidad_neta = ebt_anio - impuestos
    
    capex = ingresos_arr[t] * capex_pct
    wc_val = ingresos_arr[t] * wc_pct
    delta_wc = wc_val - (ingresos_arr[t - 1] * wc_pct if t > 0 else ingreso_inicial * wc_pct)
    fcf = utilidad_neta + depreciacion_arr[t] - capex - delta_wc
    
    fcf_post_int = fcf - intereses_t
    cash_sweep = max(0, fcf_post_int - amort_oblig)
    cash_sweep = min(cash_sweep, saldo_deuda_ds - amort_oblig)
    
    amort_total = amort_oblig + cash_sweep
    saldo_deuda_ds -= amort_total
    
    remanente = max(0, fcf_post_int - amort_total)
    flujos_sponsor_ds.append(remanente)
    
    print(f"{t + 1:>5} {saldo_inicial_t:>10.1f} {intereses_t:>8.1f} {amort_oblig:>12.1f} {cash_sweep:>11.1f} {amort_total:>12.1f} {saldo_deuda_ds:>10.1f}")

equity_salida_ds = ebitda_salida * multiplo_salida - saldo_deuda_ds
flujos_ds = [-equity_inicial] + flujos_sponsor_ds + [equity_salida_ds]
tir_ds = newton(lambda r: sum(f / (1 + r) ** t for t, f in enumerate(flujos_ds)), 0.15)
moic_ds = (sum(flujos_sponsor_ds) + equity_salida_ds) / equity_inicial

print(f"\nIRR con debt schedule: {tir_ds:.1%}")
print(f"MOIC con debt schedule: {moic_ds:.2f}x")


# ============================================================
# Ejercicio 3: Sensibilidad 3x3 — Multiplos Entrada vs Salida
# ============================================================
print("\n=== Ejercicio 3: Sensibilidad 3x3 ===")
multiplos_entrada = [7.0, 8.0, 9.0]
multiplos_salida = [7.0, 8.0, 9.0]

def lbo_simple(ebitda_0, mult_entrada, mult_salida, deuda_pct_lbo=0.60,
               crecimiento=0.06, tasa_deuda_lbo=0.05, anios=5):
    """LBO simplificado para sensibilidad."""
    precio = ebitda_0 * mult_entrada
    deuda = precio * deuda_pct_lbo
    equity = precio * (1 - deuda_pct_lbo)
    
    # EBITDA crece anualmente
    ebitda_final = ebitda_0 * (1 + crecimiento) ** anios
    
    # Deuda remanente: se paga con FCF (asumimos 50% del EBITDA disponible)
    fcf_acum = ebitda_0 * sum((1 + crecimiento) ** t for t in range(1, anios + 1)) * 0.15
    deuda_rem = max(deuda - fcf_acum, 0)
    
    ev_salida = ebitda_final * mult_salida
    equity_salida = ev_salida - deuda_rem
    
    flujos = [-equity] + [0] * (anios - 1) + [equity_salida]
    tir = newton(lambda r: sum(f / (1 + r) ** t for t, f in enumerate(flujos)), 0.15)
    
    return tir

print("=== Sensibilidad IRR: Entrada x Salida ===")
print(f"{'':>12} {'Salida 7x':>10} {'Salida 8x':>10} {'Salida 9x':>10}")
print("-" * 44)
for mult_ent in multiplos_entrada:
    fila = f"Entrada {mult_ent:.0f}x "
    for mult_sal in multiplos_salida:
        irr_val = lbo_simple(ebitda_inicial, mult_ent, mult_sal)
        fila += f" {irr_val:>9.1%}"
    print(fila)

print("\nEscenarios con IRR < 15%:")
irr_bajo = []
for mult_ent in multiplos_entrada:
    for mult_sal in multiplos_salida:
        irr_val = lbo_simple(ebitda_inicial, mult_ent, mult_sal)
        if irr_val < 0.15:
            irr_bajo.append((mult_ent, mult_sal, irr_val))
            print(f"  - Entrada {mult_ent:.0f}x con Salida {mult_sal:.0f}x: {irr_val:.1%}")

print("\nConclusion: Comprar a 9x EBITDA es arriesgado, solo genera")
print("retorno aceptable si la salida es >= 9x (multiple expansion).")


# ============================================================
# Ejercicio 4: Estructura de Deuda en Capas
# ============================================================
print("\n=== Ejercicio 4: Estructura de Deuda en Capas ===")
deuda_senior_x = 4.0
tasa_senior = 0.05
deuda_sub_x = 2.0
tasa_sub = 0.09

deuda_senior = ebitda_inicial * deuda_senior_x
deuda_sub = ebitda_inicial * deuda_sub_x
equity_sponsor = ebitda_inicial * multiplo_entrada - deuda_senior - deuda_sub

print(f"Deuda Senior: ${deuda_senior:.1f}M ({tasa_senior:.1%}) | "
      f"Subordinada: ${deuda_sub:.1f}M ({tasa_sub:.1%})")
print(f"Equity Sponsor: ${equity_sponsor:.1f}M ({equity_sponsor/(ebitda_inicial*multiplo_entrada):.0%})")

saldo_senior = deuda_senior
saldo_sub = deuda_sub
fcf_sponsor_capas = []

print(f"\n{'Anio':>5} {'Saldo_Senior':>13} {'Saldo_Sub':>10} {'FCF_Sponsor':>12}")
print("-" * 42)
for t in range(anios_proyeccion):
    int_senior = saldo_senior * tasa_senior
    int_sub = saldo_sub * tasa_sub
    
    ebt_anio = ebit_arr[t] - int_senior - int_sub
    impuestos = max(0, ebt_anio * tasa_impositiva)
    utilidad_neta = ebt_anio - impuestos
    
    capex = ingresos_arr[t] * capex_pct
    wc_val = ingresos_arr[t] * wc_pct
    delta_wc = wc_val - (ingresos_arr[t - 1] * wc_pct if t > 0 else ingreso_inicial * wc_pct)
    fcf = utilidad_neta + depreciacion_arr[t] - capex - delta_wc
    
    # Calcular exceso de caja despues de servir deuda senior
    fcf_despues_senior = fcf - int_senior
    if fcf_despues_senior > 0:
        pago_senior = min(fcf_despues_senior, saldo_senior)
        saldo_senior -= pago_senior
        fcf_despues_senior -= pago_senior
    else:
        pago_senior = 0
    
    # Pagar subordinada con lo que sobra
    if fcf_despues_senior > 0:
        pago_sub = min(fcf_despues_senior, saldo_sub)
        saldo_sub -= pago_sub
        fcf_despues_senior -= pago_sub
    else:
        pago_sub = 0
    
    fcf_sponsor_capas.append(max(0, fcf_despues_senior))
    print(f"{t + 1:>5} {saldo_senior:>13.1f} {saldo_sub:>10.1f} {fcf_sponsor_capas[-1]:>12.1f}")

equity_salida_capas = ebitda_salida * multiplo_salida - saldo_senior - saldo_sub
flujos_capas = [-equity_sponsor] + fcf_sponsor_capas + [equity_salida_capas]
tir_capas = newton(lambda r: sum(f / (1 + r) ** t for t, f in enumerate(flujos_capas)), 0.15)
moic_capas = (sum(fcf_sponsor_capas) + equity_salida_capas) / equity_sponsor

print(f"\nEquity salida: ${equity_salida_capas:.1f}M | FCF acumulado sponsor: ${sum(fcf_sponsor_capas):.1f}M")
print(f"IRR: {tir_capas:.1%} | MOIC: {moic_capas:.2f}x")

print("\nComparacion:")
print(f"  LBO 1 capa (60% deuda):  IRR {tir_result:.1%}, MOIC {moic_result:.2f}x")
print(f"  LBO 2 capas (75% deuda): IRR {tir_capas:.1%}, MOIC {moic_capas:.2f}x")
print("\nMayor apalancamiento aumenta retorno pero tambien riesgo de default.")


# ============================================================
# Ejercicio 5: Sensibilidad Avanzada 5x5
# ============================================================
print("\n=== Ejercicio 5: Sensibilidad Avanzada 5x5 ===")
crecimientos_ebitda = [-0.02, 0.00, 0.02, 0.04, 0.06]
multiplos_salida_5 = [6.0, 7.0, 8.0, 9.0, 10.0]

def lbo_capas_sens(ebitda_0, crecimiento_eb, mult_salida):
    """LBO 2 capas para sensibilidad."""
    mult_entrada_lbo = 8.0
    precio = ebitda_0 * mult_entrada_lbo
    d_senior = ebitda_0 * 4.0
    d_sub = ebitda_0 * 2.0
    equity = precio - d_senior - d_sub
    
    ebitda_f = ebitda_0 * (1 + crecimiento_eb) ** 5
    ev_s = ebitda_f * mult_salida
    
    # Deuda remanente aprox (50% pagada)
    deuda_rem_senior = d_senior * 0.4
    deuda_rem_sub = d_sub * 0.7
    
    eq_s = ev_s - deuda_rem_senior - deuda_rem_sub
    flujos = [-equity, 0, 0, 0, 0, eq_s]
    
    try:
        return newton(lambda r: sum(f / (1 + r) ** t for t, f in enumerate(flujos)), 0.15)
    except:
        return -0.10

irr_matriz = np.zeros((len(crecimientos_ebitda), len(multiplos_salida_5)))

for i, crec in enumerate(crecimientos_ebitda):
    for j, mult_s in enumerate(multiplos_salida_5):
        irr_matriz[i, j] = lbo_capas_sens(ebitda_inicial, crec, mult_s)

print("=== Sensibilidad Avanzada: IRR por Crecimiento y Exit Multiple ===")
header = f"{'Crec\\Exit':<12}" + "".join([f"{f'{ms:.0f}x':>8}" for ms in multiplos_salida_5])
print(header)
print("-" * len(header))
for i, crec in enumerate(crecimientos_ebitda):
    fila = f"  {crec:+.0%}     "
    for j, ms in enumerate(multiplos_salida_5):
        marca = "*" if irr_matriz[i, j] > 0.25 else " "
        fila += f" {irr_matriz[i, j]:>6.1%}{marca}"
    print(fila)

print("\n* IRR > 25% (target agresivo PE)")
print("\nConclusion: Para alcanzar IRR > 25% se requiere:")
print("  - Crecimiento >= 2% + Exit Multiple >= 9x, o")
print("  - Crecimiento >= 4% + Exit Multiple >= 8x, o")
print("  - Crecimiento >= 6% + Exit Multiple >= 7x")
