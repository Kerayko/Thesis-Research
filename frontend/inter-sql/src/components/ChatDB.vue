<template>
  <div class="chatdb-container">
    <!-- 左侧数据库图标 -->
    <div class="db-icon-section">
      <div class="image-container">
        <img :src="currentDbImage" :alt="selectedDB || 'Database ER Diagram'" class="db-icon">
        <!-- 添加点击放大功能 -->
        <div class="image-overlay" @click="showFullImage = true">
          <span>点击查看大图</span>
        </div>
      </div>
      <p class="db-name">{{ selectedDB || '请选择数据库' }}</p>
    </div>

    <!-- 图片全屏显示弹窗 -->
    <div v-if="showFullImage" class="fullscreen-image" @click="showFullImage = false">
      <div class="image-wrapper">
        <img :src="currentDbImage" :alt="selectedDB || 'Database ER Diagram'">
        <span class="close-button">&times;</span>
      </div>
    </div>

    <!-- 中间操作区域 -->
    <div class="db-control-section">
      <div class="select-group">
        <label>选择数据库：</label>
        <select v-model="selectedDB" @change="loadTables">
          <option value="">请选择</option>
          <option v-for="db in databases" :key="db" :value="db">{{ db }}</option>
        </select>
      </div>
      
      <div class="select-group" v-if="selectedDB">
        <label>选择数据表：</label>
        <select v-model="selectedTable" @change="loadTableData">
          <option value="">请选择</option>
          <option v-for="table in tables" :key="table" :value="table">{{ table }}</option>
        </select>
      </div>
    </div>

    <!-- 右侧数据预览 -->
    <div class="table-preview-section">
      <h3 v-if="selectedTable">{{ selectedTable }} 预览数据</h3>
      <div class="table-container" v-if="tableData.length">
        <table>
          <thead>
            <tr>
              <th v-for="column in tableColumns" :key="column">{{ column }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in tableData" :key="index">
              <td v-for="column in tableColumns" :key="column">{{ row[column] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="selectedTable" class="loading">
        加载数据中...
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatDB',
  data() {
    return {
      showFullImage: false,  // 添加控制图片全屏显示的状态
      databases: ['MySQL_Demo', 'PostgreSQL_Test', 'SQLite_Sample'],
      dbData: null,
      loading: true,
      error: null,
      selectedDB: '',
      // 添加数据库图片映射
      dbImages: {
        'MySQL_Demo': require('@/assets/xixi.png'),
        'PostgreSQL_Test': require('@/assets/xixi.png'),
        'SQLite_Sample': require('@/assets/xixi.png'),
        'default': require('@/assets/123.png')
      },
      tables: {},
      relationships: [],
      selectedTable: '',
      tableData: [],
      tableColumns: []
    }
  },
  computed: {
    // 计算当前应该显示的图片
    currentDbImage() {
      return this.selectedDB ? this.dbImages[this.selectedDB] : this.dbImages.default
    }
  },
  async created() {
    try {
      const response = await fetch('http://localhost:8000/api/db-structure/')
      if (!response.ok) {
        throw new Error('获取数据库结构失败')
      }
      const result = await response.json()
      if (result.status === 'success') {
        this.dbData = result.data
      } else {
        throw new Error(result.message || '获取数据失败')
      }
    } catch (error) {
      console.error('获取数据库结构错误:', error)
      this.error = error.message
    } finally {
      this.loading = false
    }
  },
  methods: {
    loadTables() {
      if (!this.selectedDB || !this.dbData) {
        this.tables = []
        this.selectedTable = ''
        return
      }
      
      const dbTables = this.dbData[this.selectedDB]?.tables || {}
      this.tables = Object.keys(dbTables)
      this.selectedTable = ''
      this.tableData = []
      this.tableColumns = []
    },
    
    loadTableData() {
      if (!this.selectedDB || !this.selectedTable || !this.dbData) {
        this.tableData = []
        this.tableColumns = []
        return
      }
      
      const tableInfo = this.dbData[this.selectedDB]?.tables[this.selectedTable]
      if (tableInfo) {
        this.tableColumns = tableInfo.columns
        this.tableData = tableInfo.rows
      } else {
        this.tableColumns = []
        this.tableData = []
      }
    }
  }
}
</script>

<style scoped>
.chatdb-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
  padding: 15px;
  color: #000;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

/* 上部分 - 数据库图标 */
.db-icon-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 10px;
}

.image-container {
  position: relative;
  width: 220px;
  height: 220px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.1);
}

.db-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.image-container:hover .db-icon {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-container:hover .image-overlay {
  opacity: 1;
}

.image-overlay span {
  color: white;
  font-size: 14px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 4px;
}

/* 全屏图片显示样式 */
.fullscreen-image {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  cursor: pointer;
  padding: 20px;
}

.image-wrapper {
  position: relative;
  max-width: 95%;
  max-height: 95%;
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 12px;
}

.fullscreen-image img {
  max-width: 100%;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

.close-button {
  position: absolute;
  top: -40px;
  right: 0;
  color: white;
  font-size: 30px;
  cursor: pointer;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.8);
}

.db-name {
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
  color: #000;
  font-weight: 500;
}

/* 中间部分 - 控制区域 */
.db-control-section {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 40px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.select-group {
  min-width: 200px;
}

.select-group label {
  color: #000;
  font-weight: 500;
  margin-bottom: 5px;
  display: block;
}

select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.9);
  color: #000;
  backdrop-filter: blur(4px);
  width: 100%;
}

select option {
  background: #fff;
  color: #000;
}

/* 下部分 - 数据预览 */
.table-preview-section {
  flex: 1;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.table-preview-section h3 {
  color: #000;
  font-weight: 500;
  margin: 0;
}

.table-container {
  flex: 1;
  min-height: 250px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px;
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  font-size: 12px;
  color: #000;
}

th {
  background: rgba(0, 0, 0, 0.05);
  font-weight: bold;
  color: #000;
}

.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
  opacity: 0.8;
  color: #000;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .db-control-section {
    flex-direction: column;
    gap: 20px;
  }
  
  .select-group {
    width: 100%;
  }
  
  .image-container {
    width: 180px;
    height: 180px;
  }
}
</style> 