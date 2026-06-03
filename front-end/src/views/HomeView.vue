<script setup>
import { RouterLink } from 'vue-router';
import { ArrowRight, MapPin, Activity, ShieldCheck, Star } from 'lucide-vue-next';

</script>

<template>
  <div class="relative min-h-screen overflow-hidden bg-gradient-to-b from-white via-[#fbfaf8] to-[#f6f3ef] pb-6">

    <section class="relative container mx-auto px-12 md:px-50 pt-24 md:pt-25">
      <div class="grid items-center gap-8 lg:grid-cols-[1fr_auto]">
          <div class="max-w-4xl space-y-8">
          <div class="inline-flex items-center space-x-2 px-4 py-2 bg-primary/10 rounded-full text-primary font-bold text-sm animate-bounce">
            <Star class="w-4 h-4" />
            <span>SkinSense AI</span>
            <Star class="w-4 h-4" />
          </div>


          <div class="space-y-10">
            <h1 class="max-w-2xl text-5xl font-bold leading-[1.05] tracking-tight text-p-d md:text-7xl">
              Stop Guessing,
              <span class="italic text-s"><br>Start Understanding Your Skin.</span>
            </h1>

            <p class="max-w-2xl text-lg leading-relaxed text-gray-600 md:text-xl">
              SkinSense AI menggabungkan profil kulitmu dan data cuaca real time
              untuk memberikan rekomendasi skincare yang benar-benar sesuai, bukan sekadar yang populer.
            </p>
          </div>

          <div class="flex flex-col gap-4 sm:flex-row">
            <RouterLink to="/profile" class="btn-primary inline-flex items-center justify-center gap-3 text-lg px-8 py-4">
              <span>Cek Rekomendasi</span>
              <ArrowRight class="h-5 w-5" />
            </RouterLink>
          </div>
        </div>

        <div class="flex flex-col justify-center items-center lg:items-start gap-3 w-full max-w-xs mx-auto lg:mx-0">
  <div class="glass rounded-2xl p-10 shadow-sm flex items-start gap-3">
    <MapPin class="mt-0.5 h-10 w-10 shrink-0 text-primary" />
    <div>
      <p class="text-sm font-semibold text-p-d">Lokasi</p>
      <p class="text-sm text-gray-500">Rekomendasi sesuai cuaca tempatmu</p>
    </div>
  </div>
  <div class="glass rounded-2xl p-10 shadow-sm flex items-start gap-3">
    <Activity class="mt-0.5 h-10 w-10 shrink-0 text-primary" />
    <div>
      <p class="text-sm font-semibold text-p-d">Profil Kulit</p>
      <p class="text-sm text-gray-500">Analisis kebutuhan kulit yang spesifik</p>
    </div>
  </div>
  <div class="glass rounded-2xl p-10 shadow-sm flex items-start gap-3">
    <ShieldCheck class="mt-0.5 h-10 w-10 shrink-0 text-primary" />
    <div>
      <p class="text-sm font-semibold text-p-d">Aman</p>
      <p class="text-sm text-gray-500">Saran yang lebih terarah dan personal</p>
    </div>
  </div>
</div>
      </div>
    </section>
  </div>
</template>
        
