# U03: SOLUCIONES — Operadores: La Aritmética de Wall Street

# ============================================================
# Ejercicio 1: Precio promedio ponderado
# ============================================================
print("=== Ejercicio 1: Precio Promedio Ponderado ===")
cantidad1, precio1 = 100, 152.50
cantidad2, precio2 = 50, 148.00
cantidad3, precio3 = 75, 155.00

total_invertido = (cantidad1 * precio1 +
                   cantidad2 * precio2 +
                   cantidad3 * precio3)
total_acciones = cantidad1 + cantidad2 + cantidad3
precio_promedio = total_invertido / total_acciones

print(f"Total invertido: ${total_invertido:,.2f}")
print(f"Total acciones: {total_acciones}")
print(f"Precio promedio: ${precio_promedio:,.2f}")


# ============================================================
# Ejercicio 2: Verificador de stop-loss
# ============================================================
print("\n=== Ejercicio 2: Stop-Loss ===")
precio_entrada = 200.00
stop_loss_pct = 7
precio_actual = 184.00

precio_stop = precio_entrada * (1 - stop_loss_pct / 100)
activado = precio_actual <= precio_stop

print(f"Precio de entrada: ${precio_entrada:,.2f}")
print(f"Stop-loss: ${precio_stop:,.2f} ({stop_loss_pct}%)")
print(f"Precio actual: ${precio_actual:,.2f}")
print(f"¿Stop-loss activado? {activado}")


# ============================================================
# Ejercicio 3: CAGR
# ============================================================
print("\n=== Ejercicio 3: CAGR ===")
valor_inicial = 5000
valor_final = 12000
anios = 8

cagr = (valor_final / valor_inicial) ** (1 / anios) - 1
cagr_pct = cagr * 100

print(f"Valor inicial: ${valor_inicial:,.2f}")
print(f"Valor final: ${valor_final:,.2f}")
print(f"Período: {anios} años")
print(f"CAGR: {cagr_pct:.2f}%")


# ============================================================
# Ejercicio 4: Cuota de hipoteca
# ============================================================
print("\n=== Ejercicio 4: Cuota de Hipoteca ===")
monto = 200000
tasa_anual = 10
plazo_anios = 20

plazo_meses = plazo_anios * 12
tasa_mensual = (tasa_anual / 100) / 12

factor = (1 + tasa_mensual) ** plazo_meses
cuota = monto * (tasa_mensual * factor) / (factor - 1)
total_pagar = cuota * plazo_meses
interes_total = total_pagar - monto

print(f"Monto: ${monto:,.2f}")
print(f"Tasa anual: {tasa_anual}%")
print(f"Plazo: {plazo_anios} años ({plazo_meses} meses)")
print(f"Cuota mensual: ${cuota:,.2f}")
print(f"Total a pagar: ${total_pagar:,.2f}")
print(f"Interés total: ${interes_total:,.2f}")
