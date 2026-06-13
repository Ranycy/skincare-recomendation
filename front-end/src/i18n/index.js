import { createI18n } from "vue-i18n";
import en from "./messages/en.js";
import id from "./messages/id.js";
import { DEFAULT_LOCALE, getStoredLocale } from "../utils/locale.js";

export const i18n = createI18n({
  legacy: false,
  locale: getStoredLocale(),
  fallbackLocale: DEFAULT_LOCALE,
  messages: {
    en,
    id,
  },
});

export function translate(key, params) {
  return i18n.global.t(key, params);
}
