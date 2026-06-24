<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits([
  "send-message",
  "apply-changes"
]);

defineProps<{
  messages: any[];
  pendingChanges: any[];
}>();

const input = ref("");

const send = () => {

  if (!input.value.trim()) {
    return;
  }

  emit(
    "send-message",
    input.value
  );

  input.value = "";
};
</script>

<template>

  <div class="agent-chat">

    <div class="chat-header">
      Agent
    </div>

    <div class="messages">

      <div
        v-for="(
          msg,
          index
        ) in messages"
        :key="index"
        class="message"
        :class="msg.role"
      >

        <div class="role">
          {{ msg.role }}
        </div>

        <div class="content">
          {{ msg.content }}
        </div>

      </div>

    </div>

    <div
      v-if="
        pendingChanges.length
      "
      class="changes"
    >

      <div class="changes-title">
        待应用变更
      </div>

      <div
        v-for="(
          file,
          index
        ) in pendingChanges"
        :key="index"
        class="change-item"
      >

        <div>
          {{ file.action }}
        </div>

        <div>
          {{ file.path }}
        </div>

      </div>

      <button
        class="apply-btn"
        @click="
          emit(
            'apply-changes'
          )
        "
      >
        Apply Changes
      </button>

    </div>

    <div class="input-area">

      <textarea
        v-model="input"
        placeholder="
请输入需求...
"
      />

      <button
        @click="send"
      >
        Send
      </button>

    </div>

  </div>

</template>

<style scoped>

.agent-chat{
  width:400px;
  border-left:1px solid #e5e7eb;

  display:flex;
  flex-direction:column;

  background:white;
}

.chat-header{
  height:52px;

  display:flex;
  align-items:center;

  padding:0 16px;

  border-bottom:
    1px solid #e5e7eb;

  font-weight:600;
}

.messages{
  flex:1;

  overflow:auto;

  padding:12px;
}

.message{
  margin-bottom:12px;
}

.role{
  font-size:12px;
  color:#6b7280;
}

.content{
  margin-top:4px;

  background:#f3f4f6;

  padding:10px;

  border-radius:8px;
}

.changes{
  border-top:
    1px solid #e5e7eb;

  padding:12px;
}

.change-item{
  display:flex;
  justify-content:
    space-between;

  margin-top:6px;

  font-size:13px;
}

.apply-btn{
  width:100%;

  margin-top:10px;

  padding:10px;

  border:none;

  border-radius:8px;

  background:#10b981;
  color:white;

  cursor:pointer;
}

.input-area{
  border-top:
    1px solid #e5e7eb;

  padding:12px;
}

textarea{
  width:100%;

  height:90px;

  resize:none;
}

button{
  margin-top:8px;

  width:100%;
}
</style>