export const DEFAULT_LOCALE = "en";
export const SUPPORTED_LOCALES = ["en", "id"];
export const LOCALE_STORAGE_KEY = "skinsense_locale";

export function normalizeLocale(value, fallback = DEFAULT_LOCALE) {
  const locale = String(value || "").toLowerCase();
  if (SUPPORTED_LOCALES.includes(locale)) return locale;
  return SUPPORTED_LOCALES.includes(fallback) ? fallback : DEFAULT_LOCALE;
}

export function getStoredLocale() {
  return normalizeLocale(localStorage.getItem(LOCALE_STORAGE_KEY));
}

export function localeFromRouteParam(value) {
  return value === "id" ? "id" : DEFAULT_LOCALE;
}

export function stripLocalePrefix(path = "/") {
  if (path === "/id") return "/";
  if (path.startsWith("/id/")) return path.slice(3) || "/";
  return path || "/";
}

export function localizedPath(path = "/", locale = getStoredLocale()) {
  const normalizedLocale = normalizeLocale(locale);
  const cleanPath = stripLocalePrefix(path);

  if (normalizedLocale === "id") {
    return cleanPath === "/" ? "/id" : `/id${cleanPath}`;
  }

  return cleanPath;
}

export function localizedRouteParams(locale = getStoredLocale()) {
  return normalizeLocale(locale) === "id" ? { locale: "id" } : {};
}
