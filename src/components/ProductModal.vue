<template lang="">
    <transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-[60] flex items-center justify-center p-4 md:p-6">
      <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm" @click="$emit('close')"></div>
      
      <div class="relative w-full max-w-4xl bg-white rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-300">
        <button 
          @click="$emit('close')"
          class="absolute top-4 right-4 z-10 p-2 bg-white/80 backdrop-blur-md rounded-full text-gray-500 hover:text-gray-900 shadow-sm"
        >
          <X class="w-6 h-6" />
        </button>

        <div class="flex flex-col md:flex-row h-full max-h-[90vh] overflow-y-auto">
          <div class="w-full md:w-2/5 bg-secondary-light flex items-center justify-center min-h-[300px]">
            <div class="text-8xl font-display font-bold text-primary/10">{{ product.brand[0] }}</div>
          </div>

          <div class="w-full md:w-3/5 p-6 md:p-10 space-y-8">
            <div class="space-y-2">
              <div class="flex items-center space-x-3">
                <span class="text-xs font-bold text-primary px-2.5 py-1 bg-primary/10 rounded-full uppercase tracking-wider">
                  {{ product.type }}
                </span>
                <div class="flex items-center text-amber-500">
                  <Star class="w-4 h-4 fill-current" />
                  <span class="text-sm font-bold ml-1">{{ product.rating }} Rating</span>
                </div>
              </div>
              <p class="text-gray-400 font-medium tracking-wide">{{ product.brand }}</p>
              <h2 class="text-3xl md:text-4xl font-display font-bold text-gray-900">{{ product.name }}</h2>
            </div>

            <div class="space-y-4">
              <h4 class="text-sm font-bold uppercase tracking-widest text-gray-400">About Product</h4>
              <p class="text-gray-600 leading-relaxed">
                {{ product.description }}
              </p>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div class="space-y-3">
                <h4 class="text-xs font-bold uppercase tracking-widest text-gray-400">Key Ingredients</h4>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="ing in product.ingredients" 
                    :key="ing"
                    class="px-3 py-1.5 bg-gray-50 border border-gray-100 rounded-lg text-sm text-gray-700"
                  >
                    {{ ing }}
                  </span>
                </div>
              </div>
              <div class="space-y-3">
                <h4 class="text-xs font-bold uppercase tracking-widest text-gray-400">Skin Types</h4>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="skin in product.skin" 
                    :key="skin"
                    class="flex items-center text-sm text-primary-dark font-medium"
                  >
                    <CheckCircle2 class="w-4 h-4 mr-1.5 text-primary" />
                    {{ skin }}
                  </span>
                </div>
              </div>
            </div>

            <div class="bg-primary/5 rounded-2xl p-6 border border-primary/10 space-y-3">
              <div class="flex items-center space-x-2 text-primary font-bold">
                <Info class="w-5 h-5" />
                <span>Why This Product?</span>
              </div>
              <p class="text-gray-700 italic leading-relaxed">
                {{ product.whyRecommended }} Based on the current weather conditions, this product ensures your skin barrier remains protected while addressing your specific concerns.
              </p>
            </div>

            <div class="flex items-center justify-between pt-6 border-t border-gray-100">
              <div>
                <p class="text-xs font-medium text-gray-400 mb-1">Total Price</p>
                <p class="text-3xl font-display font-bold text-gray-900">{{ product.price }}</p>
              </div>
              <button class="btn-primary flex items-center space-x-3 px-8">
                <ShoppingCart class="w-5 h-5" />
                <span>Add to Routine</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
<script setup>
import { X, Star, CheckCircle2, Info, ShoppingCart } from "lucide-vue-next";

defineProps({
  product: Object,
  isOpen: Boolean,
});

</script>
<style lang="">
    
</style>