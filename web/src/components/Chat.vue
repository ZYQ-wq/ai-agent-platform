<template>
  <div class="chat-layout">
    <!-- 左侧：会话历史侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>💬 AI 对话</h3>
        <button @click="startNewChat" class="new-chat-btn">+ 新对话</button>
      </div>
      <div class="history-list">
        <!-- 后续可以在这里循环显示历史会话标题 -->
        <div class="history-item">对话 1</div>
        <div class="history-item">对话 2</div>
      </div>
      <div class="user-info">
        <span>👤 用户</span>
        <a href="#" @click.prevent="handleLogout" class="logout-link">退出登录</a>
      </div>
    </aside>

    <!-- 右侧：主聊天区域 -->
    <main class="chat-main">
      <!-- 聊天记录展示区 -->
      <div class="message-container" ref="messageContainerRef">
        <div v-if="messages.length === 0" class="empty-state">
          👋 你好！今天有什么我可以帮你的吗？
        </div>
        
        <div v-for="msg in messages" :key="msg.id" 
             class="message-bubble" 
             :class="msg.role === 'user' ? 'user-msg' : 'ai-msg'">
          <div class="avatar">{{ msg.role === 'user' ? 'U' : 'AI' }}</div>
          <div class="bubble-content">
            <p>{{ msg.content }}</p>
          </div>
        </div>

        <!-- 滚动到底部的锚点 -->
        <div ref="bottomRef"></div>
      </div>

      <!-- 底部输入区域 -->
      <div class="input-area">
        <textarea 
          v-model="inputText" 
          placeholder="请输入你想问的问题..." 
          @keydown.enter.exact.prevent="sendMessage"
          :disabled="isSending"
        ></textarea>
        <button @click="sendMessage" :disabled="!inputText.trim() || isSending">
          {{ isSending ? '思考中...' : '发送 ➤' }}
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

// --- 核心修复：配置 Axios 基础地址与正确路径 ---
// 创建专用的 apiClient，指向你的 FastAPI 后端端口
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', 
  timeout: 10000,
});

const inputText = ref('');
const isSending = ref(false);
const messages = ref([]);
const messageContainerRef = ref(null);
const bottomRef = ref(null);

// 1. 页面加载时，获取历史记录
const loadHistory = async () => {
  try {
    // ✅ 修正后的路径：对应 main.py 中的 prefix="/chat"
    const res = await apiClient.get('/chat/history'); 
    messages.value = res.data;
  } catch (error) {
    console.error('获取历史失败:', error);
    alert('无法连接到服务器，请检查后端是否启动');
  }
};

// 2. 发送消息函数
const sendMessage = async () => {
  if (!inputText.value.trim() || isSending.value) return;

  const userMsg = {
    content: inputText.value // 使用正确的变量名
  };

  const tempId = Date.now();
  messages.value.push({
    id: tempId,
    role: 'user',
    content: inputText.value
  });

  inputText.value = '';
  isSending.value = true;

  try {
    // ✅ 修正后的路径：对应 main.py 中的 prefix="/chat"
    const res = await apiClient.post('/chat/send', userMsg);
    
    // 将后端返回的 AI 回复推入消息列表
    messages.value.push({
      id: res.data.id || tempId + 1, 
      role: 'assistant',
      content: res.data.response 
    });
    
  } catch (error) {
    console.error('发送失败:', error);
    // 如果发送失败，移除刚才添加的用户消息
    messages.value = messages.value.filter(m => m.id !== tempId); 
    alert('消息发送失败，请重试');
  } finally {
    isSending.value = false;
  }
};

// 3. 自动滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (bottomRef.value) {
      bottomRef.value.scrollIntoView({ behavior: 'smooth' });
    }
  });
};

// 4. 监听消息变化，自动滚动
import { watchEffect } from 'vue';
watchEffect(() => {
  scrollToBottom();
});

// 5. 页面挂载时加载历史
onMounted(() => {
  loadHistory();
});

// 6. 退出登录
const handleLogout = () => {
  localStorage.removeItem('access_token');
  router.push('/login');
};

// 7. 开启新对话 
const startNewChat = () => {
  messages.value = [];
};
</script>

<style scoped>
/* 样式部分保持不变，为了节省篇幅，这里省略，实际使用时请保留之前的样式代码 */
/* ... (保持之前的 CSS 不变) ... */
.chat-layout {
  display: flex;
  height: 100vh;
  background-color: #f7f7f8;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.sidebar {
  width: 260px;
  background-color: #202123;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.new-chat-btn {
  background: transparent;
  border: 1px solid #4d4d4f;
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.2s;
}
.new-chat-btn:hover { background: #343541; }

.history-list {
  flex: 1;
  overflow-y: auto;
  margin-top: 20px;
}

.history-item {
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  color: #ececf1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.history-item:hover { background-color: #2a2b32; }

.user-info {
  border-top: 1px solid #4d4d4f;
  padding-top: 10px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}
.logout-link { color: #ececf1; text-decoration: none; }

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 15%;
}

.empty-state {
  text-align: center;
  margin-top: 20%;
  color: #8e8ea0;
  font-size: 18px;
}

.message-bubble {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 12px;
  flex-shrink: 0;
}

.user-msg .avatar { background-color: #5436da; color: white; }
.ai-msg .avatar { background-color: #10a37f; color: white; }

.bubble-content p {
  margin: 0;
  line-height: 1.6;
  color: #374151;
}

.input-area {
  padding: 20px 15%;
  background-color: #f7f7f8;
  display: flex;
  gap: 10px;
}

.input-area textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  height: 50px;
  outline: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.input-area button {
  padding: 0 20px;
  background-color: #10a37f;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
.input-area button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>