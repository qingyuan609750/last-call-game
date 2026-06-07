<template>
  <view class="container">
    <custom-tabbar :current="0"></custom-tabbar>
    <!-- 顶部欢迎区域 -->
    <view class="welcome-section">
      <view class="welcome-bg">
        <view class="welcome-content">
          <text class="welcome-greeting">{{greeting}}</text>
          <text class="welcome-name">时光旅人</text>
          <text class="welcome-desc">每一天都是新的冒险</text>
        </view>
        <view class="welcome-decoration">
          <text class="deco-icon">✨</text>
        </view>
      </view>
    </view>

    <!-- 每日运势卡片 -->
    <view class="fortune-card" @click="goToFortune">
      <view class="fortune-left">
        <text class="fortune-title">今日运势</text>
        <text class="fortune-desc">{{dailyFortune}}</text>
        <view class="fortune-tags">
          <text class="fortune-tag" v-for="(tag, index) in fortuneTags" :key="index">{{tag}}</text>
        </view>
      </view>
      <view class="fortune-right">
        <text class="fortune-emoji">{{fortuneEmoji}}</text>
        <text class="fortune-lucky">幸运指数 {{luckyIndex}}</text>
      </view>
    </view>

    <!-- 功能网格 -->
    <view class="features-section">
      <text class="section-title">探索功能</text>
      <view class="features-grid">
        <!-- 七日之后 -->
        <view class="feature-card feature-primary" @click="goToSevenDays">
          <view class="feature-icon-bg">
            <text class="feature-icon">🎯</text>
          </view>
          <text class="feature-name">七日之后</text>
          <text class="feature-desc">给未来的自己</text>
        </view>

        <!-- 命运转盘 -->
        <view class="feature-card feature-tertiary" @click="goToWheel">
          <view class="feature-icon-bg">
            <text class="feature-icon">🎰</text>
          </view>
          <text class="feature-name">命运转盘</text>
          <text class="feature-desc">今日小挑战</text>
        </view>

        <!-- 情绪气象站 -->
        <view class="feature-card feature-quinary" @click="goToWeather">
          <view class="feature-icon-bg">
            <text class="feature-icon">🌤️</text>
          </view>
          <text class="feature-name">情绪气象</text>
          <text class="feature-desc">心情天气图</text>
        </view>

        <!-- 未来商店 -->
        <view class="feature-card feature-senary" @click="goToShop">
          <view class="feature-icon-bg">
            <text class="feature-icon">🛒</text>
          </view>
          <text class="feature-name">未来商店</text>
          <text class="feature-desc">兑换愿望清单</text>
        </view>

        <!-- 平行人生 -->
        <view class="feature-card feature-octonary" @click="goToParallel">
          <view class="feature-icon-bg">
            <text class="feature-icon">🌍</text>
          </view>
          <text class="feature-name">平行人生</text>
          <text class="feature-desc">另一种可能</text>
        </view>

        <!-- 时光社区 -->
        <view class="feature-card feature-community" @click="goToCommunity">
          <view class="feature-icon-bg">
            <text class="feature-icon">🌈</text>
          </view>
          <text class="feature-name">时光社区</text>
          <text class="feature-desc">匿名分享交流</text>
        </view>
      </view>
    </view>

    <!-- 底部留白 -->
    <view class="bottom-space"></view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      greeting: '',
      dailyFortune: '',
      fortuneTags: [],
      fortuneEmoji: '🌟',
      luckyIndex: 88
    }
  },
  onShow() {
    this.setGreeting()
    this.generateFortune()
  },
  methods: {
    setGreeting() {
      const hour = new Date().getHours()
      if (hour < 6) this.greeting = '夜深了'
      else if (hour < 9) this.greeting = '早上好'
      else if (hour < 12) this.greeting = '上午好'
      else if (hour < 14) this.greeting = '中午好'
      else if (hour < 18) this.greeting = '下午好'
      else this.greeting = '晚上好'
    },
    generateFortune() {
      const fortunes = [
        { text: '今日适合开启新挑战', tags: ['挑战', '机遇'], emoji: '🔥' },
        { text: '桃花运旺盛，多交朋友', tags: ['桃花', '社交'], emoji: '🌸' },
        { text: '财运亨通，适合记账', tags: ['财运', '理财'], emoji: '💎' },
        { text: '灵感迸发，记录想法', tags: ['灵感', '创作'], emoji: '💡' },
        { text: '适合反思，写信给未来', tags: ['反思', '成长'], emoji: '📖' },
        { text: '好运连连，勇敢尝试', tags: ['幸运', '冒险'], emoji: '🌈' }
      ]
      const fortune = fortunes[Math.floor(Math.random() * fortunes.length)]
      this.dailyFortune = fortune.text
      this.fortuneTags = fortune.tags
      this.fortuneEmoji = fortune.emoji
      this.luckyIndex = Math.floor(Math.random() * 30) + 70
    },
    goToSevenDays() {
      uni.navigateTo({ url: '/pages/seven/index' })
    },
    goToWheel() {
      uni.switchTab({ url: '/pages/wheel/index' })
    },
    goToWeather() {
      uni.navigateTo({ url: '/pages/weather/index' })
    },
    goToShop() {
      uni.navigateTo({ url: '/pages/shop/index' })
    },
    goToParallel() {
      uni.navigateTo({ url: '/pages/parallel/index' })
    },
    goToCommunity() {
      uni.switchTab({ url: '/pages/community/index' })
    },
    goToFortune() {
      this.generateFortune()
      uni.showToast({ title: '运势已刷新', icon: 'none' })
    }
  }
}
</script>

<style scoped>
.container {
  padding: 0;
  background: linear-gradient(180deg, #f8f9fc 0%, #eef2f7 100%);
  min-height: 100vh;
}

/* 欢迎区域 */
.welcome-section {
  padding: 30rpx 30rpx 20rpx;
}

.welcome-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 30rpx;
  padding: 40rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.welcome-bg::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300rpx;
  height: 300rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.welcome-content {
  flex: 1;
}

.welcome-greeting {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  display: block;
  margin-bottom: 8rpx;
}

.welcome-name {
  font-size: 44rpx;
  font-weight: bold;
  color: #fff;
  display: block;
  margin-bottom: 8rpx;
}

.welcome-desc {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.7);
}

.welcome-decoration {
  position: relative;
  z-index: 1;
}

.deco-icon {
  font-size: 80rpx;
  opacity: 0.9;
}

/* 运势卡片 */
.fortune-card {
  margin: 0 30rpx 30rpx;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 24rpx;
  padding: 30rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.fortune-card::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 200rpx;
  height: 200rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.fortune-left {
  flex: 1;
  position: relative;
  z-index: 1;
}

.fortune-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #fff;
  display: block;
  margin-bottom: 12rpx;
}

.fortune-desc {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
  display: block;
  margin-bottom: 16rpx;
}

.fortune-tags {
  display: flex;
  gap: 12rpx;
}

.fortune-tag {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  font-size: 22rpx;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.fortune-right {
  text-align: center;
  position: relative;
  z-index: 1;
}

.fortune-emoji {
  font-size: 60rpx;
  display: block;
  margin-bottom: 8rpx;
}

.fortune-lucky {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.9);
}

/* 功能区域 */
.features-section {
  padding: 0 30rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 24rpx;
  display: block;
}

.features-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.feature-card {
  width: calc(50% - 10rpx);
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  text-align: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
  border: 2rpx solid transparent;
}

.feature-card:active {
  transform: scale(0.96);
  box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.1);
}

.feature-primary {
  border-color: rgba(102, 126, 234, 0.3);
}

.feature-secondary {
  border-color: rgba(240, 147, 251, 0.3);
}

.feature-tertiary {
  border-color: rgba(79, 172, 254, 0.3);
}

.feature-quaternary {
  border-color: rgba(67, 233, 123, 0.3);
}

.feature-quinary {
  border-color: rgba(250, 112, 154, 0.3);
}

.feature-senary {
  border-color: rgba(48, 207, 208, 0.3);
}

.feature-septenary {
  border-color: rgba(168, 237, 234, 0.3);
}

.feature-octonary {
  border-color: rgba(255, 154, 158, 0.3);
}

.feature-icon-bg {
  width: 100rpx;
  height: 100rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16rpx;
}

.feature-primary .feature-icon-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-secondary .feature-icon-bg {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.feature-tertiary .feature-icon-bg {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.feature-quaternary .feature-icon-bg {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-quinary .feature-icon-bg {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.feature-senary .feature-icon-bg {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.feature-septenary .feature-icon-bg {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.feature-octonary .feature-icon-bg {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.feature-community .feature-icon-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-icon {
  font-size: 48rpx;
}

.feature-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 6rpx;
}

.feature-desc {
  font-size: 22rpx;
  color: #a0aec0;
}

.bottom-space {
  height: 160rpx;
}
</style>
