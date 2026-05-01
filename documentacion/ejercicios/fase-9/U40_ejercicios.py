# U40: EJERCICIOS — Infraestructura y Producción

# ============================================================
# Ejercicio 1: Logging jerárquico
# Configura un sistema de logging con 3 handlers:
#   - FileHandler: guarda DEBUG y superior en 'pipeline.log'
#   - StreamHandler: muestra INFO y superior en consola
#   - Handler personalizado: para ERROR, simula envío de email
#     (guarda los mensajes en una lista email_enviados)
# Crea funciones simuladas:
#   - descargar_datos(): descarga exitosa (INFO) o fallida (ERROR)
#   - validar_datos(): valida con warnings (WARNING) o todo OK (INFO)
#   - calcular_senales(): siempre exitoso (DEBUG al inicio, INFO al final)
# Simula un pipeline completo llamando estas funciones.
# Verifica que los logs aparecen en los lugares correctos.
# ============================================================
import logging
import sys

print("=== Ejercicio 1: Logging Jerárquico ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 1: Logging Jerárquico ===
# [Consola] INFO — Pipeline iniciado
# [Consola] INFO — Datos descargados: 5 tickers
# [Consola] INFO — Validación completada: 0 anomalías
# [Consola] INFO — Señales calculadas: 5 tickers
# [Consola] INFO — Pipeline completado
# [Archivo] DEBUG — Iniciando descarga de datos...
# [Archivo] ERROR — Falló la descarga de TSLA
# [Archivo] WARNING — Valores atípicos detectados en AAPL
# [Email simulado] ERROR — Falló descarga de TSLA


# ============================================================
# Ejercicio 2: Descarga asíncrona simulada
# Implementa dos versiones de una función que "descarga"
# datos para 15 tickers (simula con time.sleep(0.1)):
#   (a) Versión secuencial: descarga uno por uno
#   (b) Versión asíncrona: descarga concurrente con asyncio
# Mide el tiempo de ejecución de ambas.
# Calcula el speedup (tiempo_secuencial / tiempo_asincrono).
# ============================================================
import asyncio
import time

print("\n=== Ejercicio 2: Descarga Asíncrona Simulada ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 2: Descarga Asíncrona Simulada ===
# Tiempo secuencial:  1.52s (15 tickers)
# Tiempo asíncrono:   0.12s (15 tickers concurrentes)
# Speedup: 12.7x


# ============================================================
# Ejercicio 3: Pipeline con base de datos
# Implementa una clase PipelineSimplificado que:
#   (a) Crea tablas 'precios' y 'senales' en SQLite (CREATE TABLE IF NOT EXISTS)
#   (b) Método insertar_precios(): inserta datos simulados (5 tickers x 100 días)
#       usando INSERT OR REPLACE para evitar duplicados
#   (c) Método calcular_senales():
#       - momentum_20d = (precio / precio_hace_20dias - 1) * 100
#       - senal = 'COMPRA' si momentum > 3, 'VENTA' si < -3, else 'NEUTRAL'
#   (d) Método consultar_senales(): retorna las señales de la última fecha
# Ejecuta el pipeline y muestra las señales generadas.
# ============================================================
import sqlite3
import pandas as pd
import numpy as np

print("\n=== Ejercicio 3: Pipeline con Base de Datos ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 3: Pipeline con Base de Datos ===
# Datos insertados: 500 registros (5 tickers x 100 días)
# Señales calculadas: 400 registros con señal
# Señales última fecha:
#   AAPL   | mom_20d=+4.2%  | COMPRA
#   MSFT   | mom_20d=-3.8%  | VENTA
#   GOOGL  | mom_20d=+1.2%  | NEUTRAL
#   TSLA   | mom_20d=+5.7%  | COMPRA
#   JPM    | mom_20d=-5.1%  | VENTA


# ============================================================
# Ejercicio 4: Scheduler y automatización
# Simula la ejecución diaria de un pipeline durante 3 "días"
# (sin esperar tiempo real, solo itera 3 veces).
# En cada día:
#   (a) Genera 5 precios nuevos (aleatorios) para cada ticker
#   (b) Insértalos en la BD (usa la clase del ejercicio 3)
#   (c) Recalcula señales
#   (d) Verifica que los datos se acumulan (más filas cada día)
# Muestra cuántos registros totales hay al final del día 3.
# ============================================================
print("\n=== Ejercicio 4: Scheduler y Automatización ===")

# Escribe tu código aquí



# Output esperado:
# === Ejercicio 4: Scheduler y Automatización ===
# Día 1: 500 registros totales
# Día 2: 505 registros totales (+5 nuevos)
# Día 3: 510 registros totales (+5 nuevos)
# Pipeline diario completado 3 veces.
