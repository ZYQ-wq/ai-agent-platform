import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 这里引用刚刚创建的 router/index.js
import "./style.css";

createApp(App)
  .use(router)  // 使用 Vue Router
  .mount("#app");