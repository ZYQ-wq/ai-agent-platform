<template>
  <div class="workflow-node">

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

<script setup lang="ts">
import { Handle, Position } from "@vue-flow/core"

defineProps({
  data: Object
})
</script>

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
</style>