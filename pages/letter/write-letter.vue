<template>
  <view class="container">
    <view class="write-section">
      <text class="page-title">✍️ 写给未来的自己</text>
      <text class="page-desc">写下你想对7天后的自己说的话，时间到了会自动开启</text>
      
      <!-- 信件内容输入 -->
      <view class="input-section">
        <textarea 
          class="letter-input" 
          v-model="letterContent"
          placeholder="亲爱的未来的我..."
          maxlength="1000"
          auto-height
        />
        <text class="word-count">{{letterContent.length}}/1000</text>
      </view>
      
      <!-- 开启时间选择 -->
      <view class="time-section">
        <text class="section-label">⏰ 选择开启时间</text>
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
            :class="{'time-active': selectedDays === 14}"
            @click="selectDays(14)"
          >
            <text class="time-number">14</text>
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
        
        <!-- 自定义日期 -->
        <view class="custom-date">
          <text class="date-label">或选择具体日期：</text>
          <picker mode="date" :value="customDate" :start="minDate" @change="onDateChange">
            <view class="date-picker">{{customDate || '点击选择日期'}}</view>
          </picker>
        </view>
      </view>
      
      <!-- 标签选择 -->
      <view class="tag-section">
        <text class="section-label">🏷️ 添加标签</text>
        <view class="tag-list">
          <view 
            class="tag-item" 
            v-for="(tag, index) in tags" 
            :key="index"
            :class="{'tag-selected': selectedTags.includes(tag)}"
            @click="toggleTag(tag)"
          >
            {{tag}}
          </view>
        </view>
      </view>
      
      <!-- 提交按钮 -->
      <button class="btn-primary submit-btn" @click="submitLetter" :disabled="!letterContent.trim()">
        封存信件
      </button>
      
      <!-- 提示 -->
      <text class="tip-text">💡 信件封存后不可修改，直到开启时间到达</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      letterContent: '',
      selectedDays: 7,
      customDate: '',
      selectedTags: [],
      tags: ['目标', '梦想', '感恩', '反思', '鼓励', '承诺', '秘密'],
      minDate: ''
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
    toggleTag(tag) {
      const index = this.selectedTags.indexOf(tag)
      if (index > -1) {
        this.selectedTags.splice(index, 1)
      } else {
        this.selectedTags.push(tag)
      }
    },
    submitLetter() {
      if (!this.letterContent.trim()) {
        uni.showToast({ title: '请填写信件内容', icon: 'none' })
        return
      }
      
      const letter = {
        id: Date.now().toString(),
        content: this.letterContent,
        createDate: new Date().toISOString(),
        openDate: new Date(this.customDate + 'T00:00:00').toISOString(),
        tags: this.selectedTags,
        isOpened: false,
        mood: ''
      }
      
      const letters = uni.getStorageSync('letters') || []
      letters.push(letter)
      uni.setStorageSync('letters', letters)
      
      uni.showToast({
        title: '信件已封存',
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

.input-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.letter-input {
  width: 100%;
  min-height: 300rpx;
  font-size: 30rpx;
  color: #eaeaea;
  line-height: 1.8;
}

.word-count {
  font-size: 24rpx;
  color: #6b6b7b;
  text-align: right;
  display: block;
  margin-top: 16rpx;
}

.time-section {
  margin-bottom: 30rpx;
}

.section-label {
  font-size: 30rpx;
  font-weight: bold;
  color: #eaeaea;
  display: block;
  margin-bottom: 20rpx;
}

.time-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.time-option {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20rpx;
  padding: 30rpx 40rpx;
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

.tag-section {
  margin-bottom: 40rpx;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
}

.tag-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 30rpx;
  padding: 16rpx 32rpx;
  margin-right: 16rpx;
  margin-bottom: 16rpx;
  font-size: 26rpx;
  color: #a0a0b0;
  border: 2px solid transparent;
  transition: all 0.3s;
}

.tag-selected {
  border-color: #e94560;
  background: rgba(233, 69, 96, 0.1);
  color: #e94560;
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
