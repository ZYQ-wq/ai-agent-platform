<script setup lang="ts">
import { ref, onMounted } from "vue";

import {
  getProjects,
  createProject as createProjectApi
} from "@/api/plugin";

const emit = defineEmits([
  "select-project"
]);

const projects = ref<any[]>([]);

const currentProjectId = ref("");

const loadProjects = async () => {
  try {

    const res = await getProjects();

    console.log(
      "项目列表",
      res
    );

    projects.value = res || [];

    if (projects.value.length > 0) {

      selectProject(
        projects.value[0]
      );

    }

  } catch (error) {

    console.error(
      "加载项目失败",
      error
    );

  }
};

const selectProject = (
  project: any
) => {

  currentProjectId.value =
    project.id;

  emit(
    "select-project",
    project
  );

};

const createProject = async () => {

  try {

    const projectName = prompt(
      "请输入项目名称"
    );

    if (!projectName) {
      return;
    }

    await createProjectApi({
      name: projectName,
      description: ""
    });

    await loadProjects();

  } catch (error) {

    console.error(
      "创建项目失败",
      error
    );

  }

};

onMounted(() => {
  loadProjects();
});
</script>

<template>
  <div class="project-sidebar">

    <div class="title">
      📦 我的插件
    </div>

    <div
      v-for="project in projects"
      :key="project.id"
      class="project-item"
      :class="{
        active:
          currentProjectId === project.id
      }"
      @click="selectProject(project)"
    >
      {{ project.name }}
    </div>

    <div class="divider"></div>

    <button
      class="create-btn"
      @click="createProject"
    >
      + 新建项目
    </button>

  </div>
</template>

<style scoped>
.project-sidebar {
  width: 260px;
  height: 100%;

  padding: 12px;

  border-right: 1px solid #e5e7eb;

  background: #ffffff;
}

.title {
  font-size: 14px;
  font-weight: 600;

  margin-bottom: 16px;
}

.project-item {
  padding: 10px;

  border-radius: 8px;

  cursor: pointer;

  margin-bottom: 6px;
}

.project-item:hover {
  background: #f3f4f6;
}

.project-item.active {
  background: #e0e7ff;
}

.divider {
  height: 1px;

  background: #e5e7eb;

  margin: 16px 0;
}

.create-btn {
  width: 100%;

  height: 38px;

  border: none;

  border-radius: 8px;

  cursor: pointer;

  background: #4f46e5;

  color: white;

  font-size: 14px;
}

.create-btn:hover {
  opacity: 0.9;
}
</style>