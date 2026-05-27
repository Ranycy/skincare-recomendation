<script setup>
import { RouterLink } from 'vue-router';
import { ArrowRight, MapPin, Activity, ShieldCheck, Sparkles } from 'lucide-vue-next';

</script>

<template>
  <div class="space-y-24 pb-6">

    <!-- HERO -->
    <section class="relative pt-12 md:pt-24 overflow-hidden">
      <div class="container mx-auto px-4 md:px-10 relative z-10">
       
        <div class="max-w-4xl space-y-8">
          <div class="inline-flex items-center space-x-2 px-4 py-2 bg-primary/10 rounded-full text-primary font-bold text-sm animate-bounce">
            <Sparkles class="w-4 h-4" />
            <span>SkinSense AI</span>
          </div>

          <h1 class="text-5xl md:text-7xl lg:text-8xl font-display font-bold text-p-d leading-[1.1] tracking-tight">
            Stop Guessing,
            <span class="text-s italic"><br>Start Understanding Your Skin.</span>
          </h1>

         
          <p class="text-lg md:text-xl text-gray-600 max-w-2xl leading-relaxed">
            SkinSense AI menggabungkan profil kulitmu dan data cuaca real time
            untuk memberikan rekomendasi skincare yang benar-benar sesuai bukan sekadar yang populer.
          </p>

          <div class="flex flex-col sm:flex-row items-center gap-4 pt-4">
            <RouterLink to="/profile" class="btn-primary flex items-center space-x-3 text-lg px-8 py-4 w-full sm:w-auto">
              <span>Cek Rekomendasi</span>
              <ArrowRight class="w-5 h-5" />
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-gradient-to-b from-primary/5 to-transparent -z-10 rounded-full blur-3xl"></div>
    </section>

    <!-- Bulatan dekoratif kiri bawah -->
      <div class="absolute -bottom-30 -left-3 w-120 h-120 rounded-full bg-[var(--color-p)] opacity-30 -z-10"></div>
 
      <!-- Bulatan dekoratif kanan atas -->
      <div class="absolute -top-0 -right-1 w-120 h-120 rounded-full bg-[var(--color-s)] opacity-20 -z-10"></div>
      <!-- Bulatan dekoratif kiri atas ujung -->
      <div class="absolute -top-20 -left-40 w-90 h-90 rounded-full bg-[var(--color-p)] opacity-30 -z-10"></div>
        <!-- Bulatan dekoratif kanan bawah -->
      <div class="absolute -bottom-18 -right-[-340px] w-80 h-80 rounded-full bg-[var(--color-s)] opacity-20 -z-10"></div>
      <!-- Bulatan dekoratif kiri atas tengah -->
      <div class="absolute -top-70 -left-[-500px] w-120 h-120 rounded-full bg-[var(--color-p)] opacity-30 -z-10"></div>


 
      
  </div>
</template>