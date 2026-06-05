<template>
  <view class="container">
    <text class="page-title">📊 数据统计</text>
    
    <!-- 总览卡片 -->
    <view class="overview-section">
      <view class="overview-card">
        <text class="overview-number">{{totalActivities}}</text>
        <text class="overview-label">总记录数</text>
      </view>
      <view class="overview-card">
        <text class="overview-number">{{consecutiveDays}}</text>
        <text class="overview-label">连续记录天数</text>
      </view>
    </view>
    
    <!-- 分类统计 -->
    <view class="category-section">
      <text class="section-title">分类统计</text>
      
      <view class="category-item">
        <view class="category-icon">📮</view>
        <view class="category-info">
          <text class="category-name">时光信笺</text>
          <text class="category-count">{{stats.letters}} 封信</text>
        </view>
        <view class="category-bar">
          <view class="category-fill" :style="{width: getPercentage(stats.letters) + '%'}"></view>
        </view>
      </view>
      
      <view class="category-item">
        <view class="category-icon">🎯</view>
        <view class="category-info">
          <text class="category-name">七日挑战</text>
          <text class="category-count">{{stats.challenges}} 个挑战</text>
        </view>
        <view class="category-bar">
          <view class="category-fill" :style="{width: getPercentage(stats.challenges) + '%'}"></view>
        </view>
      </view>
      
      <view class="category-item">
        <view class="category-icon">📸</view>
        <view class="category-info">
          <text class="category-name">记忆快照</text>
          <text class="category-count">{{stats.snapshots}} 条记录</text>
        </view>
        <view class="category-bar">
          <view class="category-fill" :style="{width: getPercentage(stats.snapshots) + '%'}"></view>
        </view>
      </view>
      
      <view class="category-item">
        <view class="category-icon">💌</view>
        <view class="category-info">
          <text class="category-name">时光信箱</text>
          <text class="category-count">{{stats.friendLetters}} 封信</text>
        </view>
        <view class="category-bar">
          <view class="category-fill" :style="{width: getPercentage(stats.friendLetters) + '%'}"></view>
        </view>
      </view>
    </view>
    
    <!-- 心情分布 -->
    <view class="mood-section" v-if="moodDistribution.length > 0">
      <text class="section-title">心情分布</text>
      <view class="mood-chart">
        <view class="mood-item" v-for="(item, index) in moodDistribution" :key="index">
          <text class="mood-emoji">{{item.emoji}}</text>
          <view class="mood-bar">
            <view class="mood-fill" :style="{width: item.percentage + '%'}"></view>
          </view>
          <text class="mood-count">{{item.count}}次</text>
        </view>
      </view>
    </view>
    
    <!-- 挑战成就 -->
    <view class="achievement-section" v-if="challengeStats.completed > 0">
      <text class="section-title">挑战成就</text>
      <view class="achievement-grid">
        <view class="achievement-card">
          <text class="achievement-value">{{challengeStats.completed}}</text>
          <text class="achievement-label">已完成</text>
        </view>
        <view class="achievement-card">
          <text class="achievement-value">{{challengeStats.ongoing}}</text>
          <text class="achievement-label">进行中</text>
        </view>
        <view class="achievement-card">
          <text class="achievement-value">{{challengeStats.totalCheckIns}}</text>
          <text class="achievement-label">总打卡</text>
        </view>
        <view class="achievement-card">
          <text class="achievement-value">{{challengeStats.successRate}}%</text>
          <text class="achievement-label">成功率</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      stats: {
        letters: 0,
        challenges: 0,
        snapshots: 0,
        friendLetters: 0
      },
      moodDistribution: [],
      challengeStats: {
        completed: 0,
        ongoing: 0,
        totalCheckIns: 0,
        successRate: 0
      },
      consecutiveDays: 0
    }
  },
  computed: {
    totalActivities() {
      return this.stats.letters + this.stats.challenges + this.stats.snapshots + this.stats.friendLetters
    }
  },
  onShow() {
    this.loadStatistics()
  },
  methods: {
    loadStatistics() {
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
      
      // 计算心情分布
      const moodCount = {}
      snapshots.forEach(s => {
        const label = s.mood.label
        const emoji = s.mood.emoji
        if (!moodCount[label]) {
          moodCount[label] = { label, emoji, count: 0 }
        }
        moodCount[label].count++
      })
      
      const totalMoods = snapshots.length
      this.moodDistribution = Object.values(moodCount)
        .map(m => ({
          ...m,
          percentage: totalMoods > 0 ? Math.round(m.count / totalMoods * 100) : 0
        }))
        .sort((a, b) => b.count - a.count)
      
      // 计算挑战统计
      this.challengeStats = {
        completed: challenges.filter(c => c.status === 'completed').length,
        ongoing: challenges.filter(c => c.status === 'ongoing').length,
        totalCheckIns: challenges.reduce((sum, c) => sum + (c.checkInDays || 0), 0),
        successRate: challenges.length > 0 
          ? Math.round(challenges.filter(c => c.status === 'completed').length / challenges.length * 100)
          : 0
      }
      
      // 计算连续记录天数
      this.calculateConsecutiveDays(snapshots)
    },
    calculateConsecutiveDays(snapshots) {
      if (snapshots.length === 0) {
        this.consecutiveDays = 0
        return
      }
      
      const dates = snapshots.map(s => new Date(s.date).toDateString()).sort()
      const uniqueDates = [...new Set(dates)]
      
      let maxConsecutive = 1
      let currentConsecutive = 1
      
      for (let i = 1; i < uniqueDates.length; i++) {
        const prevDate = new Date(uniqueDates[i - 1])
        const currDate = new Date(uniqueDates[i])
        const diffDays = (currDate - prevDate) / (1000 * 60 * 60 * 24)
        
        if (diffDays === 1) {
          currentConsecutive++
          maxConsecutive = Math.max(maxConsecutive, currentConsecutive)
        } else {
          currentConsecutive = 1
        }
      }
      
      this.consecutiveDays = maxConsecutive
    },
    getPercentage(value) {
      const max = Math.max(this.stats.letters, this.stats.challenges, this.stats.snapshots, this.stats.friendLetters, 1)
      return Math.round(value / max * 100)
    }
  }
}
</script>

<style scoped>
.page-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  text-align: center;
  padding: 40rpx 20rpx;
}

.overview-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.overview-card {
  flex: 1;
  text-align: center;
  padding: 40rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  margin: 0 10rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.overview-card:first-child {
  margin-left: 0;
}

.overview-card:last-child {
  margin-right: 0;
}

.overview-number {
  font-size: 48rpx;
  font-weight: bold;
  color: #e94560;
  display: block;
  margin-bottom: 10rpx;
}

.overview-label {
  font-size: 26rpx;
  color: #8b8b9a;
}

.category-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 20rpx;
}

.category-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.category-item:last-child {
  border-bottom: none;
}

.category-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.category-info {
  flex: 1;
}

.category-name {
  font-size: 28rpx;
  color: #eaeaea;
  display: block;
}

.category-count {
  font-size: 24rpx;
  color: #8b8b9a;
}

.category-bar {
  width: 120rpx;
  height: 8rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4rpx;
  overflow: hidden;
}

.category-fill {
  height: 100%;
  background: linear-gradient(90deg, #e94560, #ff6b6b);
  border-radius: 4rpx;
  transition: width 0.5s ease;
}

.mood-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.mood-chart {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.mood-item {
  display: flex;
  align-items: center;
}

.mood-emoji {
  font-size: 36rpx;
  margin-right: 16rpx;
  width: 60rpx;
}

.mood-bar {
  flex: 1;
  height: 16rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8rpx;
  overflow: hidden;
  margin-right: 16rpx;
}

.mood-fill {
  height: 100%;
  background: linear-gradient(90deg, #e94560, #ff6b6b);
  border-radius: 8rpx;
  transition: width 0.5s ease;
}

.mood-count {
  font-size: 24rpx;
  color: #8b8b9a;
  min-width: 80rpx;
  text-align: right;
}

.achievement-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.achievement-grid {
  display: flex;
  justify-content: space-between;
}

.achievement-card {
  flex: 1;
  text-align: center;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16rpx;
  margin: 0 8rpx;
}

.achievement-card:first-child {
  margin-left: 0;
}

.achievement-card:last-child {
  margin-right: 0;
}

.achievement-value {
  font-size: 36rpx;
  font-weight: bold;
  color: #e94560;
  display: block;
  margin-bottom: 8rpx;
}

.achievement-label {
  font-size: 24rpx;
  color: #8b8b9a;
}
</style>
