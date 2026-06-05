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
      const letters = uni.getStorageSync('letters') || []
      const challenges = uni.getStorageSync('challenges') || []
      const snapshots = uni.getStorageSync('snapshots') || []
      const friendLetters = uni.getStorageSync('friendLetters') || []
      
      uni.setStorageSync('letters', letters)
      uni.setStorageSync('challenges', challenges)
      uni.setStorageSync('snapshots', snapshots)
      uni.setStorageSync('friendLetters', friendLetters)
    }
  }
}
</script>

<style>
/* 全局样式 */
page {
  background-color: #16213e;
  color: #eaeaea;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.container {
  padding: 20rpx;
  min-height: 100vh;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}

/* 卡片样式 */
.card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
  margin-bottom: 16rpx;
}

.card-desc {
  font-size: 26rpx;
  color: #a0a0b0;
  line-height: 1.6;
}

/* 按钮样式 */
.btn-primary {
  background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx 60rpx;
  font-size: 30rpx;
  border: none;
  text-align: center;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: #eaeaea;
  border-radius: 40rpx;
  padding: 20rpx 50rpx;
  font-size: 28rpx;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
}

/* 输入框样式 */
.input-field {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16rpx;
  padding: 24rpx;
  color: #eaeaea;
  font-size: 28rpx;
  width: 100%;
  box-sizing: border-box;
}

.input-field::placeholder {
  color: #6b6b7b;
}

/* 标签样式 */
.tag {
  display: inline-block;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  margin-right: 12rpx;
  margin-bottom: 12rpx;
}

.tag-primary {
  background: rgba(233, 69, 96, 0.2);
  color: #e94560;
}

.tag-success {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
}

.tag-warning {
  background: rgba(255, 165, 2, 0.2);
  color: #ffa502;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 100rpx 40rpx;
  color: #6b6b7b;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 30rpx;
  opacity: 0.5;
}

.empty-text {
  font-size: 28rpx;
  margin-bottom: 40rpx;
}

/* 动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease forwards;
}

/* 渐变文字 */
.gradient-text {
  background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>