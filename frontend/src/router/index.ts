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
} from "@/views";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthView,
    },
    {
      path: "/app/trainer",
      name: "trainer",
      component: TrainerView,
    },
    {
      path: "/app/information/developer",
      name: "developer",
      component: AboutDevelopersView,
    },
    {
      path: "/app/information/system",
      name: "system",
      component: AboutSystemView,
    },
    {
      path: "/app/cabinet",
      name: "cabinet",
      component: CabinetView,
    },
    {
      path: "/app/cabinet/admin",
      name: "admin_cabinet",
      component: CabinetAdminView,
    },
    {
      path: "/app/choose_exercise",
      name: "choose_exercise",
      component: ChooseExerciseView,
    },
  ],
});

export default router;
