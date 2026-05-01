# U12: Manejo de Archivos CSV

> **Lectura previa:** [U11: Diccionarios y conjuntos](./U11-diccionarios-sets.md)
> **Próxima unidad:** [U13: Funciones básicas y parámetros](../fase-5/U13-funciones-basicas.md)

---

## 1. Teoría

### 1.1 ¿Por qué archivos CSV en finanzas?

El **CSV** (Comma-Separated Values) es el formato estándar para datos tabulares. Yahoo Finance, Bloomberg, y la mayoría de plataformas exportan datos financieros en CSV.

```csv
Date,Open,High,Low,Close,Volume
2024-01-01,150.00,152.50,149.00,151.00,50000000
2024-01-02,151.00,153.00,150.00,152.50,45000000
```

### 1.2 Leer archivos con `open()` y `csv.reader()`

```python
import csv

# Método 1: csv.reader
with open("datos.csv", "r") as archivo:
    lector = csv.reader(archivo)
    encabezados = next(lector)  # Saltar la primera fila
    for fila in lector:
        print(fila)

# Método 2: csv.DictReader (más legible para finanzas)
with open("datos.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        fecha = fila["Date"]
        cierre = float(fila["Close"])
        print(f"{fecha}: ${cierre:.2f}")
```

### 1.3 Escribir archivos CSV

```python
import csv

# Datos a escribir
datos = [
    {"Ticker": "AAPL", "Precio": 175.50, "Cambio": 1.2},
    {"Ticker": "MSFT", "Precio": 310.00, "Cambio": -0.5},
    {"Ticker": "TSLA", "Precio": 250.00, "Cambio": 2.8},
]

with open("output.csv", "w", newline="") as archivo:
    campos = ["Ticker", "Precio", "Cambio"]
    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(datos)
```

### 1.4 Modos de apertura

| Modo | Descripción |
|------|------------|
| `"r"` | Solo lectura (error si no existe) |
| `"w"` | Escritura (sobrescribe si existe) |
| `"a"` | Append (agrega al final) |
| `"r+"` | Lectura y escritura |

### 1.5 Manejo de errores con archivos

```python
try:
    with open("datos.csv", "r") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print("Error: el archivo no existe")
except PermissionError:
    print("Error: sin permisos para leer")
```

### 1.6 Procesamiento completo de CSV financiero

```python
import csv

def leer_precios(archivo_csv):
    """Lee un CSV de precios y retorna lista de dicts."""
    datos = []
    with open(archivo_csv, "r") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            datos.append({
                "fecha": fila["Date"],
                "apertura": float(fila["Open"]),
                "maximo": float(fila["High"]),
                "minimo": float(fila["Low"]),
                "cierre": float(fila["Close"]),
                "volumen": int(fila["Volume"]),
            })
    return datos

def calcular_retornos(datos):
    """Calcula retornos diarios desde una lista de precios."""
    retornos = []
    for i in range(1, len(datos)):
        ret = (datos[i]["cierre"] - datos[i-1]["cierre"]) / datos[i-1]["cierre"] * 100
        retornos.append({"fecha": datos[i]["fecha"], "retorno": ret})
    return retornos
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Exportar resultados

```python
import csv

# Datos calculados de un análisis
resultados = [
    {"ticker": "AAPL", "rendimiento": 12.5, "volatilidad": 18.2, "sharpe": 0.52},
    {"ticker": "MSFT", "rendimiento": 15.0, "volatilidad": 20.1, "sharpe": 0.60},
    {"ticker": "TSLA", "rendimiento": 8.0, "volatilidad": 35.5, "sharpe": 0.17},
]

# Exportar a CSV
with open("/tmp/analisis_activos.csv", "w", newline="") as f:
    campos = ["ticker", "rendimiento", "volatilidad", "sharpe"]
    escritor = csv.DictWriter(f, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(resultados)

# Leer y mostrar
with open("/tmp/analisis_activos.csv", "r") as f:
    print(f.read())
```

### 2.2 Ejercicio guiado: Leer, procesar, guardar

```python
import csv

# Crear un CSV de ejemplo
with open("/tmp/precios.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Close"])
    writer.writerows([
        ["2024-01-01", "100"],
        ["2024-01-02", "102"],
        ["2024-01-03", "101"],
        ["2024-01-04", "105"],
    ])

# Leer, calcular retornos, guardar
retornos = []
with open("/tmp/precios.csv", "r") as f:
    reader = csv.DictReader(f)
    filas = list(reader)
    for i in range(1, len(filas)):
        r = (float(filas[i]["Close"]) - float(filas[i-1]["Close"])) / float(filas[i-1]["Close"]) * 100
        retornos.append([filas[i]["Date"], f"{r:.2f}%"])

with open("/tmp/retornos.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Return"])
    writer.writerows(retornos)

print("Retornos guardados en /tmp/retornos.csv")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Leer y analizar un CSV de transacciones

```python
# Simulamos un CSV de transacciones
import csv, io

csv_data = """Date,Ticker,Type,Quantity,Price
2024-01-15,AAPL,BUY,10,150.50
2024-02-20,AAPL,BUY,5,155.00
2024-03-10,AAPL,SELL,8,175.00
2024-03-15,MSFT,BUY,4,305.00
2024-04-01,MSFT,SELL,4,320.00
"""

reader = csv.DictReader(io.StringIO(csv_data))
transacciones = list(reader)

# Calcular P&L por ticker
pl = {}
for t in transacciones:
    ticker = t["Ticker"]
    cantidad = int(t["Quantity"])
    precio = float(t["Price"])
    monto = cantidad * precio
    if t["Type"] == "BUY":
        pl[ticker] = pl.get(ticker, 0) - monto
    else:
        pl[ticker] = pl.get(ticker, 0) + monto

for ticker, resultado in pl.items():
    print(f"{ticker}: P&L ${resultado:+,.2f}")
```

---

## 4. Ejercicios Propuestos

1. **Lectura y estadísticas:** Lee un CSV con precios y calcula precio máximo, mínimo y promedio.

2. **Filtro y exportación:** Lee transacciones de un CSV, filtra por ticker específico y exporta el resultado.

3. **Merge de archivos:** Combina dos archivos CSV de precios (diferentes períodos) en uno solo ordenado por fecha.

4. **Reporte de portafolio:** Lee posiciones actuales de un CSV y genera un reporte formateado con P&L total.

---

## 5. Resumen

| Operación | Código |
|-----------|--------|
| Leer CSV lista | `csv.reader(archivo)` |
| Leer CSV dict | `csv.DictReader(archivo)` |
| Escribir CSV lista | `csv.writer(archivo)` |
| Escribir CSV dict | `csv.DictWriter(archivo)` |
| Abrir seguro | `with open(...) as f:` |

---

## ✅ Autoevaluación

1. ¿Qué ventaja tiene `csv.DictReader` sobre `csv.reader`?
2. ¿Qué hace `newline=""` en `open("file.csv", "w", newline="")`?
3. ¿Cómo manejas el error si el archivo CSV no existe?
4. Escribe código que lea precios de un CSV, calcule la volatilidad y guarde el resultado en otro CSV.

---

> 📝 **Knowledge Wiki:** Guarda `reference-U12.md` (patrones csv.reader/DictReader) y `project-U12.md` (análisis de transacciones CSV).
