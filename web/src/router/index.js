
import {
  createRouter,
  createWebHistory
} from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Chat from "../views/Chat.vue";
import Agents from "../views/Agents.vue";
import AgentStudio from "../views/AgentStudio.vue";
import WorkflowStudio from "../views/WorkflowStudio.vue"
import Plaza from "../views/Plaza.vue"
import WorkflowManagement from "../views/WorkflowManagement.vue"

const routes = [

  {
    path: "/",
    redirect: "/plaza"
  },

  {
    path: "/plaza",
    component: Plaza,
    meta: {
      requiresAuth: true
    }
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
    path: "/agents/studio",
    component: AgentStudio,
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
  },
  
  {
    path: "/workflow",
    component: WorkflowStudio,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: "/workflow-management",
    component: WorkflowManagement,
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
