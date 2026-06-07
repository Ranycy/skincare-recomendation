const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000";

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });
  } catch (error) {
    throw new Error("Gagal terhubung ke server rekomendasi. Pastikan backend sedang berjalan.");
  }

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error(data?.error || "Terjadi kesalahan saat memproses request.");
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

