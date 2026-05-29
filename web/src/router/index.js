import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Chat from '../components/Chat.vue' // ✅ 引入 Chat 组件

const routes = [
  { path: '/', redirect: '/login' }, 
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  // ✅ 添加 Chat 路由，并设置 meta.requiresAuth = true
  { 
    path: '/chat', 
    name: 'Chat', 
    component: Chat, 
    meta: { requiresAuth: true } 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  
  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    next('/login'); 
  } else {
    next(); 
  }
});

export default router