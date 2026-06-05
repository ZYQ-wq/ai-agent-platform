<template>
  <div class="workflow-page">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <button @click="addStart">+ Start</button>
      <button @click="addLLM">+ LLM</button>
      <button @click="addTool">+ Tool</button>
      <button @click="addEnd">+ End</button>
      <button @click="handleManualSave">保存工作流</button>
    </div>

    <!-- 工作流画布 -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @connect="onConnect"
      @nodeClick="onNodeClick"
      @pane-click="onPaneClick"
      :node-types="nodeTypes"
      fit-view-on-init
      class="workflow-canvas"
    >
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>

    <!-- 右侧节点配置面板 -->
    <div v-if="selectedNode" class="node-config">
      <div class="config-header">
        <h3>节点配置</h3>
        <button class="close-btn" @click="handleClosePanel">×</button>
      </div>

      <div class="form-item">
        <label>节点名称</label>
        <input v-model="selectedNode.data.label" />
      </div>

      <div class="form-item">
        <label>节点类型</label>
        <input :value="selectedNode.data.type" disabled />
      </div>

      <!-- 输入变量（开始节点除外） -->
      <div class="form-item" v-if="selectedNode.data.type !== 'start'">
        <div class="form-label-row">
          <label>输入变量</label>
          <button class="add-var-btn-inline" @click="addInputVariable">+ 添加变量</button>
        </div>
        <div class="variables-list">
          <div
            v-for="(item, index) in selectedNode.data.inputs"
            :key="index"
            class="variable-row"
          >
            <select v-model="item.type" class="var-type">
              <option value="string">string</option>
              <option value="int">int</option>
              <option value="object">object</option>
              <option value="file">file</option>
            </select>
            <input
              v-model="item.name"
              type="text"
              class="var-name"
              placeholder="变量名"
            />
            <!-- 值设置区域 -->
            <div class="var-value">
              <select v-model="item.valueKind" class="value-kind">
                <option value="constant">常量</option>
                <option value="variable">变量</option>
              </select>
              <template v-if="item.valueKind === 'constant'">
                <input
                  v-model="item.constantValue"
                  type="text"
                  class="value-input"
                  placeholder="常量值"
                />
              </template>
              <template v-else>
                <select v-model="item.variableRef" class="value-input">
                  <option value="">请选择上游输出</option>
                  <option
                    v-for="opt in availableVariables"
                    :key="opt.value"
                    :value="opt.value"
                  >
                    {{ opt.label }}
                  </option>
                </select>
              </template>
            </div>
            <button
              class="remove-var-btn"
              @click="removeInputVariable(index)"
              title="删除变量"
            >✕</button>
          </div>
        </div>
      </div>

      <!-- 输出变量（所有节点都可编辑） -->
      <div class="form-item">
        <div class="form-label-row">
          <label>输出变量</label>
          <button class="add-var-btn-inline" @click="addOutputVariable">+ 添加变量</button>
        </div>
        <div class="variables-list">
          <div
            v-for="(item, index) in selectedNode.data.outputs"
            :key="index"
            class="variable-row"
          >
            <select v-model="item.type" class="var-type">
              <option value="string">string</option>
              <option value="int">int</option>
              <option value="object">object</option>
              <option value="file">file</option>
            </select>
            <input
              v-model="item.name"
              type="text"
              class="var-name"
              placeholder="变量名"
            />
            <button
              class="remove-var-btn"
              @click="removeOutputVariable(index)"
              title="删除变量"
            >✕</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import axios from "axios"
import {
  VueFlow,
  addEdge
} from "@vue-flow/core"
import { Background } from "@vue-flow/background"
import { Controls } from "@vue-flow/controls"
import { MiniMap } from "@vue-flow/minimap"
import WorkflowNode from "../components/workflow/WorkflowNode.vue"
import "@vue-flow/core/dist/style.css"
import "@vue-flow/core/dist/theme-default.css"
import type { Node, Edge, NodeMouseEvent } from "@vue-flow/core"

const route = useRoute()
const workflowId = ref(route.query.id ? parseInt(route.query.id as string) : null)

const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])
const selectedNode = ref<Node | null>(null)

let currentId = 1

const nodeTypes = {
  workflow: WorkflowNode
}

// 计算当前节点可引用的上游输出变量（用于变量下拉框）
const availableVariables = computed(() => {
  if (!selectedNode.value) return []
  const targetId = selectedNode.value.id
  // 找出所有直接前驱节点（通过边）
  const incomingEdges = edges.value.filter(e => e.target === targetId)
  const predecessors = incomingEdges.map(e => e.source)
  const vars: { label: string; value: string }[] = []
  for (const predId of predecessors) {
    const predNode = nodes.value.find(n => n.id === predId)
    if (predNode && predNode.data.outputs) {
      for (const out of predNode.data.outputs) {
        vars.push({
          label: `${predNode.data.label}.${out.name} (${out.type})`,
          value: `${predId}.${out.name}`
        })
      }
    }
  }
  return vars
})

// 事件处理
const onNodeClick = ({ node }: NodeMouseEvent) => {
  selectedNode.value = node
}

const onPaneClick = () => {
  selectedNode.value = null
}

const onConnect = (params: any) => {
  edges.value = addEdge(params, edges.value)
}

// 辅助函数：创建一个带值结构的输入变量
function createInputVariable(name: string, type: string) {
  return {
    name,
    type,
    valueKind: "constant",   // 'constant' 或 'variable'
    constantValue: "",
    variableRef: ""
  }
}

// 添加节点的方法（确保 inputs 使用新的结构）
function addLLM() {
  nodes.value.push({
    id: String(currentId++),
    type: "workflow",
    position: { x: 300, y: 300 },
    data: {
      label: "Qwen",
      type: "llm",
      inputs: [
        createInputVariable("prompt", "string")
      ],
      outputs: [
        { name: "answer", type: "string" }
      ],
      model: "qwen-max"
    }
  })
}

function addTool() {
  nodes.value.push({
    id: String(currentId++),
    type: "workflow",
    position: { x: 300, y: 100 },
    data: {
      label: "搜索工具",
      type: "tool",
      inputs: [],
      outputs: []
    }
  })
}

function addStart() {
  nodes.value.push({
    id: String(currentId++),
    type: "workflow",
    position: { x: 100, y: 200 },
    data: {
      label: "开始节点",
      type: "start",
      inputs: [],
      outputs: [ { name: "input", type: "string" }]
    }
  })
}

function addEnd() {
  nodes.value.push({
    id: String(currentId++),
    type: "workflow",
    position: { x: 600, y: 200 },
    data: {
      label: "结束节点",
      type: "output",
      inputs: [],
      outputs: []
    }
  })
}

// 输入变量编辑方法
function addInputVariable() {
  if (!selectedNode.value) return
  if (!selectedNode.value.data.inputs) {
    selectedNode.value.data.inputs = []
  }
  selectedNode.value.data.inputs.push(createInputVariable("new_input", "string"))
}

function removeInputVariable(index: number) {
  if (!selectedNode.value) return
  selectedNode.value.data.inputs.splice(index, 1)
}

// 输出变量编辑方法
function addOutputVariable() {
  if (!selectedNode.value) return
  if (!selectedNode.value.data.outputs) {
    selectedNode.value.data.outputs = []
  }
  selectedNode.value.data.outputs.push({
    name: "new_output",
    type: "string"
  })
}

function removeOutputVariable(index: number) {
  if (!selectedNode.value) return
  selectedNode.value.data.outputs.splice(index, 1)
}

// 保存工作流（核心：转换前端格式 -> 后端期望的格式）
const saveWorkflow = async (showAlert = false) => {
  try {
    const workflowData = {
      name: "测试工作流",
      description: "",
      nodes: nodes.value.map((node: any) => {
        let inputsToSave = node.data.inputs || []
        // 如果不是开始节点，需要将 valueKind + constantValue/variableRef 转换为 value 对象
        if (node.data.type !== 'start') {
          inputsToSave = inputsToSave.map((inp: any) => {
            let valueObj = null
            if (inp.valueKind === 'constant') {
              valueObj = { kind: 'constant', value: inp.constantValue }
            } else if (inp.valueKind === 'variable' && inp.variableRef) {
              valueObj = { kind: 'variable', value: inp.variableRef }
            }
            return {
              name: inp.name,
              type: inp.type,
              value: valueObj
            }
          })
        } else {
          // 开始节点的 inputs 只保留 name 和 type
          inputsToSave = inputsToSave.map(({ name, type }: any) => ({ name, type }))
        }
        return {
          node_id: node.id,
          node_type: node.data.type,
          name: node.data.label,
          inputs: inputsToSave,
          outputs: node.data.outputs || [],
          config: { model: node.data.model || "" }
        }
      }),
      edges: edges.value.map((edge: any) => ({
        source_node: edge.source,
        target_node: edge.target
      })),
      workflow_id: workflowId.value || null
    }

    const url = "http://127.0.0.1:8000/workflow/save"
    await axios.post(url, workflowData, {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
    
    if (showAlert) {
      alert("保存成功")
    }
    return true
  } catch (error) {
    console.error('保存工作流失败:', error)
    if (showAlert) {
      alert("保存失败")
    }
    return false
  }
}

// 手动保存（按钮触发）
const handleManualSave = async () => {
  await saveWorkflow(true)
}

// 关闭面板时静默保存
const handleClosePanel = async () => {
  await saveWorkflow(false)
  selectedNode.value = null
}

// 加载工作流（后端格式 -> 前端编辑格式）
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

    if (workflow.nodes) {
      workflow.nodes.forEach((node: any) => {
        let inputsData = node.inputs || []
        // 如果不是开始节点，需要将后端存储的 value 对象展开为 valueKind 和具体值字段
        if (node.node_type !== 'start') {
          inputsData = inputsData.map((inp: any) => {
            const value = inp.value || null
            if (value && value.kind === 'constant') {
              return {
                name: inp.name,
                type: inp.type,
                valueKind: 'constant',
                constantValue: value.value || '',
                variableRef: ''
              }
            } else if (value && value.kind === 'variable') {
              return {
                name: inp.name,
                type: inp.type,
                valueKind: 'variable',
                constantValue: '',
                variableRef: value.value || ''
              }
            } else {
              // 向后兼容旧数据（没有 value 字段）
              return {
                name: inp.name,
                type: inp.type,
                valueKind: 'constant',
                constantValue: '',
                variableRef: ''
              }
            }
          })
        }
        nodes.value.push({
          id: node.node_id,
          type: "workflow",
          position: { x: 100 + (currentId * 100), y: 200 },
          data: {
            label: node.name,
            type: node.node_type,
            inputs: inputsData,
            outputs: node.outputs || [],
            config: node.config || {}
          }
        })
        currentId++
      })
    }

    if (workflow.edges) {
      workflow.edges.forEach((edge: any) => {
        edges.value.push({
          source: edge.source_node,
          target: edge.target_node
        })
      })
    }
  } catch (error) {
    console.error('加载工作流失败:', error)
    alert('加载工作流失败')
  }
}

// 如果存在工作流ID，加载数据
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
  position: relative;
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

.node-config {
  position: absolute;
  top: 80px;
  right: 20px;
  width: 380px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,.15);
  z-index: 999;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

.form-item input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 28px;
  height: 28px;
  line-height: 1;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #333;
  background: #f0f0f0;
}

/* 标签行，flex 布局将标签和添加按钮放在同一行 */
.form-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.form-label-row label {
  font-weight: 600;
  margin-bottom: 0;
}

.add-var-btn-inline {
  padding: 2px 8px;
  font-size: 12px;
  background: #f5f7fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  color: #409eff;
  transition: all 0.2s;
}

.add-var-btn-inline:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

/* 变量列表样式 */
.variables-list {
  margin-bottom: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.variable-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.var-type {
  width: 90px;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.var-name {
  width: 100px;
  padding: 6px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.var-value {
  display: flex;
  gap: 4px;
  min-width: 200px;
  flex: 1;
}

.value-kind {
  width: 70px;
  padding: 6px;
  font-size: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.value-input {
  flex: 1;
  padding: 6px;
  font-size: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.remove-var-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #f56c6c;
  padding: 0 6px;
  line-height: 1;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-var-btn:hover {
  background: #fef0f0;
  color: #f00;
}

@media (max-width: 600px) {
  .node-config {
    width: 95%;
    right: 2.5%;
    left: 2.5%;
  }
  .variable-row {
    flex-direction: column;
    align-items: stretch;
  }
  .var-value {
    width: 100%;
  }
}
</style>