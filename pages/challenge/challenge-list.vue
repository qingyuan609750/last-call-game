<template>
  <view class="container">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">🎯 七日挑战</text>
      <text class="page-desc">7天养成一个好习惯，挑战自己</text>
    </view>
    
    <!-- 进行中的挑战 -->
    <view class="section" v-if="ongoingChallenges.length > 0">
      <view class="section-header">
        <text class="section-title">进行中</text>
        <text class="section-count">{{ongoingChallenges.length}}</text>
      </view>
      <view 
        class="challenge-card ongoing" 
        v-for="(challenge, index) in ongoingChallenges" 
        :key="challenge.id"
        @click="goToDetail(challenge.id)"
      >
        <view class="challenge-info">
          <text class="challenge-title">{{challenge.title}}</text>
          <text class="challenge-desc">{{challenge.description}}</text>
          <view class="challenge-progress">
            <view class="progress-bar">
              <view class="progress-fill" :style="{width: (challenge.currentDay / 7 * 100) + '%'}"></view>
            </view>
            <text class="progress-text">第 {{challenge.currentDay}}/7 天</text>
          </view>
        </view>
        <view class="challenge-status">
          <text class="status-badge ongoing">进行中</text>
          <text class="check-icon" v-if="challenge.checkedToday">✓</text>
          <text class="check-pending" v-else>待打卡</text>
        </view>
      </view>
    </view>
    
    <!-- 推荐挑战 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">推荐挑战</text>
      </view>
      <view 
        class="challenge-card recommend" 
        v-for="(challenge, index) in recommendChallenges" 
        :key="index"
        @click="startChallenge(challenge)"
      >
        <view class="challenge-icon">{{challenge.icon}}</view>
        <view class="challenge-info">
          <text class="challenge-title">{{challenge.title}}</text>
          <text class="challenge-desc">{{challenge.description}}</text>
          <view class="challenge-tags">
            <text class="tag tag-success" v-for="(tag, i) in challenge.tags" :key="i">{{tag}}</text>
          </view>
        </view>
        <view class="challenge-action">
          <text class="action-text">开始</text>
        </view>
      </view>
    </view>
    
    <!-- 已完成挑战 -->
    <view class="section" v-if="completedChallenges.length > 0">
      <view class="section-header">
        <text class="section-title">已完成</text>
        <text class="section-count">{{completedChallenges.length}}</text>
      </view>
      <view 
        class="challenge-card completed" 
        v-for="(challenge, index) in completedChallenges" 
        :key="challenge.id"
        @click="goToDetail(challenge.id)"
      >
        <view class="challenge-info">
          <text class="challenge-title">{{challenge.title}}</text>
          <text class="challenge-desc">完成于 {{formatDate(challenge.completeDate)}}</text>
          <view class="challenge-result">
            <text class="result-text">连续打卡 {{challenge.checkInDays}} 天</text>
          </view>
        </view>
        <view class="challenge-status">
          <text class="status-badge completed">已完成</text>
        </view>
      </view>
    </view>
    
    <!-- 空状态 -->
    <view class="empty-state" v-if="challenges.length === 0">
      <text class="empty-icon">🎯</text>
      <text class="empty-text">还没有挑战</text>
      <text class="empty-desc">选择一个推荐挑战，开始你的7天之旅</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      challenges: [],
      recommendChallenges: [
        {
          icon: '📚',
          title: '每日阅读',
          description: '每天阅读30分钟，充实自己的内心世界',
          tags: ['阅读', '成长'],
          category: 'reading'
        },
        {
          icon: '🏃',
          title: '晨间运动',
          description: '每天早上运动20分钟，唤醒身体活力',
          tags: ['健康', '运动'],
          category: 'exercise'
        },
        {
          icon: '🧘',
          title: '冥想静心',
          description: '每天冥想10分钟，释放压力找回平静',
          tags: ['心理', '放松'],
          category: 'meditation'
        },
        {
          icon: '💧',
          title: '多喝水',
          description: '每天喝够8杯水，保持身体健康',
          tags: ['健康', '习惯'],
          category: 'water'
        },
        {
          icon: '📖',
          title: '写日记',
          description: '每天记录心情和感悟，留下生活印记',
          tags: ['记录', '反思'],
          category: 'diary'
        },
        {
          icon: '😴',
          title: '早睡挑战',
          description: '每晚11点前入睡，养成规律作息',
          tags: ['健康', '作息'],
          category: 'sleep'
        }
      ]
    }
  },
  computed: {
    ongoingChallenges() {
      return this.challenges.filter(c => c.status === 'ongoing')
    },
    completedChallenges() {
      return this.challenges.filter(c => c.status === 'completed')
    }
  },
  onShow() {
    this.loadChallenges()
    this.checkDailyStatus()
  },
  methods: {
    loadChallenges() {
      this.challenges = uni.getStorageSync('challenges') || []
    },
    checkDailyStatus() {
      const today = new Date().toDateString()
      this.challenges.forEach(challenge => {
        if (challenge.status === 'ongoing') {
          const lastCheck = challenge.checkInLog[challenge.checkInLog.length - 1]
          if (lastCheck) {
            const lastDate = new Date(lastCheck.date).toDateString()
            challenge.checkedToday = lastDate === today
            
            // 检查是否断签超过1天
            const lastCheckDate = new Date(lastCheck.date)
            const diffDays = Math.floor((new Date() - lastCheckDate) / (1000 * 60 * 60 * 24))
            if (diffDays > 1) {
              challenge.status = 'failed'
            }
          } else {
            challenge.checkedToday = false
          }
        }
      })
      uni.setStorageSync('challenges', this.challenges)
    },
    startChallenge(template) {
      uni.showModal({
        title: '开始挑战',
        content: `确定开始"${template.title}"挑战吗？7天内需要每日打卡。`,
        success: (res) => {
          if (res.confirm) {
            const challenge = {
              id: Date.now().toString(),
              title: template.title,
              description: template.description,
              icon: template.icon,
              category: template.category,
              tags: template.tags,
              status: 'ongoing',
              startDate: new Date().toISOString(),
              currentDay: 1,
              checkInDays: 0,
              checkInLog: [],
              checkedToday: false
            }
            
            const challenges = uni.getStorageSync('challenges') || []
            challenges.push(challenge)
            uni.setStorageSync('challenges', challenges)
            
            uni.showToast({ title: '挑战开始', icon: 'success' })
            this.loadChallenges()
          }
        }
      })
    },
    goToDetail(id) {
      uni.navigateTo({ url: `/pages/challenge/challenge-detail?id=${id}` })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日`
    }
  }
}
</script>

<style scoped>
.page-header {
  padding: 40rpx 20rpx;
  text-align: center;
}

.page-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 10rpx;
}

.page-desc {
  font-size: 26rpx;
  color: #8b8b9a;
}

.section {
  margin-bottom: 40rpx;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
  padding: 0 10rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
}

.section-count {
  font-size: 24rpx;
  color: #e94560;
  background: rgba(233, 69, 96, 0.1);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  margin-left: 16rpx;
}

.challenge-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s;
}

.challenge-card:active {
  transform: scale(0.98);
  background: rgba(255, 255, 255, 0.08);
}

.challenge-card.ongoing {
  border-left: 4rpx solid #e94560;
}

.challenge-card.completed {
  border-left: 4rpx solid #2ed573;
  opacity: 0.8;
}

.challenge-icon {
  font-size: 60rpx;
  margin-right: 24rpx;
}

.challenge-info {
  flex: 1;
}

.challenge-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 8rpx;
}

.challenge-desc {
  font-size: 24rpx;
  color: #8b8b9a;
  display: block;
  margin-bottom: 16rpx;
}

.challenge-progress {
  display: flex;
  align-items: center;
}

.progress-bar {
  flex: 1;
  height: 8rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4rpx;
  margin-right: 16rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #e94560, #ff6b6b);
  border-radius: 4rpx;
  transition: width 0.5s ease;
}

.progress-text {
  font-size: 24rpx;
  color: #e94560;
  min-width: 100rpx;
}

.challenge-status {
  text-align: center;
  margin-left: 20rpx;
}

.status-badge {
  font-size: 22rpx;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  display: block;
  margin-bottom: 10rpx;
}

.status-badge.ongoing {
  background: rgba(233, 69, 96, 0.2);
  color: #e94560;
}

.status-badge.completed {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
}

.check-icon {
  font-size: 40rpx;
  color: #2ed573;
}

.check-pending {
  font-size: 22rpx;
  color: #ffa502;
}

.challenge-tags {
  display: flex;
  flex-wrap: wrap;
}

.challenge-action {
  margin-left: 20rpx;
}

.action-text {
  font-size: 28rpx;
  color: #e94560;
  font-weight: bold;
}

.challenge-result {
  margin-top: 10rpx;
}

.result-text {
  font-size: 24rpx;
  color: #2ed573;
}
</style>
