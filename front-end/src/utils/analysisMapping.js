import { translate } from "../i18n/index.js";
import { normalizeLocale } from "./locale.js";

const skinTypeMap = {
  Normal: "normal",
  Kering: "dry",
  Dry: "dry",
  Berminyak: "oily",
  Oily: "oily",
  Kombinasi: "combination",
  Combination: "combination",
  Sensitif: "sensitive",
  Sensitive: "sensitive",
};

const concernMap = {
  Jerawat: "acne",
  Acne: "acne",
  Kusam: "dullness",
  Dullness: "dullness",
  Penuaan: "aging",
  Aging: "aging",
  "Bekas jerawat": "dark spots",
  "Dark spots": "dark spots",
  Dehidrasi: "dehydration",
  Dehydration: "dehydration",
};

const categoryMap = {
  Cleanser: "cleanser",
  Pembersih: "cleanser",
  Moisturizer: "moisturizer",
  Pelembap: "moisturizer",
  Masker: "face mask",
  "Face mask": "face mask",
  "Masker wajah": "face mask",
  "Eye cream": "eye cream",
  "Krim mata": "eye cream",
  Sunscreen: "sunscreen",
  "Tabir surya": "sunscreen",
};

const activityMap = {
  Indoor: "indoor",
  Outdoor: "outdoor",
  "Dalam ruangan": "indoor",
  "Luar ruangan": "outdoor",
};

const avoidIngredientMap = {
  Alkohol: "alcohol",
  Alcohol: "alcohol",
  Fragrance: "fragrance",
  Paraben: "paraben",
  Silikon: "silicone",
  Silicone: "silicone",
  Sulfat: "sulfate",
  Sulfate: "sulfate",
};

const displayMaps = {
  en: {
    skinType: {
      normal: "Normal",
      dry: "Dry",
      oily: "Oily",
      combination: "Combination",
      sensitive: "Sensitive",
    },
    concern: {
      acne: "Acne",
      dullness: "Dullness",
      aging: "Aging",
      "dark spots": "Dark spots",
      dehydration: "Dehydration",
    },
    category: {
      cleanser: "Cleanser",
      moisturizer: "Moisturizer",
      "face mask": "Face mask",
      "eye cream": "Eye cream",
      sunscreen: "Sunscreen",
    },
    avoidIngredient: {
      alcohol: "Alcohol",
      fragrance: "Fragrance",
      paraben: "Paraben",
      silicone: "Silicone",
      sulfate: "Sulfate",
    },
    routineTime: {
      Morning: "Morning",
      Midday: "Midday",
      Evening: "Evening",
      Weekly: "Weekly",
    },
  },
  id: {
    skinType: {
      normal: "Normal",
      dry: "Kering",
      oily: "Berminyak",
      combination: "Kombinasi",
      sensitive: "Sensitif",
    },
    concern: {
      acne: "Jerawat",
      dullness: "Kusam",
      aging: "Penuaan",
      "dark spots": "Bekas jerawat",
      dehydration: "Dehidrasi",
    },
    category: {
      cleanser: "Pembersih",
      moisturizer: "Pelembap",
      "face mask": "Masker wajah",
      "eye cream": "Krim mata",
      sunscreen: "Tabir surya",
    },
    avoidIngredient: {
      alcohol: "Alkohol",
      fragrance: "Fragrance",
      paraben: "Paraben",
      silicone: "Silikon",
      sulfate: "Sulfat",
    },
    routineTime: {
      Morning: "Pagi",
      Midday: "Siang",
      Evening: "Malam",
      Weekly: "Mingguan",
    },
  },
};

function normalizeCustomIngredients(value = "") {
  return value
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter(Boolean);
}

function lookupDisplay(group, value = "", locale = "en") {
  const selectedLocale = normalizeLocale(locale);
  return displayMaps[selectedLocale]?.[group]?.[value?.toLowerCase?.() || value] || value || "-";
}

export function getAnalysisOptions(locale = "en") {
  const selectedLocale = normalizeLocale(locale);
  const labels = displayMaps[selectedLocale];

  return {
    skinTypes: ["normal", "dry", "oily", "combination", "sensitive"].map((value) => labels.skinType[value]),
    concerns: ["acne", "dullness", "aging", "dark spots", "dehydration"].map((value) => labels.concern[value]),
    productCategories: ["cleanser", "moisturizer", "face mask", "eye cream", "sunscreen"].map((value) => labels.category[value]),
    avoidOptions: ["alcohol", "fragrance", "paraben", "silicone", "sulfate"].map((value) => labels.avoidIngredient[value]),
    activities: selectedLocale === "id" ? ["Dalam ruangan", "Luar ruangan"] : ["Indoor", "Outdoor"],
  };
}

export function isSunscreenCategory(value = "") {
  return categoryMap[value] === "sunscreen";
}

export function normalizeAnalysisForm(form) {
  const productCategory = categoryMap[form.productCategory] || form.productCategory;
  const skinType = skinTypeMap[form.skinType] || form.skinType;
  const activityType = activityMap[form.activity] || "indoor";
  const selectedAvoidIngredients = (form.avoidIngredients || [])
    .map((ingredient) => avoidIngredientMap[ingredient] || ingredient)
    .filter(Boolean);
  const customAvoidIngredients = normalizeCustomIngredients(form.customAvoidIngredients);

  if (!productCategory || !Object.values(categoryMap).includes(productCategory)) {
    throw new Error(translate("validation.chooseProduct"));
  }

  if (!skinType || !Object.values(skinTypeMap).includes(skinType)) {
    throw new Error(translate("validation.chooseSkinType"));
  }

  return {
    displayProfile: {
      skinType: form.skinType,
      concerns: [...(form.concerns || [])],
      productCategory: form.productCategory,
      activity: form.activity,
      avoidIngredients: [...(form.avoidIngredients || [])],
      customAvoidIngredients: form.customAvoidIngredients || "",
      isSet: true,
    },
    questionnaire: {
      product_category: productCategory,
      skin_type: skinType,
      skin_concerns: (form.concerns || []).map((concern) => concernMap[concern] || concern).filter(Boolean),
      activity_type: productCategory === "sunscreen" ? activityType : undefined,
      avoided_ingredients: [...new Set([...selectedAvoidIngredients, ...customAvoidIngredients])],
    },
  };
}

export function mapBackendProfileToForm(profile, locale = "en") {
  if (!profile) {
    return null;
  }

  const avoidedLabels = [];
  const customAvoided = [];

  for (const ingredient of profile.avoided_ingredients || []) {
    const label = displayMaps[normalizeLocale(locale)].avoidIngredient[ingredient];
    if (label) {
      avoidedLabels.push(label);
    } else {
      customAvoided.push(ingredient);
    }
  }

  return {
    skinType: displaySkinType(profile.skin_type, locale),
    concerns: (profile.skin_concerns || []).map((concern) => displayConcern(concern, locale)).filter(Boolean),
    productCategory: displayCategory(profile.default_product_category, locale),
    activity: normalizeLocale(locale) === "id"
      ? (profile.default_activity_type === "outdoor" ? "Luar ruangan" : "Dalam ruangan")
      : (profile.default_activity_type === "outdoor" ? "Outdoor" : "Indoor"),
    avoidIngredients: avoidedLabels,
    customAvoidIngredients: customAvoided.join(", "),
  };
}

export function deriveCondition(weather, locale = "en") {
  if ((weather?.uv_index || weather?.uvIndex || 0) >= 7) {
    return translate("condition.highUv");
  }

  if ((weather?.humidity || 0) >= 70) {
    return translate("condition.humid");
  }

  if ((weather?.humidity || 0) < 30) {
    return translate("condition.dry");
  }

  if ((weather?.pm25 || 0) >= 35) {
    return translate("condition.pm25");
  }

  return translate("condition.stable");
}

export function displayCategory(value = "", locale = "en") {
  return lookupDisplay("category", categoryMap[value] || value, locale);
}

export function displaySkinType(value = "", locale = "en") {
  return lookupDisplay("skinType", skinTypeMap[value] || value, locale);
}

export function displayConcern(value = "", locale = "en") {
  return lookupDisplay("concern", concernMap[value] || value, locale);
}

export function displayRoutineTime(value = "", locale = "en") {
  return displayMaps[normalizeLocale(locale)].routineTime[value] || value || "-";
}
