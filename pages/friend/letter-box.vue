<template>
  <view class="container">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">📬 时光信箱</text>
      <text class="page-desc">查看已发送和收到的时光信</text>
    </view>
    
    <!-- 写信按钮 -->
    <button class="btn-primary write-btn" @click="goToWriteLetter">
      ✍️ 写一封新信
    </button>
    
    <!-- 标签切换 -->
    <view class="tab-bar">
      <view 
        class="tab-item" 
        :class="{'tab-active': currentTab === 'sent'}"
        @click="currentTab = 'sent'"
      >
        <text class="tab-text">已发送</text>
        <text class="tab-badge" v-if="sentLetters.length > 0">{{sentLetters.length}}</text>
      </view>
      <view 
        class="tab-item" 
        :class="{'tab-active': currentTab === 'received'}"
        @click="currentTab = 'received'"
      >
        <text class="tab-text">待开启</text>
        <text class="tab-badge" v-if="pendingLetters.length > 0">{{pendingLetters.length}}</text>
      </view>
    </view>
    
    <!-- 已发送列表 -->
    <view class="letter-list" v-if="currentTab === 'sent'">
      <view class="letter-card" v-for="(letter, index) in sentLetters" :key="letter.id">
        <view class="letter-header">
          <text class="letter-to">To: {{letter.friendName}}</text>
          <text class="letter-status" :class="{'status-pending': !canOpen(letter), 'status-open': canOpen(letter)}">
            {{canOpen(letter) ? '已可开启' : '封存中'}}
          </text>
        </view>
        <text class="letter-preview">{{letter.content.substring(0, 50)}}...</text>
        <view class="letter-footer">
          <text class="letter-date">发送于 {{formatDate(letter.createDate)}}</text>
          <text class="letter-open-date">{{canOpen(letter) ? '已经可以开启' : '将于 ' + formatDate(letter.openDate) + ' 开启'}}</text>
        </view>
      </view>
      
      <view class="empty-state" v-if="sentLetters.length === 0">
        <text class="empty-icon">💌</text>
        <text class="empty-text">还没有发送信件</text>
        <text class="empty-desc">给好友写一封时光信吧</text>
      </view>
    </view>
    
    <!-- 待开启列表 -->
    <view class="letter-list" v-if="currentTab === 'received'">
      <view class="letter-card" v-for="(letter, index) in pendingLetters" :key="letter.id">
        <view class="letter-header">
          <text class="letter-from">来自: {{letter.friendName || '未知'}}</text>
          <text class="letter-status" :class="{'status-pending': !canOpen(letter), 'status-open': canOpen(letter)}">
            {{canOpen(letter) ? '可开启' : '待开启'}}
          </text>
        </view>
        <view class="letter-lock" v-if="!canOpen(letter)">
          <text class="lock-icon">🔒</text>
          <text class="lock-text">信件封存中</text>
          <text class="lock-countdown">{{getCountdown(letter)}}</text>
        </view>
        <view class="letter-unlock" v-else @click="openLetter(letter)">
          <text class="unlock-icon">🔓</text>
          <text class="unlock-text">点击开启信件</text>
        </view>
        <view class="letter-footer">
          <text class="letter-date">预计开启: {{formatDate(letter.openDate)}}</text>
        </view>
      </view>
      
      <view class="empty-state" v-if="pendingLetters.length === 0">
        <text class="empty-icon">📭</text>
        <text class="empty-text">没有待开启的信件</text>
        <text class="empty-desc">让好友给你写一封时光信吧</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentTab: 'sent',
      friendLetters: []
    }
  },
  computed: {
    sentLetters() {
      return this.friendLetters.filter(l => l.friendName && !l.isReceived)
    },
    pendingLetters() {
      return this.friendLetters.filter(l => !l.isRead || !canOpen(l))
    }
  },
  onShow() {
    this.loadLetters()
  },
  methods: {
    loadLetters() {
      this.friendLetters = uni.getStorageSync('friendLetters') || []
    },
    canOpen(letter) {
      return new Date(letter.openDate).getTime() <= new Date().getTime()
    },
    getCountdown(letter) {
      const diff = new Date(letter.openDate).getTime() - new Date().getTime()
      if (diff <= 0) return '已经可以开启'
      
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      return `还有 ${days}天${hours}小时`
    },
    openLetter(letter) {
      uni.showModal({
        title: '来自 ' + letter.friendName + ' 的信',
        content: letter.content,
        showCancel: false,
        success: () => {
          letter.isRead = true
          const letters = uni.getStorageSync('friendLetters') || []
          const index = letters.findIndex(l => l.id === letter.id)
          if (index > -1) {
            letters[index] = letter
            uni.setStorageSync('friendLetters', letters)
          }
        }
      })
    },
    goToWriteLetter() {
      uni.navigateTo({ url: '/pages/friend/friend-letter' })
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
  text-align: center;
  padding: 40rpx 20rpx;
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

.write-btn {
  margin: 0 20rpx 30rpx;
}

.tab-bar {
  display: flex;
  margin: 0 20rpx 30rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16rpx;
  padding: 8rpx;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 20rpx;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.tab-active {
  background: rgba(233, 69, 96, 0.2);
}

.tab-text {
  font-size: 28rpx;
  color: #a0a0b0;
}

.tab-active .tab-text {
  color: #e94560;
  font-weight: bold;
}

.tab-badge {
  font-size: 20rpx;
  color: #fff;
  background: #e94560;
  padding: 2rpx 12rpx;
  border-radius: 20rpx;
  margin-left: 10rpx;
}

.letter-list {
  padding: 0 20rpx;
}

.letter-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.letter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.letter-to, .letter-from {
  font-size: 30rpx;
  font-weight: bold;
  color: #eaeaea;
}

.letter-status {
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.status-pending {
  background: rgba(255, 165, 2, 0.2);
  color: #ffa502;
}

.status-open {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
}

.letter-preview {
  font-size: 28rpx;
  color: #a0a0b0;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
}

.letter-footer {
  display: flex;
  justify-content: space-between;
}

.letter-date {
  font-size: 24rpx;
  color: #6b6b7b;
}

.letter-open-date {
  font-size: 24rpx;
  color: #e94560;
}

.letter-lock {
  text-align: center;
  padding: 40rpx;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16rpx;
  margin-bottom: 16rpx;
}

.lock-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 10rpx;
}

.lock-text {
  font-size: 28rpx;
  color: #a0a0b0;
  display: block;
  margin-bottom: 8rpx;
}

.lock-countdown {
  font-size: 24rpx;
  color: #e94560;
}

.letter-unlock {
  text-align: center;
  padding: 40rpx;
  background: rgba(46, 213, 115, 0.05);
  border-radius: 16rpx;
  margin-bottom: 16rpx;
  border: 2px solid rgba(46, 213, 115, 0.3);
}

.unlock-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 10rpx;
}

.unlock-text {
  font-size: 28rpx;
  color: #2ed573;
}
</style>
