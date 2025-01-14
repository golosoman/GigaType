import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";
import Cookies from "js-cookie";

export const useUser = defineStore("user", () => {
  const isAuth = ref<boolean>(localStorage.getItem("isAuth") === "true");
  const login = ref<string | null>(localStorage.getItem("login"));
  const role = ref<string | null>(localStorage.getItem("role"));
  const userId = ref<string | null>(localStorage.getItem("userId")); // Новое состояние для uid пользователя

  // Новые состояния для хранения uid уровня сложности и uid упражнения
  const selectedLevelId = ref<string | null>(
    localStorage.getItem("selectedLevelId")
  );
  const selectedTaskId = ref<string | null>(
    localStorage.getItem("selectedTaskId")
  );

  const setAuth = (loginValue: string, uid: string) => {
    isAuth.value = true;
    login.value = loginValue;

    // Устанавливаем роль в зависимости от логина
    role.value = loginValue.toLowerCase() === "admin" ? "ADMIN" : "TRAINEE";
    userId.value = uid; // Сохраняем uid пользователя

    // Сохраняем состояние в localStorage
    localStorage.setItem("isAuth", "true");
    localStorage.setItem("login", loginValue);
    localStorage.setItem("role", role.value);
    localStorage.setItem("userId", uid); // Сохраняем uid в localStorage
  };

  const clearAuth = () => {
    login.value = null;
    role.value = null;
    userId.value = null; // Очищаем uid
    isAuth.value = false;
    Cookies.remove("auth", { path: "/auth" });

    // Очищаем состояние в localStorage
    localStorage.removeItem("isAuth");
    localStorage.removeItem("login");
    localStorage.removeItem("role");
    localStorage.removeItem("userId"); // Очищаем uid из localStorage
  };

  const register = async (userData: { login: string; password: string }) => {
    try {
      const response = await axios.post("api/user/register", userData, {
        withCredentials: true,
      });
      if (response.status === 200) {
        const uid = response.data.uuid; // Предполагается, что uid возвращается в ответе
        setAuth(userData.login, uid);
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
        const uid = response.data.uuid; // Предполагается, что uid возвращается в ответе
        setAuth(userData.login, uid);
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      // Отправка запроса на сервер для выхода
      const response = await axios.post(
        "/api/user/logout",
        {},
        {
          withCredentials: true,
        }
      );
      if (response.status === 200) {
        clearAuth(); // Очищаем состояние после успешного выхода
      }
    } catch (error) {
      console.error("Logout error:", error);
      throw error;
    }
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
    userId, // Возвращаем uid пользователя
    selectedLevelId,
    selectedTaskId,
    register,
    loginUser,
    logout,
    selectExercise,
  };
});
