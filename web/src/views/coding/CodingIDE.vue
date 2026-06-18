<script setup lang="ts">
import CodingToolbar from '@/components/coding/CodingToolbar.vue'
import CodingFileTree from '@/components/coding/CodingFileTree.vue'
import CodingEditor from '@/components/coding/CodingEditor.vue'
import CodingAssistant from '@/components/coding/CodingAssistant.vue'
import CodingConsole from '@/components/coding/CodingConsole.vue'
</script>

<template>

  <div class="coding-page">

    <CodingToolbar />

    <div class="workspace">

      <div class="left-panel">
        <CodingFileTree />
      </div>

      <div class="center-panel">
        <CodingEditor />
      </div>

      <div class="right-panel">
        <CodingAssistant />
      </div>

    </div>

    <div class="console-panel">
      <CodingConsole />
    </div>

  </div>

</template>

<style scoped>
.coding-page {
  height: 100vh;

  display: flex;
  flex-direction: column;
}

.workspace {
  flex: 1;

  display: flex;

  overflow: hidden;
}

.left-panel {
  width: 20%;
}

.center-panel {
  width: 55%;
}

.right-panel {
  width: 25%;

  border-left: 1px solid #ebeef5;
}

.console-panel {
  height: 220px;

  border-top: 1px solid #ebeef5;
}
</style>