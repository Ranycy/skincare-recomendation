<template>
  <div class="container mx-auto px-4 md:px-6 py-12 md:py-16 space-y-16">
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
      <div class="space-y-2">
        <h1 class="text-4xl md:text-5xl font-display font-bold text-gray-900 tracking-tight">
          Hello, <span class="text-primary italic">Ini Dashboard Kamu </span> 
        </h1>
        <p class="text-gray-500 flex items-center gap-2">
          <Lightbulb class="w-4 h-4 text-primary" />
          Ini rutinitas skincare yang cocok buat kamu hari ini.
        </p>
      </div>
      
      <div class="flex items-center space-x-3">
        <button class="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-100 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">
          <RefreshCcw class="w-4 h-4" />
          <span>Refresh Data</span>
        </button>
        <RouterLink to="/profile" class="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-100 rounded-xl text-sm font-medium hover:bg-gray-50 transition-colors">
          <Settings class="w-4 h-4" />
          <span>Edit Profile</span>
        </RouterLink>
      </div>
    </header>

    <div class="grid lg:grid-cols-12 gap-12">
      <div class="lg:col-span-5 space-y-8">
        <h2 class="text-2xl font-display text-gray-700 flex items-center space-x-3">
          <span>Kondisi Lingkungan</span>
        </h2>
        <WeatherCard :weather="store.weatherData" :alert="store.skinAlert" />
        
        <div class="bg-primary/5 p-6 md:p-8 rounded-[2rem] border border-primary/10">
          <h3 class="font-bold text-gray-900 mb-4">Current Profile Match</h3>
          <div class="space-y-4">
            <div class="flex justify-between items-center text-sm">
              <span class="text-gray-500">Skin Type</span>
              <span class="font-bold text-primary">{{ store.userProfile.skinType }}</span>
            </div>
            <div class="flex justify-between items-start text-sm">
              <span class="text-gray-500">Target Concerns</span>
              <div class="flex flex-wrap justify-end gap-2 max-w-[150px]">
                <span 
                  v-for="concern in store.userProfile.concerns" 
                  :key="concern"
                  class="px-2 py-0.5 bg-white rounded-md text-[10px] font-bold text-gray-600 border border-gray-100 shadow-sm"
                >
                  {{ concern }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Recommendations -->
      <div class="lg:col-span-7 space-y-8">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-display text-gray-700 flex items-center space-x-3">Rekomendasi Hari Ini</h2>
          <span class="text-xs font-bold uppercase tracking-widest text-primary px-3 py-1 bg-primary/10 rounded-full">
            {{ store.recommendations.length }} Matches
          </span>
        </div>

        <div class="grid sm:grid-cols-2 gap-6">
          <ProductCard 
            v-for="product in store.recommendations" 
            :key="product.id" 
            :product="product" 
            @view-details="openDetails"
          />
        </div>

        <!-- Empty state if no recommendations -->
        <div v-if="store.recommendations.length === 0" class="bg-gray-50 rounded-3xl p-12 text-center border-2 border-dashed border-gray-200">
          <p class="text-gray-500 font-medium">No direct matches found for your current profile and weather. Try updating your concerns!</p>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <ProductModal 
      v-if="selectedProduct" 
      :product="selectedProduct" 
      :is-open="isModalOpen" 
      @close="isModalOpen = false" 
    />
  </div>
</template>
<script setup>
import { Sparkles, RefreshCcw, Settings, Lightbulb } from "lucide-vue-next";
import { useAnalysisStore } from "../stores/useAnalysisStore";
import ProductCard from "../components/ProductCard.vue";
import ProductModal from "../components/ProductModal.vue";
import WeatherCard from "../components/WeatherCard.vue";
import { ref } from "vue";

const store = useAnalysisStore();

const selectedProduct = ref(null);
const isModalOpen = ref(false);

const openDetails = (product) => {
  selectedProduct.value = product;
  isModalOpen.value = true;
};
</script>
<style lang="">
  
</style>