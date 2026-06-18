// import { defineStore } from 'pinia'
// import { ref } from 'vue'

// import type {
//   CodingProject,
//   ProjectFile,
//   ChatMessage
// } from '@/types/coding'

// export const useCodingStore = defineStore('coding', () => {

//   const project = ref<CodingProject>({
//     id: 'demo-project',
//     name: '天气插件',
//     files: [
//       {
//         path: 'plugin.yaml',
//         language: 'yaml',
//         content: ''
//       },
//       {
//         path: 'main.py',
//         language: 'python',
//         content: '# hello'
//       }
//     ]
//   })

//   const currentFile = ref<ProjectFile | null>(
//     project.value.files[0]
//   )

//   const messages = ref<ChatMessage[]>([])

//   const consoleLogs = ref<string[]>([])

//   return {
//     project,
//     currentFile,
//     messages,
//     consoleLogs
//   }
// })

import { defineStore } from "pinia";
import { ref } from "vue";

export const useCodingStore = defineStore("coding", () => {

  // 🚨 必须初始化（关键）
  const project = ref({
    id: "demo",
    name: "Demo Project",
    files: [
      {
        path: "main.py",
        language: "python",
        content: "print('hello world')"
      },
      {
        path: "utils.js",
        language: "javascript",
        content: "console.log('hello')"
      }
    ]
  });

  const currentFile = ref<any>(project.value.files[0]);

  return {
    project,
    currentFile
  };
});
