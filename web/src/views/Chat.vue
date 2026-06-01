<template>
  <div class="chat-container">

```
<h2>Agent聊天</h2>

<div class="chat-box">

  <div
    v-for="(msg,index) in messages"
    :key="index"
  >

    <strong>
      {{ msg.role }}
    </strong>

    ：{{ msg.content }}

  </div>

</div>

<input
  v-model="inputMessage"
  @keyup.enter="sendMessage"
  placeholder="输入消息"
/>

<button
  @click="sendMessage"
>
  发送
</button>
```

  </div>
</template>

<script>
import axios from "axios";

export default {

  data() {

    return {

      messages: [],

      inputMessage: ""

    };

  },

  methods: {

    async sendMessage() {

      if (!this.inputMessage.trim()) {
        return;
      }

      const token =
        localStorage.getItem("token");

      const agentId =
        this.$route.params.agentId;

      this.messages.push({

        role: "你",

        content:
          this.inputMessage

      });

      try {

        const res =
          await axios.post(

            `http://127.0.0.1:8000/chat/${agentId}`,

            {
              message:
                this.inputMessage
            },

            {
              headers: {

                Authorization:
                  `Bearer ${token}`

              }
            }

          );

        this.messages.push({

          role: "AI",

          content:
            res.data.response

        });

      } catch {

        this.messages.push({

          role: "AI",

          content:
            "请求失败"

        });

      }

      this.inputMessage = "";

    }

  }

};
</script>
