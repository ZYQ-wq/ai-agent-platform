<template>
  <div class="container">
    <h1>我的智能体</h1>

    <!-- 创建表单 -->
    <div class="create-card card">
      <h3>新建智能体</h3>
      <input v-model="name" placeholder="名称" />
      <input v-model="description" placeholder="简介" />
      <textarea v-model="systemPrompt" placeholder="系统 Prompt"></textarea>
      <button @click="createAgent">创建 Agent</button>
    </div>

    <!-- Agent 列表 -->
    <div v-if="agents.length === 0" class="empty-state">
      <p>还没有智能体，点击上方按钮创建一个吧 ✨</p>
    </div>

    <div v-for="agent in agents" :key="agent.id" class="agent-card card">
      <h2>{{ agent.name }}</h2>
      <p>{{ agent.description || "暂无描述" }}</p>
      <button class="chat-btn" @click="goChat(agent.id)">进入聊天</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const router = useRouter();
    const agents = ref([]);
    const name = ref("");
    const description = ref("");
    const systemPrompt = ref("");

    const loadAgents = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://127.0.0.1:8000/agents/my", {
          headers: { Authorization: `Bearer ${token}` },
        });
        agents.value = res.data;
      } catch (err) {
        alert("获取Agent失败");
      }
    };

    const createAgent = async () => {
      try {
        const token = localStorage.getItem("token");
        await axios.post(
          "http://127.0.0.1:8000/agents/create",
          {
            name: name.value,
            description: description.value,
            system_prompt: systemPrompt.value,
          },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        name.value = "";
        description.value = "";
        systemPrompt.value = "";
        loadAgents();
      } catch (err) {
        alert("创建失败");
      }
    };

    const goChat = (agentId: number) => {
      router.push(`/chat/${agentId}`);
    };

    onMounted(() => {
      loadAgents();
    });

    return {
      agents,
      name,
      description,
      systemPrompt,
      createAgent,
      goChat,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 32px;
}

.create-card {
  margin-bottom: 40px;
}

.create-card h3 {
  margin-top: 0;
  margin-bottom: 16px;
}

input,
textarea {
  width: 100%;
  margin-bottom: 12px;
}

button {
  margin-top: 8px;
}

.agent-card {
  margin-bottom: 20px;
  transition: all 0.2s;
}

.agent-card:hover {
  transform: translateY(-2px);
}

.agent-card h2 {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 1.4rem;
}

.agent-card p {
  color: var(--text);
  margin-bottom: 16px;
}

.chat-btn {
  background: var(--accent);
}

.empty-state {
  text-align: center;
  padding: 48px;
  background: var(--code-bg);
  border-radius: 24px;
  color: var(--text);
}
</style>