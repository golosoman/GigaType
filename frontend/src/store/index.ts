import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import Cookies from "js-cookie";

export const useUser = defineStore("user", () => {
  const isAuth = ref<boolean>(localStorage.getItem("isAuth") === "true");
  const login = ref<string | null>(localStorage.getItem("login"));
  const role = ref<string | null>(localStorage.getItem("role"));

  // Новые состояния для хранения uid уровня сложности и uid упражнения
  const selectedLevelId = ref<string | null>(
    localStorage.getItem("selectedLevelId")
  );
  const selectedTaskId = ref<string | null>(
    localStorage.getItem("selectedTaskId")
  );

  const setAuth = (loginValue: string) => {
    isAuth.value = true;
    login.value = loginValue;

    // Устанавливаем роль в зависимости от логина
    role.value = loginValue === "admin" ? "ADMIN" : "TRAINEE";

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

  // Новое действие для сохранения выбранного уровня сложности и упражнения
  const selectExercise = (levelId: string, taskId: string) => {
    selectedLevelId.value = levelId;
    selectedTaskId.value = taskId;

    // Сохраняем в localStorage
    localStorage.setItem("selectedLevelId", levelId);
    localStorage.setItem("selectedTaskId", taskId);
  };

  return {
    isAuth,
    login,
    role,
    selectedLevelId,
    selectedTaskId,
    register,
    loginUser,
    logout,
    selectExercise,
  };
});
