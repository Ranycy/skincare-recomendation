import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { getCurrentUser, loginUser, registerUser } from "../services/api";

const AUTH_TOKEN_KEY = "skinsense_auth_token";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem(AUTH_TOKEN_KEY) || "");
  const user = ref(null);
  const isLoading = ref(false);
  const error = ref("");

  const isAuthenticated = computed(() => Boolean(token.value && user.value));

  function setSession(authData) {
    token.value = authData.token;
    user.value = {
      user_id: authData.user_id,
      email: authData.email,
      name: authData.name,
      is_guest: false,
    };
    localStorage.setItem(AUTH_TOKEN_KEY, authData.token);
  }

  async function login(credentials) {
    error.value = "";
    isLoading.value = true;

    try {
      const result = await loginUser(credentials);
      setSession(result);
      return result;
    } catch (loginError) {
      error.value = loginError.message || "Gagal masuk. Coba lagi.";
      throw loginError;
    } finally {
      isLoading.value = false;
    }
  }

  async function signup(payload) {
    error.value = "";
    isLoading.value = true;

    try {
      const result = await registerUser(payload);
      setSession(result);
      return result;
    } catch (signupError) {
      error.value = signupError.message || "Daftar gagal. Coba lagi.";
      throw signupError;
    } finally {
      isLoading.value = false;
    }
  }

  async function hydrate() {
    if (!token.value || user.value || isLoading.value) {
      return user.value;
    }

    isLoading.value = true;
    try {
      user.value = await getCurrentUser(token.value);
      return user.value;
    } catch (hydrateError) {
      logout();
      throw hydrateError;
    } finally {
      isLoading.value = false;
    }
  }

  function logout() {
    token.value = "";
    user.value = null;
    error.value = "";
    localStorage.removeItem(AUTH_TOKEN_KEY);
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    signup,
    hydrate,
    logout,
  };
});
