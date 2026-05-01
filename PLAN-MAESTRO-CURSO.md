# PLAN MAESTRO: Rediseño del Curso "Python para Finanzas Cuantitativas"

> **Propósito de este documento:** Este archivo contiene TODAS las instrucciones necesarias para que un agente de IA completamente independiente (sin contexto previo) pueda ejecutar el rediseño completo del curso. Cada sección es autocontenida. Léelo de arriba a abajo antes de ejecutar.

---

## 1. CONTEXTO DEL PROYECTO

### 1.1 ¿Qué es este proyecto?

Un curso educativo de Python aplicado a finanzas cuantitativas. El estudiante empieza desde cero en Python y termina preparado para roles junior en:
- **Investment Banking** (JP Morgan IBD): DCF, LBO, financial modeling
- **Private Equity** (JP Morgan PE): LBO modeling, valoración, due diligence
- **Quantitative Finance** (Citadel, Jane Street): factor models, ML, trading algorítmico

### 1.2 ¿Dónde vive el proyecto?

```
/Users/miguelangelquispetito/Desktop/ZED/
```

### 1.3 Idioma

Todo el contenido del curso (teoría, ejercicios, comentarios en código) está en **español**. Los nombres de variables y funciones en código usan **snake_case en español** (ej: `tasa_interes`, `precio_compra`). Los nombres de librerías y funciones de Python se mantienen en inglés tal cual son.

### 1.4 Meta del estudiante

Un universitario que al terminar las 43 unidades pueda:
1. Valorizar empresas como un analista de JP Morgan
2. Construir modelos LBO como un asociado de Private Equity
3. Implementar modelos de factores y pricing como un quant de Citadel
4. Hacer backtesting de estrategias de trading algorítmico
5. Usar ML para predicción financiera
6. Presentar un portafolio de proyectos en entrevistas

---

## 2. ESTADO ACTUAL DEL PROYECTO (QUÉ EXISTE HOY)

### 2.1 Estructura de archivos existente

```
ZED/
├── CLAUDE.md                          ← Guía para Claude Code (NO TOCAR)
├── ejercicios_for_anidados.py         ← Ejercicios sueltos (NO TOCAR)
└── documentacion/
    ├── README.md                      ← REESCRIBIR COMPLETO
    ├── PROGRESO.md                    ← REESCRIBIR COMPLETO
    ├── GLOSARIO.md                    ← EXPANDIR
    ├── arbol-aprendizaje.html         ← REGENERAR AL FINAL
    ├── teoria/
    │   ├── fase-0/
    │   │   └── U00-setup.md           ← EXISTE, EXPANDIR
    │   ├── fase-1/
    │   │   ├── U01-variables-tipos.md  ← EXISTE, RENUMERAR A U02
    │   │   ├── U02-operadores-python.md ← EXISTE, RENUMERAR A U03
    │   │   ├── U03-entrada-salida.md    ← EXISTE, RENUMERAR A U04
    │   │   └── U04-estructuras-control.md ← EXISTE, CONTENIDO SE REDISTRIBUYE
    │   ├── fase-2/
    │   │   ├── U05-condicionales-if.md   ← EXISTE, MANTENER NÚMERO
    │   │   └── U06-condicionales-anidados.md ← EXISTE, FUSIONAR CON BUCLES
    │   ├── fase-3/
    │   │   ├── U07-for-range.md          ← EXISTE, CONTENIDO VA A U06
    │   │   ├── U08-while-control.md      ← EXISTE, CONTENIDO VA A U06
    │   │   └── U09-for-anidados.md       ← EXISTE, CONTENIDO VA A U06
    │   ├── fase-4/
    │   │   ├── U10-listas-tuplas.md      ← EXISTE, RENUMERAR A U07
    │   │   ├── U11-diccionarios-sets.md  ← EXISTE, REDISTRIBUIR A U08-U09
    │   │   └── U12-archivos-csv.md       ← EXISTE, RENUMERAR A U10
    │   ├── fase-5/
    │   │   ├── U13-funciones-basicas.md  ← EXISTE, RENUMERAR A U11
    │   │   ├── U14-avanzado-funciones.md ← EXISTE, RENUMERAR A U12
    │   │   └── U15-modulos-jupyter.md    ← EXISTE, REDISTRIBUIR A U01 Y U13
    │   └── fase-6/
    │       ├── U16-numpy-pandas.md       ← EXISTE, SEPARAR EN U19-U21
    │       ├── U17-calculos-financieros.md ← EXISTE, REDISTRIBUIR A U24-U28
    │       ├── U18-valoracion-bonos.md    ← EXISTE, MOVER A U24
    │       ├── U19-modelos-riesgo.md      ← EXISTE, MOVER A U31
    │       └── U20-proyecto-final.md      ← EXISTE, EXPANDIR A U41-U42
    └── ejercicios/
        ├── fase-1/  (U01-U04: ejercicios + soluciones) ← RENUMERAR
        ├── fase-2/  (U05-U06: ejercicios + soluciones) ← MANTENER
        ├── fase-3/  (U07-U09: ejercicios + soluciones) ← REDISTRIBUIR
        ├── fase-4/  (U10-U12 combinado)                ← SEPARAR Y RENUMERAR
        ├── fase-5/  (U13-U15 combinado)                ← SEPARAR Y RENUMERAR
        └── fase-6/  (U16-U20 combinado)                ← SEPARAR Y REDISTRIBUIR
```

### 2.2 Formato de archivos de teoría (COPIAR EXACTAMENTE ESTE PATRÓN)

Cada archivo de teoría `.md` sigue este formato. **Todo nuevo archivo de teoría DEBE seguir esta estructura exacta:**

```markdown
# UXX: Título de la Unidad

> **Lectura previa:** [UYY: Título anterior](../fase-N/UYY-nombre.md)
> **Próxima unidad:** [UZZ: Título siguiente](./UZZ-nombre.md)

---

## 1. Teoría

### 1.1 Subtema
[Explicación clara con ejemplos de código en bloques ```python]

> 💡 Tips y datos curiosos
> ⚠️ Advertencias y errores comunes

### 1.2 Subtema
[Tablas, comparaciones, reglas]

---

## 2. Práctica

### 2.1 Ejercicio guiado: [Nombre con contexto financiero]
**Concepto financiero:** [Explicación del concepto]
**Fórmula:** [Si aplica]
**Código:**
```python
[Código completo ejecutable]
```
**Output:**
```
[Output exacto esperado]
```

---

## 3. Aplicación en Finanzas 💰
[Ejemplo real de cómo se usa en la industria]

---

## 4. Ejercicios Propuestos
> Los archivos de ejercicios están en `documentacion/ejercicios/fase-N/UXX_ejercicios.py`
[Lista numerada de ejercicios]

---

## 5. Resumen
| Concepto | Ejemplo |
|---------|---------|
[Tabla de resumen]

---

## ✅ Autoevaluación
[5 preguntas]

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - [Qué guardar]
```

### 2.3 Formato de archivos de ejercicios (COPIAR EXACTAMENTE ESTE PATRÓN)

Cada archivo `UXX_ejercicios.py`:

```python
# UXX: EJERCICIOS — Título de la Unidad

# ============================================================
# Ejercicio N: Nombre descriptivo
# Descripción del problema
# Fórmula si aplica
# ============================================================
print("=== Ejercicio N: Nombre ===")
variable_1 = valor
variable_2 = valor

# Escribe tu código aquí



# Output esperado:
# línea 1 del output
# línea 2 del output
```

Cada archivo `UXX_soluciones.py`:

```python
# UXX: SOLUCIONES — Título de la Unidad

# ============================================================
# Ejercicio N: Nombre descriptivo
# ============================================================
print("=== Ejercicio N: Nombre ===")
variable_1 = valor
variable_2 = valor

# [Código de la solución completa]

print(f"Resultado: {resultado}")
```

---

## 3. NUEVO CURRÍCULO: 43 UNIDADES EN 11 FASES

### FASE 0 — Entorno y Herramientas (U00–U01)

#### U00 — Preparando tu Entorno de Trabajo Profesional
- **Archivo teoría:** `documentacion/teoria/fase-0/U00-setup.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-0/U00_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-0/U00_soluciones.py`
- **Acción:** EXPANDIR el archivo existente `U00-setup.md`
- **Temas Python:** Instalación Python 3.12+, VS Code con extensiones (Python, Pylance), `venv`, `pip`, Git básico (`init`, `add`, `commit`, `push`), estructura de proyecto, `ruff` (linter), `black` (formatter)
- **Temas Finanzas:** Por qué los bancos de inversión exigen control de versiones; qué hace un analista cuantitativo día a día
- **Ejercicio final:** Crear repositorio `mi-finanzas/` con estructura profesional, README.md y `.gitignore`
- **Dependencias:** Ninguna

#### U01 — Jupyter Notebooks y el Flujo de Trabajo Cuantitativo
- **Archivo teoría:** `documentacion/teoria/fase-0/U01-jupyter.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-0/U01_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-0/U01_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial viene de antiguo U15-modulos-jupyter.md)
- **Temas Python:** Jupyter Lab, celdas código/markdown, magics (`%timeit`, `%%time`, `%matplotlib inline`), Google Colab
- **Temas Finanzas:** Cómo los quants en Citadel usan notebooks para research; flujo de análisis exploratorio
- **Ejercicio final:** Notebook que cargue precios de CSV y genere gráfico con `matplotlib`
- **Dependencias:** U00

---

### FASE 1 — Fundamentos de Python con Contexto Financiero (U02–U06)

#### U02 — Variables, Tipos de Datos y el Lenguaje de los Mercados
- **Archivo teoría:** `documentacion/teoria/fase-1/U02-variables-tipos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-1/U02_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-1/U02_soluciones.py`
- **Acción:** RENUMERAR desde antiguo U01. Agregar: `Decimal` para precisión bancaria, más ejemplos financieros
- **Temas Python:** `int`, `float`, `str`, `bool`, `type()`, f-strings con formato moneda (`:,.2f`), `Decimal`, type casting, asignación múltiple
- **Temas Finanzas:** Tipos de cambio, precios bid/ask, tasas de interés, tickers, interés simple y compuesto
- **Ejercicio final:** Conversor de monedas USD→EUR/PEN/BRL con precisión de 2 decimales; calculadora de interés simple y compuesto
- **Dependencias:** U01

#### U03 — Operadores: La Aritmética de Wall Street
- **Archivo teoría:** `documentacion/teoria/fase-1/U03-operadores.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-1/U03_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-1/U03_soluciones.py`
- **Acción:** RENUMERAR desde antiguo U02. Agregar: rendimiento logarítmico, spread bid-ask
- **Temas Python:** Operadores aritméticos (`**` para interés compuesto), comparación, lógicos (`and`, `or`, `not`), asignación aumentada, precedencia
- **Temas Finanzas:** Interés compuesto, rendimiento simple vs logarítmico (`ln(Pf/Pi)`), spread bid-ask, CAGR
- **Ejercicio final:** Calculadora de rendimientos (simple, logarítmico, anualizado, CAGR)
- **Dependencias:** U02

#### U04 — Entrada, Salida y Manejo de Errores Básico
- **Archivo teoría:** `documentacion/teoria/fase-1/U04-io-errores.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-1/U04_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-1/U04_soluciones.py`
- **Acción:** RENUMERAR desde antiguo U03. Agregar: `try/except` básico, `assert`, VS Code debugger
- **Temas Python:** `input()`, `print()` avanzado, `try/except` para inputs inválidos, `assert` para validación, debugging con VS Code
- **Temas Finanzas:** Validación de inputs financieros (tasas negativas, precios cero, plazos negativos)
- **Ejercicio final:** Programa interactivo que pida capital/tasa/plazo y muestre cuadro de amortización en consola
- **Dependencias:** U03

#### U05 — Condicionales: Reglas de Negocio y Señales de Trading
- **Archivo teoría:** `documentacion/teoria/fase-1/U05-condicionales.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-1/U05_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-1/U05_soluciones.py`
- **Acción:** FUSIONAR antiguo U05 + U06 (condicionales + anidados). Agregar: operador ternario, `match/case`
- **Temas Python:** `if/elif/else`, condicionales anidados, operador ternario, `match/case` (Python 3.10+), operadores lógicos combinados
- **Temas Finanzas:** Clasificación crediticia (A/B/C/D), alertas de precio (buy/sell/hold), scoring crediticio, categorías de riesgo
- **Ejercicio final:** Sistema de alertas de trading + sistema de scoring crediticio básico
- **Dependencias:** U04

#### U06 — Bucles: Iterando sobre Series de Tiempo
- **Archivo teoría:** `documentacion/teoria/fase-1/U06-bucles.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-1/U06_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-1/U06_soluciones.py`
- **Acción:** FUSIONAR antiguo U04 (break/continue/pass) + U07 (for/range) + U08 (while) + U09 (for anidados). Comprimir en una unidad densa
- **Temas Python:** `for` con `range()`, `while`, `break`/`continue`/`pass`, bucles anidados, list comprehensions
- **Temas Finanzas:** Series de precios, promedios móviles (SMA 20/50) calculados a mano, simulación de préstamos, TIR por bisección, detección de golden cross/death cross
- **Ejercicio final:** (1) SMA 20 y SMA 50 de lista de precios + detectar cruces. (2) TIR por método de bisección
- **Dependencias:** U05

---

### FASE 2 — Estructuras de Datos para Finanzas (U07–U10)

#### U07 — Listas y Tuplas: Series de Precios y Registros Financieros
- **Archivo teoría:** `documentacion/teoria/fase-2/U07-listas-tuplas.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-2/U07_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-2/U07_soluciones.py`
- **Acción:** CREAR NUEVO basado en antiguo U10-listas-tuplas.md, con más profundidad
- **Temas Python:** Listas (crear, indexar, slicing, métodos: `append`, `sort`, `reverse`, `index`, `pop`), tuplas (inmutabilidad, uso como registros), `enumerate()`, `zip()`
- **Temas Finanzas:** Datos OHLCV como tuplas, series de precios como listas, rolling windows manuales
- **Ejercicio final:** Módulo de estadísticas financieras (media, varianza, std, max drawdown) usando SOLO listas, sin librerías externas
- **Dependencias:** U06

#### U08 — Diccionarios: Portafolios y Datos Estructurados
- **Archivo teoría:** `documentacion/teoria/fase-2/U08-diccionarios.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-2/U08_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-2/U08_soluciones.py`
- **Acción:** CREAR NUEVO basado en parte de antiguo U11-diccionarios-sets.md
- **Temas Python:** Diccionarios (crear, acceder, `get()`, `items()`, `keys()`, `values()`, `update()`), diccionarios anidados, `defaultdict`, `Counter`, dict comprehensions
- **Temas Finanzas:** Portafolios como `{"AAPL": 0.3, "MSFT": 0.2, ...}`, estados financieros como dicts anidados
- **Ejercicio final:** Portafolio de 5 activos: valor total, pesos, rendimiento ponderado, rebalanceo
- **Dependencias:** U07

#### U09 — Conjuntos y Strings Avanzados para Datos Financieros
- **Archivo teoría:** `documentacion/teoria/fase-2/U09-sets-strings.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-2/U09_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-2/U09_soluciones.py`
- **Acción:** CREAR NUEVO (parte de sets viene de antiguo U11)
- **Temas Python:** Sets (unión, intersección, diferencia), string methods avanzados, expresiones regulares básicas (`re.search`, `re.findall`)
- **Temas Finanzas:** Identificadores ISIN/CUSIP, filtrado de universos de inversión, parsing de tickers en noticias
- **Ejercicio final:** Parser de noticias que extraiga tickers mencionados y clasifique sentimiento con palabras clave
- **Dependencias:** U08

#### U10 — Archivos y Datos: CSV, JSON y Datos de Mercado
- **Archivo teoría:** `documentacion/teoria/fase-2/U10-archivos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-2/U10_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-2/U10_soluciones.py`
- **Acción:** CREAR NUEVO basado en antiguo U12-archivos-csv.md, agregar JSON y pathlib
- **Temas Python:** `csv` module, `json` module, `pathlib`, context managers (`with`), encoding UTF-8
- **Temas Finanzas:** Formatos de datos Bloomberg/Reuters, archivos históricos de precios
- **Ejercicio final:** Leer CSV con 1 año de precios, calcular retornos diarios, guardar estadísticas en JSON y CSV
- **Dependencias:** U09
- **Archivo de datos necesario:** Crear `documentacion/datos/precios_ejemplo.csv` con 252 filas (1 año de trading) con columnas: `fecha,ticker,apertura,maximo,minimo,cierre,volumen`

---

### FASE 3 — Funciones, Módulos y Programación Profesional (U11–U14)

#### U11 — Funciones: Construyendo tu Librería Financiera
- **Archivo teoría:** `documentacion/teoria/fase-3/U11-funciones.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-3/U11_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-3/U11_soluciones.py`
- **Acción:** CREAR NUEVO basado en antiguo U13-funciones-basicas.md, agregar type hints y docstrings estilo NumPy
- **Temas Python:** `def`, parámetros posicionales y con nombre, valores por defecto, `*args`, `**kwargs`, docstrings NumPy-style, type hints, retorno múltiple (tuplas)
- **Temas Finanzas:** Funciones reutilizables: VPN, TIR, Sharpe ratio, volatilidad anualizada
- **Ejercicio final:** Crear módulo `finanzas_basicas.py` con 10+ funciones documentadas con type hints
- **Dependencias:** U10

#### U12 — Funciones Avanzadas: Lambda, Decoradores y Closures
- **Archivo teoría:** `documentacion/teoria/fase-3/U12-funciones-avanzadas.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-3/U12_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-3/U12_soluciones.py`
- **Acción:** CREAR NUEVO basado en antiguo U14-avanzado-funciones.md, agregar decoradores y closures
- **Temas Python:** `lambda`, `map()`, `filter()`, `sorted()` con key, closures, decoradores (`@timer`, `@log_trade`, `@validate_input`), `functools` (`partial`, `reduce`, `lru_cache`)
- **Temas Finanzas:** Filtrado de activos por criterios, caching de cálculos costosos, logging de trades
- **Ejercicio final:** Decoradores `@medir_tiempo`, `@registrar_operacion`, `@validar_positivo` aplicados a funciones de pricing
- **Dependencias:** U11

#### U13 — Módulos, Paquetes y Arquitectura de Proyecto
- **Archivo teoría:** `documentacion/teoria/fase-3/U13-modulos-paquetes.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-3/U13_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-3/U13_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial de antiguo U15-modulos-jupyter.md)
- **Temas Python:** `__init__.py`, imports absolutos y relativos, `if __name__ == "__main__"`, estructura de proyecto, `requirements.txt`, `pyproject.toml`
- **Temas Finanzas:** Organización de código como en un desk cuantitativo
- **Ejercicio final:** Reestructurar código anterior en paquete `quantlib/` con sub-módulos: `pricing`, `risk`, `data`, `utils`
- **Dependencias:** U12

#### U14 — Manejo de Errores y Logging Profesional
- **Archivo teoría:** `documentacion/teoria/fase-3/U14-errores-logging.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-3/U14_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-3/U14_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Jerarquía de excepciones, excepciones personalizadas (`InvalidTickerError`, `DataNotFoundError`), `logging` (niveles, handlers, formatters), `warnings`, intro a `pytest`
- **Temas Finanzas:** Validación de datos de mercado, alertas de datos anómalos, auditoría de operaciones
- **Ejercicio final:** Agregar error handling y logging al paquete `quantlib/`; escribir 10 tests con `pytest`
- **Dependencias:** U13

---

### FASE 4 — Programación Orientada a Objetos para Finanzas (U15–U18)

#### U15 — Clases y Objetos: Modelando Instrumentos Financieros
- **Archivo teoría:** `documentacion/teoria/fase-4/U15-clases-objetos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-4/U15_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-4/U15_soluciones.py`
- **Acción:** CREAR NUEVO (no existe contenido OOP en el curso actual)
- **Temas Python:** `class`, `__init__`, atributos de instancia y clase, métodos, `@property`, `__repr__`, `__str__`
- **Temas Finanzas:** Clases `Accion` (ticker, precio, cantidad, valor()), `Bono` (face_value, coupon, maturity, precio()), `Portafolio` (activos, valor_total())
- **Ejercicio final:** Clases `Accion`, `Bono`, `Portafolio` con métodos para calcular métricas
- **Dependencias:** U14

#### U16 — Herencia y Polimorfismo: Jerarquía de Instrumentos
- **Archivo teoría:** `documentacion/teoria/fase-4/U16-herencia.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-4/U16_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-4/U16_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Herencia, `super()`, `abc.ABC` y `@abstractmethod`, polimorfismo, composición vs herencia, mixins
- **Temas Finanzas:** `Instrumento` (abstracta) → `Accion`, `Bono`, `Opcion`. Método `valorar()` polimórfico
- **Ejercicio final:** Jerarquía completa con `valorar()` polimórfico; `Portafolio` que contiene múltiples tipos
- **Dependencias:** U15

#### U17 — Métodos Especiales y Data Classes
- **Archivo teoría:** `documentacion/teoria/fase-4/U17-dunders-dataclasses.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-4/U17_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-4/U17_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Dunders: `__add__`, `__eq__`, `__lt__`, `__len__`, `__getitem__`, `__iter__`. `@dataclass`, `NamedTuple`, `__slots__`
- **Temas Finanzas:** Trade records como dataclasses, order books, combinación de portafolios (`port_a + port_b`)
- **Ejercicio final:** `OrderBook` con dataclasses, slicing con `__getitem__`, comparación con `__eq__`
- **Dependencias:** U16

#### U18 — Patrones de Diseño en Finanzas Cuantitativas
- **Archivo teoría:** `documentacion/teoria/fase-4/U18-patrones-diseno.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-4/U18_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-4/U18_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Strategy pattern, Factory pattern, Observer pattern, Singleton, iteradores con `__iter__`/`__next__`, generadores (`yield`)
- **Temas Finanzas:** Motor de pricing intercambiable (BSM vs binomial vs Monte Carlo), event-driven market data, factory de instrumentos desde JSON/CSV
- **Ejercicio final:** Motor de pricing con Strategy pattern para opciones
- **Dependencias:** U17

---

### FASE 5 — Stack Científico: NumPy, Pandas y Visualización (U19–U23)

#### U19 — NumPy: Computación Numérica de Alto Rendimiento
- **Archivo teoría:** `documentacion/teoria/fase-5/U19-numpy.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-5/U19_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-5/U19_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial de antiguo U16-numpy-pandas.md, solo la parte NumPy expandida)
- **Temas Python:** Arrays (crear, indexar, slicing, reshaping, broadcasting), operaciones vectorizadas vs loops (benchmark con `%timeit`), `np.linalg` (inversas, determinantes, eigenvalores, SVD), `np.random` para simulaciones, funciones estadísticas
- **Temas Finanzas:** Matrices de covarianza, retornos como arrays, simulación de 10,000 trayectorias de precios con GBM
- **Librería:** `numpy`
- **Ejercicio final:** (1) Matriz de covarianza de 10 activos. (2) 10,000 trayectorias GBM. (3) Benchmark loops vs vectorizado
- **Dependencias:** U18

#### U20 — Pandas Fundamentos: El DataFrame como Hoja de Cálculo Avanzada
- **Archivo teoría:** `documentacion/teoria/fase-5/U20-pandas-fundamentos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-5/U20_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-5/U20_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial de antiguo U16, solo Pandas expandido)
- **Temas Python:** `Series`, `DataFrame` (desde CSV, dicts, arrays), `loc`/`iloc`/boolean indexing, `DatetimeIndex`, `resample`, `shift`, `pct_change`, `groupby`/`agg`/`transform`, `pivot_table`, merge/join
- **Temas Finanzas:** Series de precios, retornos diarios con `pct_change()`, resampling (diario→semanal→mensual)
- **Librería:** `pandas`
- **Ejercicio final:** 5 años del S&P 500: retornos por mes, volatilidad rolling, peores/mejores días, correlación con tasas
- **Dependencias:** U19

#### U21 — Pandas Avanzado: Análisis de Series Financieras
- **Archivo teoría:** `documentacion/teoria/fase-5/U21-pandas-avanzado.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-5/U21_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-5/U21_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `rolling()`, `ewm()`, `MultiIndex`, `pipe()`, datos faltantes (`fillna`, `interpolate`), performance (`eval()`, `query()`, dtypes categóricos)
- **Temas Finanzas:** SMA, EMA, Bollinger Bands, VWAP, RSI, MACD con detección de señales
- **Librería:** `pandas`
- **Ejercicio final:** Dashboard de indicadores técnicos para cualquier acción: SMA, EMA, Bollinger, RSI, MACD + señales
- **Dependencias:** U20

#### U22 — Visualización Financiera con Matplotlib y Plotly
- **Archivo teoría:** `documentacion/teoria/fase-5/U22-visualizacion.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-5/U22_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-5/U22_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `matplotlib` (line plots, subplots, ejes duales, anotaciones), candlestick/OHLC, heatmaps de correlación, `plotly` interactivo, `mplfinance`
- **Temas Finanzas:** Gráficos de velas japonesas, Bollinger Bands visuales, fronteras eficientes, equity curves
- **Librerías:** `matplotlib`, `plotly`, `mplfinance`, `seaborn`
- **Ejercicio final:** Reporte visual: candlestick + volumen + indicadores técnicos + drawdown chart
- **Dependencias:** U21

#### U23 — Obtención de Datos: APIs y Web Scraping Financiero
- **Archivo teoría:** `documentacion/teoria/fase-5/U23-apis-datos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-5/U23_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-5/U23_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `yfinance`, `requests` para APIs REST, autenticación con API keys, rate limiting, `BeautifulSoup` para scraping ético
- **Temas Finanzas:** Yahoo Finance, FRED (datos macro de la Fed), SEC filings, Alpha Vantage
- **Librerías:** `yfinance`, `requests`, `beautifulsoup4`, `fredapi`
- **Ejercicio final:** Pipeline que descargue 20 acciones del S&P 500 + datos macro de FRED → DataFrame unificado
- **Dependencias:** U22

---

### FASE 6 — Matemáticas Financieras y Valoración (U24–U28)

#### U24 — Valor del Dinero en el Tiempo y Renta Fija
- **Archivo teoría:** `documentacion/teoria/fase-6/U24-tvm-renta-fija.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-6/U24_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-6/U24_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial de antiguos U17 y U18)
- **Temas Python:** `numpy-financial` (`npv`, `irr`, `pmt`, `fv`, `pv`), `scipy.optimize` (Newton-Raphson para YTM)
- **Temas Finanzas:** VP, VF, anualidades, perpetuidades, precio de bonos, YTM, duration (Macaulay y modificada), convexidad, curvas de rendimiento (bootstrapping), spread de crédito, amortización (francés, alemán, americano)
- **Librerías:** `numpy-financial`, `scipy.optimize`
- **Ejercicio final:** Pricer de bonos completo: precio, YTM por Newton-Raphson, duration modificada, convexidad; graficar curva del Tesoro US
- **Dependencias:** U23

#### U25 — Análisis de Estados Financieros con Python
- **Archivo teoría:** `documentacion/teoria/fase-6/U25-estados-financieros.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-6/U25_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-6/U25_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Pandas para tablas financieras, funciones de ratios encadenadas
- **Temas Finanzas:** 3 estados financieros (income statement, balance sheet, cash flow), 50+ ratios (profitability, leverage, liquidity, efficiency), DuPont (3 y 5 componentes), análisis horizontal/vertical, Altman Z-Score
- **Referencia:** FinanceToolkit (github.com/JerBouma/FinanceToolkit) como inspiración de ratios
- **Ejercicio final:** Analizar AAPL, TSLA, JPM: 30 ratios, DuPont, Z-Score, equity research summary
- **Dependencias:** U24

#### U26 — Valoración de Empresas: DCF y Comparables
- **Archivo teoría:** `documentacion/teoria/fase-6/U26-valoracion-dcf.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-6/U26_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-6/U26_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Modelos en Pandas + NumPy, tablas de sensibilidad con meshgrid
- **Temas Finanzas:** FCFF y FCFE, proyección de flujos (crecimiento, márgenes, capex), WACC (CAPM para equity, costo de deuda, estructura de capital), DCF con valor terminal (Gordon Growth + Exit Multiple), análisis por comparables (EV/EBITDA, P/E, P/B)
- **Nota:** Este es el skill #1 que pide JP Morgan IBD. Debe ser extremadamente detallado.
- **Ejercicio final:** DCF completo de una empresa pública: proyectar 5 años FCF, WACC, valor terminal, equity value, precio implícito por acción; tabla de sensibilidad WACC vs growth rate
- **Dependencias:** U25

#### U27 — Modelo LBO y Private Equity
- **Archivo teoría:** `documentacion/teoria/fase-6/U27-lbo.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-6/U27_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-6/U27_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Modelos iterativos con loops y DataFrames, `scipy` para IRR
- **Temas Finanzas:** Estructura LBO (fuentes y usos), calendario de deuda (senior, mezzanine, subordinada), cash flow waterfall y repago, IRR y MOIC del sponsor, sensibilidad (entry multiple × exit multiple × leverage)
- **Nota:** Core skill para JP Morgan PE. Debe modelar un caso real completo.
- **Ejercicio final:** LBO completo: adquisición a 8x EBITDA, 60% deuda, 5 años hold, IRR y MOIC bajo 9 escenarios (3×3)
- **Dependencias:** U26

#### U28 — Derivados: Opciones y Modelos de Pricing
- **Archivo teoría:** `documentacion/teoria/fase-6/U28-derivados.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-6/U28_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-6/U28_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `scipy.stats.norm`, optimización para implied volatility, árboles binomiales recursivos
- **Temas Finanzas:** Opciones (calls, puts, payoffs), estrategias (straddle, spread, collar), Black-Scholes-Merton (derivación intuitiva + implementación), griegas (Delta, Gamma, Theta, Vega, Rho), modelo binomial CRR, implied volatility y volatility smile
- **Nota:** Core skill para Jane Street y desks de derivados.
- **Librerías:** `scipy`, `numpy`
- **Ejercicio final:** Pricer completo: BSM + binomial + griegas + IV solver; gráficos de payoffs y vol smile
- **Dependencias:** U26

---

### FASE 7 — Gestión de Portafolios y Riesgo (U29–U32)

#### U29 — Teoría Moderna de Portafolios
- **Archivo teoría:** `documentacion/teoria/fase-7/U29-mpt.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-7/U29_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-7/U29_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `scipy.optimize.minimize` con constraints, simulación Monte Carlo
- **Temas Finanzas:** Markowitz (retorno esperado, varianza, covarianza de portafolio), frontera eficiente (10,000 portafolios simulados), portafolio de mínima varianza y máximo Sharpe, CML, limitaciones de Markowitz
- **Ejercicio final:** Optimizar portafolio de 10 acciones: frontera eficiente, portafolio tangente, CML; comparar con equal-weight
- **Dependencias:** U28

#### U30 — Modelos de Factores y Asset Pricing
- **Archivo teoría:** `documentacion/teoria/fase-7/U30-factores.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-7/U30_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-7/U30_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `statsmodels` OLS, regresión multivariable, `linearmodels`
- **Temas Finanzas:** CAPM (beta, SML), Fama-French 3 y 5 factores, regresión de factores, alpha y performance attribution, Black-Litterman
- **Referencia:** getfactormodels (github.com/x512/getfactormodels) para datos de factores
- **Librerías:** `statsmodels`, `linearmodels`
- **Ejercicio final:** Fama-French de 20 acciones: alphas, betas, R²; Black-Litterman con views propias
- **Dependencias:** U29

#### U31 — Gestión de Riesgo: VaR, CVaR y Stress Testing
- **Archivo teoría:** `documentacion/teoria/fase-7/U31-riesgo.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-7/U31_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-7/U31_soluciones.py`
- **Acción:** CREAR NUEVO (contenido parcial de antiguo U19-modelos-riesgo.md, expandido significativamente)
- **Temas Python:** Simulación, distribuciones estadísticas, backtesting de modelos
- **Temas Finanzas:** VaR (histórico, paramétrico, Monte Carlo), CVaR/Expected Shortfall, stress testing (escenarios 2008 y COVID), backtesting VaR (Kupiec test), risk budgeting
- **Ejercicio final:** Sistema de riesgo: VaR por 3 métodos, CVaR, stress test, backtesting con Kupiec
- **Dependencias:** U30

#### U32 — Optimización Avanzada de Portafolios
- **Archivo teoría:** `documentacion/teoria/fase-7/U32-optimizacion-avanzada.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-7/U32_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-7/U32_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Algoritmos de clustering, optimización avanzada
- **Temas Finanzas:** HRP (Hierarchical Risk Parity), Risk Parity, Ledoit-Wolf shrinkage, rebalanceo (periodicidad, costos de transacción, turnover)
- **Referencia:** PyPortfolioOpt (github.com/PyPortfolio/PyPortfolioOpt)
- **Librerías:** `PyPortfolioOpt`, `scipy`, `sklearn.covariance`
- **Ejercicio final:** Comparar 5 estrategias (equal weight, min var, max Sharpe, HRP, risk parity) en 10 años; análisis de turnover y costos
- **Dependencias:** U31

---

### FASE 8 — Métodos Cuantitativos y Econometría (U33–U36)

#### U33 — Probabilidad, Estadística y Distribuciones Financieras
- **Archivo teoría:** `documentacion/teoria/fase-8/U33-distribuciones.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-8/U33_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-8/U33_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `scipy.stats` (distribuciones, tests), `numpy.random`, bootstrap
- **Temas Finanzas:** Normal, log-normal, t-Student, fat tails, tests de normalidad (Jarque-Bera, Shapiro-Wilk, Q-Q plots), Monte Carlo, bootstrap para intervalos de confianza, random walk, GBM
- **Ejercicio final:** Distribución de retornos de 50 acciones: tests de normalidad, ajustar t-Student, simular GBM, comparar MC vs histórico
- **Dependencias:** U32

#### U34 — Series de Tiempo: ARIMA y Volatilidad
- **Archivo teoría:** `documentacion/teoria/fase-8/U34-series-tiempo.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-8/U34_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-8/U34_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `statsmodels` (ARIMA, ACF, PACF), `arch` (GARCH), `pmdarima` (auto-ARIMA)
- **Temas Finanzas:** Estacionariedad (ADF, KPSS), autocorrelación, ARIMA, ARCH/GARCH(1,1)/EGARCH, forecasting de volatilidad
- **Librerías:** `statsmodels`, `arch`, `pmdarima`
- **Ejercicio final:** Modelar volatilidad S&P 500: GARCH(1,1), comparar con vol realizada, forecast 30 días
- **Dependencias:** U33

#### U35 — Econometría Financiera: Regresión y Panel Data
- **Archivo teoría:** `documentacion/teoria/fase-8/U35-econometria.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-8/U35_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-8/U35_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `statsmodels` avanzado, `linearmodels` para panel data
- **Temas Finanzas:** OLS, GLS, errores robustos (White, Newey-West), errores clustered, panel data (fixed effects, random effects, Hausman test), Fama-MacBeth, 2SLS básico
- **Referencia:** linearmodels (github.com/bashtage/linearmodels)
- **Librerías:** `statsmodels`, `linearmodels`
- **Ejercicio final:** Replicar paper: regresión cross-sectional con Fama-MacBeth, errores clustered, robustness checks
- **Dependencias:** U34

#### U36 — SQL para Datos Financieros
- **Archivo teoría:** `documentacion/teoria/fase-8/U36-sql.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-8/U36_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-8/U36_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `sqlite3`, `sqlalchemy`, `pandas.read_sql()`
- **Temas Finanzas:** SELECT/WHERE/JOIN/GROUP BY, window functions (LAG, LEAD, RANK, running sums), subqueries y CTEs, base de datos local de precios
- **Librerías:** `sqlite3`, `sqlalchemy`
- **Ejercicio final:** Base SQLite con 5 años de precios + fundamentales + factores; queries: top performers, momentum portfolios, factor sorts
- **Dependencias:** U35

---

### FASE 9 — Machine Learning y Trading Algorítmico (U37–U40)

#### U37 — Machine Learning para Finanzas: Fundamentos
- **Archivo teoría:** `documentacion/teoria/fase-9/U37-ml-fundamentos.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-9/U37_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-9/U37_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `scikit-learn` pipeline completo (preprocessing, model, evaluation)
- **Temas Finanzas:** Feature engineering financiero (retornos rezagados, volatilidad, momentum), cross-validation temporal (`TimeSeriesSplit`), métricas (accuracy, AUC), overfitting y regularización (L1/L2)
- **Referencia:** MIT ML (github.com/denikn/Machine-Learning-MIT-Assignment)
- **Librerías:** `scikit-learn`, `pandas`
- **Ejercicio final:** Predecir dirección del mercado a 1 semana con random forest: features, TimeSeriesSplit, comparar con benchmark
- **Dependencias:** U36

#### U38 — Machine Learning Avanzado: Métodos Cuantitativos
- **Archivo teoría:** `documentacion/teoria/fase-9/U38-ml-avanzado.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-9/U38_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-9/U38_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** XGBoost, LightGBM, PCA, clustering, intro redes neuronales
- **Temas Finanzas:** Gradient boosting para predicción, PCA para factores, clustering para regímenes de mercado, autoencoders para asset pricing
- **Referencia:** Autoencoder-Asset-Pricing-Models (github.com/RichardS0268/Autoencoder-Asset-Pricing-Models)
- **Librerías:** `xgboost`, `lightgbm`, `sklearn`, `torch` o `keras`
- **Ejercicio final:** Detectar regímenes (bull/bear/sideways) con clustering; autoencoder para factores latentes
- **Dependencias:** U37

#### U39 — Algorithmic Trading: Estrategias y Backtesting
- **Archivo teoría:** `documentacion/teoria/fase-9/U39-algo-trading.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-9/U39_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-9/U39_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** Framework de backtesting vectorizado propio (no usar librería externa, construir desde cero)
- **Temas Finanzas:** Mean reversion, momentum, pairs trading (cointegración Engle-Granger), señales→ejecución→PnL, métricas (Sharpe, Sortino, max drawdown, Calmar), walk-forward optimization
- **Referencia:** QuantResearch (github.com/letianzj/QuantResearch)
- **Ejercicio final:** Implementar y backtestear 3 estrategias sobre 10 años; comparar Sharpe, drawdowns, equity curves
- **Dependencias:** U38

#### U40 — Infraestructura y Producción
- **Archivo teoría:** `documentacion/teoria/fase-9/U40-infraestructura.md`
- **Archivo ejercicios:** `documentacion/ejercicios/fase-9/U40_ejercicios.py`
- **Archivo soluciones:** `documentacion/ejercicios/fase-9/U40_soluciones.py`
- **Acción:** CREAR NUEVO
- **Temas Python:** `threading`, `asyncio`, `aiohttp`, `Docker` básico, CI/CD con GitHub Actions, `APScheduler`/`cron`
- **Temas Finanzas:** Sistemas de producción en desks cuantitativos, pipelines de datos automatizados
- **Ejercicio final:** Pipeline automatizado: descarga diaria → actualizar DB → recalcular señales → alertas por email
- **Dependencias:** U39

---

### FASE 10 — Proyectos Integradores de Nivel Profesional (U41–U42)

#### U41 — Proyecto: Plataforma de Análisis Cuantitativo Completa
- **Archivo teoría:** `documentacion/teoria/fase-10/U41-plataforma.md`
- **Archivo ejercicios:** Proyecto completo en `documentacion/proyectos/plataforma/`
- **Acción:** CREAR NUEVO (expandir concepto de antiguo U20)
- **Temas:** Arquitectura end-to-end, Streamlit/Dash, documentación profesional
- **Entregable:** Plataforma web: (1) seleccionar activos, (2) análisis fundamental (ratios, DCF), (3) análisis técnico (indicadores), (4) optimización de portafolio, (5) gestión de riesgo (VaR, stress test), (6) reporte PDF
- **Librerías:** `streamlit` o `dash`, todas las anteriores
- **Dependencias:** U40

#### U42 — Proyecto: Sistema de Trading Cuantitativo End-to-End
- **Archivo teoría:** `documentacion/teoria/fase-10/U42-sistema-trading.md`
- **Archivo ejercicios:** Proyecto completo en `documentacion/proyectos/trading-system/`
- **Acción:** CREAR NUEVO
- **Temas:** Data pipeline → feature engineering → modelo ML → backtest → risk management → tear sheet
- **Entregable:** Sistema completo: (1) pipeline de datos, (2) 3 estrategias ML, (3) portfolio optimizer, (4) risk manager, (5) backtester con costos, (6) tear sheet tipo pyfolio
- **Dependencias:** U41

---

## 4. INSTRUCCIONES DE EJECUCIÓN PASO A PASO

### PASO 1: Crear estructura de carpetas

Ejecutar estos comandos exactos:

```bash
cd /Users/miguelangelquispetito/Desktop/ZED

# Crear carpeta de datos
mkdir -p documentacion/datos

# Crear carpetas de teoría nuevas (fase-0 a fase-2 ya existen pero con contenido viejo)
mkdir -p documentacion/teoria/fase-7
mkdir -p documentacion/teoria/fase-8
mkdir -p documentacion/teoria/fase-9
mkdir -p documentacion/teoria/fase-10

# Crear carpetas de ejercicios nuevas
mkdir -p documentacion/ejercicios/fase-0
mkdir -p documentacion/ejercicios/fase-7
mkdir -p documentacion/ejercicios/fase-8
mkdir -p documentacion/ejercicios/fase-9
mkdir -p documentacion/ejercicios/fase-10

# Crear carpetas de proyectos finales
mkdir -p documentacion/proyectos/plataforma
mkdir -p documentacion/proyectos/trading-system
```

### PASO 2: Migrar contenido existente

**IMPORTANTE:** No borrar archivos originales hasta que los nuevos estén verificados. Proceso:

1. **Fase 0 — U00:** Leer `teoria/fase-0/U00-setup.md`. Expandir agregando: `venv`, `pip`, `git` básico, `ruff`, `black`, estructura de proyecto. Mantener el formato existente.

2. **Fase 0 — U01 (Jupyter):** Crear `teoria/fase-0/U01-jupyter.md`. Extraer contenido de Jupyter de `teoria/fase-5/U15-modulos-jupyter.md`. Expandir con magics y Colab.

3. **Fase 1 — U02 a U06:** Renumerar los archivos existentes:
   - Antiguo U01 → Nuevo U02 (agregar `Decimal`, más ejemplos financieros)
   - Antiguo U02 → Nuevo U03 (agregar rendimiento logarítmico, CAGR)
   - Antiguo U03 → Nuevo U04 (agregar `try/except`, debugger)
   - Antiguo U05+U06 → Nuevo U05 (fusionar condicionales + anidados + match/case)
   - Antiguo U04+U07+U08+U09 → Nuevo U06 (fusionar break/continue + for + while + anidados + list comprehensions)

4. **Fase 2 — U07 a U10:** Redistribuir:
   - Antiguo U10 → Nuevo U07 (listas y tuplas, expandir)
   - Antiguo U11 (parte dicts) → Nuevo U08
   - Antiguo U11 (parte sets) → Nuevo U09 (agregar regex)
   - Antiguo U12 → Nuevo U10 (agregar JSON, pathlib)

5. **Fase 3 — U11 a U14:** Redistribuir:
   - Antiguo U13 → Nuevo U11 (agregar type hints, docstrings)
   - Antiguo U14 → Nuevo U12 (agregar decoradores, closures)
   - Antiguo U15 (parte módulos) → Nuevo U13
   - Nuevo U14 es completamente nuevo (errores, logging, pytest)

6. **Fases 4-10 — U15 a U42:** Todo completamente nuevo. Crear desde cero siguiendo las especificaciones de la Sección 3.

### PASO 3: Actualizar los ejercicios

Para cada unidad renumerada o nueva:
- Crear `UXX_ejercicios.py` con 4 ejercicios mínimo, formato exacto de Sección 2.3
- Crear `UXX_soluciones.py` con soluciones completas ejecutables
- Cada ejercicio debe tener contexto financiero real
- Cada ejercicio debe tener `# Output esperado:` con el resultado exacto

### PASO 4: Reescribir README.md

Usar el mismo estilo del README actual pero con el nuevo mapa de 43 unidades y 11 fases. Incluir:
- Objetivo del curso actualizado (mención JP Morgan, PE, quant)
- Mapa del curso (árbol ASCII con las 11 fases)
- Instrucciones de uso
- Estructura del proyecto actualizada
- Bibliografía expandida

### PASO 5: Reescribir PROGRESO.md

Nuevo checklist con 43 unidades en 11 fases. Formato:

```markdown
| # | Unidad | Estado |
|---|--------|--------|
| U00 | Preparando tu entorno profesional | ⬜ Pendiente |
```

Tabla resumen al final con progreso por fase.

### PASO 6: Expandir GLOSARIO.md

Agregar términos nuevos organizados por categoría:

- **OOP:** clase, objeto, herencia, polimorfismo, ABC, dataclass, decorator, generator
- **NumPy/Pandas:** array, DataFrame, Series, vectorización, broadcasting, rolling, ewm
- **Valoración:** DCF, FCFF, FCFE, WACC, LBO, IRR, MOIC, EV/EBITDA, P/E
- **Derivados:** opción, call, put, Black-Scholes, griegas, implied volatility, payoff
- **Portafolio:** Markowitz, frontera eficiente, Sharpe ratio, HRP, risk parity, Ledoit-Wolf
- **Riesgo:** VaR, CVaR, stress test, Kupiec, drawdown
- **Econometría:** OLS, panel data, fixed effects, Fama-MacBeth, 2SLS, GARCH, ARIMA
- **ML:** overfitting, cross-validation, random forest, XGBoost, PCA, autoencoder
- **Trading:** momentum, mean reversion, pairs trading, cointegración, backtesting, Sharpe, Sortino
- **Infra:** API, REST, SQL, Docker, CI/CD, asyncio

### PASO 7: Crear archivo de datos de ejemplo

Crear `documentacion/datos/precios_ejemplo.csv` con 252 filas de datos ficticios pero realistas:

```csv
fecha,ticker,apertura,maximo,minimo,cierre,volumen
2024-01-02,AAPL,185.50,186.75,184.20,185.90,45230100
2024-01-03,AAPL,185.90,187.10,185.00,186.50,38920500
...
```

Generar con un script Python que simule precios con GBM para tener datos coherentes.

### PASO 8: Actualizar CLAUDE.md

Actualizar la sección "Project Overview" y "File Summary" del CLAUDE.md para reflejar la nueva estructura de 43 unidades.

### PASO 9: Verificación

Para cada archivo creado o modificado:

```bash
# Verificar que todos los archivos de teoría existen
ls documentacion/teoria/fase-*/U*.md | wc -l
# Esperado: 43

# Verificar que todos los archivos de ejercicios existen
ls documentacion/ejercicios/fase-*/U*_ejercicios.py | wc -l
# Esperado: 40 (U41 y U42 son proyectos, no ejercicios simples)

# Verificar que todos los .py ejecutan sin errores de sintaxis
for f in documentacion/ejercicios/fase-*/*.py; do python -c "import ast; ast.parse(open('$f').read())" && echo "OK: $f" || echo "FAIL: $f"; done

# Verificar que PROGRESO.md tiene 43 unidades
grep -c "⬜ Pendiente" documentacion/PROGRESO.md
# Esperado: 43

# Verificar links internos en README.md
grep -oP '\(\..*?\)' documentacion/README.md | while read link; do
    path="documentacion/${link:2:-1}"
    [ -f "$path" ] || echo "BROKEN LINK: $link"
done
```

---

## 5. SECUENCIA DE DEPENDENCIAS (GRAFO)

```
U00 → U01 → U02 → U03 → U04 → U05 → U06
                                         ↓
                              U07 → U08 → U09 → U10
                                                  ↓
                                       U11 → U12 → U13 → U14
                                                           ↓
                                                U15 → U16 → U17 → U18
                                                                   ↓
                                                        U19 → U20 → U21 → U22 → U23
                                                                                  ↓
                                                               U24 → U25 → U26 → U27
                                                                           ↓       ↓
                                                                          U28      |
                                                                           ↓       |
                                                               U29 → U30 → U31 → U32
                                                                                   ↓
                                                               U33 → U34 → U35 → U36
                                                                                   ↓
                                                               U37 → U38 → U39 → U40
                                                                                   ↓
                                                                          U41 → U42
```

Nota: Después de U23, las Fases 6–7 y Fases 8–9 pueden avanzarse en paralelo (dependencias cruzadas mínimas). Ambos caminos convergen en Fase 10.

---

## 6. LIBRERÍAS POR FASE (requirements.txt)

```
# Fase 0-4: Python estándar (no requiere pip install)

# Fase 5
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
plotly>=5.15
mplfinance>=0.12
seaborn>=0.12
yfinance>=0.2
requests>=2.31
beautifulsoup4>=4.12

# Fase 6
numpy-financial>=1.0
scipy>=1.11

# Fase 7
PyPortfolioOpt>=1.5
statsmodels>=0.14
linearmodels>=5.3

# Fase 8
arch>=6.2
pmdarima>=2.0
sqlalchemy>=2.0

# Fase 9
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
torch>=2.0

# Fase 10
streamlit>=1.28
```

---

## 7. PRIORIDAD DE EJECUCIÓN

Si los recursos son limitados, construir en este orden de prioridad:

1. **CRÍTICO (core IB/PE):** U24 (TVM/Bonos), U25 (Estados Financieros), U26 (DCF), U27 (LBO)
2. **CRÍTICO (core quant):** U28 (Derivados), U29 (MPT), U30 (Factores), U31 (Riesgo)
3. **ALTO (stack científico):** U19 (NumPy), U20-U21 (Pandas), U22 (Viz), U23 (APIs)
4. **ALTO (OOP):** U15-U18
5. **MEDIO (econometría/ML):** U33-U39
6. **MEDIO (funciones pro):** U11-U14
7. **BAJO (fundamentos):** U00-U10 (ya existe contenido, solo renumerar y expandir)
8. **BAJO (infra/proyectos):** U40-U42

---

## 8. NOTAS PARA EL AGENTE EJECUTOR

1. **Idioma:** Todo en español. Variables en español snake_case. Nombres de librerías/funciones de Python en inglés.
2. **Formato:** Seguir EXACTAMENTE los patrones de Sección 2.2 y 2.3. No inventar formatos nuevos.
3. **Profundidad:** Cada archivo de teoría debe tener mínimo 150 líneas. Cada ejercicio debe ser ejecutable.
4. **Contexto financiero:** NUNCA hacer un ejercicio genérico. Siempre usar datos financieros reales o realistas.
5. **NO TOCAR:** `CLAUDE.md` (excepto actualizar overview), `ejercicios_for_anidados.py`, archivos en `~/.claude/`
6. **Ejecutar paso a paso:** No intentar crear todo de golpe. Hacer una fase completa, verificar, luego la siguiente.
7. **Verificación:** Después de crear cada archivo `.py`, ejecutar `python -c "import ast; ast.parse(open('archivo.py').read())"` para verificar sintaxis.
