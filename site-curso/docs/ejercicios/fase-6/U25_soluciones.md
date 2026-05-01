# ✅ Soluciones: U25 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U25_soluciones)

---

```python
# U25: SOLUCIONES — Analisis de Estados Financieros con Python

import pandas as pd
import numpy as np

# Datos compartidos para todos los ejercicios
datos_empresas = {
    'AAPL': {
        'ingresos': 383285, 'costo_ventas': 214137, 'gastos_operativos': 54847,
        'depreciacion': 11500, 'intereses': 3933, 'impuestos': 19736,
        'activos_corrientes': 143566, 'activos_totales': 352583,
        'pasivos_corrientes': 145308, 'pasivos_totales': 290437,
        'patrimonio': 62146, 'efectivo': 29965, 'inventarios': 6331,
        'cuentas_por_cobrar': 60085, 'cuentas_por_pagar': 62611,
        'utilidades_retenidas': 5142,
        'precio_accion': 185.0, 'acciones_en_circulacion': 15500,
        'valor_mercado': 2867500, 'dividendo_anual': 0.96
    },
    'TSLA': {
        'ingresos': 81462, 'costo_ventas': 65636, 'gastos_operativos': 9355,
        'depreciacion': 3421, 'intereses': 356, 'impuestos': 539,
        'activos_corrientes': 37551, 'activos_totales': 82338,
        'pasivos_corrientes': 26709, 'pasivos_totales': 36440,
        'patrimonio': 45898, 'efectivo': 16398, 'inventarios': 9620,
        'cuentas_por_cobrar': 2900, 'cuentas_por_pagar': 11245,
        'utilidades_retenidas': 18792,
        'precio_accion': 240.0, 'acciones_en_circulacion': 3169,
        'valor_mercado': 760560, 'dividendo_anual': 0.0
    },
    'JPM': {
        'ingresos': 154872, 'costo_ventas': 0, 'gastos_operativos': 93500,
        'depreciacion': 0, 'intereses': 0, 'impuestos': 12274,
        'activos_corrientes': 0, 'activos_totales': 3665743,
        'pasivos_corrientes': 0, 'pasivos_totales': 3585625,
        'patrimonio': 80118, 'efectivo': 52000, 'inventarios': 0,
        'cuentas_por_cobrar': 0, 'cuentas_por_pagar': 0,
        'utilidades_retenidas': 35000,
        'precio_accion': 175.0, 'acciones_en_circulacion': 2900,
        'valor_mercado': 507500, 'dividendo_anual': 4.00
    }
}


# ============================================================
# Ejercicio 1: Calculadora de 30 Ratios
# ============================================================
print("=== Ejercicio 1: Calculadora de 30 Ratios ===")

def calcular_todos_ratios(nombre, d):
    """Calcula 30+ ratios financieros para una empresa."""
    ingresos = d['ingresos']
    costo_ventas = d['costo_ventas']
    gastos_operativos = d['gastos_operativos']
    depreciacion = d['depreciacion']
    intereses = d['intereses']
    impuestos = d['impuestos']
    activos_corrientes = d['activos_corrientes']
    activos_totales = d['activos_totales']
    pasivos_corrientes = d['pasivos_corrientes']
    pasivos_totales = d['pasivos_totales']
    patrimonio = d['patrimonio']
    efectivo = d['efectivo']
    inventarios = d['inventarios']
    cxc = d['cuentas_por_cobrar']
    cxp = d['cuentas_por_pagar']
    precio = d['precio_accion']
    acciones = d['acciones_en_circulacion']
    valor_mercado = d['valor_mercado']
    dividendo = d['dividendo_anual']

    utilidad_bruta = ingresos - costo_ventas
    ebitda = utilidad_bruta - gastos_operativos
    ebit = ebitda - depreciacion
    ebt = ebit - intereses
    utilidad_neta = ebt - impuestos
    upa = utilidad_neta / acciones if acciones > 0 else 0
    valor_libro_accion = patrimonio / acciones if acciones > 0 else 0
    deuda_total = pasivos_totales
    
    ratios = {}
    
    # Rentabilidad
    ratios['margen_bruto'] = utilidad_bruta / ingresos * 100 if ingresos > 0 else np.nan
    ratios['margen_ebitda'] = ebitda / ingresos * 100 if ingresos > 0 else np.nan
    ratios['margen_operativo'] = ebit / ingresos * 100 if ingresos > 0 else np.nan
    ratios['margen_neto'] = utilidad_neta / ingresos * 100 if ingresos > 0 else np.nan
    ratios['roa'] = utilidad_neta / activos_totales * 100 if activos_totales > 0 else np.nan
    ratios['roe'] = utilidad_neta / patrimonio * 100 if patrimonio > 0 else np.nan
    nopat = ebit * 0.79  # Asumiendo tasa 21%
    capital_invertido = activos_totales - pasivos_corrientes
    ratios['roic'] = nopat / capital_invertido * 100 if capital_invertido > 0 else np.nan
    
    # Liquidez
    ratios['razon_corriente'] = activos_corrientes / pasivos_corrientes if pasivos_corrientes > 0 else np.nan
    ratios['prueba_acida'] = (activos_corrientes - inventarios) / pasivos_corrientes if pasivos_corrientes > 0 else np.nan
    ratios['razon_efectivo'] = efectivo / pasivos_corrientes if pasivos_corrientes > 0 else np.nan
    
    # Solvencia
    ratios['deuda_patrimonio'] = deuda_total / patrimonio if patrimonio > 0 else np.nan
    ratios['deuda_ebitda'] = deuda_total / ebitda if ebitda > 0 else np.nan
    ratios['deuda_activos'] = deuda_total / activos_totales if activos_totales > 0 else np.nan
    ratios['cobertura_intereses'] = ebit / intereses if intereses > 0 else np.nan
    
    # Eficiencia
    ratios['rotacion_activos'] = ingresos / activos_totales if activos_totales > 0 else np.nan
    if costo_ventas > 0 and inventarios > 0:
        ratios['rotacion_inventario'] = costo_ventas / inventarios
        ratios['dias_inventario'] = 365 / ratios['rotacion_inventario']
    else:
        ratios['rotacion_inventario'] = np.nan
        ratios['dias_inventario'] = np.nan
    ingresos_diarios = ingresos / 365
    ratios['dias_cobro'] = cxc / ingresos_diarios if ingresos_diarios > 0 and cxc > 0 else np.nan
    ratios['dias_pago'] = cxp / ingresos_diarios if ingresos_diarios > 0 and cxp > 0 else np.nan
    
    # Valoracion
    ratios['per'] = precio / upa if upa > 0 else np.nan
    ratios['precio_valor_libro'] = precio / valor_libro_accion if valor_libro_accion > 0 else np.nan
    ev = valor_mercado + deuda_total - efectivo
    ratios['ev_ebitda'] = ev / ebitda if ebitda > 0 else np.nan
    ratios['ev_ingresos'] = ev / ingresos if ingresos > 0 else np.nan
    ratios['rentabilidad_dividendo'] = dividendo / precio * 100 if precio > 0 else 0
    ratios['payout_ratio'] = dividendo / upa * 100 if upa > 0 else 0
    fcf_aprox = ebitda - depreciacion - (0.08 * ingresos)
    ratios['fcf_yield'] = fcf_aprox / valor_mercado * 100 if valor_mercado > 0 else np.nan
    
    return ratios

resultados_ratios = {}
for nombre, datos in datos_empresas.items():
    resultados_ratios[nombre] = calcular_todos_ratios(nombre, datos)

df_ratios = pd.DataFrame(resultados_ratios)
print("\\n=== Ratios Financieros ===")
print(f"{'Ratio':<30} {'AAPL':>10} {'TSLA':>10} {'JPM':>10}")
print("-" * 63)
for ratio in df_ratios.index:
    valores = []
    for empresa in ['AAPL', 'TSLA', 'JPM']:
        v = df_ratios.loc[ratio, empresa]
        if pd.isna(v):
            valores.append('N/A')
        elif ratio == 'per' or ratio == 'precio_valor_libro' or ratio == 'ev_ebitda' or ratio == 'ev_ingresos':
            valores.append(f"{v:>8.1f}x")
        elif 'margen' in ratio or 'roa' in ratio or 'roe' in ratio or 'roic' in ratio or '_pct' in ratio or 'yield' in ratio or 'rentabilidad' in ratio or 'payout' in ratio:
            valores.append(f"{v:>8.2f}%")
        elif 'razon' in ratio or 'prueba' in ratio or 'deuda_' in ratio or 'rotacion' in ratio or 'cobertura' in ratio:
            valores.append(f"{v:>8.2f}")
        else:
            valores.append(f"{v:>8.1f}")
    print(f"{ratio:<30} {' '.join(valores)}")


# ============================================================
# Ejercicio 2: Analisis DuPont (3 y 5 componentes)
# ============================================================
print("\\n=== Ejercicio 2: Analisis DuPont ===")

for nombre, d in datos_empresas.items():
    ingresos = d['ingresos']
    costo_ventas = d['costo_ventas']
    gastos_operativos = d['gastos_operativos']
    depreciacion = d['depreciacion']
    intereses = d['intereses']
    impuestos = d['impuestos']
    activos_totales = d['activos_totales']
    patrimonio = d['patrimonio']

    utilidad_bruta = ingresos - costo_ventas
    ebitda = utilidad_bruta - gastos_operativos
    ebit = ebitda - depreciacion
    ebt = ebit - intereses
    utilidad_neta = ebt - impuestos

    margen_neto = utilidad_neta / ingresos if ingresos > 0 else 0
    rotacion_activos = ingresos / activos_totales if activos_totales > 0 else 0
    multiplicador_patrimonio = activos_totales / patrimonio if patrimonio > 0 else 0
    roe_dupont3 = margen_neto * rotacion_activos * multiplicador_patrimonio * 100

    carga_impositiva = utilidad_neta / ebt if ebt != 0 else np.nan
    carga_intereses = ebt / ebit if ebit != 0 else np.nan
    margen_operativo = ebit / ingresos if ingresos > 0 else np.nan
    roe_dupont5 = carga_impositiva * carga_intereses * margen_operativo * rotacion_activos * multiplicador_patrimonio * 100

    print(f"\\n{nombre}:")
    print(f"  DuPont 3: MN={margen_neto:.2%} x RA={rotacion_activos:.3f} x EM={multiplicador_patrimonio:.2f} = ROE={roe_dupont3:.1f}%")
    if not np.isnan(carga_impositiva) and not np.isnan(carga_intereses) and not np.isnan(margen_operativo):
        print(f"  DuPont 5: CI={carga_impositiva:.3f} x CInt={carga_intereses:.3f} x MO={margen_operativo:.3f} x RA={rotacion_activos:.3f} x EM={multiplicador_patrimonio:.2f} = ROE={roe_dupont5:.1f}%")

print("\\nConclusion:")
print("  AAPL: ROE elevado por alto margen operativo + leverage")
print("  TSLA: ROE bajo por margenes comprimidos, poco leverage")
print("  JPM:  ROE elevado casi exclusivamente por apalancamiento extremo")


# ============================================================
# Ejercicio 3: Altman Z-Score
# ============================================================
print("\\n=== Ejercicio 3: Altman Z-Score ===")

def altman_zscore(d):
    activos_corrientes = d['activos_corrientes']
    pasivos_corrientes = d['pasivos_corrientes']
    activos_totales = d['activos_totales']
    ingresos = d['ingresos']
    pasivos_totales = d['pasivos_totales']
    utilidades_retenidas = d['utilidades_retenidas']
    valor_mercado = d['valor_mercado']
    
    costo_ventas = d['costo_ventas']
    gastos_operativos = d['gastos_operativos']
    depreciacion = d['depreciacion']
    ebit = (ingresos - costo_ventas - gastos_operativos - depreciacion)
    
    capital_trabajo = activos_corrientes - pasivos_corrientes
    
    x1 = capital_trabajo / activos_totales if activos_totales > 0 else 0
    x2 = utilidades_retenidas / activos_totales if activos_totales > 0 else 0
    x3 = ebit / activos_totales if activos_totales > 0 else 0
    x4 = valor_mercado / pasivos_totales if pasivos_totales > 0 else 0
    x5 = ingresos / activos_totales if activos_totales > 0 else 0
    
    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
    
    if z > 2.99:
        interpretacion = 'Zona Segura'
    elif z >= 1.81:
        interpretacion = 'Zona Gris'
    else:
        interpretacion = 'Zona de Peligro'
    
    return z, x1, x2, x3, x4, x5, interpretacion

print(f"{'Empresa':<8} {'Z-Score':>8} {'Interpretacion':<20}")
print("-" * 38)
for nombre, d in datos_empresas.items():
    z, x1, x2, x3, x4, x5, interp = altman_zscore(d)
    if nombre == 'JPM':
        print(f"{nombre:<8} {'N/A':>8} {'No aplica (banco)':<20}")
    else:
        print(f"{nombre:<8} {z:>8.2f} {interp:<20}")


# ============================================================
# Ejercicio 4: Analisis Horizontal y Vertical
# ============================================================
print("\\n=== Ejercicio 4: Analisis Horizontal y Vertical ===")

ingresos_aapl_2022 = 394328
ingresos_aapl_2023 = 383285

d = datos_empresas['AAPL']
ingresos_23 = d['ingresos']
costo_ventas = d['costo_ventas']
gastos_operativos = d['gastos_operativos']
depreciacion = d['depreciacion']
intereses = d['intereses']
impuestos = d['impuestos']

utilidad_bruta = ingresos_23 - costo_ventas
ebitda = utilidad_bruta - gastos_operativos
ebit = ebitda - depreciacion
ebt = ebit - intereses
utilidad_neta = ebt - impuestos

print("=== Analisis Vertical AAPL FY2023 ===")
print(f"{'Concepto':<25} {'% Ingresos':>10}")
print("-" * 37)
print(f"{'Ingresos':<25} {100.0:>10.1f}%")
print(f"{'Costo Ventas':<25} {costo_ventas/ingresos_23*100:>10.1f}%")
print(f"{'Utilidad Bruta':<25} {utilidad_bruta/ingresos_23*100:>10.1f}%")
print(f"{'Gastos Operativos':<25} {gastos_operativos/ingresos_23*100:>10.1f}%")
print(f"{'EBITDA':<25} {ebitda/ingresos_23*100:>10.1f}%")
print(f"{'EBIT':<25} {ebit/ingresos_23*100:>10.1f}%")
print(f"{'Utilidad Neta':<25} {utilidad_neta/ingresos_23*100:>10.1f}%")

crecimiento = (ingresos_aapl_2023 - ingresos_aapl_2022) / ingresos_aapl_2022 * 100
print(f"\\n=== Analisis Horizontal AAPL ===")
print(f"Ingresos 2022: ${ingresos_aapl_2022:,}M")
print(f"Ingresos 2023: ${ingresos_aapl_2023:,}M")
print(f"Crecimiento: {crecimiento:+.1f}%")


# ============================================================
# Ejercicio 5: Equity Research Summary
# ============================================================
print("\\n=== Ejercicio 5: Equity Research Summary ===")

def resumen_empresa(nombre, d):
    ratios = calcular_todos_ratios(nombre, d)
    z, x1, x2, x3, x4, x5, interp = altman_zscore(d)
    
    ingresos = d['ingresos']
    costo_ventas = d['costo_ventas']
    gastos_operativos = d['gastos_operativos']
    depreciacion = d['depreciacion']
    intereses = d['intereses']
    impuestos = d['impuestos']
    activos_totales = d['activos_totales']
    patrimonio = d['patrimonio']
    
    utilidad_bruta = ingresos - costo_ventas
    ebitda_val = utilidad_bruta - gastos_operativos
    ebit_val = ebitda_val - depreciacion
    ebt_val = ebit_val - intereses
    utilidad_neta = ebt_val - impuestos
    
    margen_neto = utilidad_neta / ingresos if ingresos > 0 else 0
    rotacion_activos = ingresos / activos_totales if activos_totales > 0 else 0
    multiplicador = activos_totales / patrimonio if patrimonio > 0 else 0
    
    print(f"\\n{'='*12} EQUITY RESEARCH: {nombre} {'='*12}")
    print("Ratios Clave:")
    print(f"  ROE: {ratios['roe']:.1f}% | ROA: {ratios['roa']:.1f}% | Margen EBITDA: {ratios['margen_ebitda']:.1f}%")
    print(f"  P/E: {ratios['per']:.1f}x | EV/EBITDA: {ratios['ev_ebitda']:.1f}x | Deuda/EBITDA: {ratios['deuda_ebitda']:.1f}x")
    print(f"  Current Ratio: {ratios['razon_corriente']:.1f}x | FCF Yield: {ratios['fcf_yield']:.1f}%")
    print(f"DuPont: MN {margen_neto:.1%} x RA {rotacion_activos:.2f} x EM {multiplicador:.1f} = ROE {ratios['roe']:.1f}%")
    
    if nombre != 'JPM':
        print(f"Z-Score: {z:.1f} ({interp})")
    
    print("\\nConclusion:")
    if nombre == 'AAPL':
        print("  AAPL es una maquina de generacion de efectivo con margenes")
        print("  operativos superiores al 30%. Su ROE excepcional (127%)")
        print("  combina alta rentabilidad con apalancamiento via recompras.")
    elif nombre == 'TSLA':
        print("  TSLA muestra crecimiento en ingresos pero margenes comprimidos")
        print("  por guerra de precios en EVs. Su baja deuda y alto efectivo")
        print("  le dan flexibilidad financiera. Valoracion premium (65x P/E).")
    elif nombre == 'JPM':
        print("  JPM opera con apalancamiento extremo (44x Deuda/Patrimonio)")
        print("  tipico de la banca. Su ROE de 61% proviene del multiplicador,")
        print("  no de eficiencia operativa. Sensible a ciclo de credito.")

resumen_empresa('AAPL', datos_empresas['AAPL'])
resumen_empresa('TSLA', datos_empresas['TSLA'])
resumen_empresa('JPM', datos_empresas['JPM'])
```

---

> [📥 Descargar archivo .py](U25_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
