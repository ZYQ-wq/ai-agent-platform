<template>
  <div class="plaza-container">

    <!-- 顶部标题 -->
    <div class="plaza-header">
      <h1>AI Agent 平台</h1>
      <p>探索智能体、知识库与工作流的世界</p>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">

      <!-- Agent -->
      <div
        class="entrance-card"
        @click="goToAgents"
      >
        <div class="card-icon">🤖</div>

        <h2>智能体</h2>

        <p>
          创建和管理你的AI智能体，
          与它们进行对话交互
        </p>

        <div class="card-stats">
          <span>
            已创建：
            {{ agentCount || 0 }}
            个
          </span>
        </div>

        <div class="card-arrow">
          →
        </div>
      </div>

      <!-- Workflow -->
      <div
        class="entrance-card"
        @click="goToWorkflows"
      >
        <div class="card-icon">⚙️</div>

        <h2>工作流</h2>

        <p>
          构建复杂工作流，
          将多个AI能力组合使用
        </p>

        <div class="card-stats">
          <span>
            已创建：
            {{ workflowCount || 0 }}
            个
          </span>
        </div>

        <div class="card-arrow">
          →
        </div>
      </div>

      <!-- Knowledge Base -->
      <div
        class="entrance-card"
        @click="goToKB"
      >
        <div class="card-icon">📚</div>

        <h2>知识库</h2>

        <p>
          上传文档、向量化训练、
          构建专属知识库
        </p>

        <div class="card-stats">
          <span>
            已创建：
            {{ kbCount || 0 }}
            个
          </span>
        </div>

        <div class="card-arrow">
          →
        </div>
      </div>

      <!-- AI Coding -->
      <div
        class="entrance-card"
        @click="goToAICode"
      >
        <div class="card-icon">💻</div>

        <h2>AI编程</h2>

        <p>
          AI辅助代码生成、
          调试与工程开发
        </p>

        <div class="card-stats">
          <span>
            即将上线
          </span>
        </div>

        <div class="card-arrow">
          →
        </div>
      </div>

    </div>

    <!-- 底部快捷操作 -->
    <div class="quick-actions">

      <div
        class="action-item"
        @click="goToCreateAgent"
      >
        <span class="action-icon">+</span>
        <span>新建智能体</span>
      </div>

      <div
        class="action-item"
        @click="goToCreateWorkflow"
      >
        <span class="action-icon">+</span>
        <span>新建工作流</span>
      </div>

      <div
        class="action-item"
        @click="goToKB"
      >
        <span class="action-icon">+</span>
        <span>进入知识库</span>
      </div>

    </div>

  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  onMounted
} from "vue"

import axios from "axios"
import { useRouter } from "vue-router"

export default defineComponent({

  setup() {

    const router = useRouter()

    const agentCount = ref(0)

    const workflowCount = ref(0)

    const kbCount = ref(0)

    // =====================
    // 加载数据
    // =====================
    const loadData = async () => {

      try {

        const token =
          localStorage.getItem("token")

        if (!token) return

        const headers = {
          Authorization:
            `Bearer ${token}`
        }

        // Agent
        try {

          const res =
            await axios.get(
              "http://127.0.0.1:8000/agents/my",
              { headers }
            )

          agentCount.value =
            res.data?.length || 0

        } catch {
          agentCount.value = 0
        }

        // Workflow
        try {

          const res =
            await axios.get(
              "http://127.0.0.1:8000/workflow/my",
              { headers }
            )

          workflowCount.value =
            res.data?.length || 0

        } catch {

          workflowCount.value = 0
        }

        // KB
        try {

          const res =
            await axios.get(
              "http://127.0.0.1:8000/kb/list",
              { headers }
            )

          kbCount.value =
            res.data?.data?.length || 0

        } catch {

          kbCount.value = 0
        }

      } catch (err) {

        console.error(err)
      }
    }

    // =====================
    // 跳转
    // =====================

    const goToAgents = () => {

      router.push(
        "/agents/studio"
      )
    }

    const goToWorkflows = () => {

      router.push(
        "/workflow-management"
      )
    }

    const goToKB = () => {

      router.push("/kb")
    }

    const goToAICode = () => {

      alert("AI编程模块开发中")
    }

    const goToCreateAgent = () => {

      router.push(
        "/agents/studio"
      )
    }

    const goToCreateWorkflow = () => {

      router.push(
        "/workflow"
      )
    }

    onMounted(() => {

      loadData()
    })

    return {

      agentCount,
      workflowCount,
      kbCount,

      goToAgents,
      goToWorkflows,
      goToKB,
      goToAICode,

      goToCreateAgent,
      goToCreateWorkflow
    }
  }
})
</script>

<style scoped>

.plaza-container {
  min-height: 100vh;
  background:
    linear-gradient(
      135deg,
      #667eea 0%,
      #764ba2 100%
    );
  display: flex;
  flex-direction: column;
  color: white;
}

.plaza-header {
  text-align: center;
  padding: 60px 20px 40px;
}

.plaza-header h1 {
  font-size: 3rem;
  margin: 0 0 16px;
}

.plaza-header p {
  font-size: 1.2rem;
  opacity: .9;
}

.main-content {

  flex: 1;

  display: grid;

  grid-template-columns:
    repeat(
      auto-fit,
      minmax(320px, 1fr)
    );

  gap: 30px;

  padding: 40px;

  max-width: 1500px;

  width: 100%;

  margin: 0 auto;
}

.entrance-card {

  background:
    rgba(
      255,
      255,
      255,
      0.95
    );

  border-radius: 24px;

  padding: 40px;

  cursor: pointer;

  color: #333;

  position: relative;

  transition: .3s;

  min-height: 280px;

  box-shadow:
    0 10px 30px
    rgba(0,0,0,.2);
}

.entrance-card:hover {

  transform:
    translateY(-10px);

  box-shadow:
    0 20px 40px
    rgba(0,0,0,.3);
}

.card-icon {

  font-size: 4rem;

  margin-bottom: 20px;
}

.entrance-card h2 {

  font-size: 2rem;

  margin-bottom: 16px;
}

.entrance-card p {

  color: #666;

  line-height: 1.6;
}

.card-stats {

  margin-top: 20px;

  display: inline-block;

  padding: 12px 20px;

  border-radius: 12px;

  background:
    rgba(
      102,
      126,
      234,
      .1
    );

  color: #667eea;
}

.card-arrow {

  position: absolute;

  right: 30px;

  top: 50%;

  transform:
    translateY(-50%);

  font-size: 2rem;

  color: #667eea;
}

.quick-actions {

  display: flex;

  justify-content: center;

  gap: 20px;

  padding: 20px;

  background:
    rgba(
      0,
      0,
      0,
      .1
    );
}

.action-item {

  display: flex;

  align-items: center;

  gap: 10px;

  cursor: pointer;

  padding: 12px 24px;

  border-radius: 12px;

  background:
    rgba(
      255,
      255,
      255,
      .2
    );
}

.action-item:hover {

  background:
    rgba(
      255,
      255,
      255,
      .3
    );
}

.action-icon {

  width: 32px;

  height: 32px;

  border-radius: 50%;

  background: white;

  color: #667eea;

  display: flex;

  align-items: center;

  justify-content: center;

  font-weight: bold;
}

@media (max-width: 768px) {

  .main-content {

    grid-template-columns: 1fr;

    padding: 20px;
  }

  .plaza-header h1 {

    font-size: 2rem;
  }
}
</style>