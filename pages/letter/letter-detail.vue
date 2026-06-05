<template>
  <view class="container">
    <view class="letter-container" v-if="letter">
      <!-- 未开启状态 -->
      <view class="locked-section" v-if="!canOpen">
        <view class="lock-icon">🔒</view>
        <text class="lock-title">信件尚未开启</text>
        <text class="lock-desc">这封信将在以下时间自动解锁</text>
        <view class="countdown-box">
          <text class="countdown-time">{{countdownText}}</text>
        </view>
        <view class="letter-preview">
          <text class="preview-label">创建时间</text>
          <text class="preview-value">{{formatDate(letter.createDate)}}</text>
          <text class="preview-label">标签</text>
          <view class="preview-tags">
            <text class="tag tag-primary" v-for="(tag, index) in letter.tags" :key="index">{{tag}}</text>
          </view>
        </view>
      </view>
      
      <!-- 已开启状态 -->
      <view class="opened-section" v-else>
        <view class="open-header">
          <text class="open-icon">✉️</text>
          <text class="open-title">来自过去的信</text>
          <text class="open-date">写于 {{formatDate(letter.createDate)}}</text>
        </view>
        
        <view class="letter-content">
          <text class="content-text">{{letter.content}}</text>
        </view>
        
        <view class="letter-tags" v-if="letter.tags.length > 0">
          <text class="tag tag-primary" v-for="(tag, index) in letter.tags" :key="index">{{tag}}</text>
        </view>
        
        <!-- 心情记录 -->
        <view class="mood-section" v-if="!letter.mood">
          <text class="mood-title">读完这封信，你现在的心情是？</text>
          <view class="mood-options">
            <view class="mood-item" v-for="(mood, index) in moods" :key="index" @click="selectMood(mood)">
              <text class="mood-emoji">{{mood.emoji}}</text>
              <text class="mood-label">{{mood.label}}</text>
            </view>
          </view>
        </view>
        
        <view class="mood-display" v-else>
          <text class="mood-result">你当时的心情：{{letter.mood.emoji}} {{letter.mood.label}}</text>
        </view>
      </view>
      
      <!-- 删除按钮 -->
      <button class="btn-secondary delete-btn" @click="deleteLetter">删除信件</button>
    </view>
    
    <view class="empty-state" v-else>
      <text class="empty-icon">📭</text>
      <text class="empty-text">信件不存在</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      letter: null,
      letterId: '',
      countdownText: '',
      countdownTimer: null,
      moods: [
        { emoji: '😊', label: '开心' },
        { emoji: '😢', label: '感动' },
        { emoji: '💪', label: '振奋' },
        { emoji: '🤔', label: '思考' },
        { emoji: '😌', label: '平静' },
        { emoji: '😔', label: '遗憾' }
      ]
    }
  },
  computed: {
    canOpen() {
      if (!this.letter) return false
      return new Date(this.letter.openDate).getTime() <= new Date().getTime()
    }
  },
  onLoad(options) {
    this.letterId = options.id
    this.loadLetter()
  },
  onShow() {
    if (!this.canOpen) {
      this.startCountdown()
    }
  },
  onHide() {
    this.stopCountdown()
  },
  methods: {
    loadLetter() {
      const letters = uni.getStorageSync('letters') || []
      this.letter = letters.find(l => l.id === this.letterId)
      if (this.letter && this.canOpen && !this.letter.isOpened) {
        this.letter.isOpened = true
        this.saveLetters(letters)
      }
    },
    startCountdown() {
      this.updateCountdown()
      this.countdownTimer = setInterval(() => {
        this.updateCountdown()
      }, 1000)
    },
    stopCountdown() {
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer)
        this.countdownTimer = null
      }
    },
    updateCountdown() {
      if (!this.letter) return
      const now = new Date().getTime()
      const target = new Date(this.letter.openDate).getTime()
      const diff = target - now
      
      if (diff <= 0) {
        this.countdownText = '已经可以开启'
        this.loadLetter()
        return
      }
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((diff % (1000 * 60)) / 1000)
      
      this.countdownText = `${days}天${hours}时${minutes}分${seconds}秒`
    },
    selectMood(mood) {
      this.letter.mood = mood
      const letters = uni.getStorageSync('letters') || []
      const index = letters.findIndex(l => l.id === this.letterId)
      if (index > -1) {
        letters[index] = this.letter
        this.saveLetters(letters)
      }
      uni.showToast({ title: '已记录心情', icon: 'success' })
    },
    deleteLetter() {
      uni.showModal({
        title: '确认删除',
        content: '删除后无法恢复，是否继续？',
        confirmColor: '#e94560',
        success: (res) => {
          if (res.confirm) {
            const letters = uni.getStorageSync('letters') || []
            const filtered = letters.filter(l => l.id !== this.letterId)
            this.saveLetters(filtered)
            uni.showToast({ title: '已删除', icon: 'success' })
            setTimeout(() => {
              uni.navigateBack()
            }, 1500)
          }
        }
      })
    },
    saveLetters(letters) {
      uni.setStorageSync('letters', letters)
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
    }
  }
}
</script>

<style scoped>
.letter-container {
  padding: 20rpx;
}

.locked-section {
  text-align: center;
  padding: 60rpx 40rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.lock-icon {
  font-size: 100rpx;
  margin-bottom: 30rpx;
}

.lock-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 16rpx;
}

.lock-desc {
  font-size: 26rpx;
  color: #8b8b9a;
  display: block;
  margin-bottom: 30rpx;
}

.countdown-box {
  background: rgba(233, 69, 96, 0.1);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.countdown-time {
  font-size: 40rpx;
  font-weight: bold;
  color: #e94560;
}

.letter-preview {
  text-align: left;
}

.preview-label {
  font-size: 24rpx;
  color: #6b6b7b;
  display: block;
  margin-bottom: 10rpx;
}

.preview-value {
  font-size: 28rpx;
  color: #eaeaea;
  display: block;
  margin-bottom: 20rpx;
}

.preview-tags {
  display: flex;
  flex-wrap: wrap;
}

.opened-section {
  padding: 40rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.open-header {
  text-align: center;
  margin-bottom: 40rpx;
  padding-bottom: 30rpx;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.open-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 16rpx;
}

.open-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 10rpx;
}

.open-date {
  font-size: 24rpx;
  color: #8b8b9a;
}

.letter-content {
  margin-bottom: 30rpx;
}

.content-text {
  font-size: 32rpx;
  color: #eaeaea;
  line-height: 1.8;
  display: block;
}

.letter-tags {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 30rpx;
}

.mood-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 30rpx;
}

.mood-title {
  font-size: 28rpx;
  color: #a0a0b0;
  display: block;
  margin-bottom: 20rpx;
  text-align: center;
}

.mood-options {
  display: flex;
  justify-content: space-around;
}

.mood-item {
  text-align: center;
  padding: 20rpx;
  transition: all 0.3s;
}

.mood-item:active {
  transform: scale(1.1);
}

.mood-emoji {
  font-size: 60rpx;
  display: block;
  margin-bottom: 10rpx;
}

.mood-label {
  font-size: 24rpx;
  color: #a0a0b0;
}

.mood-display {
  text-align: center;
  padding: 30rpx;
  background: rgba(46, 213, 115, 0.1);
  border-radius: 20rpx;
}

.mood-result {
  font-size: 28rpx;
  color: #2ed573;
}

.delete-btn {
  width: 100%;
}
</style>
