# ✅ Soluciones: U26 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U26_soluciones)

---

```python
# U26: SOLUCIONES — Valoracion de Empresas: DCF y Comparables

import numpy as np
import pandas as pd

# ============================================================
# Ejercicio 1: DCF Completo — MegaCorp S.A.
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

anios = 5
ingresos = np.zeros(anios)
ingresos[0] = ingreso_inicial * (1 + tasas_crecimiento[0])
for t in range(1, anios):
    ingresos[t] = ingresos[t - 1] * (1 + tasas_crecimiento[t])

ebitda = ingresos * margen_ebitda
depreciacion = ingresos * depreciacion_pct
ebit = ebitda - depreciacion
nopat = ebit * (1 - tasa_impositiva)
capex = ingresos * capex_pct
wc = ingresos * wc_pct
delta_wc = np.diff(wc, prepend=ingreso_inicial * wc_pct)
fcff = nopat + depreciacion - capex - delta_wc

# Valor terminal
valor_terminal = fcff[-1] * (1 + crecimiento_perpetuo) / (wacc_val - crecimiento_perpetuo)

# Enterprise Value
ev = sum(fcff[t] / (1 + wacc_val) ** (t + 1) for t in range(anios))
ev += valor_terminal / (1 + wacc_val) ** anios

equity_value = ev - deuda_neta
precio_implicito = equity_value / acciones

print("=== Proyeccion de Flujos ===")
print(f"{'Anio':>5} {'Ingresos':>10} {'EBITDA':>10} {'NOPAT':>10} {'CAPEX':>10} {'Delta_WC':>10} {'FCFF':>10}")
print("-" * 67)
for t in range(anios):
    print(f"{t+1:>5} {ingresos[t]:>10,.1f} {ebitda[t]:>10,.1f} {nopat[t]:>10,.1f} "
          f"{capex[t]:>10,.1f} {delta_wc[t]:>10,.1f} {fcff[t]:>10,.1f}")

print(f"\\nValor Terminal (Gordon): ${valor_terminal:,.1f}M")
print(f"Enterprise Value: ${ev:,.1f}M")
print(f"Equity Value: ${equity_value:,.1f}M")
print(f"Precio Implicito por Accion: ${precio_implicito:,.2f}")


# ============================================================
# Ejercicio 2: Tabla de Sensibilidad (9x9)
# ============================================================
print("\\n=== Ejercicio 2: Tabla de Sensibilidad ===")

wacc_rango = np.linspace(0.07, 0.11, 9)
crecimiento_rango = np.linspace(0.01, 0.05, 9)

precios_matriz = np.zeros((len(wacc_rango), len(crecimiento_rango)))

for i, w in enumerate(wacc_rango):
    for j, g in enumerate(crecimiento_rango):
        vt = fcff[-1] * (1 + g) / (w - g) if w > g else np.inf
        ev_ij = sum(fcff[t] / (1 + w) ** (t + 1) for t in range(anios))
        if w > g:
            ev_ij += vt / (1 + w) ** anios
        eq_ij = ev_ij - deuda_neta
        precios_matriz[i, j] = eq_ij / acciones

print("\\n=== Tabla de Sensibilidad: Precio Implicito por Accion ===")
header = "WACC\\\\g    " + "".join([f"  g={g:.1%}" for g in crecimiento_rango])
print(header)
print("-" * len(header))
for i, w in enumerate(wacc_rango):
    fila = f"WACC={w:.1%} "
    for j, g in enumerate(crecimiento_rango):
        fila += f" {precios_matriz[i, j]:>7.2f}"
    print(fila)

precio_base = precios_matriz[3, 2]  # WACC=8.5%, g=2.0%
print(f"\\nPrecio en escenario base (WACC=8.5%, g=2.0%): ${precio_base:,.2f}")
print(f"Rango de precios: ${np.min(precios_matriz):,.2f} - ${np.max(precios_matriz):,.2f}")


# ============================================================
# Ejercicio 3: CAPM y WACC Desglosado
# ============================================================
print("\\n=== Ejercicio 3: CAPM y WACC Desglosado ===")
rf = 0.04
beta_val = 1.2
prima_mercado = 0.055
kd = 0.035
d_sobre_v = 0.25
e_sobre_v = 1 - d_sobre_v
tasa_imp = 0.21

ke = rf + beta_val * prima_mercado
wacc_capm = e_sobre_v * ke + d_sobre_v * kd * (1 - tasa_imp)

print(f"Ke (CAPM) = Rf + beta * (Rm - Rf) = {rf:.1%} + {beta_val} * {prima_mercado:.1%} = {ke:.2%}")
print(f"WACC = (E/V)*Ke + (D/V)*Kd*(1-t)")
print(f"     = {e_sobre_v:.2f} * {ke:.2%} + {d_sobre_v:.2f} * {kd:.1%} * {1 - tasa_imp:.2f}")
print(f"     = {e_sobre_v * ke:.2%} + {d_sobre_v * kd * (1 - tasa_imp):.2%} = {wacc_capm:.2%}")

# Recalcular DCF con WACC CAPM
ev_capm = sum(fcff[t] / (1 + wacc_capm) ** (t + 1) for t in range(anios))
vt_capm = fcff[-1] * (1 + crecimiento_perpetuo) / (wacc_capm - crecimiento_perpetuo)
ev_capm += vt_capm / (1 + wacc_capm) ** anios
eq_capm = ev_capm - deuda_neta
precio_capm = eq_capm / acciones

print(f"\\n=== DCF con WACC CAPM ===")
print(f"Enterprise Value: ${ev_capm:,.1f}M")
print(f"Precio Implicito: ${precio_capm:,.2f}")
print(f"Diferencia vs WACC 8.5%: ${precio_capm - precio_implicito:,.2f} ({(precio_capm/precio_implicito - 1) * 100:+.1f}%)")


# ============================================================
# Ejercicio 4: Valor Terminal — Gordon vs Exit Multiple
# ============================================================
print("\\n=== Ejercicio 4: Valor Terminal — Gordon vs Exit Multiple ===")

vt_gordon = fcff[-1] * (1 + crecimiento_perpetuo) / (wacc_val - crecimiento_perpetuo)
vt_exit_multiple = ebitda[-1] * 12

# Crecimiento perpetuo implicito
# VT = EBITDA * Multiple = FCFF * (1+g) / (WACC - g)
# Despejando g implicito
fcf_final = fcff[-1]
ebitda_final = ebitda[-1]
g_implicito = (ebitda_final * 12 * wacc_val - fcf_final) / (ebitda_final * 12 + fcf_final)

print("=== Comparacion Valor Terminal ===")
print(f"Gordon Growth (g={crecimiento_perpetuo:.1%}): ${vt_gordon:,.1f}M")
print(f"Exit Multiple (12x EBITDA): ${vt_exit_multiple:,.1f}M")
print(f"Diferencia: ${vt_exit_multiple - vt_gordon:,.1f}M (Exit Multiple es {(vt_exit_multiple/vt_gordon - 1)*100:.0f}% mayor)")

print(f"\\nCrecimiento perpetuo implicito en el exit multiple de 12x:")
print(f"g_implicito: {g_implicito:.1%}")
print(f"\\nEl Exit Multiple a 12x implica un crecimiento perpetuo")
print(f"de {g_implicito:.1%}, mucho mas agresivo que el {crecimiento_perpetuo:.1%} de Gordon.")
print(f"En la practica, se triangulan ambos metodos.")


# ============================================================
# Ejercicio 5: DCF con Analisis de Escenarios
# ============================================================
print("\\n=== Ejercicio 5: DCF con Analisis de Escenarios ===")

def dcf_escenario(tasas_crec, wacc, g_perp, deuda, acciones_val):
    """Ejecuta un DCF completo y retorna precio implicito."""
    ingresos_val = np.zeros(anios)
    ingresos_val[0] = ingreso_inicial * (1 + tasas_crec[0])
    for t in range(1, anios):
        ingresos_val[t] = ingresos_val[t - 1] * (1 + tasas_crec[t])
    
    ebitda_val = ingresos_val * margen_ebitda
    ebit_val = ebitda_val - ingresos_val * depreciacion_pct
    nopat_val = ebit_val * (1 - tasa_impositiva)
    capex_val = ingresos_val * capex_pct
    wc_val = ingresos_val * wc_pct
    delta_wc_val = np.diff(wc_val, prepend=ingreso_inicial * wc_pct)
    fcff_val = nopat_val + ingresos_val * depreciacion_pct - capex_val - delta_wc_val
    
    vt_val = fcff_val[-1] * (1 + g_perp) / (wacc - g_perp) if wacc > g_perp else 1e12
    ev_val = sum(fcff_val[t] / (1 + wacc) ** (t + 1) for t in range(anios))
    ev_val += vt_val / (1 + wacc) ** anios
    
    eq_val = ev_val - deuda
    return eq_val / acciones_val

tasas_base = tasas_crecimiento.copy()
tasas_bull = [t + 0.03 for t in tasas_base]
tasas_bear = [max(t - 0.03, 0.005) for t in tasas_base]

precio_bull = dcf_escenario(tasas_bull, wacc_val - 0.01, crecimiento_perpetuo + 0.005, deuda_neta, acciones)
precio_base_dcf = dcf_escenario(tasas_base, wacc_val, crecimiento_perpetuo, deuda_neta, acciones)
precio_bear = dcf_escenario(tasas_bear, wacc_val + 0.01, max(crecimiento_perpetuo - 0.005, 0.005), deuda_neta, acciones)

print("=== Analisis de Escenarios ===")
print(f"{'Escenario':<12} {'Precio':>16} {'vs Base':>10}")
print("-" * 40)
print(f"{'Bull':<12} ${precio_bull:>14,.2f} {((precio_bull/precio_base_dcf - 1)*100):>+9.1f}%")
print(f"{'Base':<12} ${precio_base_dcf:>14,.2f} {'0.0%':>10}")
print(f"{'Bear':<12} ${precio_bear:>14,.2f} {((precio_bear/precio_base_dcf - 1)*100):>+9.1f}%")
print(f"\\nRango: ${precio_bear:,.2f} - ${precio_bull:,.2f}")
print("Football Field: Bear - | -- Base -- | -- Bull")
print("Conclusion: Alta sensibilidad a supuestos. Triangulacion")
print("con comparables necesaria para validar valoracion.")
```

---

> [📥 Descargar archivo .py](U26_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
