<template>
  <view class="container">
    <view class="write-section">
      <text class="page-title">💌 给朋友的信</text>
      <text class="page-desc">写一封信给好友，设定时间后自动发送</text>
      
      <!-- 好友选择 -->
      <view class="friend-section">
        <text class="section-label">👤 收件人</text>
        <view class="friend-input">
          <input 
            class="input-field" 
            v-model="friendName"
            placeholder="输入好友昵称"
          />
        </view>
      </view>
      
      <!-- 信件内容 -->
      <view class="content-section">
        <text class="section-label">📝 信件内容</text>
        <textarea 
          class="letter-textarea" 
          v-model="letterContent"
          placeholder="想对好友说什么..."
          maxlength="800"
        />
        <text class="word-count">{{letterContent.length}}/800</text>
      </view>
      
      <!-- 发送时间 -->
      <view class="time-section">
        <text class="section-label">⏰ 发送时间</text>
        <view class="time-options">
          <view 
            class="time-option" 
            :class="{'time-active': selectedDays === 7}"
            @click="selectDays(7)"
          >
            <text class="time-number">7</text>
            <text class="time-unit">天后</text>
          </view>
          <view 
            class="time-option" 
            :class="{'time-active': selectedDays === 30}"
            @click="selectDays(30)"
          >
            <text class="time-number">30</text>
            <text class="time-unit">天后</text>
          </view>
          <view 
            class="time-option" 
            :class="{'time-active': selectedDays === 90}"
            @click="selectDays(90)"
          >
            <text class="time-number">90</text>
            <text class="time-unit">天后</text>
          </view>
        </view>
        <view class="custom-date">
          <text class="date-label">或选择具体日期：</text>
          <picker mode="date" :value="customDate" :start="minDate" @change="onDateChange">
            <view class="date-picker">{{customDate || '点击选择日期'}}</view>
          </picker>
        </view>
      </view>
      
      <!-- 提交按钮 -->
      <button class="btn-primary submit-btn" @click="submitLetter" :disabled="!canSubmit">
        发送时光信
      </button>
      
      <text class="tip-text">💡 信件将在设定时间后送达好友</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      friendName: '',
      letterContent: '',
      selectedDays: 7,
      customDate: '',
      minDate: ''
    }
  },
  computed: {
    canSubmit() {
      return this.friendName.trim() && this.letterContent.trim()
    }
  },
  onLoad() {
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    this.minDate = this.formatDate(tomorrow)
    this.customDate = this.formatDate(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000))
  },
  methods: {
    selectDays(days) {
      this.selectedDays = days
      const date = new Date()
      date.setDate(date.getDate() + days)
      this.customDate = this.formatDate(date)
    },
    onDateChange(e) {
      this.customDate = e.detail.value
      this.selectedDays = null
    },
    submitLetter() {
      if (!this.canSubmit) return
      
      const letter = {
        id: Date.now().toString(),
        friendName: this.friendName,
        content: this.letterContent,
        createDate: new Date().toISOString(),
        openDate: new Date(this.customDate + 'T00:00:00').toISOString(),
        isRead: false,
        isSent: false
      }
      
      const letters = uni.getStorageSync('friendLetters') || []
      letters.push(letter)
      uni.setStorageSync('friendLetters', letters)
      
      uni.showToast({
        title: '信件已保存',
        icon: 'success',
        duration: 2000
      })
      
      setTimeout(() => {
        uni.navigateBack()
      }, 2000)
    },
    formatDate(date) {
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }
  }
}
</script>

<style scoped>
.write-section {
  padding: 20rpx;
}

.page-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 16rpx;
}

.page-desc {
  font-size: 26rpx;
  color: #8b8b9a;
  display: block;
  margin-bottom: 40rpx;
}

.friend-section {
  margin-bottom: 30rpx;
}

.section-label {
  font-size: 30rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 16rpx;
}

.friend-input {
  margin-bottom: 20rpx;
}

.content-section {
  margin-bottom: 30rpx;
}

.letter-textarea {
  width: 100%;
  min-height: 250rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 28rpx;
  color: #eaeaea;
  line-height: 1.6;
  margin-bottom: 10rpx;
}

.word-count {
  font-size: 24rpx;
  color: #6b6b7b;
  text-align: right;
  display: block;
}

.time-section {
  margin-bottom: 40rpx;
}

.time-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.time-option {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx 50rpx;
  text-align: center;
  border: 2px solid transparent;
  transition: all 0.3s;
  flex: 1;
  margin: 0 10rpx;
}

.time-option:first-child {
  margin-left: 0;
}

.time-option:last-child {
  margin-right: 0;
}

.time-active {
  border-color: #e94560;
  background: rgba(233, 69, 96, 0.1);
}

.time-number {
  font-size: 48rpx;
  font-weight: bold;
  color: #e94560;
  display: block;
}

.time-unit {
  font-size: 24rpx;
  color: #8b8b9a;
}

.custom-date {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16rpx;
  padding: 20rpx 30rpx;
}

.date-label {
  font-size: 28rpx;
  color: #a0a0b0;
  margin-right: 20rpx;
}

.date-picker {
  font-size: 28rpx;
  color: #e94560;
  flex: 1;
}

.submit-btn {
  margin-bottom: 20rpx;
}

.tip-text {
  font-size: 24rpx;
  color: #6b6b7b;
  text-align: center;
  display: block;
}
</style>
