<script setup lang="ts">
import { useCodingStore } from '@/stores/coding'

const store = useCodingStore()
</script>

<template>
  <div class="console">

    <div
      v-for="(log,index) in store.consoleLogs"
      :key="index"
    >
      {{ log }}
    </div>

  </div>
</template>

<style scoped>
.console {
  height: 100%;

  background: #1e1e1e;

  color: #00ff66;

  padding: 12px;

  overflow-y: auto;
}
</style>