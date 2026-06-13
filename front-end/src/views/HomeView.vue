<script setup>
import { RouterLink } from 'vue-router';
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { ArrowRight, MapPin, Activity, ShieldCheck, Sparkles } from 'lucide-vue-next';
import { useLocaleStore } from '../stores/useLocaleStore';

const { t } = useI18n();
const locale = useLocaleStore();
const featureItems = computed(() => [
  {
    icon: MapPin,
    title: t('home.features.weather.title'),
    description: t('home.features.weather.description'),
  },
  {
    icon: Activity,
    title: t('home.features.profile.title'),
    description: t('home.features.profile.description'),
  },
  {
    icon: ShieldCheck,
    title: t('home.features.explanation.title'),
    description: t('home.features.explanation.description'),
  },
]);
</script>

<template>
  <div class="relative overflow-hidden">
    <section class="page-container section-pad">
      <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_22rem] lg:items-center">
        <div class="space-y-7">
          <div class="badge w-fit">
            <Sparkles class="h-3.5 w-3.5" />
            <span>{{ t('home.badge') }}</span>
          </div>

          <div class="space-y-5">
            <h1 class="max-w-3xl text-5xl font-bold leading-[0.98] tracking-tight text-p-d sm:text-6xl lg:text-7xl">
              {{ t('home.titleStart') }}
              <span class="block italic text-s-d decoration-accent-pink decoration-8 underline underline-offset-[-0.12em]">{{ t('home.titleEmphasis') }}</span>
            </h1>
            <p class="max-w-2xl text-base leading-7 text-gray-600 sm:text-lg">
              {{ t('home.description') }}
            </p>
          </div>

          <div class="flex flex-col gap-3 sm:flex-row">
            <RouterLink :to="locale.path('/profile')" class="btn-primary min-h-12 px-6">
              <span>{{ t('home.primaryCta') }}</span>
              <ArrowRight class="h-4 w-4" />
            </RouterLink>
            <RouterLink :to="locale.path('/dashboard')" class="btn-secondary min-h-12 px-6">
              <span>{{ t('home.secondaryCta') }}</span>
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
