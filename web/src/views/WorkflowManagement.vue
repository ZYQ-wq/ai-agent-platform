<template>
  <div class="container">
    <div class="header">
      <h2>我的工作流</h2>
      <button class="create-btn" @click="goToCreateWorkflow">+ 新建工作流</button>
    </div>

    <div v-if="workflows.length === 0" class="empty-state">
      <p>还没有任何工作流，点击上方按钮创建一个吧 🚀</p>
    </div>

    <div v-for="workflow in workflows" :key="workflow.id" class="workflow-card card">
      <div class="workflow-info">
        <div class="workflow-icon">⚙️</div>
        <div class="workflow-details">
          <h3>{{ workflow.name }}</h3>
          <p>{{ workflow.description || "暂无描述" }}</p>
          <div class="workflow-meta">
            <span class="meta-item">创建时间: {{ formatDate(workflow.created_at) }}</span>
            <span class="meta-item">节点数: {{ workflow.node_count || 0 }}</span>
          </div>
        </div>
      </div>
      <div class="workflow-actions">
        <button class="run-btn" @click="runWorkflow(workflow)">▶️ 运行</button>
        <button class="edit-btn" @click="editWorkflow(workflow)">✏️ 编辑</button>
        <button class="delete-btn" @click="deleteWorkflow(workflow.id)">🗑️ 删除</button>
      </div>
    </div>

    <!-- 返回广场按钮 -->
    <div class="back-to-plaza">
      <button class="back-btn" @click="goToPlaza">← 返回广场</button>
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
    const workflows = ref([])
    const loading = ref(false)

    // 加载工作流列表
    const loadWorkflows = async () => {
      loading.value = true
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://127.0.0.1:8000/workflows/my', {
          headers: { Authorization: `Bearer ${token}` }
        })

        // 为每个工作流添加节点数量
        workflows.value = res.data?.map(wf => ({
          ...wf,
          node_count: wf.nodes ? wf.nodes.length : 0
        })) || []
      } catch (error) {
        console.error('加载工作流失败:', error)
        // 如果API未实现，使用模拟数据
        console.log('工作流API暂未实现，使用模拟数据')
        workflows.value = [
          {
            id: 1,
            name: '示例工作流',
            description: '这是一个示例工作流',
            created_at: new Date().toISOString(),
            node_count: 3
          }
        ]
      } finally {
        loading.value = false
      }
    }

    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 删除工作流
    const deleteWorkflow = async (id) => {
      if (!confirm('确认删除这个工作流？')) return

      try {
        const token = localStorage.getItem('token')
        await axios.delete(`http://127.0.0.1:8000/workflows/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        loadWorkflows()
      } catch (error) {
        console.error('删除失败:', error)
        alert('删除失败')
      }
    }

    // 运行工作流
    const runWorkflow = (workflow) => {
      // 这里可以添加运行工作流的逻辑
      alert(`运行工作流: ${workflow.name}`)
    }

    // 编辑工作流
    const editWorkflow = (workflow) => {
      router.push(`/workflow?id=${workflow.id}`)
    }

    // 导航方法
    const goToCreateWorkflow = () => {
      router.push('/workflow')
    }

    const goToPlaza = () => {
      router.push('/')
    }

    onMounted(() => {
      loadWorkflows()
    })

    return {
      workflows,
      loading,
      formatDate,
      deleteWorkflow,
      runWorkflow,
      editWorkflow,
      goToCreateWorkflow,
      goToPlaza
    }
  }
})
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
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
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.create-btn:hover {
  opacity: 0.9;
}

.workflow-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.2s;
}

.workflow-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.workflow-info {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
}

.workflow-icon {
  font-size: 3rem;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.workflow-details {
  flex: 1;
}

.workflow-details h3 {
  margin: 0 0 8px 0;
  font-size: 1.4rem;
  color: #333;
}

.workflow-details p {
  margin: 0 0 12px 0;
  color: #666;
  line-height: 1.5;
}

.workflow-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.9rem;
  color: #999;
  background: #f5f5f5;
  padding: 4px 12px;
  border-radius: 6px;
}

.workflow-actions {
  display: flex;
  gap: 12px;
}

.run-btn, .edit-btn, .delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.run-btn {
  background: #10b981;
  color: white;
}

.run-btn:hover {
  background: #059669;
}

.edit-btn {
  background: #3b82f6;
  color: white;
}

.edit-btn:hover {
  background: #2563eb;
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
  background: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 64px;
  background: var(--code-bg);
  border-radius: 32px;
  color: var(--text);
  font-size: 1.1rem;
}

.back-to-plaza {
  margin-top: 40px;
  text-align: center;
}

.back-btn {
  background: #6b7280;
  color: white;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #4b5563;
}

@media (max-width: 768px) {
  .container {
    padding: 16px;
  }

  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .workflow-card {
    flex-direction: column;
    gap: 20px;
  }

  .workflow-info {
    width: 100%;
  }

  .workflow-actions {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .workflow-meta {
    justify-content: flex-start;
  }
}
</style>