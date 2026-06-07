<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-5">
      <div class="space-y-2">
        <span class="badge">Daily result</span>
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
          <span>{{ store.isLoading ? 'Refreshing' : 'Refresh' }}</span>
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

        <section class="soft-card p-5">
          <div class="mb-5 flex items-start justify-between gap-4">
            <div>
              <p class="eyebrow">Profile match</p>
              <h2 class="mt-1 text-xl font-bold text-p-d">Kondisi pilihanmu</h2>
            </div>
            <span class="badge">{{ store.recommendations.length }} matches</span>
          </div>

          <div class="space-y-4 text-sm">
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Skin type</span>
              <strong class="text-right text-primary-dark">{{ store.userProfile.skinType }}</strong>
            </div>
            <div class="flex items-center justify-between gap-4">
              <span class="text-gray-500">Kategori</span>
              <strong class="text-right text-primary-dark">{{ store.userProfile.productCategory }}</strong>
            </div>
            <div class="space-y-2">
              <span class="text-gray-500">Concern</span>
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
        </section>

        <div v-if="store.error" class="rounded-3xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ store.error }}
        </div>
      </aside>

      <section class="space-y-4">
        <div class="flex items-end justify-between gap-4">
          <div>
            <p class="eyebrow">Recommendation</p>
            <h2 class="mt-1 text-2xl font-bold text-p-d">Produk paling cocok</h2>
          </div>
          <span class="hidden rounded-full bg-primary/10 px-3 py-1 text-xs font-bold uppercase tracking-[0.14em] text-primary md:inline-flex">
            {{ store.recommendations.length }} matches
          </span>
        </div>

        <div v-if="store.recommendations.length > 0" class="grid gap-4 sm:grid-cols-2">
          <ProductCard
            v-for="product in store.recommendations"
            :key="product.id"
            :product="product"
            @view-details="openDetails"
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
      @close="isModalOpen = false"
    />
  </div>
</template>

<script setup>
import { RefreshCcw, Settings } from "lucide-vue-next";
import { useAnalysisStore } from "../stores/useAnalysisStore";
import ProductCard from "../components/ProductCard.vue";
import ProductModal from "../components/ProductModal.vue";
import WeatherCard from "../components/WeatherCard.vue";
import { ref } from "vue";
import { notifyError, notifySuccess } from "../utils/notifications";

const store = useAnalysisStore();

const selectedProduct = ref(null);
const isModalOpen = ref(false);

const openDetails = (product) => {
  selectedProduct.value = product;
  isModalOpen.value = true;
};

const handleRefresh = async () => {
  try {
    await store.refreshAnalysis();
    notifySuccess('Data diperbarui', 'Rekomendasi terbaru sudah dimuat ulang.');
  } catch (error) {
    notifyError('Refresh gagal', store.error || error.message);
  }
};
</script>
