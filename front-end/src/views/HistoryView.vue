<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-2">
      <span class="badge">{{ t('history.badge') }}</span>
      <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">{{ t('history.title') }}</h1>
      <p class="max-w-2xl text-sm leading-6 text-gray-600">
        {{ t('history.description') }}
      </p>
    </header>

    <div v-if="isLoading" class="soft-card p-8 text-center text-sm font-semibold text-gray-500">
      {{ t('history.loading') }}
    </div>

    <div v-else-if="history.length === 0" class="soft-card p-8 text-center">
      <p class="font-bold text-p-d">{{ t('history.emptyTitle') }}</p>
      <p class="mt-2 text-sm leading-6 text-gray-500">{{ t('history.emptyDescription') }}</p>
      <RouterLink :to="locale.path('/profile')" class="btn-primary mt-5">{{ t('history.start') }}</RouterLink>
    </div>

    <TransitionGroup v-else name="list" tag="div" class="grid gap-4 lg:grid-cols-2">
      <article v-for="item in history" :key="item.questionnaire_id" class="soft-card p-5">
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <p class="eyebrow">{{ formatDate(item.created_at) }}</p>
            <h2 class="mt-1 text-xl font-bold text-p-d">{{ displayCategory(item.product_category) }}</h2>
          </div>
          <span class="badge">{{ item.weather?.humidity ?? '-' }}% {{ t('history.humidity') }}</span>
        </div>

        <div class="mb-4 grid grid-cols-2 gap-3 text-sm">
          <div class="rounded-2xl bg-primary/5 p-3">
            <span class="text-xs font-bold uppercase tracking-[0.12em] text-primary/70">{{ t('history.skinType') }}</span>
            <p class="mt-1 font-bold text-primary-dark">{{ displaySkinType(item.skin_type, locale.locale) }}</p>
          </div>
          <div class="rounded-2xl bg-accent-pink/50 p-3">
            <span class="text-xs font-bold uppercase tracking-[0.12em] text-s-d/80">{{ t('history.weather') }}</span>
            <p class="mt-1 font-bold text-s-d">{{ item.weather?.temperature ?? '-' }}&deg;C</p>
          </div>
        </div>

        <div v-if="item.top_recommendation" class="rounded-2xl border border-primary/10 bg-white p-4">
          <p class="text-xs font-bold uppercase tracking-[0.14em] text-gray-400">{{ item.top_recommendation.brand }}</p>
          <h3 class="mt-1 font-bold leading-snug text-gray-950">{{ item.top_recommendation.product_name }}</h3>
          <p class="mt-2 text-xs font-semibold text-primary-dark">{{ Math.round((item.top_recommendation.score || 0) * 100) }}% match</p>
        </div>

        <div class="mt-4 grid grid-cols-[1fr_auto] gap-2">
          <button class="btn-secondary min-h-11" @click="openDetail(item.questionnaire_id)">
            <Eye class="h-4 w-4" />
            <span>{{ t('common.viewDetails') }}</span>
          </button>
          <button
            class="grid min-h-11 w-12 place-items-center rounded-full border border-red-100 bg-red-50 text-red-600 transition hover:bg-red-100 disabled:opacity-50"
            :disabled="deletingId === item.questionnaire_id"
            @click="openDeleteDialog(item)"
            :aria-label="t('history.deleteAria')"
          >
            <LoaderCircle v-if="deletingId === item.questionnaire_id" class="h-4 w-4 animate-spin" />
            <Trash2 v-else class="h-4 w-4" />
          </button>
        </div>
      </article>
    </TransitionGroup>

    <ProductModal
      v-if="selectedProduct"
      :product="selectedProduct"
      :is-open="Boolean(selectedProduct)"
      :is-saved="favorites.isSaved(selectedProduct)"
      @close="selectedProduct = null"
      @toggle-save="handleToggleSave"
    />

    <Transition name="modal-pop">
      <div
        v-if="deleteTarget"
        class="fixed inset-0 z-[70] flex items-end justify-center bg-gray-950/45 p-4 backdrop-blur-sm sm:items-center"
      >
        <button class="absolute inset-0 cursor-default" :aria-label="t('history.cancelDeleteAria')" @click="closeDeleteDialog"></button>

        <section class="relative w-full max-w-md rounded-[2rem] bg-white p-5 shadow-2xl sm:p-6">
          <button
            class="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-full bg-gray-50 text-gray-500 transition hover:bg-gray-100 hover:text-gray-900"
            :aria-label="t('history.closeDialog')"
            @click="closeDeleteDialog"
          >
            <X class="h-4 w-4" />
          </button>

          <div class="mb-5 flex items-start gap-4 pr-10">
            <span class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-red-50 text-red-600">
              <Trash2 class="h-5 w-5" />
            </span>
            <div>
              <p class="eyebrow text-red-600">{{ t('history.deleteBadge') }}</p>
              <h2 class="mt-1 text-2xl font-bold leading-tight text-p-d">{{ t('history.deleteTitle') }}</h2>
              <p class="mt-2 text-sm leading-6 text-gray-600">
                {{ t('history.deleteDescription') }}
              </p>
            </div>
          </div>

          <div class="rounded-3xl border border-primary/10 bg-primary/5 p-4">
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-xs font-bold uppercase tracking-[0.14em] text-primary/70">
                  {{ formatDate(deleteTarget.created_at) }}
                </p>
                <h3 class="mt-1 text-lg font-bold text-primary-dark">{{ displayCategory(deleteTarget.product_category, locale.locale) }}</h3>
              </div>
              <span class="badge bg-white/80">{{ deleteTarget.weather?.humidity ?? '-' }}% {{ t('history.humidity') }}</span>
            </div>
            <p v-if="deleteTarget.top_recommendation" class="mt-3 text-sm font-semibold leading-6 text-gray-700">
              {{ t('history.mainMatch') }} {{ deleteTarget.top_recommendation.brand }} {{ deleteTarget.top_recommendation.product_name }}
            </p>
          </div>

          <div class="mt-5 grid grid-cols-2 gap-3">
            <button class="btn-secondary min-h-12" :disabled="Boolean(deletingId)" @click="closeDeleteDialog">
              {{ t('common.cancel') }}
            </button>
            <button
              class="inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-red-600 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-red-700 active:scale-[0.98] disabled:opacity-60"
              :disabled="Boolean(deletingId)"
              @click="confirmDelete"
            >
              <LoaderCircle v-if="deletingId" class="h-4 w-4 animate-spin" />
              <Trash2 v-else class="h-4 w-4" />
              <span>{{ deletingId ? t('common.deleting') : t('common.delete') }}</span>
            </button>
          </div>
        </section>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { deleteHistory, getHistory, getHistoryDetail } from "../services/api";
import { useAuthStore } from "../stores/useAuthStore";
import { useFavoritesStore } from "../stores/useFavoritesStore";
import { useLocaleStore } from "../stores/useLocaleStore";
import ProductModal from "../components/ProductModal.vue";
import { notifyError, notifySuccess } from "../utils/notifications";
import { Eye, LoaderCircle, Trash2, X } from "lucide-vue-next";
import { displayCategory, displaySkinType } from "../utils/analysisMapping";

const auth = useAuthStore();
const favorites = useFavoritesStore();
const locale = useLocaleStore();
const { t } = useI18n();
const history = ref([]);
const isLoading = ref(false);
const deletingId = ref("");
const selectedProduct = ref(null);
const deleteTarget = ref(null);

function normalizeHistoryProduct(product) {
  return {
    id: product.rank,
    rank: product.rank,
    name: product.product_name,
    brand: product.brand,
    type: product.category,
    displayType: displayCategory(product.category, locale.locale),
    displaySkin: (product.skin_types || []).map((skin) => displaySkinType(skin, locale.locale)),
    skin: product.skin_types || [],
    ingredients: product.active_ingredients || [],
    whyRecommended: product.why_recommended,
    explanationFactors: product.explanation_factors || null,
    summaryPoints: product.explanation_factors?.summary_points || [],
    score: product.score,
    matchScore: Math.round((product.score || 0) * 100),
  };
}

function formatDate(value) {
  return new Intl.DateTimeFormat(locale.locale === "id" ? "id-ID" : "en-US", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

async function loadHistory() {
  isLoading.value = true;
  try {
    const result = await getHistory(auth.token, { page: 1, limit: 20, locale: locale.locale });
    history.value = result.history || [];
  } catch (error) {
    notifyError(t("history.loadFailedTitle"), error.message);
  } finally {
    isLoading.value = false;
  }
}

async function openDetail(id) {
  try {
    const result = await getHistoryDetail(id, auth.token, locale.locale);
    const firstProduct = result.history_item?.recommendations?.[0];
    if (firstProduct) {
      selectedProduct.value = normalizeHistoryProduct(firstProduct);
    }
  } catch (error) {
    notifyError(t("history.detailFailedTitle"), error.message);
  }
}

function openDeleteDialog(item) {
  deleteTarget.value = item;
}

function closeDeleteDialog() {
  if (deletingId.value) return;
  deleteTarget.value = null;
}

async function confirmDelete() {
  if (!deleteTarget.value) return;

  const targetId = deleteTarget.value.questionnaire_id;
  deletingId.value = targetId;
  try {
    await deleteHistory(targetId, auth.token);
    history.value = history.value.filter((item) => item.questionnaire_id !== targetId);
    deleteTarget.value = null;
    notifySuccess(t("history.deletedTitle"), t("history.deletedDescription"));
  } catch (error) {
    notifyError(t("history.deleteFailedTitle"), error.message);
  } finally {
    deletingId.value = "";
  }
}

async function handleToggleSave(product) {
  try {
    if (favorites.isSaved(product)) {
      await favorites.removeProduct(product);
      notifySuccess(t("notifications.productRemovedTitle"), t("notifications.productRemovedDescription"));
    } else {
      await favorites.saveProduct(product);
      notifySuccess(t("notifications.productSavedTitle"), t("notifications.productSavedDescription"));
    }
  } catch (error) {
    notifyError(t("notifications.productSaveFailedTitle"), error.message);
  }
}

onMounted(async () => {
  try {
    await Promise.all([loadHistory(), favorites.loadFavorites()]);
  } catch (error) {
    notifyError(t("history.dataFailedTitle"), error.message);
  }
});

watch(
  () => locale.locale,
  () => {
    loadHistory();
    selectedProduct.value = null;
  },
);
</script>
