<template>
  <view class="container">
    <!-- 月份选择 -->
    <view class="month-selector">
      <text class="month-arrow" @click="changeMonth(-1)">‹</text>
      <text class="month-text">{{currentYear}}年{{currentMonth + 1}}月</text>
      <text class="month-arrow" @click="changeMonth(1)">›</text>
    </view>
    
    <!-- 星期标题 -->
    <view class="week-header">
      <text class="week-day" v-for="day in weekDays" :key="day">{{day}}</text>
    </view>
    
    <!-- 日历网格 -->
    <view class="calendar-grid">
      <view 
        class="calendar-cell" 
        v-for="(cell, index) in calendarCells" 
        :key="index"
        :class="{
          'other-month': !cell.isCurrentMonth,
          'has-snapshot': cell.snapshot,
          'today': cell.isToday
        }"
        @click="cell.snapshot ? showSnapshotDetail(cell.snapshot) : null"
      >
        <text class="cell-date">{{cell.date}}</text>
        <view class="cell-mood" v-if="cell.snapshot">
          <text class="mood-emoji">{{cell.snapshot.mood.emoji}}</text>
        </view>
        <view class="cell-dot" v-else-if="cell.isCurrentMonth"></view>
      </view>
    </view>
    
    <!-- 月度统计 -->
    <view class="stats-section">
      <text class="section-title">本月统计</text>
      <view class="stats-grid">
        <view class="stat-card">
          <text class="stat-value">{{monthStats.total}}</text>
          <text class="stat-label">记录天数</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{monthStats.mostMood}}</text>
          <text class="stat-label">最常心情</text>
        </view>
        <view class="stat-card">
          <text class="stat-value">{{monthStats.rate}}%</text>
          <text class="stat-label">记录率</text>
        </view>
      </view>
      
      <!-- 心情分布 -->
      <view class="mood-distribution">
        <text class="dist-title">心情分布</text>
        <view class="dist-list">
          <view class="dist-item" v-for="(item, index) in moodDistribution" :key="index">
            <text class="dist-emoji">{{item.emoji}}</text>
            <view class="dist-bar">
              <view class="dist-fill" :style="{width: item.percentage + '%'}"></view>
            </view>
            <text class="dist-count">{{item.count}}天</text>
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
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth(),
      weekDays: ['日', '一', '二', '三', '四', '五', '六'],
      snapshots: []
    }
  },
  computed: {
    calendarCells() {
      const cells = []
      const firstDay = new Date(this.currentYear, this.currentMonth, 1)
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0)
      const startDate = new Date(firstDay)
      startDate.setDate(startDate.getDate() - firstDay.getDay())
      
      const today = new Date()
      
      for (let i = 0; i < 42; i++) {
        const date = new Date(startDate)
        date.setDate(startDate.getDate() + i)
        
        const snapshot = this.snapshots.find(s => {
          const sDate = new Date(s.date)
          return sDate.toDateString() === date.toDateString()
        })
        
        cells.push({
          date: date.getDate(),
          isCurrentMonth: date.getMonth() === this.currentMonth,
          isToday: date.toDateString() === today.toDateString(),
          snapshot: snapshot || null
        })
      }
      
      return cells
    },
    monthStats() {
      const monthSnapshots = this.snapshots.filter(s => {
        const date = new Date(s.date)
        return date.getFullYear() === this.currentYear && date.getMonth() === this.currentMonth
      })
      
      const total = monthSnapshots.length
      const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate()
      const rate = Math.round(total / daysInMonth * 100)
      
      const moodCount = {}
      monthSnapshots.forEach(s => {
        const label = s.mood.label
        moodCount[label] = (moodCount[label] || 0) + 1
      })
      
      const mostMood = Object.entries(moodCount).sort((a, b) => b[1] - a[1])[0]?.[0] || '-'
      
      return { total, mostMood, rate }
    },
    moodDistribution() {
      const monthSnapshots = this.snapshots.filter(s => {
        const date = new Date(s.date)
        return date.getFullYear() === this.currentYear && date.getMonth() === this.currentMonth
      })
      
      const moodCount = {}
      monthSnapshots.forEach(s => {
        const label = s.mood.label
        const emoji = s.mood.emoji
        if (!moodCount[label]) {
          moodCount[label] = { label, emoji, count: 0 }
        }
        moodCount[label].count++
      })
      
      const total = monthSnapshots.length
      return Object.values(moodCount)
        .map(m => ({
          ...m,
          percentage: total > 0 ? Math.round(m.count / total * 100) : 0
        }))
        .sort((a, b) => b.count - a.count)
    }
  },
  onShow() {
    this.loadSnapshots()
  },
  methods: {
    loadSnapshots() {
      this.snapshots = uni.getStorageSync('snapshots') || []
    },
    changeMonth(delta) {
      this.currentMonth += delta
      if (this.currentMonth > 11) {
        this.currentMonth = 0
        this.currentYear++
      } else if (this.currentMonth < 0) {
        this.currentMonth = 11
        this.currentYear--
      }
    },
    showSnapshotDetail(snapshot) {
      uni.showModal({
        title: `${new Date(snapshot.date).getMonth() + 1}月${new Date(snapshot.date).getDate()}日的记录`,
        content: `${snapshot.mood.emoji} ${snapshot.mood.label}\n\n${snapshot.content}`,
        showCancel: false
      })
    }
  }
}
</script>

<style scoped>
.month-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx 40rpx;
  margin-bottom: 20rpx;
}

.month-arrow {
  font-size: 48rpx;
  color: #e94560;
  padding: 10rpx 20rpx;
}

.month-text {
  font-size: 36rpx;
  font-weight: bold;
  color: #eaeaea;
}

.week-header {
  display: flex;
  padding: 20rpx 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.week-day {
  flex: 1;
  text-align: center;
  font-size: 26rpx;
  color: #8b8b9a;
}

.calendar-grid {
  display: flex;
  flex-wrap: wrap;
  padding: 20rpx 0;
}

.calendar-cell {
  width: 14.28%;
  height: 100rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
  margin-bottom: 10rpx;
  transition: all 0.3s;
}

.calendar-cell.other-month {
  opacity: 0.3;
}

.calendar-cell.has-snapshot {
  background: rgba(233, 69, 96, 0.1);
}

.calendar-cell.today {
  border: 2px solid #e94560;
}

.cell-date {
  font-size: 28rpx;
  color: #eaeaea;
}

.cell-mood {
  margin-top: 4rpx;
}

.mood-emoji {
  font-size: 32rpx;
}

.cell-dot {
  width: 8rpx;
  height: 8rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  margin-top: 8rpx;
}

.stats-section {
  margin-top: 30rpx;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 20rpx;
}

.stats-grid {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30rpx;
}

.stat-card {
  flex: 1;
  text-align: center;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  margin: 0 10rpx;
}

.stat-card:first-child {
  margin-left: 0;
}

.stat-card:last-child {
  margin-right: 0;
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

.mood-distribution {
  margin-top: 20rpx;
}

.dist-title {
  font-size: 28rpx;
  color: #a0a0b0;
  display: block;
  margin-bottom: 16rpx;
}

.dist-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.dist-item {
  display: flex;
  align-items: center;
}

.dist-emoji {
  font-size: 36rpx;
  margin-right: 16rpx;
  width: 60rpx;
}

.dist-bar {
  flex: 1;
  height: 16rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8rpx;
  overflow: hidden;
  margin-right: 16rpx;
}

.dist-fill {
  height: 100%;
  background: linear-gradient(90deg, #e94560, #ff6b6b);
  border-radius: 8rpx;
  transition: width 0.5s ease;
}

.dist-count {
  font-size: 24rpx;
  color: #8b8b9a;
  min-width: 80rpx;
  text-align: right;
}
</style>
