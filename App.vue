<script>
export default {
  onLaunch() {
    console.log('App Launch')
    this.initStorage()
  },
  onShow() {
    console.log('App Show')
  },
  onHide() {
    console.log('App Hide')
  },
  methods: {
    initStorage() {
      const keys = ['letters', 'capsules', 'challenges', 'snapshots', 'friendLetters', 'wheelHistory', 'weatherRecords', 'userPoints', 'wishes']
      keys.forEach(key => {
        const value = uni.getStorageSync(key)
        if (value === undefined || value === null || value === '') {
          uni.setStorageSync(key, key === 'userPoints' ? 100 : [])
        }
      })
    }
  }
}
</script>

<style>
/* 全局样式 */
page {
  background-color: #f8f9fc;
  color: #2d3748;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* 按钮基础样式 */
button {
  margin: 0;
  padding: 0;
  background: none;
  border: none;
  line-height: inherit;
}

button::after {
  border: none;
}

/* 输入框基础样式 */
input, textarea {
  outline: none;
  border: none;
  box-sizing: border-box;
}

/* 滚动条隐藏 */
::-webkit-scrollbar {
  display: none;
}
</style>