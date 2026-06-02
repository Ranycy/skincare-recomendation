<script setup>
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import { Sparkles, Menu, X, Leaf } from 'lucide-vue-next';

const isMenuOpen = ref(false);
const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Analysis', path: '/profile' },
  { name: 'Dashboard', path: '/dashboard' },
];
</script>

<template>
  <nav class="sticky top-0 z-50 glass border-b border-gray-100">
    <div class="container mx-auto px-4 md:px-6">
      <div class="flex items-center justify-between h-16 md:h-20">
        <RouterLink to="/" class="flex items-center space-x-2 group">
          <div class=" p-1 rounded-lg transition-transform group-hover:rotate-12">
            <Leaf class="w-6 h-6 text-primary" />
          </div>
          <span class="text-xl md:text-2xl font-display font-bold text-p-d tracking-tight">
            SkinSense AI
          </span>
        </RouterLink>

        <div class="hidden md:flex items-center space-x-8">
          <RouterLink 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            class="text-gray-600 hover:text-primary font-medium transition-colors"
            active-class="text-primary"
          >
            {{ link.name }}
          </RouterLink>
          <RouterLink to="/profile" class="btn-primary py-2 px-5 text-sm">
            Get Started
          </RouterLink>
        </div>

        <button 
          @click="isMenuOpen = !isMenuOpen"
          class="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Menu v-if="!isMenuOpen" class="w-6 h-6" />
          <X v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="isMenuOpen" class="md:hidden bg-white border-b border-gray-100 py-4 px-4 space-y-4">
        <RouterLink 
          v-for="link in navLinks" 
          :key="link.path"
          :to="link.path"
          @click="isMenuOpen = false"
          class="block text-gray-600 font-medium py-2"
          active-class="text-primary font-bold"
        >
          {{ link.name }}
        </RouterLink>
        <RouterLink 
          to="/profile" 
          @click="isMenuOpen = false"
          class="btn-primary block text-center w-full"
        >
          Get Started
        </RouterLink>
      </div>
    </transition>
  </nav>
</template>
