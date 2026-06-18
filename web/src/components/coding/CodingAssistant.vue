<script setup lang="ts">
import { ref } from 'vue'

const input = ref('')
</script>

<template>
  <div class="assistant">

    <div class="assistant-header">
      AI Assistant
    </div>

    <div class="assistant-body">

    </div>

    <div class="assistant-footer">

      <el-input
        v-model="input"
        placeholder="请输入需求..."
      />

    </div>

  </div>
</template>

<style scoped>
.assistant {
  height: 100%;

  display: flex;
  flex-direction: column;
}

.assistant-header {
  height: 48px;

  display: flex;
  align-items: center;

  padding: 0 12px;

  border-bottom: 1px solid #ebeef5;
}

.assistant-body {
  flex: 1;
}

.assistant-footer {
  padding: 12px;

  border-top: 1px solid #ebeef5;
}
</style>