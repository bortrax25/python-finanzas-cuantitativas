# 📝 Ejercicios: U25 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U25_ejercicios)

---

```python
# U25: EJERCICIOS — Analisis de Estados Financieros con Python

import pandas as pd
import numpy as np

# Datos compartidos para todos los ejercicios
# Estados financieros de AAPL, TSLA, JPM (datos estilizados FY2023, millones USD)
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
# A partir de datos financieros de AAPL, TSLA y JPM, calcula al
# menos 30 ratios financieros organizados por categoria:
# rentabilidad, liquidez, eficiencia, valoracion y cobertura.
# Presenta los resultados en un DataFrame.
# ============================================================
print("=== Ejercicio 1: Calculadora de 30 Ratios ===")

# Escribe tu codigo aqui



# Output esperado:
# === Ratios Financieros ===
#                                 AAPL      TSLA       JPM
# Rentabilidad
#   Margen Bruto (%)              44.13     19.43       N/A
#   Margen EBITDA (%)             29.81      7.94     39.63
#   Margen Neto (%)               20.65      2.65     31.70
#   ROA (%)                       22.45      2.62      1.34
#   ROE (%)                      127.36      4.70     61.28
#   ROIC (%)                      32.50      4.80      5.20
# Liquidez
#   Current Ratio                  0.99      1.41       N/A
#   Quick Ratio                    0.94      1.05       N/A
#   Cash Ratio                     0.21      0.61       N/A
# Solvencia
#   Deuda/Patrimonio               4.67      0.79     44.75
#   Deuda/EBITDA                   2.49      5.16     58.42
#   Cobertura Intereses           27.12      8.78       N/A
# 
# (continuacion con 30+ ratios)


# ============================================================
# Ejercicio 2: Analisis DuPont (3 y 5 componentes)
# Descompone el ROE de cada empresa usando DuPont de 3 y 5
# componentes. Identifica cual empresa genera ROE principalmente
# por eficiencia operativa, cual por rotacion y cual por leverage.
# ============================================================
print("\\n=== Ejercicio 2: Analisis DuPont ===")

# Escribe tu codigo aqui



# Output esperado:
# === DuPont de 3 Componentes ===
#             Margen Neto  Rotacion Activos  Multiplicador  ROE
# AAPL            20.65%           1.087           5.67   127.4%
# TSLA             2.65%           0.989           1.79     4.7%
# JPM             31.70%           0.042          45.75    61.3%
# 
# === DuPont de 5 Componentes ===
#             Carga Imp  Carga Int  Margen Op  Rot Act  Multiplicador  ROE
# AAPL            0.800      0.962      0.268    1.087         5.67   127.4%
# TSLA            0.800      0.884      0.052    0.989         1.79     4.7%
# JPM             0.800      1.000      0.396    0.042        45.75    61.3%
# 
# Conclusion:
#   AAPL: ROE elevado por alto margen operativo + leverage
#   TSLA: ROE bajo por margenes comprimidos, poco leverage
#   JPM:  ROE elevado casi exclusivamente por apalancamiento extremo


# ============================================================
# Ejercicio 3: Altman Z-Score
# Calcula el Z-Score de Altman para las tres empresas.
# Interpreta los resultados considerando sus modelos de negocio.
# Nota: El Z-Score original aplica a manufactureras. Para JPM
# (banco) el Z-Score no es directamente aplicable.
# ============================================================
print("\\n=== Ejercicio 3: Altman Z-Score ===")

# Escribe tu codigo aqui



# Output esperado:
# === Altman Z-Score ===
# Empresa    X1      X2      X3      X4      X5   Z-Score  Interpretacion
# AAPL    -0.0049  0.0146  0.2992  9.8733  1.0871  12.09   Zona Segura
# TSLA     0.1317  0.2282  0.0413 20.8716  0.9894  14.29   Zona Segura
# JPM        N/A     N/A  0.0167  0.1415  0.0422   0.60   No aplica (banco)
# 
# Nota: El Z-Score no es directamente aplicable a JPM (banco).
# En la practica se usa el Z-Score para no-financieras.


# ============================================================
# Ejercicio 4: Analisis Horizontal y Vertical
# Realiza un analisis vertical de los income statements (cada
# linea como % de ingresos) y un analisis horizontal simplificado
# (crecimiento vs anio anterior). Para el horizontal, usa datos
# de dos anios de AAPL.
# ============================================================
print("\\n=== Ejercicio 4: Analisis Horizontal y Vertical ===")

# Datos de AAPL para 2 anios (FY2022 y FY2023)
ingresos_aapl_2022 = 394328
ingresos_aapl_2023 = 383285

# Escribe tu codigo aqui



# Output esperado:
# === Analisis Vertical AAPL FY2023 ===
# Ingresos             100.0%
# Costo Ventas          55.9%
# Utilidad Bruta        44.1%
# Gastos Operativos     14.3%
# EBITDA                29.8%
# EBIT                  26.8%
# Utilidad Neta         20.7%
# 
# === Analisis Horizontal AAPL ===
# Ingresos 2022: $394,328M
# Ingresos 2023: $383,285M
# Crecimiento: -2.8%


# ============================================================
# Ejercicio 5: Equity Research Summary
# Escribe una funcion resumen_empresa() que reciba el diccionario
# de datos de una empresa y genere un mini-reporte con:
#   - 10 ratios clave
#   - DuPont de 3 componentes
#   - Z-Score (si aplica)
#   - Conclusion de 3 lineas estilo "equity research"
# Pruebala con las 3 empresas.
# ============================================================
print("\\n=== Ejercicio 5: Equity Research Summary ===")

def resumen_empresa(nombre, datos):
    pass  # Escribe tu codigo aqui



# Output esperado:
# ============ EQUITY RESEARCH: AAPL ============
# Ratios Clave:
#   ROE: 127.4% | ROA: 22.5% | Margen EBITDA: 29.8%
#   P/E: 29.5x | EV/EBITDA: 23.2x | Deuda/EBITDA: 2.5x
#   Current Ratio: 1.0x | FCF Yield: 3.2%
# DuPont: MN 20.7% x RA 1.09 x EM 5.67 = ROE 127.4%
# Z-Score: 12.1 (Zona Segura)
# 
# Conclusion:
#   AAPL es una maquina de generacion de efectivo con margenes
#   operativos superiores al 30%. Su ROE excepcional (127%)
#   combina alta rentabilidad con apalancamiento via recompras.
#   Valoracion en 29x P/E refleja calidad premium. Catalizadores:
#   servicios (+15% YoY) y potencial ciclo de upgrade con AI.
```

---

> [📥 Descargar archivo .py](U25_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
