<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>智能体聊天</h2>
      <router-link to="/agents/studio" class="back-link">← 返回工作室</router-link>
    </div>

    <div class="chat-box" ref="chatBox">
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['message', msg.role === 'user' ? 'user' : 'ai']"
      >
        <div class="message-avatar">
          {{ msg.role === 'user' ? '👤' : '🤖' }}
        </div>
        <div class="message-content">
          <div class="message-text">
            {{ msg.content }}
            <span
              v-if="isGenerating && idx === messages.length - 1 && msg.role !== 'user'"
              class="typing-cursor"
            >|</span>
          </div>
        </div>
      </div>
      <div v-if="messages.length === 0" class="empty-chat">
        <p>发送一条消息开始对话 ✨</p>
      </div>
    </div>

    <div class="chat-input-area">
      <input
        v-model="inputMessage"
        :disabled="isGenerating"
        @keyup.enter="handlePrimaryAction"
        placeholder="输入消息..."
      />
      <button
        :class="[
          'action-btn',
          isGenerating ? 'stop-btn' : 'send-btn'
        ]"
        @click="handlePrimaryAction"
      >
        {{ isGenerating ? "停止" : "发送" }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  onMounted,
  onBeforeUnmount,
  nextTick
} from "vue";
import axios from "axios";
import { useRoute } from "vue-router";

interface Message {
  role: string;
  content: string;
  tool_call_id?: string;
}

interface StreamEvent {
  type: string;
  delta?: string;
  content?: string;
  message?: string;
}

export default defineComponent({
  setup() {
    const route = useRoute();
    const messages = ref<Message[]>([]);
    const inputMessage = ref("");
    const chatBox = ref<HTMLDivElement | null>(null);
    const isGenerating = ref(false);
    const abortController = ref<AbortController | null>(null);

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

    const stopGeneration = () => {
      abortController.value?.abort();
    };

    const parseSseEvents = (
      buffer: string
    ): { events: StreamEvent[]; rest: string } => {
      const events: StreamEvent[] = [];
      const parts = buffer.split("\n\n");
      const rest = parts.pop() || "";

      for (const part of parts) {
        const line = part
          .split("\n")
          .find((item) => item.startsWith("data: "));

        if (!line) {
          continue;
        }

        try {
          events.push(
            JSON.parse(line.slice(6))
          );
        } catch (error) {
          console.error("解析流式消息失败", error);
        }
      }

      return { events, rest };
    };

    const sendMessage = async () => {
      const text = inputMessage.value.trim();
      if (!text || isGenerating.value) {
        return;
      }

      const agentId = route.params.agentId;
      const token = localStorage.getItem("token");

      if (!token) {
        return;
      }

      inputMessage.value = "";

      messages.value.push({
        role: "user",
        content: text
      });

      const assistantIndex = messages.value.length;

      messages.value.push({
        role: "assistant",
        content: ""
      });

      await scrollToBottom();

      isGenerating.value = true;
      abortController.value = new AbortController();

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/chat/${agentId}/stream`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ message: text }),
            signal: abortController.value.signal,
          }
        );

        if (!response.ok || !response.body) {
          throw new Error("请求失败");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          buffer += decoder.decode(value, { stream: true });

          const parsed = parseSseEvents(buffer);
          buffer = parsed.rest;

          for (const event of parsed.events) {
            if (event.type === "content" && event.delta) {
              messages.value[assistantIndex].content += event.delta;
              await scrollToBottom();
            }

            if (event.type === "done" && event.content) {
              messages.value[assistantIndex].content = event.content;
            }

            if (event.type === "error") {
              throw new Error(event.message || "Agent 执行失败");
            }
          }
        }

        if (!messages.value[assistantIndex].content.trim()) {
          messages.value[assistantIndex].content =
            "未收到回复，请重试。";
        }
      } catch (err: any) {
        if (err?.name === "AbortError") {
          if (!messages.value[assistantIndex].content.trim()) {
            messages.value[assistantIndex].content =
              "已停止生成。";
          } else {
            messages.value[assistantIndex].content +=
              "\n\n[已停止]";
          }
        } else {
          messages.value[assistantIndex].content =
            err?.message || "发送失败，请重试";
        }
      } finally {
        isGenerating.value = false;
        abortController.value = null;
        await scrollToBottom();
      }
    };

    const handlePrimaryAction = () => {
      if (isGenerating.value) {
        stopGeneration();
        return;
      }

      sendMessage();
    };

    onMounted(() => {
      loadHistory();
    });

    onBeforeUnmount(() => {
      stopGeneration();
    });

    return {
      messages,
      inputMessage,
      isGenerating,
      handlePrimaryAction,
      chatBox,
    };
  },
});
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  height: 85vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--bg);
}

.back-link {
  color: var(--accent);
  text-decoration: none;
  font-size: 14px;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  max-width: 80%;
  animation: fadeInUp 0.2s ease;
}

.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message.ai {
  align-self: flex-start;
}

.message-avatar {
  width: 36px;
  height: 36px;
  background: var(--code-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-content {
  background: var(--code-bg);
  padding: 10px 16px;
  border-radius: 18px;
  max-width: 100%;
}

.user .message-content {
  background: var(--accent);
  color: white;
}

.message-text {
  word-break: break-word;
  line-height: 1.4;
  white-space: pre-wrap;
}

.typing-cursor {
  animation: blink 1s step-end infinite;
}

.empty-chat {
  text-align: center;
  padding: 40px;
  color: var(--text);
}

.chat-input-area {
  display: flex;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  background: var(--bg);
}

.chat-input-area input {
  flex: 1;
  margin-bottom: 0;
}

.action-btn {
  min-width: 88px;
  border: none;
  border-radius: 12px;
  padding: 0 18px;
  cursor: pointer;
  color: white;
}

.send-btn {
  background: var(--accent);
}

.stop-btn {
  background: #ef4444;
}

.action-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes blink {
  50% {
    opacity: 0;
  }
}
</style>
