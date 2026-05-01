# Glosario — Python para Finanzas Cuantitativas

> 250+ términos organizados por categoría. Consulta rápida.

---

## 🔤 Términos Python

| Término | Definición | Unidad |
|---------|-----------|--------|
| **variable** | Espacio en memoria que almacena un valor con nombre | U02 |
| **tipo de dato** | Clasificación de valores: `int`, `float`, `str`, `bool` | U02 |
| **int** | Número entero | U02 |
| **float** | Número decimal | U02 |
| **str** | Cadena de texto | U02 |
| **bool** | Valor lógico: `True` o `False` | U02 |
| **Decimal** | Tipo de alta precisión para cálculos monetarios | U02 |
| **operador aritmético** | `+`, `-`, `*`, `/`, `//`, `%`, `**` | U03 |
| **operador relacional** | `==`, `!=`, `<`, `>`, `<=`, `>=` | U03 |
| **operador lógico** | `and`, `or`, `not` | U03 |
| **rendimiento logarítmico** | `ln(Pf/Pi)` — preferido en finanzas cuantitativas | U03 |
| **input()** | Función que lee entrada del usuario (siempre str) | U04 |
| **print()** | Función que muestra salida en consola | U04 |
| **f-string** | Formato de texto: `f"texto {variable}"` | U04 |
| **try/except** | Captura y maneja errores | U04 |
| **if/elif/else** | Estructura condicional | U05 |
| **operador ternario** | `x if cond else y` | U05 |
| **match/case** | Pattern matching (Python 3.10+) | U05 |
| **for** | Bucle que itera sobre una secuencia | U06 |
| **range()** | Genera secuencias: `range(inicio, fin, paso)` | U06 |
| **while** | Bucle que ejecuta mientras condición sea True | U06 |
| **break** | Detiene un bucle por completo | U06 |
| **continue** | Salta a la siguiente iteración | U06 |
| **pass** | Sentencia nula, marcador de posición | U06 |
| **list comprehension** | `[x for x in lista if cond]` | U06 |
| **lista** | Colección mutable ordenada: `[1, 2, 3]` | U07 |
| **tupla** | Colección inmutable ordenada: `(1, 2, 3)` | U07 |
| **slicing** | `lista[inicio:fin:paso]` | U07 |
| **enumerate()** | Itera con índice y valor | U07 |
| **zip()** | Empareja múltiples secuencias | U07 |
| **diccionario** | Colección clave-valor: `{"ticker": "AAPL"}` | U08 |
| **defaultdict** | Dict con valor por defecto automático | U08 |
| **Counter** | Contador de frecuencias | U08 |
| **conjunto (set)** | Colección sin duplicados: `{1, 2, 3}` | U09 |
| **regex** | Expresiones regulares para patrones de texto | U09 |
| **CSV** | Valores separados por comas | U10 |
| **JSON** | Formato de intercambio de datos | U10 |
| **pathlib** | Manejo moderno de rutas de archivos | U10 |
| **función** | Bloque de código reutilizable con `def` | U11 |
| **type hints** | Anotaciones de tipo: `def f(x: int) -> float:` | U11 |
| **docstring** | Documentación de función: `"""Descripción."""` | U11 |
| **parámetro por defecto** | `def f(x=10)` | U11 |
| **\*args** | Argumentos posicionales variables | U11 |
| **\*\*kwargs** | Argumentos nombrados variables | U11 |
| **lambda** | Función anónima: `lambda x: x*2` | U12 |
| **decorador** | `@nombre` — modifica funciones | U12 |
| **closure** | Función que captura variables del scope externo | U12 |
| **map/filter** | Aplicar función a secuencia / filtrar | U12 |
| **módulo** | Archivo `.py` reutilizable | U13 |
| **paquete** | Directorio con `__init__.py` | U13 |
| **requirements.txt** | Dependencias del proyecto | U13 |
| **pyproject.toml** | Configuración moderna de proyecto | U13 |
| **if \_\_name\_\_ == "\_\_main\_\_"** | Punto de entrada | U13 |
| **excepción** | Error en tiempo de ejecución | U14 |
| **logging** | Sistema de registro de eventos | U14 |
| **pytest** | Framework de testing | U14 |

---

## 🏛️ Términos OOP (Programación Orientada a Objetos)

| Término | Definición | Unidad |
|---------|-----------|--------|
| **clase** | Plantilla para crear objetos: `class Accion:` | U15 |
| **objeto** | Instancia de una clase | U15 |
| **\_\_init\_\_** | Constructor de clase | U15 |
| **atributo** | Variable dentro de un objeto | U15 |
| **método** | Función dentro de una clase | U15 |
| **@property** | Getter que se accede como atributo | U15 |
| **herencia** | Una clase hereda de otra: `class Bono(Instrumento)` | U16 |
| **super()** | Llama al método de la clase padre | U16 |
| **ABC / @abstractmethod** | Clase abstracta que fuerza implementación | U16 |
| **polimorfismo** | Mismo método, diferente comportamiento | U16 |
| **composición** | "Tiene un" vs herencia "Es un" | U16 |
| **mixin** | Clase que agrega funcionalidad sin ser padre | U16 |
| **dunder** | Métodos especiales: `__add__`, `__eq__`, `__str__` | U17 |
| **@dataclass** | Decorador que genera `__init__` y otros automáticamente | U17 |
| **NamedTuple** | Tupla con nombres de campo | U17 |
| **\_\_slots\_\_** | Optimización de memoria en clases | U17 |
| **Strategy pattern** | Encapsula algoritmos intercambiables | U18 |
| **Factory pattern** | Crea objetos sin especificar clase concreta | U18 |
| **Observer pattern** | Notifica cambios a suscriptores | U18 |
| **generator (yield)** | Función que produce valores bajo demanda | U18 |

---

## 🔬 Términos NumPy/Pandas

| Término | Definición | Unidad |
|---------|-----------|--------|
| **NumPy array** | Estructura de datos numérica eficiente | U19 |
| **broadcasting** | Operación entre arrays de diferente forma | U19 |
| **vectorización** | Operación sobre todo el array sin loops | U19 |
| **GBM** | Movimiento Browniano Geométrico | U19 |
| **SVD** | Descomposición en Valores Singulares | U19 |
| **DataFrame** | Tabla bidimensional de Pandas | U20 |
| **Series** | Columna unidimensional de Pandas | U20 |
| **DatetimeIndex** | Índice de fechas en Pandas | U20 |
| **loc/iloc** | Acceso por etiqueta / posición | U20 |
| **groupby** | Agrupación y agregación | U20 |
| **resample** | Cambiar frecuencia temporal | U20 |
| **pct_change** | Cambio porcentual entre períodos | U20 |
| **rolling()** | Ventana móvil para cálculos | U21 |
| **ewm()** | Promedio móvil exponencial | U21 |
| **SMA** | Media móvil simple | U21 |
| **EMA** | Media móvil exponencial | U21 |
| **Bollinger Bands** | Bandas de volatilidad (SMA ± 2σ) | U21 |
| **RSI** | Índice de Fuerza Relativa | U21 |
| **MACD** | Convergencia/Divergencia de Medias Móviles | U21 |
| **candlestick chart** | Gráfico de velas japonesas | U22 |
| **heatmap** | Mapa de calor de correlaciones | U22 |
| **API REST** | Interfaz HTTP para obtener datos | U23 |
| **yfinance** | Librería para datos de Yahoo Finance | U23 |
| **web scraping** | Extraer datos de páginas web | U23 |

---

## 💰 Términos de Valoración y Finanzas Corporativas

| Término | Definición | Unidad |
|---------|-----------|--------|
| **TVM** | Valor del Dinero en el Tiempo | U24 |
| **VPN / NPV** | Valor Presente Neto | U24 |
| **TIR / IRR** | Tasa Interna de Retorno | U24 |
| **YTM** | Rendimiento al Vencimiento (bonos) | U24 |
| **Duration (Macaulay)** | Tiempo promedio ponderado de flujos de un bono | U24 |
| **Duration Modificada** | Sensibilidad del precio del bono a cambios en la tasa | U24 |
| **Convexidad** | Curvatura de la relación precio-tasa | U24 |
| **Curva de rendimiento** | Relación entre YTM y plazo | U24 |
| **Bootstrapping** | Construir curva cero-cupón desde bonos con cupón | U24 |
| **Income Statement** | Estado de resultados | U25 |
| **Balance Sheet** | Balance general | U25 |
| **Cash Flow Statement** | Estado de flujo de efectivo | U25 |
| **EBITDA** | Ganancias antes de intereses, impuestos, depreciación y amortización | U25 |
| **EBIT** | Ganancias antes de intereses e impuestos | U25 |
| **Gross Margin** | Margen bruto: (Revenue - COGS) / Revenue | U25 |
| **ROE** | Retorno sobre patrimonio: Net Income / Equity | U25 |
| **ROA** | Retorno sobre activos: Net Income / Assets | U25 |
| **DuPont (3 factores)** | ROE = Margen × Rotación × Apalancamiento | U25 |
| **DuPont (5 factores)** | Descomposición extendida del ROE | U25 |
| **Altman Z-Score** | Predictor de quiebra corporativa | U25 |
| **FCFF** | Flujo de Caja Libre para la Firma | U26 |
| **FCFE** | Flujo de Caja Libre para el Accionista | U26 |
| **WACC** | Costo Promedio Ponderado de Capital | U26 |
| **CAPM** | Capital Asset Pricing Model: E(R) = Rf + β(Rm - Rf) | U26 |
| **Beta (β)** | Sensibilidad de una acción al mercado | U26 |
| **Terminal Value** | Valor de la empresa más allá del período de proyección | U26 |
| **Gordon Growth Model** | TV = FCF × (1+g) / (WACC - g) | U26 |
| **Exit Multiple** | TV = EBITDA × múltiplo de salida | U26 |
| **EV/EBITDA** | Enterprise Value / EBITDA — múltiplo de valoración | U26 |
| **P/E Ratio** | Price to Earnings — múltiplo de valoración | U26 |
| **LBO** | Leveraged Buyout — adquisición apalancada | U27 |
| **Sources & Uses** | Fuentes y usos de fondos en un LBO | U27 |
| **Debt Schedule** | Calendario de deuda (senior, mezzanine, subordinada) | U27 |
| **Cash Sweep** | Exceso de caja para pagar deuda | U27 |
| **MOIC** | Multiple on Invested Capital | U27 |
| **IRR sponsor** | TIR del fondo de PE sobre su inversión | U27 |
| **Call Option** | Derecho a comprar a precio strike | U28 |
| **Put Option** | Derecho a vender a precio strike | U28 |
| **Black-Scholes-Merton** | Modelo de valoración de opciones europeas | U28 |
| **Delta** | Sensibilidad del precio de la opción al subyacente | U28 |
| **Gamma** | Sensibilidad de Delta al subyacente | U28 |
| **Theta** | Decaimiento temporal de la opción | U28 |
| **Vega** | Sensibilidad a la volatilidad | U28 |
| **Rho** | Sensibilidad a la tasa de interés | U28 |
| **CRR Binomial** | Modelo binomial de Cox-Ross-Rubinstein | U28 |
| **Implied Volatility** | Volatilidad implícita del mercado | U28 |
| **Volatility Smile** | Patrón de IV vs strike price | U28 |

---

## 📈 Términos de Portafolios y Riesgo

| Término | Definición | Unidad |
|---------|-----------|--------|
| **Markowitz** | Teoría moderna de portafolios (mean-variance) | U29 |
| **Frontera Eficiente** | Conjunto de portafolios óptimos riesgo/retorno | U29 |
| **Portafolio Tangente** | Máximo Sharpe Ratio | U29 |
| **CML** | Capital Market Line | U29 |
| **Sharpe Ratio** | (Rp - Rf) / σp | U29 |
| **Sortino Ratio** | Similar a Sharpe pero solo volatilidad downside | U29 |
| **CAPM** | Modelo de valoración de activos de capital | U30 |
| **Fama-French 3F** | Market + SMB + HML | U30 |
| **Fama-French 5F** | + RMW (profitability) + CMA (investment) | U30 |
| **Alpha** | Retorno excedente no explicado por factores | U30 |
| **Black-Litterman** | Modelo que combina equilibrio con views del inversor | U30 |
| **VaR (Value at Risk)** | Pérdida máxima en un horizonte con confianza dada | U31 |
| **CVaR / Expected Shortfall** | Promedio de pérdidas que exceden el VaR | U31 |
| **VaR Histórico** | Percentil de retornos históricos | U31 |
| **VaR Paramétrico** | Asume distribución normal | U31 |
| **VaR Monte Carlo** | Simula escenarios aleatorios | U31 |
| **Stress Testing** | Escenarios extremos (2008, COVID) | U31 |
| **Kupiec Test** | Backtesting estadístico del VaR | U31 |
| **HRP** | Hierarchical Risk Parity | U32 |
| **Risk Parity** | Igual contribución al riesgo | U32 |
| **Ledoit-Wolf** | Shrinkage de matriz de covarianza | U32 |
| **Equal Weight** | Portafolio 1/N como benchmark | U32 |

---

## 📐 Términos de Econometría

| Término | Definición | Unidad |
|---------|-----------|--------|
| **Distribución Normal** | Campana de Gauss | U33 |
| **Log-Normal** | Precios de acciones | U33 |
| **Fat Tails** | Colas gruesas — más eventos extremos | U33 |
| **Jarque-Bera** | Test de normalidad | U33 |
| **Bootstrap** | Remuestreo para intervalos de confianza | U33 |
| **Estacionariedad** | Media y varianza constantes en el tiempo | U34 |
| **ADF Test** | Augmented Dickey-Fuller (test de raíz unitaria) | U34 |
| **ARIMA** | Modelo Autorregresivo Integrado de Media Móvil | U34 |
| **GARCH(1,1)** | Modelo de volatilidad condicional | U34 |
| **ACF/PACF** | Funciones de autocorrelación | U34 |
| **OLS** | Mínimos Cuadrados Ordinarios | U35 |
| **GLS** | Mínimos Cuadrados Generalizados | U35 |
| **Newey-West** | Errores estándar robustos a autocorrelación | U35 |
| **Panel Data** | Datos con dimensión cross-section y temporal | U35 |
| **Fixed Effects** | Efectos fijos (control por entidad) | U35 |
| **Random Effects** | Efectos aleatorios | U35 |
| **Hausman Test** | Test FE vs RE | U35 |
| **Fama-MacBeth** | Regresión en dos etapas para paneles | U35 |
| **2SLS** | Mínimos Cuadrados en Dos Etapas (IV) | U35 |
| **SQL** | Lenguaje de consulta de bases de datos | U36 |
| **Window Functions** | LAG, LEAD, RANK en SQL | U36 |
| **CTE** | Common Table Expression (subconsultas) | U36 |

---

## 🤖 Términos de ML y Trading

| Término | Definición | Unidad |
|---------|-----------|--------|
| **Feature Engineering** | Crear variables predictoras | U37 |
| **TimeSeriesSplit** | Cross-validation temporal (sin data leakage) | U37 |
| **Random Forest** | Ensemble de árboles de decisión | U37 |
| **Regularización L1/L2** | Penalización para evitar overfitting | U37 |
| **XGBoost** | Gradient boosting extremo | U38 |
| **LightGBM** | Gradient boosting ligero de Microsoft | U38 |
| **PCA** | Análisis de Componentes Principales | U38 |
| **Autoencoder** | Red neuronal para reducción dimensional | U38 |
| **Market Regime** | Régimen de mercado (bull/bear/sideways) | U38 |
| **Backtesting** | Simular estrategia en datos históricos | U39 |
| **Momentum** | Comprar ganadores, vender perdedores | U39 |
| **Mean Reversion** | Precios revierten a su media | U39 |
| **Pairs Trading** | Arbitraje estadístico entre dos activos | U39 |
| **Cointegración** | Relación de largo plazo entre series | U39 |
| **Walk-Forward** | Optimización con ventana móvil | U39 |
| **Calmar Ratio** | Retorno / Max Drawdown | U39 |
| **threading** | Ejecución concurrente con hilos | U40 |
| **asyncio** | Programación asíncrona | U40 |
| **Docker** | Contenedores para despliegue | U40 |
| **CI/CD** | Integración y despliegue continuo | U40 |
| **Streamlit** | Framework para dashboards en Python | U41 |
| **Tear Sheet** | Resumen visual de performance de estrategia | U42 |

---

## 📝 Convenciones del Curso

| Símbolo | Significado |
|---------|------------|
| `$` | Comando en terminal (bash/zsh) |
| `>>>` | Intérprete interactivo de Python |
| 💡 | Dato curioso o truco |
| ⚠️ | Advertencia o error común |
| ✅ | Autoevaluación / ejercicio completado |
| 📝 | Instrucción para Knowledge Wiki |
