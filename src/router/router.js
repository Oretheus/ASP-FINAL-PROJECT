import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import CandidatePage1 from "@/components/CandidatePage1.vue";
import CandidatePage2 from "@/components/CandidatePage2.vue";

const routes = [
  {
    path: "/",
    name: "Register",
    component: Register,
  },
  {
    path: "/Login",
    name: "Login",
    component: Login,
  },
  {
    path: "/candidate1",
    name: "CandidatePage1",
    component: CandidatePage1,
  },
  {
    path: "/candidate2",
    name: "CandidatePage2",
    component: CandidatePage2,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
