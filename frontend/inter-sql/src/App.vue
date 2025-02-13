<template>
  <nav class="nav-container">
    <div class="nav-content">
      <router-link to="/" class="logo">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img">
      </router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link" exact>首页</router-link>
        <router-link to="/about" class="nav-link">智能问答</router-link>
      </div>
    </div>
  </nav>
  <router-view/>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: #f5f5f5;
}

.nav-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: opacity 0.3s ease;
}

.logo:hover {
  opacity: 0.8;
}

.logo-img {
  height: 40px;
  width: 40px;
  object-fit: contain;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-size: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: #4CAF50;
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: #4CAF50;
}

.nav-link:hover::after {
  width: 80%;
}

.router-link-exact-active,
.router-link-active {
  color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
}

.router-link-exact-active::after,
.router-link-active::after {
  width: 80%;
}

/* 为了适应固定导航栏，给主内容添加上边距 */
#app {
  padding-top: 80px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-content {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    gap: 1rem;
  }

  #app {
    padding-top: 120px;
  }
}
</style>
