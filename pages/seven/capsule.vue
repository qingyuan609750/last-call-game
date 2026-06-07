<template>
  <view class="container">
    <view class="capsule-header">
      <text class="capsule-title">💊 时光胶囊</text>
      <text class="capsule-desc">封存此刻，未来开启</text>
    </view>

    <!-- 创建胶囊 -->
    <view class="create-section" v-if="!showForm">
      <view class="create-card" @click="showForm = true">
        <text class="create-icon">+</text>
        <text class="create-text">创建新胶囊</text>
        <text class="create-desc">封存照片、语音、文字、位置</text>
      </view>
    </view>

    <!-- 胶囊表单 -->
    <view class="form-section" v-else>
      <view class="form-card">
        <text class="form-title">📝 胶囊内容</text>
        
        <!-- 文字 -->
        <textarea 
          class="form-textarea" 
          v-model="capsuleContent"
          placeholder="写下想对未来说的话..."
          maxlength="500"
        />
        
        <!-- 照片 -->
        <view class="photo-section">
          <text class="section-label">📷 照片</text>
          <view class="photo-list">
            <view class="photo-item" v-for="(img, index) in photos" :key="index">
              <image :src="img" mode="aspectFill" class="photo-image" />
              <view class="photo-delete" @click="removePhoto(index)">×</view>
            </view>
            <view class="photo-add" @click="choosePhoto" v-if="photos.length < 3">
              <text class="add-icon">+</text>
            </view>
          </view>
        </view>
        
        <!-- 位置 -->
        <view class="location-section">
          <text class="section-label">📍 位置</text>
          <view class="location-btn" @click="chooseLocation">
            <text class="location-icon">📍</text>
            <text class="location-text">{{location.name || '点击选择位置'}}</text>
          </view>
        </view>
        
        <!-- 开启时间 -->
        <view class="time-section">
          <text class="section-label">⏰ 开启时间</text>
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
            <view 
              class="time-option" 
              :class="{'time-active': selectedDays === 365}"
              @click="selectDays(365)"
            >
              <text class="time-number">1</text>
              <text class="time-unit">年后</text>
            </view>
          </view>
        </view>
        
        <!-- 按钮 -->
        <view class="form-buttons">
          <button class="btn-cancel" @click="showForm = false">取消</button>
          <button class="btn-submit" @click="submitCapsule">封存胶囊</button>
        </view>
      </view>
    </view>

    <!-- 胶囊列表 -->
    <view class="capsule-list" v-if="capsules.length > 0">
      <text class="section-title">我的胶囊</text>
      <view 
        class="capsule-item" 
        v-for="(capsule, index) in capsules" 
        :key="capsule.id"
        :class="{'capsule-openable': canOpen(capsule)}"
        @click="openCapsule(capsule)"
      >
        <view class="capsule-left">
          <text class="capsule-emoji">{{canOpen(capsule) ? '🔓' : '🔒'}}</text>
          <view class="capsule-info">
            <text class="capsule-date">{{formatDate(capsule.createDate)}}</text>
            <text class="capsule-status">{{canOpen(capsule) ? '可开启' : getCountdown(capsule)}}</text>
          </view>
        </view>
        <view class="capsule-preview">
          <text class="preview-text">{{capsule.content.substring(0, 30)}}...</text>
          <view class="preview-icons">
            <text v-if="capsule.photos.length > 0">📷</text>
            <text v-if="capsule.location.name">📍</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-section" v-if="capsules.length === 0 && !showForm">
      <text class="empty-icon">💊</text>
      <text class="empty-text">还没有时光胶囊</text>
      <text class="empty-desc">创建一个，封存此刻的美好</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      showForm: false,
      capsuleContent: '',
      photos: [],
      location: {},
      selectedDays: 7,
      capsules: []
    }
  },
  onShow() {
    this.loadCapsules()
  },
  methods: {
    loadCapsules() {
      this.capsules = uni.getStorageSync('capsules') || []
    },
    choosePhoto() {
      uni.chooseImage({
        count: 3 - this.photos.length,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.photos = [...this.photos, ...res.tempFilePaths]
        }
      })
    },
    removePhoto(index) {
      this.photos.splice(index, 1)
    },
    chooseLocation() {
      uni.chooseLocation({
        success: (res) => {
          this.location = {
            name: res.name,
            address: res.address,
            latitude: res.latitude,
            longitude: res.longitude
          }
        }
      })
    },
    selectDays(days) {
      this.selectedDays = days
    },
    submitCapsule() {
      if (!this.capsuleContent.trim() && this.photos.length === 0) {
        uni.showToast({ title: '请填写内容或添加照片', icon: 'none' })
        return
      }

      const openDate = new Date()
      openDate.setDate(openDate.getDate() + this.selectedDays)

      const capsule = {
        id: Date.now().toString(),
        content: this.capsuleContent,
        photos: this.photos,
        location: this.location,
        createDate: new Date().toISOString(),
        openDate: openDate.toISOString(),
        isOpened: false
      }

      this.capsules.push(capsule)
      uni.setStorageSync('capsules', this.capsules)

      // 重置表单
      this.capsuleContent = ''
      this.photos = []
      this.location = {}
      this.selectedDays = 7
      this.showForm = false

      uni.showToast({ title: '胶囊已封存', icon: 'success' })
    },
    canOpen(capsule) {
      return new Date(capsule.openDate).getTime() <= new Date().getTime()
    },
    getCountdown(capsule) {
      const diff = new Date(capsule.openDate).getTime() - new Date().getTime()
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      return `还有${days}天`
    },
    openCapsule(capsule) {
      if (!this.canOpen(capsule)) {
        uni.showToast({ title: '还未到开启时间', icon: 'none' })
        return
      }

      let content = capsule.content
      if (capsule.location.name) {
        content += `\n\n📍 ${capsule.location.name}`
      }

      uni.showModal({
        title: '时光胶囊',
        content: content,
        showCancel: false,
        success: () => {
          if (!capsule.isOpened) {
            capsule.isOpened = true
            uni.setStorageSync('capsules', this.capsules)
          }
        }
      })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return `${date.getMonth() + 1}月${date.getDate()}日`
    }
  }
}
</script>

<style scoped>
.container {
  padding: 30rpx;
  background: linear-gradient(180deg, #f8f9fc 0%, #eef2f7 100%);
  min-height: 100vh;
}

.capsule-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.capsule-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.capsule-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 创建卡片 */
.create-section {
  margin-bottom: 30rpx;
}

.create-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  padding: 60rpx;
  text-align: center;
  color: #fff;
  transition: all 0.3s;
}

.create-card:active {
  transform: scale(0.98);
}

.create-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 16rpx;
}

.create-text {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.create-desc {
  font-size: 24rpx;
  opacity: 0.8;
}

/* 表单 */
.form-section {
  margin-bottom: 30rpx;
}

.form-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.form-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.form-textarea {
  width: 100%;
  min-height: 200rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
  margin-bottom: 20rpx;
}

.photo-section, .location-section, .time-section {
  margin-bottom: 20rpx;
}

.section-label {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 12rpx;
}

.photo-list {
  display: flex;
  gap: 16rpx;
}

.photo-item {
  position: relative;
  width: 160rpx;
  height: 160rpx;
}

.photo-image {
  width: 100%;
  height: 100%;
  border-radius: 12rpx;
}

.photo-delete {
  position: absolute;
  top: -8rpx;
  right: -8rpx;
  width: 36rpx;
  height: 36rpx;
  background: #e53e3e;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 36rpx;
  font-size: 24rpx;
}

.photo-add {
  width: 160rpx;
  height: 160rpx;
  background: #f7fafc;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2rpx dashed #cbd5e0;
}

.add-icon {
  font-size: 48rpx;
  color: #a0aec0;
}

.location-btn {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
}

.location-icon {
  font-size: 32rpx;
  margin-right: 12rpx;
}

.location-text {
  font-size: 28rpx;
  color: #2d3748;
}

.time-options {
  display: flex;
  gap: 16rpx;
}

.time-option {
  flex: 1;
  text-align: center;
  padding: 20rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  border: 2rpx solid transparent;
}

.time-active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.time-number {
  font-size: 36rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
}

.time-unit {
  font-size: 22rpx;
  color: #a0aec0;
}

.form-buttons {
  display: flex;
  gap: 16rpx;
  margin-top: 30rpx;
}

.btn-cancel {
  flex: 1;
  background: #f7fafc;
  color: #718096;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

.btn-submit {
  flex: 2;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

/* 胶囊列表 */
.capsule-list {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20rpx;
  display: block;
}

.capsule-item {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.capsule-openable {
  border: 2rpx solid #48bb78;
}

.capsule-left {
  display: flex;
  align-items: center;
  margin-right: 20rpx;
}

.capsule-emoji {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.capsule-info {
  flex: 1;
}

.capsule-date {
  font-size: 26rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.capsule-status {
  font-size: 22rpx;
  color: #a0aec0;
}

.capsule-preview {
  text-align: right;
}

.preview-text {
  font-size: 24rpx;
  color: #718096;
  display: block;
  margin-bottom: 8rpx;
}

.preview-icons {
  display: flex;
  justify-content: flex-end;
  gap: 8rpx;
}

/* 空状态 */
.empty-section {
  text-align: center;
  padding: 100rpx 40rpx;
}

.empty-icon {
  font-size: 80rpx;
  display: block;
  margin-bottom: 20rpx;
}

.empty-text {
  font-size: 32rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: #a0aec0;
}
</style>
