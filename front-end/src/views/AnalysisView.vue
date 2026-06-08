<template>
  <div class="page-container section-pad">
    <div class="mx-auto max-w-3xl">
      <div class="mb-6 space-y-3">
        <span class="badge">Profil kulit</span>
        <div class="space-y-2">
          <h1 class="text-4xl font-bold tracking-tight text-p-d sm:text-5xl">Profil kulit kamu</h1>
          <p class="text-sm leading-6 text-gray-600 sm:text-base">
            Jawaban ini dipakai untuk mengambil cuaca dari lokasi kamu dan mencocokkannya dengan rekomendasi produk.
          </p>
        </div>
      </div>

      <section class="soft-card p-4 sm:p-6 lg:p-8">
        <div class="space-y-8">
          <div class="space-y-3">
            <div class="flex items-center justify-between gap-3">
              <label class="eyebrow">Jenis kulit</label>
              <span class="text-xs font-semibold text-gray-400">Wajib</span>
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
            <label class="eyebrow">Masalah kulit</label>
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
              <label class="eyebrow">Produk yang dibutuhkan</label>
              <span class="text-xs font-semibold text-gray-400">Pilih satu</span>
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

          <div v-if="form.productCategory === 'Sunscreen'" class="rounded-3xl border border-primary/10 bg-accent-pink/45 p-4 sm:p-5">
            <div class="mb-4 space-y-1">
              <label class="eyebrow text-primary-dark">Aktivitas harian</label>
              <p class="text-sm leading-6 text-gray-600">Khusus sunscreen, aktivitas membantu mencocokkan proteksi yang paling pas.</p>
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
            <label class="eyebrow">Kandungan yang dihindari</label>
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
              placeholder="Contoh: Centella, Salicylic Acid"
              class="min-h-12 w-full rounded-2xl border border-primary/10 bg-white px-4 text-sm text-gray-700 shadow-sm outline-none transition focus:border-primary/30 focus:ring-4 focus:ring-primary/10"
            />
          </div>
        </div>

        <div class="sticky bottom-3 z-10 mt-8 rounded-3xl border border-white/70 bg-white/90 p-3 shadow-[0_18px_40px_rgba(45,62,39,0.14)] backdrop-blur-xl sm:static sm:border-0 sm:bg-transparent sm:p-0 sm:shadow-none">
          <label v-if="auth.isAuthenticated" class="mb-3 flex items-start gap-3 rounded-2xl bg-primary/5 px-4 py-3 text-sm font-semibold text-primary-dark">
            <input v-model="saveProfile" type="checkbox" class="mt-1 h-4 w-4 accent-primary" />
            <span>Simpan pilihan ini sebagai profil kulit utama saya.</span>
          </label>
          <div v-else class="mb-3 rounded-2xl bg-accent-pink/55 px-4 py-3 text-sm font-semibold text-s-d">
            Login untuk menyimpan profil kulit dan melihat riwayat rekomendasi.
          </div>

          <button
            @click="handleSubmit"
            :disabled="!form.skinType || !form.productCategory || store.isLoading"
            class="btn-primary min-h-14 w-full text-base"
          >
            <LoaderCircle v-if="store.isLoading" class="h-5 w-5 animate-spin" />
            <Leaf v-else class="h-5 w-5" />
            <span>{{ store.isLoading ? 'Menganalisis lokasi dan profil...' : 'Lihat rekomendasi saya' }}</span>
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
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { Check, Leaf, LoaderCircle } from 'lucide-vue-next';
import { useAnalysisStore } from '../stores/useAnalysisStore';
import { useAuthStore } from '../stores/useAuthStore';
import { notifyError, notifySuccess } from '../utils/notifications';

const router = useRouter();
const store = useAnalysisStore();
const auth = useAuthStore();
const saveProfile = ref(true);

const skinTypes = ['Normal', 'Kering', 'Berminyak', 'Kombinasi', 'Sensitif'];
const concerns = ['Jerawat', 'Kusam', 'Penuaan', 'Bekas jerawat', 'Dehidrasi'];
const productCategories = ['Cleanser', 'Moisturizer', 'Masker', 'Eye cream', 'Sunscreen'];
const avoidOptions = ['Alkohol', 'Fragrance', 'Paraben', 'Silikon', 'Sulfat'];
const activities = ['Indoor', 'Outdoor'];

const form = reactive({
  skinType: '',
  concerns: [],
  productCategory: '',
  activity: 'Indoor',
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

onMounted(async () => {
  if (!auth.isAuthenticated) return;

  try {
    const savedForm = await store.loadSavedSkinProfile();
    applyFormValues(savedForm);
  } catch (error) {
    notifyError('Profil tersimpan gagal dimuat', error.message);
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
    notifySuccess('Rekomendasi siap', 'Hasil sudah disesuaikan dengan profil dan cuaca saat ini.');
    router.push('/dashboard');
  } catch (error) {
    notifyError('Gagal mengambil rekomendasi', store.error || error.message);
  }
};
</script>
