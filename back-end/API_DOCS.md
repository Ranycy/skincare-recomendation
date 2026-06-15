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
  "name": "User Name",
  "preferred_locale": "id"
}
```

| Field | Type | Required | Keterangan |
|-------|------|----------|------------|
| `email` | string | **Yes** | Email unik |
| `password` | string | **Yes** | Minimal 6 karakter |
| `name` | string | **Yes** | Nama tampilan |
| `preferred_locale` | string | No | `id` \| `en` (default: `en`) |

**Response `201`:**

```json
{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "is_guest": false,
  "preferred_locale": "id",
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
  "is_guest": false,
  "preferred_locale": "id",
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
  "expires_at": "2026-06-15T11:30:00+00:00"
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
  "is_guest": false,
  "preferred_locale": "id"
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

Bisa menggunakan JWT token (registered user) atau `user_id` + `session_token` (guest).

**Headers (opsional untuk registered user):**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "user_id": "uuid-or-null",
  "session_token": "string-for-guest",
  "locale": "id",
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
| `user_id` | string | No | UUID registered user, null jika pakai JWT |
| `session_token` | string | No | Token dari `/api/auth/guest` |
| `locale` | string | No | `id` \| `en` — bahasa response (default: user preference atau `en`) |
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
  "locale": "id",
  "questionnaire_id": "e1f2a3b4-...",
  "weather": {
    "location_name": "Menteng, Jakarta",
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
      "why_recommended": "L'OREAL UV Perfect Aqua Essence menjadi kandidat tabir surya dengan skor kecocokan 87%...",
      "explanation_factors": {
        "skin_type_match": true,
        "matched_concerns": ["jerawat", "kulit kusam"],
        "weather_reason": "UV sedang tinggi",
        "ingredient_highlights": ["niacinamide", "zinc oxide"],
        "summary_points": [
          "Cocok untuk kulit berminyak",
          "Relevan untuk jerawat, kulit kusam",
          "Kandungan utama: niacinamide, zinc oxide",
          "Disesuaikan dengan UV sedang tinggi"
        ],
        "avoidance_note": "Tidak terdeteksi kandungan yang kamu pilih untuk dihindari"
      },
      "score": 0.87
    }
  ],
  "weather_insights": [
    {
      "type": "uv",
      "level": "high",
      "message": "Indeks UV 9 sedang tinggi. Prioritaskan tabir surya..."
    }
  ],
  "routine_summary": {
    "morning_focus": "Perlindungan tabir surya dan pemakaian ulang...",
    "midday_focus": "Gunakan ulang tabir surya...",
    "evening_focus": "Pembersihan lebih teliti lalu hidrasi...",
    "weekly_focus": "Pantau area T dan pilih tekstur...",
    "ingredient_focus": ["niacinamide", "zinc oxide"],
    "avoid_reminder": ["retinol"],
    "steps": [
      { "time": "Morning", "message": "..." },
      { "time": "Midday", "message": "..." },
      { "time": "Evening", "message": "..." },
      { "time": "Weekly", "message": "..." }
    ]
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Invalid product_category. Must be one of: ..." }` |
| 400 | `{ "error": "Invalid skin_type. Must be one of: ..." }` |
| 400 | `{ "error": "Location (lat, lon) is required" }` |
| 401 | `{ "error": "Guest session is required" }` |
| 401 | `{ "error": "Invalid or expired guest session" }` |
| 502 | `{ "error": "Failed to fetch weather data: ..." }` |

---

## History

### GET `/api/history`

Riwayat rekomendasi user (dengan pagination).

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**

| Param | Type | Default | Keterangan |
|-------|------|---------|------------|
| `page` | int | 1 | Halaman |
| `limit` | int | 10 | Item per halaman (max 50) |
| `locale` | string | user pref | `id` \| `en` |

**Response `200`:**

```json
{
  "locale": "id",
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
      "created_at": "2026-06-15T10:30:00",
      "weather": {
        "location_name": "Menteng, Jakarta",
        "temperature": 34.2,
        "humidity": 78,
        "uv_index": 9.0,
        "pm25": 38.4
      },
      "weather_insights": [...],
      "routine_summary": {...},
      "top_recommendation": {
        "rank": 1,
        "product_name": "UV Perfect Aqua Essence",
        "brand": "L'OREAL",
        "category": "sunscreen",
        "score": 0.87,
        "...": "..."
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "total_pages": 3
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 401 | `{ "error": "Invalid or expired token" }` |

---

### GET `/api/history/<questionnaire_id>`

Detail lengkap satu riwayat rekomendasi (termasuk semua produk).

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**

| Param | Type | Default | Keterangan |
|-------|------|---------|------------|
| `locale` | string | user pref | `id` \| `en` |

**Response `200`:**

```json
{
  "locale": "id",
  "history_item": {
    "questionnaire_id": "e1f2a3b4-...",
    "product_category": "sunscreen",
    "skin_type": "oily",
    "skin_concerns": ["acne", "dullness"],
    "activity_type": "outdoor",
    "avoided_ingredients": ["retinol"],
    "location": { "lat": -6.2088, "lon": 106.8456, "method": "gps" },
    "created_at": "2026-06-15T10:30:00",
    "weather": { "location_name": "Menteng, Jakarta", "temperature": 34.2, "humidity": 78, "uv_index": 9.0, "pm25": 38.4 },
    "weather_insights": [...],
    "routine_summary": {...},
    "top_recommendation": {...},
    "recommendations": [
      {
        "rank": 1,
        "product_name": "UV Perfect Aqua Essence",
        "brand": "L'OREAL",
        "category": "sunscreen",
        "skin_types": ["oily", "combination"],
        "active_ingredients": ["niacinamide", "zinc oxide"],
        "why_recommended": "...",
        "score": 0.87,
        "explanation_factors": {...}
      }
    ]
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 404 | `{ "error": "History item not found" }` |

---

### DELETE `/api/history/<questionnaire_id>`

Hapus satu riwayat rekomendasi beserta semua data terkait.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "message": "History item deleted"
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 404 | `{ "error": "History item not found" }` |

---

## Skin Profile

### GET `/api/profile/skin`

Ambil profil kulit user yang tersimpan.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "profile": {
    "id": "a1b2c3d4-...",
    "skin_type": "oily",
    "skin_concerns": ["acne", "dullness"],
    "avoided_ingredients": ["retinol"],
    "default_product_category": "sunscreen",
    "default_activity_type": "outdoor",
    "created_at": "2026-06-15T10:00:00",
    "updated_at": "2026-06-15T10:00:00"
  }
}
```

> `profile` bernilai `null` jika belum pernah disimpan.

---

### PUT `/api/profile/skin`

Simpan atau update profil kulit user (upsert).

**Headers:**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "skin_type": "oily",
  "skin_concerns": ["acne", "dullness"],
  "avoided_ingredients": ["retinol"],
  "default_product_category": "sunscreen",
  "default_activity_type": "outdoor"
}
```

| Field | Type | Required | Keterangan |
|-------|------|----------|------------|
| `skin_type` | string | **Yes** | `normal` \| `dry` \| `oily` \| `combination` \| `sensitive` |
| `skin_concerns` | string[] | No | List of skin concerns |
| `avoided_ingredients` | string[] | No | Ingredients to avoid |
| `default_product_category` | string | No | Default category untuk form |
| `default_activity_type` | string | No | `indoor` \| `outdoor` |

**Response `200`:**

```json
{
  "profile": {
    "id": "a1b2c3d4-...",
    "skin_type": "oily",
    "skin_concerns": ["acne", "dullness"],
    "avoided_ingredients": ["retinol"],
    "default_product_category": "sunscreen",
    "default_activity_type": "outdoor",
    "created_at": "2026-06-15T10:00:00",
    "updated_at": "2026-06-15T10:30:00"
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Invalid skin_type. Must be one of: ..." }` |
| 400 | `{ "error": "Invalid default_product_category. Must be one of: ..." }` |
| 400 | `{ "error": "Invalid default_activity_type. Must be indoor or outdoor" }` |
| 401 | `{ "error": "Authorization header required" }` |

---

## Preferences

### GET `/api/profile/preferences`

Ambil preferensi user (bahasa).

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "preferences": {
    "preferred_locale": "id"
  }
}
```

---

### PUT `/api/profile/preferences`

Update preferensi bahasa user.

**Headers:**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "preferred_locale": "id"
}
```

**Response `200`:**

```json
{
  "preferences": {
    "preferred_locale": "id"
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "Unsupported locale" }` |
| 401 | `{ "error": "Authorization header required" }` |

---

## Favorites

### GET `/api/favorites`

Daftar produk favorit user.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "favorites": [
    {
      "id": "f1a2b3c4-...",
      "product_name": "UV Perfect Aqua Essence",
      "brand": "L'OREAL",
      "category": "sunscreen",
      "score": 0.87,
      "source_questionnaire_id": "e1f2a3b4-...",
      "created_at": "2026-06-15T10:30:00"
    }
  ]
}
```

---

### POST `/api/favorites`

Tambah produk ke favorit. Jika sudah ada (duplikat), tidak membuat baru.

**Headers:**

```
Authorization: Bearer <token>
```

**Request:**

```json
{
  "product_name": "UV Perfect Aqua Essence",
  "brand": "L'OREAL",
  "category": "sunscreen",
  "score": 0.87,
  "source_questionnaire_id": "e1f2a3b4-..."
}
```

| Field | Type | Required | Keterangan |
|-------|------|----------|------------|
| `product_name` | string | **Yes** | Nama produk |
| `brand` | string | No | Brand |
| `category` | string | No | Kategori produk |
| `score` | float | No | Skor dari rekomendasi |
| `source_questionnaire_id` | string | No | ID riwayat asal rekomendasi |

**Response `201`:**

```json
{
  "favorite": {
    "id": "f1a2b3c4-...",
    "product_name": "UV Perfect Aqua Essence",
    "brand": "L'OREAL",
    "category": "sunscreen",
    "score": 0.87,
    "source_questionnaire_id": "e1f2a3b4-...",
    "created_at": "2026-06-15T10:30:00"
  }
}
```

**Errors:**

| Code | Body |
|------|------|
| 400 | `{ "error": "product_name is required" }` |
| 401 | `{ "error": "Authorization header required" }` |

---

### DELETE `/api/favorites/<favorite_id>`

Hapus produk dari favorit.

**Headers:**

```
Authorization: Bearer <token>
```

**Response `200`:**

```json
{
  "message": "Favorite product removed"
}
```

**Errors:**

| Code | Body |
|------|------|
| 401 | `{ "error": "Authorization header required" }` |
| 404 | `{ "error": "Favorite product not found" }` |

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
  "ml_model_path": "/app/machine-learning",
  "server_time": "2026-06-15T11:30:00+00:00"
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

| Value | Label ID | Label EN |
|-------|----------|----------|
| `moisturizer` | Pelembap | Moisturizer |
| `cleanser` | Pembersih wajah | Cleanser |
| `face mask` | Masker wajah | Face mask |
| `eye cream` | Krim mata | Eye cream |
| `sunscreen` | Tabir surya | Sunscreen |

### Skin Type

| Value | Label ID | Label EN |
|-------|----------|----------|
| `normal` | Normal | Normal |
| `dry` | Kering | Dry |
| `oily` | Berminyak | Oily |
| `combination` | Kombinasi | Combination |
| `sensitive` | Sensitif | Sensitive |

### Skin Concerns

| Value | Label ID | Label EN |
|-------|----------|----------|
| `acne` | Jerawat | Acne |
| `dullness` | Kulit kusam | Dullness |
| `aging` | Tanda penuaan | Aging signs |
| `dark spots` | Bekas jerawat atau noda gelap | Dark spots |
| `dehydration` | Dehidrasi kulit | Dehydration |

### Activity Type

| Value | Keterangan |
|-------|------------|
| `indoor` | Aktivitas dalam ruangan |
| `outdoor` | Aktivitas luar ruangan |

> `activity_type` hanya relevan jika `product_category = "sunscreen"`.

### Locale

| Value | Keterangan |
|-------|------------|
| `id` | Bahasa Indonesia |
| `en` | English (default) |

---

## Environment Variables

| Variable | Default | Keterangan |
|----------|---------|------------|
| `SECRET_KEY` | `dev-secret-key...` | Secret key untuk JWT signing |
| `DATABASE_URL` | `sqlite:///skinsense.db` | Connection string database (PostgreSQL untuk production) |
| `WEATHERAPI_KEY` | _(kosong)_ | API key dari weatherapi.com |
| `ML_MODEL_PATH` | `../machine-learning` | Path ke folder machine-learning |
| `JWT_EXPIRATION_HOURS` | `24` | Masa berlaku JWT token (jam) |
| `GUEST_SESSION_HOURS` | `24` | Masa berlaku guest session (jam) |

---

## Quick Start

```bash
cd back-end
copy .env.example .env     # lalu isi WEATHERAPI_KEY dan DATABASE_URL
pip install -r requirements.txt
python run.py
```

Server jalan di `http://localhost:5000`. Buka di browser untuk melihat dashboard status + API docs interaktif.

---

*SkinSense AI — Capstone Pijak × IBM SkillsBuild — PJK-GM066*
