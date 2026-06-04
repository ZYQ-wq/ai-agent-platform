<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core"

// 定义节点数据的类型
interface NodeData {
  label: string
  type: string
  // 可以根据需要添加更多属性
}

defineProps<{
  data: NodeData
}>()
</script>

<template>
  <div
    class="workflow-node"
    :class="data.type"
  >

    <Handle
      type="target"
      :position="Position.Left"
    />

    <div class="title">

      {{ data.label }}

    </div>

    <div class="type">

      {{ data.type }}

    </div>

    <Handle
      type="source"
      :position="Position.Right"
    />

  </div>
</template>

<style scoped>

.workflow-node {

  min-width: 180px;

  padding: 12px;

  border-radius: 12px;

  border: 1px solid #ddd;

  background: white;

  box-shadow: 0 2px 8px rgba(0,0,0,.08);

}

.node-title {

  font-weight: bold;

  margin-bottom: 6px;

}

.node-type {

  color: #666;

  font-size: 13px;

}

.start {
  border: 2px solid #67c23a;
}

.llm {
  border: 2px solid #409eff;
}

.tool {
  border: 2px solid #e6a23c;
}

.output {
  border: 2px solid #f56c6c;
}
</style>