<template>
  <div class="workflow-node">
    <!-- 节点头部：名称 + 类型标识 -->
    <div class="node-header">
      <div class="node-name">{{ data.label }}</div>
      <div v-if="data.nodeType" class="node-type-badge">{{ data.nodeType }}</div>
      <div v-else-if="data.tag" class="node-type-badge">{{ data.tag }}</div>
    </div>

    <!-- 输入区域 -->
    <div class="vars-section inputs-section">
      <div class="vars-title">
        <span class="title-icon">▶</span> 输入
      </div>
      <div class="vars-list">
        <template v-if="data.inputs && data.inputs.length">
          <div v-for="item in data.inputs" :key="item.name" class="var-item">
            <span class="var-type-bracket">
              {{ item.type ? '{' + item.type + '}' : '{}' }}
            </span>
            <span class="var-name">{{ item.name }}</span>
          </div>
        </template>
        <div v-else class="var-placeholder">
          未配置输入
        </div>
      </div>
    </div>

    <!-- 输出区域 -->
    <div class="vars-section outputs-section">
      <div class="vars-title">
        <span class="title-icon">▼</span> 输出
      </div>
      <div class="vars-list">
        <template v-if="data.outputs && data.outputs.length">
          <div v-for="item in data.outputs" :key="item.name" class="var-item">
            <span class="var-type-bracket">
              {{ item.type ? '{' + item.type + '}' : '{}' }}
            </span>
            <span class="var-name">{{ item.name }}</span>
          </div>
        </template>
        <div v-else class="var-placeholder">
          未配置输出
        </div>
      </div>
      <div v-if="data.extraOutputInfo" class="extra-output-info">
        {{ data.extraOutputInfo }}
      </div>
      <div v-else-if="data.showReturnHint" class="extra-output-info">
        输出类型 · 返回变量
      </div>
    </div>

    <Handle type="target" :position="Position.Left" />
    <Handle type="source" :position="Position.Right" />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core"

defineProps({
  data: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.workflow-node {
  min-width: 220px;
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  transition: all 0.2s ease;
}

.workflow-node:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  border-color: #cbd5e1;
}

.node-header {
  padding: 12px 16px 8px 16px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.node-name {
  font-weight: 700;
  font-size: 15px;
  color: #1e293b;
  letter-spacing: -0.2px;
}

.node-type-badge {
  font-size: 11px;
  font-weight: 500;
  background: #f1f5f9;
  color: #475569;
  padding: 2px 8px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.vars-section {
  padding: 8px 16px 12px 16px;
}

.inputs-section {
  border-bottom: 1px solid #f1f5f9;
}

.outputs-section {
  padding-top: 8px;
}

.vars-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #3b82f6;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.title-icon {
  font-size: 10px;
  opacity: 0.7;
}

.vars-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.var-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
  font-size: 13px;
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 10px;
  border-left: 2px solid #e2e8f0;
  transition: all 0.1s;
}

.var-item:hover {
  background: #f1f5f9;
  border-left-color: #3b82f6;
}

.var-type-bracket {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-weight: 500;
  color: #8b5cf6;
  background: #ede9fe;
  padding: 0px 6px;
  border-radius: 14px;
  font-size: 11px;
  letter-spacing: 0.2px;
  line-height: 20px;
  white-space: nowrap;
}

.var-name {
  font-weight: 500;
  color: #0f172a;
  word-break: break-word;
  font-size: 12.5px;
}

.var-placeholder {
  font-size: 12px;
  color: #94a3b8;
  font-style: italic;
  padding: 4px 0 4px 4px;
  background: transparent;
  letter-spacing: 0.2px;
}

.extra-output-info {
  margin-top: 10px;
  font-size: 11px;
  color: #64748b;
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 8px;
  border-top: 1px dashed #e2e8f0;
  text-align: center;
  font-family: monospace;
}

:deep(.vue-flow__handle) {
  width: 10px;
  height: 10px;
  background: #94a3b8;
  border: 2px solid white;
  transition: 0.1s;
}

:deep(.vue-flow__handle:hover) {
  background: #3b82f6;
  transform: scale(1.2);
}
</style>