<template>
  <view class="container">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="page-title">📸 记忆快照</text>
      <text class="page-desc">记录每一天的心情与瞬间</text>
    </view>
    
    <!-- 今日快照输入 -->
    <view class="snapshot-input">
      <view class="input-header">
        <text class="input-title">今天过得怎么样？</text>
        <text class="input-date">{{todayDate}}</text>
      </view>
      
      <!-- 心情选择 -->
      <view class="mood-selector">
        <text class="selector-label">心情</text>
        <view class="mood-options">
          <view 
            class="mood-item" 
            v-for="(mood, index) in moods" 
            :key="index"
            :class="{'mood-selected': selectedMood === mood}"
            @click="selectMood(mood)"
          >
            <text class="mood-emoji">{{mood.emoji}}</text>
            <text class="mood-label">{{mood.label}}</text>
          </view>
        </view>
      </view>
      
      <!-- 文字记录 -->
      <textarea 
        class="snapshot-textarea" 
        v-model="snapshotContent"
        placeholder="记录今天发生的美好瞬间..."
        maxlength="500"
      />
      <text class="word-count">{{snapshotContent.length}}/500</text>
      
      <!-- 图片上传 -->
      <view class="image-section">
        <view class="image-list">
          <view class="image-item" v-for="(img, index) in images" :key="index">
            <image :src="img" mode="aspectFill" class="uploaded-image" />
            <view class="image-delete" @click="removeImage(index)">×</view>
          </view>
          <view class="image-add" @click="chooseImage" v-if="images.length < 3">
            <text class="add-icon">+</text>
            <text class="add-text">添加照片</text>
          </view>
        </view>
      </view>
      
      <!-- 提交按钮 -->
      <button class="btn-primary submit-btn" @click="submitSnapshot" :disabled="!canSubmit">
        记录今日
      </button>
    </view>
    
    <!-- 历史快照 -->
    <view class="history-section">
      <view class="section-header">
        <text class="section-title">历史记录</text>
        <text class="section-more" @click="goToCalendar">查看日历</text>
      </view>
      
      <view class="snapshot-list" v-if="snapshots.length > 0">
        <view class="snapshot-card" v-for="(snapshot, index) in recentSnapshots" :key="snapshot.id">
          <view class="snapshot-header">
            <view class="snapshot-mood">
              <text class="mood-emoji">{{snapshot.mood.emoji}}</text>
              <text class="mood-text">{{snapshot.mood.label}}</text>
            </view>
            <text class="snapshot-date">{{formatDate(snapshot.date)}}</text>
          </view>
          <text class="snapshot-content">{{snapshot.content}}</text>
          <view class="snapshot-images" v-if="snapshot.images.length > 0">
            <image 
              v-for="(img, i) in snapshot.images" 
              :key="i"
              :src="img" 
              mode="aspectFill" 
              class="snapshot-image"
            />
          </view>
        </view>
      </view>
      
      <view class="empty-state" v-else>
        <text class="empty-icon">📸</text>
        <text class="empty-text">还没有记录</text>
        <text class="empty-desc">记录你的第一个美好瞬间吧</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      moods: [
        { emoji: '😊', label: '开心', color: '#ffa502' },
        { emoji: '😌', label: '平静', color: '#2ed573' },
        { emoji: '😔', label: '低落', color: '#70a1ff' },
        { emoji: '😤', label: '生气', color: '#e94560' },
        { emoji: '😴', label: '疲惫', color: '#a4b0be' },
        { emoji: '🤗', label: '感恩', color: '#ff6348' }
      ],
      selectedMood: null,
      snapshotContent: '',
      images: [],
      snapshots: []
    }
  },
  computed: {
    todayDate() {
      const date = new Date()
      const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      return `${date.getMonth() + 1}月${date.getDate()}日 ${weekDays[date.getDay()]}`
    },
    canSubmit() {
      return this.selectedMood && this.snapshotContent.trim()
    },
    recentSnapshots() {
      return this.snapshots.slice(-10).reverse()
    }
  },
  onShow() {
    this.loadSnapshots()
    this.checkTodaySnapshot()
  },
  methods: {
    loadSnapshots() {
      this.snapshots = uni.getStorageSync('snapshots') || []
    },
    checkTodaySnapshot() {
      const today = new Date().toDateString()
      const todaySnapshot = this.snapshots.find(s => new Date(s.date).toDateString() === today)
      if (todaySnapshot) {
        this.selectedMood = todaySnapshot.mood
        this.snapshotContent = todaySnapshot.content
        this.images = [...todaySnapshot.images]
      }
    },
    selectMood(mood) {
      this.selectedMood = mood
    },
    chooseImage() {
      uni.chooseImage({
        count: 3 - this.images.length,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.images = [...this.images, ...res.tempFilePaths]
        }
      })
    },
    removeImage(index) {
      this.images.splice(index, 1)
    },
    submitSnapshot() {
      if (!this.canSubmit) return
      
      const today = new Date().toDateString()
      const existingIndex = this.snapshots.findIndex(s => new Date(s.date).toDateString() === today)
      
      const snapshot = {
        id: Date.now().toString(),
        date: new Date().toISOString(),
        mood: this.selectedMood,
        content: this.snapshotContent,
        images: this.images
      }
      
      if (existingIndex > -1) {
        this.snapshots[existingIndex] = snapshot
      } else {
        this.snapshots.push(snapshot)
      }
      
      uni.setStorageSync('snapshots', this.snapshots)
      uni.showToast({ title: '记录成功', icon: 'success' })
      
      // 重置表单
      this.selectedMood = null
      this.snapshotContent = ''
      this.images = []
      this.loadSnapshots()
    },
    goToCalendar() {
      uni.navigateTo({ url: '/pages/snapshot/snapshot-calendar' })
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

.snapshot-input {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 30rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.input-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #eaeaea;
}

.input-date {
  font-size: 24rpx;
  color: #8b8b9a;
}

.mood-selector {
  margin-bottom: 20rpx;
}

.selector-label {
  font-size: 28rpx;
  color: #a0a0b0;
  display: block;
  margin-bottom: 16rpx;
}

.mood-options {
  display: flex;
  justify-content: space-between;
}

.mood-item {
  text-align: center;
  padding: 20rpx 16rpx;
  border-radius: 16rpx;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  transition: all 0.3s;
}

.mood-item:active {
  transform: scale(1.05);
}

.mood-selected {
  border-color: #e94560;
  background: rgba(233, 69, 96, 0.1);
}

.mood-emoji {
  font-size: 48rpx;
  display: block;
  margin-bottom: 8rpx;
}

.mood-label {
  font-size: 22rpx;
  color: #a0a0b0;
}

.mood-selected .mood-label {
  color: #e94560;
}

.snapshot-textarea {
  width: 100%;
  min-height: 200rpx;
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
  margin-bottom: 20rpx;
}

.image-section {
  margin-bottom: 20rpx;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.image-item {
  position: relative;
  width: 180rpx;
  height: 180rpx;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  border-radius: 12rpx;
}

.image-delete {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  width: 40rpx;
  height: 40rpx;
  background: #e94560;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 40rpx;
  font-size: 28rpx;
}

.image-add {
  width: 180rpx;
  height: 180rpx;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(255, 255, 255, 0.2);
}

.add-icon {
  font-size: 48rpx;
  color: #8b8b9a;
  margin-bottom: 8rpx;
}

.add-text {
  font-size: 24rpx;
  color: #8b8b9a;
}

.submit-btn {
  margin-top: 20rpx;
}

.history-section {
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

.snapshot-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.snapshot-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20rpx;
  padding: 24rpx;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.snapshot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.snapshot-mood {
  display: flex;
  align-items: center;
}

.snapshot-mood .mood-emoji {
  font-size: 40rpx;
  margin-right: 12rpx;
}

.mood-text {
  font-size: 28rpx;
  color: #eaeaea;
}

.snapshot-date {
  font-size: 24rpx;
  color: #6b6b7b;
}

.snapshot-content {
  font-size: 28rpx;
  color: #a0a0b0;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
}

.snapshot-images {
  display: flex;
  gap: 12rpx;
}

.snapshot-image {
  width: 160rpx;
  height: 160rpx;
  border-radius: 12rpx;
}
</style>
