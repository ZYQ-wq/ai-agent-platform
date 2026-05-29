
import {
  createRouter,
  createWebHistory
} from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Chat from "../views/Chat.vue";
import Agents from "../views/Agents.vue";

const routes = [

  {
    path: "/",
    redirect: "/agents"
  },

  {
    path: "/login",
    component: Login
  },

  {
    path: "/register",
    component: Register
  },

  {
    path: "/agents",
    component: Agents,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/chat/:agentId",
    component: Chat,
    meta: {
      requiresAuth: true
    }
  }

];

const router = createRouter({
  history: createWebHistory(),
  routes
});


// 路由守卫
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("token");

  if (
    to.meta.requiresAuth &&
    !token
  ) {

    next("/login");

  } else {

    next();

  }

});

export default router;
