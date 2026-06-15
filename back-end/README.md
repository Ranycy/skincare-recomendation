# SkinSense AI — Backend

Backend Flask untuk platform rekomendasi produk skincare berbasis AI.
Bagian dari Capstone Pijak × IBM SkillsBuild — **PJK-GM066**.

---

## Prasyarat

- Python 3.11+
- PostgreSQL 14+
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

### 3. Siapkan PostgreSQL

Buat database:

```sql
CREATE DATABASE skinsense;
```

### 4. Buat file `.env`

Salin dari contoh lalu isi:

```bash
cp .env.example .env
```

Isi `.env`:

```env
FLASK_ENV=development
SECRET_KEY=ganti-dengan-secret-key-acak
DATABASE_URL=postgresql://postgres:password@localhost:5432/skinsense
WEATHERAPI_KEY=isi-api-key-kamu-di-sini
ML_MODEL_PATH=../machine-learning
JWT_EXPIRATION_HOURS=24
GUEST_SESSION_HOURS=1
```

### 5. Jalankan server

```bash
python run.py
```

Server berjalan di **`http://localhost:5000`**

Tabel database otomatis dibuat saat pertama kali server dijalankan.

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
│   │   ├── profile_controller.py
│   │   ├── favorite_controller.py
│   │   └── home_controller.py
│   ├── routes/             # Routing — hanya memanggil controller
│   │   ├── auth.py
│   │   ├── recommend.py
│   │   ├── history.py
│   │   ├── profile.py
│   │   ├── favorites.py
│   │   └── home.py
│   ├── models/             # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── questionnaire.py
│   │   ├── recommendation.py
│   │   ├── skin_profile.py
│   │   └── favorite_product.py
│   ├── repositories/       # Database query layer
│   │   ├── auth_repository.py
│   │   ├── questionnaire_repository.py
│   │   ├── recommendation_repository.py
│   │   ├── skin_profile_repository.py
│   │   └── favorite_repository.py
│   └── services/
│       ├── weather_service.py
│       └── guidance_service.py
├── config.py
├── run.py
├── requirements.txt
├── .env.example
├── API_DOCS.md
└── SkinSense_AI.postman_collection.json
```

### Arsitektur

```
Request → Route → Controller → Repository → Model/DB
                      ↓
                   Service (weather, guidance)
```

- **Route** — parsing request, memanggil controller
- **Controller** — validasi, business logic, memanggil repository & service
- **Repository** — semua query database (CRUD)
- **Model** — definisi tabel (SQLAlchemy ORM)
- **Service** — logic eksternal (weather API, guidance text)

---

## API Docs

Dokumentasi lengkap seluruh endpoint tersedia di **[API_DOCS.md](API_DOCS.md)**.

Tersedia juga Postman collection di `SkinSense_AI.postman_collection.json` — import ke Postman untuk langsung testing.

---

## Catatan

- Database menggunakan **PostgreSQL**. Pastikan service PostgreSQL berjalan sebelum menjalankan server.
- ML model (`machine-learning/services/recommender.py`) **tidak boleh diubah** — milik tim ML.
- WeatherAPI free tier tidak menyertakan data PM2.5, fallback otomatis ke `0.0`.
