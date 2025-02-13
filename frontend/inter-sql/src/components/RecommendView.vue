<template>
  <div class="recommend-container">
    <h3>推荐问题</h3>
    <div class="recommend-list">
      <button 
        v-for="(item, index) in recommendations" 
        :key="index"
        class="recommend-item"
        @click="selectRecommendation(item)"
      >
        {{ item }}
      </button>
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendView',
  data() {
    return {
      recommendations: [
        '如何查询所有用户信息？',
        '如何添加新用户？',
        '如何删除指定记录？',
        '如何更新用户密码？'
      ],
      error: null,
      updateInterval: null
    }
  },
  methods: {
    selectRecommendation(text) {
      this.$emit('select-recommendation', text)
    },
    async fetchRecommendations() {
      try {
        const response = await fetch('http://localhost:8000/api/recommendations/')
        if (!response.ok) {
          throw new Error('获取推荐失败')
        }
        const data = await response.json()
        this.recommendations = data
        this.error = null
      } catch (err) {
        console.error('获取推荐失败:', err)
        this.error = '获取推荐失败，使用默认推荐'
      }
    },
    updateRecommendations(newRecommendations) {
      if (Array.isArray(newRecommendations)) {
        this.recommendations = newRecommendations
      }
    }
  },
  created() {
    this.fetchRecommendations()
    
    // 每30秒更新一次推荐
    this.updateInterval = setInterval(() => {
      this.fetchRecommendations()
    }, 30000)
  },
  beforeUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval)
    }
  }
}
</script>

<style scoped>
.recommend-container {
  width: 250px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #000;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recommend-item {
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
  transition: all 0.3s ease;
  backdrop-filter: blur(4px);
  color: #000;
}

.recommend-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.error-message {
  color: #ff4444;
  font-size: 12px;
  margin-top: 10px;
  text-align: center;
}
</style> 