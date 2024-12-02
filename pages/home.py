import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import numpy as np


def prepare_data(sql_result_df):
    # Mapeo de nombres de estados a códigos
    state_codes = {
        'Ciudad de México': 'MX-CMX', 'Michoacán de Ocampo': 'MX-MIC',
        'Sinaloa': 'MX-SIN', 'Durango': 'MX-DUR', 'Guerrero': 'MX-GRO',
        'Chiapas': 'MX-CHP', 'Guanajuato': 'MX-GUA', 'Hidalgo': 'MX-HID',
        'Nayarit': 'MX-NAY', 'Coahuila de Zaragoza': 'MX-COA',
        'Chihuahua': 'MX-CHH', 'Morelos': 'MX-MOR',
        'Veracruz de Ignacio de la Llave': 'MX-VER', 'Yucatán': 'MX-YUC',
        'Colima': 'MX-COL', 'Campeche': 'MX-CAM', 'Tabasco': 'MX-TAB',
        'Oaxaca': 'MX-OAX', 'San Luis Potosí': 'MX-SLP',
        'Aguascalientes': 'MX-AGU', 'Baja California Sur': 'MX-BCS',
        'Puebla': 'MX-PUE', 'Nuevo León': 'MX-NLE', 'Tamaulipas': 'MX-TAM',
        'Zacatecas': 'MX-ZAC', 'Tlaxcala': 'MX-TLA', 'Querétaro': 'MX-QUE',
        'Jalisco': 'MX-JAL', 'Quintana Roo': 'MX-ROO', 'Sonora': 'MX-SON',
        'México': 'MX-MEX', 'Baja California': 'MX-BCN'
    }

    df = sql_result_df.rename(columns={'ent_mat': 'estado', 'count(1)': 'muertes'})
    df['id'] = df['estado'].map(state_codes)

    # Calcular rangos dinámicos basados en los cuartiles de los datos
    q1, q2, q3 = np.percentile(df['muertes'], [25, 50, 75])
    
    # Crear bins únicos
    bins = sorted(list(set([0, q1, q2, q3, float('inf')])))
    labels = ['Very Low', 'Low', 'Mid', 'High'][:len(bins)-1]  # Ajustar las etiquetas al número de bins

    # Categorizar los valores usando rangos dinámicos
    df['categoria'] = pd.cut(
        df['muertes'],
        bins=bins,
        labels=labels,
        duplicates='drop'  # Agregar esta opción
    )

    return df, [q1, q2, q3]

def create_interactive_map(df, title="2023", ranges=None):
    url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
    geojson_data = requests.get(url).json()

    fig = px.choropleth(
        df,
        geojson=geojson_data,
        locations='id',
        color='muertes',
        hover_data={
            'estado': True,
            'categoria': True,
            'muertes': ':,',
            'id': False
        },
        color_continuous_scale=[
            [0, 'rgba(255, 255, 255, 0.2)'],
            [0.25, 'rgba(222, 255, 13, 0.3)'],
            [0.5, 'rgba(222, 255, 13, 0.5)'],
            [0.75, 'rgba(222, 255, 13, 0.7)'],
            [1, 'rgba(222, 255, 13, 1.0)']
        ],
        featureidkey='properties.id',
        range_color=[df['muertes'].min(), df['muertes'].max()]
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.5)",
        showland=True,
        landcolor="#15110F",
        showcountries=True,
        countrycolor="rgba(255, 255, 255, 0.5)",
        showframe=False,
        projection_scale=2,
        center=dict(lat=24, lon=-102)
    )

    if ranges:
        min_val = df['muertes'].min()
        max_val = df['muertes'].max()
        tickvals = [min_val] + ranges + [max_val]
        ticktext = [f'{int(val):,}' for val in tickvals]

    fig.update_layout(
        paper_bgcolor='#15110F',
        plot_bgcolor='#15110F',
        geo=dict(
            bgcolor='#15110F',
            lakecolor='#15110F',
        ),
        title=dict(
            text=f'Deaths by {title}',
            font=dict(size=20, color='white', family='Arial Black'),
            x=0.5,
            y=0.95
        ),
        coloraxis_colorbar=dict(
            title='Number of<br>deaths',
            tickfont=dict(color='white', size=12),
            titlefont=dict(color='white', size=14),
            thickness=20,
            len=0.75,
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            ticktext=ticktext if ranges else None,
            tickvals=tickvals if ranges else None,
            tickmode='array' if ranges else 'auto'
        ),
        hoverlabel=dict(
            bgcolor='rgba(50, 50, 50, 0.9)',
            font_size=14,
            font_color='white',
            bordercolor='rgba(255, 255, 255, 0.2)'
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                     "Category: %{customdata[1]}<br>" +
                     "# of Deaths: %{customdata[2]}<extra></extra>"
    )

    return fig

# Configuración de la página de Streamlit
st.set_page_config(page_title="Mexico Deaths Map", layout="wide")

# Título principal
st.title("Deaths Distribution in Mexico (2023)")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Defunciones_Mex_2023.csv", low_memory=False)

df = load_data()

# Sidebar para controles
st.sidebar.header("Filters")

# Obtener lista única de causas de muerte
causes = sorted(df["lista_mex"].dropna().unique())

# Selector de causa de muerte
selected_cause = st.sidebar.selectbox(
    "Select Cause of Death",
    causes
)

# Filtrar datos según la causa seleccionada
df_filtered = df[df["lista_mex"] == selected_cause]
df_deaths = df_filtered["ent_ocurr"].value_counts().reset_index()
df_deaths.columns = ['ent_mat', 'count(1)']

# Preparar datos y crear mapa
df_prepared, ranges = prepare_data(df_deaths)
fig = create_interactive_map(df_prepared, selected_cause, ranges)

# Mostrar el mapa
st.plotly_chart(fig, use_container_width=True)

# Mostrar estadísticas adicionales
st.subheader("Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Deaths", f"{df_deaths['count(1)'].sum():,}")
with col2:
    st.metric("Most Affected State", df_prepared.loc[df_prepared['muertes'].idxmax(), 'estado'])
with col3:
    st.metric("Average Deaths per State", f"{df_deaths['count(1)'].mean():,.0f}")

# Tabla de datos
if st.checkbox("Show Detailed Data"):
    st.dataframe(
        df_prepared[['estado', 'muertes', 'categoria']]
        .sort_values('muertes', ascending=False)
    )