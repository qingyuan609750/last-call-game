<template>
  <view class="custom-tabbar">
    <view class="tabbar-bg">
      <!-- 左侧按钮 -->
      <view 
        class="tab-item" 
        :class="{'tab-active': current === 0}"
        @click="switchTab(0, '/pages/index/index')"
      >
        <view class="tab-icon">
          <text class="icon-text">🏠</text>
        </view>
        <text class="tab-text">首页</text>
      </view>

      <view 
        class="tab-item" 
        :class="{'tab-active': current === 1}"
        @click="switchTab(1, '/pages/community/index')"
      >
        <view class="tab-icon">
          <text class="icon-text">🌈</text>
        </view>
        <text class="tab-text">社区</text>
      </view>

      <!-- 中间凸起按钮 -->
      <view class="tab-center" @click="showMenu">
        <view class="center-btn">
          <text class="center-icon">✨</text>
        </view>
        <text class="center-text">功能</text>
      </view>

      <!-- 右侧按钮 -->
      <view 
        class="tab-item" 
        :class="{'tab-active': current === 2}"
        @click="switchTab(2, '/pages/wheel/index')"
      >
        <view class="tab-icon">
          <text class="icon-text">🎰</text>
        </view>
        <text class="tab-text">发现</text>
      </view>

      <view 
        class="tab-item" 
        :class="{'tab-active': current === 3}"
        @click="switchTab(3, '/pages/profile/profile')"
      >
        <view class="tab-icon">
          <text class="icon-text">👤</text>
        </view>
        <text class="tab-text">我的</text>
      </view>
    </view>

    <!-- 功能菜单弹窗 -->
    <view class="menu-modal" v-if="showMenuModal">
      <view class="menu-mask" @click="showMenuModal = false"></view>
      <view class="menu-content">
        <view class="menu-grid">
          <view class="menu-item" @click="goToPage('/pages/seven/index')">
            <view class="menu-icon bg-purple">🎯</view>
            <text class="menu-text">七日之后</text>
          </view>
          <view class="menu-item" @click="goToPage('/pages/wheel/index')">
            <view class="menu-icon bg-blue">🎰</view>
            <text class="menu-text">命运转盘</text>
          </view>
          <view class="menu-item" @click="goToPage('/pages/weather/index')">
            <view class="menu-icon bg-pink">🌤️</view>
            <text class="menu-text">情绪气象</text>
          </view>
          <view class="menu-item" @click="goToPage('/pages/shop/index')">
            <view class="menu-icon bg-teal">🛒</view>
            <text class="menu-text">未来商店</text>
          </view>
          <view class="menu-item" @click="goToPage('/pages/parallel/index')">
            <view class="menu-icon bg-orange">🌍</view>
            <text class="menu-text">平行人生</text>
          </view>
          <view class="menu-item" @click="goToPage('/pages/community/index')">
            <view class="menu-icon bg-purple">🌈</view>
            <text class="menu-text">时光社区</text>
          </view>
        </view>
        <view class="menu-close" @click="showMenuModal = false">
          <text class="close-icon">✕</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  props: {
    current: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      showMenuModal: false
    }
  },
  methods: {
    switchTab(index, url) {
      uni.switchTab({ url })
    },
    showMenu() {
      this.showMenuModal = true
    },
    goToPage(url) {
      this.showMenuModal = false
      uni.navigateTo({ url })
    }
  }
}
</script>

<style scoped>
.custom-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
}

.tabbar-bg {
  background: #ffffff;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10rpx 0 30rpx;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.08);
  border-radius: 30rpx 30rpx 0 0;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  padding: 10rpx 0;
  transition: all 0.3s;
}

.tab-icon {
  width: 56rpx;
  height: 56rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6rpx;
  transition: all 0.3s;
}

.icon-text {
  font-size: 40rpx;
}

.tab-text {
  font-size: 22rpx;
  color: #a0aec0;
  transition: all 0.3s;
}

.tab-active .tab-icon {
  transform: scale(1.1);
}

.tab-active .tab-text {
  color: #667eea;
  font-weight: bold;
}

/* 中间凸起按钮 */
.tab-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: -40rpx;
  position: relative;
}

.center-btn {
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 30rpx rgba(102, 126, 234, 0.4);
  border: 6rpx solid #ffffff;
  transition: all 0.3s;
}

.center-btn:active {
  transform: scale(0.95);
}

.center-icon {
  font-size: 48rpx;
}

.center-text {
  font-size: 22rpx;
  color: #667eea;
  margin-top: 8rpx;
  font-weight: bold;
}

/* 菜单弹窗 */
.menu-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: flex-end;
}

.menu-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.menu-content {
  background: #ffffff;
  border-radius: 40rpx 40rpx 0 0;
  padding: 40rpx;
  width: 100%;
  position: relative;
  z-index: 1001;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.menu-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 30rpx;
  margin-bottom: 40rpx;
}

.menu-item {
  width: calc(33.33% - 20rpx);
  text-align: center;
  padding: 30rpx 0;
  transition: all 0.3s;
}

.menu-item:active {
  transform: scale(0.95);
}

.menu-icon {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16rpx;
  font-size: 48rpx;
}

.bg-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.bg-blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.bg-pink {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.bg-teal {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.bg-orange {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.menu-text {
  font-size: 26rpx;
  color: #2d3748;
}

.menu-close {
  text-align: center;
  padding: 20rpx;
}

.close-icon {
  font-size: 40rpx;
  color: #a0aec0;
  padding: 20rpx;
}
</style>
