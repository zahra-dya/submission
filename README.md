# 🚲 Bike Sharing Dashboard

Dashboard interaktif berbasis **Streamlit** untuk menganalisis data penyewaan sepeda harian menggunakan dataset Bike Sharing (2011–2012).

---

## 📊 Features

- Visualisasi tren penyewaan sepeda harian
- Analisis penyewaan berdasarkan musim dan tahun
- Perbandingan penyewaan hari kerja vs hari libur
- Analisis hubungan kelembapan dan jumlah penyewaan
- Filter rentang tanggal interaktif

---

## 📁 Project Structure

```
submission/
├── dashboard/
│   ├── dashboard.py       # Streamlit app
│   └── logo.jpg
├── data/
│   └── day.csv            # Dataset utama
├── notebook.ipynb         # Analisis data lengkap
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Environment

### 1. Clone / Download Project

Pastikan seluruh file sudah tersedia di direktori lokal kamu.

### 2. Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install streamlit pandas matplotlib seaborn babel
```

---

## ▶️ Run Streamlit App

Jalankan perintah berikut dari **root direktori project** (`submission/`):

```bash
streamlit run dashboard/dashboard.py
```

> ⚠️ Pastikan menjalankan perintah dari root direktori (`submission/`), bukan dari dalam folder `dashboard/`, agar path pembacaan file data (`data/day.csv`) dapat ditemukan dengan benar.

---

## 📦 Dataset

Dataset `day.csv` berisi informasi penyewaan sepeda harian, meliputi:

| Kolom | Deskripsi |
|---|---|
| `dteday` | Tanggal penyewaan |
| `season` | Musim (1=Spring, 2=Summer, 3=Fall, 4=Winter) |
| `workingday` | Hari kerja (1) atau libur/akhir pekan (0) |
| `weathersit` | Kondisi cuaca |
| `temp` | Suhu (ternormalisasi) |
| `hum` | Kelembapan (ternormalisasi) |
| `windspeed` | Kecepatan angin (ternormalisasi) |
| `casual` | Jumlah pengguna kasual |
| `registered` | Jumlah pengguna terdaftar |
| `cnt` | Total penyewaan sepeda |

---

## 👤 Author

**Nindya Zahra**  
📧 cdcc899d6x1477@student.devacademy.id  
🆔 Dicoding ID: nindyazahra
