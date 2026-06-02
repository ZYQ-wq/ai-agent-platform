<template>
  <div class="container">

    <h2>我的 Agent</h2>

    <button @click="openCreate">
      创建Agent
    </button>

    <hr />

    <div
      v-for="agent in agents"
      :key="agent.id"
      class="agent-card"
    >
      <h3>{{ agent.name }}</h3>

      <p>
        {{ agent.description }}
      </p>

      <button
        @click="goChat(agent.id)"
      >
        聊天
      </button>

      <button
        @click="openEdit(agent)"
      >
        编辑
      </button>

      <button
        @click="deleteAgent(agent.id)"
      >
        删除
      </button>
    </div>

    <div
      v-if="showForm"
      class="form-box"
    >

      <h3>
        {{ editingAgent ? "编辑Agent" : "创建Agent" }}
      </h3>

      <input
        v-model="form.name"
        placeholder="名称"
      />

      <input
        v-model="form.description"
        placeholder="描述"
      />

      <textarea
        v-model="form.system_prompt"
        placeholder="System Prompt"
      />

      <button @click="saveAgent">
        保存
      </button>

      <button @click="closeForm">
        取消
      </button>

    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {

  data() {

    return {

      agents: [],

      showForm: false,

      editingAgent: null,

      form: {

        name: "",

        description: "",

        system_prompt: ""

      }

    };

  },

  mounted() {

    this.loadAgents();

  },

  methods: {

    authHeader() {

      return {

        Authorization:
          `Bearer ${localStorage.getItem("token")}`

      };

    },

    async loadAgents() {

      const res =
        await axios.get(

          "http://127.0.0.1:8000/agents/my",

          {
            headers:
              this.authHeader()
          }

        );

      this.agents =
        res.data;

    },

    openCreate() {

      this.editingAgent = null;

      this.form = {

        name: "",

        description: "",

        system_prompt: ""

      };

      this.showForm = true;

    },

    openEdit(agent) {

      this.editingAgent = agent;

      this.form = {

        name: agent.name,

        description: agent.description,

        system_prompt: agent.system_prompt

      };

      this.showForm = true;

    },

    closeForm() {

      this.showForm = false;

    },

    async saveAgent() {

      if (this.editingAgent) {

        await axios.put(

          `http://127.0.0.1:8000/agents/${this.editingAgent.id}`,

          this.form,

          {
            headers:
              this.authHeader()
          }

        );

      } else {

        await axios.post(

          "http://127.0.0.1:8000/agents/create",

          this.form,

          {
            headers:
              this.authHeader()
          }

        );

      }

      this.showForm = false;

      this.loadAgents();

    },

    async deleteAgent(id) {
        if (!confirm("确认删除这个Agent？")) return;
        try {
            await axios.delete(
            `http://127.0.0.1:8000/agents/${id}`,
            { headers: this.authHeader() }
            );
            this.loadAgents();
        } catch (e) {
            console.error("删除Agent失败:", e);
        }
        },

    goChat(id) {

      this.$router.push(
        `/chat/${id}`
      );

    }

  }

};
</script>

<style scoped>

.container {
  width: 900px;
  margin: 20px auto;
}

.agent-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 10px;
}

.form-box {
  border: 1px solid #333;
  padding: 20px;
  margin-top: 20px;
}

input,
textarea {
  width: 100%;
  margin-bottom: 10px;
}

</style>