const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

const API_ERROR_MESSAGES = {
  "Email and password are required": "Email dan password wajib diisi.",
  "Name, email, and password are required": "Nama, email, dan password wajib diisi.",
  "Password must be at least 6 characters": "Password minimal 6 karakter.",
  "Email already registered": "Email sudah terdaftar.",
  "Invalid email or password": "Email atau password tidak valid.",
  "Authorization header required": "Sesi login tidak ditemukan. Silakan login ulang.",
  "Invalid or expired token": "Sesi login sudah kedaluwarsa. Silakan login ulang.",
  "User not found": "Akun tidak ditemukan.",
  "Request body is required": "Data request wajib diisi.",
  "Invalid or expired guest session": "Sesi guest sudah kedaluwarsa. Coba ulangi analisis.",
  "History item not found": "Riwayat rekomendasi tidak ditemukan.",
  "Favorite product not found": "Produk tersimpan tidak ditemukan.",
  "product_name is required": "Nama produk wajib diisi.",
};

function translateApiError(message) {
  if (!message) return "";
  if (API_ERROR_MESSAGES[message]) return API_ERROR_MESSAGES[message];
  if (message.startsWith("Invalid product_category")) return "Kategori produk tidak valid.";
  if (message.startsWith("Invalid default_product_category")) return "Kategori produk utama tidak valid.";
  if (message.startsWith("Invalid skin_type")) return "Jenis kulit tidak valid.";
  if (message.startsWith("Missing required fields")) return "Data rekomendasi belum lengkap.";
  if (message.startsWith("Location lat and lon are required")) return "Lokasi GPS belum lengkap.";
  return message;
}

async function request(path, options = {}) {
  const { authToken, ...fetchOptions } = options;
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        ...(fetchOptions.headers || {}),
      },
      ...fetchOptions,
    });
  } catch (error) {
    throw new Error("Gagal terhubung ke server rekomendasi. Pastikan backend sedang berjalan.");
  }

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error(translateApiError(data?.error) || "Terjadi kesalahan saat memproses request.");
  }

  return data;
}

export function createGuestSession() {
  return request("/api/auth/guest", {
    method: "POST",
  });
}

export function requestRecommendation(payload) {
  return request("/api/recommend", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function requestAuthenticatedRecommendation(payload, token) {
  return request("/api/recommend", {
    method: "POST",
    authToken: token,
    body: JSON.stringify(payload),
  });
}

export function registerUser(payload) {
  return request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginUser(payload) {
  return request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getCurrentUser(token) {
  return request("/api/auth/me", {
    method: "GET",
    authToken: token,
  });
}

export function getSkinProfile(token) {
  return request("/api/profile/skin", {
    method: "GET",
    authToken: token,
  });
}

export function updateSkinProfile(payload, token) {
  return request("/api/profile/skin", {
    method: "PUT",
    authToken: token,
    body: JSON.stringify(payload),
  });
}

export function getHistory(token, { page = 1, limit = 10 } = {}) {
  return request(`/api/history?page=${page}&limit=${limit}`, {
    method: "GET",
    authToken: token,
  });
}

export function getHistoryDetail(id, token) {
  return request(`/api/history/${id}`, {
    method: "GET",
    authToken: token,
  });
}

export function deleteHistory(id, token) {
  return request(`/api/history/${id}`, {
    method: "DELETE",
    authToken: token,
  });
}

export function getFavorites(token) {
  return request("/api/favorites", {
    method: "GET",
    authToken: token,
  });
}

export function addFavorite(payload, token) {
  return request("/api/favorites", {
    method: "POST",
    authToken: token,
    body: JSON.stringify(payload),
  });
}

export function deleteFavorite(id, token) {
  return request(`/api/favorites/${id}`, {
    method: "DELETE",
    authToken: token,
  });
}
