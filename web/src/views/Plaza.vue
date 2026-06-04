<template>
  <div class="plaza-container">
    <!-- 顶部标题 -->
    <div class="plaza-header">
      <h1>AI Agent 平台</h1>
      <p>探索智能体与工作流的世界</p>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- Agent 入口卡片 -->
      <div class="entrance-card" @click="goToAgents">
        <div class="card-icon">🤖</div>
        <h2>智能体</h2>
        <p>创建和管理你的AI智能体，与它们进行对话交互</p>
        <div class="card-stats">
          <span>已创建: {{ agentCount || 0 }} 个</span>
        </div>
        <div class="card-arrow">→</div>
      </div>

      <!-- Workflow 入口卡片 -->
      <div class="entrance-card" @click="goToWorkflows">
        <div class="card-icon">⚙️</div>
        <h2>工作流</h2>
        <p>构建复杂的工作流，将多个AI工具组合使用</p>
        <div class="card-stats">
          <span>已创建: {{ workflowCount || 0 }} 个</span>
        </div>
        <div class="card-arrow">→</div>
      </div>
    </div>

    <!-- 底部快捷操作 -->
    <div class="quick-actions">
      <div class="action-item" @click="goToCreateAgent">
        <span class="action-icon">+</span>
        <span>新建智能体</span>
      </div>
      <div class="action-item" @click="goToCreateWorkflow">
        <span class="action-icon">+</span>
        <span>新建工作流</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const router = useRouter()
    const agentCount = ref(0)
    const workflowCount = ref(0)

    // 加载数据
    const loadData = async () => {
      try {
        const token = localStorage.getItem('token')

        // 加载智能体数量
        if (token) {
          const agentsRes = await axios.get('http://127.0.0.1:8000/agents/my', {
            headers: { Authorization: `Bearer ${token}` }
          })
          agentCount.value = agentsRes.data?.length || 0

          // 加载工作流数量
          try {
            const workflowsRes = await axios.get('http://127.0.0.1:8000/workflow/my', {
              headers: { Authorization: `Bearer ${token}` }
            })
            workflowCount.value = workflowsRes.data?.length || 0
          } catch (error) {
            console.log('工作流API暂未实现，使用模拟数据')
            workflowCount.value = 0
          }
        }
      } catch (error) {
        console.error('加载数据失败:', error)
      }
    }

    // 导航方法
    const goToAgents = () => {
      router.push('/agents/studio')
    }

    const goToWorkflows = () => {
      router.push('/workflow-management')
    }

    const goToCreateAgent = () => {
      router.push('/agents/studio')
    }

    const goToCreateWorkflow = () => {
      router.push('/workflow')
    }

    onMounted(() => {
      loadData()
    })

    return {
      agentCount,
      workflowCount,
      goToAgents,
      goToWorkflows,
      goToCreateAgent,
      goToCreateWorkflow
    }
  }
})
</script>

<style scoped>
.plaza-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  margin: 0 0 16px 0;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.plaza-header p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  gap: 40px;
  flex-wrap: wrap;
}

.entrance-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 40px;
  min-width: 320px;
  max-width: 380px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #333;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
  position: relative;
  overflow: hidden;
}

.entrance-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.entrance-card:active {
  transform: translateY(-5px);
}

.card-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  display: block;
}

.entrance-card h2 {
  font-size: 2rem;
  margin: 0 0 16px 0;
  font-weight: 600;
}

.entrance-card p {
  font-size: 1rem;
  line-height: 1.6;
  margin: 0 0 20px 0;
  color: #666;
}

.card-stats {
  background: rgba(102, 126, 234, 0.1);
  padding: 12px 20px;
  border-radius: 12px;
  display: inline-block;
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: #667eea;
}

.card-arrow {
  position: absolute;
  right: 30px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2rem;
  color: #667eea;
  opacity: 0.6;
}

.quick-actions {
  background: rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  justify-content: center;
  gap: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
  color: white;
}

.action-item:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.action-icon {
  background: white;
  color: #667eea;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

@media (max-width: 768px) {
  .plaza-header h1 {
    font-size: 2rem;
  }

  .main-content {
    flex-direction: column;
    gap: 20px;
  }

  .entrance-card {
    min-width: 280px;
    padding: 30px;
  }

  .quick-actions {
    gap: 20px;
  }
}
</style>