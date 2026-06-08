<template>
  <div class="page-container section-pad">
    <section class="mx-auto max-w-md soft-card p-5 sm:p-7">
      <div class="mb-7 space-y-2">
        <span class="badge">Selamat datang kembali</span>
        <h1 class="text-3xl font-bold tracking-tight text-p-d">Masuk ke SkinSense</h1>
        <p class="text-sm leading-6 text-gray-600">
          Simpan profil, lihat riwayat, dan lanjutkan rekomendasi dari perangkat mana pun.
        </p>
      </div>

      <div class="space-y-4">
        <label class="block space-y-2">
          <span class="eyebrow">Email</span>
          <input v-model="form.email" type="email" class="auth-input" placeholder="nama@email.com" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">Password</span>
          <div class="relative">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="auth-input pr-12" placeholder="Password kamu" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" @click="showPassword = !showPassword">
              <EyeOff v-if="showPassword" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
            </button>
          </div>
        </label>

        <button :disabled="!canSubmit || auth.isLoading" class="btn-primary min-h-12 w-full" @click="handleLogin">
          <LoaderCircle v-if="auth.isLoading" class="h-5 w-5 animate-spin" />
          <LogIn v-else class="h-5 w-5" />
          <span>{{ auth.isLoading ? 'Masuk...' : 'Masuk' }}</span>
        </button>

        <p v-if="auth.error" class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ auth.error }}
        </p>
      </div>

      <p class="mt-6 text-center text-sm text-gray-500">
        Belum punya akun?
        <RouterLink to="/signup" class="font-bold text-primary">Daftar</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { Eye, EyeOff, LoaderCircle, LogIn } from "lucide-vue-next";
import { useAuthStore } from "../stores/useAuthStore";
import { notifyError, notifySuccess } from "../utils/notifications";

const router = useRouter();
const auth = useAuthStore();
const showPassword = ref(false);
const form = reactive({
  email: "",
  password: "",
});

const canSubmit = computed(() => form.email.trim() && form.password.length >= 6);

async function handleLogin() {
  if (!canSubmit.value || auth.isLoading) return;

  try {
    await auth.login({
      email: form.email,
      password: form.password,
    });
    notifySuccess("Berhasil masuk", "Profil dan riwayat kamu siap dipakai.");
    router.push("/profile");
  } catch (error) {
    notifyError("Gagal masuk", auth.error || error.message);
  }
}
</script>
