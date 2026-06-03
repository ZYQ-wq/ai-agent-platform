<template>
  <div class="auth-container">
    <div class="auth-card card">
      <h2>欢迎回来</h2>
      <p class="subtitle">登录到你的智能体平台</p>

      <input
        v-model="email"
        placeholder="电子邮箱"
        type="email"
      />

      <input
        v-model="password"
        placeholder="密码"
        type="password"
      />

      <button @click="loginUser" class="auth-btn">登录</button>

      <p v-if="message" class="message">{{ message }}</p>

      <p class="switch-link">
        没有账号？
        <router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const router = useRouter();

    const email = ref("");
    const password = ref("");
    const message = ref("");

    const loginUser = async () => {
      if (!email.value || !password.value) {
        message.value = "邮箱和密码不能为空";
        return;
      }

      try {
        const res = await axios.post("http://127.0.0.1:8000/users/login", {
          email: email.value,
          password: password.value,
        });

        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("email", email.value);

        router.push("/plaza");
      } catch (err: any) {
        if (err.response) {
          message.value = err.response.data.detail || "登录失败";
        } else {
          message.value = "网络错误或服务器未响应";
        }
      }
    };

    return {
      email,
      password,
      message,
      loginUser,
    };
  },
});
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