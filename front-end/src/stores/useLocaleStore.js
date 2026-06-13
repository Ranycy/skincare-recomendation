import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { i18n } from "../i18n/index.js";
import { updatePreferences } from "../services/api.js";
import {
  DEFAULT_LOCALE,
  LOCALE_STORAGE_KEY,
  getStoredLocale,
  localizedPath,
  normalizeLocale,
} from "../utils/locale.js";

export const useLocaleStore = defineStore("locale", () => {
  const locale = ref(getStoredLocale());
  const isSyncing = ref(false);
  const error = ref("");

  const isEnglish = computed(() => locale.value === DEFAULT_LOCALE);

  function applyLocale(value, { persist = true } = {}) {
    const normalized = normalizeLocale(value);
    locale.value = normalized;
    i18n.global.locale.value = normalized;

    if (persist) {
      localStorage.setItem(LOCALE_STORAGE_KEY, normalized);
    }

    return normalized;
  }

  function applyRouteLocale(routeLocale) {
    return applyLocale(routeLocale === "id" ? "id" : DEFAULT_LOCALE);
  }

  function path(pathValue = "/", targetLocale = locale.value) {
    return localizedPath(pathValue, targetLocale);
  }

  function switchRouteLocale(targetLocale, route, router) {
    const nextLocale = applyLocale(targetLocale);
    const nextPath = localizedPath(route.path, nextLocale);
    const query = route.query || {};
    const hash = route.hash || "";

    return router.push({
      path: nextPath,
      query,
      hash,
    });
  }

  async function syncPreference(token) {
    if (!token) return null;

    error.value = "";
    isSyncing.value = true;
    try {
      const result = await updatePreferences({ preferred_locale: locale.value }, token);
      return result.preferences;
    } catch (syncError) {
      error.value = syncError.message || "Language preference failed to sync.";
      throw syncError;
    } finally {
      isSyncing.value = false;
    }
  }

  return {
    locale,
    isEnglish,
    isSyncing,
    error,
    applyLocale,
    applyRouteLocale,
    path,
    switchRouteLocale,
    syncPreference,
  };
});
