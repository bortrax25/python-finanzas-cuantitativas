# U18: EJERCICIOS — Patrones de Diseño en Finanzas Cuantitativas

# ============================================================
# Ejercicio 1: Pricing Engine con Strategy Pattern
# Implementa:
#   - EstrategiaPrecio(ABC) con @abstractmethod precio(spot, strike, plazo, tasa, vol, tipo)
#   - BSM(EstrategiaPrecio): Black-Scholes-Merton
#   - Binomial(EstrategiaPrecio): CRR con N pasos (default 50)
#   - MotorPrecios: __init__(estrategia), cambiar_estrategia, valorar(**params)
# Valora una opción CALL ATM con spot=100, strike=100, plazo=0.5, tasa=0.05, vol=0.25
# usando los dos modelos y muestra la diferencia.
# ============================================================
print("=== Ejercicio 1: Pricing Engine con Strategy ===")

# Escribe tu código aquí



# Output esperado:
# BSM      CALL ATM (S=100, K=100, T=0.5): $7.5180
# Binomial CALL ATM (S=100, K=100, T=0.5): $7.9783
# Diferencia absoluta: $0.4603


# ============================================================
# Ejercicio 2: Factory de Instrumentos desde JSON simulado
# Implementa:
#   - Instrumento: clase simple con ticker, tipo, atributos (dict)
#   - FabricaInstrumento(ABC): @abstractmethod desde_dict(datos) -> Instrumento
#       + metodo desde_json(texto_json) -> list[Instrumento]
#   - FabricaAccion(FabricaInstrumento): parsea ticker, precio, cantidad, sector
#   - FabricaBono(FabricaInstrumento): parsea ticker, valor_nominal, cupon, vencimiento
#   - crear_fabrica(tipo): factory method que retorne la fábrica correcta
# Crea 2 acciones y 2 bonos desde un JSON simulado (string).
# ============================================================
print("\n=== Ejercicio 2: Factory de Instrumentos ===")

# Escribe tu código aquí



# Output esperado:
# Instrumento(AAPL, Accion, precio=175.0, cantidad=100, sector=Tecnologia)
# Instrumento(JPM, Accion, precio=140.0, cantidad=200, sector=Finanzas)
# Instrumento(UST10Y, Bono, valor_nominal=1000, cupon=0.05, vencimiento=10)
# Instrumento(CORP5Y, Bono, valor_nominal=5000, cupon=0.07, vencimiento=5)
# Total instrumentos creados: 4


# ============================================================
# Ejercicio 3: Observer Pattern — Stop Loss y Take Profit
# Implementa:
#   - Observador(ABC) con @abstractmethod actualizar(ticker, precio)
#   - MarketDataFeed (Sujeto): registrar, eliminar, notificar, actualizar_precio
#   - StopLoss(Observador): ticker, precio_stop. Si precio <= stop, imprime alerta y se autodesregistra
#   - TakeProfit(Observador): ticker, precio_target. Si precio >= target, imprime alerta y se autodesregistra
#   - RegistroPrecios(Observador): guarda todos los precios en una lista
# Simula el siguiente stream de AAPL:
#   150, 155, 162, 158, 168, 165, 172
# con StopLoss en 157 y TakeProfit en 170.
# ============================================================
print("\n=== Ejercicio 3: Observer para Stop Loss / Take Profit ===")

# Escribe tu código aquí



# Output esperado:
# Precio AAPL: $150.00
# Precio AAPL: $155.00
# Precio AAPL: $162.00
# Precio AAPL: $158.00
# 🛑 STOP LOSS AAPL: Precio $158.00 <= Stop $157.00 → VENDER
# Precio AAPL: $168.00
# Precio AAPL: $165.00
# Precio AAPL: $172.00
# ✅ TAKE PROFIT AAPL: Precio $172.00 >= Target $170.00 → VENDER
# Historial de precios registrados: [150.0, 155.0, 162.0, 158.0, 168.0, 165.0, 172.0]


# ============================================================
# Ejercicio 4: Generador de señales RSI
# Implementa:
#   - generar_rsi(precios, periodo=14): generador que recibe lista de precios y
#     para cada día (después del periodo inicial) calcula RSI:
#       RS = ganancia_promedio / perdida_promedio
#       RSI = 100 - (100 / (1 + RS))
#     Emite tupla (dia, precio, rsi) si RSI > 70 ("sobrecompra") o RSI < 30 ("sobreventa"),
#     de lo contrario emite None.
#   - Usa el generador para detectar señales en una serie de 30 precios sintéticos.
# ============================================================
print("\n=== Ejercicio 4: Generador de señales RSI ===")

# Escribe tu código aquí



# Output esperado:
# Serie de 30 precios generada
# Señales detectadas:
# Día 18: Precio=125.85 | RSI=71.2 → SOBRECOMPRA (vender)
# Día 21: Precio=131.42 | RSI=72.8 → SOBRECOMPRA (vender)
# Día 26: Precio=120.15 | RSI=28.5 → SOBREVENTA (comprar)
# Día 28: Precio=118.33 | RSI=26.1 → SOBREVENTA (comprar)
