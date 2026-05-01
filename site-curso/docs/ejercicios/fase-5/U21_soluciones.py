# U21: SOLUCIONES — Pandas Avanzado: Análisis Técnico

import pandas as pd
import numpy as np

# Datos compartidos para todos los ejercicios
np.random.seed(42)
fechas = pd.date_range("2024-01-02", periods=252, freq="B")
retornos_sim = np.random.normal(0.0005, 0.015, 252)
retornos_sim[0] = 0
precios = pd.Series(100 * np.cumprod(1 + retornos_sim), index=fechas, name="precio")

# ============================================================
# Ejercicio 1: SMA, EMA y Golden/Death Cross
# ============================================================
print("=== Ejercicio 1: Cruces de medias móviles ===")

sma_20 = precios.rolling(20).mean()
sma_50 = precios.rolling(50).mean()
ema_12 = precios.ewm(span=12, adjust=False).mean()
ema_26 = precios.ewm(span=26, adjust=False).mean()

golden_cross = (sma_20 > sma_50) & (sma_20.shift(1) <= sma_50.shift(1))
death_cross = (sma_20 < sma_50) & (sma_20.shift(1) >= sma_50.shift(1))

golden_dates = precios[golden_cross].dropna()
death_dates = precios[death_cross].dropna()

print(f"Golden Crosses detectados: {len(golden_dates)}")
for fecha in golden_dates.head(3).index:
    print(f"  {fecha.date()}: SMA_20 cruzó sobre SMA_50 (precio=${precios[fecha]:.2f})")

print(f"Death Crosses detectados: {len(death_dates)}")
for fecha in death_dates.head(3).index:
    print(f"  {fecha.date()}: SMA_20 cruzó bajo SMA_50 (precio=${precios[fecha]:.2f})")

# ============================================================
# Ejercicio 2: Bollinger Bands con señales de ruptura
# ============================================================
print("\n=== Ejercicio 2: Bollinger Bands ===")

sma_20 = precios.rolling(20).mean()
std_20 = precios.rolling(20).std()
bb_superior = sma_20 + 2 * std_20
bb_inferior = sma_20 - 2 * std_20
pct_b = (precios - bb_inferior) / (bb_superior - bb_inferior)

# Ruptura: primer día que cruza
ruptura_alcista = (precios > bb_superior) & (precios.shift(1) <= bb_superior.shift(1))
ruptura_bajista = (precios < bb_inferior) & (precios.shift(1) >= bb_inferior.shift(1))

alcistas = precios[ruptura_alcista].dropna()
bajistas = precios[ruptura_bajista].dropna()

print(f"Rupturas alcistas detectadas: {len(alcistas)}")
for fecha in alcistas.head(3).index:
    print(f"  {fecha.date()}: Precio=${precios[fecha]:.2f} | "
          f"Banda Sup=${bb_superior[fecha]:.2f} | %B={pct_b[fecha]:.2f}")

print(f"Rupturas bajistas detectadas: {len(bajistas)}")
for fecha in bajistas.head(3).index:
    print(f"  {fecha.date()}: Precio=${precios[fecha]:.2f} | "
          f"Banda Inf=${bb_inferior[fecha]:.2f} | %B={pct_b[fecha]:.2f}")

# Reversiones post-ruptura (vuelve dentro de bandas en 5 días)
def contar_reversiones(fechas_ruptura, es_alcista=True):
    total = 0
    reversiones = 0
    for fecha in fechas_ruptura.index:
        total += 1
        idx = precios.index.get_loc(fecha)
        fin = min(idx + 6, len(precios))
        ventana = precios.iloc[idx + 1:fin]
        if es_alcista:
            if any(ventana <= bb_superior.iloc[idx + 1:fin]):
                reversiones += 1
        else:
            if any(ventana >= bb_inferior.iloc[idx + 1:fin]):
                reversiones += 1
    return reversiones, total

rev_alc, tot_alc = contar_reversiones(alcistas, True)
rev_baj, tot_baj = contar_reversiones(bajistas, False)

print(f"Reversiones post-ruptura alcista: {rev_alc}/{tot_alc} "
      f"({rev_alc/tot_alc*100:.1f}%)" if tot_alc > 0 else "")
print(f"Reversiones post-ruptura bajista: {rev_baj}/{tot_baj} "
      f"({rev_baj/tot_baj*100:.1f}%)" if tot_baj > 0 else "")

# ============================================================
# Ejercicio 3: RSI con detección de sobrecompra/sobreventa
# ============================================================
print("\n=== Ejercicio 3: RSI y zonas extremas ===")

delta = precios.diff()
ganancia = delta.clip(lower=0)
perdida = (-delta).clip(lower=0)

ganancia_media = ganancia.ewm(alpha=1/14, adjust=False).mean()
perdida_media = perdida.ewm(alpha=1/14, adjust=False).mean()
rs = ganancia_media / perdida_media
rsi = 100 - (100 / (1 + rs))

sobrecompra = rsi >= 70
sobreventa = rsi <= 30

dias_sobrecompra = sobrecompra.sum()
dias_sobreventa = sobreventa.sum()

print(f"Días en sobrecompra (RSI>=70): {dias_sobrecompra} "
      f"({dias_sobrecompra / len(rsi.dropna()) * 100:.1f}%)")
print(f"Días en sobreventa (RSI<=30): {dias_sobreventa} "
      f"({dias_sobreventa / len(rsi.dropna()) * 100:.1f}%)")

# Rachas consecutivas
def encontrar_racha_maxima(serie_bool):
    racha_actual = 0
    racha_max = 0
    fecha_inicio = None
    fecha_racha_max = None
    for fecha, valor in serie_bool.items():
        if pd.isna(valor):
            continue
        if valor:
            if racha_actual == 0:
                fecha_inicio = fecha
            racha_actual += 1
        else:
            if racha_actual > racha_max:
                racha_max = racha_actual
                fecha_racha_max = fecha_inicio
            racha_actual = 0
    if racha_actual > racha_max:
        racha_max = racha_actual
        fecha_racha_max = fecha_inicio
    return racha_max, fecha_racha_max

racha_oc, fecha_oc = encontrar_racha_maxima(sobrecompra)
racha_ov, fecha_ov = encontrar_racha_maxima(sobreventa)

if fecha_oc:
    print(f"Racha más larga sobrecompra: {racha_oc} días desde {fecha_oc.date()}")
if fecha_ov:
    print(f"Racha más larga sobreventa: {racha_ov} días desde {fecha_ov.date()}")

# ============================================================
# Ejercicio 4: MACD con estrategia de cruce y P&L simulado
# ============================================================
print("\n=== Ejercicio 4: Estrategia MACD ===")

ema_12 = precios.ewm(span=12, adjust=False).mean()
ema_26 = precios.ewm(span=26, adjust=False).mean()
macd_line = ema_12 - ema_26
senal_line = macd_line.ewm(span=9, adjust=False).mean()
histograma = macd_line - senal_line

cruce_alcista = (macd_line > senal_line) & (macd_line.shift(1) <= senal_line.shift(1))
cruce_bajista = (macd_line < senal_line) & (macd_line.shift(1) >= senal_line.shift(1))

print(f"Cruces alcistas del MACD: {cruce_alcista.sum()}")
print(f"Cruces bajistas del MACD: {cruce_bajista.sum()}")

# Estrategia simple: comprar en cruce alcista, vender en cruce bajista
capital = 10_000.0
en_posicion = False
acciones = 0
trades = []
capital_inicial = capital

for fecha in precios.dropna().index:
    if cruce_alcista.get(fecha, False) and not en_posicion:
        acciones = capital / precios[fecha]
        precio_compra = precios[fecha]
        capital = 0
        en_posicion = True
    elif cruce_bajista.get(fecha, False) and en_posicion:
        capital = acciones * precios[fecha]
        pnl = capital - precio_compra * acciones
        trades.append(pnl)
        acciones = 0
        en_posicion = False

if en_posicion:
    capital = acciones * precios.iloc[-1]
    pnl = capital - precio_compra * acciones
    trades.append(pnl)

retorno_total = (capital / capital_inicial - 1) * 100
trades_positivos = sum(1 for t in trades if t > 0)
win_rate = (trades_positivos / len(trades)) * 100 if trades else 0

print(f"Estrategia MACD:")
print(f"  Trades totales: {len(trades)}")
print(f"  Capital inicial: ${capital_inicial:,.2f}")
print(f"  Capital final: ${capital:,.2f}")
print(f"  Retorno total: {retorno_total:.2f}%")
print(f"  Win rate: {win_rate:.1f}%")
if trades:
    print(f"  Mejor trade: +${max(trades):,.2f}")
    print(f"  Peor trade: ${min(trades):,.2f}")
