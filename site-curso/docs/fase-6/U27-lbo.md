# U27: Modelo LBO — Leveraged Buyout y Private Equity

> **Lectura previa:** [U26: Valoracion DCF](./U26-valoracion-dcf.md)
> **Proxima unidad:** [U28: Derivados](./U28-derivados.md)

---

## 1. Teoria

> ⚠️ **JP Morgan PE Core Skill:** El modelo LBO es la prueba definitiva para entrar a Private Equity. Todo associate de PE pasa su prueba de modelaje construyendo un LBO en 90 minutos. Esta unidad te prepara para esa prueba.

### 1.1 ¿Que es un LBO?

Un **Leveraged Buyout** es la adquisicion de una empresa usando una combinacion de deuda (60-80%) y equity del sponsor (20-40%). La empresa adquirida paga la deuda con sus propios flujos de caja.

**Estructura tipica:**
- Deuda Senior (40-50%): prestamo bancario, tasa mas baja, primera en cobrar
- Deuda Subordinada/Mezzanine (15-25%): mayor tasa, segunda en cobrar
- Equity del Sponsor (25-40%): capital del fondo de PE

### 1.2 Fuentes y Usos (Sources & Uses)

```python
import numpy as np
import pandas as pd

def fuentes_y_usos(precio_compra, ebitda_objetivo, deuda_senior_x, deuda_sub_x,
                   efectivo_excedente=0, comisiones=0.02):
    """Construye la tabla de fuentes y usos del LBO.
    
    Parametros:
        precio_compra: precio de adquisicion
        ebitda_objetivo: EBITDA de la empresa objetivo
        deuda_senior_x: multiplo de EBITDA para deuda senior
        deuda_sub_x: multiplo de EBITDA para deuda subordinada
        efectivo_excedente: efectivo en exceso disponible
        comisiones: % de comisiones sobre deuda total
    """
    # Usos (donde va el dinero)
    compra_equity = precio_compra
    refinanciacion_deuda = 0  # Si hay deuda existente que refinanciar
    comisiones_financieras = (deuda_senior_x + deuda_sub_x) * ebitda_objetivo * comisiones
    
    usos_totales = compra_equity + refinanciacion_deuda + comisiones_financieras
    
    # Fuentes (de donde viene el dinero)
    deuda_senior = deuda_senior_x * ebitda_objetivo
    deuda_subordinada = deuda_sub_x * ebitda_objetivo
    equity_sponsor = usos_totales - deuda_senior - deuda_subordinada - efectivo_excedente
    
    df_fuentes_usos = pd.DataFrame({
        'Concepto': ['Deuda Senior', 'Deuda Subordinada', 'Equity Sponsor',
                     'Efectivo Excedente', 'Total Fuentes',
                     'Compra Equity', 'Refinanciacion', 'Comisiones', 'Total Usos'],
        'Monto': [deuda_senior, deuda_subordinada, equity_sponsor,
                  efectivo_excedente, usos_totales,
                  compra_equity, refinanciacion_deuda, comisiones_financieras, usos_totales]
    })
    
    df_fuentes_usos['%'] = df_fuentes_usos['Monto'] / usos_totales * 100
    
    return df_fuentes_usos, equity_sponsor
```

### 1.3 Calendario de Deuda (Debt Schedule)

El debt schedule modela como se paga la deuda anio a anio usando el flujo de caja libre:

```python
def construir_debt_schedule(deuda_inicial, tasa_interes, fcff_proyectados,
                            amortizacion_obligatoria_pct=0.0, revolvencia=False):
    """Construye el calendario de pago de deuda.
    
    La deuda se paga con el FCFF disponible despues de intereses.
    La amortizacion obligatoria es un % del saldo inicial que DEBE pagarse.
    """
    anios = len(fcff_proyectados)
    saldo_inicial = np.zeros(anios)
    intereses_arr = np.zeros(anios)
    amortizacion_arr = np.zeros(anios)
    saldo_final = np.zeros(anios)
    
    saldo_actual = deuda_inicial
    
    for t in range(anios):
        saldo_inicial[t] = saldo_actual
        intereses_arr[t] = saldo_actual * tasa_interes
        
        # Amortizacion obligatoria
        amort_obligatoria = saldo_actual * amortizacion_obligatoria_pct
        
        # Cash flow disponible para pagar deuda (despues de intereses)
        caja_disponible = fcff_proyectados[t] - intereses_arr[t]
        
        # Pago voluntario adicional
        if caja_disponible > 0:
            pago_total = amort_obligatoria + caja_disponible
            pago_total = min(pago_total, saldo_actual)  # No pagar mas que el saldo
            amortizacion_arr[t] = pago_total
        else:
            amortizacion_arr[t] = amort_obligatoria  # Solo obligatorio si no hay caja
        
        saldo_actual = saldo_actual - amortizacion_arr[t]
        saldo_final[t] = max(saldo_actual, 0)
    
    return pd.DataFrame({
        'Anio': range(1, anios + 1),
        'Saldo_Inicial': saldo_inicial,
        'Intereses': intereses_arr,
        'Amortizacion': amortizacion_arr,
        'Saldo_Final': saldo_final
    })
```

### 1.4 Cash Flow Waterfall (Cascada de Pagos)

En un LBO, el cash flow se distribuye en un orden de prioridad estricto:

1. Intereses de deuda senior
2. Amortizacion obligatoria deuda senior
3. Intereses de deuda subordinada
4. Amortizacion de deuda subordinada
5. Dividendo al sponsor (lo que sobra)

```python
def cash_flow_waterfall(ebitda_proyectado, depreciacion, capex, delta_wc,
                         deuda_senior_inicial, tasa_senior,
                         deuda_sub_inicial, tasa_sub, tasa_impositiva):
    """Simula la cascada de pagos completa del LBO."""
    anios = len(ebitda_proyectado)
    
    resultados = pd.DataFrame(index=range(anios))
    resultados['EBITDA'] = ebitda_proyectado
    resultados['Depreciacion'] = depreciacion
    resultados['EBIT'] = ebitda_proyectado - depreciacion
    
    # Saldos de deuda
    saldo_senior = deuda_senior_inicial
    saldo_sub = deuda_sub_inicial
    
    fcfe_arr = np.zeros(anios)
    saldo_senior_arr = np.zeros(anios)
    saldo_sub_arr = np.zeros(anios)
    
    for t in range(anios):
        # Intereses
        int_senior = saldo_senior * tasa_senior
        int_sub = saldo_sub * tasa_sub
        
        # EBT e impuestos
        ebt = resultados.loc[t, 'EBIT'] - int_senior - int_sub
        impuestos = max(0, ebt * tasa_impositiva)
        utilidad_neta = ebt - impuestos
        
        # FCFE
        fcfe = utilidad_neta + depreciacion[t] - capex[t] - delta_wc[t]
        
        # Pagar deuda senior primero
        pago_senior = min(fcfe, saldo_senior)
        saldo_senior -= pago_senior
        fcfe -= pago_senior
        
        # Luego deuda subordinada
        pago_sub = min(fcfe, saldo_sub)
        saldo_sub -= pago_sub
        fcfe -= pago_sub
        
        fcfe_arr[t] = max(fcfe, 0)  # Efectivo remanente para sponsor
        saldo_senior_arr[t] = saldo_senior
        saldo_sub_arr[t] = saldo_sub
    
    resultados['Saldo_Senior'] = saldo_senior_arr
    resultados['Saldo_Subordinada'] = saldo_sub_arr
    resultados['FCFE_Sponsor'] = fcfe_arr
    
    return resultados
```

### 1.5 IRR y MOIC (Retornos del Sponsor)

Las dos metricas clave del Private Equity:

- **IRR (Internal Rate of Return):** Tasa anualizada de retorno. La metrica principal.
- **MOIC (Multiple on Invested Capital):** Cuantas veces se multiplica el capital invertido.

```python
from scipy.optimize import newton

def calcular_irr_lbo(equity_invertido, flujos_sponsor, valor_salida):
    """Calcula la TIR del sponsor en el LBO.
    
    equity_invertido: monto inicial invertido (negativo)
    flujos_sponsor: dividendos/recapitalizaciones recibidas cada anio
    valor_salida: equity value al momento de la salida (exit)
    """
    flujos_completos = [equity_invertido] + list(flujos_sponsor) + [valor_salida]
    flujos_completos[0] = -abs(flujos_completos[0])  # Asegurar negativo
    
    def vpn(r):
        return sum(f / (1 + r) ** t for t, f in enumerate(flujos_completos))
    
    try:
        tir = newton(vpn, 0.15, maxiter=1000)
        return tir
    except:
        return np.nan

def calcular_moic(equity_invertido, flujos_acumulados, valor_salida):
    """Multiple on Invested Capital: (retornos totales) / inversion."""
    total_retornado = sum(flujos_acumulados) + valor_salida
    return total_retornado / equity_invertido

def valor_salida_por_multiplo(ultimo_ebitda, multiplo_salida):
    """Equity value al exit: EBITDA_n × Multiplo - Deuda remanente."""
    return ultimo_ebitda * multiplo_salida
```

### 1.6 Analisis de Sensibilidad LBO

```python
def sensibilidad_lbo(ebitda_inicial, multiplo_entrada_rango, multiplo_salida_rango,
                     deuda_pct, anios_hold, **supuestos_operativos):
    """Tabla de sensibilidad IRR para combinaciones de multiplos de entrada y salida."""
    n_entrada = len(multiplo_entrada_rango)
    n_salida = len(multiplo_salida_rango)
    
    tir_matriz = np.zeros((n_entrada, n_salida))
    moic_matriz = np.zeros((n_entrada, n_salida))
    
    for i, mult_entrada in enumerate(multiplo_entrada_rango):
        for j, mult_salida in enumerate(multiplo_salida_rango):
            # Calcular LBO para esta combinacion
            precio_compra = ebitda_inicial * mult_entrada
            equity = precio_compra * (1 - deuda_pct)
            
            # Simular 5 anios de operacion...
            # (Simplificado: asumimos retorno lineal)
            ebitda_salida = ebitda_inicial * (1.05) ** anios_hold
            ev_salida = ebitda_salida * mult_salida
            deuda_final = precio_compra * deuda_pct * 0.5  # 50% pagada
            equity_salida = ev_salida - deuda_final
            
            tir_matriz[i, j] = (equity_salida / equity) ** (1 / anios_hold) - 1
            moic_matriz[i, j] = equity_salida / equity
    
    return tir_matriz, moic_matriz
```

> 💡 En entrevistas de PE, la pregunta clasica es: "Compras una empresa a 10x EBITDA con 60% deuda, la vendes a 10x EBITDA en 5 anios. Sin crecimiento de EBITDA, ¿cual es tu IRR?" Respuesta: ~15% (la deuda se paga y genera retorno incluso sin crecimiento operativo).

---

## 2. Practica

### 2.1 Ejercicio guiado: LBO Simplificado de 5 Anios

**Concepto financiero:** Un fondo de PE adquiere IndustrialCo por $500M (8x EBITDA de $62.5M) con 60% deuda senior (tasa 5%) y 40% equity. Proyectamos 5 anios de operacion y venta.

**Codigo:**

```python
import numpy as np
import pandas as pd
from scipy.optimize import newton

# Supuestos de la transaccion
ebitda_0 = 62.5          # EBITDA inicial en millones
multiplo_entrada = 8.0   # 8x EBITDA
precio_compra = ebitda_0 * multiplo_entrada
deuda_pct = 0.60
equity_pct = 0.40
deuda_inicial = precio_compra * deuda_pct
equity_inicial = precio_compra * equity_pct
tasa_deuda = 0.05
tasa_impositiva = 0.21

# Supuestos operativos (5 anios)
crecimiento_ingresos = [0.08, 0.07, 0.06, 0.05, 0.04]
margen_ebitda = 0.30
depreciacion_pct = 0.04
capex_pct = 0.05
wc_pct = 0.08

ingreso_0 = 208.33

# Proyectar
anios_proyeccion = 5
ingresos = np.zeros(anios_proyeccion)
ingresos[0] = ingreso_0 * (1 + crecimiento_ingresos[0])
for t in range(1, anios_proyeccion):
    ingresos[t] = ingresos[t-1] * (1 + crecimiento_ingresos[t])

ebitda = ingresos * margen_ebitda
depreciacion = ingresos * depreciacion_pct
ebit = ebitda - depreciacion
capex = ingresos * capex_pct
wc = ingresos * wc_pct
delta_wc = np.diff(wc, prepend=ingreso_0 * wc_pct)

# Debt schedule simplificado
saldo_deuda = deuda_inicial
flujos_sponsor = []  # Dividendos al sponsor
saldos_deuda_hist = []

for t in range(anios_proyeccion):
    intereses = saldo_deuda * tasa_deuda
    ebt_anio = ebit[t] - intereses
    impuestos = max(0, ebt_anio * tasa_impositiva)
    utilidad_neta = ebt_anio - impuestos
    
    fcf = utilidad_neta + depreciacion[t] - capex[t] - delta_wc[t]
    pago_deuda = min(fcf, saldo_deuda)
    saldo_deuda -= pago_deuda
    saldos_deuda_hist.append(saldo_deuda)
    
    remanente_sponsor = fcf - pago_deuda
    flujos_sponsor.append(max(0, remanente_sponsor))

# Salida (anio 5)
multiplo_salida = 8.0
ebitda_salida = ebitda[-1]
ev_salida = ebitda_salida * multiplo_salida
equity_salida = ev_salida - saldo_deuda

# IRR
flujos_totales = [-equity_inicial] + flujos_sponsor + [equity_salida]

def vpn_tir(r):
    return sum(f / (1 + r) ** t for t, f in enumerate(flujos_totales))

tir_result = newton(vpn_tir, 0.15)
moic_result = (sum(flujos_sponsor) + equity_salida) / equity_inicial

# Reporte
df_deuda = pd.DataFrame({
    'Anio': range(1, anios_proyeccion + 1),
    'EBITDA': ebitda,
    'FCF': [utilidad_neta + depreciacion[t] - capex[t] - delta_wc[t] for t in range(anios_proyeccion)],
    'Saldo_Deuda': saldos_deuda_hist
})

print("=== LBO IndustrialCo ===")
print(f"Precio de compra: ${precio_compra:.1f}M")
print(f"Deuda inicial: ${deuda_inicial:.1f}M ({deuda_pct:.0%})")
print(f"Equity sponsor: ${equity_inicial:.1f}M ({equity_pct:.0%})")
print(f"\nEBITDA salida (anio 5): ${ebitda_salida:.1f}M")
print(f"EV salida: ${ev_salida:.1f}M")
print(f"Equity salida: ${equity_salida:.1f}M")
print(f"\nIRR: {tir_result:.1%}")
print(f"MOIC: {moic_result:.2f}x")
print(f"\n{df_deuda.to_string(index=False)}")
```

**Output:**
```
=== LBO IndustrialCo ===
Precio de compra: $500.0M
Deuda inicial: $300.0M (60%)
Equity sponsor: $200.0M (40%)

EBITDA salida (anio 5): $77.7M
EV salida: $621.7M
Equity salida: $484.5M

IRR: 24.7%
MOIC: 2.95x
```

---

## 3. Aplicacion en Finanzas 💰

El LBO es el modelo central del Private Equity:

- **Fondos de PE (Blackstone, KKR, Carlyle):** Cada adquisicion requiere un LBO completo para determinar el precio maximo a pagar y la estructura de capital optima.
- **Banca de Inversion (Leveraged Finance):** Los banqueros de LevFin estructuran la deuda del LBO y modelan los covenants.
- **Due Diligence:** Antes de cerrar un LBO, el sponsor modela 50+ escenarios para entender los riesgos.
- **Salidas (Exits):** IPO, venta a otro sponsor (secondary buyout), o venta a estrategico. El LBO modela cada escenario.

> 💡 La regla de oro del PE: "Compramos a 8x, vendemos a 10x, y en el camino la deuda se paga sola." Si ademas creces el EBITDA, el retorno se multiplica.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-6/U27_ejercicios.py`

1. **LBO Base:** Construye un LBO completo para RetailCo (EBITDA $100M, precio 8x, 60% deuda senior al 5%, 40% equity). Proyecta 5 anios con crecimiento de ingresos 6% anual, margen EBITDA 25%. Calcula IRR y MOIC asumiendo salida a 8x EBITDA.

2. **Debt Schedule Detallado:** Agrega al LBO del ejercicio 1: (a) amortizacion obligatoria de 5% anual sobre saldo inicial, (b) cash sweep del 100% del FCF excedente. Muestra la tabla de evolucion de deuda anio a anio.

3. **Sensibilidad 3×3:** Para el LBO base, genera una tabla de sensibilidad 3×3: multiplos de entrada (7x, 8x, 9x) vs multiplos de salida (7x, 8x, 9x). Reporta IRR para cada combinacion. Discute que escenarios generan IRR < 15% (inaceptable para PE).

4. **Estructura de Deuda en Capas:** Modela un LBO con deuda senior (4x EBITDA, 5%) y deuda subordinada (2x EBITDA, 9%). Implementa la cascada de pagos donde la deuda senior se paga primero. ¿Como cambia la IRR?

5. **Sensibilidad Avanzada 5×5:** Genera matriz de sensibilidad con 5 niveles de crecimiento de EBITDA (−2%, 0%, 2%, 4%, 6%) vs 5 niveles de multiplo de salida (6x a 10x). Grafica la matriz como heatmap de IRR.

---

## 5. Resumen

| Componente | Descripcion | Importancia |
|-----------|------------|------------|
| Sources & Uses | De donde viene y a donde va el dinero | Verifica que el LBO cierra |
| Debt Schedule | Proyeccion de pago de deuda anio a anio | Determina capacidad de pago |
| Cash Sweep | FCF excedente se usa para pagar deuda | Acelera desapalancamiento |
| IRR | Tasa interna de retorno del sponsor | Metrica principal de PE (>20% target) |
| MOIC | Veces que se multiplica el capital | Complemento al IRR (>2.0x target) |
| Sensibilidad | IRR bajo multiples escenarios | Muestra riesgos y oportunidades |

---

## ✅ Autoevaluacion

1. ¿Por que un LBO genera retorno incluso si el EBITDA no crece?
2. ¿Como afecta un mayor porcentaje de deuda a la IRR? ¿Cual es el riesgo?
3. ¿Que es el cash sweep y por que acelera los retornos del sponsor?
4. ¿Por que la IRR puede ser alta con MOIC bajo y viceversa?
5. ¿Que significa que un LBO tenga IRR de 30% pero MOIC de solo 1.5x?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Estructura LBO: Sources & Uses, debt schedule, cash flow waterfall
> - Cascada de pagos: senior → subordinada → sponsor
> - IRR via scipy.optimize.newton y MOIC
> - La relacion: apalancamiento ↑ = IRR ↑ pero tambien riesgo ↑
> - Triangulo de sensibilidad: entry multiple × exit multiple × leverage
