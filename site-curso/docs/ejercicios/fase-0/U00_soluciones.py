# U00: SOLUCIONES — Preparando tu Entorno de Trabajo Profesional

# ============================================================
# Ejercicio 1: Estructura del Proyecto
# ============================================================
print("=== Ejercicio 1: Estructura del Proyecto ===")

estructura = r"""
mi-finanzas/
├── .gitignore
├── README.md
├── requirements.txt
├── datos/
├── notebooks/
├── src/
│   └── __init__.py
└── tests/
"""
print(estructura.strip())


# ============================================================
# Ejercicio 2: Contenido .gitignore
# ============================================================
print("\n=== Ejercicio 2: Contenido .gitignore ===")

gitignore = """
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
.ipynb_checkpoints/
datos/sensibles/
"""
print(gitignore.strip())


# ============================================================
# Ejercicio 3: Primer Script Financiero
# ============================================================
print("\n=== Ejercicio 3: Primer Script Financiero ===")
ticker = "MSFT"
precio = 310.50
cantidad = 25

valor_total = precio * cantidad

print("=" * 40)
print("MI PRIMER CÁLCULO FINANCIERO")
print("=" * 40)
print(f"Ticker: {ticker}")
print(f"Precio por acción: ${precio:,.2f}")
print(f"Cantidad: {cantidad}")
print(f"Valor total: ${valor_total:,.2f}")


# ============================================================
# Ejercicio 4: Flujo de Trabajo Git
# ============================================================
print("\n=== Ejercicio 4: Flujo de Trabajo Git ===")

flujo_git = [
    ("git status", "Ver el estado del repositorio"),
    ("git add src/pricing.py", "Agregar archivo modificado al staging"),
    ('git commit -m "feat: agregar función de valoración DCF"', "Crear commit con mensaje convencional"),
    ("git log --oneline", "Ver historial de commits"),
]

for comando, descripcion in flujo_git:
    print(f"$ {comando}")
    if descripcion == "Ver historial de commits":
        print("a1b2c3d feat: agregar función de valoración DCF")
        print("e4f5g6h feat: estructura inicial del proyecto")
