# main.py — Plataforma de Análisis Cuantitativo
# Punto de entrada de la aplicación Streamlit.

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Agregar directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TICKERS_DEFAULT, FECHA_INICIO_DEFAULT, FECHA_FIN_DEFAULT
from data.descargador import descargar_datos
from fundamental.ratios import calcular_ratios
from fundamental.dcf import modelo_dcf
from fundamental.dupont import analisis_dupont
from tecnico.indicadores import calcular_indicadores
from tecnico.senales import generar_senales
from portafolio.optimizador import optimizar_portafolio
from portafolio.frontera import calcular_frontera_eficiente
from riesgo.var import calcular_var
from riesgo.stress import stress_test
from riesgo.metricas import calcular_metricas_riesgo
from reportes.generador_pdf import generar_reporte_pdf
from ui.componentes import (
    crear_seccion_titulo,
    crear_metricas_kpi,
    crear_grafico_velas,
    crear_tabla_formateada,
)

# Configuración de la página
st.set_page_config(
    page_title="Plataforma de Análisis Cuantitativo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Plataforma de Análisis Cuantitativo")
st.markdown("*Análisis fundamental, técnico, portafolio y riesgo — todo en un solo lugar.*")

# ============================================================
# Sidebar — Selección de Activos
# ============================================================
with st.sidebar:
    st.header("📈 Selección de Activos")
    
    tickers_input = st.text_input(
        "Tickers (separados por coma)",
        value=",".join(TICKERS_DEFAULT),
        help="Ejemplo: AAPL, MSFT, GOOGL"
    )
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input(
            "Fecha inicio",
            value=FECHA_INICIO_DEFAULT,
        )
    with col2:
        fecha_fin = st.date_input(
            "Fecha fin",
            value=FECHA_FIN_DEFAULT,
        )
    
    if st.button("🔍 Descargar Datos", use_container_width=True):
        with st.spinner("Descargando datos del mercado..."):
            st.session_state.datos_precios = descargar_datos(
                tickers, fecha_inicio, fecha_fin
            )
            st.session_state.tickers_activos = tickers
            st.success(f"Datos descargados: {len(tickers)} activos")
    
    st.divider()
    
    # Navegación
    st.header("🧭 Módulos")
    seccion = st.radio(
        "Seleccionar módulo",
        [
            "📊 Resumen",
            "💰 Análisis Fundamental",
            "📉 Análisis Técnico",
            "🎯 Optimización de Portafolio",
            "⚠️ Gestión de Riesgo",
            "📄 Generar Reporte",
        ]
    )

# ============================================================
# Inicializar estado de sesión
# ============================================================
if "datos_precios" not in st.session_state:
    st.session_state.datos_precios = None
    st.session_state.tickers_activos = []

# ============================================================
# Verificar datos cargados
# ============================================================
if st.session_state.datos_precios is None:
    st.info("👈 Selecciona tickers y haz clic en **Descargar Datos** para comenzar.")
    
    # Mostrar datos de ejemplo mientras tanto
    st.subheader("Vista previa — Datos de ejemplo")
    
    np.random.seed(42)
    fechas_ejemplo = pd.date_range("2024-01-01", periods=60, freq="B")
    precios_ejemplo = pd.DataFrame({
        "AAPL": 185 + np.cumsum(np.random.normal(0, 0.5, 60)),
        "MSFT": 380 + np.cumsum(np.random.normal(0, 1, 60)),
        "GOOGL": 140 + np.cumsum(np.random.normal(0, 0.4, 60)),
    }, index=fechas_ejemplo)
    
    st.line_chart(precios_ejemplo)
    st.stop()

# ============================================================
# Datos cargados — Mostrar módulo seleccionado
# ============================================================
datos = st.session_state.datos_precios
tickers = st.session_state.tickers_activos

if seccion == "📊 Resumen":
    crear_seccion_titulo("Resumen del Mercado", "Vista general de los activos seleccionados")
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcular métricas rápidas
    retornos = datos["Close"].pct_change().dropna()
    
    with col1:
        rendimiento_total = (datos["Close"].iloc[-1] / datos["Close"].iloc[0] - 1).mean()
        st.metric("Rendimiento Promedio", f"{rendimiento_total:.2%}")
    
    with col2:
        volatilidad = retornos.std().mean() * np.sqrt(252)
        st.metric("Volatilidad Anual", f"{volatilidad:.2%}")
    
    with col3:
        sharpe = (retornos.mean().mean() / retornos.std().mean()) * np.sqrt(252)
        st.metric("Sharpe Aproximado", f"{sharpe:.2f}")
    
    with col4:
        max_dd = (datos["Close"] / datos["Close"].cummax() - 1).min().min()
        st.metric("Max Drawdown", f"{max_dd:.2%}")
    
    # Gráfico de precios
    st.subheader("Precios de Cierre")
    st.line_chart(datos["Close"])
    
    # Gráfico de rendimientos acumulados
    st.subheader("Rendimientos Acumulados")
    rend_acum = (1 + retornos).cumprod()
    st.line_chart(rend_acum)

elif seccion == "💰 Análisis Fundamental":
    crear_seccion_titulo("Análisis Fundamental", "Ratios financieros, DCF y DuPont")
    
    sub_modulo = st.selectbox(
        "Seleccionar análisis",
        ["Ratios Financieros", "Modelo DCF", "Análisis DuPont"]
    )
    
    ticker_seleccionado = st.selectbox("Seleccionar activo", tickers)
    
    if sub_modulo == "Ratios Financieros":
        st.subheader(f"Ratios Financieros — {ticker_seleccionado}")
        
        with st.spinner("Calculando ratios..."):
            ratios = calcular_ratios(ticker_seleccionado)
            crear_tabla_formateada(ratios)
    
    elif sub_modulo == "Modelo DCF":
        st.subheader(f"Valoración DCF — {ticker_seleccionado}")
        
        col1, col2 = st.columns(2)
        with col1:
            crecimiento = st.slider("Crecimiento de FCF (%)", 0.0, 30.0, 10.0) / 100
            wacc = st.slider("WACC (%)", 5.0, 20.0, 10.0) / 100
        with col2:
            margen = st.slider("Margen FCF (%)", 5.0, 40.0, 20.0) / 100
            crecimiento_terminal = st.slider("Crecimiento terminal (%)", 0.0, 5.0, 2.5) / 100
        
        if st.button("Calcular Valoración"):
            with st.spinner("Ejecutando modelo DCF..."):
                resultado_dcf = modelo_dcf(
                    ticker_seleccionado,
                    crecimiento, wacc, margen, crecimiento_terminal
                )
                st.metric("Valor Intrínseco por Acción", f"${resultado_dcf['valor_accion']:.2f}")
                st.metric("Precio Actual", f"${resultado_dcf['precio_actual']:.2f}")
                st.metric("Upside/Downside", f"{resultado_dcf['upside']:.2%}")
    
    elif sub_modulo == "Análisis DuPont":
        st.subheader(f"Análisis DuPont — {ticker_seleccionado}")
        
        with st.spinner("Calculando DuPont..."):
            dupont = analisis_dupont(ticker_seleccionado)
            st.write("**ROE = Margen Neto × Rotación Activos × Multiplicador Patrimonial**")
            crear_tabla_formateada(dupont)

elif seccion == "📉 Análisis Técnico":
    crear_seccion_titulo("Análisis Técnico", "Indicadores, patrones y señales de trading")
    
    ticker_seleccionado = st.selectbox("Seleccionar activo", tickers)
    precios_ticker = datos["Close"][ticker_seleccionado]
    
    # Gráfico de velas
    st.subheader(f"Gráfico de Velas — {ticker_seleccionado}")
    fig_velas = crear_grafico_velas(ticker_seleccionado, datos)
    st.plotly_chart(fig_velas, use_container_width=True)
    
    # Indicadores
    st.subheader("Indicadores Técnicos")
    
    indicadores_seleccionados = st.multiselect(
        "Seleccionar indicadores",
        ["SMA 20", "SMA 50", "SMA 200", "EMA 12", "EMA 26",
         "Bollinger Bands", "RSI (14)", "MACD"],
        default=["SMA 20", "SMA 50"]
    )
    
    if indicadores_seleccionados:
        with st.spinner("Calculando indicadores..."):
            df_indicadores = calcular_indicadores(precios_ticker, indicadores_seleccionados)
            st.line_chart(df_indicadores)
    
    # Señales
    st.subheader("Señales de Trading")
    with st.spinner("Generando señales..."):
        df_senales = generar_senales(precios_ticker)
        
        ultima_senal = df_senales.iloc[-1]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("RSI", f"{ultima_senal.get('rsi', 'N/A')}")
        with col2:
            st.metric("MACD", ultima_senal.get('senal_macd', 'N/A'))
        with col3:
            st.metric("SMA Cruce", ultima_senal.get('senal_sma', 'N/A'))

elif seccion == "🎯 Optimización de Portafolio":
    crear_seccion_titulo("Optimización de Portafolio", "Markowitz, HRP y Risk Parity")
    
    retornos = datos["Close"].pct_change().dropna()
    
    metodo = st.selectbox(
        "Método de optimización",
        ["Equal Weight", "Mínima Varianza", "Máximo Sharpe", "Risk Parity", "HRP"]
    )
    
    if st.button("Optimizar Portafolio"):
        with st.spinner("Optimizando..."):
            # Frontera eficiente
            fig_frontera, pesos_optimos = calcular_frontera_eficiente(retornos, metodo)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.plotly_chart(fig_frontera, use_container_width=True)
            
            with col2:
                st.subheader("Pesos Óptimos")
                df_pesos = pd.DataFrame({
                    "Activo": retornos.columns,
                    "Peso (%)": pesos_optimos * 100
                }).sort_values("Peso (%)", ascending=False)
                crear_tabla_formateada(df_pesos)
            
            # Métricas del portafolio óptimo
            ret_port = (retornos * pesos_optimos).sum(axis=1)
            metricas_port = {
                "Retorno Anualizado": ret_port.mean() * 252,
                "Volatilidad Anualizada": ret_port.std() * np.sqrt(252),
                "Sharpe Ratio": (ret_port.mean() / ret_port.std()) * np.sqrt(252),
            }
            st.subheader("Métricas del Portafolio Óptimo")
            cols = st.columns(3)
            for col, (nombre, valor) in zip(cols, metricas_port.items()):
                with col:
                    st.metric(nombre, f"{valor:.4f}" if "Sharpe" not in nombre else f"{valor:.2f}")

elif seccion == "⚠️ Gestión de Riesgo":
    crear_seccion_titulo("Gestión de Riesgo", "VaR, Stress Testing y Backtesting")
    
    retornos = datos["Close"].pct_change().dropna()
    retornos_portafolio = retornos.mean(axis=1)
    
    sub_modulo = st.selectbox(
        "Seleccionar análisis",
        ["Value at Risk (VaR)", "Stress Testing", "Métricas de Riesgo"]
    )
    
    if sub_modulo == "Value at Risk (VaR)":
        st.subheader("Value at Risk — Portafolio Equitativo")
        
        col1, col2 = st.columns(2)
        with col1:
            confianza = st.slider("Nivel de confianza", 0.90, 0.999, 0.95, 0.01)
        with col2:
            horizonte = st.slider("Horizonte (días)", 1, 30, 1)
        
        if st.button("Calcular VaR"):
            with st.spinner("Calculando VaR..."):
                resultados_var = calcular_var(retornos_portafolio, confianza, horizonte)
                
                cols = st.columns(3)
                with cols[0]:
                    st.metric("VaR Histórico", f"{resultados_var['historico']:.2%}")
                with cols[1]:
                    st.metric("VaR Paramétrico", f"{resultados_var['parametrico']:.2%}")
                with cols[2]:
                    st.metric("VaR Monte Carlo", f"{resultados_var['monte_carlo']:.2%}")
                
                st.metric("CVaR (Expected Shortfall)", f"{resultados_var['cvar']:.2%}")
    
    elif sub_modulo == "Stress Testing":
        st.subheader("Stress Testing — Escenarios Históricos")
        
        escenarios = st.multiselect(
            "Seleccionar escenarios",
            ["Crisis 2008 (-38%)", "COVID 2020 (-34%)", "Dot-com 2000 (-49%)",
             "Flash Crash 2010 (-9%)", "Taper Tantrum 2013 (-5%)"],
            default=["Crisis 2008 (-38%)", "COVID 2020 (-34%)"]
        )
        
        if escenarios and st.button("Ejecutar Stress Test"):
            with st.spinner("Calculando impacto..."):
                resultados_stress = stress_test(retornos_portafolio, escenarios)
                crear_tabla_formateada(pd.DataFrame(resultados_stress))
    
    elif sub_modulo == "Métricas de Riesgo":
        st.subheader("Métricas de Riesgo")
        
        with st.spinner("Calculando métricas..."):
            metricas_riesgo = calcular_metricas_riesgo(retornos_portafolio)
            
            for nombre, valor in metricas_riesgo.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{nombre}**")
                with col2:
                    if isinstance(valor, float):
                        st.write(f"{valor:.4f}")
                    else:
                        st.write(valor)

elif seccion == "📄 Generar Reporte":
    crear_seccion_titulo("Generar Reporte PDF", "Reporte profesional con análisis completo")
    
    ticker_seleccionado = st.selectbox("Seleccionar activo principal", tickers)
    
    incluir_secciones = st.multiselect(
        "Secciones a incluir",
        ["Resumen Ejecutivo", "Análisis Fundamental", "Análisis Técnico",
         "Optimización de Portafolio", "Gestión de Riesgo"],
        default=["Resumen Ejecutivo", "Análisis Fundamental", "Análisis Técnico",
                 "Optimización de Portafolio", "Gestión de Riesgo"]
    )
    
    if st.button("📄 Generar Reporte PDF", type="primary"):
        with st.spinner("Generando reporte..."):
            ruta_pdf = generar_reporte_pdf(
                ticker_seleccionado, datos, incluir_secciones
            )
            st.success(f"Reporte generado: {ruta_pdf}")
            
            with open(ruta_pdf, "rb") as f:
                st.download_button(
                    "⬇️ Descargar Reporte PDF",
                    f,
                    file_name=f"reporte_{ticker_seleccionado}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption(
    "Plataforma de Análisis Cuantitativo — Curso Python para Finanzas Cuantitativas | "
    "Datos: Yahoo Finance | "
    f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
