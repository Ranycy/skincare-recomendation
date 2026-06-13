<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-2">
      <span class="badge">{{ t('savedProducts.badge') }}</span>
      <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">{{ t('savedProducts.title') }}</h1>
      <p class="max-w-2xl text-sm leading-6 text-gray-600">
        {{ t('savedProducts.description') }}
      </p>
    </header>

    <div v-if="favorites.isLoading" class="soft-card p-8 text-center text-sm font-semibold text-gray-500">
      {{ t('savedProducts.loading') }}
    </div>

    <div v-else-if="favorites.favorites.length === 0" class="soft-card p-8 text-center">
      <p class="font-bold text-p-d">{{ t('savedProducts.emptyTitle') }}</p>
      <p class="mt-2 text-sm leading-6 text-gray-500">{{ t('savedProducts.emptyDescription') }}</p>
      <RouterLink :to="locale.path('/dashboard')" class="btn-primary mt-5">{{ t('savedProducts.openDashboard') }}</RouterLink>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <article v-for="favorite in favorites.favorites" :key="favorite.id" class="card p-5">
        <div class="mb-5 flex items-start justify-between gap-3">
          <span class="badge">{{ displayCategory(favorite.category, locale.locale) }}</span>
          <span class="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary-dark">
            {{ Math.round((favorite.score || 0) * 100) }}%
          </span>
        </div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-primary/70">{{ favorite.brand }}</p>
        <h2 class="mt-2 min-h-14 text-lg font-bold leading-snug text-gray-950">{{ favorite.product_name }}</h2>
        <p class="mt-4 text-xs font-semibold text-gray-400">{{ t('savedProducts.savedAt', { date: formatDate(favorite.created_at) }) }}</p>
        <button class="btn-secondary mt-5 w-full" @click="removeFavorite(favorite)">
          {{ t('common.remove') }}
        </button>
      </article>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useFavoritesStore } from "../stores/useFavoritesStore";
import { useLocaleStore } from "../stores/useLocaleStore";
import { notifyError, notifySuccess } from "../utils/notifications";
import { displayCategory } from "../utils/analysisMapping";

const favorites = useFavoritesStore();
const locale = useLocaleStore();
const { t } = useI18n();

function formatDate(value) {
  return new Intl.DateTimeFormat(locale.locale === "id" ? "id-ID" : "en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

async function removeFavorite(favorite) {
  try {
    await favorites.removeProduct(favorite);
    notifySuccess(t("savedProducts.removedTitle"), t("savedProducts.removedDescription"));
  } catch (error) {
    notifyError(t("savedProducts.removeFailedTitle"), error.message);
  }
}

onMounted(async () => {
  try {
    await favorites.loadFavorites();
  } catch (error) {
    notifyError(t("savedProducts.loadFailedTitle"), error.message);
  }
});
</script>
