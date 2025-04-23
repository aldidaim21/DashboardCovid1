import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#show data
def load_data():
    df= pd.read_csv("covid_19_indonesia_time_series_all.csv")
    df = df[df["Location"] != "Indonesia"]
    return df

# Filter data berdasarkan tahun (optional)
def filter_data(df, year=None, locations=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    if locations:
        df = df[df['Location'].isin(locations)]
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else x
    )

def select_location(df):
    locations = sorted(df['Location'].unique())
    return st.sidebar.multiselect(
        "Pilih Provinsi 📍",
        options=locations,
        default=locations 
    )

def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data Covid-19 Indonesia 🔴⚪")
    st.dataframe(df_selected.head(10))
    
# Fungsi untuk total kasus
def total_case(df):    
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()

# Fungsi untuk total kematian
def total_death(df):
    total_mati = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_mati['Total Deaths'].sum()

# Fungsi untuk total sembuh
def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

# Tampilkan scoreboard/metrik dalam 3 kolom
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(label="🦠 Total Kasus", value=kasus,border=True)
    col2.metric(label="💀 Total Kematian", value=kematian, border=True)
    col3.metric(label="💚 Total Sembuh", value=sembuh, border=True)

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


def bar_chart1(df):
    # Ambil data terakhir per provinsi (group by Location ambil baris terakhir)
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest(5, 'Total Deaths')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='🔝 5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kematian', title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

def bar_chart2(df):
      # Ambil data terakhir per provinsi (group by Location ambil baris terakhir)
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()

    # Ambil 5 provinsi dengan kematian terbanyak
    top5 = df_last.nlargest(5, 'Total Recovered')

    # Buat bar chart
    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='greens',
        title='🔝 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(xaxis_title='Provinsi', yaxis_title='Total Kesembuhan', title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)

def map_chart(df, year=None):
    # Konversi kolom Date
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter data berdasarkan tahun
    if year:
        df = df[df['Date'].dt.year == year]

    # Agregasi data per lokasi
    df_agg = df.groupby(['Location', 'Latitude', 'Longitude'], as_index=False)['New Cases'].sum()
    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    # Validasi data
    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return

    # Buat scatter mapbox
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},  # Fokus Indonesia
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    # Gunakan style default Mapbox (tanpa perlu token khusus)
    fig.update_layout(
        mapbox_style="carto-positron",  # Alternatif: "open-street-map", "carto-darkmatter"
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    # Tampilkan peta di Streamlit
    st.plotly_chart(fig, use_container_width=True)
