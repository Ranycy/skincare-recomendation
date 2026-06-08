<template>
  <div class="page-container section-pad">
    <header class="mb-7 space-y-2">
      <span class="badge">Produk tersimpan</span>
      <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">Produk tersimpan</h1>
      <p class="max-w-2xl text-sm leading-6 text-gray-600">
        Kumpulan produk yang kamu simpan dari hasil rekomendasi.
      </p>
    </header>

    <div v-if="favorites.isLoading" class="soft-card p-8 text-center text-sm font-semibold text-gray-500">
      Memuat produk tersimpan...
    </div>

    <div v-else-if="favorites.favorites.length === 0" class="soft-card p-8 text-center">
      <p class="font-bold text-p-d">Belum ada produk tersimpan</p>
      <p class="mt-2 text-sm leading-6 text-gray-500">Simpan produk dari dashboard rekomendasi agar mudah ditemukan lagi.</p>
      <RouterLink to="/dashboard" class="btn-primary mt-5">Buka dashboard</RouterLink>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <article v-for="favorite in favorites.favorites" :key="favorite.id" class="card p-5">
        <div class="mb-5 flex items-start justify-between gap-3">
          <span class="badge">{{ displayCategory(favorite.category) }}</span>
          <span class="rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary-dark">
            {{ Math.round((favorite.score || 0) * 100) }}%
          </span>
        </div>
        <p class="text-xs font-bold uppercase tracking-[0.14em] text-primary/70">{{ favorite.brand }}</p>
        <h2 class="mt-2 min-h-14 text-lg font-bold leading-snug text-gray-950">{{ favorite.product_name }}</h2>
        <p class="mt-4 text-xs font-semibold text-gray-400">Tersimpan {{ formatDate(favorite.created_at) }}</p>
        <button class="btn-secondary mt-5 w-full" @click="removeFavorite(favorite)">
          Hapus
        </button>
      </article>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useFavoritesStore } from "../stores/useFavoritesStore";
import { notifyError, notifySuccess } from "../utils/notifications";
import { displayCategory } from "../utils/analysisMapping";

const favorites = useFavoritesStore();

function formatDate(value) {
  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(value));
}

async function removeFavorite(favorite) {
  try {
    await favorites.removeProduct(favorite);
    notifySuccess("Produk dihapus", "Daftar tersimpan sudah diperbarui.");
  } catch (error) {
    notifyError("Gagal menghapus", error.message);
  }
}

onMounted(async () => {
  try {
    await favorites.loadFavorites();
  } catch (error) {
    notifyError("Produk tersimpan gagal dimuat", error.message);
  }
});
</script>
