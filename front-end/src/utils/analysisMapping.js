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

export function deriveCondition(weather) {
  if ((weather?.uv_index || weather?.uvIndex || 0) >= 7) {
    return "High UV";
  }

  if ((weather?.humidity || 0) >= 70) {
    return "Humid";
  }

  return "Stable";
}

