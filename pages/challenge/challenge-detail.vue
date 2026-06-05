<template>
  <view class="container">
    <view class="challenge-container" v-if="challenge">
      <!-- 挑战头部 -->
      <view class="challenge-header">
        <text class="challenge-icon">{{challenge.icon}}</text>
        <text class="challenge-title">{{challenge.title}}</text>
        <text class="challenge-desc">{{challenge.description}}</text>
        <view class="challenge-meta">
          <text class="meta-item">开始于 {{formatDate(challenge.startDate)}}</text>
          <text class="meta-item" v-if="challenge.status === 'completed'">完成于 {{formatDate(challenge.completeDate)}}</text>
        </view>
      </view>
      
      <!-- 进度区域 -->
      <view class="progress-section" v-if="challenge.status === 'ongoing'">
        <view class="progress-circle">
          <view class="circle-bg">
            <view class="circle-fill" :style="{transform: `rotate(${challenge.currentDay / 7 * 360}deg)`}"></view>
          </view>
          <view class="circle-text">
            <text class="circle-day">{{challenge.currentDay}}</text>
            <text class="circle-total">/ 7 天</text>
          </view>
        </view>
        
        <!-- 今日打卡按钮 -->
        <button 
          class="btn-primary checkin-btn" 
          @click="checkIn"
          :disabled="challenge.checkedToday"
          :class="{'checked': challenge.checkedToday}"
        >
          {{challenge.checkedToday ? '今日已打卡 ✓' : '今日打卡'}}
        </button>
        
        <text class="checkin-tip" v-if="!challenge.checkedToday">
          记得今天完成"{{challenge.title}}"哦
        </text>
      </view>
      
      <!-- 已完成状态 -->
      <view class="completed-section" v-if="challenge.status === 'completed'">
        <view class="completed-icon">🎉</view>
        <text class="completed-title">挑战完成！</text>
        <text class="completed-desc">你坚持了7天，太棒了！</text>
        <view class="completed-stats">
          <view class="stat-item">
            <text class="stat-value">{{challenge.checkInDays}}</text>
            <text class="stat-label">打卡天数</text>
          </view>
          <view class="stat-item">
            <text class="stat-value">7</text>
            <text class="stat-label">总天数</text>
          </view>
          <view class="stat-item">
            <text class="stat-value">{{Math.round(challenge.checkInDays / 7 * 100)}}%</text>
            <text class="stat-label">完成率</text>
          </view>
        </view>
      </view>
      
      <!-- 打卡日历 -->
      <view class="calendar-section">
        <text class="section-title">打卡记录</text>
        <view class="calendar-grid">
          <view 
            class="calendar-day" 
            v-for="day in 7" 
            :key="day"
            :class="{
              'checked': isDayChecked(day),
              'current': day === challenge.currentDay && challenge.status === 'ongoing',
              'future': day > challenge.currentDay
            }"
          >
            <text class="day-number">{{day}}</text>
            <text class="day-status">{{getDayStatus(day)}}</text>
          </view>
        </view>
      </view>
      
      <!-- 打卡日志 -->
      <view class="log-section" v-if="challenge.checkInLog.length > 0">
        <text class="section-title">打卡日志</text>
        <view class="log-list">
          <view class="log-item" v-for="(log, index) in challenge.checkInLog" :key="index">
            <view class="log-dot"></view>
            <view class="log-content">
              <text class="log-date">{{formatDateTime(log.date)}}</text>
              <text class="log-note" v-if="log.note">{{log.note}}</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 放弃挑战 -->
      <button 
        class="btn-secondary giveup-btn" 
        @click="giveUp"
        v-if="challenge.status === 'ongoing'"
      >
        放弃挑战
      </button>
    </view>
    
    <view class="empty-state" v-else>
      <text class="empty-icon">🎯</text>
      <text class="empty-text">挑战不存在</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      challenge: null,
      challengeId: ''
    }
  },
  onLoad(options) {
    this.challengeId = options.id
    this.loadChallenge()
  },
  onShow() {
    this.loadChallenge()
  },
  methods: {
    loadChallenge() {
      const challenges = uni.getStorageSync('challenges') || []
      this.challenge = challenges.find(c => c.id === this.challengeId)
    },
    checkIn() {
      if (this.challenge.checkedToday) return
      
      uni.showModal({
        title: '今日打卡',
        content: '完成今天的挑战了吗？',
        confirmText: '完成了',
        cancelText: '还没',
        success: (res) => {
          if (res.confirm) {
            const now = new Date()
            const log = {
              date: now.toISOString(),
              day: this.challenge.currentDay,
              note: ''
            }
            
            this.challenge.checkInLog.push(log)
            this.challenge.checkInDays++
            this.challenge.checkedToday = true
            
            // 检查是否完成7天
            if (this.challenge.currentDay >= 7) {
              this.challenge.status = 'completed'
              this.challenge.completeDate = now.toISOString()
              uni.showToast({ title: '挑战完成！', icon: 'success' })
            } else {
              this.challenge.currentDay++
              this.challenge.checkedToday = false
              uni.showToast({ title: '打卡成功', icon: 'success' })
            }
            
            this.saveChallenge()
          }
        }
      })
    },
    giveUp() {
      uni.showModal({
        title: '确认放弃',
        content: '放弃后无法恢复，是否继续？',
        confirmColor: '#e94560',
        success: (res) => {
          if (res.confirm) {
            const challenges = uni.getStorageSync('challenges') || []
            const filtered = challenges.filter(c => c.id !== this.challengeId)
            uni.setStorageSync('challenges', filtered)
            uni.showToast({ title: '已放弃', icon: 'none' })
            setTimeout(() => {
              uni.navigateBack()
            }, 1500)
          }
        }
      })
    },
    saveChallenge() {
      const challenges = uni.getStorageSync('challenges') || []
      const index = challenges.findIndex(c => c.id === this.challengeId)
      if (index > -1) {
        challenges[index] = this.challenge
        uni.setStorageSync('challenges', challenges)
      }
    },
    isDayChecked(day) {
      return this.challenge.checkInLog.some(log => log.day === day)
    },
    getDayStatus(day) {
      if (this.isDayChecked(day)) return '✓'
      if (day === this.challenge.currentDay && !this.challenge.checkedToday) return '今'
      if (day > this.challenge.currentDay) return ''
      return '×'
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日`
    },
    formatDateTime(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    }
  }
}
</script>

<style scoped>
.challenge-container {
  padding: 20rpx;
}

.challenge-header {
  text-align: center;
  padding: 40rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.challenge-icon {
  font-size: 80rpx;
  display: block;
  margin-bottom: 20rpx;
}

.challenge-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 16rpx;
}

.challenge-desc {
  font-size: 26rpx;
  color: #8b8b9a;
  display: block;
  margin-bottom: 20rpx;
}

.challenge-meta {
  display: flex;
  justify-content: center;
  gap: 20rpx;
}

.meta-item {
  font-size: 24rpx;
  color: #6b6b7b;
}

.progress-section {
  text-align: center;
  padding: 40rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
}

.progress-circle {
  position: relative;
  width: 200rpx;
  height: 200rpx;
  margin: 0 auto 40rpx;
}

.circle-bg {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.circle-fill {
  position: absolute;
  top: 0;
  left: 50%;
  width: 50%;
  height: 100%;
  background: linear-gradient(180deg, #e94560, #ff6b6b);
  transform-origin: left center;
}

.circle-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.circle-day {
  font-size: 64rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
}

.circle-total {
  font-size: 24rpx;
  color: #8b8b9a;
}

.checkin-btn {
  margin-bottom: 20rpx;
}

.checkin-btn.checked {
  background: rgba(46, 213, 115, 0.2);
  border: 1px solid #2ed573;
  color: #2ed573;
}

.checkin-tip {
  font-size: 24rpx;
  color: #8b8b9a;
}

.completed-section {
  text-align: center;
  padding: 60rpx 40rpx;
  background: rgba(46, 213, 115, 0.05);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
  border: 1px solid rgba(46, 213, 115, 0.2);
}

.completed-icon {
  font-size: 100rpx;
  margin-bottom: 20rpx;
}

.completed-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2ed573;
  display: block;
  margin-bottom: 16rpx;
}

.completed-desc {
  font-size: 26rpx;
  color: #8b8b9a;
  display: block;
  margin-bottom: 40rpx;
}

.completed-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 48rpx;
  font-weight: bold;
  color: #2ed573;
  display: block;
}

.stat-label {
  font-size: 24rpx;
  color: #8b8b9a;
}

.calendar-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
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

.calendar-grid {
  display: flex;
  justify-content: space-between;
}

.calendar-day {
  width: 80rpx;
  height: 100rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid transparent;
}

.calendar-day.checked {
  background: rgba(46, 213, 115, 0.1);
  border-color: #2ed573;
}

.calendar-day.current {
  background: rgba(233, 69, 96, 0.1);
  border-color: #e94560;
}

.calendar-day.future {
  opacity: 0.5;
}

.day-number {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
}

.day-status {
  font-size: 24rpx;
  color: #8b8b9a;
}

.calendar-day.checked .day-status {
  color: #2ed573;
}

.log-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.log-list {
  padding-left: 20rpx;
}

.log-item {
  display: flex;
  align-items: flex-start;
  padding: 20rpx 0;
  border-left: 2px solid rgba(255, 255, 255, 0.1);
  padding-left: 30rpx;
  position: relative;
}

.log-dot {
  position: absolute;
  left: -8rpx;
  top: 30rpx;
  width: 14rpx;
  height: 14rpx;
  background: #e94560;
  border-radius: 50%;
}

.log-content {
  flex: 1;
}

.log-date {
  font-size: 28rpx;
  color: #eaeaea;
  display: block;
  margin-bottom: 6rpx;
}

.log-note {
  font-size: 24rpx;
  color: #8b8b9a;
}

.giveup-btn {
  width: 100%;
  color: #e94560;
  border-color: rgba(233, 69, 96, 0.3);
}
</style>
