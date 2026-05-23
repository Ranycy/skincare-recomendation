<script setup>
import { RouterLink } from 'vue-router';
import { ArrowRight, MapPin, Activity, ShieldCheck, Sparkles } from 'lucide-vue-next';

const steps = [
  {
    title: 'Detect Location',
    desc: 'We analyze your current environmental data automatically.',
    icon: MapPin,
    color: 'bg-emerald-100 text-emerald-600'
  },
  {
    title: 'Analyze Weather',
    desc: 'Humidity, UV, and pollution levels are factored in.',
    icon: Activity,
    color: 'bg-blue-100 text-blue-600'
  },
  {
    title: 'Get Results',
    desc: 'Receive curated products tailored to your skin needs.',
    icon: ShieldCheck,
    color: 'bg-amber-100 text-amber-600'
  }
];
</script>

<template>
  <div class="space-y-24 pb-24">
    <section class="relative pt-16 md:pt-32 overflow-hidden">
      <div class="container mx-auto px-4 md:px-6 relative z-10">
        <div class="max-w-4xl mx-auto text-center space-y-8">
          <div class="inline-flex items-center space-x-2 px-4 py-2 bg-primary/10 rounded-full text-primary font-bold text-sm animate-bounce">
            <Sparkles class="w-4 h-4" />
            <span>Smart Skincare for the Modern Age</span>
          </div>
          
          <h1 class="text-5xl md:text-7xl lg:text-8xl font-display font-bold text-gray-900 leading-[1.1] tracking-tight">
            SkinSync: Adapted to Your <span class="text-primary italic">Environment</span>
          </h1>
          
          <p class="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Personalized skincare recommendations that change with the weather. 
            Because your skin needs different care in 80% humidity than it does in 20%.
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <RouterLink to="/profile" class="btn-primary flex items-center space-x-3 text-lg px-8 py-4 w-full sm:w-auto">
              <span>Get My Recommendations</span>
              <ArrowRight class="w-5 h-5" />
            </RouterLink>
            <RouterLink to="/" class="btn-secondary px-8 py-4 w-full sm:w-auto border border-gray-200">
              How it works
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-gradient-to-b from-primary/5 to-transparent -z-10 rounded-full blur-3xl"></div>
    </section>

    <section class="container mx-auto px-4 md:px-6">
      <div class="bg-white rounded-[3rem] p-8 md:p-16 shadow-sm border border-gray-100">
        <div class="text-center mb-16 space-y-4">
          <h2 class="text-3xl md:text-4xl font-display font-bold text-gray-900">How It Works</h2>
          <p class="text-gray-500 max-w-lg mx-auto">Our smart algorithm ensures your routine is always optimized for your current surroundings.</p>
        </div>

        <div class="grid md:grid-cols-3 gap-12">
          <div v-for="(step, index) in steps" :key="index" class="relative group text-center">
            <div class="mb-8 relative flex justify-center">
              <div :class="['w-16 h-16 rounded-2xl flex items-center justify-center transition-transform group-hover:scale-110 duration-300', step.color]">
                <component :is="step.icon" class="w-8 h-8" />
              </div>
              <div v-if="index < 2" class="hidden md:block absolute top-8 left-full w-full border-t-2 border-dashed border-gray-100 -z-10"></div>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ step.title }}</h3>
            <p class="text-gray-500 leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="container mx-auto px-4 md:px-6">
      <div class="bg-primary-dark rounded-[3rem] p-12 md:p-24 text-center text-white relative overflow-hidden">
        <div class="absolute inset-0 opacity-10">
          <div class="absolute top-0 left-0 w-96 h-96 bg-primary-light rounded-full blur-[100px]"></div>
          <div class="absolute bottom-0 right-0 w-96 h-96 bg-primary-light rounded-full blur-[100px]"></div>
        </div>
        
        <div class="relative z-10 space-y-8">
          <h2 class="text-4xl md:text-6xl font-display font-bold max-w-2xl mx-auto">Ready to synchronize your skincare?</h2>
          <p class="text-lg text-primary-light/80 max-w-xl mx-auto">Join thousands of others who have optimized their routine for their local weather.</p>
          <RouterLink to="/profile" class="btn-secondary inline-flex items-center space-x-3 text-lg px-10 py-5">
            <span>Start Free Analysis</span>
            <ArrowRight class="w-5 h-5" />
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>