<template>
  <div class="auth-container">
    <div class="auth-card card">
      <h2>创建账号</h2>
      <p class="subtitle">开始你的智能体之旅</p>

      <input v-model="username" placeholder="用户名" />
      <input v-model="email" placeholder="电子邮箱" type="email" />
      <input v-model="password" placeholder="密码" type="password" />

      <button @click="registerUser" class="auth-btn">注册</button>

      <p v-if="message" class="message">{{ message }}</p>

      <p class="switch-link">
        已有账号？
        <router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      message: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post("http://127.0.0.1:8000/users/register", {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.message = "注册成功！请登录。";
        this.$router.push("/login");
      } catch (err) {
        this.message = err.response.data.detail || "注册失败";
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  text-align: center;
}

h2 {
  margin-bottom: 8px;
}

.subtitle {
  color: var(--text);
  margin-bottom: 24px;
  font-size: 14px;
}

input {
  width: 100%;
  margin-bottom: 16px;
}

.auth-btn {
  width: 100%;
  margin-top: 8px;
  padding: 12px;
  font-size: 16px;
}

.message {
  margin-top: 16px;
  color: #e5484d;
  font-size: 14px;
}

.switch-link {
  margin-top: 24px;
  font-size: 14px;
}

a {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
}
a:hover {
  text-decoration: underline;
}
</style>