module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  // 添加配置以支持 Vue 单文件组件
  plugins: [
    '@babel/plugin-transform-runtime',
    '@babel/plugin-proposal-class-properties'
  ]
}
