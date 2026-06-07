<template>
  <view class="container">
    <view class="seven-header">
      <text class="seven-title">🎯 七日之后</text>
      <text class="seven-desc">给未来的自己，一个惊喜</text>
    </view>

    <!-- 功能卡片 -->
    <view class="features-list">
      <!-- 时光信笺 -->
      <view class="feature-row" @click="goToLetters">
        <view class="feature-icon-bg bg-purple">
          <text class="feature-icon">📮</text>
        </view>
        <view class="feature-content">
          <text class="feature-name">时光信笺</text>
          <text class="feature-desc">写给未来自己的信</text>
        </view>
        <view class="feature-meta">
          <text class="feature-count" v-if="letterCount > 0">{{letterCount}}封</text>
          <text class="feature-arrow">›</text>
        </view>
      </view>

      <!-- 时光胶囊 -->
      <view class="feature-row" @click="goToCapsule">
        <view class="feature-icon-bg bg-pink">
          <text class="feature-icon">💊</text>
        </view>
        <view class="feature-content">
          <text class="feature-name">时光胶囊</text>
          <text class="feature-desc">封存照片、语音、位置</text>
        </view>
        <view class="feature-meta">
          <text class="feature-count" v-if="capsuleCount > 0">{{capsuleCount}}个</text>
          <text class="feature-arrow">›</text>
        </view>
      </view>

      <!-- 七日挑战 -->
      <view class="feature-row" @click="goToChallenges">
        <view class="feature-icon-bg bg-blue">
          <text class="feature-icon">🏆</text>
        </view>
        <view class="feature-content">
          <text class="feature-name">七日挑战</text>
          <text class="feature-desc">7天养成好习惯</text>
        </view>
        <view class="feature-meta">
          <text class="feature-count" v-if="challengeCount > 0">{{challengeCount}}个</text>
          <text class="feature-arrow">›</text>
        </view>
      </view>

      <!-- 记忆快照 -->
      <view class="feature-row" @click="goToSnapshots">
        <view class="feature-icon-bg bg-green">
          <text class="feature-icon">📸</text>
        </view>
        <view class="feature-content">
          <text class="feature-name">记忆快照</text>
          <text class="feature-desc">记录每日心情瞬间</text>
        </view>
        <view class="feature-meta">
          <text class="feature-count" v-if="snapshotCount > 0">{{snapshotCount}}条</text>
          <text class="feature-arrow">›</text>
        </view>
      </view>

      <!-- 时光信箱 -->
      <view class="feature-row" @click="goToMailbox">
        <view class="feature-icon-bg bg-orange">
          <text class="feature-icon">💌</text>
        </view>
        <view class="feature-content">
          <text class="feature-name">时光信箱</text>
          <text class="feature-desc">给好友的定时信</text>
        </view>
        <view class="feature-meta">
          <text class="feature-count" v-if="mailCount > 0">{{mailCount}}封</text>
          <text class="feature-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 最近动态 -->
    <view class="recent-section" v-if="recentActivities.length > 0">
      <text class="section-title">最近动态</text>
      <view class="recent-list">
        <view class="recent-item" v-for="(item, index) in recentActivities" :key="index">
          <text class="recent-icon">{{item.icon}}</text>
          <view class="recent-info">
            <text class="recent-text">{{item.text}}</text>
            <text class="recent-time">{{item.time}}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      letterCount: 0,
      capsuleCount: 0,
      challengeCount: 0,
      snapshotCount: 0,
      mailCount: 0,
      recentActivities: []
    }
  },
  onShow() {
    this.loadData()
  },
  methods: {
    loadData() {
      const letters = uni.getStorageSync('letters') || []
      const capsules = uni.getStorageSync('capsules') || []
      const challenges = uni.getStorageSync('challenges') || []
      const snapshots = uni.getStorageSync('snapshots') || []
      const mails = uni.getStorageSync('friendLetters') || []

      this.letterCount = letters.length
      this.capsuleCount = capsules.length
      this.challengeCount = challenges.filter(c => c.status === 'ongoing').length
      this.snapshotCount = snapshots.length
      this.mailCount = mails.length

      // 生成最近动态
      this.recentActivities = []
      if (letters.length > 0) {
        const last = letters[letters.length - 1]
        this.recentActivities.push({
          icon: '📮',
          text: '写了一封时光信',
          time: this.timeAgo(last.createDate)
        })
      }
      if (challenges.length > 0) {
        const ongoing = challenges.filter(c => c.status === 'ongoing')
        if (ongoing.length > 0) {
          this.recentActivities.push({
            icon: '🏆',
            text: `正在进行"${ongoing[0].title}"挑战`,
            time: `第${ongoing[0].currentDay}/7天`
          })
        }
      }
      if (snapshots.length > 0) {
        const last = snapshots[snapshots.length - 1]
        this.recentActivities.push({
          icon: '📸',
          text: '记录了一张记忆快照',
          time: this.timeAgo(last.date)
        })
      }
    },
    goToLetters() {
      uni.navigateTo({ url: '/pages/letter/write-letter' })
    },
    goToCapsule() {
      uni.navigateTo({ url: '/pages/seven/capsule' })
    },
    goToChallenges() {
      uni.navigateTo({ url: '/pages/challenge/challenge-list' })
    },
    goToSnapshots() {
      uni.navigateTo({ url: '/pages/snapshot/daily-snapshot' })
    },
    goToMailbox() {
      uni.navigateTo({ url: '/pages/friend/letter-box' })
    },
    timeAgo(dateStr) {
      const now = new Date().getTime()
      const date = new Date(dateStr).getTime()
      const diff = now - date
      const minutes = Math.floor(diff / (1000 * 60))
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))

      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      return `${days}天前`
    }
  }
}
</script>

<style scoped>
.container {
  padding: 30rpx;
  background: linear-gradient(180deg, #f8f9fc 0%, #eef2f7 100%);
  min-height: 100vh;
}

.seven-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.seven-title {
  font-size: 44rpx;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: block;
  margin-bottom: 10rpx;
}

.seven-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 功能列表 */
.features-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 30rpx;
}

.feature-row {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

.feature-row:active {
  transform: scale(0.98);
  background: #f7fafc;
}

.feature-icon-bg {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.bg-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-pink {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.bg-blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.bg-green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.bg-orange {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.feature-icon {
  font-size: 40rpx;
}

.feature-content {
  flex: 1;
}

.feature-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.feature-desc {
  font-size: 24rpx;
  color: #a0aec0;
}

.feature-meta {
  display: flex;
  align-items: center;
}

.feature-count {
  font-size: 22rpx;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  margin-right: 12rpx;
}

.feature-arrow {
  font-size: 32rpx;
  color: #a0aec0;
}

/* 最近动态 */
.recent-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20rpx;
  display: block;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.recent-item {
  display: flex;
  align-items: center;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-icon {
  font-size: 36rpx;
  margin-right: 16rpx;
}

.recent-info {
  flex: 1;
}

.recent-text {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.recent-time {
  font-size: 22rpx;
  color: #a0aec0;
}
</style>
