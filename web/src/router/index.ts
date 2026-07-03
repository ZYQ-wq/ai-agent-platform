import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw
} from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Chat from "../views/Chat.vue";
import Agents from "../views/Agents.vue";
import AgentStudio from "../views/AgentStudio.vue";
import WorkflowStudio from "../views/WorkflowStudio.vue";
import Plaza from "../views/Plaza.vue";
import WorkflowManagement from "../views/WorkflowManagement.vue";
import Knowledge from "../views/Knowledge.vue";
import KBUpload from "../views/KBUpload.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", redirect: "/plaza" },

  { path: "/plaza", component: Plaza, meta: { requiresAuth: true } },
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  { path: "/agents", component: Agents, meta: { requiresAuth: true } },
  { path: "/agents/studio", component: AgentStudio, meta: { requiresAuth: true } },

  { path: "/chat/:agentId", component: Chat, meta: { requiresAuth: true } },

  { path: "/workflow", component: WorkflowStudio, meta: { requiresAuth: true } },

  {
    path: "/workflow-management",
    component: WorkflowManagement,
    meta: { requiresAuth: true }
  },
  {
    path: "/kb",
    component: Knowledge,
    meta: { requiresAuth: true }
  },
  {
    path: "/kb/upload/:id",
    component: KBUpload,
    meta: { requiresAuth: true }
  },
  {
    path: "/kb/:id",
    redirect: (to) => `/kb/upload/${to.params.id}`
  },
  {
    path: "/coding",
    component: () => import("../views/coding/CodingIDE.vue"),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;