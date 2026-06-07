<template>
  <section class="overflow-hidden rounded-3xl bg-gradient-to-br from-primary to-primary-dark p-5 text-white shadow-[0_18px_45px_rgba(45,62,39,0.20)]">
    <div class="mb-6 flex items-start justify-between gap-4">
      <div>
        <div class="mb-2 flex items-start gap-2 text-primary-light">
          <MapPin class="h-4 w-4" />
          <div class="min-w-0">
            <span class="block text-[10px] font-bold uppercase tracking-[0.16em] text-primary-light/75">Scanned location</span>
            <span class="mt-0.5 block max-w-[13rem] truncate text-xs font-bold uppercase tracking-[0.12em] text-white">
              {{ weather.location }}
            </span>
          </div>
        </div>
        <h2 class="text-5xl font-display font-bold leading-none">{{ weather.temperature }}&deg;C</h2>
        <p class="mt-2 text-sm font-semibold text-white/80">{{ weather.condition }} today</p>
      </div>
      <span class="rounded-2xl bg-white/15 px-3 py-2 text-xs font-bold text-white/90">
        Live
      </span>
    </div>

    <div class="grid grid-cols-3 gap-2">
      <div class="rounded-2xl bg-white/12 p-3">
        <Droplets class="mb-2 h-4 w-4 text-primary-light" />
        <p class="text-[10px] font-semibold uppercase tracking-[0.12em] text-white/60">Humidity</p>
        <p class="mt-1 text-sm font-bold">{{ weather.humidity }}%</p>
      </div>
      <div class="rounded-2xl bg-white/12 p-3">
        <Sun class="mb-2 h-4 w-4 text-primary-light" />
        <p class="text-[10px] font-semibold uppercase tracking-[0.12em] text-white/60">UV</p>
        <p class="mt-1 text-sm font-bold">{{ weather.uvIndex }}</p>
      </div>
      <div class="rounded-2xl bg-white/12 p-3">
        <Wind class="mb-2 h-4 w-4 text-primary-light" />
        <p class="text-[10px] font-semibold uppercase tracking-[0.12em] text-white/60">PM2.5</p>
        <p class="mt-1 text-sm font-bold">{{ weather.pm25 }}</p>
      </div>
    </div>

    <div class="mt-4 rounded-2xl border border-white/10 bg-white/10 p-3">
      <div class="flex gap-3">
        <ShieldAlert class="mt-0.5 h-4 w-4 shrink-0 text-primary-light" />
        <p class="text-sm leading-6 text-white/86">{{ alert }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { MapPin, Droplets, Sun, Wind, ShieldAlert } from "lucide-vue-next";

defineProps({
  weather: Object,
  alert: String,
});
</script>
