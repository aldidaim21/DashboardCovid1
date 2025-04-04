import streamlit as st
from data import *


#judul dashboard
def judul():
    st.title("Dashboard Covid-19 Indonesia")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data Covid-19 di Indonesia 🔴⚪")

st.sidebar.title("Navigasi")
menu= st.sidebar.radio("Pilih Halaman",["Home","Halaman Data"])



if menu == "Home":
    judul()
    kolom()
elif menu == "Halaman Data":
    judul()
    show_data()