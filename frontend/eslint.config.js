import pluginVue from 'eslint-plugin-vue'

export default [
  ...pluginVue.configs['flat/recommended'],
  {
    rules: {
      // 技术宪法：组件名 PascalCase、一文件一组件，由目录约定保证，此处不再强制多词名
      'vue/multi-word-component-names': 'off',
    },
  },
]
