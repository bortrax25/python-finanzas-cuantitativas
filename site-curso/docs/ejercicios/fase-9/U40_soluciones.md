# ✅ Soluciones: U40 — Fase 9

> [← Volver a ejercicios Fase 9](index.md) | [📥 Descargar .py](U40_soluciones)

---

```python
# U40: SOLUCIONES — Infraestructura y Producción

# ============================================================
# Ejercicio 1: Logging jerárquico
# ============================================================
import logging
import sys

print("=== Ejercicio 1: Logging Jerárquico ===")

email_enviados = []

class EmailSimuladoHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            mensaje = self.format(record)
            email_enviados.append(mensaje)

# Logger raíz
logger = logging.getLogger('pipeline_demo')
logger.setLevel(logging.DEBUG)

# FileHandler (DEBUG+)
fh = logging.FileHandler('pipeline.log', mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

# StreamHandler (INFO+)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('[Consola] %(levelname)s — %(message)s'))

# EmailHandler (ERROR)
eh = EmailSimuladoHandler()
eh.setLevel(logging.ERROR)
eh.setFormatter(logging.Formatter('[Email simulado] %(levelname)s — %(message)s'))

logger.addHandler(fh)
logger.addHandler(ch)
logger.addHandler(eh)

# Funciones simuladas
def descargar_datos():
    logger.debug("Iniciando descarga de datos...")
    logger.info("Datos descargados: 4 tickers")
    logger.error("Falló la descarga de TSLA")

def validar_datos():
    logger.info("Validación completada: 0 anomalías")
    logger.warning("Valores atípicos detectados en AAPL")

def calcular_senales():
    logger.debug("Iniciando cálculo de señales...")
    logger.info("Señales calculadas: 5 tickers")

# Pipeline
logger.info("Pipeline iniciado")
descargar_datos()
validar_datos()
calcular_senales()
logger.info("Pipeline completado")

print(f"\\nEmails simulados enviados: {len(email_enviados)}")

# Limpiar handlers
for h in [fh, ch, eh]:
    logger.removeHandler(h)
fh.close()


# ============================================================
# Ejercicio 2: Descarga asíncrona simulada
# ============================================================
import asyncio
import time

print("\\n=== Ejercicio 2: Descarga Asíncrona Simulada ===")

tickers = [f'TICKER_{i}' for i in range(15)]

# Versión secuencial
async def descargar_uno(nombre):
    await asyncio.sleep(0.1)  # simula latencia de red
    return nombre, 150.0

async def secuencial(tickers_list):
    resultados = []
    for t in tickers_list:
        resultados.append(await descargar_uno(t))
    return resultados

# Versión asíncrona
async def asincrono(tickers_list):
    tareas = [descargar_uno(t) for t in tickers_list]
    return await asyncio.gather(*tareas)

# Medir tiempos
inicio = time.time()
asyncio.run(secuencial(tickers))
tiempo_seq = time.time() - inicio

inicio = time.time()
asyncio.run(asincrono(tickers))
tiempo_async = time.time() - inicio

print(f"Tiempo secuencial:  {tiempo_seq:.2f}s ({len(tickers)} tickers)")
print(f"Tiempo asíncrono:   {tiempo_async:.2f}s ({len(tickers)} tickers concurrentes)")
speedup = tiempo_seq / tiempo_async if tiempo_async > 0 else 0
print(f"Speedup: {speedup:.1f}x")


# ============================================================
# Ejercicio 3: Pipeline con base de datos
# ============================================================
import sqlite3
import pandas as pd
import numpy as np

print("\\n=== Ejercicio 3: Pipeline con Base de Datos ===")

class PipelineSimplificado:
    def __init__(self, db_path=':memory:'):
        self.conexion = sqlite3.connect(db_path)
        self._crear_tablas()
    
    def _crear_tablas(self):
        self.conexion.executescript("""
            CREATE TABLE IF NOT EXISTS precios (
                fecha TEXT, ticker TEXT, cierre REAL,
                PRIMARY KEY (fecha, ticker)
            );
            CREATE TABLE IF NOT EXISTS senales (
                fecha TEXT, ticker TEXT,
                momentum_20d REAL, senal TEXT,
                PRIMARY KEY (fecha, ticker)
            );
        """)
        self.conexion.commit()
    
    def insertar_precios(self):
        tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']
        fechas = pd.date_range('2024-09-01', periods=100, freq='B').strftime('%Y-%m-%d')
        
        np.random.seed(42)
        for ticker in tickers:
            precio_base = np.random.uniform(50, 350)
            precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.012, len(fechas))))
            for fecha, precio in zip(fechas, precios):
                self.conexion.execute(
                    "INSERT OR REPLACE INTO precios VALUES (?, ?, ?)",
                    (fecha, ticker, round(precio, 2))
                )
        self.conexion.commit()
        
        cursor = self.conexion.execute("SELECT COUNT(*) FROM precios")
        total = cursor.fetchone()[0]
        print(f"Datos insertados: {total} registros (5 tickers x 100 días)")
    
    def calcular_senales(self):
        query = """
            WITH momentum AS (
                SELECT fecha, ticker, cierre,
                       (cierre / LAG(cierre, 20) OVER (PARTITION BY ticker ORDER BY fecha) - 1) * 100 as mom_20d
                FROM precios
            )
            INSERT OR REPLACE INTO senales (fecha, ticker, momentum_20d, senal)
            SELECT fecha, ticker, ROUND(mom_20d, 2),
                   CASE
                       WHEN mom_20d > 3 THEN 'COMPRA'
                       WHEN mom_20d < -3 THEN 'VENTA'
                       ELSE 'NEUTRAL'
                   END
            FROM momentum
            WHERE mom_20d IS NOT NULL
        """
        self.conexion.execute(query)
        self.conexion.commit()
        
        cursor = self.conexion.execute("SELECT COUNT(*) FROM senales")
        total = cursor.fetchone()[0]
        print(f"Señales calculadas: {total} registros con señal")
    
    def consultar_senales(self):
        query = """
            SELECT s.ticker, ROUND(s.momentum_20d, 1) as mom, s.senal
            FROM senales s
            WHERE s.fecha = (SELECT MAX(fecha) FROM senales)
            ORDER BY ABS(s.momentum_20d) DESC
        """
        df = pd.read_sql(query, self.conexion)
        print("Señales última fecha:")
        for _, row in df.iterrows():
            print(f"  {row['ticker']:<6} | mom_20d={row['mom']:+.1f}%  | {row['senal']}")

# Ejecutar pipeline
pipe = PipelineSimplificado()
pipe.insertar_precios()
pipe.calcular_senales()
pipe.consultar_senales()
pipe.conexion.close()


# ============================================================
# Ejercicio 4: Scheduler y automatización
# ============================================================
print("\\n=== Ejercicio 4: Scheduler y Automatización ===")

class PipelineDiario:
    def __init__(self):
        self.conexion = sqlite3.connect(':memory:')
        self.conexion.executescript("""
            CREATE TABLE IF NOT EXISTS precios (
                fecha TEXT, ticker TEXT, cierre REAL,
                PRIMARY KEY (fecha, ticker)
            );
        """)
        self.conexion.commit()
        self.tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']
        self.dia_actual = 0
    
    def insertar_datos_iniciales(self, n_dias=100):
        fechas = pd.date_range('2024-09-01', periods=n_dias, freq='B').strftime('%Y-%m-%d')
        np.random.seed(42)
        for ticker in self.tickers:
            precio_base = np.random.uniform(50, 350)
            precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.012, len(fechas))))
            for fecha, precio in zip(fechas, precios):
                self.conexion.execute(
                    "INSERT OR REPLACE INTO precios VALUES (?, ?, ?)",
                    (fecha, ticker, round(precio, 2))
                )
        self.conexion.commit()
    
    def ejecutar_paso_diario(self):
        self.dia_actual += 1
        ultima_fecha = self.conexion.execute("SELECT MAX(fecha) FROM precios").fetchone()[0]
        nueva_fecha = pd.date_range(ultima_fecha, periods=2, freq='B')[-1].strftime('%Y-%m-%d')
        
        np.random.seed(42 + self.dia_actual)
        for ticker in self.tickers:
            ultimo_precio = self.conexion.execute(
                "SELECT cierre FROM precios WHERE ticker = ? ORDER BY fecha DESC LIMIT 1",
                (ticker,)
            ).fetchone()[0]
            nuevo_precio = ultimo_precio * (1 + np.random.normal(0.0003, 0.012))
            self.conexion.execute(
                "INSERT OR REPLACE INTO precios VALUES (?, ?, ?)",
                (nueva_fecha, ticker, round(nuevo_precio, 2))
            )
        self.conexion.commit()
        
        total = self.conexion.execute("SELECT COUNT(*) FROM precios").fetchone()[0]
        print(f"Día {self.dia_actual}: {total} registros totales")
        
        return nueva_fecha

# Simular pipeline
pipe_diario = PipelineDiario()
pipe_diario.insertar_datos_iniciales(100)

# Día 1 (datos iniciales)
cursor = pipe_diario.conexion.execute("SELECT COUNT(*) FROM precios")
total = cursor.fetchone()[0]
print(f"Día 0: {total} registros totales")

# Simular 3 días
for _ in range(3):
    pipe_diario.ejecutar_paso_diario()

print(f"Pipeline diario completado 3 veces.")
pipe_diario.conexion.close()
```

---

> [📥 Descargar archivo .py](U40_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 9](index.md)
