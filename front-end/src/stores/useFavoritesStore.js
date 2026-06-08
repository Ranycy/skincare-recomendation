import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { addFavorite, deleteFavorite, getFavorites } from "../services/api";
import { useAuthStore } from "./useAuthStore";

function productKey(product) {
  return `${product?.name || product?.product_name || ""}|${product?.brand || ""}|${product?.type || product?.category || ""}`.toLowerCase();
}

export const useFavoritesStore = defineStore("favorites", () => {
  const favorites = ref([]);
  const isLoading = ref(false);
  const error = ref("");

  const favoriteKeys = computed(() => new Set(favorites.value.map((favorite) => productKey({
    name: favorite.product_name,
    brand: favorite.brand,
    type: favorite.category,
  }))));

  function isSaved(product) {
    return favoriteKeys.value.has(productKey(product));
  }

  function findFavorite(product) {
    const key = productKey(product);
    return favorites.value.find((favorite) => productKey({
      name: favorite.product_name,
      brand: favorite.brand,
      type: favorite.category,
    }) === key);
  }

  async function loadFavorites() {
    const auth = useAuthStore();
    if (!auth.token) return [];

    error.value = "";
    isLoading.value = true;
    try {
      const result = await getFavorites(auth.token);
      favorites.value = result.favorites || [];
      return favorites.value;
    } catch (loadError) {
      error.value = loadError.message || "Gagal memuat produk tersimpan.";
      throw loadError;
    } finally {
      isLoading.value = false;
    }
  }

  async function saveProduct(product, questionnaireId) {
    const auth = useAuthStore();
    if (!auth.isAuthenticated) {
      throw new Error("Login diperlukan untuk menyimpan produk.");
    }

    const result = await addFavorite({
      product_name: product.name,
      brand: product.brand,
      category: product.type,
      score: product.score,
      source_questionnaire_id: questionnaireId,
    }, auth.token);

    if (!findFavorite(product)) {
      favorites.value.unshift(result.favorite);
    }

    return result.favorite;
  }

  async function removeProduct(productOrFavorite) {
    const auth = useAuthStore();
    const favorite = productOrFavorite.id && productOrFavorite.product_name
      ? productOrFavorite
      : findFavorite(productOrFavorite);

    if (!favorite) return null;

    await deleteFavorite(favorite.id, auth.token);
    favorites.value = favorites.value.filter((item) => item.id !== favorite.id);
    return favorite;
  }

  return {
    favorites,
    isLoading,
    error,
    isSaved,
    findFavorite,
    loadFavorites,
    saveProduct,
    removeProduct,
  };
});
