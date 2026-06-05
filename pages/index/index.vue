<template>
  <view class="container">
    <!-- 顶部欢迎区域 -->
    <view class="welcome-section animate-fade-in">
      <text class="welcome-title">七日之后</text>
      <text class="welcome-subtitle">给未来的自己写一封信</text>
      <view class="countdown-box" v-if="nearestLetter">
        <text class="countdown-label">最近的信件将在</text>
        <text class="countdown-time">{{countdownText}}</text>
        <text class="countdown-label">后开启</text>
      </view>
    </view>

    <!-- 功能模块入口 -->
    <view class="modules-grid">
      <!-- 时光信笺 -->
      <view class="module-card animate-fade-in" @click="goToWriteLetter" style="animation-delay: 0.1s">
        <view class="module-icon">📮</view>
        <view class="module-info">
          <text class="module-title">时光信笺</text>
          <text class="module-desc">写给7天后的自己</text>
        </view>
        <view class="module-arrow">›</view>
      </view>

      <!-- 七日挑战 -->
      <view class="module-card animate-fade-in" @click="goToChallenges" style="animation-delay: 0.2s">
        <view class="module-icon">🎯</view>
        <view class="module-info">
          <text class="module-title">七日挑战</text>
          <text class="module-desc">7天养成一个好习惯</text>
        </view>
        <view class="module-arrow">›</view>
        <view class="module-badge" v-if="activeChallenges > 0">{{activeChallenges}}</view>
      </view>

      <!-- 记忆快照 -->
      <view class="module-card animate-fade-in" @click="goToSnapshot" style="animation-delay: 0.3s">
        <view class="module-icon">📸</view>
        <view class="module-info">
          <text class="module-title">记忆快照</text>
          <text class="module-desc">记录每日心情与瞬间</text>
        </view>
        <view class="module-arrow">›</view>
      </view>

      <!-- 时光信箱 -->
      <view class="module-card animate-fade-in" @click="goToLetterBox" style="animation-delay: 0.4s">
        <view class="module-icon">💌</view>
        <view class="module-info">
          <text class="module-title">时光信箱</text>
          <text class="module-desc">给朋友的定时信件</text>
        </view>
        <view class="module-arrow">›</view>
        <view class="module-badge" v-if="unreadLetters > 0">{{unreadLetters}}</view>
      </view>
    </view>

    <!-- 最近动态 -->
    <view class="recent-section animate-fade-in" style="animation-delay: 0.5s">
      <view class="section-header">
        <text class="section-title">最近动态</text>
        <text class="section-more" @click="goToProfile">查看全部</text>
      </view>
      
      <view class="recent-list" v-if="recentActivities.length > 0">
        <view class="recent-item" v-for="(item, index) in recentActivities" :key="index">
          <view class="recent-icon">{{item.icon}}</view>
          <view class="recent-content">
            <text class="recent-text">{{item.text}}</text>
            <text class="recent-time">{{item.time}}</text>
          </view>
        </view>
      </view>
      
      <view class="empty-state" v-else>
        <text class="empty-icon">🌟</text>
        <text class="empty-text">开始你的七日之旅吧</text>
        <button class="btn-primary" @click="goToWriteLetter">写第一封信</button>
      </view>
    </view>

    <!-- 每日一句 -->
    <view class="quote-section animate-fade-in" style="animation-delay: 0.6s">
      <text class="quote-text">"{{dailyQuote}}"</text>
      <text class="quote-author">— {{quoteAuthor}}</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      letters: [],
      challenges: [],
      snapshots: [],
      friendLetters: [],
      countdownText: '',
      countdownTimer: null,
      dailyQuotes: [
        { text: '种一棵树最好的时间是十年前，其次是现在。', author: 'Dambisa Moyo' },
        { text: '未来属于那些相信梦想之美的人。', author: 'Eleanor Roosevelt' },
        { text: '不要等待机会，而要创造机会。', author: 'George Bernard Shaw' },
        { text: '今天的努力，是明天的实力。', author: '佚名' },
        { text: '坚持不是因为看到了希望，而是因为坚持了才有希望。', author: '佚名' }
      ]
    }
  },
  computed: {
    nearestLetter() {
      const now = new Date().getTime()
      const pendingLetters = this.letters.filter(l => new Date(l.openDate).getTime() > now)
      if (pendingLetters.length === 0) return null
      return pendingLetters.sort((a, b) => new Date(a.openDate) - new Date(b.openDate))[0]
    },
    activeChallenges() {
      return this.challenges.filter(c => c.status === 'ongoing').length
    },
    unreadLetters() {
      return this.friendLetters.filter(l => !l.isRead && new Date(l.openDate).getTime() <= new Date().getTime()).length
    },
    recentActivities() {
      const activities = []
      
      // 添加信件记录
      this.letters.slice(-2).forEach(l => {
        activities.push({
          icon: '📮',
          text: `写了一封给${this.formatDate(l.openDate)}的信`,
          time: this.timeAgo(l.createDate)
        })
      })
      
      // 添加挑战记录
      this.challenges.filter(c => c.status === 'ongoing').slice(-2).forEach(c => {
        activities.push({
          icon: '🎯',
          text: `正在进行"${c.title}"挑战`,
          time: `第${c.currentDay}/7天`
        })
      })
      
      // 添加快照记录
      this.snapshots.slice(-2).forEach(s => {
        activities.push({
          icon: '📸',
          text: '记录了一张记忆快照',
          time: this.timeAgo(s.date)
        })
      })
      
      return activities.sort((a, b) => new Date(b.time) - new Date(a.time)).slice(0, 5)
    },
    dailyQuote() {
      const day = new Date().getDay()
      return this.dailyQuotes[day % this.dailyQuotes.length].text
    },
    quoteAuthor() {
      const day = new Date().getDay()
      return this.dailyQuotes[day % this.dailyQuotes.length].author
    }
  },
  onShow() {
    this.loadData()
    this.startCountdown()
  },
  onHide() {
    this.stopCountdown()
  },
  methods: {
    loadData() {
      this.letters = uni.getStorageSync('letters') || []
      this.challenges = uni.getStorageSync('challenges') || []
      this.snapshots = uni.getStorageSync('snapshots') || []
      this.friendLetters = uni.getStorageSync('friendLetters') || []
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
      if (!this.nearestLetter) {
        this.countdownText = ''
        return
      }
      const now = new Date().getTime()
      const target = new Date(this.nearestLetter.openDate).getTime()
      const diff = target - now
      
      if (diff <= 0) {
        this.countdownText = '已经可以开启'
        return
      }
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((diff % (1000 * 60)) / 1000)
      
      this.countdownText = `${days}天${hours}时${minutes}分${seconds}秒`
    },
    goToWriteLetter() {
      uni.navigateTo({ url: '/pages/letter/write-letter' })
    },
    goToChallenges() {
      uni.switchTab({ url: '/pages/challenge/challenge-list' })
    },
    goToSnapshot() {
      uni.switchTab({ url: '/pages/snapshot/daily-snapshot' })
    },
    goToLetterBox() {
      uni.switchTab({ url: '/pages/friend/letter-box' })
    },
    goToProfile() {
      uni.switchTab({ url: '/pages/profile/profile' })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日`
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
      if (days < 30) return `${days}天前`
      return this.formatDate(dateStr)
    }
  }
}
</script>

<style scoped>
.welcome-section {
  text-align: center;
  padding: 60rpx 40rpx;
  background: linear-gradient(135deg, rgba(233, 69, 96, 0.1) 0%, rgba(22, 33, 62, 0) 100%);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.welcome-title {
  font-size: 56rpx;
  font-weight: bold;
  background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: block;
  margin-bottom: 16rpx;
}

.welcome-subtitle {
  font-size: 28rpx;
  color: #a0a0b0;
  display: block;
  margin-bottom: 30rpx;
}

.countdown-box {
  background: rgba(233, 69, 96, 0.1);
  border-radius: 20rpx;
  padding: 20rpx;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
}

.countdown-label {
  font-size: 24rpx;
  color: #a0a0b0;
}

.countdown-time {
  font-size: 36rpx;
  font-weight: bold;
  color: #e94560;
  margin: 8rpx 0;
}

.modules-grid {
  margin-bottom: 30rpx;
}

.module-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  transition: all 0.3s;
}

.module-card:active {
  transform: scale(0.98);
  background: rgba(255, 255, 255, 0.08);
}

.module-icon {
  font-size: 60rpx;
  margin-right: 24rpx;
}

.module-info {
  flex: 1;
}

.module-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 8rpx;
}

.module-desc {
  font-size: 24rpx;
  color: #8b8b9a;
}

.module-arrow {
  font-size: 40rpx;
  color: #8b8b9a;
}

.module-badge {
  position: absolute;
  top: 20rpx;
  right: 60rpx;
  background: #e94560;
  color: #fff;
  font-size: 22rpx;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  min-width: 32rpx;
  text-align: center;
}

.recent-section {
  margin-bottom: 30rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 0 10rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
}

.section-more {
  font-size: 26rpx;
  color: #e94560;
}

.recent-list {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 20rpx;
}

.recent-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.recent-content {
  flex: 1;
}

.recent-text {
  font-size: 28rpx;
  color: #eaeaea;
  display: block;
  margin-bottom: 6rpx;
}

.recent-time {
  font-size: 24rpx;
  color: #6b6b7b;
}

.quote-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 40rpx;
  text-align: center;
  border-left: 4rpx solid #e94560;
}

.quote-text {
  font-size: 28rpx;
  color: #a0a0b0;
  font-style: italic;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
}

.quote-author {
  font-size: 24rpx;
  color: #6b6b7b;
}
</style>
