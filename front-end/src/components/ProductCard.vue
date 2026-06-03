<template lang="">
  <div class="card group h-full flex flex-col cursor-pointer" @click="$emit('view-details', product)">
    <div class="aspect-square bg-secondary-light relative overflow-hidden">
      <div class="absolute inset-0 flex items-center justify-center text-primary/20">
        <div class="text-4xl font-display font-bold">{{ product.brand[0] }}</div>
      </div>
      <div class="absolute top-3 left-3">
        <span class="px-2.5 py-1 bg-white/90 backdrop-blur-sm text-[10px] font-bold uppercase tracking-wider rounded-full text-primary border border-primary/10">
          {{ product.type }}
        </span>
      </div>
      <div class="absolute inset-0 bg-primary/0 group-hover:bg-primary/5 transition-colors duration-300"></div>
    </div>
    
    <div class="p-5 flex-grow flex flex-col">
      <div class="flex justify-between items-start mb-2">
        <p class="text-xs font-medium text-gray-400 uppercase tracking-wide">{{ product.brand }}</p>
        <div class="flex items-center text-amber-500">
          <Star class="w-3 h-3 fill-current" />
          <span class="text-xs font-bold ml-1">{{ product.rating }}</span>
        </div>
      </div>
      
      <h3 class="text-lg font-bold text-gray-900 mb-2 leading-tight group-hover:text-primary transition-colors">
        {{ product.name }}
      </h3>

      <div class="flex flex-wrap gap-1.5 mb-4">
        <span 
          v-for="ing in product.ingredients" 
          :key="ing"
          class="text-[10px] px-2 py-0.5 bg-gray-50 text-gray-500 rounded-md border border-gray-100"
        >
          {{ ing }}
        </span>
      </div>

      <div class="mt-auto pt-4 border-t border-gray-50 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-lg font-display font-bold text-gray-900">{{ product.price }}</span>
          <button class="p-2 bg-primary/10 text-primary rounded-lg group-hover:bg-primary group-hover:text-white transition-all duration-300">
            <ArrowRight class="w-4 h-4" />
          </button>
        </div>
        
        <div class="bg-primary/5 p-2.5 rounded-xl">
          <p class="text-[11px] text-primary-dark/80 leading-relaxed italic">
            "{{ product.whyRecommended }}"
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import{Star, ArrowRight} from "lucide-vue-next";

defineProps({
  product: Object,
});
</script>
<style lang="">
    
</style>