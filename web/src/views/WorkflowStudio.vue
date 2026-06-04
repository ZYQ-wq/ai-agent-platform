<template>
  <div class="workflow-page">

    <!-- 顶部工具栏 -->
    <div class="toolbar">

      <button @click="addStart">
        + Start
      </button>

      <button @click="addLLM">
        + LLM
      </button>

      <button @click="addTool">
        + Tool
      </button>

      <button @click="addEnd">
        + End
      </button>

      <button @click="saveWorkflow">
        保存工作流
      </button>

    </div>

    <!-- 工作流画布 -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @connect="onConnect"
      :node-types="nodeTypes"
      fit-view-on-init
      class="workflow-canvas"
    >

      <Background />

      <Controls />

      <MiniMap />

    </VueFlow>

  </div>
</template>

<script setup lang="ts">

import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

import axios from "axios"

import {
  VueFlow
} from "@vue-flow/core"

import {
  Background
} from "@vue-flow/background"

import {
  Controls
} from "@vue-flow/controls"

import {
  MiniMap
} from "@vue-flow/minimap"

import {
  addEdge
} from "@vue-flow/core"

import WorkflowNode from "../components/workflow/WorkflowNode.vue"

import "@vue-flow/core/dist/style.css"
import "@vue-flow/core/dist/theme-default.css"

import type { Node, Edge } from "@vue-flow/core"

const route = useRoute()
const workflowId = ref(route.query.id ? parseInt(route.query.id as string) : null)

const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const onConnect = (params: any) => {

  edges.value = addEdge(
    params,
    edges.value
  )

}

let currentId = 1

// 加载工作流数据
const loadWorkflow = async () => {
  if (!workflowId.value) return

  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`http://127.0.0.1:8000/workflow/${workflowId.value}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const workflow = res.data
    nodes.value = []
    edges.value = []
    currentId = 1

    // 加载节点
    if (workflow.nodes) {
      workflow.nodes.forEach((node: any) => {
        nodes.value.push({
          id: node.node_id,
          type: "workflow",
          position: {
            x: 100 + (currentId * 100),
            y: 200
          },
          data: {
            label: node.name,
            type: node.node_type
          }
        })
        currentId++
      })
    }

    // 加载边
    if (workflow.edges) {
      workflow.edges.forEach((edge: any) => {
        edges.value.push({
          source: edge.source_node,
          target: edge.target_node
        })
      })
    }

    // 更新工作流名称
    // 这里可以添加一个编辑工作流名称的功能
  } catch (error) {
    console.error('加载工作流失败:', error)
    alert('加载工作流失败')
  }
}

const nodeTypes = {
  workflow: WorkflowNode
}

function addLLM() {

  nodes.value.push({

    id: String(currentId++),

    type: "workflow",

    position: {
      x: 300,
      y: 300
    },

    data: {
      label: "Qwen",
      type: "llm"
    }

  })

}

function addTool() {

  nodes.value.push({

    id: String(currentId++),

    type: "workflow",

    position: {
      x: 300,
      y: 100
    },

    data: {
      label: "搜索工具",
      type: "tool"
    }

  })

}

function addStart() {

  nodes.value.push({

    id: String(currentId++),

    type: "workflow",

    position: {
      x: 100,
      y: 200
    },

    data: {
      label: "开始节点",
      type: "start"
    }

  })

}

function addEnd() {

  nodes.value.push({

    id: String(currentId++),

    type: "workflow",

    position: {
      x: 600,
      y: 200
    },

    data: {
      label: "结束节点",
      type: "output"
    }

  })

}

const saveWorkflow = async () => {

  const workflowData = {

    name: "测试工作流",

    nodes: nodes.value.map((node: any) => ({

      node_id: node.id,

      node_type: node.data.type,

      name: node.data.label,

      config: {}

    })),

    edges: edges.value.map((edge: any) => ({

      source_node: edge.source,

      target_node: edge.target

    })),

    // 如果有工作流ID，则传递给后端
    workflow_id: workflowId.value || null
  }

  const url = workflowId.value
    ? `http://127.0.0.1:8000/workflow/save`
    : "http://127.0.0.1:8000/workflow/save"

  await axios.post(
    url,
    workflowData,
    {
      headers: {
        Authorization:
          "Bearer " +
          localStorage.getItem("token")
      }
    }
  )

  alert("保存成功")
}


// 如果有工作流ID，加载工作流数据
if (workflowId.value) {
  loadWorkflow()
}
  

</script>

<style scoped>

.workflow-page {

  width: 100%;

  height: 100vh;

  display: flex;

  flex-direction: column;

}

.toolbar {

  height: 60px;

  display: flex;

  align-items: center;

  gap: 12px;

  padding: 0 20px;

  border-bottom: 1px solid #ddd;

  background: white;

}

.toolbar button {

  padding: 8px 16px;

  border: none;

  border-radius: 8px;

  cursor: pointer;

  background: #409eff;

  color: white;

}

.toolbar button:hover {

  opacity: 0.9;

}

.workflow-canvas {

  flex: 1;

}

</style>