<script setup>
import { RouterLink } from 'vue-router';
import { ArrowRight, MapPin, Activity, ShieldCheck, Sparkles } from 'lucide-vue-next';

const featureItems = [
  {
    icon: MapPin,
    title: 'Cuaca real time',
    description: 'Rekomendasi mengikuti lokasi, UV, kelembapan, dan kondisi harianmu.',
  },
  {
    icon: Activity,
    title: 'Profil kulit personal',
    description: 'Skin type, concern, kategori produk, dan kandungan yang dihindari ikut dihitung.',
  },
  {
    icon: ShieldCheck,
    title: 'Lebih terarah',
    description: 'Hasilnya menjelaskan alasan produk dipilih, bukan sekadar daftar populer.',
  },
];
</script>

<template>
  <div class="relative overflow-hidden">
    <section class="page-container section-pad">
      <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-center">
        <div class="space-y-7">
          <div class="badge w-fit">
            <Sparkles class="h-3.5 w-3.5" />
            <span>AI skincare companion</span>
          </div>

          <div class="space-y-5">
            <h1 class="max-w-3xl text-5xl font-bold leading-[0.98] tracking-tight text-p-d sm:text-6xl lg:text-7xl">
              Stop guessing.
              <span class="block italic text-s-d decoration-accent-pink decoration-8 underline underline-offset-[-0.12em]">Start understanding your skin.</span>
            </h1>
            <p class="max-w-2xl text-base leading-7 text-gray-600 sm:text-lg">
              SkinSense AI menggabungkan profil kulit dan cuaca real time untuk memberi rekomendasi skincare yang terasa personal, praktis, dan siap dipakai hari ini.
            </p>
          </div>

          <div class="flex flex-col gap-3 sm:flex-row">
            <RouterLink to="/profile" class="btn-primary min-h-12 px-6">
              <span>Cek Rekomendasi</span>
              <ArrowRight class="h-4 w-4" />
            </RouterLink>
            <RouterLink to="/dashboard" class="btn-secondary min-h-12 px-6">
              <span>Lihat Dashboard</span>
            </RouterLink>
          </div>
        </div>

        <div class="grid gap-3">
          <article
            v-for="item in featureItems"
            :key="item.title"
            class="glass rounded-3xl p-5"
          >
            <div class="flex gap-4">
              <span class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-primary/10 text-primary">
                <component :is="item.icon" class="h-5 w-5" />
              </span>
              <div class="space-y-1">
                <h2 class="text-base font-bold text-p-d">{{ item.title }}</h2>
                <p class="text-sm leading-6 text-gray-600">{{ item.description }}</p>
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>
