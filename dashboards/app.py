import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# 1. Configuración de página
st.set_page_config(
    page_title="Sura - Data Quality Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Rutas relativas a la base de datos (dinámico basado en ubicación de app.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'db_financiera.sqlite')

# 3. Estilos CSS personalizados adicionales
st.markdown("""
    <style>
        .main { background-color: #f4f6f9; }
        h1, h2, h3 { color: #0033a0; font-family: 'Segoe UI', sans-serif;}
        .stMetric { background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #0033a0;}
        .metric-title { font-size: 14px; color: #555; }
        .metric-value { font-size: 24px; font-weight: bold; color: #0033a0; }
    </style>
""", unsafe_allow_html=True)

# 4. Encabezado
col1, col2 = st.columns([1, 6])
with col1:
    # Usamos un logo público de Sura desde internet
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/43/Logo_SURA.svg", width=120)
with col2:
    st.title("Centro de Monitoreo: Calidad de Datos")
    st.markdown("**Panel de trazabilidad y gobierno sobre excepciones financieras**")

st.divider()

# 5. Carga de Datos desde SQLite
@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(), pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    # Tabla de excepciones
    df_exc = pd.read_sql_query("SELECT * FROM transacciones_excepciones", conn)
    # Tabla oficial
    df_clean = pd.read_sql_query("SELECT * FROM transacciones", conn)
    conn.close()
    
    return df_exc, df_clean

df_excepciones, df_limpio = load_data()

if df_excepciones.empty and df_limpio.empty:
    st.error(f"❌ No se encontró la base de datos en {DB_PATH}. Por favor, ejecuta primero el script ETL `src/data_cleaning.py`.")
    st.stop()

# Procesamiento menor para visualización
df_excepciones['fecha_carga'] = pd.to_datetime(df_excepciones['fecha_carga'])
capital_riesgo = df_excepciones['valor_bruto'].sum()
cantidad_errores = len(df_excepciones)
total_limpios = len(df_limpio)
capital_oficial = df_limpio['valor_neto'].sum()

# 6. KPIs (Métricas Principales)
st.subheader("1. Impacto Financiero y Volumen")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Capital Inmovilizado (Riesgo)", f"${capital_riesgo:,.0f}", delta="En Cuarentena", delta_color="inverse")
with m2:
    st.metric("Transacciones Defectuosas", f"{cantidad_errores}", delta="Excepciones Aisladas", delta_color="inverse")
with m3:
    st.metric("Capital Oficial Procesado", f"${capital_oficial:,.0f}", delta="Aprobado")
with m4:
    st.metric("Transacciones Oficiales", f"{total_limpios}", delta="Calidad 100%")

st.divider()

# 7. Análisis Visual y Trazabilidad (Tabs)
st.subheader("2. Auditoría de Errores (Data Steward view)")

tab1, tab2 = st.tabs(["📊 Distribución de Errores", "🔎 Bandeja de Corrección (Data)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        # Agrupación por etiqueta de defecto
        df_agrupado = df_excepciones.groupby('etiqueta_dq').size().reset_index(name='Cantidad')
        fig_bar = px.bar(
            df_agrupado, 
            x='etiqueta_dq', 
            y='Cantidad',
            title="Volumen de Transacciones por Tipo de Error",
            labels={'etiqueta_dq': 'Motivo de Rechazo'},
            color='etiqueta_dq',
            color_discrete_sequence=['#0033a0', '#00b0f0', '#0087a3', '#002060']
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        # Riesgo económico por error
        df_riesgo = df_excepciones.groupby('etiqueta_dq')['valor_bruto'].sum().reset_index(name='Capital en Riesgo')
        fig_pie = px.pie(
            df_riesgo, 
            values='Capital en Riesgo', 
            names='etiqueta_dq',
            title="Distribución de Capital Inmovilizado por Error",
            color_discrete_sequence=['#0033a0', '#00b0f0', '#0087a3', '#002060'],
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.markdown("Busca y filtra transacciones específicas para corregirlas en el sistema de origen.")
    
    # Filtro interactivo
    filtro_tipo = st.selectbox("Filtrar por Tipo de Error:", ["Todos"] + list(df_excepciones['etiqueta_dq'].unique()))
    
    if filtro_tipo == "Todos":
        df_mostrar = df_excepciones
    else:
        df_mostrar = df_excepciones[df_excepciones['etiqueta_dq'] == filtro_tipo]
        
    st.dataframe(
        df_mostrar[['id_transaccion', 'etiqueta_dq', 'fecha_transaccion', 'valor_bruto', 'centro_costo', 'cliente', 'estado']],
        use_container_width=True,
        height=400
    )

st.divider()
st.caption("🛡️ **Pipeline de Data Governance Activo**: Los registros defectuosos mostrados en este panel han sido aislados automáticamente para evitar contaminar la Base Oficial (Single Source of Truth) que alimenta los reportes de KPIs y Rentabilidad.")
