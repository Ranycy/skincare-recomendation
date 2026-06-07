<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { Menu, X, Leaf, Sparkles } from 'lucide-vue-next';

const isMenuOpen = ref(false);
const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Analysis', path: '/profile' },
  { name: 'Dashboard', path: '/dashboard' },
];
</script>

<template>
  <nav class="sticky top-0 z-50 border-b border-primary/10 bg-white/85 backdrop-blur-xl">
    <div class="page-container">
      <div class="flex h-16 items-center justify-between md:h-20">
        <RouterLink to="/" class="flex min-w-0 items-center gap-2 group" @click="isMenuOpen = false">
          <span class="grid h-10 w-10 shrink-0 place-items-center rounded-2xl bg-primary/10 text-primary transition-transform group-hover:-rotate-6">
            <Leaf class="h-5 w-5" />
          </span>
          <span class="truncate text-lg font-display font-bold tracking-tight text-p-d sm:text-2xl">
            SkinSense AI
          </span>
        </RouterLink>

        <div class="hidden items-center gap-7 md:flex">
          <RouterLink
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="text-sm font-semibold text-gray-500 transition-colors hover:text-primary"
            active-class="text-primary"
          >
            {{ link.name }}
          </RouterLink>
          <RouterLink to="/profile" class="btn-primary px-5 py-2.5">
            <Sparkles class="h-4 w-4" />
            <span>Get Started</span>
          </RouterLink>
        </div>

        <button
          @click="isMenuOpen = !isMenuOpen"
          class="grid h-10 w-10 place-items-center rounded-2xl border border-primary/10 bg-white text-primary shadow-sm md:hidden"
          aria-label="Toggle navigation menu"
        >
          <Menu v-if="!isMenuOpen" class="h-5 w-5" />
          <X v-else class="h-5 w-5" />
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isMenuOpen" class="border-t border-primary/10 bg-white px-4 py-4 shadow-sm md:hidden">
        <div class="space-y-2">
          <RouterLink
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            @click="isMenuOpen = false"
            class="flex items-center justify-between rounded-2xl px-4 py-3 text-sm font-bold text-gray-600"
            active-class="bg-primary/10 text-primary"
          >
            {{ link.name }}
          </RouterLink>
          <RouterLink to="/profile" @click="isMenuOpen = false" class="btn-primary mt-2 w-full">
            <Sparkles class="h-4 w-4" />
            <span>Start Analysis</span>
          </RouterLink>
        </div>
      </div>
    </transition>
  </nav>
</template>
