import streamlit as st
import pandas as pd
from pandas import read_excel

if "df" not in st.session_state:
    st.session_state.df = read_excel(r'data\Temp.xlsx')  # your initial df
df = st.session_state.df

df = df.T
df.loc['Date', 0:'Total'] = df.loc['Date', 0:'Total'].map(lambda x: x.day if isinstance(x, pd.Timestamp) else x)
df = st.data_editor(df.fillna(''))
