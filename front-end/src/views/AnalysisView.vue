<template>
  <div class="page-container section-pad">
    <div class="mx-auto max-w-3xl">
      <div class="mb-6 space-y-3">
        <span class="badge">{{ t('analysis.badge') }}</span>
        <div class="space-y-2">
          <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">{{ t('analysis.title') }}</h1>
          <p class="text-sm leading-6 text-gray-600 sm:text-base">
            {{ t('analysis.description') }}
          </p>
        </div>
      </div>

      <section class="soft-card p-4 sm:p-6 lg:p-8">
        <div class="space-y-8">
          <div class="space-y-3">
            <div class="flex items-center justify-between gap-3">
              <label class="eyebrow">{{ t('analysis.skinType') }}</label>
              <span class="text-xs font-semibold text-gray-400">{{ t('analysis.required') }}</span>
            </div>
            <div class="grid grid-cols-2 gap-3 sm:grid-cols-5">
              <button
                v-for="type in skinTypes"
                :key="type"
                @click="form.skinType = type"
                :class="['field-chip min-h-12', form.skinType === type ? 'field-chip-active' : '']"
              >
                {{ type }}
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <label class="eyebrow">{{ t('analysis.concerns') }}</label>
            <div class="flex flex-wrap gap-2.5">
              <button
                v-for="concern in concerns"
                :key="concern"
                @click="toggleConcern(concern)"
                :class="[
                  'field-chip inline-flex min-h-11 items-center gap-2 rounded-full px-4 py-2',
                  form.concerns.includes(concern) ? 'field-chip-active' : ''
                ]"
              >
                <Check v-if="form.concerns.includes(concern)" class="h-4 w-4" />
                <span>{{ concern }}</span>
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between gap-3">
              <label class="eyebrow">{{ t('analysis.productCategory') }}</label>
              <span class="text-xs font-semibold text-gray-400">{{ t('analysis.chooseOne') }}</span>
            </div>
            <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
              <button
                v-for="prod in productCategories"
                :key="prod"
                @click="form.productCategory = prod"
                :class="[
                  'field-chip flex min-h-14 items-center justify-center gap-2 text-center',
                  form.productCategory === prod ? 'field-chip-active' : ''
                ]"
              >
                <Check v-if="form.productCategory === prod" class="h-4 w-4 shrink-0" />
                <span>{{ prod }}</span>
              </button>
            </div>
          </div>

          <div v-if="isSunscreenCategory(form.productCategory)" class="rounded-3xl border border-primary/10 bg-accent-pink/45 p-4 sm:p-5">
            <div class="mb-4 space-y-1">
              <label class="eyebrow text-primary-dark">{{ t('analysis.activity') }}</label>
              <p class="text-sm leading-6 text-gray-600">{{ t('analysis.activityDescription') }}</p>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="activity in activities"
                :key="activity"
                @click="form.activity = activity"
                :class="['field-chip min-h-12', form.activity === activity ? 'field-chip-active' : '']"
              >
                {{ activity }}
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <label class="eyebrow">{{ t('analysis.avoidedIngredients') }}</label>
            <div class="flex flex-wrap gap-2.5">
              <button
                v-for="ing in avoidOptions"
                :key="ing"
                @click="toggleAvoid(ing)"
                :class="[
                  'field-chip inline-flex min-h-10 items-center gap-2 rounded-full px-4 py-2 text-xs',
                  form.avoidIngredients.includes(ing) ? 'border-red-200 bg-red-50 text-red-700 ring-2 ring-red-100' : ''
                ]"
              >
                <Check v-if="form.avoidIngredients.includes(ing)" class="h-3.5 w-3.5" />
                <span>{{ ing }}</span>
              </button>
            </div>
            <input
              type="text"
              v-model="form.customAvoidIngredients"
              :placeholder="t('analysis.customPlaceholder')"
              class="min-h-12 w-full rounded-2xl border border-primary/10 bg-white px-4 text-sm text-gray-700 shadow-sm outline-none transition focus:border-primary/30 focus:ring-4 focus:ring-primary/10"
            />
          </div>
        </div>

        <div class="sticky bottom-3 z-10 mt-8 rounded-3xl border border-white/70 bg-white/90 p-3 shadow-[0_18px_40px_rgba(45,62,39,0.14)] backdrop-blur-xl sm:static sm:border-0 sm:bg-transparent sm:p-0 sm:shadow-none">
          <label v-if="auth.isAuthenticated" class="mb-3 flex items-start gap-3 rounded-2xl bg-primary/5 px-4 py-3 text-sm font-semibold text-primary-dark">
            <input v-model="saveProfile" type="checkbox" class="mt-1 h-4 w-4 accent-primary" />
            <span>{{ t('analysis.saveProfile') }}</span>
          </label>
          <div v-else class="mb-3 rounded-2xl bg-accent-pink/55 px-4 py-3 text-sm font-semibold text-s-d">
            {{ t('analysis.guestPrompt') }}
          </div>

          <button
            @click="handleSubmit"
            :disabled="!form.skinType || !form.productCategory || store.isLoading"
            class="btn-primary min-h-14 w-full text-base"
          >
            <LoaderCircle v-if="store.isLoading" class="h-5 w-5 animate-spin" />
            <Leaf v-else class="h-5 w-5" />
            <span>{{ store.isLoading ? t('analysis.loading') : t('analysis.submit') }}</span>
          </button>

          <div v-if="store.error" class="mt-3 rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
            {{ store.error }}
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Check, Leaf, LoaderCircle } from 'lucide-vue-next';
import { useAnalysisStore } from '../stores/useAnalysisStore';
import { useAuthStore } from '../stores/useAuthStore';
import { useLocaleStore } from '../stores/useLocaleStore';
import { getAnalysisOptions, isSunscreenCategory, mapBackendProfileToForm, normalizeAnalysisForm } from '../utils/analysisMapping';
import { notifyError, notifySuccess } from '../utils/notifications';

const router = useRouter();
const store = useAnalysisStore();
const auth = useAuthStore();
const locale = useLocaleStore();
const { t } = useI18n();
const saveProfile = ref(true);

const options = computed(() => getAnalysisOptions(locale.locale));
const skinTypes = computed(() => options.value.skinTypes);
const concerns = computed(() => options.value.concerns);
const productCategories = computed(() => options.value.productCategories);
const avoidOptions = computed(() => options.value.avoidOptions);
const activities = computed(() => options.value.activities);

const form = reactive({
  skinType: '',
  concerns: [],
  productCategory: '',
  activity: locale.locale === 'id' ? 'Dalam ruangan' : 'Indoor',
  avoidIngredients: [],
  customAvoidIngredients: '',
});

function applyFormValues(values) {
  if (!values) return;

  form.skinType = values.skinType || '';
  form.concerns = [...(values.concerns || [])];
  form.productCategory = values.productCategory || '';
  form.activity = values.activity || 'Indoor';
  form.avoidIngredients = [...(values.avoidIngredients || [])];
  form.customAvoidIngredients = values.customAvoidIngredients || '';
}

watch(
  () => locale.locale,
  (newLocale) => {
    try {
      const normalized = normalizeAnalysisForm(form);
      const translatedForm = mapBackendProfileToForm({
        skin_type: normalized.questionnaire.skin_type,
        skin_concerns: normalized.questionnaire.skin_concerns,
        avoided_ingredients: normalized.questionnaire.avoided_ingredients,
        default_product_category: normalized.questionnaire.product_category,
        default_activity_type: normalized.questionnaire.activity_type || 'indoor',
      }, newLocale);
      applyFormValues(translatedForm);
    } catch (error) {
      form.activity = newLocale === 'id' ? 'Dalam ruangan' : 'Indoor';
    }
  },
);

onMounted(async () => {
  if (!auth.isAuthenticated) return;

  try {
    const savedForm = await store.loadSavedSkinProfile();
    applyFormValues(savedForm);
  } catch (error) {
    notifyError(t('analysis.errorLoadProfileTitle'), error.message);
  }
});

const toggleConcern = (concern) => {
  const index = form.concerns.indexOf(concern);
  if (index === -1) {
    form.concerns.push(concern);
  } else {
    form.concerns.splice(index, 1);
  }
};

const toggleAvoid = (ingredient) => {
  const index = form.avoidIngredients.indexOf(ingredient);
  if (index === -1) {
    form.avoidIngredients.push(ingredient);
  } else {
    form.avoidIngredients.splice(index, 1);
  }
};

const handleSubmit = async () => {
  if (!form.skinType || !form.productCategory || store.isLoading) return;

  try {
    await store.submitAnalysis(form);
    if (auth.isAuthenticated && saveProfile.value) {
      await store.saveSkinProfile(form);
    }
    notifySuccess(t('analysis.successTitle'), t('analysis.successDescription'));
    router.push(locale.path('/dashboard'));
  } catch (error) {
    notifyError(t('analysis.failedTitle'), store.error || error.message);
  }
};
</script>
