import pandas as pd
import streamlit as st
import plotly.express as px
import types

# Load data
@st.cache_data(hash_funcs={types.FunctionType: id})
def load_data():
    day_url = 'https://raw.githubusercontent.com/fitoooooo/Bangkit/main/day.csv'
    df_day = pd.read_csv(day_url) 
    return df_day

df_day = load_data()

# Set page title
st.title("Bike Share Dashboard")

# Display sidebar information
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama: Ahmad Nayef Al Fito**")

st.sidebar.title("Dataset Bike Share")
# Show the dataset if selected in the sidebar
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Data Mentah")
    st.write(df_day)

# Display summary statistics if selected in the sidebar
if st.sidebar.checkbox("Tampilkan Statistik Ringkas"):
    st.subheader("Statistik Ringkas")
    st.write(df_day.describe())

# Sidebar
st.sidebar.title("Pilihan Visualisasi")
visualization_option = st.sidebar.radio("Pilih visualisasi:", ["Suhu vs Jumlah Pengguna Terdaftar",
                                                               "Cuaca vs Jumlah Sewa Sepeda (Musim Panas)",
                                                               "Penggunaan Sepeda Berdasarkan Musim",
                                                               "Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja"])

# Visualisasi berdasarkan pilihan pada sidebar
if visualization_option == "Suhu vs Jumlah Pengguna Terdaftar":
    st.header("Hubungan Suhu dengan Jumlah Pengguna Terdaftar")
    fig = px.scatter(df_day, x="temp", y="registered", title="Hubungan Suhu dengan Jumlah Pengguna Terdaftar")
    fig.update_xaxes(title="Suhu (temp)")
    fig.update_yaxes(title="Jumlah Pengguna Terdaftar")
    st.plotly_chart(fig)

elif visualization_option == "Cuaca vs Jumlah Sewa Sepeda (Musim Panas)":
    st.header("Pengaruh Cuaca terhadap Jumlah Sewa Sepeda (Musim Panas)")
    filtered_data = df_day[df_day["season"] == 2]
    fig = px.bar(filtered_data, x="weathersit", y="cnt", title="Pengaruh Cuaca terhadap Jumlah Sewa Sepeda (Musim Panas)")
    fig.update_xaxes(title="Cuaca (weathersit)")
    fig.update_yaxes(title="Jumlah Sewa Sepeda (cnt)")
    st.plotly_chart(fig)

elif visualization_option == "Penggunaan Sepeda Berdasarkan Musim":
    st.header("Penggunaan Sepeda Berdasarkan Musim")
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_day['month'] = df_day['dteday'].dt.month
    fig = px.box(df_day, x='season', y='cnt', color='season',
                 category_orders={'season': ['1', '2', '3', '4']},
                 labels={'season': 'Musim', 'cnt': 'Jumlah Sewa Sepeda'})
    fig.update_layout(title='Penggunaan Sepeda Berdasarkan Musim',
                      xaxis_title='Musim', yaxis_title='Jumlah Sewa Sepeda')
    st.plotly_chart(fig)

else:
    st.header("Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja")
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_day['day_of_week'] = df_day['dteday'].dt.dayofweek
    df_day['is_weekend'] = df_day['day_of_week'].isin([5, 6]).astype(int)
    df_weekend = df_day.groupby('is_weekend')['cnt'].mean().reset_index()
    fig = px.bar(df_weekend, x='is_weekend', y='cnt', color='is_weekend',
                 labels={'is_weekend': 'Hari Libur (0: Tidak, 1: Ya)', 'cnt': 'Rata-rata Jumlah Sewa Sepeda'},
                 title='Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja',
                 text='cnt')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(xaxis_title='Hari Libur (0: Tidak, 1: Ya)', yaxis_title='Rata-rata Jumlah Sewa Sepeda')
    fig.update_xaxes(tickvals=[0, 1], ticktext=['Hari Kerja', 'Akhir Pekan'])
    st.plotly_chart(fig)
