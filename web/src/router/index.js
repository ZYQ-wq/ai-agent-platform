import {
  createRouter,
  createWebHistory
} from "vue-router";

import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import Chat from "../components/Chat.vue";

const routes = [

  {
    path: "/",
    redirect: "/login"
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
    path: "/chat",
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

  // 判断是否需要登录
  if (to.meta.requiresAuth) {

    const token = localStorage.getItem("token");

    // 没 token
    if (!token) {

      alert("请先登录");

      return next("/login");
    }
  }

  next();
});

export default router;