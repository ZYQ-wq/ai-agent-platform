---
name: front-end-dev-server-startup
description: 记录前端开发服务器的启动命令和端口信息
metadata:
  type: reference
---

**前端开发服务器启动命令**

```bash
cd "d:\公司学习\ai-agent-platform\web"
npm run dev
```

**运行信息**
- 默认端口：5173
- 如果端口被占用，会自动切换到5174或其他可用端口
- 访问地址：http://localhost:5173/

**注意事项**
- 如果需要停止服务器，可以运行 `taskkill /f /im node.exe`
- 每次修改路由配置后，重启服务器才能生效