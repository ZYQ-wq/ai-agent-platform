<script setup lang="ts">
import { useCodingStore } from '@/stores/coding'

const store = useCodingStore()

const selectFile = (file: any) => {
  store.currentFile = file
}
</script>

<template>
  <div class="file-tree">

    <div
      v-for="file in store.project?.files || []"
      :key="file.path"
      class="file-item"
      @click="selectFile(file)"
    >
      {{ file.path }}
    </div>

  </div>
</template>

<style scoped>
.file-tree {
  height: 100%;

  border-right: 1px solid #ebeef5;
}

.file-item {
  padding: 10px 12px;

  cursor: pointer;
}

.file-item:hover {
  background: #f5f7fa;
}
</style>