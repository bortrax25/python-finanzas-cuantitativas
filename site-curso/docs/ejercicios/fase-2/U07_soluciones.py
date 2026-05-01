# U07: SOLUCIONES — Listas y Tuplas: Series de Precios y Registros Financieros

# ============================================================
# Ejercicio 1: Rastreador de Portafolio
# ============================================================
print("=== Ejercicio 1: Rastreador de Portafolio ===")
portafolio = [
    ("AAPL", 10, 150.00),
    ("MSFT", 5, 280.00),
    ("TSLA", 3, 900.00),
    ("JPM", 20, 135.00),
]
precios_actuales = {"AAPL": 175.00, "MSFT": 310.00, "TSLA": 820.00, "JPM": 142.00}

pl_total = 0
for ticker, cantidad, precio_compra in portafolio:
    precio_actual = precios_actuales[ticker]
    valor_compra = cantidad * precio_compra
    valor_actual = cantidad * precio_actual
    pl = valor_actual - valor_compra
    pl_pct = (pl / valor_compra) * 100
    pl_total += pl
    print(f"{ticker}: {cantidad} × ${precio_compra:.2f} → Actual: ${precio_actual:.2f} | P&L: {pl:+,.2f} ({pl_pct:+.2f}%)")

print(f"P&L Total: {pl_total:+,.2f}")


# ============================================================
# Ejercicio 2: Filtro de oportunidades
# ============================================================
print("\n=== Ejercicio 2: Filtro de Oportunidades ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
    ("PFE", 14, 5),
]

oportunidades = [a for a in acciones if a[1] < 15 and a[2] > 10]
print(f"Oportunidades (PER<15, Crec>10%): {oportunidades}")


# ============================================================
# Ejercicio 3: SMA 5 con Slicing
# ============================================================
print("\n=== Ejercicio 3: SMA 5 con Slicing ===")
precios = [100, 102, 101, 105, 103, 108, 110, 107, 112, 115, 113, 118]

ventana = 5
for i in range(len(precios) - ventana + 1):
    sma = sum(precios[i:i + ventana]) / ventana
    print(f"SMA({ventana}) día {i + ventana}: {sma:.2f}")


# ============================================================
# Ejercicio 4: Estadísticas Financieras
# ============================================================
print("\n=== Ejercicio 4: Estadísticas Financieras ===")
precios_cierre = [100, 102, 105, 98, 103, 108, 95, 102, 110, 105, 99, 106]

# Calcular retornos
retornos = [(precios_cierre[i] - precios_cierre[i-1]) / precios_cierre[i-1] * 100
            for i in range(1, len(precios_cierre))]

# Media
media_ret = sum(retornos) / len(retornos)

# Varianza (n-1)
varianza = sum((r - media_ret) ** 2 for r in retornos) / (len(retornos) - 1)

# Desviación estándar
vol_diaria = varianza ** 0.5

# Volatilidad anualizada
vol_anual = vol_diaria * (252 ** 0.5)

# Max Drawdown
pico = precios_cierre[0]
max_dd = 0
for precio in precios_cierre:
    if precio > pico:
        pico = precio
    dd = (pico - precio) / pico * 100
    if dd > max_dd:
        max_dd = dd

print(f"Media de retornos: {media_ret:.2f}%")
print(f"Volatilidad diaria: {vol_diaria:.2f}%")
print(f"Volatilidad anualizada (x√252): {vol_anual:.2f}%")
print(f"Max Drawdown: {max_dd:.2f}%")
