<template>
  <div class="kb-detail">

    <!-- 顶部 -->
    <div class="header">
      <h2>📚 知识库详情</h2>

      <button @click="goUpload">
        + 上传文件
      </button>

    </div>

    <!-- KB信息 -->
    <div class="kb-info">
      <h3>{{ kb.name }}</h3>
      <p>{{ kb.description }}</p>
    </div>

    <!-- Chunk区域 -->
    <div class="chunk-section">

      <h3>📦 Chunk列表</h3>

      <div v-if="chunks.length === 0">
        暂无chunk数据
      </div>

      <div
        class="chunk-card"
        v-for="chunk in chunks"
        :key="chunk.id"
      >

        <div class="chunk-content">
          {{ chunk.content }}
        </div>

        <div class="chunk-actions">

          <button @click="viewChunk(chunk)">
            查看
          </button>

          <button class="danger" @click="deleteChunk(chunk.id)">
            删除
          </button>

        </div>

      </div>

    </div>

    <!-- Chunk弹窗 -->
    <div v-if="selectedChunk" class="modal">

      <div class="modal-content">

        <h3>Chunk内容</h3>

        <p>{{ selectedChunk.content }}</p>

        <button @click="selectedChunk = null">
          关闭
        </button>

      </div>

    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"

export default defineComponent({

  setup() {

    const route = useRoute()
    const router = useRouter()

    const kbId = route.params.id

    const kb = ref<any>({})

    const chunks = ref<any[]>([])

    const selectedChunk = ref<any>(null)

    const authHeader = () => ({
      Authorization: `Bearer ${localStorage.getItem("token")}`
    })

    // =========================
    // 加载KB详情
    // =========================
    const loadKB = async () => {

      const res = await axios.get(
        `http://127.0.0.1:8000/kb/${kbId}`,
        { headers: authHeader() }
      )

      kb.value = res.data.data
    }

    // =========================
    // 加载chunk列表
    // =========================
    const loadChunks = async () => {

      const res = await axios.get(
        `http://127.0.0.1:8000/kb/${kbId}`,
        { headers: authHeader() }
      )

      chunks.value = res.data.data
    }

    // =========================
    // 删除chunk
    // =========================
    const deleteChunk = async (id: number) => {

      await axios.delete(
        `http://127.0.0.1:8000/kb/chunk/${id}`,
        { headers: authHeader() }
      )

      await loadChunks()
    }

    // =========================
    // 查看chunk
    // =========================
    const viewChunk = (chunk: any) => {
      selectedChunk.value = chunk
    }

    // =========================
    // 跳转上传
    // =========================
    const goUpload = () => {
      router.push(`/kb/upload/${kbId}`)
    }

    onMounted(() => {
      loadKB()
      loadChunks()
    })

    return {
      kb,
      chunks,
      selectedChunk,
      deleteChunk,
      viewChunk,
      goUpload
    }
  }

})
</script>

<style scoped>
.kb-detail {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.kb-info {
  margin: 20px 0;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.chunk-section {
  margin-top: 20px;
}

.chunk-card {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
}

.chunk-content {
  font-size: 14px;
  margin-bottom: 8px;
}

.chunk-actions {
  display: flex;
  gap: 8px;
}

.danger {
  color: red;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
}
</style>