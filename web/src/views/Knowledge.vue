<template>
  <div class="kb-page">

    <!-- 顶部 -->
    <div class="header">
      <div class="header-left">
        <router-link to="/plaza" class="back-link">← 返回广场</router-link>
        <h2>📚 我的知识库</h2>
      </div>

      <button class="create-btn" @click="showCreate = true">
        + 新建知识库
      </button>
    </div>

    <!-- 列表 -->
    <div class="kb-list">

      <div
        class="kb-card"
        v-for="kb in kbList"
        :key="kb.id"
      >

        <div class="kb-title">
          {{ kb.name }}
        </div>

        <div class="kb-meta">
          类型：{{ kb.file_type || '未上传' }}
        </div>

        <div class="kb-actions">

          <button @click="goManage(kb.id)">
            管理
          </button>

          <button class="danger" @click="deleteKb(kb.id)">
            删除
          </button>

        </div>

      </div>

    </div>

    <!-- 创建弹窗 -->
    <div v-if="showCreate" class="modal">

      <div class="modal-content">

        <h3>创建知识库</h3>

        <input v-model="form.name" placeholder="知识库名称" />

        <textarea v-model="form.description" placeholder="简介" />

        <div class="modal-actions">
          <button @click="createKb">保存</button>
          <button @click="showCreate = false">取消</button>
        </div>

      </div>

    </div>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

export default defineComponent({

  setup() {

    const router = useRouter()

    const kbList = ref<any[]>([])

    const showCreate = ref(false)

    const form = ref({
      name: "",
      description: ""
    })

    const authHeader = () => ({
      Authorization: `Bearer ${localStorage.getItem("token")}`
    })

    // =====================
    // 获取列表
    // =====================
    const loadKB = async () => {

      try {

        const res = await axios.get(
          "http://127.0.0.1:8000/kb/list",
          { headers: authHeader() }
        )

        kbList.value = res.data?.data || []

      } catch (error) {

        console.error(error)
        kbList.value = []

      }
    }

    // =====================
    // 创建KB
    // =====================
    const createKb = async () => {

      await axios.post(
        "http://127.0.0.1:8000/kb/create",
        form.value,
        { headers: authHeader() }
      )

      showCreate.value = false
      form.value = { name: "", description: "" }

      await loadKB()
    }

    // =====================
    // 删除KB
    // =====================
    const deleteKb = async (id: number) => {

      await axios.delete(
        `http://127.0.0.1:8000/kb/${id}`,
        { headers: authHeader() }
      )

      await loadKB()
    }

    // =====================
    // 进入知识库管理
    // =====================
    const goManage = (id: number) => {
      router.push(`/kb/upload/${id}`)
    }

    onMounted(() => {
      loadKB()
    })

    return {
      kbList,
      showCreate,
      form,
      createKb,
      deleteKb,
      goManage
    }
  }
})
</script>

<style scoped>
.kb-page {
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-left h2 {
  margin: 0;
}

.back-link {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

.create-btn {
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  background: #667eea;
  color: white;
  cursor: pointer;
}

.kb-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 20px;
}

.kb-card {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: #fff;
}

.kb-title {
  font-size: 18px;
  font-weight: bold;
}

.kb-actions {
  margin-top: 12px;
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
  border-radius: 12px;
  width: 400px;
}
</style>