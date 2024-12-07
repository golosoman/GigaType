import { defineStore } from "pinia";
import axios from "axios";
import { ref, watch } from "vue";
import Cookies from "js-cookie";

export const useUser = defineStore("user", () => {
  const isAuth = ref<boolean>(localStorage.getItem("isAuth") === "true");
  const login = ref<string | null>(localStorage.getItem("login"));
  const role = ref<string | null>(localStorage.getItem("role"));

  const setAuth = (loginValue: string) => {
    isAuth.value = true;
    login.value = loginValue;

    // Устанавливаем роль в зависимости от логина
    if (loginValue === "admin") {
      role.value = "ADMIN";
    } else {
      role.value = "TRAINEE";
    }

    // Сохраняем состояние в localStorage
    localStorage.setItem("isAuth", "true");
    localStorage.setItem("login", loginValue);
    localStorage.setItem("role", role.value);
  };

  const clearAuth = () => {
    login.value = null;
    role.value = null;
    isAuth.value = false;
    Cookies.remove("auth", { path: "/auth" });

    // Очищаем состояние в localStorage
    localStorage.removeItem("isAuth");
    localStorage.removeItem("login");
    localStorage.removeItem("role");
  };

  const register = async (userData: { login: string; password: string }) => {
    try {
      const response = await axios.post("api/user/register", userData, {
        withCredentials: true,
      });
      if (response.status === 200) {
        setAuth(userData.login);
      }
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    }
  };

  const loginUser = async (userData: { login: string; password: string }) => {
    try {
      const response = await axios.post("/api/user/login", userData, {
        withCredentials: true,
      });
      if (response.status === 200) {
        setAuth(userData.login);
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = () => {
    clearAuth();
  };

  return {
    isAuth,
    login,
    role,
    register,
    loginUser,
    logout,
  };
});
