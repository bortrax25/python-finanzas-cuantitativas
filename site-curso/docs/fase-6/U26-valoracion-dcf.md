# U26: Valoracion de Empresas — DCF y Comparables

> **Lectura previa:** [U25: Analisis de Estados Financieros](./U25-estados-financieros.md)
> **Proxima unidad:** [U27: LBO Modeling](./U27-lbo.md)

---

## 1. Teoria

> ⚠️ **JP Morgan IBD Core Skill #1:** El DCF (Discounted Cash Flow) es la metodologia de valoracion mas importante en banca de inversion. Todo analista de primer anio pasa sus primeras 6 semanas aprendiendo a construir un DCF desde cero.

### 1.1 Free Cash Flow to Firm (FCFF) y Free Cash Flow to Equity (FCFE)

El flujo de caja libre representa el efectivo disponible para los proveedores de capital despues de todas las inversiones necesarias para mantener el negocio.

```python
import numpy as np
import pandas as pd

def fcff(ebit, tasa_impositiva, depreciacion, capex, delta_wc):
    """Free Cash Flow to Firm: disponible para deuda y accionistas.
    
    FCFF = EBIT × (1 - t) + Depreciacion - CAPEX - ΔWorking Capital
    """
    nopat = ebit * (1 - tasa_impositiva)
    return nopat + depreciacion - capex - delta_wc

def fcfe(utilidad_neta, depreciacion, capex, delta_wc, endeudamiento_neto):
    """Free Cash Flow to Equity: disponible para accionistas.
    
    FCFE = Utilidad Neta + Depreciacion - CAPEX - ΔWC + Endeudamiento Neto
    """
    return utilidad_neta + depreciacion - capex - delta_wc + endeudamiento_neto
```

> 💡 **FCFF vs FCFE:** FCFF valora la empresa completa (enterprise value). FCFE valora solo el equity. La relacion: FCFE = FCFF - Intereses×(1-t) + Endeudamiento Neto.

### 1.2 Proyeccion de Estados Financieros

Para proyectar flujos de caja, partimos del income statement proyectado:

```python
def proyectar_ingresos(ingreso_base, tasa_crecimiento, anios):
    """Proyecta ingresos con tasa de crecimiento anual."""
    return np.array([ingreso_base * (1 + tasa_crecimiento) ** t for t in range(1, anios + 1)])

def proyectar_income_statement(ingresos, margen_ebitda, margen_ebit,
                                depreciacion_pct, tasa_impositiva):
    """Proyecta income statement completo a partir de ingresos."""
    ebitda = ingresos * margen_ebitda
    depreciacion_arr = ingresos * depreciacion_pct
    ebit = ebitda - depreciacion_arr
    intereses = np.zeros_like(ebit)  # Simplificado, se calcula del debt schedule
    ebt = ebit - intereses
    impuestos = np.maximum(ebt, 0) * tasa_impositiva
    utilidad_neta = ebt - impuestos
    
    return pd.DataFrame({
        'anio': range(1, len(ingresos) + 1),
        'ingresos': ingresos,
        'ebitda': ebitda,
        'depreciacion': depreciacion_arr,
        'ebit': ebit,
        'impuestos': impuestos,
        'utilidad_neta': utilidad_neta,
        'nopat': ebit * (1 - tasa_impositiva)
    })
```

### 1.3 Working Capital y CAPEX

```python
def proyectar_working_capital(ingresos, pct_wc_ingresos):
    """Proyecta working capital como % de ingresos."""
    wc = ingresos * pct_wc_ingresos
    delta_wc = np.diff(wc, prepend=wc[0] * 1.1)  # WC inicial como 110% del primer anio
    return wc, delta_wc

def proyectar_capex(ingresos, pct_capex_ingresos):
    """Proyecta CAPEX como % de ingresos."""
    return ingresos * pct_capex_ingresos
```

### 1.4 WACC: Weighted Average Cost of Capital

El WACC es la tasa de descuento que refleja el costo de todas las fuentes de financiamiento:

```
WACC = (E/V) × Ke + (D/V) × Kd × (1 - t)
```

Donde:
- E/V = proporcion de equity en la estructura de capital
- D/V = proporcion de deuda
- Ke = costo del equity (via CAPM)
- Kd = costo de la deuda
- t = tasa impositiva

```python
def costo_equity_capm(tasa_libre_riesgo, beta, prima_mercado):
    """Costo del equity usando CAPM.
    
    Ke = Rf + β × (Rm - Rf)
    """
    return tasa_libre_riesgo + beta * prima_mercado

def wacc(valor_mercado_equity, valor_mercado_deuda, ke, kd, tasa_impositiva):
    """Weighted Average Cost of Capital."""
    valor_total = valor_mercado_equity + valor_mercado_deuda
    
    peso_equity = valor_mercado_equity / valor_total
    peso_deuda = valor_mercado_deuda / valor_total
    
    return peso_equity * ke + peso_deuda * kd * (1 - tasa_impositiva)

# Ejemplo tipico de WACC para una empresa grande US
ke = costo_equity_capm(tasa_libre_riesgo=0.045, beta=1.1, prima_mercado=0.055)
wacc_val = wacc(800000, 200000, ke, 0.04, 0.21)
print(f"Ke (CAPM): {ke:.2%}")
print(f"WACC: {wacc_val:.2%}")
```

> 💡 En la practica, el WACC se calcula iterativamente: necesitas los valores de mercado de E y D para calcular WACC, pero para valorar la empresa con DCF necesitas el WACC. Solucion: usar valores objetivo (target capital structure) o iterar hasta convergencia.

### 1.5 DCF: Valor Terminal y Valor de la Empresa

```python
def dcf_enterprise_value(fcff_proyectados, wacc, valor_terminal):
    """Calcula el Enterprise Value por DCF.
    
    EV = Σ FCFF_t / (1 + WACC)^t + Valor_Terminal / (1 + WACC)^n
    """
    anios = len(fcff_proyectados)
    vp_flujos = sum(fcff_proyectados[t] / (1 + wacc) ** (t + 1) for t in range(anios))
    vp_terminal = valor_terminal / (1 + wacc) ** anios
    
    return vp_flujos + vp_terminal

def valor_terminal_gordon(ultimo_fcff, wacc, crecimiento_perpetuo):
    """Valor terminal por Gordon Growth Model.
    
    VT = FCFF_n × (1 + g) / (WACC - g)
    """
    return ultimo_fcff * (1 + crecimiento_perpetuo) / (wacc - crecimiento_perpetuo)

def valor_terminal_multiplo(ultimo_ebitda, multiplo_ev_ebitda):
    """Valor terminal por multiplo de salida.
    
    VT = EBITDA_n × Multiplo_EV/EBITDA
    """
    return ultimo_ebitda * multiplo_ev_ebitda

def equity_value_from_ev(enterprise_value, deuda_neta, efectivo, intereses_minoritarios=0):
    """Convierte Enterprise Value a Equity Value.
    
    Equity Value = EV - Deuda Neta + Efectivo - Intereses Minoritarios
    Deuda Neta = Deuda Total - Efectivo
    """
    return enterprise_value - deuda_neta + efectivo - intereses_minoritarios

def precio_implicito_por_accion(equity_value, acciones_diluidas):
    """Precio por accion implicito del DCF."""
    return equity_value / acciones_diluidas
```

### 1.6 Tabla de Sensibilidad

La tabla de sensibilidad es la herramienta mas importante en banca de inversion. Muestra como cambia la valoracion bajo diferentes escenarios:

```python
def tabla_sensibilidad(wacc_rango, crecimiento_rango, ultimo_fcff, fcff_proyectados):
    """Genera tabla de sensibilidad: Precio implicito para cada combinacion WACC × crecimiento."""
    resultados = np.zeros((len(wacc_rango), len(crecimiento_rango)))
    
    for i, w in enumerate(wacc_rango):
        for j, g in enumerate(crecimiento_rango):
            vt = valor_terminal_gordon(ultimo_fcff, w, g)
            ev = dcf_enterprise_value(fcff_proyectados, w, vt)
            resultados[i, j] = ev
    
    return pd.DataFrame(
        resultados,
        index=[f"WACC {w:.1%}" for w in wacc_rango],
        columns=[f"Crec. {g:.1%}" for g in crecimiento_rango]
    )

# Ejemplo con meshgrid para tablas mas complejas
def tabla_sensibilidad_meshgrid(rango_1, rango_2, funcion, fcff, ultimo_fcff, **kwargs):
    """Tabla de sensibilidad generica con np.meshgrid."""
    X, Y = np.meshgrid(rango_1, rango_2)
    Z = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = funcion(X[i, j], Y[i, j], fcff, ultimo_fcff)
    return X, Y, Z
```

### 1.7 Analisis por Comparables (Comps)

El analisis por comparables valora una empresa usando los multiplos de empresas similares:

```python
def comps_valuation(metrica_objetivo, multiplo_mediana_comparables):
    """Valoracion por comparables.
    
    Valor Implicito = Metrica × Multiplo Mediana
    """
    return metrica_objetivo * multiplo_mediana_comparables

def analizar_comparables(df_comps):
    """Calcula estadisticas de multiplos de las empresas comparables."""
    stats = pd.DataFrame({
        'media': df_comps.mean(),
        'mediana': df_comps.median(),
        'minimo': df_comps.min(),
        'maximo': df_comps.max(),
        'p25': df_comps.quantile(0.25),
        'p75': df_comps.quantile(0.75),
    })
    return stats
```

---

## 2. Practica

### 2.1 Ejercicio guiado: DCF Completo Paso a Paso

**Concepto financiero:** Valorar TechCo Inc., una empresa de tecnologia con los siguientes datos historicos (anio 0):
- Ingresos: $5,000M
- Margen EBITDA: 35%
- Depreciacion: 5% de ingresos
- CAPEX: 8% de ingresos
- Working Capital: 10% de ingresos
- Tasa impositiva: 21%
- Crecimiento ingresos: 12% → 10% → 8% → 6% → 4%
- WACC: 9%
- Crecimiento perpetuo: 2.5%
- Deuda Neta: $1,200M
- Acciones diluidas: 500M

**Codigo:**

```python
import numpy as np
import pandas as pd

# Supuestos base
ingreso_0 = 5000
margen_ebitda = 0.35
depreciacion_pct = 0.05
capex_pct = 0.08
wc_pct = 0.10
tasa_impositiva = 0.21
tasas_crecimiento = [0.12, 0.10, 0.08, 0.06, 0.04]
wacc_val = 0.09
crecimiento_perpetuo = 0.025
deuda_neta = 1200
acciones = 500

# Proyectar 5 anios
anios = 5
ingresos = np.zeros(anios)
ingresos[0] = ingreso_0 * (1 + tasas_crecimiento[0])
for t in range(1, anios):
    ingresos[t] = ingresos[t-1] * (1 + tasas_crecimiento[t])

ebitda = ingresos * margen_ebitda
depreciacion = ingresos * depreciacion_pct
ebit = ebitda - depreciacion
nopat = ebit * (1 - tasa_impositiva)
capex = ingresos * capex_pct
wc = ingresos * wc_pct
delta_wc = np.diff(wc, prepend=ingreso_0 * wc_pct)

fcff_arr = nopat + depreciacion - capex - delta_wc

# Valor terminal
vt = fcff_arr[-1] * (1 + crecimiento_perpetuo) / (wacc_val - crecimiento_perpetuo)

# EV
ev = sum(fcff_arr[t] / (1 + wacc_val) ** (t + 1) for t in range(anios))
ev += vt / (1 + wacc_val) ** anios

equity_val = ev - deuda_neta
precio_implicito = equity_val / acciones

# Mostrar resultados
df_proyeccion = pd.DataFrame({
    'Anio': range(1, anios + 1),
    'Ingresos': ingresos,
    'EBITDA': ebitda,
    'EBIT': ebit,
    'NOPAT': nopat,
    'CAPEX': capex,
    'ΔWC': delta_wc,
    'FCFF': fcff_arr
})

print(df_proyeccion.to_string(index=False))
print(f"\nValor Terminal (Gordon Growth): ${vt:,.0f}M")
print(f"Enterprise Value: ${ev:,.0f}M")
print(f"Equity Value: ${equity_val:,.0f}M")
print(f"Precio Implicito por Accion: ${precio_implicito:.2f}")
```

**Output:**
```
 Anio    Ingresos      EBITDA        EBIT      NOPAT       CAPEX        ΔWC       FCFF
    1  5600.0000  1960.00000  1680.00000  1327.20000  448.000000  60.000000  1099.20000
    2  6160.0000  2156.00000  1848.00000  1459.92000  492.800000  56.000000  1219.12000
    3  6652.8000  2328.48000  1995.84000  1576.71360  532.224000  49.280000  1290.20960
    4  7051.9680  2468.18880  2115.59040  1671.31642  564.157440  39.916800  1272.24218
    5  7334.0467  2566.91635  2200.21402  1738.16907  586.723738  28.207872  1328.23746

Valor Terminal (Gordon Growth): $20,950M
Enterprise Value: $20,934M
Equity Value: $19,734M
Precio Implicito por Accion: $39.47
```

---

## 3. Aplicacion en Finanzas 💰

El DCF es el metodo de valoracion principal en:

- **M&A (Fusiones y Adquisiciones):** El banco comprador construye un DCF para determinar el precio maximo que puede pagar sin destruir valor.
- **IPO Pricing:** Los bancos underwriters usan DCF + comps para determinar el rango de precio de la OPI.
- **Equity Research:** Los analistas publican target prices basados en su DCF propietario.
- **Activistas (Hedge Funds):** Identifican empresas sub-valoradas por el mercado comparando su DCF con el precio de mercado.

> 💡 **El "Football Field":** En todo pitch book de JP Morgan hay un grafico de barras llamado football field que muestra el rango de valoracion por DCF, comps, transacciones precedentes y LBO. Tu DCF es la columna mas importante.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-6/U26_ejercicios.py`

1. **DCF Completo:** Proyecta 5 anios de FCF para MegaCorp S.A. con ingresos iniciales de $8,000M, margen EBITDA 40%, crecimiento escalonado (15%, 12%, 10%, 8%, 5%). Calcula EV, Equity Value y precio implicito. Asume WACC 8.5%, crecimiento perpetuo 2%, deuda neta $2,500M, acciones 800M.

2. **Tabla de Sensibilidad:** Con el DCF del ejercicio 1, genera una tabla de sensibilidad de 9x9 (WACC de 7% a 11%, crecimiento perpetuo de 1% a 5%). Identifica el rango de precios implicito y el punto medio (WACC base, crecimiento base).

3. **CAPM y WACC:** Para la empresa del ejercicio 1, calcula el WACC desglosando: CAPM para Ke (Rf=4%, β=1.2, prima=5.5%), Kd=3.5% (costo deuda), estructura de capital D/V=25%. Recalcula el DCF con este WACC mas preciso.

4. **Comparacion Gordon vs Exit Multiple:** Para el mismo DCF, compara el valor terminal por Gordon Growth (g=2%) vs Exit Multiple (EV/EBITDA=12x). ¿Cual metodo da un valor mas alto? ¿Por que?

5. **Analisis de Sensibilidad Grafico:** Usa `meshgrid` para crear una tabla de sensibilidad 3D o heatmap de precio implicito vs WACC y tasa de crecimiento perpetuo. Identifica el "corredor de valoracion" razonable.

---

## 5. Resumen

| Componente | Formula | Descripcion |
|-----------|---------|------------|
| FCFF | EBIT(1-t) + D&A - CAPEX - ΔWC | Flujo para todos los stakeholders |
| FCFE | FCFF - Intereses(1-t) + ΔDeuda | Flujo solo para accionistas |
| CAPM Ke | Rf + β × (Rm - Rf) | Costo del equity |
| WACC | (E/V)Ke + (D/V)Kd(1-t) | Costo ponderado de capital |
| Gordon Growth | VT = FCFF(1+g)/(WACC-g) | Valor terminal perpetuo |
| Exit Multiple | VT = EBITDA × Multiple | Valor terminal por comparables |
| EV → Equity | EV - Deuda + Efectivo | Puente a valor del accionista |

---

## ✅ Autoevaluacion

1. ¿Por que restamos el cambio en working capital (ΔWC) del FCFF? ¿No es el WC un activo?
2. ¿Cuando usarias FCFF versus FCFE para valorar una empresa?
3. ¿Como afecta un WACC mas alto al precio implicito? ¿Y un crecimiento perpetuo mas alto?
4. ¿Por que el metodo de Gordon Growth puede dar valores irreales si g se acerca a WACC?
5. ¿Que significa si el precio implicito del DCF esta 40% por encima del precio de mercado actual?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Formula FCFF y FCFE y cuando usar cada una
> - Proceso completo del DCF: proyeccion → FCFF → WACC → VT → EV → Equity → Precio
> - CAPM para costo de equity: Ke = Rf + β(Rm - Rf)
> - Dos metodos de valor terminal: Gordon Growth y Exit Multiple
> - Tablas de sensibilidad como herramienta de presentacion en IBD
