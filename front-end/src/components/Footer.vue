<template>
  <footer class="mt-8 border-t border-primary/10 bg-primary-dark text-white">
    <div class="page-container py-8 sm:py-10">
      <div class="grid gap-6 md:grid-cols-[1fr_auto] md:items-center">
        <div class="space-y-2">
          <div class="flex items-center gap-2">
            <span class="grid h-9 w-9 place-items-center rounded-2xl bg-white/10">
              <Leaf class="h-4 w-4 text-primary-light" />
            </span>
            <span class="text-xl font-display font-bold tracking-tight">SkinSense AI</span>
          </div>
          <p class="max-w-sm text-sm leading-relaxed text-primary-light/85">
            {{ t('footer.description') }}
          </p>
        </div>

        <div class="flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold text-primary-light/85">
          <a href="#" class="transition-colors hover:text-white">{{ t('footer.privacy') }}</a>
          <a href="#" class="transition-colors hover:text-white">{{ t('footer.terms') }}</a>
          <a href="#" class="transition-colors hover:text-white">{{ t('footer.contact') }}</a>
        </div>
      </div>

      <p class="mt-7 text-xs text-primary-light/60">
        {{ t('footer.copyright') }}
      </p>
    </div>
  </footer>
</template>

<script setup>
import { Leaf } from 'lucide-vue-next';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>
