import pandas as pd
import streamlit as st


@st.cache_data
def load_data(csv_path: str):

    df = pd.read_csv(csv_path)

    # Standardize column names
    df.columns = [col.strip() for col in df.columns]

    return df