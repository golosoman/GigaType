// stores/userStore.ts
import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import Cookies from "js-cookie"; // Импортируем библиотеку js-cookie

export const useUser = defineStore("user", () => {
  const token = ref<string | null>(null);
  const login = ref<string | null>(null);

  const setAuth = (tokenValue: string, loginValue: string) => {
    token.value = tokenValue;
    login.value = loginValue;
    // Устанавливаем куку с помощью js-cookie
    Cookies.set("auth", tokenValue, { path: "/", secure: true });
  };

  const clearAuth = () => {
    token.value = null;
    login.value = null;
    // Удаляем куку с помощью js-cookie
    Cookies.remove("auth", { path: "/" });
  };

  const register = async (userData: { login: string; password: string }) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/user/register",
        userData,
        { withCredentials: true }
      );
      // Куки автоматически сохраняются в браузере, если сервер их устанавливает
      // Здесь не нужно извлекать куки из заголовков
      const authCookie = Cookies.get("auth"); // Извлекаем куку auth
      if (authCookie) {
        setAuth(authCookie, userData.login); // Устанавливаем токен и логин
      }
    } catch (error) {
      console.error("Registration error:", error);
      throw error; // Обработка ошибки, если необходимо
    }
  };

  const loginUser = async (userData: { login: string; password: string }) => {
    try {
      const response = await axios.post(
        "/api/user/login",
        userData,
        { withCredentials: true }
      );
      console.log(response);
      // Куки автоматически сохраняются в браузере, если сервер их устанавливает
      const authCookie = Cookies.get("auth"); // Извлекаем куку auth
      console.log(authCookie);
      if (authCookie) {
        setAuth(authCookie, userData.login); // Устанавливаем токен и логин
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error; // Обработка ошибки, если необходимо
    }
  };

  const logout = () => {
    clearAuth();
  };

  return {
    token,
    login,
    register,
    loginUser,
    logout,
  };
});
