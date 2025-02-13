<template>
  <div class="entity-node">
    <div class="entity-header">
      <input 
        v-model="label" 
        class="entity-name"
        @change="updateNodeLabel"
      >
    </div>
    <div class="entity-attributes">
      <div 
        v-for="(attr, index) in attributes" 
        :key="index"
        class="attribute-item"
      >
        <input 
          v-model="attr.name"
          class="attribute-input"
          placeholder="属性名"
        >
        <select v-model="attr.type" class="attribute-type">
          <option value="string">String</option>
          <option value="number">Number</option>
          <option value="date">Date</option>
          <option value="boolean">Boolean</option>
        </select>
        <button 
          @click="removeAttribute(index)"
          class="remove-btn"
        >
          ×
        </button>
      </div>
      <button 
        @click="addAttribute"
        class="add-attribute-btn"
      >
        + 添加属性
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EntityNode',
  props: {
    id: {
      type: String,
      required: true
    },
    data: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      label: this.data.label || '新实体',
      attributes: this.data.attributes || []
    }
  },
  methods: {
    updateNodeLabel() {
      this.$emit('update:data', { ...this.data, label: this.label })
    },
    addAttribute() {
      this.attributes.push({
        name: '',
        type: 'string'
      })
    },
    removeAttribute(index) {
      this.attributes.splice(index, 1)
    }
  }
}
</script>

<style scoped>
.entity-node {
  min-width: 200px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.entity-header {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.entity-name {
  width: 100%;
  border: none;
  font-size: 14px;
  font-weight: bold;
  padding: 4px;
}

.entity-attributes {
  padding: 8px;
}

.attribute-item {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
}

.attribute-input {
  flex: 1;
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 2px;
  font-size: 12px;
}

.attribute-type {
  width: 80px;
  padding: 4px;
  border: 1px solid #ddd;
  border-radius: 2px;
  font-size: 12px;
}

.remove-btn {
  padding: 0 6px;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 2px;
  cursor: pointer;
}

.add-attribute-btn {
  width: 100%;
  padding: 4px;
  margin-top: 8px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 2px;
  cursor: pointer;
}
</style> 