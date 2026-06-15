<template>
  <div class="page-container section-pad">
    <section class="mx-auto max-w-md soft-card p-5 sm:p-7">
      <div class="mb-7 space-y-2">
        <span class="badge">{{ t('auth.signupBadge') }}</span>
        <h1 class="text-3xl font-bold tracking-tight text-p-d">{{ t('auth.signupTitle') }}</h1>
        <p class="text-sm leading-6 text-gray-600">
          {{ t('auth.signupDescription') }}
        </p>
      </div>

      <div class="space-y-4">
        <label class="block space-y-2">
          <span class="eyebrow">{{ t('auth.name') }}</span>
          <input v-model="form.name" type="text" class="auth-input" :placeholder="t('auth.namePlaceholder')" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">{{ t('auth.email') }}</span>
          <input v-model="form.email" type="email" class="auth-input" :placeholder="t('auth.emailPlaceholder')" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">{{ t('auth.password') }}</span>
          <div class="relative">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="auth-input pr-12" :placeholder="t('auth.passwordSignupPlaceholder')" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" @click="showPassword = !showPassword">
              <EyeOff v-if="showPassword" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
            </button>
          </div>
        </label>

        <button :disabled="!canSubmit || auth.isLoading" class="btn-primary min-h-12 w-full" @click="handleSignup">
          <LoaderCircle v-if="auth.isLoading" class="h-5 w-5 animate-spin" />
          <UserPlus v-else class="h-5 w-5" />
          <span>{{ auth.isLoading ? t('auth.signupLoading') : t('auth.signupButton') }}</span>
        </button>

        <p v-if="auth.error" class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ auth.error }}
        </p>
      </div>

      <p class="mt-6 text-center text-sm text-gray-500">
        {{ t('auth.hasAccount') }}
        <RouterLink :to="locale.path('/login')" class="font-bold text-primary">{{ t('auth.loginLink') }}</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { Eye, EyeOff, LoaderCircle, UserPlus } from "lucide-vue-next";
import { useAuthStore } from "../stores/useAuthStore";
import { useLocaleStore } from "../stores/useLocaleStore";
import { notifyError, notifySuccess } from "../utils/notifications";

const router = useRouter();
const auth = useAuthStore();
const locale = useLocaleStore();
const { t } = useI18n();
const showPassword = ref(false);
const form = reactive({
  name: "",
  email: "",
  password: "",
});

const canSubmit = computed(() => form.name.trim() && form.email.trim() && form.password.length >= 6);

async function handleSignup() {
  if (!canSubmit.value || auth.isLoading) return;

  try {
    await auth.signup({
      name: form.name,
      email: form.email,
      password: form.password,
      preferred_locale: locale.locale,
    });
    auth.setPreferredLocale(locale.locale);
    notifySuccess(t("notifications.signupSuccessTitle"), t("notifications.signupSuccessDescription"));
    router.push(locale.path("/profile"));
  } catch (error) {
    notifyError(t("notifications.signupFailedTitle"), auth.error || error.message);
  }
}
</script>
