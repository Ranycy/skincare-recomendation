const skinTypeMap = {
  Normal: "normal",
  Kering: "dry",
  Berminyak: "oily",
  Kombinasi: "combination",
  Sensitif: "sensitive",
};

const concernMap = {
  Jerawat: "acne",
  Kusam: "dullness",
  Penuaan: "aging",
  "Bekas jerawat": "dark spots",
  Dehidrasi: "dehydration",
};

const categoryMap = {
  Cleanser: "cleanser",
  Moisturizer: "moisturizer",
  Masker: "face mask",
  "Eye cream": "eye cream",
  Sunscreen: "sunscreen",
};

const activityMap = {
  Indoor: "indoor",
  Outdoor: "outdoor",
};

const avoidIngredientMap = {
  Alkohol: "alcohol",
  Fragrance: "fragrance",
  Paraben: "paraben",
  Silikon: "silicone",
  Sulfat: "sulfate",
};

const reverseSkinTypeMap = Object.fromEntries(Object.entries(skinTypeMap).map(([label, value]) => [value, label]));
const reverseCategoryMap = Object.fromEntries(Object.entries(categoryMap).map(([label, value]) => [value, label]));
const reverseActivityMap = Object.fromEntries(Object.entries(activityMap).map(([label, value]) => [value, label]));
const reverseConcernMap = Object.fromEntries(Object.entries(concernMap).map(([label, value]) => [value, label]));
const reverseAvoidIngredientMap = Object.fromEntries(Object.entries(avoidIngredientMap).map(([label, value]) => [value, label]));

const displayCategoryMap = {
  cleanser: "Cleanser",
  moisturizer: "Moisturizer",
  "face mask": "Face mask",
  "eye cream": "Eye cream",
  sunscreen: "Sunscreen",
};

const displaySkinTypeMap = {
  normal: "Normal",
  dry: "Kering",
  oily: "Berminyak",
  combination: "Kombinasi",
  sensitive: "Sensitif",
};

const displayConcernMap = {
  acne: "Jerawat",
  dullness: "Kulit kusam",
  aging: "Tanda penuaan",
  "dark spots": "Bekas jerawat",
  dehydration: "Dehidrasi kulit",
};

const displayRoutineTimeMap = {
  Morning: "Pagi",
  Midday: "Siang",
  Evening: "Malam",
  Weekly: "Mingguan",
};

function normalizeCustomIngredients(value = "") {
  return value
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter(Boolean);
}

export function normalizeAnalysisForm(form) {
  const productCategory = categoryMap[form.productCategory];
  const skinType = skinTypeMap[form.skinType];
  const activityType = activityMap[form.activity] || "indoor";
  const selectedAvoidIngredients = (form.avoidIngredients || [])
    .map((ingredient) => avoidIngredientMap[ingredient])
    .filter(Boolean);
  const customAvoidIngredients = normalizeCustomIngredients(form.customAvoidIngredients);

  if (!productCategory) {
    throw new Error("Pilih satu produk yang kamu butuhkan.");
  }

  if (!skinType) {
    throw new Error("Pilih jenis kulit kamu terlebih dahulu.");
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
      skin_concerns: (form.concerns || []).map((concern) => concernMap[concern]).filter(Boolean),
      activity_type: productCategory === "sunscreen" ? activityType : undefined,
      avoided_ingredients: [...new Set([...selectedAvoidIngredients, ...customAvoidIngredients])],
    },
  };
}

export function mapBackendProfileToForm(profile) {
  if (!profile) {
    return null;
  }

  const avoidedLabels = [];
  const customAvoided = [];

  for (const ingredient of profile.avoided_ingredients || []) {
    if (reverseAvoidIngredientMap[ingredient]) {
      avoidedLabels.push(reverseAvoidIngredientMap[ingredient]);
    } else {
      customAvoided.push(ingredient);
    }
  }

  return {
    skinType: reverseSkinTypeMap[profile.skin_type] || "",
    concerns: (profile.skin_concerns || []).map((concern) => reverseConcernMap[concern]).filter(Boolean),
    productCategory: reverseCategoryMap[profile.default_product_category] || "",
    activity: reverseActivityMap[profile.default_activity_type] || "Indoor",
    avoidIngredients: avoidedLabels,
    customAvoidIngredients: customAvoided.join(", "),
  };
}

export function deriveCondition(weather) {
  if ((weather?.uv_index || weather?.uvIndex || 0) >= 7) {
    return "UV tinggi";
  }

  if ((weather?.humidity || 0) >= 70) {
    return "Kondisi lembap";
  }

  if ((weather?.humidity || 0) < 30) {
    return "Udara kering";
  }

  if ((weather?.pm25 || 0) >= 35) {
    return "PM2.5 meningkat";
  }

  return "Cuaca stabil";
}

export function displayCategory(value = "") {
  return displayCategoryMap[value?.toLowerCase?.()] || value || "-";
}

export function displaySkinType(value = "") {
  return displaySkinTypeMap[value?.toLowerCase?.()] || value || "-";
}

export function displayConcern(value = "") {
  return displayConcernMap[value?.toLowerCase?.()] || value || "-";
}

export function displayRoutineTime(value = "") {
  return displayRoutineTimeMap[value] || value || "-";
}
