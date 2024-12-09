import { createRouter, createWebHistory } from "vue-router";
import {
  AboutDevelopersView,
  AboutSystemView,
  AuthView,
  HomeView,
  TrainerView,
  CabinetView,
  ChooseExerciseView,
  CabinetAdminView,
  LevelEditorView,
  UserEditorView,
  ExerciseEditorView,
} from "@/views";
import c from "@/store/c.vue";
import { useUser } from "@/store/index"; // Импортируем хранилище пользователей

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: false },
    },
    {
      path: "/test",
      name: "test",
      component: c, // Замените на ваш компонент
      meta: { requiresAuth: false },
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthView,
      meta: { requiresAuth: false },
    },
    {
      path: "/app/trainer",
      name: "trainer",
      component: TrainerView,
      meta: { requiresAuth: true, roles: ["TRAINEE", "ADMIN"] },
    },
    {
      path: "/app/information/developer",
      name: "developer",
      component: AboutDevelopersView,
      meta: { requiresAuth: true, roles: ["TRAINEE", "ADMIN"] },
    },
    {
      path: "/app/information/system",
      name: "system",
      component: AboutSystemView,
      meta: { requiresAuth: true, roles: ["TRAINEE", "ADMIN"] },
    },
    {
      path: "/app/cabinet/trainee",
      name: "cabinet",
      component: CabinetView,
      meta: { requiresAuth: true, roles: ["TRAINEE", "ADMIN"] },
    },
    {
      path: "/app/edit/level",
      name: "edit_level",
      component: LevelEditorView,
      meta: { requiresAuth: true, roles: ["ADMIN"] },
    },
    {
      path: "/app/edit/user",
      name: "edit_user",
      component: UserEditorView,
      meta: { requiresAuth: true, roles: ["ADMIN"] },
    },
    {
      path: "/app/edit/exercise",
      name: "edit_exercise",
      component: ExerciseEditorView,
      meta: { requiresAuth: true, roles: ["ADMIN"] },
    },
    {
      path: "/app/cabinet/admin",
      name: "admin_cabinet",
      component: CabinetAdminView,
      meta: { requiresAuth: true, roles: ["ADMIN"] },
    },
    {
      path: "/app/choose_exercise",
      name: "choose_exercise",
      component: ChooseExerciseView,
      meta: { requiresAuth: true, roles: ["TRAINEE", "ADMIN"] },
    },
  ],
});

// Навигационный охранник
router.beforeEach((to, from, next) => {
  const userStore = useUser();
  const isAuth = userStore.isAuth;
  const role = userStore.role;

  // Если маршрут требует аутентификации
  if (to.meta.requiresAuth) {
    if (!isAuth) {
      // Если пользователь не авторизован, перенаправляем на страницу авторизации
      next({ name: "auth" });
    } else if (Array.isArray(to.meta.roles) && !to.meta.roles.includes(role)) {
      // Если у пользователя нет прав доступа к маршруту
      next({ name: "home" }); // Или перенаправьте на другую страницу
    } else {
      next(); // Разрешаем доступ
    }
  } else {
    next(); // Разрешаем доступ к публичным маршрутам
  }
});

export default router;
