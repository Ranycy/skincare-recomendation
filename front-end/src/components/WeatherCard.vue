<template lang="">
    <div class="space-y-6">
    <div class="bg-gradient-to-br from-primary to-primary-dark p-6 md:p-8 rounded-3xl text-white shadow-xl relative overflow-hidden">
      <div class="absolute top-0 right-0 -mr-8 -mt-8 w-48 h-48 bg-white/10 rounded-full blur-3xl"></div>
      
      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div class="flex items-center space-x-2 text-primary-light mb-2">
            <MapPin class="w-4 h-4" />
            <span class="text-sm font-medium tracking-wide uppercase">{{ weather.location }}</span>
          </div>
          <h2 class="text-5xl font-display font-bold mb-2">{{ weather.temperature }}°C</h2>
          <p class="text-lg opacity-90 capitalize">{{ weather.condition }} Today</p>
        </div>

        <div class="grid grid-cols-2 gap-4 md:gap-8">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-white/20 rounded-xl">
              <Droplets class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs opacity-70">Humidity</p>
              <p class="font-bold">{{ weather.humidity }}%</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-white/20 rounded-xl">
              <Sun class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs opacity-70">UV Index</p>
              <p class="font-bold">{{ weather.uvIndex }} (High)</p>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <div class="p-2 bg-white/20 rounded-xl">
              <Wind class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs opacity-70">PM2.5</p>
              <p class="font-bold">{{ weather.pm25 }} µg/m³</p>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <div class="p-2 bg-white/20 rounded-xl">
              <CloudRain class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs opacity-70">Precip.</p>
              <p class="font-bold">12%</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-amber-50 border border-amber-100 p-4 rounded-2xl flex items-start space-x-4">
      <div class="p-2 bg-amber-100 rounded-full text-amber-600">
        <ShieldAlert class="w-5 h-5" />
      </div>
      <div>
        <h4 class="font-bold text-amber-900 text-sm">Skin Condition Alert</h4>
        <p class="text-amber-800 text-sm leading-relaxed">{{ alert }}</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { MapPin, Droplets, Sun, Wind, CloudRain, ShieldAlert } from "lucide-vue-next";

defineProps({
  weather: Object,
  alert: String,
});

</script>
<style lang="">
    
</style>