# U10: Archivos y Datos — CSV, JSON y Datos de Mercado

> **Lectura previa:** [U09: Sets y Strings Avanzados](./U09-sets-strings.md)
> **Próxima unidad:** [U11: Funciones — Construyendo tu Librería Financiera](../fase-3/U11-funciones.md)

---

## 1. Teoría

### 1.1 CSV — El formato estándar de datos financieros

Yahoo Finance, Bloomberg y Reuters exportan en CSV. Es el pan de cada día del analista.

```csv
Date,Open,High,Low,Close,Volume
2024-01-02,150.00,152.50,149.00,151.00,50000000
2024-01-03,151.00,153.00,150.00,152.50,45000000
```

### 1.2 Leer CSV con `csv.reader()` y `csv.DictReader()`

```python
import csv

# csv.reader: acceso por índice
with open("precios.csv", "r") as archivo:
    lector = csv.reader(archivo)
    encabezados = next(lector)  # Saltar primera fila
    for fila in lector:
        fecha, cierre = fila[0], float(fila[4])
        print(f"{fecha}: ${cierre:.2f}")

# csv.DictReader: acceso por nombre de columna (RECOMENDADO)
with open("precios.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        fecha = fila["Date"]
        cierre = float(fila["Close"])
        volumen = int(fila["Volume"])
        print(f"{fecha}: Cierre ${cierre:.2f} | Vol {volumen:,}")
```

### 1.3 Escribir CSV

```python
import csv

# Escribir desde lista de dicts
resultados = [
    {"ticker": "AAPL", "rendimiento": 12.5, "sharpe": 0.52},
    {"ticker": "MSFT", "rendimiento": 15.0, "sharpe": 0.60},
]

with open("analisis.csv", "w", newline="") as f:
    campos = ["ticker", "rendimiento", "sharpe"]
    escritor = csv.DictWriter(f, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(resultados)
```

### 1.4 JSON — Datos estructurados

JSON es el formato de APIs financieras. Bloomberg y Reuters lo usan para datos en tiempo real.

```python
import json

# Escribir JSON
datos = {
    "fecha": "2024-01-15",
    "ticker": "AAPL",
    "precio": 175.50,
    "indicadores": {"sma20": 172.30, "sma50": 168.50, "rsi": 58.2}
}

with open("datos.json", "w") as f:
    json.dump(datos, f, indent=2)        # Guardar con indentación

# Leer JSON
with open("datos.json", "r") as f:
    cargado = json.load(f)
    print(cargado["ticker"])              # AAPL
    print(cargado["indicadores"]["rsi"])  # 58.2

# JSON desde string
json_str = '{"AAPL": 175.50, "MSFT": 310.00}'
precios = json.loads(json_str)
```

### 1.5 `pathlib` — Manejo moderno de rutas

`pathlib` reemplaza `os.path` con una API orientada a objetos. Más legible y menos errores.

```python
from pathlib import Path

# Crear ruta al directorio de datos
datos_dir = Path("documentacion/datos")
datos_dir.mkdir(exist_ok=True)           # Crear si no existe

# Construir rutas
archivo_csv = datos_dir / "precios.csv"  # Usa / para unir rutas
archivo_json = datos_dir / "stats.json"

# Verificar existencia
if archivo_csv.exists():
    print(f"Archivo encontrado: {archivo_csv}")
    print(f"Tamaño: {archivo_csv.stat().st_size} bytes")

# Leer todo el contenido
contenido = archivo_csv.read_text()      # Como string
lineas = archivo_csv.read_text().splitlines()

# Listar archivos en directorio
for archivo in datos_dir.glob("*.csv"):
    print(f"CSV: {archivo.name}")

# Rutas absolutas y relativas
print(Path.cwd())                        # Directorio actual
print(Path.home())                       # Home del usuario
```

### 1.6 Context managers (`with`)

El `with` garantiza que el archivo se cierre correctamente, incluso si hay errores.

```python
# Siempre usa with para archivos
with open("datos.csv", "r") as f:
    contenido = f.read()
# El archivo se cierra automáticamente aquí

# Múltiples archivos
with open("entrada.csv", "r") as entrada, open("salida.json", "w") as salida:
    datos = entrada.read()
    salida.write(json.dumps({"contenido": datos}))
```

### 1.7 Manejo de encoding

Los datos de Bloomberg a veces vienen en latin-1, no UTF-8.

```python
# Especificar encoding
with open("datos_bloomberg.csv", "r", encoding="latin-1") as f:
    datos = f.read()

# Siempre guardar en UTF-8
with open("output.csv", "w", encoding="utf-8") as f:
    f.write("ticker,precio\nAAPL,175.50\n")
```

### 1.8 Modos de apertura

| Modo | Descripción |
|------|------------|
| `"r"` | Solo lectura (error si no existe) |
| `"w"` | Escritura (sobrescribe) |
| `"a"` | Append (agrega al final) |
| `"r+"` | Lectura y escritura |
| `"x"` | Creación exclusiva (error si existe) |

---

## 2. Práctica

### 2.1 Ejercicio guiado: Leer CSV, calcular retornos, guardar JSON

```python
import csv
import json
from pathlib import Path

# Datos CSV de ejemplo
csv_contenido = """Date,Open,Close,Volume
2024-01-02,150.00,151.00,50000000
2024-01-03,151.00,152.50,45000000
2024-01-04,152.50,150.00,48000000
2024-01-05,150.00,153.00,52000000
2024-01-08,153.00,155.00,51000000
"""

# Guardar CSV temporal
ruta_csv = Path("/tmp/precios_ejemplo.csv")
ruta_csv.write_text(csv_contenido)

# Leer y calcular retornos
with open(ruta_csv, "r") as f:
    lector = csv.DictReader(f)
    filas = list(lector)

precios_cierre = [float(fila["Close"]) for fila in filas]
fechas = [fila["Date"] for fila in filas]

retornos = []
for i in range(1, len(precios_cierre)):
    r = (precios_cierre[i] - precios_cierre[i-1]) / precios_cierre[i-1] * 100
    retornos.append({"fecha": fechas[i], "retorno_pct": round(r, 2)})

# Calcular estadísticas
ret_vals = [r["retorno_pct"] for r in retornos]
estadisticas = {
    "periodo": f"{fechas[0]} a {fechas[-1]}",
    "dias": len(retornos),
    "retorno_total_pct": round((precios_cierre[-1]/precios_cierre[0] - 1) * 100, 2),
    "retorno_promedio_pct": round(sum(ret_vals)/len(ret_vals), 2),
    "precio_max": max(precios_cierre),
    "precio_min": min(precios_cierre),
}

# Guardar resultados en JSON
ruta_json = Path("/tmp/estadisticas.json")
with open(ruta_json, "w") as f:
    json.dump({"retornos_diarios": retornos, "estadisticas": estadisticas}, f, indent=2)

print("Estadísticas:")
print(json.dumps(estadisticas, indent=2))
print(f"\nResultados guardados en {ruta_json}")
```

### 2.2 Ejercicio guiado: Explorar archivos existentes con pathlib

```python
from pathlib import Path

proyecto = Path("documentacion")
datos_dir = proyecto / "datos"
datos_dir.mkdir(exist_ok=True)

print(f"Directorio de datos: {datos_dir.absolute()}")
print(f"¿Existe?: {datos_dir.exists()}")

# Crear un archivo de ejemplo si no existe
ejemplo = datos_dir / "precios_ejemplo.csv"
if not ejemplo.exists():
    print(f"Creando {ejemplo}...")
    ejemplo.write_text("Date,Open,High,Low,Close,Volume\n")

print(f"Tamaño: {ejemplo.stat().st_size} bytes")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Pipeline: CSV → Calcular → JSON

```python
import csv
import json
from pathlib import Path

def procesar_csv_a_json(archivo_entrada, archivo_salida):
    """Lee un CSV de precios, calcula retornos diarios y guarda en JSON."""

    with open(archivo_entrada, "r") as f:
        lector = csv.DictReader(f)
        filas = list(lector)

    precios = [float(fila["Close"]) for fila in filas]
    fechas = [fila["Date"] for fila in filas]

    retornos = []
    for i in range(1, len(precios)):
        r = (precios[i] - precios[i-1]) / precios[i-1]
        retornos.append({"fecha": fechas[i], "retorno": round(r, 6)})

    # Calcular estadísticas
    ret_vals = [r["retorno"] for r in retornos]
    n = len(ret_vals)
    media = sum(ret_vals) / n
    varianza = sum((x - media) ** 2 for x in ret_vals) / (n - 1)
    vol_diaria = varianza ** 0.5

    resultado = {
        "retornos": retornos,
        "estadisticas": {
            "media_diaria": round(media, 6),
            "volatilidad_diaria": round(vol_diaria, 6),
            "volatilidad_anualizada": round(vol_diaria * (252 ** 0.5), 6),
        }
    }

    with open(archivo_salida, "w") as f:
        json.dump(resultado, f, indent=2)

    print(f"Pipeline completado: {archivo_salida}")
```

### 3.2 Datos Bloomberg/Reuters típicos

```python
# Estructura típica de un archivo de Bloomberg exportado a CSV
# Nota: Bloomberg a veces usa encoding latin-1 y delimitador | en vez de ,

import csv

datos_bloomberg = """Ticker|PX_LAST|PX_OPEN|PX_HIGH|PX_LOW|VOLUME
AAPL US|175.50|174.00|176.20|173.80|52456789
MSFT US|310.25|308.50|312.00|307.80|23456789
"""

# Leer con delimitador pipe
reader = csv.DictReader(datos_bloomberg.splitlines(), delimiter="|")
for row in reader:
    ticker = row["Ticker"].replace(" US", "")
    precio = float(row["PX_LAST"])
    print(f"{ticker}: ${precio:.2f}")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-2/U10_ejercicios.py`

1. **Lectura y estadísticas:** Lee `precios_ejemplo.csv`, calcula precio máximo, mínimo y promedio.

2. **Filtro y exportación:** Lee transacciones y exporta solo las de un ticker específico a CSV.

3. **CSV → JSON:** Convierte un CSV de precios a JSON con estadísticas.

4. **Pipeline completo:** Lee CSV, calcula retornos diarios, guarda estadísticas en JSON y reporte en CSV.

---

## 5. Resumen

| Operación | Código |
|-----------|--------|
| Leer CSV | `csv.DictReader(archivo)` |
| Escribir CSV | `csv.DictWriter(archivo, fieldnames=campos)` |
| Leer JSON | `json.load(archivo)` |
| Escribir JSON | `json.dump(datos, archivo, indent=2)` |
| Ruta pathlib | `Path("carpeta") / "archivo.csv"` |
| Verificar existencia | `ruta.exists()` |
| Abrir seguro | `with open(...) as f:` |

---

## ✅ Autoevaluación

1. ¿Qué ventaja tiene `csv.DictReader` sobre `csv.reader`?
2. ¿Por qué usar `with open(...)` en vez de `f = open(...)`?
3. ¿Cómo unes rutas con `pathlib`?
4. Convierte `{"AAPL": 175.50}` a string JSON y de vuelta a dict.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U10.md`: csv.DictReader/Writer, json.dump/load, pathlib
> - `project-U10.md`: Pipeline CSV → estadísticas → JSON
