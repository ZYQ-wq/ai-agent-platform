<template>
  <div class="auth-container">
    <h2>登录</h2>

    <input
      v-model="email"
      placeholder="邮箱"
      type="email"
    />

    <input
      v-model="password"
      placeholder="密码"
      type="password"
    />

    <button @click="loginUser">
      登录
    </button>

    <p class="message">{{ message }}</p>

    <p>
      没有账号？
      <router-link to="/register">去注册</router-link>
    </p>
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
          password: password.value
        });

        // 保存 JWT token 到 localStorage
        localStorage.setItem("token", res.data.access_token);
        // 保存用户 email 方便前端显示或其他用途
        localStorage.setItem("email", email.value);

        // 跳转到聊天页面
        router.push("/chat");
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
      loginUser
    };
  }
});
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
}

input {
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
}

button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

.message {
  color: red;
  margin-top: 10px;
}
</style>