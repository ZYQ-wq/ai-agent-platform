<template>
  <div class="upload-page">

    <!-- 标题 -->
    <h2>📤 知识库上传</h2>

    <!-- Step -->
    <div class="steps">
      <div :class="step === 1 ? 'active' : ''">1. 上传文件</div>
      <div :class="step === 2 ? 'active' : ''">2. 切片预览</div>
    </div>

    <!-- ========================= -->
    <!-- STEP 1：上传文件 -->
    <!-- ========================= -->
    <div v-if="step === 1" class="step-box">

      <input type="file" @change="handleFile" />

      <p v-if="file">
        已选择：{{ file.name }}
      </p>

      <button
        :disabled="!file"
        @click="uploadFile"
      >
        上传并解析
      </button>

    </div>

    <!-- ========================= -->
    <!-- STEP 2：切片预览 -->
    <!-- ========================= -->
    <div v-if="step === 2" class="step-box">

      <h3>📄 切片预览</h3>

      <div class="chunk-list">

        <div
          class="chunk"
          v-for="(c, i) in chunks"
          :key="i"
        >
          {{ c }}
        </div>

      </div>

      <button @click="confirmSave">
        确认保存到知识库
      </button>

    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"

export default defineComponent({

  setup() {

    const route = useRoute()
    const router = useRouter()

    const kbId = route.params.id

    const step = ref(1)

    const file = ref<File | null>(null)

    const chunks = ref<string[]>([])

    const authHeader = () => ({
      Authorization: `Bearer ${localStorage.getItem("token")}`
    })

    // =========================
    // 选择文件
    // =========================
    const handleFile = (e: any) => {
      file.value = e.target.files[0]
    }

    // =========================
    // 上传 + 切片（核心）
    // =========================
    const uploadFile = async () => {

      if (!file.value) return

      const formData = new FormData()
      formData.append("file", file.value)

      const res = await axios.post(
        `http://127.0.0.1:8000/kb/upload/${kbId}`,
        formData,
        {
          headers: {
            ...authHeader(),
            "Content-Type": "multipart/form-data"
          }
        }
      )

      // 假设后端返回 chunks
      chunks.value = res.data.data.chunks || []

      step.value = 2
    }

    // =========================
    // 确认保存
    // =========================
    const confirmSave = async () => {

      await axios.post(
        `http://127.0.0.1:8000/kb/confirm/${kbId}`,
        {},
        { headers: authHeader() }
      )

      router.push("/kb")
    }

    return {
      step,
      file,
      chunks,
      handleFile,
      uploadFile,
      confirmSave
    }
  }

})
</script>

<style scoped>
.upload-page {
  padding: 24px;
}

.steps {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.steps div {
  padding: 8px 12px;
  border-radius: 8px;
  background: #eee;
}

.steps .active {
  background: #409eff;
  color: white;
}

.step-box {
  margin-top: 20px;
}

.chunk-list {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chunk {
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
}
</style>