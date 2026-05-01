# U06: SOLUCIONES — Bucles: Iterando sobre Series de Tiempo

# ============================================================
# Ejercicio 1: SMA y Golden Cross
# ============================================================
print("=== Ejercicio 1: SMA y Golden Cross ===")
import random
random.seed(101)

precios = [100.0]
for _ in range(49):
    precios.append(precios[-1] * (1 + random.gauss(0.0003, 0.012)))

ventana_corta = 5
ventana_larga = 20

sma_corta = []
sma_larga = []

for i in range(len(precios)):
    if i >= ventana_corta - 1:
        sma = sum(precios[i - ventana_corta + 1 : i + 1]) / ventana_corta
        sma_corta.append(sma)
    else:
        sma_corta.append(None)

    if i >= ventana_larga - 1:
        sma = sum(precios[i - ventana_larga + 1 : i + 1]) / ventana_larga
        sma_larga.append(sma)
    else:
        sma_larga.append(None)

# Detectar Golden Cross
cruce_detectado = False
for dia in range(ventana_larga, len(precios)):
    if sma_corta[dia] is None or sma_larga[dia] is None:
        continue
    if (sma_corta[dia - 1] is not None and sma_larga[dia - 1] is not None
            and sma_corta[dia - 1] <= sma_larga[dia - 1]
            and sma_corta[dia] > sma_larga[dia]):
        print(f"Primer Golden Cross detectado en día {dia + 1}")
        print(f"  SMA({ventana_corta}): ${sma_corta[dia]:.2f} | SMA({ventana_larga}): ${sma_larga[dia]:.2f}")
        print(f"  Precio: ${precios[dia]:.2f}")
        cruce_detectado = True
        break

if not cruce_detectado:
    print("Sin cruce en los datos generados")


# ============================================================
# Ejercicio 2: TIR por Bisección
# ============================================================
print("\n=== Ejercicio 2: TIR por Bisección ===")
flujos = [-2000, 600, 700, 800, 900]
tasa_min = 0.0
tasa_max = 1.0
tolerancia = 0.0001

while (tasa_max - tasa_min) > tolerancia:
    tasa_media = (tasa_min + tasa_max) / 2
    vpn = sum(flujo / (1 + tasa_media) ** t for t, flujo in enumerate(flujos))
    if vpn > 0:
        tasa_min = tasa_media
    else:
        tasa_max = tasa_media

tir = (tasa_min + tasa_max) / 2
vpn_final = sum(flujo / (1 + tir) ** t for t, flujo in enumerate(flujos))

print(f"TIR encontrada: {tir:.4%}")
print(f"VPN a la TIR: ${vpn_final:,.2f}")


# ============================================================
# Ejercicio 3: Ruina del jugador
# ============================================================
print("\n=== Ejercicio 3: Ruina del Jugador ===")
random.seed(42)

capital = 1000
objetivo_ganar = 2000
apuesta = 100
trades = 0

while capital > 0 and capital < objetivo_ganar:
    trades += 1
    if random.random() < 0.5:
        capital += apuesta
        print(f"Trade {trades}: Ganaste → ${capital}")
    else:
        capital -= apuesta
        print(f"Trade {trades}: Perdiste → ${capital}")

resultado = "GANASTE" if capital >= objetivo_ganar else "PERDISTE"
print(f"Resultado: {resultado} en {trades} trades")


# ============================================================
# Ejercicio 4: Máximo Drawdown
# ============================================================
print("\n=== Ejercicio 4: Máximo Drawdown ===")
precios = [100, 105, 98, 92, 96, 88, 94, 85, 90, 82, 87, 95]

pico = precios[0]
max_drawdown = 0
pos_pico = 0
pos_valle = 0

for i, precio in enumerate(precios):
    if precio > pico:
        pico = precio
        pos_pico = i
    drawdown = (pico - precio) / pico * 100
    if drawdown > max_drawdown:
        max_drawdown = drawdown
        pos_valle = i

print(f"Máximo drawdown: {max_drawdown:.2f}%")
print(f"Pico: ${pico:.2f} en posición {pos_pico + 1}")
print(f"Valle: ${precios[pos_valle]:.2f} en posición {pos_valle + 1}")
