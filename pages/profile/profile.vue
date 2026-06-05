<template>
  <view class="container">
    <!-- 用户信息 -->
    <view class="user-section">
      <view class="user-avatar">
        <text class="avatar-text">👤</text>
      </view>
      <text class="user-name">时光旅人</text>
      <text class="user-desc">已加入七日之后 {{joinDays}} 天</text>
    </view>
    
    <!-- 数据统计 -->
    <view class="stats-section">
      <view class="stat-item" @click="goToStatistics">
        <text class="stat-value">{{stats.letters}}</text>
        <text class="stat-label">时光信</text>
      </view>
      <view class="stat-item" @click="goToStatistics">
        <text class="stat-value">{{stats.challenges}}</text>
        <text class="stat-label">挑战</text>
      </view>
      <view class="stat-item" @click="goToStatistics">
        <text class="stat-value">{{stats.snapshots}}</text>
        <text class="stat-label">快照</text>
      </view>
      <view class="stat-item" @click="goToStatistics">
        <text class="stat-value">{{stats.friendLetters}}</text>
        <text class="stat-label">好友信</text>
      </view>
    </view>
    
    <!-- 功能列表 -->
    <view class="menu-section">
      <view class="menu-item" @click="goToMyLetters">
        <view class="menu-icon">📮</view>
        <view class="menu-info">
          <text class="menu-title">我的时光信</text>
          <text class="menu-desc">查看所有写给未来的信</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
      
      <view class="menu-item" @click="goToMyChallenges">
        <view class="menu-icon">🎯</view>
        <view class="menu-info">
          <text class="menu-title">我的挑战</text>
          <text class="menu-desc">查看挑战记录</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
      
      <view class="menu-item" @click="goToCalendar">
        <view class="menu-icon">📅</view>
        <view class="menu-info">
          <text class="menu-title">时光日历</text>
          <text class="menu-desc">查看记忆快照日历</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
      
      <view class="menu-item" @click="goToStatistics">
        <view class="menu-icon">📊</view>
        <view class="menu-info">
          <text class="menu-title">数据统计</text>
          <text class="menu-desc">查看详细统计信息</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>
    
    <!-- 设置 -->
    <view class="menu-section">
      <view class="menu-item" @click="clearData">
        <view class="menu-icon">🗑️</view>
        <view class="menu-info">
          <text class="menu-title">清除数据</text>
          <text class="menu-desc">清空所有本地数据</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
      
      <view class="menu-item">
        <view class="menu-icon">ℹ️</view>
        <view class="menu-info">
          <text class="menu-title">关于</text>
          <text class="menu-desc">七日之后 v1.0.0</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      joinDays: 1,
      stats: {
        letters: 0,
        challenges: 0,
        snapshots: 0,
        friendLetters: 0
      }
    }
  },
  onShow() {
    this.loadStats()
    this.calculateJoinDays()
  },
  methods: {
    loadStats() {
      const letters = uni.getStorageSync('letters') || []
      const challenges = uni.getStorageSync('challenges') || []
      const snapshots = uni.getStorageSync('snapshots') || []
      const friendLetters = uni.getStorageSync('friendLetters') || []
      
      this.stats = {
        letters: letters.length,
        challenges: challenges.length,
        snapshots: snapshots.length,
        friendLetters: friendLetters.length
      }
    },
    calculateJoinDays() {
      const firstUse = uni.getStorageSync('firstUseDate')
      if (firstUse) {
        const diff = new Date() - new Date(firstUse)
        this.joinDays = Math.floor(diff / (1000 * 60 * 60 * 24)) + 1
      } else {
        uni.setStorageSync('firstUseDate', new Date().toISOString())
        this.joinDays = 1
      }
    },
    goToMyLetters() {
      uni.navigateTo({ url: '/pages/letter/letter-list' })
    },
    goToMyChallenges() {
      uni.switchTab({ url: '/pages/challenge/challenge-list' })
    },
    goToCalendar() {
      uni.navigateTo({ url: '/pages/snapshot/snapshot-calendar' })
    },
    goToStatistics() {
      uni.navigateTo({ url: '/pages/profile/statistics' })
    },
    clearData() {
      uni.showModal({
        title: '确认清除',
        content: '这将清空所有数据，包括信件、挑战和快照。确定继续吗？',
        confirmColor: '#e94560',
        success: (res) => {
          if (res.confirm) {
            uni.clearStorageSync()
            uni.showToast({ title: '数据已清除', icon: 'success' })
            this.loadStats()
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.user-section {
  text-align: center;
  padding: 60rpx 40rpx;
  background: linear-gradient(135deg, rgba(233, 69, 96, 0.1) 0%, rgba(22, 33, 62, 0) 100%);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.user-avatar {
  width: 120rpx;
  height: 120rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20rpx;
}

.avatar-text {
  font-size: 60rpx;
}

.user-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 10rpx;
}

.user-desc {
  font-size: 26rpx;
  color: #8b8b9a;
}

.stats-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  margin: 0 10rpx;
  transition: all 0.3s;
}

.stat-item:first-child {
  margin-left: 0;
}

.stat-item:last-child {
  margin-right: 0;
}

.stat-item:active {
  background: rgba(255, 255, 255, 0.08);
}

.stat-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #e94560;
  display: block;
  margin-bottom: 8rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #8b8b9a;
}

.menu-section {
  margin-bottom: 20rpx;
}

.menu-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 16rpx;
  display: flex;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.menu-item:active {
  background: rgba(255, 255, 255, 0.08);
}

.menu-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.menu-info {
  flex: 1;
}

.menu-title {
  font-size: 30rpx;
  color: #eaeaea;
  display: block;
  margin-bottom: 6rpx;
}

.menu-desc {
  font-size: 24rpx;
  color: #8b8b9a;
}

.menu-arrow {
  font-size: 32rpx;
  color: #8b8b9a;
}
</style>
