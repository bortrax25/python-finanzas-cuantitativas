# U00: Preparando tu Entorno de Trabajo Profesional

> **Próxima unidad:** [U01: Jupyter Notebooks y el Flujo de Trabajo Cuantitativo](./U01-jupyter.md)

---

## 1. Teoría: ¿Qué necesitas para programar en finanzas?

### 1.1 Python

Python es un lenguaje interpretado, de alto nivel y propósito general. Es el estándar en finanzas cuantitativas, ciencia de datos y machine learning. Bancos como JP Morgan, Citadel y Jane Street lo usan diariamente para pricing, risk management y algorithmic trading.

**Versión recomendada:** Python 3.12 o superior. Verifica con:

```bash
python3 --version
```

### 1.2 Editor de código: VS Code

Visual Studio Code (VS Code) es gratuito, ligero y tiene extensiones potentes para Python.

**Extensiones imprescindibles:**
- **Python** (Microsoft) — soporte básico del lenguaje
- **Pylance** — autocompletado inteligente y type checking
- **Jupyter** — notebooks dentro de VS Code

### 1.3 Entornos virtuales (`venv`)

Un entorno virtual aísla las dependencias de cada proyecto. En finanzas, es crítico: un proyecto de pricing de opciones puede necesitar `scipy==1.11` mientras que otro de ML requiere `scipy==1.12`. Sin `venv`, hay conflicto.

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar (macOS/Linux)
source .venv/bin/activate

# Activar (Windows)
.venv\Scripts\activate

# Verificar que estás dentro
which python
# → .../ZED/.venv/bin/python

# Desactivar
deactivate
```

> ⚠️ Cada vez que abras una terminal nueva, activa el entorno: `source .venv/bin/activate`

### 1.4 `pip` — Instalador de paquetes

`pip` es el gestor de paquetes de Python. Los quants instalan librerías como `numpy`, `pandas` y `scipy` con él.

```bash
# Instalar paquetes
pip install numpy pandas matplotlib

# Instalar versión específica
pip install scipy==1.11.0

# Ver paquetes instalados
pip list

# Guardar dependencias del proyecto
pip freeze > requirements.txt

# Instalar desde requirements.txt
pip install -r requirements.txt

# Actualizar pip mismo
pip install --upgrade pip
```

### 1.5 Git — Control de versiones

En banca de inversión, todo el código vive en Git. JP Morgan exige que cada modelo esté versionado. Si pierdes un archivo sin Git, pierdes días de trabajo. Si rompes algo, `git checkout` te salva.

```bash
# Inicializar repositorio
git init

# Ver estado
git status

# Agregar archivos al staging
git add archivo.py
git add .                    # Agregar todo

# Crear commit (foto del proyecto)
git commit -m "feat: agregar calculadora de bonos"

# Ver historial
git log --oneline

# Volver a versión anterior
git checkout <hash-del-commit> -- archivo.py

# Crear .gitignore (archivos que NO van a Git)
echo ".venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

**Commits convencionales** (estándar en la industria):
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` documentación
- `refactor:` reestructuración sin cambiar comportamiento

### 1.6 Ruff (linter) y Black (formatter)

En un desk de trading, el código limpio no es opcional. Un error de indentación puede costar millones.

**Ruff:** linter ultrarrápido que detecta errores, código no usado y malas prácticas.

```bash
pip install ruff
ruff check archivo.py
ruff check --fix archivo.py   # Corregir automáticamente
```

**Black:** formatter que aplica un estilo consistente sin discusiones.

```bash
pip install black
black archivo.py              # Formatear
black --check archivo.py      # Solo verificar
```

> 💡 Configura VS Code para ejecutar Ruff al guardar: Settings → "format on save" + "ruff" como linter.

### 1.7 Estructura profesional de proyecto

Un proyecto cuantitativo serio sigue esta estructura:

```
mi-finanzas/
├── .venv/                  # Entorno virtual (NO se commitea)
├── .gitignore              # Archivos a ignorar por Git
├── README.md               # Descripción del proyecto
├── requirements.txt        # Dependencias del proyecto
├── datos/                  # Datos de mercado (CSV, JSON)
├── notebooks/              # Jupyter Notebooks exploratorios
├── src/                    # Código fuente
│   ├── __init__.py
│   ├── pricing.py          # Funciones de valoración
│   ├── riesgo.py           # Cálculo de riesgo
│   └── utils.py            # Utilidades generales
└── tests/                  # Tests unitarios
    └── test_pricing.py
```

### 1.8 ¿Qué hace un analista cuantitativo día a día?

Un quant en Citadel o Jane Street típicamente:

1. **Morning meeting (8:00):** revisa P&L del día anterior, riesgo de portafolio, eventos macro
2. **Research (9:00-12:00):** explora datos en Jupyter, prueba hipótesis, backtestea estrategias
3. **Implementación (13:00-16:00):** escribe código en Python (pricing, señales, risk checks)
4. **Code review (16:00-17:00):** revisa PRs de compañeros, discute edge cases
5. **Cierre (17:00):** verifica posiciones, actualiza dashboards, commitea cambios

En JP Morgan IBD, un analista pasa el día construyendo modelos DCF/LBO en Excel... pero cada vez más se migra a Python por trazabilidad y escalabilidad.

---

## 2. Práctica

### 2.1 Instalar Python

**En macOS:**

```bash
# Opción 1: Homebrew (recomendado)
brew install python@3.12

# Opción 2: Descargar de python.org
# https://www.python.org/downloads/
```

Verifica:
```bash
python3 --version
# Python 3.12.x
```

### 2.2 Instalar VS Code

```bash
brew install --cask visual-studio-code
```

O descarga desde: https://code.visualstudio.com/

### 2.3 Crear el proyecto desde cero

```bash
# Crear carpeta
mkdir ~/Desktop/mi-finanzas
cd ~/Desktop/mi-finanzas

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Inicializar Git
git init

# Crear estructura
mkdir -p datos notebooks src tests

# Crear README.md
echo "# Mi Proyecto de Finanzas Cuantitativas" > README.md
echo "" >> README.md
echo "Herramientas para análisis financiero y valoración." >> README.md

# Crear .gitignore
cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
.ipynb_checkpoints/
EOF

# Instalar dependencias
pip install jupyter numpy pandas matplotlib

# Guardar dependencias
pip freeze > requirements.txt

# Crear primer archivo
cat > src/__init__.py << 'EOF'
# paquete mi_finanzas
__version__ = "0.1.0"
EOF

# Primer commit
git add .
git commit -m "feat: estructura inicial del proyecto"
```

### 2.4 Ejercicio guiado: Tu primer script Python

Crea `src/hola_finanzas.py`:

```python
# Mi primer script de finanzas
ticker = "AAPL"
precio = 175.50
cantidad = 100
valor_total = precio * cantidad

print("=" * 40)
print("MI PRIMER CÁLCULO FINANCIERO")
print("=" * 40)
print(f"Ticker: {ticker}")
print(f"Precio por acción: ${precio:,.2f}")
print(f"Cantidad: {cantidad}")
print(f"Valor total: ${valor_total:,.2f}")
```

Ejecuta:
```bash
python3 src/hola_finanzas.py
```

Output:
```
========================================
MI PRIMER CÁLCULO FINANCIERO
========================================
Ticker: AAPL
Precio por acción: $175.50
Cantidad: 100
Valor total: $17,550.00
```

### 2.5 Probar Ruff y Black

```bash
# Instalar
pip install ruff black

# Lint
ruff check src/hola_finanzas.py

# Formatear
black src/hola_finanzas.py
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 ¿Por qué los bancos de inversión exigen control de versiones?

Imagina que estás modelando un LBO de $2B para JP Morgan PE:
- 5 analistas modifican el mismo modelo
- El MD pide cambios de último minuto antes del pitch
- Sin Git: caos de archivos `modelo_v2_final_FINAL_v3.xlsx`
- Con Git: historial limpio, blame para saber quién cambió qué, branches por escenario

**Reguladores (SEC, FCA) exigen trazabilidad.** Si el modelo tiene un error y pierdes $50M, necesitas saber exactamente qué commit introdujo el bug.

### 3.2 Flujo de trabajo real en un desk

```bash
# Mañana típica en un desk cuantitativo
git pull origin main                    # Bajar cambios del equipo
git checkout -b feat/nuevo-factor       # Rama para nueva feature
# ... investigar, codear, testear ...
ruff check src/ && black src/           # Lint + format
pytest tests/                           # Correr tests
git add . && git commit -m "feat: factor momentum 12-1"
git push origin feat/nuevo-factor       # Subir para code review
```

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-0/U00_ejercicios.py`

1. **Crear proyecto mi-finanzas:** Sigue la guía de la Sección 2.3 para crear la estructura completa. Verifica que `git status` muestre "nothing to commit, working tree clean" después del commit inicial.

2. **Linter y formatter:** Ejecuta `ruff check` y `black --check` sobre tu proyecto. Corrige cualquier warning.

3. **Comandos de Git:** Simula un flujo: crea un archivo `src/utilidades.py`, haz commit, modifícalo, ve el diff con `git diff`, haz commit de la modificación y revisa el log.

4. **requirements.txt:** Agrega `yfinance` a tu proyecto con `pip install`, actualiza `requirements.txt` con `pip freeze > requirements.txt` y verifica que el archivo refleje los cambios.

---

## 5. Resumen

| Concepto | Comando / Herramienta |
|---------|----------------------|
| Entorno virtual | `python3 -m venv .venv` |
| Activar venv | `source .venv/bin/activate` |
| Instalar paquetes | `pip install <paquete>` |
| Guardar dependencias | `pip freeze > requirements.txt` |
| Inicializar Git | `git init` |
| Guardar cambios | `git add . && git commit -m "mensaje"` |
| Linter | `ruff check archivo.py` |
| Formatter | `black archivo.py` |
| Extensiones VS Code | Python, Pylance, Jupyter |

---

## ✅ Autoevaluación

1. ¿Qué comando usas para verificar tu versión de Python?
2. ¿Por qué los bancos de inversión exigen control de versiones?
3. ¿Cuál es la diferencia entre `venv` y el Python del sistema?
4. ¿Qué hace `pip freeze > requirements.txt`?
5. Crea y ejecuta un archivo que imprima tu nombre, tu meta de aprendizaje y la fecha actual.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `reference-U00.md`: Ruta del proyecto, comandos de activación del venv, estructura de carpetas
> - `project-U00.md`: Objetivo del curso, herramientas instaladas, flujo de trabajo Git
