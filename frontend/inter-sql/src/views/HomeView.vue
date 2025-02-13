<template>
  <div class="home">
    <div class="background-container">
      <div class="gradient-overlay"></div>
    </div>
    <!-- 添加雪花容器 -->
    <div class="snowflakes" aria-hidden="true">
      <div class="snowflake" v-for="n in 28" :key="n">❅</div>
    </div>
    <!-- 添加左侧导航容器到这里 -->
    <div class="side-nav glass-effect">
      <button 
        @click="navigateTo('http://localhost:5173/')" 
        class="nav-btn" 
        title="ChartDB"
      >
        📊
      </button>
      <button 
        @click="navigateTo('http://localhost:3000/')" 
        class="nav-btn" 
        title="SQLens"
      >
        🔍
      </button>
      <button 
        @click="navigateTo('http://localhost:8888/')" 
        class="nav-btn" 
        title="DBDesign"
      >
        📐
      </button>
    </div>
    <div class="content-container">
      <div class="header">
        <h1>SQL智能助手</h1>
        <p class="subtitle">数据库可视化与智能问答系统</p>
      </div>
      <div class="main-content glass-effect">
        <div class="iframe-container">
          <iframe 
            ref="frame"
            :src="currentUrl"
            frameborder="0"
            class="embedded-frame"
            title="Embedded Content"
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
            @load="handleIframeLoad"
          ></iframe>
          <!-- 添加主页按钮 -->
          <button @click="goHome" class="home-btn" title="返回主页">
            <span>🏠</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      currentUrl: 'http://localhost:5173/',
      history: ['http://localhost:5173/'],
      currentIndex: 0,
      canGoBack: false,
      canGoForward: false,
      iframeWindow: null,
      // 添加主页映射
      homeUrls: {
        'localhost:5173': 'http://localhost:5173/',
        'localhost:3000': 'http://localhost:3000/',
        'localhost:8888': 'http://localhost:8888/'  // 添加 dbdesign 的主页地址
      }
    }
  },
  methods: {
    handleIframeLoad() {
      const frame = this.$refs.frame;
      if (frame) {
        try {
          this.iframeWindow = frame.contentWindow;
          // 获取当前 URL
          const newUrl = frame.contentWindow.location.href;
          if (newUrl !== this.currentUrl) {
            this.currentUrl = newUrl;
            if (!this.history.includes(newUrl)) {
              if (this.currentIndex < this.history.length - 1) {
                this.history = this.history.slice(0, this.currentIndex + 1);
              }
              this.history.push(newUrl);
              this.currentIndex = this.history.length - 1;
            }
            this.updateNavState();
          }
        } catch (e) {
          console.warn('无法访问 iframe URL:', e);
        }
      }
    },
    goBack() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
        this.currentUrl = this.history[this.currentIndex];
        const frame = this.$refs.frame;
        if (frame) {
          frame.src = this.currentUrl;
        }
        this.updateNavState();
      }
    },
    goForward() {
      if (this.currentIndex < this.history.length - 1) {
        this.currentIndex++;
        this.currentUrl = this.history[this.currentIndex];
        const frame = this.$refs.frame;
        if (frame) {
          frame.src = this.currentUrl;
        }
        this.updateNavState();
      }
    },
    updateNavState() {
      this.canGoBack = this.currentIndex > 0;
      this.canGoForward = this.currentIndex < this.history.length - 1;
    },
    checkIframeUrl() {
      if (this.iframeWindow) {
        try {
          const newUrl = this.iframeWindow.location.href;
          if (newUrl !== this.currentUrl) {
            this.currentUrl = newUrl;
            if (!this.history.includes(newUrl)) {
              if (this.currentIndex < this.history.length - 1) {
                this.history = this.history.slice(0, this.currentIndex + 1);
              }
              this.history.push(newUrl);
              this.currentIndex = this.history.length - 1;
            }
            this.updateNavState();
          }
        } catch (e) {
          console.warn('无法访问 iframe URL:', e);
        }
      }
    },
    goHome() {
      const frame = this.$refs.frame;
      if (frame) {
        // 获取当前 URL 的主机名
        const currentHost = new URL(this.currentUrl).host;
        // 根据当前主机名选择对应的主页
        const homeUrl = this.homeUrls[currentHost] || 'http://localhost:5173/';
        frame.src = homeUrl;
        // 更新当前 URL
        this.currentUrl = homeUrl;
      }
    },
    navigateTo(url) {
      const frame = this.$refs.frame;
      if (frame) {
        frame.src = url;
        // 更新当前 URL
        this.currentUrl = url;
      }
    }
  },
  mounted() {
    const frame = this.$refs.frame;
    if (frame) {
      frame.addEventListener('load', this.handleIframeLoad);
      // 定期检查 URL 变化
      setInterval(this.checkIframeUrl, 100);
    }
    this.updateNavState();
  },
  beforeUnmount() {
    const frame = this.$refs.frame;
    if (frame) {
      frame.removeEventListener('load', this.handleIframeLoad);
    }
  }
}
</script>

<style scoped>
.home {
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
  background-image: url('@/assets/123.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  background-color: #f5f5f5;
  z-index: -2;
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

/* 雪花容器样式 */
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

.content-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
  color: white;  /* 改为白色以适应背景 */
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

.main-content {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  padding: 1rem;
  min-height: 85vh;
  height: 85vh;
  animation: fadeInUp 0.8s ease-out;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;  /* 防止内容溢出 */
}

.glass-effect {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.placeholder {
  text-align: center;
  color: white;  /* 改为白色以适应背景 */
}

.logo {
  width: 120px;
  height: 120px;
  margin-bottom: 2rem;
  opacity: 0.8;
}

.welcome-text {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: white;  /* 改为白色以适应背景 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.hint-text {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);  /* 改为半透明白色 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .content-container {
    padding: 0.5rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .main-content {
    padding: 0.5rem;
    min-height: 80vh;
    height: 80vh;
  }
  
  .logo {
    width: 80px;
    height: 80px;
  }
  
  .welcome-text {
    font-size: 1.2rem;
  }
  
  .iframe-container {
    height: 100%;
  }
  
  .embedded-frame {
    height: 100%;
  }
}

/* 修改侧边导航样式 */
.side-nav {
  position: fixed;  /* 改为固定定位 */
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;  /* 提高层级 */
}

.nav-btn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  color: #333;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  text-decoration: none;  /* 移除链接下划线 */
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-btn:active {
  transform: translateX(0);
}

/* 移除 iframe-container 的左边距 */
.iframe-container {
  flex: 1;
  min-height: 0;
  height: 100%;
  position: relative;
  overflow: hidden;
  margin-left: 0;  /* 移除左边距 */
}

.embedded-frame {
  width: 100%;
  height: 100%;  /* 设置高度为100% */
  border: none;
  background: transparent;
  position: absolute;  /* 绝对定位 */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 添加主页按钮样式 */
.home-btn {
  position: absolute;
  left: 20px;
  bottom: 20px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  color: #333;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.home-btn:active {
  transform: translateY(0);
}

/* 移除旧的导航相关样式 */
.address-bar,
.url-display,
.iframe-nav {
  display: none;
}
</style>
