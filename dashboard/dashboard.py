import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "../data/day.csv"))
df["dteday"] = pd.to_datetime(df["dteday"])
df.sort_values(by="dteday", inplace=True)
df.reset_index(drop=True, inplace=True)

# --- Helper functions ---
def create_daily_rentals_df(df):
    daily_df = df.groupby("dteday")["cnt"].sum().reset_index()
    daily_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return daily_df

def create_byseason_df(df):
    season_df = df.groupby("season")["cnt"].sum().reset_index()
    season_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return season_df

def create_byyear_df(df):
    year_df = df.groupby("yr")["cnt"].sum().reset_index()
    year_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return year_df

# --- Sidebar ---
with st.sidebar:
    st.image(os.path.join(BASE_DIR, "logo.jpg"), width=200)
    st.header("Filter Tanggal")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=df["dteday"].min(),
        max_value=df["dteday"].max(),
        value=[df["dteday"].min(), df["dteday"].max()]
    )

main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]
daily_df = create_daily_rentals_df(main_df)
season_df = create_byseason_df(main_df)
year_df = create_byyear_df(main_df)

# ============================================================
# HEADER
# ============================================================
st.title("🚲 Bike Sharing Dashboard ✨")

# --- Metrics ---
st.subheader("Ringkasan")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", f"{int(main_df['cnt'].sum()):,}")
col2.metric("Rata-rata Harian", f"{round(main_df['cnt'].mean(), 1):,}")
col3.metric("Rata-rata Kelembapan", f"{round(main_df['hum'].mean(), 2)}")

st.divider()

# --- Tren Harian ---
st.subheader("📈 Tren Penyewaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(16, 5))
ax.plot(daily_df["dteday"], daily_df["total_rentals"], linewidth=2, color="steelblue")
ax.fill_between(daily_df["dteday"], daily_df["total_rentals"], alpha=0.2, color="steelblue")
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Total Penyewaan", fontsize=12)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)
plt.close()

st.divider()

# ============================================================
# EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
st.header("🔍 Exploratory Data Analysis (EDA)")

# --- EDA 1: Distribusi Variabel Numerik ---
st.subheader("1. Distribusi Variabel Numerik")
st.caption("Histogram distribusi variabel numerik utama untuk memahami sebaran data.")

num_cols = ["cnt", "casual", "registered", "temp", "hum", "windspeed"]
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    axes[i].hist(main_df[col], bins=25, color="steelblue", edgecolor="white")
    axes[i].set_title(f"Distribusi {col}", fontsize=11)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Frekuensi")
plt.suptitle("Distribusi Variabel Numerik", fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- `cnt` terdistribusi mendekati normal dengan sedikit right-skew.\n"
        "- `casual` sangat right-skewed — pengguna kasual jauh lebih sedikit dari pengguna terdaftar.\n"
        "- `hum` tersebar merata, sementara `windspeed` condong ke nilai rendah."
    )

st.divider()

# --- EDA 2: Distribusi Variabel Kategorikal ---
st.subheader("2. Distribusi Variabel Kategorikal")
st.caption("Frekuensi tiap kategori pada variabel season, weathersit, workingday, dan weekday.")

cat_map = {
    "season": {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"},
    "weathersit": {1: "Clear", 2: "Mist/Cloudy", 3: "Light Rain/Snow"},
    "workingday": {0: "Libur/Akhir Pekan", 1: "Hari Kerja"},
    "weekday": {0: "Min", 1: "Sen", 2: "Sel", 3: "Rab", 4: "Kam", 5: "Jum", 6: "Sab"},
}
fig, axes = plt.subplots(1, 4, figsize=(18, 5))
colors = ["#FF9800", "#4CAF50", "#2196F3", "#9C27B0"]
for i, (col, mapping) in enumerate(cat_map.items()):
    counts = main_df[col].value_counts().sort_index()
    labels = [mapping.get(k, str(k)) for k in counts.index]
    axes[i].bar(labels, counts.values, color=colors[i], edgecolor="white")
    axes[i].set_title(f"Distribusi {col}", fontsize=11)
    axes[i].set_ylabel("Jumlah Hari")
    axes[i].tick_params(axis='x', rotation=20)
plt.suptitle("Distribusi Variabel Kategorikal", fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- Data tersebar merata di 4 musim.\n"
        "- Mayoritas hari adalah hari kerja (~68%).\n"
        "- Kondisi cuaca paling umum adalah cerah/berawan ringan."
    )

st.divider()

# --- EDA 3: Heatmap Korelasi ---
st.subheader("3. Korelasi Antar Variabel Numerik")
st.caption("Heatmap korelasi untuk mengidentifikasi variabel yang paling berpengaruh terhadap jumlah penyewaan.")

corr_cols = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
corr_matrix = main_df[corr_cols].corr()
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, linewidths=0.5, ax=ax)
ax.set_title("Heatmap Korelasi", fontsize=13, fontweight="bold")
plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- `temp` & `atemp` berkorelasi positif kuat dengan `cnt` (~0.63).\n"
        "- `hum` berkorelasi negatif lemah dengan `cnt` (~-0.10).\n"
        "- `windspeed` berkorelasi negatif lemah (~-0.23).\n"
        "- `registered` mendominasi `cnt` dengan korelasi ~0.95."
    )

st.divider()

# --- EDA 4: Hari Kerja vs Hari Libur ---
st.subheader("4. Penyewaan: Hari Kerja vs Hari Libur")
st.caption("Perbandingan distribusi dan rata-rata penyewaan berdasarkan jenis hari.")

main_df = main_df.copy()
main_df["workingday_label"] = main_df["workingday"].map({0: "Libur/Akhir Pekan", 1: "Hari Kerja"})

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(x="workingday_label", y="cnt", data=main_df, palette="Set2", ax=axes[0])
axes[0].set_title("Distribusi Penyewaan per Jenis Hari", fontsize=12)
axes[0].set_xlabel("Jenis Hari")
axes[0].set_ylabel("Jumlah Penyewaan")

weekday_avg = main_df.groupby("weekday")["cnt"].mean()
day_names = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"]
axes[1].bar(day_names, weekday_avg.values, color="coral", edgecolor="white")
axes[1].set_title("Rata-rata Penyewaan per Hari", fontsize=12)
axes[1].set_xlabel("Hari")
axes[1].set_ylabel("Rata-rata Penyewaan")

plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- Hari kerja memiliki rata-rata penyewaan sedikit lebih tinggi (~4.584 vs ~4.330).\n"
        "- Hari Jumat dan Sabtu cenderung memiliki penyewaan tertinggi.\n"
        "- Hari Minggu memiliki rata-rata terendah karena komuter tidak aktif."
    )

st.divider()

# --- EDA 5: Kelembapan vs Penyewaan ---
st.subheader("5. Hubungan Kelembapan dan Jumlah Penyewaan")
st.caption("Scatter plot dengan garis regresi dan rata-rata penyewaan per rentang kelembapan.")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.regplot(x="hum", y="cnt", data=main_df, ax=axes[0],
            scatter_kws={"alpha": 0.4, "color": "steelblue"},
            line_kws={"color": "red", "linewidth": 2})
axes[0].set_title("Kelembapan vs Jumlah Penyewaan", fontsize=12)
axes[0].set_xlabel("Kelembapan (hum)")
axes[0].set_ylabel("Jumlah Penyewaan")

main_df["hum_bin"] = pd.cut(main_df["hum"], bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                             labels=["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"])
hum_avg = main_df.groupby("hum_bin", observed=True)["cnt"].mean()
axes[1].bar(hum_avg.index.astype(str), hum_avg.values, color="teal", edgecolor="white")
axes[1].set_title("Rata-rata Penyewaan per Rentang Kelembapan", fontsize=12)
axes[1].set_xlabel("Rentang Kelembapan")
axes[1].set_ylabel("Rata-rata Penyewaan")

plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- Korelasi negatif lemah antara kelembapan dan penyewaan (r ≈ -0.10).\n"
        "- Penyewaan tertinggi pada kelembapan 40–60% (kondisi paling nyaman).\n"
        "- Kelembapan >80% menurunkan penyewaan secara signifikan."
    )

st.divider()

# --- EDA 6: Tren Musiman ---
st.subheader("6. Tren Penyewaan Berdasarkan Musim dan Bulan")
st.caption("Rata-rata penyewaan per musim dan tren bulanan per tahun.")

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_avg = main_df.groupby("season")["cnt"].mean()
season_avg.index = season_avg.index.map(season_labels)
axes[0].bar(season_avg.index, season_avg.values,
            color=["#4CAF50", "#FF9800", "#F44336", "#2196F3"], edgecolor="white")
axes[0].set_title("Rata-rata Penyewaan per Musim", fontsize=12)
axes[0].set_xlabel("Musim")
axes[0].set_ylabel("Rata-rata Penyewaan")

month_labels = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
for yr, label in [(0, "2011"), (1, "2012")]:
    data = main_df[main_df["yr"] == yr].groupby("mnth")["cnt"].mean()
    if not data.empty:
        axes[1].plot(data.index, data.values, marker="o", label=label, linewidth=2)
axes[1].set_title("Tren Penyewaan Bulanan per Tahun", fontsize=12)
axes[1].set_xlabel("Bulan")
axes[1].set_ylabel("Rata-rata Penyewaan")
axes[1].set_xticks(range(1, 13))
axes[1].set_xticklabels(month_labels, rotation=30)
axes[1].legend(title="Tahun")

plt.tight_layout()
st.pyplot(fig)
plt.close()

with st.expander("📌 Insight"):
    st.markdown(
        "- Musim gugur (Fall) memiliki rata-rata penyewaan tertinggi.\n"
        "- Pola musiman konsisten: naik dari awal tahun, puncak Jun–Sep, lalu turun.\n"
        "- Tahun 2012 secara konsisten lebih tinggi dari 2011 di semua bulan."
    )

st.divider()

# ============================================================
# VISUALISASI UTAMA (Pertanyaan Bisnis)
# ============================================================
st.header("📊 Visualisasi & Analisis")

st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="total_rentals", data=season_df, palette="Blues", ax=ax)
ax.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
ax.set_title("Total Penyewaan per Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)
plt.close()

st.subheader("Penyewaan Berdasarkan Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="yr", y="total_rentals", data=year_df, palette="Blues", ax=ax)
ax.set_xticklabels(["2011", "2012"])
ax.set_title("Total Penyewaan per Tahun")
ax.set_xlabel("Tahun")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)
plt.close()
