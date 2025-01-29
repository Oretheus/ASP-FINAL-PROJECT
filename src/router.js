import { createRouter, createWebHistory } from "vue-router";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import CandidatePage from '@/components/CandidatePage.vue'; //Added 23/01

// Altered paths as names were different, added meta tags so page title changes.//
// Added authentication for when we have the backend, not tested.

// Authentication function
const isAuthenticated = () => {
  return localStorage.getItem('loggedIn') === 'true'; // Check login status
};

const routes = [
  {
    path: '/',
    name: 'RegisterPage',
    component: RegisterPage,
    meta:{title:'Register'},
  },
  {
    path: '/Login',
    name: 'LoginPage',
    component: Login, 
    meta:{title:'Login'},
  },
  {
    path: '/Candidate',
    name: 'CandidatePage',
    component: CandidatePage,
    meta:{title:'Candidate 2'},
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next(); // Allow access
      } else {
        next('/'); // Redirect to registration if not logged in
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // Set the document title using the meta title, or default to 'App'
  document.title = to.meta.title || 'App';
  next();
});

export default router;
