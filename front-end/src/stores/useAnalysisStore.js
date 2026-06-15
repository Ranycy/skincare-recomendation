import { defineStore } from "pinia";
import { computed, reactive, ref } from "vue";
import { createGuestSession, getSkinProfile, requestAuthenticatedRecommendation, requestRecommendation, updateSkinProfile } from "../services/api";
import { getCurrentLocation } from "../services/geolocation";
import { deriveCondition, displayCategory, displaySkinType, mapBackendProfileToForm, normalizeAnalysisForm } from "../utils/analysisMapping";
import { translate } from "../i18n/index.js";
import { useAuthStore } from "./useAuthStore";
import { useLocaleStore } from "./useLocaleStore";

const GUEST_SESSION_KEY = "skinsense_guest_session";
const ANALYSIS_RESULT_KEY = "skinsense_analysis_result";

function createEmptyUserProfile() {
  return {
    skinType: "",
    concerns: [],
    productCategory: "",
    activity: "Indoor",
    avoidIngredients: [],
    customAvoidIngredients: "",
    isSet: false,
  };
}

function readJsonStorage(key) {
  try {
    return JSON.parse(localStorage.getItem(key));
  } catch (error) {
    localStorage.removeItem(key);
    return null;
  }
}

function readStoredGuestSession() {
  const storedSession = readJsonStorage(GUEST_SESSION_KEY);

  if (!storedSession?.user_id || !storedSession?.session_token || !storedSession?.expires_at) {
    return null;
  }

  if (new Date(storedSession.expires_at).getTime() <= Date.now()) {
    localStorage.removeItem(GUEST_SESSION_KEY);
    return null;
  }

  return storedSession;
}

function storeGuestSession(session) {
  localStorage.setItem(GUEST_SESSION_KEY, JSON.stringify(session));
}

function readStoredAnalysisResult() {
  const storedResult = readJsonStorage(ANALYSIS_RESULT_KEY);

  if (!storedResult?.userProfile?.isSet || !storedResult?.weatherData || !Array.isArray(storedResult?.recommendations)) {
    localStorage.removeItem(ANALYSIS_RESULT_KEY);
    return null;
  }

  return storedResult;
}

function normalizeWeather(weather = {}) {
  return {
    location: weather.location_name || (translate("weather.locationDetected")),
    temperature: weather.temperature,
    humidity: weather.humidity,
    uvIndex: weather.uv_index,
    pm25: weather.pm25,
    condition: deriveCondition(weather),
  };
}

function normalizeRecommendations(recommendations = [], locale = "en") {
  return recommendations.map((product) => ({
    id: product.rank,
    rank: product.rank,
    name: product.product_name,
    brand: product.brand,
    type: product.category,
    displayType: displayCategory(product.category, locale),
    displaySkin: (product.skin_types || []).map((skin) => displaySkinType(skin, locale)),
    skin: product.skin_types || [],
    ingredients: product.active_ingredients || [],
    whyRecommended: product.why_recommended,
    explanationFactors: product.explanation_factors || null,
    summaryPoints: product.explanation_factors?.summary_points || [],
    score: product.score,
    matchScore: Math.round((product.score || 0) * 100),
  }));
}

export const useAnalysisStore = defineStore("profile", () => {
  const storedAnalysisResult = readStoredAnalysisResult();
  const userProfile = reactive({
    skinType: storedAnalysisResult?.userProfile?.skinType || "",
    concerns: storedAnalysisResult?.userProfile?.concerns || [],
    productCategory: storedAnalysisResult?.userProfile?.productCategory || "",
    activity: storedAnalysisResult?.userProfile?.activity || "Indoor",
    avoidIngredients: storedAnalysisResult?.userProfile?.avoidIngredients || [],
    customAvoidIngredients: storedAnalysisResult?.userProfile?.customAvoidIngredients || "",
    isSet: Boolean(storedAnalysisResult?.userProfile?.isSet),
  });

  const guestSession = ref(readStoredGuestSession());
  const location = ref(storedAnalysisResult?.location || null);
  const weatherData = ref(storedAnalysisResult?.weatherData || null);
  const recommendations = ref(storedAnalysisResult?.recommendations || []);
  const questionnaireId = ref(storedAnalysisResult?.questionnaireId || "");
  const weatherInsights = ref(storedAnalysisResult?.weatherInsights || []);
  const routineSummary = ref(storedAnalysisResult?.routineSummary || null);
  const savedSkinProfile = ref(null);
  const isLoading = ref(false);
  const error = ref("");
  const hasResult = ref(Boolean(storedAnalysisResult?.hasResult));
  const lastSubmittedForm = ref(storedAnalysisResult?.lastSubmittedForm || null);

  const skinAlert = computed(() => {
    if (!weatherData.value) {
      return "";
    }

    if (weatherData.value.uvIndex >= 7) {
      return translate("alert.highUv");
    }

    if (weatherData.value.humidity > 70) {
      return translate("alert.humid");
    }

    if (weatherData.value.humidity < 30) {
      return translate("alert.dry");
    }

    return translate("alert.stable");
  });

  async function getOrCreateGuestSession() {
    const storedSession = readStoredGuestSession();

    if (storedSession) {
      guestSession.value = storedSession;
      return storedSession;
    }

    const newSession = await createGuestSession();
    storeGuestSession(newSession);
    guestSession.value = newSession;
    return newSession;
  }

  function saveDisplayProfile(profile) {
    userProfile.skinType = profile.skinType;
    userProfile.concerns = [...(profile.concerns || [])];
    userProfile.productCategory = profile.productCategory;
    userProfile.activity = profile.activity;
    userProfile.avoidIngredients = [...(profile.avoidIngredients || [])];
    userProfile.customAvoidIngredients = profile.customAvoidIngredients;
    userProfile.isSet = profile.isSet;
  }

  function persistAnalysisResult() {
    localStorage.setItem(
      ANALYSIS_RESULT_KEY,
      JSON.stringify({
        userProfile: {
          skinType: userProfile.skinType,
          concerns: userProfile.concerns,
          productCategory: userProfile.productCategory,
          activity: userProfile.activity,
          avoidIngredients: userProfile.avoidIngredients,
          customAvoidIngredients: userProfile.customAvoidIngredients,
          isSet: userProfile.isSet,
        },
        location: location.value,
        weatherData: weatherData.value,
        recommendations: recommendations.value,
        questionnaireId: questionnaireId.value,
        weatherInsights: weatherInsights.value,
        routineSummary: routineSummary.value,
        hasResult: hasResult.value,
        lastSubmittedForm: lastSubmittedForm.value,
      }),
    );
  }

  async function submitAnalysis(form) {
    error.value = "";
    isLoading.value = true;

    try {
      const auth = useAuthStore();
      const locale = useLocaleStore();
      const normalized = normalizeAnalysisForm(form);
      const currentLocation = await getCurrentLocation();
      const payload = {
        locale: locale.locale,
        questionnaire: normalized.questionnaire,
        location: currentLocation,
      };

      let result;
      if (auth.isAuthenticated) {
        result = await requestAuthenticatedRecommendation(payload, auth.token);
      } else {
        const session = await getOrCreateGuestSession();
        result = await requestRecommendation({
          ...payload,
          user_id: session.user_id,
          session_token: session.session_token,
        });
      }

      saveDisplayProfile(normalized.displayProfile);
      location.value = currentLocation;
      weatherData.value = normalizeWeather(result.weather);
      recommendations.value = normalizeRecommendations(result.recommendations, locale.locale);
      questionnaireId.value = result.questionnaire_id || "";
      weatherInsights.value = result.weather_insights || [];
      routineSummary.value = result.routine_summary || null;
      hasResult.value = true;
      lastSubmittedForm.value = {
        ...form,
        concerns: [...(form.concerns || [])],
        avoidIngredients: [...(form.avoidIngredients || [])],
      };
      persistAnalysisResult();

      return result;
    } catch (submitError) {
      error.value = submitError.message || translate("apiErrors.generic");
      if (!hasResult.value) {
        recommendations.value = [];
      }
      throw submitError;
    } finally {
      isLoading.value = false;
    }
  }

  async function refreshAnalysis() {
    if (!lastSubmittedForm.value) {
      error.value = translate("analysis.failedTitle");
      return null;
    }

    return submitAnalysis(lastSubmittedForm.value);
  }

  async function loadSavedSkinProfile() {
    const auth = useAuthStore();
    if (!auth.isAuthenticated) {
      savedSkinProfile.value = null;
      return null;
    }

    const result = await getSkinProfile(auth.token);
    savedSkinProfile.value = result.profile;
    return mapBackendProfileToForm(result.profile, useLocaleStore().locale);
  }

  async function saveSkinProfile(form) {
    const auth = useAuthStore();
    if (!auth.isAuthenticated) {
      return null;
    }

    const normalized = normalizeAnalysisForm(form);
    const result = await updateSkinProfile({
      skin_type: normalized.questionnaire.skin_type,
      skin_concerns: normalized.questionnaire.skin_concerns,
      avoided_ingredients: normalized.questionnaire.avoided_ingredients,
      default_product_category: normalized.questionnaire.product_category,
      default_activity_type: normalized.questionnaire.activity_type || "indoor",
    }, auth.token);

    savedSkinProfile.value = result.profile;
    return result.profile;
  }

  function clearAnalysisResult({ keepGuestSession = true } = {}) {
    Object.assign(userProfile, createEmptyUserProfile());
    location.value = null;
    weatherData.value = null;
    recommendations.value = [];
    questionnaireId.value = "";
    weatherInsights.value = [];
    routineSummary.value = null;
    savedSkinProfile.value = null;
    error.value = "";
    hasResult.value = false;
    lastSubmittedForm.value = null;
    localStorage.removeItem(ANALYSIS_RESULT_KEY);

    if (!keepGuestSession) {
      guestSession.value = null;
      localStorage.removeItem(GUEST_SESSION_KEY);
    }
  }

  return {
    userProfile,
    guestSession,
    location,
    weatherData,
    recommendations,
    questionnaireId,
    weatherInsights,
    routineSummary,
    savedSkinProfile,
    isLoading,
    error,
    hasResult,
    skinAlert,
    submitAnalysis,
    refreshAnalysis,
    loadSavedSkinProfile,
    saveSkinProfile,
    clearAnalysisResult,
  };
});
