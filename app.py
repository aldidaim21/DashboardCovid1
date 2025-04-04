import streamlit as st
from data import *

# Fungsi judul halaman
def judul():
    st.title("😷 Dashboard Covid-19 Indonesia")
    st.markdown("Selamat datang di dashboard interaktif untuk menganalisis data **Covid-19** di Indonesia 🇮🇩.")

# Sidebar navigasi
st.sidebar.title("📊 Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

# Halaman HOME
if menu == "Home": 
    judul()
    # Pilih tahun
    year = select_year()
    # Load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    kolom(df_filtered)
    pie_chart1(df_filtered)

# Halaman DATAx``
elif menu == "Halaman Data":
    judul()
    year = select_year()
    # Load & filter data
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)
