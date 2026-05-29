```vue
<template>
  <div class="chat-container">

    <div class="top-bar">

      <h2>AI 聊天</h2>

      <button class="logout-btn" @click="logout">
        退出登录
      </button>

    </div>

    <div class="chat-box">

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="message"
      >
        <strong>{{ msg.role }}:</strong>
        {{ msg.content }}
      </div>

    </div>

    <input
      v-model="inputMessage"
      @keyup.enter="sendMessage"
      placeholder="输入消息..."
    />

    <button @click="sendMessage">
      发送
    </button>

  </div>
</template>

<script lang="ts">

import {
  defineComponent,
  ref,
  onMounted
} from "vue";

import axios from "axios";

import { useRouter } from "vue-router";

interface Message {
  role: string;
  content: string;
}

export default defineComponent({

  setup() {

    const router = useRouter();

    const messages = ref<Message[]>([]);

    const inputMessage = ref("");

    // 页面加载检查 token
    onMounted(() => {

      const token = localStorage.getItem("token");

      if (!token) {

        alert("请先登录");

        router.push("/login");
      }
    });

    const sendMessage = async () => {

      if (!inputMessage.value.trim()) return;

      const token = localStorage.getItem("token");

      // 没 token
      if (!token) {

        alert("登录已失效");

        router.push("/login");

        return;
      }

      // 添加用户消息
      messages.value.push({
        role: "你",
        content: inputMessage.value
      });

      try {

        const res = await axios.post(
          "http://127.0.0.1:8000/chat/",
          {
            message: inputMessage.value
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        messages.value.push({
          role: "AI",
          content: res.data.response
        });

      } catch (err: any) {

        console.error(err);

        // token失效
        if (err.response?.status === 401) {

          alert("登录已过期，请重新登录");

          localStorage.removeItem("token");

          localStorage.removeItem("email");

          router.push("/login");

          return;
        }

        messages.value.push({
          role: "AI",
          content: "发送失败"
        });
      }

      inputMessage.value = "";
    };

    // 退出登录
    const logout = () => {

      localStorage.removeItem("token");

      localStorage.removeItem("email");

      router.push("/login");
    };

    return {
      messages,
      inputMessage,
      sendMessage,
      logout
    };
  }
});
</script>

<style scoped>

.chat-container {
  max-width: 700px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logout-btn {
  background: red;
  color: white;
}

.chat-box {
  border: 1px solid #ccc;
  min-height: 400px;
  padding: 10px;
  margin: 20px 0;
  overflow-y: auto;
}

.message {
  margin-bottom: 10px;
}

input {
  padding: 10px;
  font-size: 16px;
  margin-bottom: 10px;
}

button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

</style>
```
