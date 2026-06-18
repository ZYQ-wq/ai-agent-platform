<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCodingStore } from '@/stores/coding'

const store = useCodingStore()

const { currentFile } = storeToRefs(store)
</script>

<template>
  <div class="editor-container">

    <textarea
      v-if="currentFile"
      v-model="currentFile.content"
      class="editor"
    />

  </div>
</template>

<style scoped>
.editor-container {
  height: 100%;
}

.editor {
  width: 100%;
  height: 100%;

  border: none;
  outline: none;

  resize: none;

  padding: 16px;

  font-family: Consolas;
}
</style>