<script setup lang="ts">

import { updateFile } from "@/api/plugin";

const props = defineProps<{
  file: any
}>();

const saveFile = async () => {

  if (!props.file) {
    return;
  }

  await updateFile(
    props.file.id,
    props.file.content
  );

  alert("保存成功");
};

</script>

<template>

  <div class="editor">

    <div
      v-if="file"
      class="editor-body"
    >

      <div class="editor-header">

        <div>
          {{ file.path }}
        </div>

        <button
          class="save-btn"
          @click="saveFile"
        >
          保存
        </button>

      </div>

      <textarea
        v-model="file.content"
      />

    </div>

    <div
      v-else
      class="empty"
    >
      请选择文件
    </div>

  </div>

</template>

<style scoped>

.editor {
  height: 100%;
}

.editor-title {
  height: 40px;

  display: flex;
  align-items: center;

  border-bottom: 1px solid #e5e7eb;

  padding-left: 12px;
}

textarea {
  width: 100%;
  height: calc(100vh - 140px);

  border: none;
  outline: none;

  resize: none;

  font-family: Consolas;
}

.empty {
  padding: 20px;
}

.editor-header {
  height: 44px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 0 12px;

  border-bottom: 1px solid #e5e7eb;
}

.save-btn {
  border: none;

  background: #4f46e5;

  color: white;

  border-radius: 6px;

  padding: 6px 12px;

  cursor: pointer;
}

</style>