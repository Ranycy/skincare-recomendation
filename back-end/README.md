# SkinSense AI — Backend

Backend Flask untuk platform rekomendasi produk skincare berbasis AI.
Bagian dari Capstone Pijak × IBM SkillsBuild — **PJK-GM066**.

---

## Prasyarat

- Python 3.11+
- API key dari [weatherapi.com](https://www.weatherapi.com/) (gratis)

---

## Cara Menjalankan

### 1. Masuk ke folder backend

```bash
cd back-end
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Buat file `.env`

Salin dari contoh lalu isi `WEATHERAPI_KEY`:

```bash
cp .env.example .env
```

Isi `.env`:

```env
FLASK_ENV=development
SECRET_KEY=ganti-dengan-secret-key-acak
DATABASE_URL=sqlite:///skinsense.db
WEATHERAPI_KEY=isi-api-key-kamu-di-sini
ML_MODEL_PATH=../machine-learning
JWT_EXPIRATION_HOURS=24
GUEST_SESSION_HOURS=24
```

### 4. Jalankan server

```bash
python run.py
```

Server berjalan di **`http://localhost:5000`**

---

## Verifikasi

Buka `http://localhost:5000` di browser — akan tampil dashboard status yang menunjukkan:

- ML Model loaded (1472 products)
- Database connected
- WeatherAPI Key configured

Atau cek via terminal:

```bash
curl http://localhost:5000/api/status
```

---

## Struktur Folder

```
back-end/
├── app/
│   ├── controllers/        # Business logic
│   │   ├── auth_controller.py
│   │   ├── recommend_controller.py
│   │   ├── history_controller.py
│   │   └── home_controller.py
│   ├── routes/             # Routing — hanya memanggil controller
│   │   ├── auth.py
│   │   ├── recommend.py
│   │   ├── history.py
│   │   └── home.py
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── questionnaire.py
│   │   └── recommendation.py
│   └── services/
│       └── weather_service.py
├── config.py
├── run.py
├── requirements.txt
├── .env.example
├── API_DOCS.md             # Dokumentasi lengkap API
└── SkinSense_AI.postman_collection.json
```

---

## API Docs

Dokumentasi lengkap seluruh endpoint tersedia di **[API_DOCS.md](API_DOCS.md)**.

Tersedia juga Postman collection di `SkinSense_AI.postman_collection.json` — import ke Postman untuk langsung testing.

---

## Catatan

- Database SQLite digunakan secara default untuk development. Ganti `DATABASE_URL` ke PostgreSQL untuk production.
- ML model (`machine-learning/services/recommender.py`) **tidak boleh diubah** — milik tim ML.
- WeatherAPI free tier tidak menyertakan data PM2.5, fallback otomatis ke `0.0`.
