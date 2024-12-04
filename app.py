import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Defunciones 2023",
    page_icon="📊",
    layout="wide"
)

df = load_data()

# Título y descripción
st.title("Análisis de Defunciones México 2023")
st.markdown("Exploración y análisis de los datos de defunciones registradas durante 2023 en México.")

# Sidebar con filtros relevantes
with st.sidebar:
    st.header("Filtros")
    
    # Filtro por sexo
    sexo_filter = st.multiselect(
        "Sexo",
        options=sorted(df['sexo'].unique()),
        default=sorted(df['sexo'].unique())
    )
    
    # Filtro por mes
    mes_filter = st.multiselect(
        "Mes de ocurrencia",
        options=sorted(df['mes_ocurr'].unique()),
        default=sorted(df['mes_ocurr'].unique())
    )
    
    # Filtro por entidad
    entidad_filter = st.multiselect(
        "Entidad de ocurrencia",
        options=sorted(df['ent_ocurr'].unique()),
        default=sorted(df['ent_ocurr'].unique())
    )

# Aplicar filtros
filtered_df = df[
    (df['sexo'].isin(sexo_filter)) &
    (df['mes_ocurr'].isin(mes_filter)) &
    (df['ent_ocurr'].isin(entidad_filter))
]

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Defunciones",
        value=f"{len(filtered_df):,}"
    )

with col2:
    edad_promedio = round(filtered_df['edad_final'].mean(), 1)
    st.metric(
        label="Edad Promedio",
        value=f"{edad_promedio} años"
    )

with col3:
    causa_principal = filtered_df['lista_mex'].mode()[0]
    st.metric(
        label="Causa Principal",
        value=causa_principal
    )

# Gráficas principales
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Defunciones por Mes")
    fig_mes = px.histogram(
        filtered_df,
        x='mes_ocurr',
        title='Distribución por Mes',
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig_mes, use_container_width=True)

with col_right:
    st.subheader("Distribución por Edad")
    fig_edad = px.histogram(
        filtered_df,
        x='edad_final',
        title='Distribución por Edad',
        color_discrete_sequence=['#2ca02c']
    )
    st.plotly_chart(fig_edad, use_container_width=True)

# Análisis adicional
st.subheader("Distribución por Estado Civil y Sexo")
fig_civil = px.histogram(
    filtered_df,
    x='edo_civil',
    color='sexo',
    barmode='group',
    title='Defunciones por Estado Civil y Sexo'
)
st.plotly_chart(fig_civil, use_container_width=True)

# Tabla de datos
with st.expander("Ver datos detallados"):
    st.dataframe(
        filtered_df.head(1000),
        use_container_width=True
    )

# Pie de página
st.markdown("---")
st.markdown("Datos proporcionados por INEGI - Registros de Mortalidad 2023")