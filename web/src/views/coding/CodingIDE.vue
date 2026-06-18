<script setup lang="ts">
import { ref } from "vue";

import ProjectSidebar from "@/components/coding/ProjectSidebar.vue";
import CodingFileTree from "@/components/coding/CodingFileTree.vue";
import CodingEditor from "@/components/coding/CodingEditor.vue";

import { getProjectFiles } from "@/api/plugin";

const currentProject = ref<any>(null);

const files = ref<any[]>([]);

const currentFile = ref<any>(null);

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

  currentFile.value = null;
};
</script>

<template>

  <div class="coding-layout">

    <ProjectSidebar
      @select-project="onSelectProject"
    />

    <CodingFileTree
      :files="files"
      @select-file="selectFile"
    />

    <CodingEditor
      :file="currentFile"
    />

  </div>

</template>

<style scoped>

.coding-layout {
  height: 100vh;
  display: flex;
}

</style>