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

import { ref } from "vue"

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

const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const onConnect = (params: any) => {

  edges.value = addEdge(
    params,
    edges.value
  )

}

let currentId = 1

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

    }))

  }

  await axios.post(
    "http://127.0.0.1:8000/workflow/save",
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