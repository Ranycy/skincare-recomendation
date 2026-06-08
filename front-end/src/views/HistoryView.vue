<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-2">
      <span class="badge">Riwayat rekomendasi</span>
      <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">Riwayat rekomendasi</h1>
      <p class="max-w-2xl text-sm leading-6 text-gray-600">
        Lihat kembali analisis sebelumnya, kondisi cuaca saat itu, dan produk yang paling cocok.
      </p>
    </header>

    <div v-if="isLoading" class="soft-card p-8 text-center text-sm font-semibold text-gray-500">
      Memuat riwayat...
    </div>

    <div v-else-if="history.length === 0" class="soft-card p-8 text-center">
      <p class="font-bold text-p-d">Belum ada riwayat</p>
      <p class="mt-2 text-sm leading-6 text-gray-500">Kirim analisis saat login agar hasilnya tersimpan di akun kamu.</p>
      <RouterLink to="/profile" class="btn-primary mt-5">Mulai analisis</RouterLink>
    </div>

    <TransitionGroup v-else name="list" tag="div" class="grid gap-4 lg:grid-cols-2">
      <article v-for="item in history" :key="item.questionnaire_id" class="soft-card p-5">
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <p class="eyebrow">{{ formatDate(item.created_at) }}</p>
            <h2 class="mt-1 text-xl font-bold text-p-d">{{ displayCategory(item.product_category) }}</h2>
          </div>
          <span class="badge">{{ item.weather?.humidity ?? '-' }}% Humidity</span>
        </div>

        <div class="mb-4 grid grid-cols-2 gap-3 text-sm">
          <div class="rounded-2xl bg-primary/5 p-3">
            <span class="text-xs font-bold uppercase tracking-[0.12em] text-primary/70">Jenis kulit</span>
            <p class="mt-1 font-bold text-primary-dark">{{ displaySkinType(item.skin_type) }}</p>
          </div>
          <div class="rounded-2xl bg-accent-pink/50 p-3">
            <span class="text-xs font-bold uppercase tracking-[0.12em] text-s-d/80">Weather</span>
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
            <span>Lihat detail</span>
          </button>
          <button
            class="grid min-h-11 w-12 place-items-center rounded-full border border-red-100 bg-red-50 text-red-600 transition hover:bg-red-100 disabled:opacity-50"
            :disabled="deletingId === item.questionnaire_id"
            @click="openDeleteDialog(item)"
            aria-label="Hapus riwayat"
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
        <button class="absolute inset-0 cursor-default" aria-label="Batal hapus riwayat" @click="closeDeleteDialog"></button>

        <section class="relative w-full max-w-md rounded-[2rem] bg-white p-5 shadow-2xl sm:p-6">
          <button
            class="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-full bg-gray-50 text-gray-500 transition hover:bg-gray-100 hover:text-gray-900"
            aria-label="Tutup dialog"
            @click="closeDeleteDialog"
          >
            <X class="h-4 w-4" />
          </button>

          <div class="mb-5 flex items-start gap-4 pr-10">
            <span class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-red-50 text-red-600">
              <Trash2 class="h-5 w-5" />
            </span>
            <div>
              <p class="eyebrow text-red-600">Hapus riwayat</p>
              <h2 class="mt-1 text-2xl font-bold leading-tight text-p-d">Hapus rekomendasi ini?</h2>
              <p class="mt-2 text-sm leading-6 text-gray-600">
                Riwayat analisis akan dihapus dari akun kamu. Produk yang sudah tersimpan tetap aman.
              </p>
            </div>
          </div>

          <div class="rounded-3xl border border-primary/10 bg-primary/5 p-4">
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-xs font-bold uppercase tracking-[0.14em] text-primary/70">
                  {{ formatDate(deleteTarget.created_at) }}
                </p>
                <h3 class="mt-1 text-lg font-bold text-primary-dark">{{ displayCategory(deleteTarget.product_category) }}</h3>
              </div>
              <span class="badge bg-white/80">{{ deleteTarget.weather?.humidity ?? '-' }}% Humidity</span>
            </div>
            <p v-if="deleteTarget.top_recommendation" class="mt-3 text-sm font-semibold leading-6 text-gray-700">
              Match utama: {{ deleteTarget.top_recommendation.brand }} {{ deleteTarget.top_recommendation.product_name }}
            </p>
          </div>

          <div class="mt-5 grid grid-cols-2 gap-3">
            <button class="btn-secondary min-h-12" :disabled="Boolean(deletingId)" @click="closeDeleteDialog">
              Batal
            </button>
            <button
              class="inline-flex min-h-12 items-center justify-center gap-2 rounded-full bg-red-600 px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-red-700 active:scale-[0.98] disabled:opacity-60"
              :disabled="Boolean(deletingId)"
              @click="confirmDelete"
            >
              <LoaderCircle v-if="deletingId" class="h-4 w-4 animate-spin" />
              <Trash2 v-else class="h-4 w-4" />
              <span>{{ deletingId ? 'Menghapus...' : 'Hapus' }}</span>
            </button>
          </div>
        </section>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { deleteHistory, getHistory, getHistoryDetail } from "../services/api";
import { useAuthStore } from "../stores/useAuthStore";
import { useFavoritesStore } from "../stores/useFavoritesStore";
import ProductModal from "../components/ProductModal.vue";
import { notifyError, notifySuccess } from "../utils/notifications";
import { Eye, LoaderCircle, Trash2, X } from "lucide-vue-next";
import { displayCategory, displaySkinType } from "../utils/analysisMapping";

const auth = useAuthStore();
const favorites = useFavoritesStore();
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
    displayType: displayCategory(product.category),
    displaySkin: (product.skin_types || []).map((skin) => displaySkinType(skin)),
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
  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

async function loadHistory() {
  isLoading.value = true;
  try {
    const result = await getHistory(auth.token, { page: 1, limit: 20 });
    history.value = result.history || [];
  } catch (error) {
    notifyError("Riwayat gagal dimuat", error.message);
  } finally {
    isLoading.value = false;
  }
}

async function openDetail(id) {
  try {
    const result = await getHistoryDetail(id, auth.token);
    const firstProduct = result.history_item?.recommendations?.[0];
    if (firstProduct) {
      selectedProduct.value = normalizeHistoryProduct(firstProduct);
    }
  } catch (error) {
    notifyError("Detail gagal dimuat", error.message);
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
    notifySuccess("Riwayat dihapus", "Riwayat rekomendasi berhasil dihapus.");
  } catch (error) {
    notifyError("Gagal menghapus riwayat", error.message);
  } finally {
    deletingId.value = "";
  }
}

async function handleToggleSave(product) {
  try {
    if (favorites.isSaved(product)) {
      await favorites.removeProduct(product);
      notifySuccess("Produk dihapus", "Produk dihapus dari daftar tersimpan.");
    } else {
      await favorites.saveProduct(product);
      notifySuccess("Produk tersimpan", "Produk bisa dilihat di halaman produk tersimpan.");
    }
  } catch (error) {
    notifyError("Gagal menyimpan produk", error.message);
  }
}

onMounted(async () => {
  try {
    await Promise.all([loadHistory(), favorites.loadFavorites()]);
  } catch (error) {
    notifyError("Data gagal dimuat", error.message);
  }
});
</script>
