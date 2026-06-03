
<template>
  <div class="min-h-[calc(100vh-80px)] flex items-center justify-center py-20 px-4">
    <div class="max-w-xl w-full bg-white rounded-[2.5rem] shadow-2xl shadow-s\p-d/70 p-8 md:p-12 space-y-10 border border-gray-100">
      <div class="text-center space-y-2">
        <div class="w-16 h-16 bg-s-l/50 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <Flower class="w-10 h-10 text-s " />
        </div>
        <h1 class="text-3xl font-display font-bold text-gray-900">Profil Kulit Kamu</h1>
        <p class="text-gray-500">Yuk, ceritakan kondisi kulitmu supaya rekomendasinya makin pas.</p>
      </div>

      <div class="space-y-10">
        <!-- Skin Type selection -->
        <div class="space-y-4">
          <label class="text-sm font-bold uppercase tracking-widest text-gray-400">Jenis kulit kamu</label>
          <div class="grid grid-cols-5 sm:grid-cols-3 gap-5">
            <button 
              v-for="type in skinTypes" 
              :key="type"
              @click="form.skinType = type"
              :class="[
                'px-4 py-3 rounded-xl border-2 text-sm font-medium transition-all duration-200',
                form.skinType === type 
                  ? 'border-s bg-primary/5 text-s shadow-sm font-semibold' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              {{ type }}
            </button>
          </div>
        </div>

        <!-- Skin concerns selection -->
        <div class="space-y-4">
          <label class="text-sm font-bold uppercase tracking-widest text-gray-400">Masalah kulit yang kamu alami</label>
          <div class="flex flex-wrap gap-3">
            <button 
              v-for="concern in concerns" 
              :key="concern"
              @click="toggleConcern(concern)"
              :class="[
                'px-5 py-2.5 rounded-full border-2 text-sm font-medium flex items-center space-x-2 transition-all duration-200',
                form.concerns.includes(concern)
                  ? 'border-s bg-s text-white shadow-md' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              <Check v-if="form.concerns.includes(concern)" class="w-4 h-4" />
              <span>{{ concern }}</span>
            </button>
          </div>
        </div>

        <!-- Product selection -->
        <div class="space-y-4">
          <label class="text-sm font-bold uppercase tracking-widest text-gray-400">Produk yang kamu butuhkan (pilih minimal satu)</label>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <button 
              v-for="prod in productCategories" 
              :key="prod"
              @click="toggleProduct(prod)"
              :class="[
                'px-4 py-3 rounded-xl border-2 text-sm font-medium flex items-center justify-center space-x-2 transition-all duration-200',
                form.products.includes(prod) 
                  ? 'border-s bg-primary/5 text-s shadow-sm font-semibold' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              <Check v-if="form.products.includes(prod)" class="w-4 h-4 shrink-0" />
              <span>{{ prod }}</span>
            </button>
          </div>
        </div>

        <!-- Daily activity (Only shows if Sunscreen is selected) -->
        <div v-if="form.products.includes('Sunscreen')" class="space-y-4 p-5 bg-secondary-light/30 border border-secondary/30 rounded-2xl transition-all duration-300">
          <label class="text-sm font-bold uppercase tracking-widest text-gray-600 block">Aktivitas Harian (Khusus Sunscreen)</label>
          <p class="text-xs text-gray-500 mb-2 font-sans">Pilih aktivitas harian Anda untuk mencocokkan tingkat SPF yang paling sesuai.</p>
          <div class="grid grid-cols-2 gap-3">
            <button 
              @click="form.activity = 'Indoor'"
              :class="[
                'px-4 py-3 rounded-xl border-2 text-sm font-medium transition-all duration-200',
                form.activity === 'Indoor'
                  ? 'border-s bg-s text-white shadow-sm font-semibold' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              Indoor (Dalam Ruangan)
            </button>
            <button 
              @click="form.activity = 'Outdoor'"
              :class="[
                'px-4 py-3 rounded-xl border-2 text-sm font-medium transition-all duration-200',
                form.activity === 'Outdoor'
                 ? 'border-s bg-s text-white shadow-sm font-semibold' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              Outdoor (Luar Ruangan)
            </button>
          </div>
        </div>

        <!-- Allergies / Avoid ingredients selection -->
        <div class="space-y-4">
          <label class="text-sm font-bold uppercase tracking-widest text-gray-400">Alergi & Kandungan yang Dihindari</label>
          <p class="text-xs text-gray-500 mb-2 font-sans">Kami akan memfilter produk yang mengandung bahan-bahan ini.</p>
          
          <div class="flex flex-wrap gap-2 mb-3">
            <button 
              v-for="ing in avoidOptions" 
              :key="ing"
              @click="toggleAvoid(ing)"
              :class="[
                'px-4 py-2 rounded-full border-2 text-xs font-medium flex items-center space-x-1.5 transition-all duration-200',
                form.avoidIngredients.includes(ing)
                  ? 'border-red-500 bg-red-50 text-red-600 shadow-sm font-semibold' 
                  : 'border-gray-100 bg-gray-50 text-gray-600 hover:border-gray-200'
              ]"
            >
              <Check v-if="form.avoidIngredients.includes(ing)" class="w-3.5 h-3.5 shrink-0" />
              <span>{{ ing }}</span>
            </button>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-semibold text-gray-500 font-sans">Bahan Kimia/Kandungan Khusus Lainnya</label>
            <input 
              type="text" 
              v-model="form.customAvoidIngredients"
              placeholder="Contoh: Centella, Salicylic Acid (pisahkan dengan koma)" 
              class="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200"
            />
          </div>
        </div>
      </div>

      <!-- Submit button -->
      <button 
        @click="handleSubmit"
        :disabled="!form.skinType || form.products.length === 0"
        class="btn-s-light w-full py-4 flex items-center justify-center space-x-3 disabled:opacity-50 disabled:cursor-not-allowed mt-8 shadow-xl shadow-primary/20 font-semibold"
      >
        <Leaf class="w-5 h-5 animate-pulse" />
        <span>Lihat Hasil Analisis</span>
        <ArrowRight class="w-5 h-5" />
      </button>

      <p class="text-center text-xs text-gray-400 italic font-sans">
        Kami menggunakan jawabanmu untuk memberikan rekomendasi yang lebih sesuai.
      </p>
    </div>
  </div>
</template>

<script setup>
import { Leaf, Flower, Smile, Star } from 'lucide-vue-next'
import { useRouter } from 'vue-router';
import {useAnalysisStore} from '../stores/useAnalysisStore';
import { reactive, ref } from 'vue';

import { Check, ArrowRight } from 'lucide-vue-next';

const router = useRouter();
const store = useAnalysisStore();

const skinTypes = ['Normal', 'Kering', 'Berminyak', 'Kombinasi', 'Sensitif'];
const concerns = ['Jerawat', 'Kusam', 'Penuaan', 'Bekas jerawat', 'Dehidrasi'];
const productCategories = ['Cleanser', 'Moisturizer', 'Masker', 'Eye cream', 'Sunscreen'];
const avoidOptions = ['Alkohol', 'Fragrance', 'Paraben', 'Silikon', 'Sulfat'];

const form = reactive({
  skinType: '',
  concerns: [],          
  products: [],          
  activity: 'Indoor',    
  avoidIngredients: [],  
  customAvoidIngredients: ''
});

const toggleConcern = (concern) => {
  const index = form.concerns.indexOf(concern);
  if (index === -1) {
    form.concerns.push(concern);
  } else {
    form.concerns.splice(index, 1);
  }
};

const toggleProduct = (product) => {
  const index = form.products.indexOf(product);
  if (index === -1) {
    form.products.push(product);
  } else {
    form.products.splice(index, 1);
  }
};

const toggleAvoid = (ingredient) => {
  const index = form.avoidIngredients.indexOf(ingredient);
  if (index === -1) {
    form.avoidIngredients.push(ingredient);
  } else {
    form.avoidIngredients.splice(index, 1);
  }
};

const handleSubmit = () => {
  if (!form.skinType || form.products.length === 0) return;
  store.setProfile(form);
  router.push('/dashboard');
};

</script>

<style>
    
</style>