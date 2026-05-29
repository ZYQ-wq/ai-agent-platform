
<template>
  <div class="chat-container">

    <h2>Agent聊天</h2>

    <div class="chat-box">

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
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
import { defineComponent } from "vue";
import { ref } from "vue";

import axios from "axios";

import { useRoute } from "vue-router";

interface Message {

  role: string;

  content: string;

}

export default defineComponent({

  setup() {

    const route = useRoute();

    const agentId = route.params.agentId;

    const messages = ref<Message[]>([]);

    const inputMessage = ref("");

    const sendMessage = async () => {

      if (!inputMessage.value.trim()) return;

      const token = localStorage.getItem("token");

      if (!token) {

        alert("请先登录");

        return;

      }

      // 用户消息
      messages.value.push({
        role: "你",
        content: inputMessage.value
      });

      try {

        const res = await axios.post(
          `http://127.0.0.1:8000/chat/${agentId}`,
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

        inputMessage.value = "";

      } catch (err) {

        messages.value.push({
          role: "AI",
          content: "发送失败"
        });

      }

    };

    return {
      messages,
      inputMessage,
      sendMessage
    };

  }

});
</script>

<style scoped>

.chat-container {
  max-width: 700px;
  margin: 40px auto;
}

.chat-box {
  border: 1px solid #ccc;
  min-height: 400px;
  padding: 20px;
  margin-bottom: 20px;
  overflow-y: auto;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

button {
  padding: 10px;
  cursor: pointer;
}

</style>

