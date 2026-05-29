
<template>
  <div class="container">

    <h1>我的智能体</h1>

    <!-- 创建Agent -->
    <div class="create-box">

      <input
        v-model="name"
        placeholder="Agent名称"
      />

      <input
        v-model="description"
        placeholder="Agent简介"
      />

      <textarea
        v-model="systemPrompt"
        placeholder="系统Prompt"
      />

      <button @click="createAgent">
        创建Agent
      </button>

    </div>

    <!-- Agent列表 -->
    <div
      class="agent-card"
      v-for="agent in agents"
      :key="agent.id"
    >

      <h2>{{ agent.name }}</h2>

      <p>{{ agent.description }}</p>

      <button @click="goChat(agent.id)">
        进入聊天
      </button>

    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default defineComponent({

  setup() {

    const router = useRouter();

    const agents = ref([]);

    const name = ref("");

    const description = ref("");

    const systemPrompt = ref("");

    // 获取Agent列表
    const loadAgents = async () => {

      try {

        const token = localStorage.getItem("token");

        const res = await axios.get(
          "http://127.0.0.1:8000/agents/my",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        agents.value = res.data;

      } catch (err) {

        alert("获取Agent失败");

      }

    };

    // 创建Agent
    const createAgent = async () => {

      try {

        const token = localStorage.getItem("token");

        await axios.post(
          "http://127.0.0.1:8000/agents/create",
          {
            name: name.value,
            description: description.value,
            system_prompt: systemPrompt.value
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        name.value = "";
        description.value = "";
        systemPrompt.value = "";

        loadAgents();

      } catch (err) {

        alert("创建失败");

      }

    };

    // 进入聊天
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
      goChat
    };

  }

});
</script>

<style scoped>

.container {
  max-width: 900px;
  margin: 40px auto;
}

.create-box {
  display: flex;
  flex-direction: column;
  margin-bottom: 30px;
}

input,
textarea {
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px;
  cursor: pointer;
}

.agent-card {
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
}

</style>

