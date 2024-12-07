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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/test",
      name: "test",
      component: c,
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
      path: "/app/edit/level",
      name: "edit_level",
      component: LevelEditorView,
    },
    {
      path: "/app/edit/user",
      name: "edit_user",
      component: UserEditorView,
    },
    {
      path: "/app/edit/exercise",
      name: "edit_exercise",
      component: ExerciseEditorView,
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
