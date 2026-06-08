<template>
  <div class="page-container section-pad">
    <section class="mx-auto max-w-md soft-card p-5 sm:p-7">
      <div class="mb-7 space-y-2">
        <span class="badge">Buat akun</span>
        <h1 class="text-3xl font-bold tracking-tight text-p-d">Buat akun SkinSense</h1>
        <p class="text-sm leading-6 text-gray-600">
          Akun dipakai untuk menyimpan profil kulit, riwayat rekomendasi, dan produk favorit.
        </p>
      </div>

      <div class="space-y-4">
        <label class="block space-y-2">
          <span class="eyebrow">Nama</span>
          <input v-model="form.name" type="text" class="auth-input" placeholder="Nama kamu" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">Email</span>
          <input v-model="form.email" type="email" class="auth-input" placeholder="nama@email.com" />
        </label>
        <label class="block space-y-2">
          <span class="eyebrow">Password</span>
          <div class="relative">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="auth-input pr-12" placeholder="Minimal 6 karakter" />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" @click="showPassword = !showPassword">
              <EyeOff v-if="showPassword" class="h-5 w-5" />
              <Eye v-else class="h-5 w-5" />
            </button>
          </div>
        </label>

        <button :disabled="!canSubmit || auth.isLoading" class="btn-primary min-h-12 w-full" @click="handleSignup">
          <LoaderCircle v-if="auth.isLoading" class="h-5 w-5 animate-spin" />
          <UserPlus v-else class="h-5 w-5" />
          <span>{{ auth.isLoading ? 'Membuat akun...' : 'Daftar' }}</span>
        </button>

        <p v-if="auth.error" class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {{ auth.error }}
        </p>
      </div>

      <p class="mt-6 text-center text-sm text-gray-500">
        Sudah punya akun?
        <RouterLink to="/login" class="font-bold text-primary">Login</RouterLink>
      </p>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { Eye, EyeOff, LoaderCircle, UserPlus } from "lucide-vue-next";
import { useAuthStore } from "../stores/useAuthStore";
import { notifyError, notifySuccess } from "../utils/notifications";

const router = useRouter();
const auth = useAuthStore();
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
    });
    notifySuccess("Akun dibuat", "Sekarang kamu bisa menyimpan profil dan produk favorit.");
    router.push("/profile");
  } catch (error) {
    notifyError("Daftar gagal", auth.error || error.message);
  }
}
</script>
