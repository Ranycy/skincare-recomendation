<template>
  <div class="page-container section-pad">
    <section class="mx-auto max-w-md soft-card p-5 sm:p-7">
      <div class="mb-7 space-y-2">
        <span class="badge">{{ t('auth.loginBadge') }}</span>
        <h1 class="text-3xl font-bold tracking-tight text-p-d">{{ t('auth.loginTitle') }}</h1>
        <p class="text-sm leading-6 text-gray-600">
          {{ t('auth.loginDescription') }}
        </p>
      </div>

      <div class="space-y-4">
        <label class="block space-y-2">
          <span class="eyebrow">{{ t('auth.email') }}</span>
          <input v-model="form.email" type="email" class="auth-input" :placeholder="t('auth.emailPlaceholder')" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">{{ t('auth.password') }}</span>
          <div class="relative">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="auth-input pr-12" :placeholder="t('auth.passwordPlaceholder')" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" @click="showPassword = !showPassword">
              <EyeOff v-if="showPassword" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
            </button>
          </div>
        </label>

        <button :disabled="!canSubmit || isSubmitting" class="btn-primary min-h-12 w-full" @click="handleLogin">
          <LoaderCircle v-if="isSubmitting" class="h-5 w-5 animate-spin" />
          <LogIn v-else class="h-5 w-5" />
          <span>{{ isSubmitting ? t('auth.loginLoading') : t('auth.loginButton') }}</span>
        </button>

        <p v-if="auth.error" class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ auth.error }}
        </p>
      </div>

      <p class="mt-6 text-center text-sm text-gray-500">
        {{ t('auth.noAccount') }}
        <RouterLink :to="locale.path('/signup')" class="font-bold text-primary">{{ t('auth.signupLink') }}</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { Eye, EyeOff, LoaderCircle, LogIn } from "lucide-vue-next";
import { useAuthStore } from "../stores/useAuthStore";
import { useAnalysisStore } from "../stores/useAnalysisStore";
import { useLocaleStore } from "../stores/useLocaleStore";
import { notifyError, notifySuccess } from "../utils/notifications";

const router = useRouter();
const auth = useAuthStore();
const analysis = useAnalysisStore();
const locale = useLocaleStore();
const { t } = useI18n();
const showPassword = ref(false);
const form = reactive({
  email: "",
  password: "",
});

const isSubmitting = computed(() => auth.isLoading || analysis.isLoading);
const canSubmit = computed(() => form.email.trim() && form.password.length >= 6);

async function handleLogin() {
  if (!canSubmit.value || isSubmitting.value) return;

  try {
    await auth.login({
      email: form.email,
      password: form.password,
    });
  } catch (error) {
    notifyError(t("notifications.loginFailedTitle"), auth.error || error.message);
    return;
  }

  try {
    await locale.syncPreference(auth.token);
    auth.setPreferredLocale(locale.locale);
  } catch (error) {
    notifyError(t("language.syncFailedTitle"), error.message);
  }

  try {
    const savedForm = await analysis.loadSavedSkinProfile();
    if (!savedForm) {
      notifySuccess(t("notifications.loginSuccessTitle"), t("notifications.loginNeedsProfile"));
      router.push(locale.path("/profile"));
      return;
    }

    try {
      await analysis.submitAnalysis(savedForm);
      notifySuccess(t("notifications.loginSuccessTitle"), t("notifications.loginReady"));
      router.push(locale.path("/dashboard"));
    } catch (analysisError) {
      notifyError(t("notifications.savedProfileFoundTitle"), analysis.error || analysisError.message);
      router.push(locale.path("/profile"));
    }
  } catch (error) {
    notifyError(t("notifications.savedProfileLoadFailedTitle"), error.message);
    router.push(locale.path("/profile"));
  }
}
</script>
