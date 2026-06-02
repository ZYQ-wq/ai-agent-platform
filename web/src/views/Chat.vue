<template>
  <div class="chat-container">
    <h2>Agent 聊天</h2>

    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, idx) in messages" :key="idx" :class="msg.role.toLowerCase()">
        <strong>{{ msg.role }}:</strong> {{ msg.content }}
      </div>
    </div>

    <input
      v-model="inputMessage"
      @keyup.enter="sendMessage"
      placeholder="输入消息..."
    />
    <button @click="sendMessage">发送</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";

interface Message {
  role: string;
  content: string;
  tool_call_id?: string;
}

export default defineComponent({
  setup() {
    const route = useRoute();
    const messages = ref<Message[]>([]);
    const inputMessage = ref("");
    const chatBox = ref<HTMLDivElement | null>(null);

    const authHeader = () => ({
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    });

    const scrollToBottom = async () => {
      await nextTick();
      if (chatBox.value) {
        chatBox.value.scrollTop = chatBox.value.scrollHeight;
      }
    };

    const loadHistory = async () => {
      const agentId = route.params.agentId;
      try {
        const res = await axios.get(
          `http://127.0.0.1:8000/chat/history/${agentId}`,
          { headers: authHeader() }
        );
        messages.value = res.data;
        scrollToBottom();
      } catch (err) {
        console.error("加载聊天历史失败", err);
      }
    };

    const sendMessage = async () => {
      if (!inputMessage.value.trim()) return;

      const agentId = route.params.agentId;
      const userMsg: Message = { role: "你", content: inputMessage.value };
      messages.value.push(userMsg);
      scrollToBottom();

      try {
        const res = await axios.post(
          `http://127.0.0.1:8000/chat/${agentId}`,
          { message: inputMessage.value },
          { headers: authHeader() }
        );

        const aiMsg: Message = { role: "AI", content: res.data.response };
        messages.value.push(aiMsg);
        scrollToBottom();
      } catch (err: any) {
        messages.value.push({ role: "AI", content: "发送失败" });
        scrollToBottom();
      }

      inputMessage.value = "";
    };

    onMounted(() => {
      loadHistory();
    });

    return {
      messages,
      inputMessage,
      sendMessage,
      chatBox,
    };
  },
});
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 50px auto;
  display: flex;
  flex-direction: column;
}

.chat-box {
  border: 1px solid #ccc;
  min-height: 300px;
  padding: 10px;
  margin-bottom: 10px;
  overflow-y: auto;
}

.chat-box .你 {
  color: blue;
  margin-bottom: 5px;
}

.chat-box .ai {
  color: green;
  margin-bottom: 5px;
}

input {
  padding: 8px;
  font-size: 16px;
  margin-bottom: 10px;
}

button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>