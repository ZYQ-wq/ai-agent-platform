```vue
<template>
  <div class="workspace">

    <!-- ===================== -->
    <!-- 左侧导航 -->
    <!-- ===================== -->
    <aside class="sidebar-card">

      <button
        class="back-btn"
        @click="goBack"
      >
        ← 返回知识库
      </button>

      <div class="menu">

      <button
        :class="[
          'menu-item',
          currentMenu==='learn'
          ? 'active'
          : ''
        ]"
        @click="currentMenu='learn'"
      >
        📚 数据学习
      </button>

      <button
        :class="[
          'menu-item',
          currentMenu==='search'
          ? 'active'
          : ''
        ]"
        @click="currentMenu='search'"
      >
        🔍 搜索测试
      </button>

      <button
        :class="[
          'menu-item',
          currentMenu==='setting'
          ? 'active'
          : ''
        ]"
        @click="currentMenu='setting'"
      >
        ⚙️ 知识库设置
      </button>

    </div>

    </aside>

    <!-- ===================== -->
    <!-- 右侧内容区 -->
    <!-- ===================== -->
    <main class="main-area">

    <!-- 数据学习 -->
    <template v-if="currentMenu==='learn'">

      <div class="toolbar-card">

        <div>

          <input
            ref="fileInput"
            type="file"
            style="display:none"
            @change="handleFile"
          />

          <button
            class="upload-btn"
            @click="triggerUpload"
          >
            📤 导入数据
          </button>

        </div>

        <input
          v-model="keyword"
          class="search-input"
          placeholder="搜索文件..."
        />

      </div>

      <div class="table-card">

        <table class="file-table">

          <thead>
            <tr>
              <th>名称</th>
              <th>待训练</th>
              <th>已训练</th>
              <th>数据总量</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="file in filteredFiles"
              :key="file.id"
            >

              <td>{{ file.file_name }}</td>

              <td>{{ file.pending || 0 }}</td>

              <td>
                {{ file.trained || 0 }}
              </td>

              <td>
                {{ file.total || 0 }}
              </td>

              <td>
                {{ formatTime(file.created_at) }}
              </td>

              <td>

                <button
                  class="action-btn"
                  @click="renameFile(file)"
                >
                  重命名
                </button>

                <button
                  class="danger-btn"
                  @click="deleteFile(file.id)"
                >
                  删除
                </button>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </template>

    <!-- 搜索测试 -->
    <template v-if="currentMenu==='search'">

      <div class="search-layout">

        <div class="search-left">

          <div class="search-card">

            <h3>测试文本</h3>

            <textarea
              v-model="testQuestion"
              class="question-input"
              placeholder="请输入测试问题..."
            />

          </div>

        </div>

        <div class="search-right">

          <div class="search-toolbar">

            <span>
              向量检索
            </span>

            <select
              v-model="topK"
              class="top-select"
            >
              <option :value="3">
                Top3
              </option>

              <option :value="5">
                Top5
              </option>

              <option :value="8">
                Top8
              </option>
            </select>

            <button
              class="action-btn"
              @click="testSearch"
            >
              测试
            </button>

            <button
              class="danger-btn"
              @click="resetSearch"
            >
              重置
            </button>

          </div>

          <div class="result-list">

            <div
              class="result-card"
              v-for="(
                item,
                index
              ) in searchResults"
              :key="index"
            >

              <div class="score">

                匹配率：

                {{
                  (
                    item.score * 100
                  ).toFixed(1)
                }}%

              </div>

              <div class="content">

                {{ item.content }}

              </div>

            </div>

          </div>

        </div>

      </div>

    </template>

    <!-- ===================== -->
    <!-- 知识库设置 -->
    <!-- ===================== -->
    <template
      v-if="currentMenu==='setting'"
    >

      <div class="setting-card">

        <h2>
          知识库设置
        </h2>

        <p class="setting-desc">
          修改名称、简介、向量模型与文本处理模型，
          保存后生效。
        </p>

        <div class="form-item">

          <label>
            知识库名称
          </label>

          <input
            v-model="kbName"
            class="setting-input"
          />

        </div>

        <div class="form-item">

          <label>
            简介
          </label>

          <textarea
            v-model="kbDescription"
            class="setting-textarea"
          />

        </div>

        <div class="form-item">

          <label>
            向量模型选择
          </label>

          <select
            v-model="embeddingModel"
            class="setting-select"
          >
            <option>
              BAAI/bge-small-zh-v1.5
            </option>
          </select>

        </div>

        <div class="form-item">

          <label>
            文本处理模型
          </label>

          <select
            v-model="llmModel"
            class="setting-select"
          >
            <option>
              qwen3-max
            </option>
          </select>

        </div>

        <button
          class="save-btn"
          @click="saveSetting"
        >
          保存设置
        </button>

      </div>

    </template>

    

  </main>


  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"

export default defineComponent({

  setup() {

    const route = useRoute()
    const router = useRouter()

    const kbId = route.params.id

    const files = ref<any[]>([])

    const keyword = ref("")

    const fileInput = ref()

    const currentMenu = ref("learn")

    const testQuestion = ref("")

    const topK = ref(3)

    const searchResults = ref<any[]>([])

    const kbName = ref("")
    const kbDescription = ref("")

    const embeddingModel = ref(
      "BAAI/bge-small-zh-v1.5"
    )

    const llmModel = ref(
      "qwen3-max"
    )

    const authHeader = () => ({
      Authorization: `Bearer ${localStorage.getItem("token")}`
    })

    const filteredFiles = computed(() => {

      if (!keyword.value)
        return files.value

      return files.value.filter((f) =>
        f.file_name
          ?.toLowerCase()
          .includes(keyword.value.toLowerCase())
      )
    })

    const loadKB = async () => {

      const res = await axios.get(
        `http://127.0.0.1:8000/kb/${kbId}`,
        {
          headers: authHeader()
        }
      )

      files.value =
        res.data.data.files || []

      kbName.value =res.data.data.kb.name

      kbDescription.value =res.data.data.kb.description
    }

    const triggerUpload = () => {
      fileInput.value.click()
    }

    const handleFile = async (e: any) => {

      const file = e.target.files[0]

      if (!file) return

      const formData = new FormData()

      formData.append(
        "file",
        file
      )

      await axios.post(
        `http://127.0.0.1:8000/kb/upload/${kbId}`,
        formData,
        {
          headers: {
            ...authHeader(),
            "Content-Type":
              "multipart/form-data"
          }
        }
      )

      await loadKB()
    }

    const renameFile = (file: any) => {

      const name = prompt(
        "请输入新名称",
        file.file_name
      )

      if (!name) return

      console.log(
        "待实现重命名",
        file.id,
        name
      )
    }

    const deleteFile = async (
      fileId: number
    ) => {

      if (
        !confirm("确定删除该文件？")
      ) {
        return
      }

      try {

        await axios.delete(
          `http://127.0.0.1:8000/kb/file/${fileId}`,
          {
            headers: authHeader()
          }
        )

        await loadKB()

      } catch (err) {

        console.error(err)

        alert("删除失败")
      }
    }

    const formatTime = (
      time: string
    ) => {

      if (!time) return ""

      return time.replace(
        "T",
        " "
      )
    }

    const goBack = () => {
      router.push("/kb")
    }

    const testSearch = async () => {

      if (!testQuestion.value.trim()) {
        alert("请输入测试问题")
        return
      }

      try {

        const res = await axios.post(
          `http://127.0.0.1:8000/kb/search/${kbId}`,
          {
            query: testQuestion.value,
            top_k: topK.value
          },
          {
            headers: authHeader()
          }
        )

        searchResults.value =
          res.data.data || []

      } catch (err) {

        console.error(err)

        alert("检索失败")
      }
    }

    const resetSearch = () => {

      testQuestion.value = ""

      searchResults.value = []
    }

    const saveSetting = async () => {

      try {

        await axios.put(
          `http://127.0.0.1:8000/kb/${kbId}`,
          {
            name: kbName.value,
            description:
              kbDescription.value
          },
          {
            headers: authHeader()
          }
        )

        alert("保存成功")

      } catch (err) {

        console.error(err)

        alert("保存失败")
      }
    }

    onMounted(() => {
      loadKB()
    })

    return {
      fileInput,
      files,
      keyword,
      filteredFiles,
      triggerUpload,
      handleFile,
      renameFile,
      deleteFile,
      formatTime,
      goBack,
      currentMenu,
      testQuestion,
      topK,
      searchResults,
      testSearch,
      resetSearch,
      kbName,
      kbDescription,
      embeddingModel,
      llmModel,
      saveSetting,
    }
  }
})
</script>

<style scoped>

.workspace {
  display: flex;
  height: 100vh;
  padding: 20px;
  gap: 20px;
  background: #f5f7fa;
}

.sidebar-card {

  width: 20%;

  background: white;

  border-radius: 20px;

  padding: 20px;

  box-shadow:
    0 2px 12px rgba(0,0,0,.05);
}

.back-btn {

  width: 100%;

  border: none;

  padding: 12px;

  border-radius: 12px;

  background: #f0f2f5;

  cursor: pointer;

  margin-bottom: 24px;
}

.menu {

  display: flex;

  flex-direction: column;

  gap: 12px;
}

.menu-item {

  border: none;

  background: #f7f8fa;

  padding: 14px;

  border-radius: 12px;

  cursor: pointer;

  text-align: left;

  font-size: 15px;
}

.menu-item.active {

  background: #1677ff;

  color: white;
}

.main-area {

  width: 80%;

  display: flex;

  flex-direction: column;

  gap: 20px;
}

.toolbar-card {

  height: 90px;

  background: white;

  border-radius: 20px;

  padding: 20px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  box-shadow:
    0 2px 12px rgba(0,0,0,.05);
}

.upload-btn {

  border: none;

  padding: 12px 20px;

  border-radius: 12px;

  background: #1677ff;

  color: white;

  cursor: pointer;
}

.search-input {

  width: 300px;

  padding: 10px 14px;

  border-radius: 12px;

  border: 1px solid #ddd;
}

.table-card {

  flex: 1;

  background: white;

  border-radius: 20px;

  padding: 20px;

  overflow-y: auto;

  box-shadow:
    0 2px 12px rgba(0,0,0,.05);
}

.file-table {

  width: 100%;

  border-collapse: collapse;
}

.file-table th {

  text-align: left;

  padding: 14px;

  border-bottom:
    1px solid #eee;

  color: #666;
}

.file-table td {

  padding: 16px;

  border-bottom:
    1px solid #f0f0f0;
}

.action-btn {

  border: none;

  background: #1677ff;

  color: white;

  padding: 8px 12px;

  border-radius: 8px;

  cursor: pointer;

  margin-right: 8px;
}

.danger-btn {

  border: none;

  background: #ff4d4f;

  color: white;

  padding: 8px 12px;

  border-radius: 8px;

  cursor: pointer;
}

.search-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

.search-left,
.search-right {
  width: 50%;
}

.search-card {
  height: 100%;
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow:
    0 2px 12px rgba(0,0,0,.05);
}

.question-input {
  width: 100%;
  height: 500px;
  resize: none;
  margin-top: 12px;
}

.search-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.top-select {
  padding: 8px 12px;
  border-radius: 8px;
}

.result-list {
  height: calc(100% - 60px);
  overflow-y: auto;
}

.result-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow:
    0 2px 12px rgba(0,0,0,.05);
}

.score {
  color: #1677ff;
  font-weight: 600;
  margin-bottom: 8px;
}

.setting-card {

  flex: 1;

  background: white;

  border-radius: 20px;

  padding: 30px;

  box-shadow:
    0 2px 12px rgba(0,0,0,.05);

  overflow-y: auto;
}

.setting-desc {

  color: #888;

  margin-bottom: 30px;
}

.form-item {

  display: flex;

  flex-direction: column;

  gap: 10px;

  margin-bottom: 24px;
}

.form-item label {

  font-size: 14px;

  color: #555;

  font-weight: 600;
}

.setting-input,
.setting-textarea,
.setting-select {

  width: 100%;

  padding: 12px;

  border-radius: 12px;

  border: 1px solid #ddd;
}

.setting-textarea {

  min-height: 120px;

  resize: vertical;
}

.save-btn {

  background: #1677ff;

  color: white;

  border: none;

  padding: 12px 24px;

  border-radius: 12px;

  cursor: pointer;
}

.content {
  line-height: 1.7;
}
</style>
```
