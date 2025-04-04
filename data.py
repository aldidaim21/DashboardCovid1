import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#show data
def load_data():
    df= pd.read_csv("covid_19_indonesia_time_series_all.csv")
    return df

# Filter data berdasarkan tahun (optional)
def filter_data(df, year=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else x
    )

def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia 🔴⚪")
    st.dataframe(df_selected.head(10))
    
# Fungsi untuk total kasus
def total_case(df):    
    total_kasus = df['Total Cases'].sum()
    return total_kasus

# Fungsi untuk total kematian
def total_death(df):
    total_mati = df['Total Deaths'].sum()
    return total_mati

# Fungsi untuk total sembuh
def total_recovery(df):
    total_sembuh = df['Total Recovered'].sum()
    return total_sembuh

# Tampilkan scoreboard/metrik dalam 3 kolom
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(label="🦠 Total Kasus", value=f"{kasus/1000:.1f}K",border=True)
    col2.metric(label="💀 Total Kematian", value=f"{kematian/1000:.1f}K", border=True)
    col3.metric(label="💚 Total Sembuh", value=f"{sembuh/1000:.1f}K", border=True)

def pie_chart1(df):
    # Ambil data total kematian dan sembuh
    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    # Buat DataFrame untuk Plotly
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sembuh]
    }

    # Buat pie chart dengan lubang (donut style)
    fig = px.pie(
        data, 
        names='Status', 
        values='Jumlah', 
        title='📊 Perbandingan Total Kematian vs Total Sembuh',
        hole=0.5,  
        color_discrete_sequence=['red', 'green']  
    )

    # Tampilkan chart di Streamlit
    st.plotly_chart(fig, use_container_width=True)