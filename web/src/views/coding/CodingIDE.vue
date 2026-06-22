<script setup lang="ts">
import { ref } from "vue";

import ProjectSidebar from "@/components/coding/ProjectSidebar.vue";
import CodingFileTree from "@/components/coding/CodingFileTree.vue";
import CodingEditor from "@/components/coding/CodingEditor.vue";

import {
  getProjectFiles,
  updateFile,
  runProject
} from "@/api/plugin";

const currentProject = ref<any>(null);

const files = ref<any[]>([]);

const currentFile = ref<any>(null);

const output = ref("");

const saveTimeout = ref<any>(null);

const selectFile = (
  file: any
) => {
  currentFile.value = file;
};

const onSelectProject = async (
  project: any
) => {
  currentProject.value = project;

  const res = await getProjectFiles(
    project.id
  );

  files.value = res;

  if (files.value.length > 0) {
    currentFile.value =
      files.value[0];
  }
};

const updateContent = (
  content: string
) => {

  if (!currentFile.value) {
    return;
  }

  currentFile.value.content =
    content;

  clearTimeout(
    saveTimeout.value
  );

  saveTimeout.value =
    setTimeout(async () => {

      try {

        await updateFile(
          currentFile.value.id,
          content
        );

        console.log(
          "自动保存成功"
        );

      } catch (error) {

        console.error(
          "保存失败",
          error
        );

      }

    }, 800);
};

const handleRun = async () => {

  if (!currentProject.value) {
    return;
  }

  try {

    output.value =
      "正在运行...\n";

    const res =
      await runProject(
        currentProject.value.id
      );

    output.value =
      (res.stdout || "") +
      (res.stderr || "");

  } catch (error) {

    console.error(error);

    output.value =
      "运行失败";

  }

};
</script>

<template>

  <div class="coding-layout">

    <!-- 项目列表 -->
    <ProjectSidebar
      @select-project="onSelectProject"
    />

    <!-- 文件树 -->
    <CodingFileTree
      :files="files"
      @select-file="selectFile"
    />

    <!-- 主区域 -->
    <div class="workspace">

      <!-- 顶部工具栏 -->
      <div class="toolbar">

        <div class="project-name">
          {{ currentProject?.name }}
        </div>

        <button
          class="run-btn"
          @click="handleRun"
        >
          ▶ Run
        </button>

      </div>

      <!-- 编辑器 -->
      <div class="editor-wrapper">

        <CodingEditor
          :file="currentFile"
          @update-content="
            updateContent
          "
        />

      </div>

      <!-- Console -->
      <div class="console">

        <div class="console-header">
          Console
        </div>

        <pre class="console-content">
{{ output }}
        </pre>

      </div>

    </div>

  </div>

</template>

<style scoped>
.coding-layout {
  height: 100vh;
  display: flex;
  overflow: hidden;
  background: #f8fafc;
}

.workspace {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.toolbar {
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 0 16px;

  border-bottom: 1px solid #e5e7eb;

  background: white;
}

.project-name {
  font-size: 14px;
  font-weight: 600;
}

.run-btn {
  border: none;

  padding: 8px 16px;

  border-radius: 8px;

  cursor: pointer;

  background: #2563eb;
  color: white;
}

.run-btn:hover {
  opacity: 0.9;
}

.editor-wrapper {
  flex: 1;
  overflow: hidden;
}

.console {
  height: 220px;

  border-top: 1px solid #e5e7eb;

  background: #111827;

  color: #22c55e;

  display: flex;
  flex-direction: column;
}

.console-header {
  height: 40px;

  display: flex;
  align-items: center;

  padding: 0 12px;

  color: white;

  border-bottom: 1px solid #374151;
}

.console-content {
  flex: 1;

  overflow: auto;

  margin: 0;

  padding: 12px;

  font-size: 13px;

  font-family:
    Consolas,
    Monaco,
    monospace;
}
</style>