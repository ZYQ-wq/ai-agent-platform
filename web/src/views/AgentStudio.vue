<template>
  <div class="container">
    <div class="header">
      <h2>我的 Agent 工作室</h2>
      <button class="create-btn" @click="openCreate">+ 新建 Agent</button>
    </div>

    <div v-if="agents.length === 0" class="empty-state">
      <p>还没有任何 Agent，点击上方按钮创建一个吧 🚀</p>
    </div>

    <div v-for="agent in agents" :key="agent.id" class="agent-card card">
      <div class="agent-info">
        <h3>{{ agent.name }}</h3>
        <p>{{ agent.description || "暂无描述" }}</p>
      </div>
      <div class="agent-actions">
        <button class="chat-btn" @click="goChat(agent.id)">💬 聊天</button>
        <button class="edit-btn" @click="openEdit(agent)">✏️ 编辑</button>
        <button class="delete-btn" @click="deleteAgent(agent.id)">🗑️ 删除</button>
      </div>
    </div>

    <!-- 表单模态框 (内联，可改进为弹窗，但保持原逻辑) -->
    <div v-if="showForm" class="form-overlay">
      <div class="form-card card">
        <h3>{{ editingAgent ? "编辑 Agent" : "新建 Agent" }}</h3>
        <input v-model="form.name" placeholder="名称" />
        <input v-model="form.description" placeholder="描述" />
        <textarea v-model="form.system_prompt" placeholder="System Prompt"></textarea>
        <div class="form-buttons">
          <button class="save-btn" @click="saveAgent">保存</button>
          <button class="cancel-btn" @click="closeForm">取消</button>
        </div>
      </div>
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
        system_prompt: "",
      },
    };
  },
  mounted() {
    this.loadAgents();
  },
  methods: {
    authHeader() {
      return { Authorization: `Bearer ${localStorage.getItem("token")}` };
    },
    async loadAgents() {
      const res = await axios.get("http://127.0.0.1:8000/agents/my", {
        headers: this.authHeader(),
      });
      this.agents = res.data;
    },
    openCreate() {
      this.editingAgent = null;
      this.form = { name: "", description: "", system_prompt: "" };
      this.showForm = true;
    },
    openEdit(agent) {
      this.editingAgent = agent;
      this.form = {
        name: agent.name,
        description: agent.description,
        system_prompt: agent.system_prompt,
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
          { headers: this.authHeader() }
        );
      } else {
        await axios.post("http://127.0.0.1:8000/agents/create", this.form, {
          headers: this.authHeader(),
        });
      }
      this.showForm = false;
      this.loadAgents();
    },
    async deleteAgent(id) {
      if (!confirm("确认删除这个 Agent？")) return;
      try {
        await axios.delete(`http://127.0.0.1:8000/agents/${id}`, {
          headers: this.authHeader(),
        });
        this.loadAgents();
      } catch (e) {
        console.error("删除失败", e);
      }
    },
    goChat(id) {
      this.$router.push(`/chat/${id}`);
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.create-btn {
  background: var(--accent);
  padding: 10px 24px;
}

.agent-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.agent-info {
  flex: 2;
}

.agent-info h3 {
  margin: 0 0 4px 0;
}

.agent-info p {
  margin: 0;
  color: var(--text);
}

.agent-actions {
  display: flex;
  gap: 12px;
}

.chat-btn, .edit-btn, .delete-btn {
  padding: 6px 16px;
  font-size: 13px;
}

.edit-btn {
  background: #3b82f6;
}

.delete-btn {
  background: #ef4444;
}

.empty-state {
  text-align: center;
  padding: 64px;
  background: var(--code-bg);
  border-radius: 32px;
  color: var(--text);
}

.form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.form-card {
  width: 90%;
  max-width: 500px;
  background: var(--bg);
}

.form-card input, .form-card textarea {
  width: 100%;
  margin-bottom: 16px;
}

.form-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.save-btn {
  background: var(--accent);
}
.cancel-btn {
  background: #6b7280;
}
</style>