<script setup lang="ts">

const props = defineProps<{
  files: any[]
}>()

const emit = defineEmits([
  "select-file"
])

const handleClick = (
  file: any
) => {
  emit(
    "select-file",
    file
  )
}

</script>

<template>

  <div class="file-tree">

    <div
      v-for="file in files"
      :key="file.id"
      class="file-item"
      @click="handleClick(file)"
    >
      {{ file.path }}
    </div>

  </div>

</template>

<style scoped>
.file-tree {
  height: 100%;
}

.file-item {
  padding: 8px 12px;
  cursor: pointer;
}

.file-item:hover {
  background: #f3f4f6;
}
</style>