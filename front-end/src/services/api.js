import { translate } from "../i18n/index.js";
import { getStoredLocale, normalizeLocale } from "../utils/locale.js";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

function translateApiError(message) {
  if (!message) return "";
  const directKey = `apiErrors.${message}`;
  const translated = translate(directKey);
  if (translated !== directKey) return translated;
  if (message.startsWith("Invalid product_category")) return translate("apiErrors.invalidCategory");
  if (message.startsWith("Invalid default_product_category")) return translate("apiErrors.invalidDefaultCategory");
  if (message.startsWith("Invalid skin_type")) return translate("apiErrors.invalidSkinType");
  if (message.startsWith("Missing required fields")) return translate("apiErrors.missingFields");
  if (message.startsWith("Location lat and lon are required")) return translate("apiErrors.locationRequired");
  if (message.startsWith("Location (lat, lon) is required")) return translate("apiErrors.locationRequired");
  return message;
}

function withLocaleQuery(path, locale = getStoredLocale()) {
  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}locale=${encodeURIComponent(normalizeLocale(locale))}`;
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
    throw new Error(translate("apiErrors.connectFailed"));
  }

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error(translateApiError(data?.error) || translate("apiErrors.generic"));
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

export function getPreferences(token) {
  return request("/api/profile/preferences", {
    method: "GET",
    authToken: token,
  });
}

export function updatePreferences(payload, token) {
  return request("/api/profile/preferences", {
    method: "PUT",
    authToken: token,
    body: JSON.stringify(payload),
  });
}

export function getHistory(token, { page = 1, limit = 10, locale = getStoredLocale() } = {}) {
  return request(withLocaleQuery(`/api/history?page=${page}&limit=${limit}`, locale), {
    method: "GET",
    authToken: token,
  });
}

export function getHistoryDetail(id, token, locale = getStoredLocale()) {
  return request(withLocaleQuery(`/api/history/${id}`, locale), {
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
