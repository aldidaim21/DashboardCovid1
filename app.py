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
    df = load_data()
    year = select_year()
    locations = select_location(df)

    # Filter data
    df_filtered = filter_data(df, year, locations)
    kolom(df_filtered)
    pie_chart1(df_filtered)

    #barchart
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)


# Halaman DATA
elif menu == "Halaman Data":
    judul()
    df = load_data()
    year = select_year()
    locations = select_location(df)
    df_filtered = filter_data(df, year, locations)
    show_data(df_filtered)