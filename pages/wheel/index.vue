<template>
  <view class="container">
    <custom-tabbar :current="2"></custom-tabbar>
    <view class="wheel-header">
      <text class="wheel-title">🎰 命运转盘</text>
      <text class="wheel-desc">让命运决定今天的小挑战</text>
    </view>

    <!-- 转盘区域 -->
    <view class="wheel-container">
      <view class="wheel-outer">
        <view class="wheel-inner" :style="{transform: 'rotate(' + rotation + 'deg)'}">
          <view 
            class="wheel-segment" 
            v-for="(item, index) in wheelItems" 
            :key="index"
            :style="{transform: 'rotate(' + (index * 45) + 'deg)'}">
            <text class="segment-text">{{item.emoji}}</text>
          </view>
        </view>
        <view class="wheel-pointer">▼</view>
        <view class="wheel-center" @click="spinWheel">
          <text class="center-text">{{isSpinning ? '...' : '开始'}}</text>
        </view>
      </view>
    </view>

    <!-- 结果展示 -->
    <view class="result-card" v-if="showResult">
      <view class="result-header">
        <text class="result-emoji">{{result.emoji}}</text>
        <text class="result-title">{{result.title}}</text>
      </view>
      <text class="result-desc">{{result.desc}}</text>
      <view class="result-tags">
        <text class="result-tag" v-for="(tag, index) in result.tags" :key="index">{{tag}}</text>
      </view>
      <button class="accept-btn" @click="acceptChallenge" v-if="!accepted">
        接受挑战
      </button>
      <text class="accepted-text" v-else>✓ 已接受挑战</text>
    </view>

    <!-- 历史记录 -->
    <view class="history-section" v-if="history.length > 0">
      <text class="section-title">挑战历史</text>
      <view class="history-list">
        <view class="history-item" v-for="(item, index) in history" :key="index">
          <text class="history-emoji">{{item.emoji}}</text>
          <view class="history-info">
            <text class="history-title">{{item.title}}</text>
            <text class="history-date">{{item.date}}</text>
          </view>
          <text class="history-status" :class="{'status-done': item.done}">
            {{item.done ? '已完成' : '进行中'}}
          </text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      rotation: 0,
      isSpinning: false,
      showResult: false,
      accepted: false,
      result: {},
      history: [],
      wheelItems: [
        { emoji: '📚', title: '阅读30分钟', desc: '找一本喜欢的书，静心阅读30分钟', tags: ['成长', '静心'], type: 'study' },
        { emoji: '🏃', title: '运动20分钟', desc: '跑步、瑜伽或任何你喜欢的运动', tags: ['健康', '活力'], type: 'sport' },
        { emoji: '📝', title: '写日记', desc: '记录今天的心情和感悟', tags: ['反思', '记录'], type: 'write' },
        { emoji: '🎨', title: '学点新东西', desc: '学习一个新技能或知识点', tags: ['学习', '探索'], type: 'learn' },
        { emoji: '🤝', title: '联系老朋友', desc: '给许久未联系的朋友发个消息', tags: ['社交', '温暖'], type: 'social' },
        { emoji: '🧘', title: '冥想10分钟', desc: '闭上眼睛，深呼吸，放空思绪', tags: ['放松', ' mindfulness'], type: 'meditate' },
        { emoji: '🌱', title: '做件好事', desc: '帮助陌生人或做一件善事', tags: ['善意', '正能量'], type: 'kindness' },
        { emoji: '🎵', title: '听音乐放松', desc: '找一首喜欢的歌，静静聆听', tags: ['放松', '享受'], type: 'music' }
      ]
    }
  },
  onShow() {
    this.loadHistory()
  },
  methods: {
    spinWheel() {
      if (this.isSpinning) return
      
      this.isSpinning = true
      this.showResult = false
      this.accepted = false
      
      const randomRotations = 5 + Math.random() * 5
      const randomDegree = Math.random() * 360
      this.rotation += randomRotations * 360 + randomDegree
      
      setTimeout(() => {
        const index = Math.floor(((360 - (this.rotation % 360)) % 360) / 45)
        this.result = this.wheelItems[index]
        this.showResult = true
        this.isSpinning = false
      }, 3000)
    },
    acceptChallenge() {
      this.accepted = true
      const challenge = {
        ...this.result,
        date: new Date().toLocaleDateString(),
        done: false,
        id: Date.now()
      }
      this.history.unshift(challenge)
      uni.setStorageSync('wheelHistory', this.history)
      uni.showToast({ title: '挑战已接受', icon: 'success' })
    },
    loadHistory() {
      this.history = uni.getStorageSync('wheelHistory') || []
    }
  }
}
</script>

<style scoped>
.container {
  padding: 30rpx;
  background: linear-gradient(180deg, #f8f9fc 0%, #eef2f7 100%);
  min-height: 100vh;
  padding-bottom: 160rpx;
}

.wheel-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.wheel-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.wheel-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 转盘 */
.wheel-container {
  display: flex;
  justify-content: center;
  margin-bottom: 40rpx;
}

.wheel-outer {
  position: relative;
  width: 500rpx;
  height: 500rpx;
}

.wheel-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  transition: transform 3s cubic-bezier(0.23, 1, 0.32, 1);
  background: conic-gradient(
    #667eea 0deg 45deg,
    #f093fb 45deg 90deg,
    #4facfe 90deg 135deg,
    #43e97b 135deg 180deg,
    #fa709a 180deg 225deg,
    #30cfd0 225deg 270deg,
    #ff9a9e 270deg 315deg,
    #a8edea 315deg 360deg
  );
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.15);
}

.wheel-segment {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 50%;
  transform-origin: left bottom;
  display: flex;
  align-items: center;
  justify-content: center;
}

.segment-text {
  font-size: 40rpx;
  transform: rotate(22.5deg);
  margin-left: 60rpx;
  margin-top: 40rpx;
}

.wheel-pointer {
  position: absolute;
  top: -20rpx;
  left: 50%;
  transform: translateX(-50%);
  font-size: 40rpx;
  color: #e94560;
  z-index: 10;
}

.wheel-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  box-shadow: 0 4rpx 20rpx rgba(102, 126, 234, 0.4);
}

.center-text {
  color: #fff;
  font-size: 28rpx;
  font-weight: bold;
}

/* 结果卡片 */
.result-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  text-align: center;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.result-header {
  margin-bottom: 20rpx;
}

.result-emoji {
  font-size: 60rpx;
  display: block;
  margin-bottom: 10rpx;
}

.result-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2d3748;
}

.result-desc {
  font-size: 28rpx;
  color: #718096;
  line-height: 1.6;
  display: block;
  margin-bottom: 20rpx;
}

.result-tags {
  display: flex;
  justify-content: center;
  gap: 16rpx;
  margin-bottom: 30rpx;
}

.result-tag {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 24rpx;
  padding: 8rpx 24rpx;
  border-radius: 20rpx;
}

.accept-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx 80rpx;
  font-size: 30rpx;
  border: none;
}

.accepted-text {
  font-size: 28rpx;
  color: #48bb78;
}

/* 历史记录 */
.history-section {
  margin-top: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20rpx;
  display: block;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.history-item {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.history-emoji {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.history-info {
  flex: 1;
}

.history-title {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.history-date {
  font-size: 22rpx;
  color: #a0aec0;
}

.history-status {
  font-size: 24rpx;
  color: #e53e3e;
  background: rgba(229, 62, 62, 0.1);
  padding: 6rpx 16rpx;
  border-radius: 12rpx;
}

.status-done {
  color: #48bb78;
  background: rgba(72, 187, 120, 0.1);
}
</style>
