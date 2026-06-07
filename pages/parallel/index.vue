<template>
  <view class="container">
    <view class="parallel-header">
      <text class="parallel-title">🌍 平行人生</text>
      <text class="parallel-desc">探索另一种可能的人生轨迹</text>
    </view>

    <!-- 当前人生 -->
    <view class="current-life">
      <view class="life-card">
        <text class="life-label">当前人生</text>
        <view class="life-stats">
          <view class="stat-item">
            <text class="stat-icon">📚</text>
            <text class="stat-name">学习</text>
            <view class="stat-bar">
              <view class="stat-fill" style="width: 60%; background: #667eea;"></view>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-icon">💼</text>
            <text class="stat-name">事业</text>
            <view class="stat-bar">
              <view class="stat-fill" style="width: 45%; background: #f093fb;"></view>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-icon">❤️</text>
            <text class="stat-name">感情</text>
            <view class="stat-bar">
              <view class="stat-fill" style="width: 70%; background: #fa709a;"></view>
            </view>
          </view>
          <view class="stat-item">
            <text class="stat-icon">💰</text>
            <text class="stat-name">财富</text>
            <view class="stat-bar">
              <view class="stat-fill" style="width: 35%; background: #48bb78;"></view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 选择分支 -->
    <view class="branch-section">
      <text class="section-title">如果当初...</text>
      <view class="branch-list">
        <view 
          class="branch-card" 
          v-for="(branch, index) in branches" 
          :key="index"
          @click="exploreBranch(branch)"
        >
          <view class="branch-icon">{{branch.emoji}}</view>
          <view class="branch-info">
            <text class="branch-title">{{branch.title}}</text>
            <text class="branch-desc">{{branch.desc}}</text>
          </view>
          <text class="branch-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 平行人生结果 -->
    <view class="result-section" v-if="showResult">
      <view class="result-card">
        <text class="result-title">{{resultBranch.title}}</text>
        <text class="result-story">{{resultStory}}</text>
        
        <view class="parallel-stats">
          <view class="p-stat-item" v-for="(stat, index) in resultStats" :key="index">
            <text class="p-stat-icon">{{stat.icon}}</text>
            <text class="p-stat-name">{{stat.name}}</text>
            <view class="p-stat-bar">
              <view class="p-stat-fill" :style="{width: stat.value + '%', background: stat.color}"></view>
            </view>
            <text class="p-stat-value">{{stat.value}}%</text>
          </view>
        </view>
        
        <view class="result-quote">
          <text class="quote-mark">"</text>
          <text class="quote-text">{{resultQuote}}</text>
        </view>
      </view>
    </view>

    <!-- 人生格言 -->
    <view class="motto-section">
      <view class="motto-card">
        <text class="motto-text">{{currentMotto}}</text>
        <text class="motto-refresh" @click="refreshMotto">换一句</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      showResult: false,
      resultBranch: {},
      resultStory: '',
      resultStats: [],
      resultQuote: '',
      branches: [
        {
          emoji: '🎓',
          title: '如果当初选择了考研',
          desc: '继续深造的学术人生',
          stories: [
            '你选择了考研，经过两年的努力，成功考上了理想的学校。在研究生期间，你发表了多篇论文，最终成为了一名大学老师。',
            '你选择了考研，虽然第一次失败了，但你没有放弃。第二次你成功了，并且在研究生期间遇到了志同道合的伙伴，一起创业成功。'
          ],
          stats: [
            { icon: '📚', name: '学习', value: 95, color: '#667eea' },
            { icon: '💼', name: '事业', value: 70, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 50, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 60, color: '#48bb78' }
          ],
          quotes: '知识改变命运，但选择决定方向'
        },
        {
          emoji: '✈️',
          title: '如果当初选择了出国',
          desc: '在异国他乡的冒险人生',
          stories: [
            '你选择了出国留学，在异国他乡经历了文化冲击，但也开阔了眼界。你学会了三门外语，成为了一名国际商务人士。',
            '你选择了出国打工，从底层做起，经历了无数困难。十年后，你有了自己的餐厅，成为了当地小有名气的华人企业家。'
          ],
          stats: [
            { icon: '📚', name: '学习', value: 80, color: '#667eea' },
            { icon: '💼', name: '事业', value: 75, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 40, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 85, color: '#48bb78' }
          ],
          quotes: '世界那么大，勇敢去看看'
        },
        {
          emoji: '💼',
          title: '如果当初选择了创业',
          desc: '充满挑战的创业人生',
          stories: [
            '你选择了创业，经历了三次失败，第四次终于成功。你的公司从3人发展到300人，成为了行业新星。',
            '你选择了创业，虽然公司没有做大，但你积累了宝贵的经验。后来你成为了一名投资人，帮助更多创业者实现梦想。'
          ],
          stats: [
            { icon: '📚', name: '学习', value: 70, color: '#667eea' },
            { icon: '💼', name: '事业', value: 90, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 45, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 80, color: '#48bb78' }
          ],
          quotes: '失败是成功之母，坚持就是胜利'
        },
        {
          emoji: '🎨',
          title: '如果当初选择了艺术',
          desc: '追逐梦想的文艺人生',
          stories: [
            '你选择了艺术道路，虽然一开始很艰难，但你的作品逐渐被认可。十年后，你举办了个人画展，成为了知名艺术家。',
            '你选择了音乐，在酒吧驻唱多年。一次偶然的机会，你的原创歌曲被知名歌手翻唱，你终于走上了音乐之路。'
          ],
          stats: [
            { icon: '📚', name: '学习', value: 75, color: '#667eea' },
            { icon: '💼', name: '事业', value: 60, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 80, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 50, color: '#48bb78' }
          ],
          quotes: '追随内心，做真实的自己'
        },
        {
          emoji: '🏠',
          title: '如果当初选择了安稳',
          desc: '平淡幸福的生活人生',
          stories: [
            '你选择了安稳的生活，考上了公务员。虽然收入不高，但工作稳定，有时间陪伴家人，过着平淡而幸福的日子。',
            '你选择了回老家，接手了父母的生意。虽然没有大富大贵，但一家人其乐融融，生活安稳幸福。'
          ],
          stats: [
            { icon: '📚', name: '学习', value: 50, color: '#667eea' },
            { icon: '💼', name: '事业', value: 55, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 95, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 65, color: '#48bb78' }
          ],
          quotes: '平平淡淡才是真，知足常乐'
        }
      ],
      mottos: [
        '人生没有对错，只有选择',
        '每一种人生都有它的精彩',
        '活在当下，珍惜眼前',
        '过去无法改变，未来掌握在自己手中',
        '平行人生的意义，是让我们更珍惜现在'
      ],
      currentMotto: ''
    }
  },
  onShow() {
    this.refreshMotto()
  },
  methods: {
    exploreBranch(branch) {
      this.resultBranch = branch
      this.resultStory = branch.stories[Math.floor(Math.random() * branch.stories.length)]
      this.resultStats = branch.stats
      this.resultQuote = branch.quotes
      this.showResult = true
      
      // 滚动到结果区域
      setTimeout(() => {
        uni.createSelectorQuery().select('.result-section').boundingClientRect(rect => {
          if (rect) {
            uni.pageScrollTo({ scrollTop: rect.top, duration: 300 })
          }
        }).exec()
      }, 100)
    },
    refreshMotto() {
      this.currentMotto = this.mottos[Math.floor(Math.random() * this.mottos.length)]
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

.parallel-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.parallel-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.parallel-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 当前人生 */
.current-life {
  margin-bottom: 30rpx;
}

.life-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  padding: 30rpx;
  color: #fff;
}

.life-label {
  font-size: 28rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 20rpx;
}

.life-stats {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 32rpx;
  margin-right: 12rpx;
  width: 50rpx;
}

.stat-name {
  font-size: 26rpx;
  width: 80rpx;
  margin-right: 16rpx;
}

.stat-bar {
  flex: 1;
  height: 12rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6rpx;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 6rpx;
  transition: width 1s ease;
}

/* 分支选择 */
.branch-section {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20rpx;
  display: block;
}

.branch-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.branch-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

.branch-card:active {
  transform: scale(0.98);
  background: #f7fafc;
}

.branch-icon {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.branch-info {
  flex: 1;
}

.branch-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.branch-desc {
  font-size: 24rpx;
  color: #a0aec0;
}

.branch-arrow {
  font-size: 36rpx;
  color: #a0aec0;
}

/* 结果展示 */
.result-section {
  margin-bottom: 30rpx;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.result-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.result-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 16rpx;
  text-align: center;
}

.result-story {
  font-size: 28rpx;
  color: #4a5568;
  line-height: 1.8;
  display: block;
  margin-bottom: 30rpx;
}

.parallel-stats {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 30rpx;
}

.p-stat-item {
  display: flex;
  align-items: center;
}

.p-stat-icon {
  font-size: 32rpx;
  margin-right: 12rpx;
  width: 50rpx;
}

.p-stat-name {
  font-size: 26rpx;
  color: #2d3748;
  width: 80rpx;
  margin-right: 16rpx;
}

.p-stat-bar {
  flex: 1;
  height: 16rpx;
  background: #edf2f7;
  border-radius: 8rpx;
  overflow: hidden;
  margin-right: 16rpx;
}

.p-stat-fill {
  height: 100%;
  border-radius: 8rpx;
  transition: width 1s ease;
}

.p-stat-value {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
  width: 60rpx;
  text-align: right;
}

.result-quote {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 16rpx;
  padding: 24rpx;
  text-align: center;
}

.quote-mark {
  font-size: 40rpx;
  color: rgba(255, 255, 255, 0.5);
  display: block;
  margin-bottom: 4rpx;
}

.quote-text {
  font-size: 28rpx;
  color: #fff;
  font-style: italic;
}

/* 格言 */
.motto-section {
  margin-bottom: 30rpx;
}

.motto-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
}

.motto-text {
  font-size: 30rpx;
  color: #fff;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
}

.motto-refresh {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: underline;
}
</style>
