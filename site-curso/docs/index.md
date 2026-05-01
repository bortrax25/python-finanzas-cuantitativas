---
hide:
  - navigation
  - toc
  - footer
---

<style>
  /* --- HERO --- */
  .hero {
    text-align: center;
    padding: 4rem 1rem 2.5rem;
  }
  .hero h1 {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--color-navy);
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
    animation: heroIn 0.8s ease-out;
  }
  .hero h1 span {
    color: var(--color-gold);
  }
  .hero .subtitle {
    font-size: 1.1rem;
    color: var(--color-text-light);
    margin-bottom: 2rem;
    max-width: 580px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.7;
    animation: heroIn 0.8s ease-out 0.15s both;
  }
  @keyframes heroIn {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* --- SEARCH --- */
  .search-box {
    max-width: 500px;
    margin: 0 auto 2.5rem;
    animation: heroIn 0.8s ease-out 0.3s both;
  }
  .search-box input {
    width: 100%;
    padding: 0.9rem 1.4rem;
    font-size: 1rem;
    font-family: inherit;
    border: 2px solid var(--color-border);
    border-radius: 12px;
    background: var(--color-cream);
    color: var(--color-text);
    outline: none;
    transition: all 0.3s ease;
  }
  .search-box input:focus {
    border-color: var(--color-gold);
    box-shadow: 0 0 0 4px var(--color-gold-pale);
  }
  .search-box .hint {
    font-size: 0.8rem;
    color: var(--color-text-light);
    margin-top: 0.5rem;
    text-align: center;
  }

  /* --- STATS --- */
  .stats-bar {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-bottom: 3rem;
    animation: heroIn 0.8s ease-out 0.45s both;
  }
  .stat {
    text-align: center;
  }
  .stat .number {
    font-family: "Playfair Display", Georgia, serif;
    font-size: 2rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--color-gold), var(--color-gold-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
    line-height: 1;
  }
  .stat .label {
    font-size: 0.78rem;
    color: var(--color-text-light);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 0.3rem;
  }

  /* --- QUICK LINKS --- */
  .quick-links {
    text-align: center;
    margin-bottom: 2.5rem;
    animation: heroIn 0.8s ease-out 0.6s both;
  }
  .quick-links a {
    display: inline-block;
    margin: 0 0.6rem;
    padding: 0.4rem 1rem;
    border: 1px solid var(--color-border);
    border-radius: 20px;
    color: var(--color-text-light);
    text-decoration: none;
    font-size: 0.85rem;
    transition: all 0.2s ease;
  }
  .quick-links a:hover {
    border-color: var(--color-gold);
    color: var(--color-gold);
    background: var(--color-gold-pale);
    text-decoration: none;
  }

  /* --- PHASE GRID --- */
  .phase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
    gap: 1.2rem;
    max-width: 1000px;
    margin: 0 auto 4rem;
    padding: 0 1rem;
  }
  .phase-card {
    position: relative;
    background: var(--color-cream);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    text-decoration: none;
    color: inherit;
    display: block;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                box-shadow 0.3s ease,
                border-color 0.3s ease;
    animation: cardIn 0.6s ease-out both;
  }
  .phase-card:nth-child(1) { animation-delay: 0.1s; }
  .phase-card:nth-child(2) { animation-delay: 0.15s; }
  .phase-card:nth-child(3) { animation-delay: 0.2s; }
  .phase-card:nth-child(4) { animation-delay: 0.25s; }
  .phase-card:nth-child(5) { animation-delay: 0.3s; }
  .phase-card:nth-child(6) { animation-delay: 0.35s; }
  .phase-card:nth-child(7) { animation-delay: 0.4s; }
  .phase-card:nth-child(8) { animation-delay: 0.45s; }
  .phase-card:nth-child(9) { animation-delay: 0.5s; }
  .phase-card:nth-child(10){ animation-delay: 0.55s; }
  .phase-card:nth-child(11){ animation-delay: 0.6s; }

  @keyframes cardIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Golden top border accent */
  .phase-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--color-gold), var(--color-gold-light));
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .phase-card:hover::before {
    opacity: 1;
  }
  .phase-card:hover {
    border-color: var(--color-gold);
    box-shadow: 0 8px 30px rgba(184, 134, 11, 0.12);
    transform: translateY(-4px);
    text-decoration: none;
  }
  .phase-card.hidden {
    display: none;
  }

  .phase-card .icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }
  .phase-card .name {
    font-family: "Playfair Display", Georgia, serif;
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.15rem;
    color: var(--color-navy);
  }
  .phase-card .units {
    font-size: 0.78rem;
    color: var(--color-text-light);
    letter-spacing: 0.04em;
  }
  .phase-card .desc {
    font-size: 0.85rem;
    color: var(--color-text-light);
    margin-top: 0.5rem;
    line-height: 1.5;
  }

  .no-results {
    grid-column: 1 / -1;
    text-align: center;
    color: var(--color-text-light);
    padding: 3rem;
    display: none;
    font-size: 1rem;
  }
</style>

<div class="hero">
  <h1>Python para <span>Finanzas Cuantitativas</span></h1>
  <p class="subtitle">
    Curso completo desde fundamentos de programación hasta modelos de valoración DCF/LBO, gestión de portafolios, machine learning y trading algorítmico.
  </p>

  <div class="search-box">
    <input
      type="text"
      id="phaseSearch"
      placeholder="Buscar por tema: DCF, opciones, VaR, Monte Carlo, LBO..."
      oninput="filterPhases()"
    >
    <div class="hint">Escribe para filtrar — o explora las fases abajo</div>
  </div>

  <div class="stats-bar">
    <div class="stat"><span class="number">43</span><span class="label">Unidades</span></div>
    <div class="stat"><span class="number">11</span><span class="label">Fases</span></div>
    <div class="stat"><span class="number">99+</span><span class="label">Ejercicios</span></div>
    <div class="stat"><span class="number">250+</span><span class="label">Conceptos</span></div>
  </div>

  <div class="quick-links">
    <a href="progreso/">📋 Progreso</a>
    <a href="glosario/">📖 Glosario</a>
    <a href="bibliografia/">📚 Bibliografía</a>
    <a href="ejercicios/">💻 Ejercicios</a>
  </div>
</div>

<div class="phase-grid" id="phaseGrid">
  <a class="phase-card" href="fase-0/" data-keywords="entorno herramientas setup python instalacion venv vs code git jupyter notebook">
    <div class="icon">🔧</div>
    <div class="name">Fase 0 — Entorno y Herramientas</div>
    <div class="units">U00–U01 · 2 unidades</div>
    <div class="desc">Python, VS Code, Git, Jupyter Notebooks y flujo de trabajo cuantitativo</div>
  </a>

  <a class="phase-card" href="fase-1/" data-keywords="fundamentos variables tipos operadores condicionales bucles for while input print if elif else">
    <div class="icon">🧱</div>
    <div class="name">Fase 1 — Fundamentos de Python</div>
    <div class="units">U02–U06 · 5 unidades</div>
    <div class="desc">Variables, operadores, I/O, condicionales, bucles — todo con contexto financiero</div>
  </a>

  <a class="phase-card" href="fase-2/" data-keywords="listas tuplas diccionarios sets conjuntos archivos csv json datos estructuras">
    <div class="icon">📊</div>
    <div class="name">Fase 2 — Estructuras de Datos</div>
    <div class="units">U07–U10 · 4 unidades</div>
    <div class="desc">Listas, tuplas, diccionarios, sets, archivos CSV/JSON y datos de mercado</div>
  </a>

  <a class="phase-card" href="fase-3/" data-keywords="funciones modulos paquetes lambda decoradores closures logging errores pytest testing">
    <div class="icon">⚙️</div>
    <div class="name">Fase 3 — Funciones y Módulos</div>
    <div class="units">U11–U14 · 4 unidades</div>
    <div class="desc">Funciones, decoradores, módulos, paquetes, errores, logging y testing</div>
  </a>

  <a class="phase-card" href="fase-4/" data-keywords="oop programacion orientada objetos clases herencia polimorfismo dataclass patrones diseño">
    <div class="icon">🏛️</div>
    <div class="name">Fase 4 — Programación OOP</div>
    <div class="units">U15–U18 · 4 unidades</div>
    <div class="desc">Clases, herencia, polimorfismo, data classes y patrones de diseño financieros</div>
  </a>

  <a class="phase-card" href="fase-5/" data-keywords="numpy pandas matplotlib plotly visualizacion datos web scraping apis yfinance ciencia datos">
    <div class="icon">🔬</div>
    <div class="name">Fase 5 — Stack Científico</div>
    <div class="units">U19–U23 · 5 unidades</div>
    <div class="desc">NumPy, Pandas, visualización (Matplotlib/Plotly) y APIs financieras</div>
  </a>

  <a class="phase-card" href="fase-6/" data-keywords="valoracion dcf lbo descuento flujos bonos opciones black scholes derivados renta fija estados financieros wacc">
    <div class="icon">💰</div>
    <div class="name">Fase 6 — Valoración Financiera</div>
    <div class="units">U24–U28 · 5 unidades</div>
    <div class="desc">TVM, estados financieros, DCF, LBO, opciones y Black-Scholes</div>
  </a>

  <a class="phase-card" href="fase-7/" data-keywords="portafolio markowitz riesgo var cvar hrp black litterman sharpe optimizacion factores fama french">
    <div class="icon">📈</div>
    <div class="name">Fase 7 — Portafolios y Riesgo</div>
    <div class="units">U29–U32 · 4 unidades</div>
    <div class="desc">Markowitz, factores Fama-French, VaR/CVaR, HRP y optimización avanzada</div>
  </a>

  <a class="phase-card" href="fase-8/" data-keywords="econometria estadistica probabilidad distribuciones series tiempo arima garch panel data regresion sql base datos">
    <div class="icon">📐</div>
    <div class="name">Fase 8 — Métodos Cuantitativos</div>
    <div class="units">U33–U36 · 4 unidades</div>
    <div class="desc">Distribuciones, ARIMA/GARCH, panel data, Fama-MacBeth y SQL financiero</div>
  </a>

  <a class="phase-card" href="fase-9/" data-keywords="machine learning ml scikit learn xgboost trading algoritmico backtesting estrategias infraestructura deep learning">
    <div class="icon">🤖</div>
    <div class="name">Fase 9 — ML y Trading Algorítmico</div>
    <div class="units">U37–U40 · 4 unidades</div>
    <div class="desc">Scikit-learn, XGBoost, backtesting, estrategias de trading y producción</div>
  </a>

  <a class="phase-card" href="fase-10/" data-keywords="proyectos finales plataforma sistema trading end-to-end recursos carrera profesional streamlit">
    <div class="icon">🚀</div>
    <div class="name">Fase 10 — Proyectos Finales</div>
    <div class="units">U41–U43 · 3 unidades</div>
    <div class="desc">Plataforma de análisis, sistema de trading y ruta profesional</div>
  </a>
</div>

<div class="no-results" id="noResults">
  <p>No se encontraron fases para "<span id="searchTerm"></span>".</p>
  <p>Prueba con: DCF, opciones, VaR, machine learning, bonos...</p>
</div>

<script>
  function filterPhases() {
    const term = document.getElementById('phaseSearch').value.toLowerCase().trim();
    const cards = document.querySelectorAll('.phase-card');
    const noResults = document.getElementById('noResults');
    const searchTermEl = document.getElementById('searchTerm');
    let visible = 0;

    cards.forEach(card => {
      const keywords = card.getAttribute('data-keywords') + ' ' +
                       card.querySelector('.name').textContent + ' ' +
                       card.querySelector('.desc').textContent;
      if (!term || keywords.toLowerCase().includes(term)) {
        card.classList.remove('hidden');
        visible++;
      } else {
        card.classList.add('hidden');
      }
    });

    noResults.style.display = visible === 0 ? 'block' : 'none';
    if (visible === 0) searchTermEl.textContent = term;
  }
</script>
