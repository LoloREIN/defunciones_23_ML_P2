import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("/Users/lorenzoreinoso/Documents/defunciones_23_ML_P2/DatasetFinal.csv", low_memory=False)