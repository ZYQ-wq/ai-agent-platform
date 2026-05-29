<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="title">系统登录</h2>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>

        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="请输入邮箱" required />
        </div>

        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>

      <div class="switch-link">
        <span>还没有账号？</span>
        <router-link to="/register" class="link-text">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      loading: false,
      error: '',
      form: {
        username: '',
        email: '',
        password: ''
      }
    };
  },
  methods: {
    async handleLogin() {
      this.error = '';
      this.loading = true;
      
      try {
        // 发送登录请求 (确保你的 vite.config.ts 里配置了 /api 代理)
        const response = await axios.post('/api/v1/user/login', this.form);
        
        // ✅ 核心步骤1：先保存 Token
        const token = response.data.access_token;
        localStorage.setItem('access_token', token);
        
        // ✅ 核心步骤2：提示成功后，再执行路由跳转
        alert('登录成功！');
        // 这里可以改成你想要的主页路径，比如 '/chat'
        this.$router.push('/chat'); 
        
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.detail || '登录失败，请检查网络或账号信息';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.auth-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}
.title { margin-bottom: 30px; color: #333; }
.auth-form .form-group { margin-bottom: 20px; text-align: left; }
.auth-form label { display: block; margin-bottom: 8px; font-weight: 500; color: #555; font-size: 14px; }
.auth-form input { width: 100%; padding: 10px 12px; border: 1px solid #d9d9d9; border-radius: 4px; box-sizing: border-box; }
.auth-form input:focus { border-color: #1890ff; outline: none; box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2); }
.submit-btn { width: 100%; padding: 12px; background-color: #1890ff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; transition: background-color 0.3s; }
.submit-btn:hover:not(:disabled) { background-color: #40a9ff; }
.submit-btn:disabled { background-color: #bae7ff; cursor: not-allowed; }
.error-msg { color: #ff4d4f; margin-bottom: 15px; font-size: 14px; background: #fff1f0; padding: 8px; border-radius: 4px; border: 1px solid #ffa39e; }
.switch-link { margin-top: 20px; font-size: 14px; color: #666; }
.link-text { color: #1890ff; text-decoration: none; margin-left: 5px; font-weight: 500; }
</style>