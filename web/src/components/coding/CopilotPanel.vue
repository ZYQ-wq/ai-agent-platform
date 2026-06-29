<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits([
  "send-message"
]);

const prompt = ref("");

const handleSend = () => {

  if (!prompt.value.trim()) {
    return;
  }

  emit(
    "send-message",
    prompt.value
  );

  prompt.value = "";
};
</script>

<template>
  <div class="copilot">

    <div class="title">
      AI Copilot
    </div>

    <textarea
      v-model="prompt"
      placeholder="请输入需求..."
    />

    <button
      @click="handleSend"
    >
      发送
    </button>

  </div>
</template>

<style scoped>
.copilot {
  width: 320px;

  border-left: 1px solid #e5e7eb;

  display: flex;
  flex-direction: column;

  padding: 12px;
}

.title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

textarea {
  flex: 1;

  resize: none;

  border: 1px solid #ddd;

  padding: 10px;
}

button {
  margin-top: 12px;

  height: 40px;

  border: none;

  background: #2563eb;

  color: white;

  cursor: pointer;
}
</style>