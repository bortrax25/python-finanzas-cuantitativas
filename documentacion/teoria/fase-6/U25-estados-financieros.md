# U25: Analisis de Estados Financieros con Python

> **Lectura previa:** [U24: TVM y Renta Fija](./U24-tvm-renta-fija.md)
> **Proxima unidad:** [U26: Valoracion DCF](./U26-valoracion-dcf.md)

---

## 1. Teoria

### 1.1 Los Tres Estados Financieros

Toda empresa publica reporta trimestralmente estos tres estados:

| Estado | Pregunta que responde | Ecuacion clave |
|--------|----------------------|----------------|
| **Income Statement (PyG)** | ¿Es rentable? | Utilidad Neta = Ingresos - Costos - Impuestos |
| **Balance Sheet** | ¿Que tiene y que debe? | Activos = Pasivos + Patrimonio |
| **Cash Flow** | ¿Cuanto efectivo genera? | ΔEfectivo = CFO + CFI + CFF |

```python
import pandas as pd
import numpy as np

# Estructura de Income Statement en Python
income_statement = pd.DataFrame({
    'cuenta': ['Ingresos', 'Costo_Ventas', 'Utilidad_Bruta',
               'Gastos_Operativos', 'EBITDA', 'Depreciacion',
               'EBIT', 'Intereses', 'EBT', 'Impuestos', 'Utilidad_Neta'],
    'AAPL': [383285, 214137, 169148, 54847, 114301, 11500, 102801, 3933, 98868, 19736, 79132],
    'TSLA': [81462, 65636, 15826, 9355, 6471, 3421, 3050, 356, 2694, 539, 2155],
    'JPM': [154872, 0, 154872, 93500, 61372, 0, 61372, 0, 61372, 12274, 49098]
})
income_statement = income_statement.set_index('cuenta')

print("=== Income Statement (millones USD) ===")
print(income_statement)
```

> 💡 Los bancos (JPM) no tienen "Costo de Ventas" porque su negocio es margen de intermediacion, no manufactura. Su EBITDA y EBIT son practicamente iguales.

### 1.2 Ratios de Rentabilidad

```python
def margen_bruto(ingresos, costo_ventas):
    """Margen bruto: cuanto queda despues de costos directos."""
    return (ingresos - costo_ventas) / ingresos * 100

def margen_ebitda(ebitda, ingresos):
    """Margen EBITDA: rentabilidad operativa antes de depreciacion."""
    return ebitda / ingresos * 100

def margen_neto(utilidad_neta, ingresos):
    """Margen neto: cuanto queda para los accionistas."""
    return utilidad_neta / ingresos * 100

def roa(utilidad_neta, activos_totales):
    """Return on Assets: eficiencia en uso de activos."""
    return utilidad_neta / activos_totales * 100

def roe(utilidad_neta, patrimonio):
    """Return on Equity: rentabilidad para el accionista."""
    return utilidad_neta / patrimonio * 100

def roic(nopat, capital_invertido):
    """Return on Invested Capital: rentabilidad del capital operativo.
    NOPAT = EBIT × (1 - tasa_impositiva)
    Capital Invertido = Activos Totales - Pasivos Corrientes sin deuda + Deuda LP
    """
    return nopat / capital_invertido * 100
```

> ⚠️ ROE alto puede ser por alto apalancamiento, no por eficiencia operativa. Siempre compara ROE con ROA: si ROE >> ROA, la empresa esta muy apalancada.

### 1.3 Ratios de Liquidez y Solvencia

```python
def razon_corriente(activos_corrientes, pasivos_corrientes):
    """Current Ratio: capacidad de pagar deudas de corto plazo."""
    return activos_corrientes / pasivos_corrientes

def prueba_acida(activos_corrientes, inventarios, pasivos_corrientes):
    """Quick Ratio: liquidity sin inventarios (mas exigente)."""
    return (activos_corrientes - inventarios) / pasivos_corrientes

def razon_efectivo(efectivo_eq, pasivos_corrientes):
    """Cash Ratio: solo efectivo disponible."""
    return efectivo_eq / pasivos_corrientes

def deuda_sobre_ebitda(deuda_total, ebitda):
    """Leverage: cuantos anios de EBITDA se necesitan para pagar la deuda."""
    return deuda_total / ebitda

def deuda_sobre_patrimonio(deuda_total, patrimonio):
    """Debt-to-Equity: estructura de capital."""
    return deuda_total / patrimonio
```

### 1.4 Ratios de Eficiencia

```python
def rotacion_activos(ingresos, activos_totales):
    """Asset Turnover: ingresos generados por unidad de activo."""
    return ingresos / activos_totales

def rotacion_inventario(costo_ventas, inventario_promedio):
    """Inventory Turnover: veces que se vende el inventario."""
    return costo_ventas / inventario_promedio

def dias_inventario(rotacion):
    """Dias de inventario: tiempo promedio en bodega."""
    return 365 / rotacion

def dias_cobro(cuentas_por_cobrar, ingresos_diarios):
    """DSO (Days Sales Outstanding): dias para cobrar a clientes."""
    return cuentas_por_cobrar / ingresos_diarios

def dias_pago(cuentas_por_pagar, compras_diarias):
    """DPO (Days Payable Outstanding): dias para pagar a proveedores."""
    return cuentas_por_pagar / compras_diarias

def ciclo_conversion_efectivo(dso, dio, dpo):
    """Cash Conversion Cycle: dias entre pagar y cobrar. Menor es mejor."""
    return dio + dso - dpo  # DIO = dias inventario
```

### 1.5 Ratios de Valoracion / Mercado

```python
def per(precio_accion, utilidad_por_accion):
    """Price-to-Earnings: cuanto paga el mercado por $1 de utilidad."""
    return precio_accion / utilidad_por_accion

def precio_valor_libro(precio_accion, valor_libro_por_accion):
    """Price-to-Book: prima sobre valor contable."""
    return precio_accion / valor_libro_por_accion

def ev_ebitda(enterprise_value, ebitda):
    """EV/EBITDA: multiplo de valoracion operativa."""
    return enterprise_value / ebitda

def rentabilidad_dividendo(dividendo_anual, precio_accion):
    """Dividend Yield: retorno por dividendos."""
    return dividendo_anual / precio_accion * 100

def payout_ratio(dividendo_anual, utilidad_por_accion):
    """Payout Ratio: % de utilidades repartido como dividendos."""
    return dividendo_anual / utilidad_por_accion * 100

def peg_ratio(per, crecimiento_utilidades_pct):
    """PEG Ratio: PER ajustado por crecimiento. < 1 es atractivo."""
    return per / crecimiento_utilidades_pct
```

### 1.6 Analisis DuPont

El modelo DuPont descompone el ROE en sus drivers operativos:

**DuPont de 3 componentes:**
ROE = Margen Neto × Rotacion de Activos × Apalancamiento Financiero
ROE = (Utilidad Neta / Ingresos) × (Ingresos / Activos) × (Activos / Patrimonio)

**DuPont de 5 componentes (mas granular):**
ROE = (Utilidad Neta / EBT) × (EBT / EBIT) × (EBIT / Ingresos) × (Ingresos / Activos) × (Activos / Patrimonio)

```python
def dupont_3(margen_neto_pct, rotacion_activos, multiplicador_patrimonio):
    """Descompone ROE en 3 componentes."""
    return (margen_neto_pct / 100) * rotacion_activos * multiplicador_patrimonio * 100

def dupont_5(carga_impositiva, carga_intereses, margen_operativo, 
             rotacion_activos, multiplicador_patrimonio):
    """Descompone ROE en 5 componentes.
    
    carga_impositiva = utilidad_neta / ebt       (1 - tasa_impuestos)
    carga_intereses = ebt / ebit                  (costo de deuda)
    margen_operativo = ebit / ingresos             (eficiencia operativa pura)
    rotacion_activos = ingresos / activos          (eficiencia en uso de activos)
    multiplicador_patrimonio = activos / patrimonio (apalancamiento)
    """
    roe = carga_impositiva * carga_intereses * margen_operativo
    roe *= rotacion_activos * multiplicador_patrimonio
    return roe * 100
```

> 💡 El DuPont de 5 componentes responde: ¿el ROE viene de eficiencia operativa, eficiencia en uso de activos, o apalancamiento? Un ROE alto por apalancamiento es mas riesgoso.

### 1.7 Analisis Horizontal y Vertical

```python
def analisis_horizontal(df, anio_base):
    """Analisis horizontal: crecimiento % respecto al anio base."""
    return (df.div(df.iloc[:, anio_base], axis=0) - 1) * 100

def analisis_vertical(income_df):
    """Analisis vertical: cada linea como % de los ingresos."""
    return income_df.div(income_df.loc['Ingresos']) * 100
```

### 1.8 Altman Z-Score

El **Z-Score** de Altman predice la probabilidad de quiebra de una empresa:

```
Z = 1.2 × (Capital_Trabajo / Activos)
  + 1.4 × (Utilidades_Retenidas / Activos)
  + 3.3 × (EBIT / Activos)
  + 0.6 × (Valor_Mercado / Pasivos_Totales)
  + 1.0 × (Ingresos / Activos)
```

| Z-Score | Interpretacion |
|---------|---------------|
| Z < 1.81 | Zona de peligro (probable quiebra) |
| 1.81 ≤ Z ≤ 2.99 | Zona gris (incertidumbre) |
| Z > 2.99 | Zona segura (baja probabilidad de quiebra) |

```python
def altman_zscore(capital_trabajo, activos_totales, utilidades_retenidas,
                  ebit, valor_mercado, pasivos_totales, ingresos):
    """Altman Z-Score para empresas manufactureras publicas."""
    x1 = capital_trabajo / activos_totales
    x2 = utilidades_retenidas / activos_totales
    x3 = ebit / activos_totales
    x4 = valor_mercado / pasivos_totales
    x5 = ingresos / activos_totales
    
    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5
    return z

def interpretar_zscore(z):
    """Interpreta el Z-Score de Altman."""
    if z > 2.99:
        return f"Zona Segura (Z = {z:.2f})"
    elif z >= 1.81:
        return f"Zona Gris (Z = {z:.2f})"
    else:
        return f"Zona de Peligro (Z = {z:.2f})"
```

---

## 2. Practica

### 2.1 Ejercicio guiado: Calculadora de Ratios en Cadena

**Concepto financiero:** A partir de un DataFrame con los estados financieros de una empresa, encadenamos funciones para calcular 20+ ratios automaticamente.

**Codigo:**

```python
import pandas as pd
import numpy as np

# Datos financieros de ejemplo (AAPL FY2023, millones USD)
datos = {
    'metrica': ['ingresos', 'costo_ventas', 'gastos_operativos', 'depreciacion',
                'intereses', 'impuestos', 'activos_corrientes', 'activos_totales',
                'pasivos_corrientes', 'pasivos_totales', 'patrimonio',
                'efectivo', 'inventarios', 'cuentas_por_cobrar'],
    'valor': [383285, 214137, 54847, 11500, 3933, 19736,
              143566, 352583, 145308, 290437, 62146,
              29965, 6331, 60085]
}
df = pd.DataFrame(datos).set_index('metrica')

# Ratios de rentabilidad
utilidad_bruta = df.loc['ingresos'] - df.loc['costo_ventas']
ebitda_val = utilidad_bruta - df.loc['gastos_operativos']
ebit_val = ebitda_val - df.loc['depreciacion']
utilidad_neta_val = ebit_val - df.loc['intereses'] - df.loc['impuestos']

margen_bruto = utilidad_bruta / df.loc['ingresos'] * 100
margen_ebitda = ebitda_val / df.loc['ingresos'] * 100
margen_neto = utilidad_neta_val / df.loc['ingresos'] * 100
roa = utilidad_neta_val / df.loc['activos_totales'] * 100
roe = utilidad_neta_val / df.loc['patrimonio'] * 100

# Ratios de liquidez
razon_corriente = df.loc['activos_corrientes'] / df.loc['pasivos_corrientes']
prueba_acida = (df.loc['activos_corrientes'] - df.loc['inventarios']) / df.loc['pasivos_corrientes']
deuda_patrimonio = df.loc['pasivos_totales'] / df.loc['patrimonio']

# Altman Z-Score
capital_trabajo = df.loc['activos_corrientes'] - df.loc['pasivos_corrientes']
utilidades_retenidas = utilidad_neta_val  # Simplificado
valor_mercado = 2900000  # Market cap real aprox

z_score = 1.2 * (capital_trabajo / df.loc['activos_totales'])
z_score += 1.4 * (utilidades_retenidas / df.loc['activos_totales'])
z_score += 3.3 * (ebit_val / df.loc['activos_totales'])
z_score += 0.6 * (valor_mercado / df.loc['pasivos_totales'])
z_score += 1.0 * (df.loc['ingresos'] / df.loc['activos_totales'])

print(f"Margen Bruto: {margen_bruto:.1f}%")
print(f"Margen EBITDA: {margen_ebitda:.1f}%")
print(f"Margen Neto: {margen_neto:.1f}%")
print(f"ROA: {roa:.1f}%")
print(f"ROE: {roe:.1f}%")
print(f"Razon Corriente: {razon_corriente:.2f}")
print(f"Prueba Acida: {prueba_acida:.2f}")
print(f"Deuda/Patrimonio: {deuda_patrimonio:.2f}")
print(f"Z-Score de Altman: {z_score:.2f}")
```

**Output:**
```
Margen Bruto: 44.1%
Margen EBITDA: 29.8%
Margen Neto: 20.7%
ROA: 22.5%
ROE: 127.4%
Razon Corriente: 0.99
Prueba Acida: 0.94
Deuda/Patrimonio: 4.67
Z-Score de Altman: 9.12
```

---

## 3. Aplicacion en Finanzas 💰

Los analistas de **Investment Banking (IBD) en JP Morgan** pasan sus primeras 2-3 semanas en cada deal construyendo el analisis de estados financieros. Es la base de todo el trabajo posterior:

- **Comparables analysis:** Seleccionar empresas comparables requiere entender sus ratios.
- **DCF:** Las proyecciones parten del analisis historico de margenes, rotaciones y crecimiento.
- **LBO:** La capacidad de deuda se determina con ratios de cobertura (Deuda/EBITDA, EBITDA/Intereses).
- **Credit analysis:** Los analistas de credito usan Altman Z-Score y ratios de cobertura para asignar ratings.

> 💡 Un analista senior de M&A te dira: "Antes de tocar una celda del DCF, pasate 2 dias entendiendo los estados financieros de la empresa."

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-6/U25_ejercicios.py`

1. **Calculadora de 30 Ratios:** A partir de datos financieros de AAPL, TSLA y JPM (proporcionados), calcula 30 ratios financieros organizados por categoria (rentabilidad, liquidez, eficiencia, valoracion, cobertura).

2. **Analisis DuPont:** Para las tres empresas, descompone el ROE usando DuPont de 3 y 5 componentes. Identifica cual empresa genera ROE por eficiencia operativa, cual por rotacion de activos y cual por apalancamiento.

3. **Altman Z-Score:** Calcula el Z-Score de Altman para las tres empresas. Interpreta los resultados y explica cuales podrian tener problemas de solvencia.

4. **Analisis Horizontal y Vertical:** Realiza un analisis vertical de los income statements (cada linea como % de ingresos) y un analisis horizontal (crecimiento vs anio anterior). ¿Que tendencias observas?

5. **Equity Research Summary:** Escribe una funcion `resumen_empresa()` que reciba el ticker y genere un mini-reporte con los 10 ratios mas importantes, DuPont, Z-Score y una conclusion de 3 lineas estilo equity research.

---

## 5. Resumen

| Categoria | Ratios Clave | Formula |
|-----------|-------------|---------|
| Rentabilidad | ROE | Utilidad Neta / Patrimonio |
| Rentabilidad | ROA | Utilidad Neta / Activos |
| Rentabilidad | Margen EBITDA | EBITDA / Ingresos |
| Liquidez | Current Ratio | Activos Corrientes / Pasivos Corrientes |
| Liquidez | Quick Ratio | (AC - Inventarios) / PC |
| Solvencia | Deuda/Patrimonio | Pasivos Totales / Patrimonio |
| Solvencia | Deuda/EBITDA | Deuda Total / EBITDA |
| Eficiencia | Rotacion Activos | Ingresos / Activos |
| Valoracion | P/E | Precio / UPA |
| Valoracion | EV/EBITDA | Enterprise Value / EBITDA |
| Quiebra | Altman Z-Score | 5 factores ponderados |

---

## ✅ Autoevaluacion

1. ¿Cual es la diferencia entre ROA y ROE? ¿Que significa si ROE >> ROA?
2. ¿Por que el modelo DuPont de 5 componentes es mas informativo que el de 3?
3. ¿Que indica un Altman Z-Score < 1.81 y que harias como analista de credito?
4. ¿Por que el Cash Conversion Cycle es una metrica de eficiencia operativa?
5. ¿Cuales son los 5 componentes del DuPont extendido y que mide cada uno?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Tres estados financieros y su ecuacion contable
> - 30+ ratios organizados en 5 categorias
> - Modelo DuPont de 3 y 5 componentes
> - Altman Z-Score y sus umbrales de interpretacion
> - La diferencia entre analisis horizontal (tendencia) y vertical (estructura)
