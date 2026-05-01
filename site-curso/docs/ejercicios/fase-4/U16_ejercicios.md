# 📝 Ejercicios: U16 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U16_ejercicios)

---

```python
# U16: EJERCICIOS — Herencia y Polimorfismo

# ============================================================
# Ejercicio 1: Jerarquía de instrumentos financieros
# Crea:
#   - Clase abstracta Instrumento(ABC) con:
#       __init__(self, ticker, nombre)
#       @abstractmethod valorar(self) -> float
#       @abstractmethod tipo_instrumento(self) -> str
#       resumen(self) -> str (método concreto)
#   - Accion(Instrumento): precio, cantidad. valorar = precio * cantidad
#   - Bono(Instrumento): valor_nominal, cupon, vencimiento, tasa_descuento.
#       valorar = VP de flujos
#   - Opcion(Instrumento): tipo (CALL/PUT), strike, spot, plazo, tasa, vol.
#       valorar = valor intrínseco (sin modelo, solo max(0, spot-strike) * 100)
# Prueba con los 3 tipos.
# ============================================================
print("=== Ejercicio 1: Jerarquía de instrumentos ===")

# Escribe tu código aquí



# Output esperado:
# AAPL | Renta Variable | Valor: $17,500.00
# UST10Y | Renta Fija | Valor: $1,081.11
# AAPL200C | Derivado | Valor: $0.00


# ============================================================
# Ejercicio 2: Portafolio polimórfico
# Crea la clase Portafolio que:
#   - __init__(self, nombre)
#   - agregar(self, instrumento: Instrumento)
#   - valor_total(self) -> float
#   - composicion_por_tipo(self) -> dict: {"Accion": 50000, "Bono": 30000, ...}
#   - instrumento_mayor_valor(self) -> Instrumento
#   - __str__(self) -> tabla resumen con todos los instrumentos
# Crea un portafolio con 2 acciones, 2 bonos y 1 opción.
# ============================================================
print("\\n=== Ejercicio 2: Portafolio polimórfico ===")
# Reutiliza las clases del Ejercicio 1

# Escribe tu código aquí



# Output esperado:
# Portafolio: Multi-Asset
# Ticker     Tipo            Valor
# ---------------------------------------
# AAPL       Renta Variable  $17,500.00
# MSFT       Renta Variable  $15,500.00
# UST10Y     Renta Fija      $1,081.11
# CORP5Y     Renta Fija      $1,040.60
# AAPL200C   Derivado        $0.00
# ---------------------------------------
# Valor Total: $35,121.71
# Mayor posición: AAPL ($17,500.00)
# Composición: {'Accion': 33000.0, 'Bono': 2121.71, 'Opcion': 0.0}


# ============================================================
# Ejercicio 3: Mixin Auditable
# Crea un mixin AuditableMixin que:
#   - Tenga un atributo historial (lista de dicts)
#   - Método auditar(self, evento, valor) que agregue {"tipo": self.tipo_instrumento(), "evento": evento, "valor": valor, "timestamp": datetime.now().isoformat()}
#   - Método reporte_auditoria(self) que imprima el historial formateado
# Aplica el mixin a Accion y Bono (herencia múltiple).
# Registra llamadas a valorar() desde el mixin.
# ============================================================
print("\\n=== Ejercicio 3: Mixin Auditable ===")
# Reutiliza las clases del Ejercicio 1

# Escribe tu código aquí



# Output esperado:
# [2024-01-15T10:30:00] Accion AAPL | valoracion | $17,500.00
# [2024-01-15T10:30:00] Bono UST10Y | valoracion | $1,081.11
# [2024-01-15T10:30:00] Accion AAPL | actualizacion | nuevo_precio=180.0
# Total eventos auditados: 3


# ============================================================
# Ejercicio 4: Sistema de pricing por composición
# Crea:
#   - ModeloPrecio (clase base): metodo calcular(self, instrumento) -> float
#   - ModeloLineal(ModeloPrecio): para acciones, calcular = precio * cantidad
#   - ModeloFlujoDescontado(ModeloPrecio): para bonos, VP de flujos
#   - MotorPrecios:
#       __init__(self, modelo: ModeloPrecio)
#       valorar(self, instrumento: Instrumento) -> float  (usa el modelo)
#       cambiar_modelo(self, nuevo_modelo: ModeloPrecio)
# Demuestra que el mismo MotorPrecios valora Accion y Bono con modelos distintos.
# ============================================================
print("\\n=== Ejercicio 4: Sistema de pricing por composición ===")

# Escribe tu código aquí



# Output esperado:
# Motor con ModeloLineal → AAPL: $17,500.00
# Motor con ModeloLineal → MSFT: $9,000.00
# Motor con ModeloFlujoDescontado → UST10Y: $1,081.11
# Motor con ModeloFlujoDescontado → CORP5Y: $1,040.60
```

---

> [📥 Descargar archivo .py](U16_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
