# SkinSense AI — API Documentation

> Backend API untuk platform rekomendasi produk skincare berbasis AI.
> Base URL: `http://localhost:5000`

---

## Authentication

### POST `/api/auth/register`

Register user baru.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "min6chars",
  "name": "User Name"
}
```

**Response `201`:**

```json
{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Email and password are required" }` |
| 400 | `{ "error": "Password must be at least 6 characters" }` |
| 409 | `{ "error": "Email already registered" }` |

---

### POST `/api/auth/login`

Login dan dapatkan JWT token.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response `200`:**

```json
{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Email and password are required" }` |
| 401 | `{ "error": "Invalid email or password" }` |

---

### POST `/api/auth/guest`

Buat guest session tanpa registrasi.

**Request:** _(empty body)_

**Response `201`:**

```json
{
  "user_id": "f8e7d6c5-...",
  "session_token": "b3a4c5d6-...",
  "expires_at": "2026-06-04T11:30:00+00:00"
}
```

---

### GET `/api/auth/me`

Info user yang sedang login.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "is_guest": false
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 401 | `{ "error": "Invalid or expired token" }` |
| 404 | `{ "error": "User not found" }` |

---

## Recommendation

### POST `/api/recommend`

Kirim profil kulit + lokasi → dapatkan rekomendasi produk skincare.

**Request:**

```json
{
  "user_id": "uuid-or-null",
  "session_token": "string-for-guest",
  "questionnaire": {
    "product_category": "sunscreen",
    "skin_type": "oily",
    "skin_concerns": ["acne", "dullness"],
    "activity_type": "outdoor",
    "avoided_ingredients": ["retinol"]
  },
  "location": {
    "lat": -6.2088,
    "lon": 106.8456,
    "method": "gps"
  }
}
```

| Field | Type | Required | Keterangan |
|-------|------|----------|------------|
| `user_id` | string | No | UUID registered user, null jika guest |
| `session_token` | string | No | Token dari `/api/auth/guest` |
| `questionnaire.product_category` | string | **Yes** | `moisturizer` \| `cleanser` \| `face mask` \| `eye cream` \| `sunscreen` |
| `questionnaire.skin_type` | string | **Yes** | `normal` \| `dry` \| `oily` \| `combination` \| `sensitive` |
| `questionnaire.skin_concerns` | string[] | No | `acne` \| `dullness` \| `aging` \| `dark spots` \| `dehydration` |
| `questionnaire.activity_type` | string | No | `indoor` \| `outdoor` — hanya relevan jika category = `sunscreen` |
| `questionnaire.avoided_ingredients` | string[] | No | Ingredient yang dihindari (hard filter) |
| `location.lat` | float | **Yes** | Latitude |
| `location.lon` | float | **Yes** | Longitude |
| `location.method` | string | No | `gps` \| `manual_map` — optional, untuk tracking saja |

**Response `200`:**

```json
{
  "questionnaire_id": "e1f2a3b4-...",
  "weather": {
    "temperature": 34.2,
    "humidity": 78,
    "uv_index": 9.0,
    "pm25": 38.4
  },
  "recommendations": [
    {
      "rank": 1,
      "product_name": "UV Perfect Aqua Essence",
      "brand": "L'OREAL",
      "category": "sunscreen",
      "skin_types": ["oily", "combination"],
      "active_ingredients": ["niacinamide", "zinc oxide"],
      "why_recommended": "Cocok karena sangat cocok untuk tipe kulit oily, serta melindungi dengan SPF 50 tinggi yang ideal untuk aktivitas luar ruangan (outdoor).",
      "score": 0.87
    }
  ]
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Invalid product_category. Must be one of: ..." }` |
| 400 | `{ "error": "Invalid skin_type. Must be one of: ..." }` |
| 400 | `{ "error": "Location (lat, lon) is required" }` |
| 502 | `{ "error": "Failed to fetch weather data: ..." }` |

---

## History

### GET `/api/history`

Riwayat rekomendasi untuk user yang login. Guest tidak punya history.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "history": [
    {
      "questionnaire_id": "e1f2a3b4-...",
      "product_category": "sunscreen",
      "skin_type": "oily",
      "skin_concerns": ["acne", "dullness"],
      "activity_type": "outdoor",
      "avoided_ingredients": ["retinol"],
      "location": {
        "lat": -6.2088,
        "lon": 106.8456,
        "method": "gps"
      },
      "created_at": "2026-06-03T10:30:00",
      "weather": {
        "temperature": 34.2,
        "humidity": 78,
        "uv_index": 9.0,
        "pm25": 38.4
      },
      "recommendations": [
        {
          "rank": 1,
          "product_name": "UV Perfect Aqua Essence",
          "brand": "L'OREAL",
          "category": "sunscreen",
          "skin_types": ["oily", "combination"],
          "active_ingredients": ["niacinamide", "zinc oxide"],
          "why_recommended": "Cocok karena ...",
          "score": 0.87
        }
      ]
    }
  ]
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 401 | `{ "error": "Invalid or expired token" }` |

---

## Health Check

### GET `/api/status`

JSON health check untuk monitoring.

**Response `200`:**

```json
{
  "status": "ok",
  "model_loaded": true,
  "product_count": 1472,
  "database": true,
  "weather_api_configured": true,
  "ml_model_path": "../machine-learning",
  "server_time": "2026-06-03T11:30:00+00:00"
}
```

| Field | Keterangan |
|-------|------------|
| `status` | `"ok"` jika model & DB ready, `"degraded"` jika salah satu down |
| `model_loaded` | ML model berhasil load products.json |
| `product_count` | Jumlah produk yang di-load (expected: 1472) |
| `database` | Koneksi DB aktif |
| `weather_api_configured` | WEATHERAPI_KEY sudah di-set di .env |

---

## Reference Values

### Product Category

| Value | Label |
|-------|-------|
| `moisturizer` | Pelembab |
| `cleanser` | Pembersih Wajah |
| `face mask` | Masker Wajah |
| `eye cream` | Krim Mata |
| `sunscreen` | Tabir Surya |

### Skin Type

| Value | Label |
|-------|-------|
| `normal` | Normal |
| `dry` | Kering |
| `oily` | Berminyak |
| `combination` | Kombinasi |
| `sensitive` | Sensitif |

### Skin Concerns

| Value | Label |
|-------|-------|
| `acne` | Jerawat |
| `dullness` | Kulit Kusam |
| `aging` | Penuaan / Anti-Aging |
| `dark spots` | Noda Hitam |
| `dehydration` | Kulit Dehidrasi |

### Activity Type

| Value | Keterangan |
|-------|------------|
| `indoor` | Aktivitas dalam ruangan |
| `outdoor` | Aktivitas luar ruangan |

> `activity_type` hanya relevan jika `product_category = "sunscreen"`. Untuk kategori lain, field ini diabaikan.

---

## Environment Variables

| Variable | Default | Keterangan |
|----------|---------|------------|
| `SECRET_KEY` | `dev-secret-key...` | Secret key untuk JWT signing |
| `DATABASE_URL` | `sqlite:///skinsense.db` | Connection string database |
| `WEATHERAPI_KEY` | _(kosong)_ | API key dari weatherapi.com |
| `ML_MODEL_PATH` | `../machine-learning` | Path ke folder machine-learning |
| `JWT_EXPIRATION_HOURS` | `24` | Masa berlaku JWT token (jam) |
| `GUEST_SESSION_HOURS` | `24` | Masa berlaku guest session (jam) |

---

## Quick Start

```bash
cd back-end
copy .env.example .env     # lalu isi WEATHERAPI_KEY
pip install -r requirements.txt
python run.py
```

Server jalan di `http://localhost:5000`. Buka di browser untuk melihat dashboard status + API docs interaktif.

---

*SkinSense AI — Capstone Pijak × IBM SkillsBuild — PJK-GM066*
