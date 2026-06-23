<script setup lang="ts">

const props = defineProps<{
  files: any[]
  currentFileId?:string
}>()

const emit = defineEmits([
  "select-file",
  "create-file",
  "delete-file",
  "rename-file"
]);

const handleCreate = () => {
  emit("create-file");
};

const handleClick = (
  file: any
) => {
  emit(
    "select-file",
    file
  )
};
const handleRename = (
  file: any
) => {

  emit(
    "rename-file",
    file
  );

};

const handleDelete = (
  file: any
) => {

  emit(
    "delete-file",
    file
  );

};

</script>

<template>

  <div class="file-tree">

    <div class="toolbar">

      <button
        @click="handleCreate"
      >
        + File
      </button>

    </div>

    <div class="file-list">

      <div
        v-for="file in files"
        :key="file.id"
        class="file-item"
        :class="{
          active:
            file.id ===
            currentFileId
        }"
      >
        <span
          class="file-name"
          @click="handleClick(file)"
        >
          {{ file.path }}
        </span>

        <div class="actions">

          <button
            @click.stop="
              handleRename(file)
            "
          >
            ✏️
          </button>

          <button
            @click.stop="
              handleDelete(file)
            "
          >
            🗑️
          </button>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.file-tree {
  width: 260px;

  border-right: 1px solid #e5e7eb;

  background: white;

  display: flex;

  flex-direction: column;
}

.toolbar {
  padding: 12px;

  border-bottom: 1px solid #e5e7eb;
}

.toolbar button {
  width: 100%;

  border: none;

  padding: 10px;

  border-radius: 8px;

  background: #7c3aed;

  color: white;

  cursor: pointer;
}

.file-list {
  flex: 1;

  overflow-y: auto;

  padding: 8px;
}

.file-item {

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 8px 10px;

  border-radius: 6px;

  margin-bottom: 4px;
}

.file-item:hover {
  background: #f3f4f6;
}

.file-name {
  flex: 1;

  cursor: pointer;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;
}

.actions {
  display: flex;

  gap: 4px;
}

.actions button {
  border: none;

  background: transparent;

  cursor: pointer;

  padding: 2px 4px;
}
.active {
  background: #dbeafe;
}

.active .file-name {
  color: #2563eb;
  font-weight: 600;
}

</style>