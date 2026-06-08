<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-5">
      <div class="space-y-2">
        <span class="badge">Hasil hari ini</span>
        <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">
          Dashboard rekomendasi
        </h1>
        <p class="max-w-2xl text-sm leading-6 text-gray-600 sm:text-base">
          Rekomendasi hari ini dibuat dari profil kulit, kondisi cuaca, dan preferensi kandungan yang kamu isi.
        </p>
      </div>

      <div class="grid grid-cols-2 gap-3 sm:flex sm:items-center">
        <button
          @click="handleRefresh"
          :disabled="store.isLoading"
          class="btn-secondary min-h-12"
        >
          <RefreshCcw class="h-4 w-4" :class="{ 'animate-spin': store.isLoading }" />
          <span>{{ store.isLoading ? 'Memuat ulang' : 'Refresh' }}</span>
        </button>
        <RouterLink to="/profile" class="btn-secondary min-h-12">
          <Settings class="h-4 w-4" />
          <span>Edit</span>
        </RouterLink>
      </div>
    </header>

    <div class="grid gap-6 lg:grid-cols-[minmax(20rem,0.85fr)_minmax(0,1.15fr)] lg:items-start">
      <aside class="space-y-5">
        <WeatherCard v-if="store.weatherData" :weather="store.weatherData" :alert="store.skinAlert" />

        <section v-if="store.weatherInsights.length" class="soft-card overflow-hidden">
          <button class="flex w-full cursor-pointer items-center justify-between gap-4 p-5 text-left" @click="togglePanel('weather')">
            <div>
              <p class="eyebrow">Weather insight</p>
              <h2 class="mt-1 text-lg font-bold text-p-d">{{ store.weatherInsights.length }} insight cuaca</h2>
            </div>
            <ChevronDown class="h-5 w-5 text-primary transition-transform duration-300" :class="{ 'rotate-180': openPanels.weather }" />
          </button>
          <Transition name="accordion">
            <div v-show="openPanels.weather" class="overflow-hidden">
              <div class="space-y-3 px-5 pb-5">
                <div
                  v-for="insight in store.weatherInsights"
                  :key="`${insight.type}-${insight.level}`"
                  class="rounded-2xl bg-primary/5 px-4 py-3 text-sm font-semibold leading-6 text-primary-dark"
                >
                  {{ insight.message }}
                </div>
              </div>
            </div>
          </Transition>
        </section>

        <section v-if="store.routineSummary" class="soft-card overflow-hidden">
          <button class="flex w-full cursor-pointer items-center justify-between gap-4 p-5 text-left" @click="togglePanel('routine')">
            <div>
              <p class="eyebrow">Daily routine</p>
              <h2 class="mt-1 text-lg font-bold text-p-d">Fokus rutinitas hari ini</h2>
            </div>
            <ChevronDown class="h-5 w-5 text-primary transition-transform duration-300" :class="{ 'rotate-180': openPanels.routine }" />
          </button>
          <Transition name="accordion">
            <div v-show="openPanels.routine" class="overflow-hidden">
              <div class="space-y-3 px-5 pb-5 text-sm">
                <div
                  v-for="step in routineSteps"
                  :key="step.time"
                  class="rounded-2xl bg-primary/5 p-3"
                  :class="{ 'bg-accent-pink/50': step.time === 'Morning' }"
                >
                  <span class="font-bold" :class="step.time === 'Morning' ? 'text-s-d' : 'text-primary-dark'">{{ displayRoutineTime(step.time) }}</span>
                  <p class="mt-1 leading-6 text-gray-700">{{ step.message }}</p>
                </div>
                <div v-if="store.routineSummary.ingredient_focus?.length" class="rounded-2xl border border-primary/10 bg-white p-3">
                  <span class="font-bold text-primary-dark">Fokus ingredient</span>
                  <div class="mt-2 flex flex-wrap gap-2">
                    <span
                      v-for="ingredient in store.routineSummary.ingredient_focus"
                      :key="ingredient"
                      class="rounded-full bg-primary/5 px-3 py-1 text-xs font-bold text-primary-dark"
                    >
                      {{ ingredient }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </section>

        <section class="soft-card overflow-hidden">
          <button class="flex w-full cursor-pointer items-center justify-between gap-4 p-5 text-left" @click="togglePanel('profile')">
            <div>
              <p class="eyebrow">Kesesuaian profil</p>
              <h2 class="mt-1 text-lg font-bold text-p-d">Kondisi pilihanmu</h2>
            </div>
            <div class="flex items-center gap-2">
              <span class="badge">{{ store.recommendations.length }} match</span>
              <ChevronDown class="h-5 w-5 text-primary transition-transform duration-300" :class="{ 'rotate-180': openPanels.profile }" />
            </div>
          </button>

          <Transition name="accordion">
            <div v-show="openPanels.profile" class="overflow-hidden">
              <div class="space-y-4 px-5 pb-5 text-sm">
                <div class="flex items-center justify-between gap-4">
                  <span class="text-gray-500">Jenis kulit</span>
                  <strong class="text-right text-primary-dark">{{ store.userProfile.skinType }}</strong>
                </div>
                <div class="flex items-center justify-between gap-4">
                  <span class="text-gray-500">Kategori</span>
                  <strong class="text-right text-primary-dark">{{ store.userProfile.productCategory }}</strong>
                </div>
                <div class="space-y-2">
                  <span class="text-gray-500">Concern kulit</span>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="concern in store.userProfile.concerns"
                      :key="concern"
                      class="rounded-full border border-primary/10 bg-primary/5 px-3 py-1 text-xs font-bold text-primary-dark"
                    >
                      {{ concern }}
                    </span>
                    <span v-if="store.userProfile.concerns.length === 0" class="text-xs font-semibold text-gray-400">
                      Tidak ada concern khusus
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </section>

        <div v-if="store.error" class="rounded-3xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ store.error }}
        </div>
      </aside>

      <section class="space-y-4">
        <div class="flex items-end justify-between gap-4">
          <div>
            <p class="eyebrow">Rekomendasi</p>
            <h2 class="mt-1 text-2xl font-bold text-p-d">Produk paling cocok</h2>
          </div>
          <span class="hidden rounded-full bg-primary/10 px-3 py-1 text-xs font-bold uppercase tracking-[0.14em] text-primary md:inline-flex">
            {{ store.recommendations.length }} match
          </span>
        </div>

        <div v-if="store.recommendations.length > 0" class="grid gap-4 sm:grid-cols-2">
          <ProductCard
            v-for="product in store.recommendations"
            :key="product.id"
            :product="product"
            :is-saved="favorites.isSaved(product)"
            @view-details="openDetails"
            @toggle-save="handleToggleSave"
          />
        </div>

        <div v-else class="soft-card p-8 text-center">
          <p class="text-sm font-semibold text-gray-500">
            Backend tidak mengembalikan rekomendasi untuk profil dan cuaca saat ini.
          </p>
        </div>
      </section>
    </div>

    <ProductModal
      v-if="selectedProduct"
      :product="selectedProduct"
      :is-open="isModalOpen"
      :is-saved="favorites.isSaved(selectedProduct)"
      @close="isModalOpen = false"
      @toggle-save="handleToggleSave"
    />
  </div>
</template>

<script setup>
import { ChevronDown, RefreshCcw, Settings } from "lucide-vue-next";
import { useAnalysisStore } from "../stores/useAnalysisStore";
import { useAuthStore } from "../stores/useAuthStore";
import { useFavoritesStore } from "../stores/useFavoritesStore";
import ProductCard from "../components/ProductCard.vue";
import ProductModal from "../components/ProductModal.vue";
import WeatherCard from "../components/WeatherCard.vue";
import { computed, onMounted, reactive, ref } from "vue";
import { notifyError, notifySuccess } from "../utils/notifications";
import { displayRoutineTime } from "../utils/analysisMapping";

const store = useAnalysisStore();
const auth = useAuthStore();
const favorites = useFavoritesStore();

const selectedProduct = ref(null);
const isModalOpen = ref(false);
const openPanels = reactive({
  weather: false,
  routine: false,
  profile: false,
});
const routineSteps = computed(() => store.routineSummary?.steps || [
  { time: 'Morning', message: store.routineSummary?.morning_focus },
  { time: 'Evening', message: store.routineSummary?.evening_focus },
].filter((step) => step.message));

const openDetails = (product) => {
  selectedProduct.value = product;
  isModalOpen.value = true;
};

const togglePanel = (panel) => {
  openPanels[panel] = !openPanels[panel];
};

const handleRefresh = async () => {
  try {
    await store.refreshAnalysis();
    notifySuccess('Data diperbarui', 'Rekomendasi terbaru sudah dimuat ulang.');
  } catch (error) {
    notifyError('Refresh gagal', store.error || error.message);
  }
};

const handleToggleSave = async (product) => {
  try {
    if (!auth.isAuthenticated) {
      notifyError('Login diperlukan', 'Masuk dulu untuk menyimpan produk favorit.');
      return;
    }

    if (favorites.isSaved(product)) {
      await favorites.removeProduct(product);
      notifySuccess('Produk dihapus', 'Produk dihapus dari daftar tersimpan.');
    } else {
      await favorites.saveProduct(product, store.questionnaireId);
      notifySuccess('Produk tersimpan', 'Kamu bisa melihatnya lagi di halaman produk tersimpan.');
    }
  } catch (error) {
    notifyError('Gagal menyimpan produk', error.message);
  }
};

onMounted(async () => {
  if (!auth.isAuthenticated) return;

  try {
    await favorites.loadFavorites();
  } catch (error) {
    notifyError('Produk tersimpan gagal dimuat', error.message);
  }
});
</script>
