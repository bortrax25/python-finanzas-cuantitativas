# U07: SOLUCIONES — Bucle for y range()

# ============================================================
# Ejercicio 1: Promedio móvil simple (SMA)
# ============================================================
print("=== Ejercicio 1: Media Móvil (SMA 3) ===")
precios = [100, 102, 101, 105, 103, 108, 110, 107]

ventana = 3
resultados = []
for i in range(len(precios) - ventana + 1):
    sma = sum(precios[i:i+ventana]) / ventana
    resultados.append(f"Día {i+ventana}: {sma:.2f}")

print(" | ".join(resultados))


# ============================================================
# Ejercicio 2: Máximo drawdown
# ============================================================
print("\n=== Ejercicio 2: Máximo Drawdown ===")
precios = [100, 105, 95, 90, 98, 92, 88, 96]

pico = precios[0]
max_drawdown = 0

for precio in precios:
    if precio > pico:
        pico = precio
    drawdown = (pico - precio) / pico * 100
    if drawdown > max_drawdown:
        max_drawdown = drawdown
    print(f"Precio: ${precio:3} | Pico: ${pico:3} | DD: {drawdown:.2f}%")

print(f"Máximo drawdown: {max_drawdown:.2f}%")


# ============================================================
# Ejercicio 3: Tabla de tasas
# ============================================================
print("\n=== Ejercicio 3: Crecimiento de $1 ===")
tasas = [5, 10, 15]
anios = range(1, 11)

print(f"{'Año':<5}", end="")
for tasa in tasas:
    print(f"{tasa}%".rjust(8), end="")
print()

for anio in anios:
    print(f"{anio:<5}", end="")
    for tasa in tasas:
        vf = (1 + tasa / 100) ** anio
        print(f"${vf:>7.2f}", end="")
    print()


# ============================================================
# Ejercicio 4: Clasificador de velas
# ============================================================
print("\n=== Ejercicio 4: Clasificador de Velas ===")
datos = [
    (100, 105),
    (105, 102),
    (102, 108),
    (108, 106),
    (106, 110),
    (110, 110),
    (110, 107),
    (107, 103),
]

verdes = rojas = doji = 0

for dia, (apertura, cierre) in enumerate(datos, start=1):
    if cierre > apertura:
        tipo = "VELA VERDE"
        verdes += 1
    elif cierre < apertura:
        tipo = "VELA ROJA"
        rojas += 1
    else:
        tipo = "DOJI"
        doji += 1
    print(f"Día {dia}: Abre ${apertura} | Cierra ${cierre} → {tipo}")

print(f"Verdes: {verdes} | Rojas: {rojas} | Doji: {doji}")
