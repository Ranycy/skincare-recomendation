<script setup>
import { computed, ref } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Menu, X, Leaf, Sparkles, LogOut } from 'lucide-vue-next';
import { useAuthStore } from '../stores/useAuthStore';
import { useAnalysisStore } from '../stores/useAnalysisStore';
import { useLocaleStore } from '../stores/useLocaleStore';
import { notifyError, notifySuccess } from '../utils/notifications';

const isMenuOpen = ref(false);
const auth = useAuthStore();
const analysis = useAnalysisStore();
const locale = useLocaleStore();
const route = useRoute();
const router = useRouter();
const { t } = useI18n();
const navLinks = computed(() => [
  { name: t('nav.home'), path: '/' },
  { name: t('nav.analysis'), path: '/profile' },
  { name: t('nav.dashboard'), path: '/dashboard' },
]);
const authLinks = computed(() => [
  { name: t('nav.history'), path: '/history' },
  { name: t('nav.saved'), path: '/saved' },
]);

function handleLogout() {
  auth.logout();
  isMenuOpen.value = false;
  notifySuccess(t('notifications.logoutTitle'), t('notifications.logoutDescription'));
}

async function handleLanguageSwitch(targetLocale) {
  if (locale.locale === targetLocale) return;

  await locale.switchRouteLocale(targetLocale, route, router);

  if (auth.isAuthenticated) {
    try {
      await locale.syncPreference(auth.token);
      auth.setPreferredLocale(locale.locale);
      notifySuccess(t('language.savedTitle'), t('language.savedDescription'));
    } catch (error) {
      notifyError(t('language.syncFailedTitle'), error.message);
    }
  }

  if (analysis.hasResult) {
    try {
      await analysis.refreshAnalysis();
    } catch (error) {
      notifyError(t('notifications.refreshFailedTitle'), analysis.error || error.message);
    }
  }
}
</script>

<template>
  <nav class="sticky top-0 z-50 border-b border-primary/10 bg-white/85 backdrop-blur-xl">
    <div class="page-container">
      <div class="flex h-16 items-center justify-between md:h-20">
        <RouterLink :to="locale.path('/')" class="flex min-w-0 items-center gap-2 group" @click="isMenuOpen = false">
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
            :to="locale.path(link.path)"
            class="text-sm font-semibold text-gray-500 transition-colors hover:text-primary"
            active-class="text-primary"
          >
            {{ link.name }}
          </RouterLink>
          <template v-if="auth.isAuthenticated">
            <RouterLink
              v-for="link in authLinks"
              :key="link.path"
              :to="locale.path(link.path)"
              class="text-sm font-semibold text-gray-500 transition-colors hover:text-primary"
              active-class="text-primary"
            >
              {{ link.name }}
            </RouterLink>
          </template>
          <RouterLink :to="locale.path('/profile')" class="btn-primary px-5 py-2.5">
            <Sparkles class="h-4 w-4" />
            <span>{{ t('nav.getStarted') }}</span>
          </RouterLink>
          <button v-if="auth.isAuthenticated" class="btn-secondary px-4 py-2.5" @click="handleLogout">
            <LogOut class="h-4 w-4" />
            <span>{{ t('nav.logout') }}</span>
          </button>
          <div v-else class="flex items-center gap-2">
            <RouterLink :to="locale.path('/login')" class="btn-secondary px-4 py-2.5">{{ t('nav.login') }}</RouterLink>
            <RouterLink :to="locale.path('/signup')" class="btn-s-light px-4 py-2.5">{{ t('nav.signup') }}</RouterLink>
          </div>
          <div class="flex rounded-full border border-primary/10 bg-white p-1 shadow-sm" :aria-label="t('language.label')">
            <button
              class="rounded-full px-3 py-1 text-xs font-bold transition"
              :class="locale.locale === 'en' ? 'bg-primary text-white' : 'text-gray-500 hover:text-primary'"
              @click="handleLanguageSwitch('en')"
            >
              {{ t('language.english') }}
            </button>
            <button
              class="rounded-full px-3 py-1 text-xs font-bold transition"
              :class="locale.locale === 'id' ? 'bg-primary text-white' : 'text-gray-500 hover:text-primary'"
              @click="handleLanguageSwitch('id')"
            >
              {{ t('language.indonesia') }}
            </button>
          </div>
        </div>

        <button
          @click="isMenuOpen = !isMenuOpen"
          class="grid h-10 w-10 place-items-center rounded-2xl border border-primary/10 bg-white text-primary shadow-sm md:hidden"
          :aria-label="t('nav.toggle')"
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
            :to="locale.path(link.path)"
            @click="isMenuOpen = false"
            class="flex items-center justify-between rounded-2xl px-4 py-3 text-sm font-bold text-gray-600"
            active-class="bg-primary/10 text-primary"
          >
            {{ link.name }}
          </RouterLink>
          <template v-if="auth.isAuthenticated">
            <RouterLink
              v-for="link in authLinks"
              :key="link.path"
              :to="locale.path(link.path)"
              @click="isMenuOpen = false"
              class="flex items-center justify-between rounded-2xl px-4 py-3 text-sm font-bold text-gray-600"
              active-class="bg-primary/10 text-primary"
            >
              {{ link.name }}
            </RouterLink>
          </template>
          <RouterLink :to="locale.path('/profile')" @click="isMenuOpen = false" class="btn-primary mt-2 w-full">
            <Sparkles class="h-4 w-4" />
            <span>{{ t('nav.startAnalysis') }}</span>
          </RouterLink>
          <button v-if="auth.isAuthenticated" class="btn-secondary mt-2 w-full" @click="handleLogout">
            <LogOut class="h-4 w-4" />
            <span>{{ t('nav.logout') }}</span>
          </button>
          <div v-else class="grid grid-cols-2 gap-2 pt-2">
            <RouterLink :to="locale.path('/login')" @click="isMenuOpen = false" class="btn-secondary w-full">{{ t('nav.login') }}</RouterLink>
            <RouterLink :to="locale.path('/signup')" @click="isMenuOpen = false" class="btn-s-light w-full">{{ t('nav.signup') }}</RouterLink>
          </div>
          <div class="grid grid-cols-2 gap-2 pt-2">
            <button
              class="rounded-full border border-primary/10 px-4 py-2 text-sm font-bold"
              :class="locale.locale === 'en' ? 'bg-primary text-white' : 'bg-white text-gray-500'"
              @click="handleLanguageSwitch('en')"
            >
              {{ t('language.english') }}
            </button>
            <button
              class="rounded-full border border-primary/10 px-4 py-2 text-sm font-bold"
              :class="locale.locale === 'id' ? 'bg-primary text-white' : 'bg-white text-gray-500'"
              @click="handleLanguageSwitch('id')"
            >
              {{ t('language.indonesia') }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>
