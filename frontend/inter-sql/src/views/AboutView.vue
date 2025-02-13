<template>
  <div class="about">
    <div class="background-container">
      <div class="gradient-overlay"></div>
    </div>
    <div class="snowflakes" aria-hidden="true">
      <div class="snowflake" v-for="n in 28" :key="n">❅</div>
    </div>
    
    <!-- 添加滑动按钮 -->
    <button class="slide-button" @click="toggleSlidePanel">
      <span class="button-icon">{{ isPanelOpen ? '›' : '‹' }}</span>
    </button>
    
    <!-- 添加滑动面板 -->
    <div class="slide-panel" :class="{ 'panel-open': isPanelOpen }">
      <div class="panel-content">
        <h2>数据库管理</h2>
        <ChatDB />
      </div>
    </div>

    <div class="content-container">
      <div class="header">
        <h1>SQL智能助手</h1>
        <p class="subtitle">让数据库操作更简单</p>
      </div>
      <div class="chat-container glass-effect">
        <ChatView />
      </div>
    </div>
  </div>
</template>

<script>
import ChatView from '@/components/ChatView.vue'
import ChatDB from '@/components/ChatDB.vue'

export default {
  name: 'AboutView',
  components: {
    ChatView,
    ChatDB
  },
  data() {
    return {
      isPanelOpen: false
    }
  },
  methods: {
    toggleSlidePanel() {
      this.isPanelOpen = !this.isPanelOpen
    }
  }
}
</script>

<style scoped>
.about {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/666.png');
  background-size: cover;  /* 改回 cover 以铺满视图 */
  background-repeat: no-repeat;
  background-position: center;
  background-color: #f5f5f5;
  z-index: -2;
  display: flex;  /* 添加 flex 布局 */
  justify-content: center;  /* 水平居中 */
  align-items: center;  /* 垂直居中 */
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(128, 128, 128, 0.5),
    rgba(169, 169, 169, 0.5)
  );
  z-index: -1;
}

.content-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  z-index: 2;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  color: white;
  animation: fadeInDown 0.8s ease-out;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

.chat-container {
  background: rgba(255, 255, 255, 0.05);  /* 更透明 */
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);  /* 边框也更透明 */
  animation: fadeInUp 0.8s ease-out;
}

.glass-effect {
  background: rgba(255, 255, 255, 0.05);  /* 更透明 */
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);  /* 边框也更透明 */
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 添加响应式设计 */
@media (max-width: 768px) {
  .content-container {
    padding: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .chat-container {
    padding: 1rem;
  }
}

/* 添加雪花样式 */
.snowflakes {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.snowflake {
  position: fixed;
  color: #fff;
  font-size: 1em;
  text-shadow: 0 0 5px rgba(255,255,255,0.8);
  animation: snowfall linear infinite;
}

/* 为每个雪花设置不同的动画时间和起始位置 */
.snowflake:nth-child(1) { left: 5%; animation-duration: 10s; animation-delay: -1s; }
.snowflake:nth-child(2) { left: 15%; animation-duration: 12s; animation-delay: -2s; }
.snowflake:nth-child(3) { left: 25%; animation-duration: 8s; animation-delay: -3s; }
.snowflake:nth-child(4) { left: 35%; animation-duration: 15s; animation-delay: -4s; }
.snowflake:nth-child(5) { left: 45%; animation-duration: 11s; animation-delay: -5s; }
.snowflake:nth-child(6) { left: 55%; animation-duration: 9s; animation-delay: -6s; }
.snowflake:nth-child(7) { left: 65%; animation-duration: 13s; animation-delay: -7s; }
.snowflake:nth-child(8) { left: 75%; animation-duration: 14s; animation-delay: -8s; }
.snowflake:nth-child(9) { left: 85%; animation-duration: 10s; animation-delay: -9s; }
.snowflake:nth-child(10) { left: 95%; animation-duration: 16s; animation-delay: -10s; }
.snowflake:nth-child(11) { left: 10%; animation-duration: 12s; animation-delay: -11s; }
.snowflake:nth-child(12) { left: 20%; animation-duration: 9s; animation-delay: -12s; }
.snowflake:nth-child(13) { left: 30%; animation-duration: 11s; animation-delay: -13s; }
.snowflake:nth-child(14) { left: 40%; animation-duration: 13s; animation-delay: -14s; }
.snowflake:nth-child(15) { left: 50%; animation-duration: 15s; animation-delay: -15s; }
.snowflake:nth-child(16) { left: 60%; animation-duration: 10s; animation-delay: -16s; }
.snowflake:nth-child(17) { left: 70%; animation-duration: 12s; animation-delay: -17s; }
.snowflake:nth-child(18) { left: 80%; animation-duration: 14s; animation-delay: -18s; }
.snowflake:nth-child(19) { left: 90%; animation-duration: 16s; animation-delay: -19s; }
.snowflake:nth-child(20) { left: 7%; animation-duration: 11s; animation-delay: -20s; }
.snowflake:nth-child(21) { left: 23%; animation-duration: 13s; animation-delay: -21s; }
.snowflake:nth-child(22) { left: 37%; animation-duration: 15s; animation-delay: -22s; }
.snowflake:nth-child(23) { left: 53%; animation-duration: 10s; animation-delay: -23s; }
.snowflake:nth-child(24) { left: 67%; animation-duration: 12s; animation-delay: -24s; }
.snowflake:nth-child(25) { left: 83%; animation-duration: 14s; animation-delay: -25s; }
.snowflake:nth-child(26) { left: 97%; animation-duration: 16s; animation-delay: -26s; }
.snowflake:nth-child(27) { left: 43%; animation-duration: 11s; animation-delay: -27s; }
.snowflake:nth-child(28) { left: 77%; animation-duration: 13s; animation-delay: -28s; }

@keyframes snowfall {
  0% {
    transform: translateY(-100vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0.3;
  }
}

/* 确保内容在雪花上层 */
.content-container {
  position: relative;
  z-index: 2;
}

/* 添加雪花悬停效果 */
.snowflake {
  transition: text-shadow 0.2s ease;
}

.snowflake:hover {
  text-shadow: 0 0 10px rgba(255,255,255,1);
}

/* 添加响应式调整 */
@media (max-width: 768px) {
  .snowflake {
    font-size: 0.8em;
  }
}

/* 修改滑动按钮位置到左边 */
.slide-button {
  position: fixed;
  left: 0;  /* 改为左侧 */
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-left: none;  /* 改为左边框消失 */
  padding: 20px 10px;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  border-radius: 0 8px 8px 0;  /* 改变圆角位置 */
}

.slide-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.button-icon {
  font-size: 24px;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  transform: rotate(180deg);  /* 旋转图标使其指向正确方向 */
}

/* 修改滑动面板位置到左边 */
.slide-panel {
  position: fixed;
  left: -800px;  /* 改为从左侧滑出 */
  top: 0;
  width: 800px;  /* 增加宽度以适应新内容 */
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);  /* 改为右边框 */
  transition: left 0.3s ease;  /* 改为控制 left 属性 */
  z-index: 999;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.panel-open {
  left: 0;  /* 改为左侧显示 */
}

.panel-content {
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.help-content {
  margin-top: 20px;
}

.help-content h3 {
  margin: 20px 0 10px;
  font-size: 1.2em;
}

.help-content ul {
  list-style: none;
  padding: 0;
}

.help-content li {
  margin: 10px 0;
  padding-left: 20px;
  position: relative;
}

.help-content li::before {
  content: '•';
  position: absolute;
  left: 0;
}

.help-content p {
  margin: 10px 0;
  line-height: 1.5;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .slide-panel {
    width: 100%;  /* 在移动端使用全宽 */
    left: -100%;
  }
}
</style>
