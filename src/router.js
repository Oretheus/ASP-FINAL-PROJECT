import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import CandidatePage from '@/components/CandidatePage.vue'; 


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
  {
    path: '/Candidate',
    name: 'CandidatePage',
    component: CandidatePage,
  
  ];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
