<script setup>
import { Sparkles } from 'lucide-vue-next';
</script>

<template>
  <footer class="bg-primary-dark text-white py-12 md:py-16">
    <div class="container mx-auto px-4 md:px-6">
      <div class="flex flex-col md:flex-row justify-between items-center space-y-8 md:space-y-0">
        <div class="text-center md:text-left space-y-4">
          <div class="flex items-center justify-center md:justify-start space-x-2">
            <Sparkles class="w-6 h-6 text-primary-light" />
            <span class="text-2xl font-display font-bold tracking-tight">SkinSense AI</span>
          </div>
          <p class="text-primary-light/80 max-w-xs">
            Smart Skincare, Adapted to Your Environment.
          </p>
        </div>

        <div class="flex space-x-8 text-sm font-medium">
          <a href="#" class="hover:text-primary-light transition-colors">Privacy Policy</a>
          <a href="#" class="hover:text-primary-light transition-colors">Terms of Service</a>
          <a href="#" class="hover:text-primary-light transition-colors">Contact Us</a>
        </div>

        <div class="text-sm text-primary-light/60">
          © 2024 SkinSense AI. All rights reserved.
        </div>
      </div>
    </div>
  </footer>
</template>
