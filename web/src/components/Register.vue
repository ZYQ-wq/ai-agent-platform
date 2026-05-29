<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2 class="title">用户注册</h2>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>

        <div class="form-group">
          <label>电子邮箱</label>
          <input v-model="form.email" type="email" placeholder="example@domain.com" required />
        </div>

        <div class="form-group">
          <label>设置密码</label>
          <input v-model="form.password" type="password" placeholder="至少6位字符" required minlength="6" />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '注册中...' : '注 册' }}
        </button>
      </form>

      <div class="switch-link">
        <span>已有账号？</span>
        <router-link to="/login" class="link-text">去登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
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
    async handleRegister() {
      this.error = '';
      this.loading = true;

      try {
        await axios.post('/api/v1/user/register', this.form);
        alert('注册成功！请登录');
        // 注册成功后跳转到登录页
        this.$router.push('/login');
        
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.detail || '注册失败，请稍后重试';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* 样式与 Login.vue 保持一致 */
.auth-container { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; }
.auth-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
.title { margin-bottom: 30px; color: #333; }
.auth-form .form-group { margin-bottom: 20px; text-align: left; }
.auth-form label { display: block; margin-bottom: 8px; font-weight: 500; color: #555; font-size: 14px; }
.auth-form input { width: 100%; padding: 10px 12px; border: 1px solid #d9d9d9; border-radius: 4px; box-sizing: border-box; }
.auth-form input:focus { border-color: #52c41a; outline: none; box-shadow: 0 0 0 2px rgba(82, 196, 26, 0.2); }
.submit-btn { width: 100%; padding: 12px; background-color: #52c41a; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; transition: background-color 0.3s; }
.submit-btn:hover:not(:disabled) { background-color: #73d13d; }
.submit-btn:disabled { background-color: #b7eb8f; cursor: not-allowed; }
.error-msg { color: #ff4d4f; margin-bottom: 15px; font-size: 14px; background: #fff1f0; padding: 8px; border-radius: 4px; border: 1px solid #ffa39e; }
.switch-link { margin-top: 20px; font-size: 14px; color: #666; }
.link-text { color: #1890ff; text-decoration: none; margin-left: 5px; font-weight: 500; }
</style>