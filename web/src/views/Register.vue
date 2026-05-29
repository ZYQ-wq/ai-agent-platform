<template>
  <div>
    <h2>注册</h2>
    <input v-model="username" placeholder="用户名" />
    <input v-model="email" placeholder="邮箱" />
    <input v-model="password" placeholder="密码" type="password" />
    <button @click="registerUser">注册</button>
    <p>{{ message }}</p>
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
      message: ""
    };
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post("http://127.0.0.1:8000/users/register", {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.message = "注册成功！请登录。";
        this.$router.push("/login");
      } catch (err) {
        this.message = err.response.data.detail || "注册失败";
      }
    }
  }
};
</script>