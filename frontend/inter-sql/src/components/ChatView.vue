<template>
  <div class="chat-container">
    <div class="chat-main">
      <div class="chat-messages glass-effect">
        <!-- 聊天消息列表 -->
        <div class="messages-list">
          <div v-for="(msg, index) in messages" :key="index" 
               :class="['message', msg.type]">
            <div class="message-content">
              <div class="avatar">
                {{ msg.type === 'user' ? '👤' : '🤖' }}
              </div>
              <div class="text" v-html="formatMessage(msg.content)"></div>
            </div>
            <div class="time">{{ msg.time }}</div>
          </div>
        </div>
      </div>
      <div class="chat-input-wrapper glass-effect">
        <div class="input-container">
          <input 
            ref="inputEl"
            type="text" 
            v-model="message" 
            @input="handleInput"
            @keydown.enter.prevent="handleEnter"
            placeholder="请输入您的问题..."
            class="main-input"
          >
          <div class="suggestion-wrapper">
            <span class="typed-text">{{ message }}</span>
            <span v-if="suggestion" class="suggestion">{{ suggestion }}</span>
          </div>
        </div>
        <button class="send-button" @click="sendMessage">
          发送
        </button>
      </div>
    </div>
    <div class="recommend-section glass-effect">
      <RecommendView 
        ref="recommendView"
        @select-recommendation="onSelectRecommendation" 
      />
    </div>
  </div>
</template>

<script>
import RecommendView from './RecommendView.vue'

export default {
  name: 'ChatView',
  components: {
    RecommendView
  },
  data() {
    return {
      message: '',
      suggestion: '',
      inputTimer: null,
      messages: [],  // 聊天消息数组
      defaultReplies: ['小黄人', '哪吒', '熊出没']  // 默认回复
    }
  },
  methods: {
    async sendMessage() {
      if (this.message.trim()) {
        // 添加用户消息
        this.addMessage(this.message, 'user')
        
        try {
          // 发送消息到 Django 后端
          const response = await fetch('http://localhost:8000/api/chat/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              message: this.message
            })
          })

          if (!response.ok) {
            throw new Error('请求失败')
          }

          const data = await response.json()
          // 添加助手回复
          this.addMessage(data.response, 'assistant')
        } catch (error) {
          console.error('发送消息失败:', error)
          // 发生错误时显示错误消息
          this.addMessage('抱歉，发生了一些错误，请稍后重试。', 'assistant')
        }

        this.message = ''
        this.suggestion = ''
      }
    },
    addMessage(content, type) {
      const now = new Date()
      const time = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}`
      this.messages.push({
        content,
        type,
        time
      })
      // 滚动到底部
      this.$nextTick(() => {
        const messagesList = document.querySelector('.messages-list')
        messagesList.scrollTop = messagesList.scrollHeight
      })
    },
    onSelectRecommendation(text) {
      const currentInput = this.message.trim();
      this.message = currentInput 
        ? `${currentInput} ${text}`
        : text;
      this.suggestion = '';
      this.handleInput();
    },
    handleEnter() {
      if (this.suggestion) {
        this.message = this.message + this.suggestion;
        this.suggestion = '';
      } else {
        this.sendMessage();
      }
    },
    handleInput() {
      if (this.inputTimer) {
        clearTimeout(this.inputTimer);
      }
      
      this.inputTimer = setTimeout(async () => {
        try {
          // 获取实时补全建议
          const completionResponse = await fetch('http://localhost:8000/api/realtime-completion/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              input: this.message
            })
          });

          if (!completionResponse.ok) {
            throw new Error('获取补全建议失败');
          }

          const completionData = await completionResponse.json();
          this.suggestion = completionData.suggestion || '';

          // 获取推荐列表
          const response = await fetch('http://localhost:8000/api/process-input/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              input: this.message
            })
          });

          if (!response.ok) {
            throw new Error('请求失败');
          }

          const data = await response.json();
          console.log('后端响应:', data);
          
          // 更新推荐列表
          if (data.recommendations) {
            this.$refs.recommendView.updateRecommendations(data.recommendations);
          }
        } catch (error) {
          console.error('发送输入到后端失败:', error);
          this.suggestion = '';
        }
      }, 300);
    },
    formatMessage(message) {
      // 将换行符转换为 HTML 的 <br> 标签
      return message.replace(/\n/g, '<br>')
    }
  },
  beforeUnmount() {
    if (this.inputTimer) {
      clearTimeout(this.inputTimer)
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  gap: 20px;
  padding: 1rem;
  height: calc(100vh - 120px);  /* 减去导航栏和padding的高度 */
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 0;  /* 防止内容溢出 */
}

.glass-effect {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
}

.chat-messages {
  flex: 1;
  min-height: 0;  /* 允许内容收缩 */
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  overflow-y: auto;
}

.chat-messages:hover {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.chat-input-wrapper {
  display: flex;
  gap: 10px;
  padding: 1rem;
  border-radius: 12px;
  align-items: center;
}

.input-container {
  position: relative;
  flex: 1;
}

.main-input {
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  color: #000;
  font-size: 14px;
  transition: all 0.3s ease;
}

.main-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
}

.main-input::placeholder {
  color: rgba(0, 0, 0, 0.4);
}

.suggestion-wrapper {
  position: absolute;
  top: 0;
  left: 16px;
  right: 16px;
  bottom: 0;
  pointer-events: none;
  display: flex;
  align-items: center;
  font-size: 14px;
  white-space: pre;
  overflow: hidden;
}

.typed-text {
  color: transparent;
  user-select: none;
}

.suggestion {
  color: rgba(0, 0, 0, 0.4);
  font-size: 14px;
  user-select: none;
}

.send-button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.send-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
  background: linear-gradient(135deg, #45a049, #4CAF50);
}

.send-button:active {
  transform: translateY(1px);
}

.recommend-section {
  width: 300px;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;  /* 使用全部可用高度 */
  overflow-y: auto;  /* 内容过多时可滚动 */
}

@media (max-width: 768px) {
  .chat-container {
    flex-direction: column;
    height: auto;
  }
  
  .recommend-section {
    width: 100%;
    height: 300px;  /* 在移动设备上固定高度 */
  }
  
  .chat-messages {
    min-height: 300px;
  }
}

.messages-list {
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-right: 10px;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.avatar {
  font-size: 1.5rem;
  min-width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text {
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  white-space: pre-line;  /* 保留换行符 */
  color: #000;
}

.user .text {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.2);
}

.time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.4);
  margin: 0 40px;
}

/* 滚动条样式 */
.messages-list::-webkit-scrollbar {
  width: 6px;
}

.messages-list::-webkit-scrollbar-track {
  background: transparent;
}

.messages-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.messages-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.2);
}
</style> 