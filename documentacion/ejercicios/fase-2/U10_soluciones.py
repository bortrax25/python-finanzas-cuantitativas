# U10: SOLUCIONES — Archivos y Datos: CSV, JSON y Datos de Mercado

# ============================================================
# Ejercicio 1: Estadísticas de CSV
# ============================================================
print("=== Ejercicio 1: Estadísticas de CSV ===")
import csv, io

csv_datos = """Date,Open,High,Low,Close,Volume
2024-01-02,150.00,152.50,149.00,151.00,50000000
2024-01-03,151.00,153.00,150.00,152.50,45000000
2024-01-04,152.50,154.00,150.00,150.00,48000000
2024-01-05,150.00,153.50,149.50,153.00,52000000
2024-01-08,153.00,155.00,152.00,155.00,51000000
"""

reader = csv.DictReader(io.StringIO(csv_datos))
filas = list(reader)

max_cierre = 0
min_cierre = float("inf")
suma_cierre = 0
volumen_total = 0

for fila in filas:
    cierre = float(fila["Close"])
    volumen = int(fila["Volume"])
    
    suma_cierre += cierre
    volumen_total += volumen
    
    if cierre > max_cierre:
        max_cierre = cierre
        fecha_max = fila["Date"]
    if cierre < min_cierre:
        min_cierre = cierre
        fecha_min = fila["Date"]

promedio = suma_cierre / len(filas)

print(f"Máximo cierre: ${max_cierre:.2f} ({fecha_max})")
print(f"Mínimo cierre: ${min_cierre:.2f} ({fecha_min})")
print(f"Promedio cierre: ${promedio:.2f}")
print(f"Volumen total: {volumen_total:,}")


# ============================================================
# Ejercicio 2: Filtro de Transacciones
# ============================================================
print("\n=== Ejercicio 2: Filtro de Transacciones ===")

transacciones_csv = """Date,Ticker,Type,Quantity,Price
2024-01-15,AAPL,BUY,10,150.50
2024-02-20,MSFT,BUY,5,305.00
2024-03-10,AAPL,SELL,8,175.00
2024-03-15,MSFT,BUY,4,308.00
2024-04-01,MSFT,SELL,4,320.00
2024-05-20,AAPL,BUY,15,180.00
"""

ticker_objetivo = "AAPL"
reader = csv.DictReader(io.StringIO(transacciones_csv))
filtradas = [fila for fila in reader if fila["Ticker"] == ticker_objetivo]

# Mostrar resultado (en la vida real escribirías a archivo)
output = io.StringIO()
writer = csv.DictWriter(output, fieldnames=["Date", "Ticker", "Type", "Quantity", "Price"])
writer.writeheader()
writer.writerows(filtradas)
print(output.getvalue())


# ============================================================
# Ejercicio 3: CSV → JSON
# ============================================================
print("=== Ejercicio 3: CSV → JSON ===")
import json
from pathlib import Path

precios_csv = """Date,Close
2024-01-02,100.00
2024-01-03,102.00
2024-01-04,101.00
2024-01-05,105.00
2024-01-08,103.00
2024-01-09,108.00
2024-01-10,110.00
2024-01-11,107.00
2024-01-12,112.00
"""

reader = csv.DictReader(io.StringIO(precios_csv))
filas = list(reader)

fechas = [f["Date"] for f in filas]
precios = [float(f["Close"]) for f in filas]

retornos = []
for i in range(1, len(precios)):
    r = (precios[i] - precios[i-1]) / precios[i-1] * 100
    retornos.append(r)

n_ret = len(retornos)
media = sum(retornos) / n_ret
varianza = sum((r - media) ** 2 for r in retornos) / (n_ret - 1)
vol = varianza ** 0.5

estadisticas = {
    "periodo": f"{fechas[0]} a {fechas[-1]}",
    "dias": len(precios),
    "precio_max": max(precios),
    "precio_min": min(precios),
    "precio_promedio": round(sum(precios) / len(precios), 2),
    "retorno_total_pct": round((precios[-1] - precios[0]) / precios[0] * 100, 2),
    "volatilidad_diaria_pct": round(vol, 2),
}

ruta_json = Path("/tmp/ejercicio3_stats.json")
ruta_json.write_text(json.dumps(estadisticas, indent=2))
print(json.dumps(estadisticas, indent=2))
print(f"Guardado en {ruta_json}")


# ============================================================
# Ejercicio 4: Pipeline Completo
# ============================================================
print("\n=== Ejercicio 4: Pipeline Completo ===")

datos = """Date,Open,High,Low,Close,Volume
2024-01-02,150.50,152.00,149.50,151.00,50100000
2024-01-03,151.00,153.50,150.00,152.50,45200000
2024-01-04,152.50,154.00,151.00,151.50,48300000
2024-01-05,151.50,153.00,150.50,152.80,49500000
2024-01-08,152.80,155.00,152.00,154.50,51200000
"""

reader = csv.DictReader(io.StringIO(datos))
filas = list(reader)

precios_cierre = [float(f["Close"]) for f in filas]
fechas = [f["Date"] for f in filas]

# Retornos diarios
retornos_diarios = []
for i in range(1, len(precios_cierre)):
    r = (precios_cierre[i] - precios_cierre[i-1]) / precios_cierre[i-1] * 100
    retornos_diarios.append({"Date": fechas[i], "Return_pct": round(r, 4)})

# Estadísticas
n = len(retornos_diarios)
ret_vals = [r["Return_pct"] for r in retornos_diarios]
media = sum(ret_vals) / n
var = sum((x - media) ** 2 for x in ret_vals) / (n - 1)
vol = var ** 0.5

estadisticas = {
    "precio_inicial": precios_cierre[0],
    "precio_final": precios_cierre[-1],
    "retorno_total_pct": round((precios_cierre[-1] - precios_cierre[0]) / precios_cierre[0] * 100, 2),
    "volatilidad_diaria_pct": round(vol, 2),
}

print("=== Estadísticas ===")
print(f"Precio inicial: ${estadisticas['precio_inicial']:.2f}")
print(f"Precio final: ${estadisticas['precio_final']:.2f}")
print(f"Retorno total: {estadisticas['retorno_total_pct']:.2f}%")
print(f"Volatilidad diaria: {estadisticas['volatilidad_diaria_pct']:.2f}%")

# Guardar JSON
ruta_json = Path("/tmp/estadisticas.json")
ruta_json.write_text(json.dumps(estadisticas, indent=2))

# Guardar CSV de retornos
ruta_csv = Path("/tmp/retornos_diarios.csv")
with open(ruta_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Date", "Return_pct"])
    writer.writeheader()
    writer.writerows(retornos_diarios)

print(f"\nArchivos generados:")
print(f"- {ruta_json}")
print(f"- {ruta_csv}")
