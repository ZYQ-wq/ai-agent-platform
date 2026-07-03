<script setup lang="ts">
import { ref,onMounted } from "vue";

import ProjectSidebar from "@/components/coding/ProjectSidebar.vue";
import CodingFileTree from "@/components/coding/CodingFileTree.vue";
import CodingEditor from "@/components/coding/CodingEditor.vue";
import CopilotPanel from "@/components/coding/CopilotPanel.vue";
import AgentChatPanel from "@/components/coding/AgentChatPanel.vue";

import {
  getProjectFiles,
  updateFile,
  runProject,
  createFile,
  renameFile,
  deleteFile,
  agentChat,
  applyChanges
} from "@/api/plugin";

import {
  generateCode
} from "@/api/codegen";

import {
  validateManifest,
  editCode
} from "@/api/plugin";

import {
  getAgents
} from "@/api/agent";

import {
  bindAgent
} from "@/api/plugin";


const currentProject = ref<any>(null);

const files = ref<any[]>([]);

const currentFile = ref<any>(null);

const output = ref("");

const agents = ref<any[]>([]);

const selectedAgentId =
  ref<number | null>(null);

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
  selectedAgentId.value =project.agent_id;

  const res =
    await getProjectFiles(
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

    if (currentFile.value?.content != null) {
      clearTimeout(saveTimeout.value);
      await updateFile(
        currentFile.value.id,
        currentFile.value.content
      );
    }

    const res =
      await runProject(
        currentProject.value.id
      );

    output.value =
      (res.stdout || "") +
      (res.stderr || "");

    if (res.preview_url) {
      window.open(
        res.preview_url,
        "_blank"
      );
    }

  } catch (error) {

    console.error(error);

    output.value =
      "运行失败";

  }

};

const handleGenerate = async () => {

  if (!currentProject.value) {
    return;
  }

  if (!currentFile.value) {
    alert(
      "请先选择一个文件"
    );
    return;
  }

  const prompt =
    window.prompt(
      "请输入需求"
    );

  if (!prompt) {
    return;
  }

  try {

    const res =
      await generateCode(
        currentProject.value.id,
        prompt
      );

    currentFile.value.content =
      res.content;

    await updateFile(
      currentFile.value.id,
      res.content
    );

    alert("生成完成");

  } catch (error) {

    console.error(error);

    alert("生成失败");

  }

};

const handleCreateFile =
  async () => {

    if (!currentProject.value) {
      return;
    }

    const filename =
      window.prompt(
        "请输入文件名"
      );

    if (!filename) {
      return;
    }

    try {

      await createFile(
        currentProject.value.id,
        filename
      );

      const res =
        await getProjectFiles(
          currentProject.value.id
        );

      files.value = res;

    } catch (error) {

      console.error(error);

      alert("创建失败");

    }
};

const handleRenameFile =
  async (
    file: any
  ) => {

    const newName =
      window.prompt(
        "新文件名",
        file.path
      );

    if (
      !newName ||
      newName === file.path
    ) {
      return;
    }

    await renameFile(
      file.id,
      newName
    );

    const res =
      await getProjectFiles(
        currentProject.value.id
      );

    files.value = res;

};

const handleDeleteFile =
  async (
    file: any
  ) => {

    const ok =
      confirm(
        `删除 ${file.path} ?`
      );

    if (!ok) {
      return;
    }

    await deleteFile(
      file.id
    );

    const res =
      await getProjectFiles(
        currentProject.value.id
      );

    files.value = res;

    if (
      currentFile.value?.id ===
      file.id
    ) {

      currentFile.value =
        files.value[0] || null;

    }

};

const handleValidate =
  async () => {

  if (!currentProject.value)
    return;

  const res =
    await validateManifest(
      currentProject.value.id
    );

  if (res.valid) {

    output.value =
      "✅ plugin.yaml 验证通过";

  } else {

    output.value =
      "❌ plugin.yaml 错误\n\n" +
      res.errors.join("\n");

  }

};

const handleEditCode =
  async () => {

  if (!currentFile.value) {
    return;
  }

  const prompt =
    window.prompt(
      "修改要求"
    );

  if (!prompt) {
    return;
  }

  const res =
    await editCode(
      currentFile.value.content,
      prompt
    );

  currentFile.value.content =
    res.content;

  await updateFile(
    currentFile.value.id,
    res.content
  );

};

const handleCopilot =
  async (
    prompt: string
  ) => {

  if (!currentFile.value) {
    return;
  }

  const res =
    await editCode(
      currentFile.value.content,
      prompt
    );

  currentFile.value.content =
    res.content;

  await updateFile(
    currentFile.value.id,
    res.content
  );
};

const handleBindAgent =
  async () => {

  if (!currentProject.value) {
    return;
  }

  try {

    await bindAgent(
      currentProject.value.id,
      selectedAgentId.value
    );

    alert(
      "Agent绑定成功"
    );

  } catch (error) {

    console.error(error);

    alert(
      "绑定失败"
    );

  }

};

onMounted(async () => {

  try {

    const res =
      await getAgents();

    agents.value = res;

  } catch (error) {

    console.error(
      "获取Agent失败",
      error
    );

  }

});

const messages = ref<any[]>([]);

const pendingChanges = ref<any[]>([]);

const agentLoading = ref(false);

const isRequestTimeout = (error: unknown) => {
  const err = error as {
    code?: string;
    message?: string;
  };

  return (
    err?.code === "ECONNABORTED" ||
    (err?.message || "").includes("timeout")
  );
};

function parseAgentFiles(
  text: string
) {

  const files = [];

  const regex =
    /FILE:\s*(.*?)\nACTION:\s*(.*?)\n([\s\S]*?)(?=\nFILE:|\s*$)/g;

  let match;

  while (
    (match = regex.exec(text))
    !== null
  ) {

    files.push({
      path:
        match[1].trim(),

      action:
        match[2].trim(),

      content:
        match[3].trim()
    });

  }

  return files;
}

const handleAgentMessage =
  async (
    prompt: string
  ) => {

  if (!currentProject.value) {
    return;
  }

  messages.value.push({
    role: "user",
    content: prompt
  });

  agentLoading.value = true;

  try {

    const res =
      await agentChat(
        currentProject.value.id,
        prompt
      );

    messages.value.push({
      role: "assistant",
      content: res.message || "Agent 已完成分析"
    });

    pendingChanges.value = res.files || [];

    if (
      pendingChanges.value.length > 0 &&
      pendingChanges.value.some(
        (file: any) =>
          file.action === "delete" ||
          (file.content || "").trim()
      )
    ) {
      await handleApplyChanges();
    }

  } catch (error) {

    console.error(error);

    messages.value.push({
      role: "assistant",
      content: isRequestTimeout(error)
        ? "Agent 生成超时。复杂应用可能需要 1-3 分钟，请稍后重试。"
        : "Agent 执行失败，请检查后端日志后重试。"
    });

  } finally {
    agentLoading.value = false;
  }

};

const handleApplyChanges =
  async () => {

  if (!currentProject.value) {
    return;
  }

  if (
    pendingChanges.value.length === 0
  ) {
    return;
  }

  try {

    await applyChanges(
      currentProject.value.id,
      pendingChanges.value
    );

    const res =
      await getProjectFiles(
        currentProject.value.id
      );

    files.value = res;

    pendingChanges.value = [];

    messages.value.push({
      role: "assistant",
      content:
        "✅ 变更已应用到项目"
    });

  } catch (error) {

    console.error(error);

    alert("应用失败");

  }

};

</script>

<template>

  <div class="coding-layout">

    <!-- 左侧项目栏 -->
    <ProjectSidebar
      @select-project="onSelectProject"
    />

    <!-- 文件树 -->
    <CodingFileTree
      :files="files"
      :current-file-id="
        currentFile?.id
      "
      @select-file="selectFile"
      @create-file="handleCreateFile"
      @delete-file="handleDeleteFile"
      @rename-file="handleRenameFile"
    />

    <!-- 工作区 -->
    <div class="workspace">

      <!-- 顶部工具栏 -->
      <div class="toolbar">

        <div class="toolbar-left">
          <router-link to="/plaza" class="back-link">
            ← 返回广场
          </router-link>

          <div class="project-name">
            {{ currentProject?.name || "AI 编程" }}
          </div>
        </div>

        <div class="actions">

          <select
            v-model="selectedAgentId"
            @change="handleBindAgent"
            class="agent-select"
          >

            <option :value="null">
              不绑定Agent
            </option>

            <option
              v-for="agent in agents"
              :key="agent.id"
              :value="agent.id"
            >
              {{ agent.name }}
            </option>

          </select>

          <button
            class="ai-btn"
            @click="handleGenerate"
          >
            🤖 AI生成
          </button>

          <button
            class="run-btn"
            @click="handleRun"
          >
            ▶ Run
          </button>

          <button
            class="validate-btn"
            @click="handleValidate"
          >
            Validate
          </button>

          <button
            class="ai-btn"
            @click="handleEditCode"
          >
            ✨ AI修改
          </button>

        </div>

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

    <AgentChatPanel
      :messages="messages"
      :pending-changes="
        pendingChanges
      "
      :loading="agentLoading"
      @send-message="
        handleAgentMessage
      "
      @apply-changes="
        handleApplyChanges
      "
    />

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

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
}

.back-link {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
  white-space: nowrap;
}

.back-link:hover {
  text-decoration: underline;
}

.project-name {
  font-size: 14px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 10px;
}

.ai-btn {
  border: none;

  padding: 8px 16px;

  border-radius: 8px;

  cursor: pointer;

  background: #7c3aed;
  color: white;
}

.ai-btn:hover {
  opacity: 0.9;
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
.agent-select {
  height: 36px;

  padding: 0 10px;

  border: 1px solid #d1d5db;

  border-radius: 8px;

  background: white;

  cursor: pointer;
}
</style>