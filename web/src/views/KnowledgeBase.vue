<template>
  <div class="kb-container">

    <h2>📚 知识库</h2>

    <!-- 上传 -->
    <div class="upload-box">
      <input type="file" @change="handleFile" />
      <button @click="uploadFile">上传文件</button>
    </div>

    <!-- 列表 -->
    <div class="file-list">
      <div v-for="item in files" :key="item.id" class="file-item">
        📄 {{ item.name }} ({{ item.file_type }})
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const files = ref([])
const selectedFile = ref(null)

const authHeader = () => ({
  Authorization: `Bearer ${localStorage.getItem("token")}`
})

const handleFile = (e) => {
  selectedFile.value = e.target.files[0]
}

const uploadFile = async () => {

  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append("file", selectedFile.value)

  await axios.post(
    "http://127.0.0.1:8000/kb/upload",
    formData,
    { headers: authHeader() }
  )

  loadFiles()
}

const loadFiles = async () => {

  const res = await axios.get(
    "http://127.0.0.1:8000/kb/list",
    { headers: authHeader() }
  )

  files.value = res.data
}

onMounted(() => {
  loadFiles()
})
</script>

<style scoped>
.kb-container {
  padding: 20px;
}

.upload-box {
  margin-bottom: 20px;
}

.file-list {
  margin-top: 20px;
}

.file-item {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
</style>