<!-- web/src/views/WorkflowEditor.vue -->
<template>
  <div class="workflow-editor-container">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="info">
        <input v-model="workflowName" placeholder="工作流名称" class="name-input" />
        <input v-model="workflowDesc" placeholder="工作流描述" class="desc-input" />
      </div>
      <div class="actions">
        <button @click="saveWorkflow" class="save-btn">💾 保存</button>
        <button @click="goBack" class="back-btn">← 返回</button>
      </div>
    </div>

    <!-- Vue Flow 画布 -->
    <div class="canvas">
      <VueFlow
        v-model:nodes="nodes"
        v-model:edges="edges"
        :default-viewport="{ x: 0, y: 0, zoom: 1 }"
        :fit-view-on-init="true"
        class="flow"
      >
        <Background />
        <Controls />
        <MiniMap />
      </VueFlow>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { VueFlow, Background, Controls, MiniMap, useVueFlow } from '@vue-flow/core'

// 定义数据类型
interface WorkflowNode {
  id: string
  type?: string
  position: { x: number; y: number }
  data: Record<string, any>
}

interface WorkflowEdge {
  id: string
  source: string
  target: string
  sourceHandle?: string
  targetHandle?: string
}

// 路由相关
const route = useRoute()
const router = useRouter()
const workflowId = route.query.id as string | undefined  // 获取 ?id=xxx

// 表单数据
const workflowName = ref('')
const workflowDesc = ref('')

// Vue Flow 数据
const nodes = ref<WorkflowNode[]>([])
const edges = ref<WorkflowEdge[]>([])
const { setNodes, setEdges } = useVueFlow()

// 从后端加载工作流详情
const loadWorkflowDetail = async (id: string) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://127.0.0.1:8000/workflow/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = response.data
    // 填充基本信息
    workflowName.value = data.name || ''
    workflowDesc.value = data.description || ''
    // 填充节点和连线
    if (data.nodes && Array.isArray(data.nodes)) {
      nodes.value = data.nodes
      setNodes(data.nodes)   // 确保 Vue Flow 更新
    }
    if (data.edges && Array.isArray(data.edges)) {
      edges.value = data.edges
      setEdges(data.edges)
    }
    console.log('工作流加载成功', data)
  } catch (error) {
    console.error('加载工作流失败:', error)
    alert('加载工作流失败，请检查网络或后端服务')
  }
}

// 保存工作流
const saveWorkflow = async () => {
  try {
    const token = localStorage.getItem('token')
    const payload = {
      id: workflowId ? parseInt(workflowId) : undefined,
      name: workflowName.value,
      description: workflowDesc.value,
      nodes: nodes.value,
      edges: edges.value
    }
    const response = await axios.post('http://127.0.0.1:8000/workflow/save', payload, {
      headers: { Authorization: `Bearer ${token}` }
    })
    alert('保存成功')
    // 如果是新建（没有id），保存成功后跳转到带id的编辑页面
    if (!workflowId && response.data.workflow_id) {
      router.push(`/workflow?id=${response.data.workflow_id}`)
    }
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败')
  }
}

// 返回列表页
const goBack = () => {
  router.push('/workflow-management')
}

// 初始化
onMounted(() => {
  if (workflowId) {
    loadWorkflowDetail(workflowId)
  } else {
    console.log('新建工作流模式，暂不加载数据')
    // 可以可选地初始化一个默认节点示例
    // nodes.value = [{ id: '1', type: 'start', position: { x: 250, y: 150 }, data: { label: '开始' } }]
  }
})
</script>

<style scoped>
.workflow-editor-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7f9fc;
}

.toolbar {
  background: white;
  padding: 12px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.info {
  display: flex;
  gap: 16px;
  align-items: center;
}

.name-input, .desc-input {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 14px;
  transition: 0.2s;
}

.name-input:focus, .desc-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59,130,246,0.1);
}

.name-input {
  width: 240px;
  font-weight: 500;
}

.desc-input {
  width: 320px;
}

.actions {
  display: flex;
  gap: 12px;
}

.save-btn, .back-btn {
  padding: 8px 20px;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: 0.2s;
}

.save-btn {
  background: #10b981;
  color: white;
}

.save-btn:hover {
  background: #059669;
}

.back-btn {
  background: #f1f5f9;
  color: #1e293b;
}

.back-btn:hover {
  background: #e2e8f0;
}

.canvas {
  flex: 1;
  position: relative;
}

.flow {
  width: 100%;
  height: 100%;
}
</style>