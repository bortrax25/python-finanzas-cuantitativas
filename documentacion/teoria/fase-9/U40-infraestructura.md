# U40: Infraestructura y Producción

> **Lectura previa:** [U39: Algorithmic Trading — Estrategias y Backtesting](./U39-algo-trading.md)
> **Próxima unidad:** [U41: Proyecto — Plataforma de Análisis Cuantitativo](../fase-10/U41-plataforma.md)

---

## 1. Teoría

### 1.1 ¿Por qué infraestructura?

Un modelo brillante que corre una vez en Jupyter vale cero. Para generar valor real, necesitas que el sistema funcione 24/7:

- Descargar datos de mercado automáticamente cada día
- Recalcular señales y métricas de riesgo
- Enviar alertas cuando ocurren eventos relevantes
- Almacenar resultados en bases de datos
- Generar reportes automáticos

Esto es lo que diferencia un script de investigación de un sistema de producción.

```python
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import asyncio
import aiohttp
import logging
import smtplib
from email.mime.text import MIMEText
```

### 1.2 Logging Profesional

El `print()` es para debugging. Para producción, usa `logging`:

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('quant_pipeline')

logger.info("Pipeline iniciado")
logger.warning("Datos de mercado atrasados 5 minutos")
logger.error("Fallo en conexión a base de datos")
```

### 1.3 Descarga Asíncrona de Datos con asyncio + aiohttp

Cuando descargas datos de múltiples fuentes (Yahoo Finance, FRED, Alpha Vantage), hacerlo secuencialmente es lento. Con `asyncio` y `aiohttp`, las descargas se ejecutan en paralelo.

```python
import asyncio
import aiohttp

async def descargar_datos_activo(session, ticker):
    """
    Descarga datos de un activo de forma asíncrona.
    Nota: En producción usarías yfinance o una API real.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                logger.info(f"{ticker}: descarga exitosa")
                return ticker, data
            else:
                logger.warning(f"{ticker}: HTTP {response.status}")
                return ticker, None
    except Exception as e:
        logger.error(f"{ticker}: error {str(e)}")
        return ticker, None

async def descargar_multiples_activos(tickers):
    """Descarga datos de múltiples activos concurrentemente."""
    async with aiohttp.ClientSession() as session:
        tareas = [descargar_datos_activo(session, ticker) for ticker in tickers]
        resultados = await asyncio.gather(*tareas)
    return dict(resultados)

# Ejecutar
# tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'JPM']
# datos = asyncio.run(descargar_multiples_activos(tickers))
```

### 1.4 Threading para Cálculos Pesados

Para tareas CPU-intensivas (backtests, simulaciones Monte Carlo, entrenamiento de modelos), usa `ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def backtest_estrategia(parametros):
    """Función que ejecuta un backtest con parámetros específicos."""
    ventana, umbral = parametros
    import time
    time.sleep(0.1)  # Simular trabajo (en realidad: cálculo real)
    resultado = np.random.random()
    return {'ventana': ventana, 'umbral': umbral, 'sharpe': resultado}

def ejecutar_backtests_paralelos():
    """Ejecuta múltiples backtests en paralelo usando threads."""
    combinaciones = [(v, u) for v in [20, 40, 60, 80] for u in [0.0, 0.01, 0.02]]
    resultados = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futuros = {executor.submit(backtest_estrategia, comb): comb for comb in combinaciones}
        
        for futuro in as_completed(futuros):
            resultado = futuro.result()
            resultados.append(resultado)
            logger.info(f"Backtest completado: ventana={resultado['ventana']}, sharpe={resultado['sharpe']:.4f}")
    
    return resultados

# En producción:
# resultados = ejecutar_backtests_paralelos()
```

### 1.5 Pipeline Automatizado de Datos

Un pipeline típico de desk cuantitativo:

```
Descarga diaria → Validación → Almacenamiento → Cálculo de señales → Alertas
```

```python
class PipelineFinanciero:
    """Pipeline automatizado para datos financieros."""
    
    def __init__(self, db_path='finanzas.db'):
        self.conexion = sqlite3.connect(db_path)
        self.crear_tablas()
    
    def crear_tablas(self):
        cursor = self.conexion.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS precios (
                fecha TEXT, ticker TEXT, cierre REAL, volumen INTEGER,
                PRIMARY KEY (fecha, ticker)
            );
            CREATE TABLE IF NOT EXISTS senales (
                fecha TEXT, ticker TEXT,
                momentum_3m REAL, vol_20d REAL, sma_50 REAL,
                senal TEXT,
                PRIMARY KEY (fecha, ticker)
            );
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT, ticker TEXT, tipo TEXT, mensaje TEXT
            );
        """)
        self.conexion.commit()
        logger.info("Tablas verificadas/creadas")
    
    def validar_datos(self, df):
        """Valida datos antes de insertar: no negativos, no nulos, fechas válidas."""
        if df['cierre'].isna().any():
            logger.warning(f"Datos con NaN detectados en columna 'cierre'")
            df = df.dropna(subset=['cierre'])
        if (df['cierre'] <= 0).any():
            logger.error("Precios negativos o cero detectados")
            return None
        return df
    
    def insertar_precios(self, df):
        """Inserta precios evitando duplicados."""
        df = self.validar_datos(df)
        if df is None:
            return
        
        for _, row in df.iterrows():
            self.conexion.execute(
                """INSERT OR REPLACE INTO precios (fecha, ticker, cierre, volumen)
                   VALUES (?, ?, ?, ?)""",
                (row['fecha'], row['ticker'], row['cierre'], row.get('volumen', 0))
            )
        self.conexion.commit()
        logger.info(f"{len(df)} registros insertados")
    
    def calcular_senales(self):
        """Calcula señales para todos los tickers."""
        query = """
            SELECT fecha, ticker, cierre
            FROM precios
            ORDER BY ticker, fecha
        """
        df = pd.read_sql(query, self.conexion)
        
        for ticker in df['ticker'].unique():
            mask = df['ticker'] == ticker
            df_ticker = df[mask].copy()
            df_ticker.set_index('fecha', inplace=True)
            
            # Calcular indicadores
            df_ticker['momentum_3m'] = df_ticker['cierre'] / df_ticker['cierre'].shift(63) - 1
            df_ticker['vol_20d'] = df_ticker['cierre'].pct_change().rolling(20).std()
            df_ticker['sma_50'] = df_ticker['cierre'].rolling(50).mean()
            
            # Generar señal
            df_ticker['senal'] = 'NEUTRAL'
            df_ticker.loc[
                (df_ticker['momentum_3m'] > 0.05) &
                (df_ticker['cierre'] > df_ticker['sma_50']),
                'senal'
            ] = 'COMPRA'
            df_ticker.loc[
                df_ticker['momentum_3m'] < -0.05,
                'senal'
            ] = 'VENTA'
            
            # Guardar señales
            for idx, row in df_ticker.dropna().iterrows():
                self.conexion.execute(
                    """INSERT OR REPLACE INTO senales
                       (fecha, ticker, momentum_3m, vol_20d, sma_50, senal)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (idx, ticker, row['momentum_3m'], row['vol_20d'], row['sma_50'], row['senal'])
                )
        
        self.conexion.commit()
        logger.info("Señales recalculadas para todos los tickers")
    
    def generar_alertas(self):
        """Genera alertas basadas en las señales calculadas."""
        # Obtener señales de hoy
        query = """
            SELECT s.ticker, s.senal, s.momentum_3m
            FROM senales s
            WHERE s.fecha = (SELECT MAX(fecha) FROM senales)
            AND s.senal != 'NEUTRAL'
            ORDER BY ABS(s.momentum_3m) DESC
        """
        df = pd.read_sql(query, self.conexion)
        
        alertas_generadas = []
        for _, row in df.iterrows():
            mensaje = f"{row['ticker']}: señal {row['senal']} (momentum 3m: {row['momentum_3m']:.2%})"
            self.conexion.execute(
                "INSERT INTO alertas (fecha, ticker, tipo, mensaje) VALUES (?, ?, ?, ?)",
                (datetime.now().strftime('%Y-%m-%d'), row['ticker'], row['senal'], mensaje)
            )
            alertas_generadas.append(mensaje)
        
        self.conexion.commit()
        logger.info(f"{len(alertas_generadas)} alertas generadas")
        return alertas_generadas
    
    def enviar_alertas_email(self, alertas, destinatario="trader@fondocuant.com"):
        """Envía alertas por email."""
        if not alertas:
            logger.info("Sin alertas para enviar")
            return
        
        cuerpo = "=== ALERTAS DE TRADING ===\n\n"
        cuerpo += "\n".join(f"• {a}" for a in alertas)
        
        msg = MIMEText(cuerpo)
        msg['Subject'] = f"Alertas de Trading — {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = 'pipeline@fondocuant.com'
        msg['To'] = destinatario
        
        try:
            # En producción, configurar SMTP real
            # with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            #     servidor.starttls()
            #     servidor.login('user', 'password')
            #     servidor.send_message(msg)
            logger.info(f"Alertas enviadas a {destinatario}")
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
    
    def ejecutar_pipeline_diario(self):
        """Ejecuta el pipeline completo."""
        logger.info("=== PIPELINE DIARIO INICIADO ===")
        
        # 1. Descargar nuevos datos
        logger.info("1/4 Descargando datos...")
        # datos_nuevos = asyncio.run(self.descargar_datos_diarios())
        
        # 2. Insertar en BD
        logger.info("2/4 Insertando datos...")
        # self.insertar_precios(datos_nuevos)
        
        # 3. Recalcular señales
        logger.info("3/4 Calculando señales...")
        self.calcular_senales()
        
        # 4. Generar y enviar alertas
        logger.info("4/4 Generando alertas...")
        alertas = self.generar_alertas()
        self.enviar_alertas_email(alertas)
        
        logger.info("=== PIPELINE COMPLETADO ===")
    
    def cerrar(self):
        self.conexion.close()
```

### 1.6 Programación con APScheduler (Cron Jobs)

```python
from apscheduler.schedulers.background import BackgroundScheduler

# Scheduler para ejecución diaria
scheduler = BackgroundScheduler()

# Pipeline diario: 6:00 PM (después del cierre del mercado)
# scheduler.add_job(pipeline.ejecutar_pipeline_diario, 'cron', hour=18, minute=0)

# Alternativa: cada X minutos
# scheduler.add_job(pipeline.ejecutar_pipeline_diario, 'interval', minutes=60)

# scheduler.start()

# Para detener:
# scheduler.shutdown()
```

### 1.7 Docker Básico para Despliegue

```dockerfile
# Dockerfile para el pipeline
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para ejecutar el pipeline
CMD ["python", "pipeline.py"]
```

```python
# docker-compose.yml
"""
version: '3.8'
services:
  pipeline:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - DB_PATH=/app/data/finanzas.db
    restart: unless-stopped
"""
```

### 1.8 CI/CD con GitHub Actions

```yaml
# .github/workflows/tests.yml
"""
name: Tests y Lint

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: ruff check .
"""
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Pipeline diario de señales

**Concepto financiero:** En un fondo cuantitativo, cada día después del cierre se recalculan todas las señales para decidir las operaciones del día siguiente.

**Código:**

```python
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('demo')

# Crear pipeline con datos demo
pipeline = PipelineFinanciero(':memory:')

# Simular inserción de datos diarios
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL']

for ticker in tickers:
    fechas = pd.date_range('2024-11-01', '2024-12-31', freq='B')
    precio_base = np.random.uniform(100, 350)
    precios = precio_base * np.exp(np.cumsum(np.random.normal(0.0002, 0.012, len(fechas))))
    
    df_ticker = pd.DataFrame({
        'fecha': fechas.strftime('%Y-%m-%d'),
        'ticker': ticker,
        'cierre': precios.round(2),
        'volumen': np.random.randint(1e6, 10e6, len(fechas))
    })
    pipeline.insertar_precios(df_ticker)

# Calcular señales
pipeline.calcular_senales()

# Ver señales
df_senales = pd.read_sql(
    "SELECT fecha, ticker, ROUND(momentum_3m * 100, 2) as mom_pct, senal FROM senales WHERE fecha = (SELECT MAX(fecha) FROM senales)",
    pipeline.conexion
)
print("=== Señales del último día ===\n")
print(df_senales.to_string(index=False))

# Generar alertas
alertas = pipeline.generar_alertas()
print(f"\nAlertas generadas: {len(alertas)}")
for a in alertas:
    print(f"  • {a}")

pipeline.cerrar()
```

**Output:**
```
=== Señales del último día ===

fecha       ticker  mom_pct  senal
2024-12-31  AAPL      3.42  NEUTRAL
2024-12-31  MSFT      6.78  COMPRA
2024-12-31  GOOGL    -7.23  VENTA

Alertas generadas: 2
  • MSFT: señal COMPRA (momentum 3m: 6.78%)
  • GOOGL: señal VENTA (momentum 3m: -7.23%)
```

---

## 3. Aplicación en Finanzas 💰

**Citadel:** Sus sistemas de producción procesan millones de mensajes de mercado por segundo. El pipeline de datos incluye: ingestión de exchanges → normalización → almacenamiento en tiempo real → modelos de ML que recalculan señales en microsegundos.

**Two Sigma:** Su infraestructura incluye miles de servidores, petabytes de almacenamiento, y un sistema de logging que registra cada decisión de trading para cumplimiento regulatorio.

**JP Morgan:** Los desks de trading tienen pipelines que descargan datos de Bloomberg, Reuters, y fuentes internas. Las señales de risk management se recalculan intra-día. Si un límite de VaR se viola, saltan alertas automáticas al Chief Risk Officer.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-9/U40_ejercicios.py`

1. **Logging jerárquico:** Configurar logging con 3 handlers: archivo (DEBUG), consola (INFO), y email (ERROR). Crear funciones que simulen un pipeline y logueen en cada nivel.

2. **Descarga asíncrona simulada:** Implementar una función asíncrona que "descargue" datos para 10 tickers concurrentemente. Medir el tiempo vs descarga secuencial.

3. **Pipeline con base de datos:** Implementar la clase PipelineFinanciero con datos simulados. Insertar datos, calcular señales y generar alertas. Verificar que las tablas se crearon correctamente con queries SQL.

4. **Scheduler y automatización:** Simular la ejecución diaria del pipeline 3 días consecutivos (sin esperar realmente). Verificar que los datos nuevos se acumulan y las señales se actualizan.

---

## 5. Resumen

| Concepto | Código / Herramienta |
|----------|---------------------|
| Logging | `logging.basicConfig(level=logging.INFO)` |
| asyncio | `async def`, `await`, `asyncio.gather()` |
| aiohttp | `aiohttp.ClientSession()` para HTTP asíncrono |
| ThreadPoolExecutor | `concurrent.futures.ThreadPoolExecutor(max_workers=4)` |
| SQLite | `sqlite3.connect()`, `CREATE TABLE IF NOT EXISTS` |
| INSERT OR REPLACE | `INSERT OR REPLACE INTO` (upsert en SQLite) |
| APScheduler | `BackgroundScheduler().add_job(func, 'cron', hour=18)` |
| Docker | `FROM python:3.12-slim`, `CMD ["python", "pipeline.py"]` |
| GitHub Actions | `.github/workflows/tests.yml` |
| Email alerts | `smtplib.SMTP()`, `MIMEText` |

---

## ✅ Autoevaluación

1. ¿Por qué usarías `asyncio` en lugar de `threading` para descargas de datos?
2. ¿Qué ventaja tiene `INSERT OR REPLACE` sobre `INSERT` simple en un pipeline diario?
3. Explica la diferencia entre log level DEBUG, INFO, WARNING y ERROR. ¿Cuál usarías en producción?
4. ¿Para qué sirve `ThreadPoolExecutor` y en qué se diferencia de ejecutar tareas secuencialmente?
5. ¿Por qué un scheduler tipo APScheduler es preferible a un script con `time.sleep()` en un bucle infinito?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Logging > print. Usa logging con niveles, handlers y formateo de timestamps.
> - asyncio para I/O (descargas, queries). ThreadPoolExecutor para CPU (cálculos).
> - Pipeline típico: descarga → validación → almacenamiento → señales → alertas
> - `INSERT OR REPLACE` evita duplicados en pipelines diarios (upsert)
> - Docker + GitHub Actions = CI/CD reproducible. El modelo corre igual en tu laptop y en un servidor.
