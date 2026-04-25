import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Style visualisasi
sns.set(style="dark")

# Membaca Dataset

df = pd.read_csv("day.csv")

# Mengubah kolom tanggal menjadi datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Fungsi Analisis
# Total penyewaan harian
def create_daily_rentals_df(df):
    daily_df = df.groupby("dteday")["cnt"].sum().reset_index()

    daily_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)

    return daily_df


# Total penyewaan berdasarkan musim
def create_byseason_df(df):
    season_df = df.groupby("season")["cnt"].sum().reset_index()

    season_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)

    return season_df


# Total penyewaan berdasarkan tahun
def create_byyear_df(df):
    year_df = df.groupby("yr")["cnt"].sum().reset_index()

    year_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)

    return year_df

# Menyiapkan DataFrame

daily_df = create_daily_rentals_df(df)
season_df = create_byseason_df(df)
year_df = create_byyear_df(df)


datetime_columns = ["dteday"]

df.sort_values(by="dteday", inplace=True)
df.reset_index(inplace=True)

for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

    min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar: 
    st.image("logo.jpg", width=200)

    st.header("Filter Tanggal")

    # Memilih rentang tanggal
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]
    

# Header Dashboard
st.title("Dicoding Collection Dashboard :sparkles: ")


# Visualisasi
st.subheader("Insight Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = int(main_df["cnt"].sum())
    st.metric("Total Rentals", value=total_rentals)

with col2:
    average_rentals = round(main_df["cnt"].mean(), 2)
    st.metric("Average Rentals", value=average_rentals)

with col3:
    average_humidity = round(main_df["hum"].mean(), 2)
    st.metric("Average Humidity", value=average_humidity)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    daily_df["dteday"],
    daily_df["total_rentals"],
    marker='o',
    linewidth=2
)

ax.set_title("Daily Bike Rentals", fontsize=20)
ax.set_xlabel("Date", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)


st.subheader("Perbandingan Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    x="workingday",
    y="cnt",
    data=main_df,
    ax=ax
)

ax.set_title("Hari Kerja vs Hari Libur")
ax.set_xlabel("Working Day")
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)


st.subheader("Hubungan Kelembaban dan Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))

sns.scatterplot(
    x="hum",
    y="cnt",
    data=main_df,
    ax=ax
)

ax.set_title("Humidity vs Bike Rentals")
ax.set_xlabel("Humidity")
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

st.subheader("Jumlah Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    x="season",
    y="total_rentals",
    data=season_df,
    palette="Blues",
    ax=ax
)

ax.set_title("Bike Rentals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Total Rentals")

st.pyplot(fig)

st.subheader("Jumlah Penyewaan Berdasarkan Tahun")

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    x="yr",
    y="total_rentals",
    data=year_df,
    palette="Blues",
    ax=ax
)

ax.set_title("Bike Rentals by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Total Rentals")

st.pyplot(fig)


