<template>
  <view class="container">
    <view class="parallel-header">
      <text class="parallel-title">🌍 平行人生</text>
      <text class="parallel-desc">探索另一种可能的人生轨迹</text>
    </view>

    <!-- 当前人生状态 -->
    <view class="current-life">
      <view class="life-card">
        <view class="life-header">
          <text class="life-label">当前人生</text>
          <text class="life-age">{{userAge}}岁</text>
        </view>
        <view class="life-stats">
          <view class="stat-item" v-for="(stat, index) in currentStats" :key="index">
            <text class="stat-icon">{{stat.icon}}</text>
            <view class="stat-info">
              <text class="stat-name">{{stat.name}}</text>
              <view class="stat-bar">
                <view class="stat-fill" :style="{width: stat.value + '%', background: stat.color}"></view>
              </view>
            </view>
            <text class="stat-value">{{stat.value}}</text>
          </view>
        </view>
        <view class="life-tags">
          <text class="life-tag" v-for="(tag, index) in lifeTags" :key="index">{{tag}}</text>
        </view>
      </view>
    </view>

    <!-- 人生时间线 -->
    <view class="timeline-section" v-if="timelineEvents.length > 0">
      <text class="section-title">人生关键节点</text>
      <view class="timeline">
        <view class="timeline-item" v-for="(event, index) in timelineEvents" :key="index">
          <view class="timeline-dot" :class="{'timeline-dot-active': event.isKey}"></view>
          <view class="timeline-content">
            <text class="timeline-age">{{event.age}}岁</text>
            <text class="timeline-text">{{event.text}}</text>
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
            <view class="branch-tags">
              <text class="branch-tag" v-for="(tag, i) in branch.tags" :key="i">{{tag}}</text>
            </view>
          </view>
          <text class="branch-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 平行人生结果 -->
    <view class="result-section" v-if="showResult">
      <view class="result-card">
        <view class="result-header">
          <text class="result-emoji">{{resultBranch.emoji}}</text>
          <text class="result-title">{{resultBranch.title}}</text>
        </view>
        
        <view class="result-timeline">
          <view class="rt-item" v-for="(stage, index) in resultTimeline" :key="index">
            <view class="rt-age">{{stage.age}}岁</view>
            <view class="rt-dot"></view>
            <view class="rt-content">
              <text class="rt-title">{{stage.title}}</text>
              <text class="rt-desc">{{stage.desc}}</text>
            </view>
          </view>
        </view>

        <text class="result-story">{{resultStory}}</text>
        
        <view class="parallel-stats">
          <view class="p-stat-item" v-for="(stat, index) in resultStats" :key="index">
            <text class="p-stat-icon">{{stat.icon}}</text>
            <text class="p-stat-name">{{stat.name}}</text>
            <view class="p-stat-bar">
              <view class="p-stat-fill" :style="{width: stat.value + '%', background: stat.color}"></view>
            </view>
            <text class="p-stat-value">{{stat.value}}</text>
          </view>
        </view>

        <view class="result-achievements">
          <text class="achievements-title">可能获得的成就</text>
          <view class="achievements-list">
            <view class="achievement-item" v-for="(ach, index) in resultAchievements" :key="index">
              <text class="achievement-icon">{{ach.icon}}</text>
              <text class="achievement-text">{{ach.text}}</text>
            </view>
          </view>
        </view>
        
        <view class="result-quote">
          <text class="quote-mark">"</text>
          <text class="quote-text">{{resultQuote}}</text>
        </view>

        <view class="result-actions">
          <button class="result-btn btn-primary" @click="saveParallelLife">收藏这个人生</button>
          <button class="result-btn btn-secondary" @click="tryAnother">试试另一个</button>
        </view>
      </view>
    </view>

    <!-- 收藏的人生 -->
    <view class="saved-section" v-if="savedLives.length > 0">
      <text class="section-title">我收藏的人生</text>
      <view class="saved-list">
        <view class="saved-card" v-for="(life, index) in savedLives" :key="index" @click="viewSavedLife(life)">
          <text class="saved-emoji">{{life.emoji}}</text>
          <view class="saved-info">
            <text class="saved-title">{{life.title}}</text>
            <text class="saved-date">{{life.date}}</text>
          </view>
          <text class="saved-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 人生格言 -->
    <view class="motto-section">
      <view class="motto-card">
        <text class="motto-icon">💫</text>
        <text class="motto-text">{{currentMotto}}</text>
        <view class="motto-refresh" @click="refreshMotto">
          <text class="refresh-icon">🔄</text>
          <text class="refresh-text">换一句</text>
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
      userAge: 25,
      currentStats: [
        { icon: '📚', name: '学识', value: 65, color: '#667eea' },
        { icon: '💼', name: '事业', value: 50, color: '#f093fb' },
        { icon: '❤️', name: '感情', value: 70, color: '#fa709a' },
        { icon: '💰', name: '财富', value: 40, color: '#48bb78' },
        { icon: '🏃', name: '健康', value: 75, color: '#4facfe' }
      ],
      lifeTags: ['正在奋斗', '充满希望', '探索中'],
      timelineEvents: [
        { age: 18, text: '高中毕业，面临人生选择', isKey: true },
        { age: 22, text: '大学毕业，进入社会', isKey: true },
        { age: 25, text: '现在的你，站在十字路口', isKey: true }
      ],
      showResult: false,
      resultBranch: {},
      resultStory: '',
      resultStats: [],
      resultQuote: '',
      resultTimeline: [],
      resultAchievements: [],
      savedLives: [],
      branches: [
        {
          emoji: '🎓',
          title: '如果当初选择了考研',
          desc: '继续深造的学术人生',
          tags: ['学术', '稳定', '知识'],
          timeline: [
            { age: 22, title: '决定考研', desc: '放弃了工作机会，全身心投入备考' },
            { age: 23, title: '考研成功', desc: '考上了理想的学校，师从知名教授' },
            { age: 25, title: '研究生在读', desc: '发表了第一篇论文，获得奖学金' },
            { age: 28, title: '博士录取', desc: '继续深造，研究方向获得认可' },
            { age: 32, title: '留校任教', desc: '成为大学讲师，开始教学生涯' }
          ],
          stories: [
            '你选择了考研，经过两年的努力，成功考上了理想的学校。在研究生期间，你发表了多篇论文，最终成为了一名大学老师。虽然收入不高，但生活充实而有意义。',
            '你选择了考研，虽然第一次失败了，但你没有放弃。第二次你成功了，并且在研究生期间遇到了志同道合的伙伴，一起创业成功，将学术成果转化为商业价值。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 95, color: '#667eea' },
            { icon: '💼', name: '事业', value: 70, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 50, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 60, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 65, color: '#4facfe' }
          ],
          achievements: [
            { icon: '📖', text: '发表SCI论文3篇' },
            { icon: '🏆', text: '获得国家奖学金' },
            { icon: '👨‍🏫', text: '成为大学讲师' }
          ],
          quotes: '知识改变命运，但选择决定方向。在学术的道路上，你找到了内心的平静。'
        },
        {
          emoji: '✈️',
          title: '如果当初选择了出国',
          desc: '在异国他乡的冒险人生',
          tags: ['冒险', '视野', '挑战'],
          timeline: [
            { age: 22, title: '决定出国', desc: '辞掉工作，准备语言考试和申请材料' },
            { age: 23, title: '踏上异国', desc: '来到陌生的国度，开始留学生涯' },
            { age: 25, title: '适应生活', desc: '克服了文化冲击，交到各国朋友' },
            { age: 28, title: '毕业工作', desc: '进入跨国公司，开始国际职业生涯' },
            { age: 32, title: '事业起飞', desc: '成为区域经理，年薪百万' }
          ],
          stories: [
            '你选择了出国留学，在异国他乡经历了文化冲击，但也开阔了眼界。你学会了三门外语，成为了一名国际商务人士，足迹遍布全球。',
            '你选择了出国打工，从底层做起，经历了无数困难。十年后，你有了自己的餐厅，成为了当地小有名气的华人企业家，还帮助了很多新来的留学生。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 80, color: '#667eea' },
            { icon: '💼', name: '事业', value: 85, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 40, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 90, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 70, color: '#4facfe' }
          ],
          achievements: [
            { icon: '🌐', text: '掌握三国语言' },
            { icon: '✈️', text: '足迹遍布20个国家' },
            { icon: '💼', text: '跨国公司高管' }
          ],
          quotes: '世界那么大，勇敢去看看。在异国他乡，你找到了不一样的自己。'
        },
        {
          emoji: '💼',
          title: '如果当初选择了创业',
          desc: '充满挑战的创业人生',
          tags: ['冒险', '财富', '自由'],
          timeline: [
            { age: 22, title: '辞职创业', desc: '带着积蓄和梦想，开始了创业之路' },
            { age: 23, title: '第一次失败', desc: '资金链断裂，团队解散，负债累累' },
            { age: 25, title: '重新出发', desc: '总结经验，开始第二个项目' },
            { age: 28, title: '获得投资', desc: '项目获得A轮融资，团队扩张到50人' },
            { age: 32, title: '公司上市', desc: '成功IPO，成为行业独角兽' }
          ],
          stories: [
            '你选择了创业，经历了三次失败，第四次终于成功。你的公司从3人发展到300人，成为了行业新星。虽然过程艰辛，但你从未后悔。',
            '你选择了创业，虽然公司没有做大，但你积累了宝贵的经验。后来你成为了一名投资人，帮助更多创业者实现梦想，找到了新的人生价值。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 75, color: '#667eea' },
            { icon: '💼', name: '事业', value: 95, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 45, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 95, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 55, color: '#4facfe' }
          ],
          achievements: [
            { icon: '🚀', text: '公司成功上市' },
            { icon: '💰', text: '身家过亿' },
            { icon: '🏅', text: '年度青年企业家' }
          ],
          quotes: '失败是成功之母，坚持就是胜利。在创业的路上，你学会了永不言弃。'
        },
        {
          emoji: '🎨',
          title: '如果当初选择了艺术',
          desc: '追逐梦想的文艺人生',
          tags: ['梦想', '自由', '创造'],
          timeline: [
            { age: 22, title: '追求艺术', desc: '不顾家人反对，进入艺术学院深造' },
            { age: 23, title: '生活窘迫', desc: '作品无人问津，靠兼职维持生计' },
            { age: 25, title: '初露锋芒', desc: '作品被画廊选中，开始有人关注' },
            { age: 28, title: '举办个展', desc: '第一次个人画展，作品开始被收藏' },
            { age: 32, title: '成名成家', desc: '成为知名艺术家，作品价值连城' }
          ],
          stories: [
            '你选择了艺术道路，虽然一开始很艰难，但你的作品逐渐被认可。十年后，你举办了个人画展，成为了知名艺术家，用画笔记录了时代的变迁。',
            '你选择了音乐，在酒吧驻唱多年。一次偶然的机会，你的原创歌曲被知名歌手翻唱，你终于走上了音乐之路，发行了属于自己的专辑。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 70, color: '#667eea' },
            { icon: '💼', name: '事业', value: 75, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 85, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 70, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 80, color: '#4facfe' }
          ],
          achievements: [
            { icon: '🎨', text: '举办个人画展' },
            { icon: '🏆', text: '获得艺术大奖' },
            { icon: '🌍', text: '作品被博物馆收藏' }
          ],
          quotes: '追随内心，做真实的自己。在艺术的世界里，你找到了灵魂的归宿。'
        },
        {
          emoji: '🏠',
          title: '如果当初选择了安稳',
          desc: '平淡幸福的生活人生',
          tags: ['家庭', '稳定', '幸福'],
          timeline: [
            { age: 22, title: '考上公务员', desc: '经过努力，成功进入体制内工作' },
            { age: 24, title: '遇见爱情', desc: '通过相亲认识了现在的伴侣' },
            { age: 26, title: '组建家庭', desc: '结婚买房，开始了二人世界' },
            { age: 28, title: '迎接新生命', desc: '孩子出生，生活更加充实' },
            { age: 32, title: '生活美满', desc: '工作稳定，家庭和睦，岁月静好' }
          ],
          stories: [
            '你选择了安稳的生活，考上了公务员。虽然收入不高，但工作稳定，有时间陪伴家人。周末带孩子去公园，假期全家出游，过着平淡而幸福的日子。',
            '你选择了回老家，接手了父母的生意。虽然没有大富大贵，但一家人其乐融融。你改良了祖传手艺，生意越来越好，还带动了村里的就业。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 55, color: '#667eea' },
            { icon: '💼', name: '事业', value: 60, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 98, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 65, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 85, color: '#4facfe' }
          ],
          achievements: [
            { icon: '💑', text: '组建幸福家庭' },
            { icon: '🏠', text: '拥有温馨小窝' },
            { icon: '👶', text: '可爱的孩子' }
          ],
          quotes: '平平淡淡才是真，知足常乐。在平凡的日子里，你品味到了最珍贵的幸福。'
        },
        {
          emoji: '🔬',
          title: '如果当初选择了科研',
          desc: '探索未知的科学人生',
          tags: ['探索', '创新', '贡献'],
          timeline: [
            { age: 22, title: '进入实验室', desc: '加入顶尖实验室，师从院士' },
            { age: 25, title: '博士毕业', desc: '发表Nature论文，获得博士学位' },
            { age: 28, title: '出国深造', desc: '进入MIT做博士后研究' },
            { age: 32, title: '回国效力', desc: '成为国家重点实验室主任' },
            { age: 38, title: '重大突破', desc: '研究成果改变世界，获得诺贝尔奖提名' }
          ],
          stories: [
            '你选择了科研道路，在实验室里度过了无数个日夜。你的研究成果解决了困扰人类多年的难题，获得了国际认可，成为了国家的骄傲。',
            '你选择了科研，虽然大部分时间都在失败中度过，但一次偶然的实验意外，让你发现了新材料，开启了全新的产业革命。'
          ],
          stats: [
            { icon: '📚', name: '学识', value: 98, color: '#667eea' },
            { icon: '💼', name: '事业', value: 90, color: '#f093fb' },
            { icon: '❤️', name: '感情', value: 40, color: '#fa709a' },
            { icon: '💰', name: '财富', value: 75, color: '#48bb78' },
            { icon: '🏃', name: '健康', value: 60, color: '#4facfe' }
          ],
          achievements: [
            { icon: '📄', text: '发表Nature论文' },
            { icon: '🏆', text: '国家科技进步奖' },
            { icon: '🌍', text: '改变世界的发现' }
          ],
          quotes: '科学的道路上没有捷径，但每一步都值得。在探索未知中，你找到了生命的意义。'
        }
      ],
      mottos: [
        '人生没有对错，只有选择',
        '每一种人生都有它的精彩',
        '活在当下，珍惜眼前',
        '过去无法改变，未来掌握在自己手中',
        '平行人生的意义，是让我们更珍惜现在',
        '无论选择哪条路，只要坚持都会开花',
        '人生的精彩不在于选择，而在于如何走下去'
      ],
      currentMotto: ''
    }
  },
  onShow() {
    this.refreshMotto()
    this.loadSavedLives()
  },
  methods: {
    exploreBranch(branch) {
      this.resultBranch = branch
      this.resultStory = branch.stories[Math.floor(Math.random() * branch.stories.length)]
      this.resultStats = branch.stats
      this.resultQuote = branch.quotes
      this.resultTimeline = branch.timeline
      this.resultAchievements = branch.achievements
      this.showResult = true
      
      setTimeout(() => {
        uni.createSelectorQuery().select('.result-section').boundingClientRect(rect => {
          if (rect) {
            uni.pageScrollTo({ scrollTop: rect.top + 200, duration: 500 })
          }
        }).exec()
      }, 100)
    },
    saveParallelLife() {
      const life = {
        emoji: this.resultBranch.emoji,
        title: this.resultBranch.title,
        quote: this.resultQuote,
        date: new Date().toLocaleDateString(),
        stats: this.resultStats,
        story: this.resultStory
      }
      this.savedLives.unshift(life)
      uni.setStorageSync('savedLives', this.savedLives)
      uni.showToast({ title: '已收藏', icon: 'success' })
    },
    loadSavedLives() {
      this.savedLives = uni.getStorageSync('savedLives') || []
    },
    tryAnother() {
      this.showResult = false
      setTimeout(() => {
        uni.pageScrollTo({ scrollTop: 400, duration: 300 })
      }, 100)
    },
    viewSavedLife(life) {
      uni.showModal({
        title: life.title,
        content: life.story + '\n\n"' + life.quote + '"',
        showCancel: false,
        confirmText: '知道了'
      })
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

.life-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.life-label {
  font-size: 28rpx;
  opacity: 0.8;
}

.life-age {
  font-size: 32rpx;
  font-weight: bold;
}

.life-stats {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 20rpx;
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

.stat-info {
  flex: 1;
}

.stat-name {
  font-size: 24rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 6rpx;
}

.stat-bar {
  height: 10rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 5rpx;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  border-radius: 5rpx;
  transition: width 1s ease;
}

.stat-value {
  font-size: 24rpx;
  font-weight: bold;
  margin-left: 12rpx;
  width: 50rpx;
  text-align: right;
}

.life-tags {
  display: flex;
  gap: 12rpx;
  flex-wrap: wrap;
}

.life-tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
}

/* 时间线 */
.timeline-section {
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 20rpx;
  display: block;
}

.timeline {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  padding: 16rpx 0;
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 15rpx;
  top: 40rpx;
  width: 2rpx;
  height: calc(100% - 10rpx);
  background: #e2e8f0;
}

.timeline-dot {
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  background: #e2e8f0;
  margin-right: 20rpx;
  flex-shrink: 0;
  margin-top: 4rpx;
}

.timeline-dot-active {
  background: #667eea;
}

.timeline-content {
  flex: 1;
}

.timeline-age {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
  display: block;
  margin-bottom: 4rpx;
}

.timeline-text {
  font-size: 26rpx;
  color: #4a5568;
}

/* 分支选择 */
.branch-section {
  margin-bottom: 30rpx;
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
  flex-shrink: 0;
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
  display: block;
  margin-bottom: 10rpx;
}

.branch-tags {
  display: flex;
  gap: 8rpx;
}

.branch-tag {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

.branch-arrow {
  font-size: 36rpx;
  color: #a0aec0;
  margin-left: 10rpx;
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

.result-header {
  text-align: center;
  margin-bottom: 30rpx;
}

.result-emoji {
  font-size: 60rpx;
  display: block;
  margin-bottom: 10rpx;
}

.result-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2d3748;
}

/* 结果时间线 */
.result-timeline {
  margin-bottom: 30rpx;
  padding-left: 20rpx;
}

.rt-item {
  display: flex;
  align-items: flex-start;
  padding: 12rpx 0;
  position: relative;
}

.rt-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 55rpx;
  top: 40rpx;
  width: 2rpx;
  height: calc(100% - 10rpx);
  background: #e2e8f0;
}

.rt-age {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  width: 60rpx;
  flex-shrink: 0;
}

.rt-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: #667eea;
  margin-right: 16rpx;
  margin-top: 6rpx;
  flex-shrink: 0;
}

.rt-content {
  flex: 1;
}

.rt-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.rt-desc {
  font-size: 24rpx;
  color: #718096;
}

.result-story {
  font-size: 28rpx;
  color: #4a5568;
  line-height: 1.8;
  display: block;
  margin-bottom: 30rpx;
  padding: 20rpx;
  background: #f7fafc;
  border-radius: 16rpx;
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
  transition: width 1.5s ease;
}

.p-stat-value {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
  width: 60rpx;
  text-align: right;
}

/* 成就 */
.result-achievements {
  margin-bottom: 30rpx;
}

.achievements-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 16rpx;
}

.achievements-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.achievement-item {
  display: flex;
  align-items: center;
  background: #f7fafc;
  padding: 16rpx 20rpx;
  border-radius: 12rpx;
}

.achievement-icon {
  font-size: 36rpx;
  margin-right: 16rpx;
}

.achievement-text {
  font-size: 26rpx;
  color: #4a5568;
}

/* 格言 */
.result-quote {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 16rpx;
  padding: 30rpx;
  text-align: center;
  margin-bottom: 30rpx;
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
  line-height: 1.6;
}

/* 操作按钮 */
.result-actions {
  display: flex;
  gap: 20rpx;
}

.result-btn {
  flex: 1;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-secondary {
  background: #f7fafc;
  color: #667eea;
}

/* 收藏的人生 */
.saved-section {
  margin-bottom: 30rpx;
}

.saved-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.saved-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.saved-emoji {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.saved-info {
  flex: 1;
}

.saved-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.saved-date {
  font-size: 22rpx;
  color: #a0aec0;
}

.saved-arrow {
  font-size: 32rpx;
  color: #a0aec0;
}

/* 格言卡片 */
.motto-section {
  margin-bottom: 30rpx;
}

.motto-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
}

.motto-icon {
  font-size: 48rpx;
  display: block;
  margin-bottom: 16rpx;
}

.motto-text {
  font-size: 30rpx;
  color: #fff;
  line-height: 1.6;
  display: block;
  margin-bottom: 20rpx;
}

.motto-refresh {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
}

.refresh-icon {
  font-size: 24rpx;
}

.refresh-text {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: underline;
}

.bottom-space {
  height: 40rpx;
}
</style>
