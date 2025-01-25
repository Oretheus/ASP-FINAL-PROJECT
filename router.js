import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";


const routes = [
    {
      path: '/',
      name: 'Register',
      component: Register, 
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login, 
    },
  ];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
