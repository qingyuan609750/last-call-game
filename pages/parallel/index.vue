<template>
  <view class="container">
    <!-- 顶部标题 -->
    <view class="parallel-header">
      <text class="parallel-title">🌍 平行人生</text>
      <text class="parallel-desc">如果人生可以重来，你会怎么选？</text>
    </view>

    <!-- 模式选择 -->
    <view class="mode-section" v-if="!gameStarted && !showHistory">
      <view class="mode-card mode-new" @click="startNewLife">
        <text class="mode-icon">🍼</text>
        <text class="mode-title">重新开始</text>
        <text class="mode-desc">从0岁开始，体验全新人生</text>
      </view>
      <view class="mode-card mode-parallel" @click="showParallelMode">
        <text class="mode-icon">🔄</text>
        <text class="mode-title">人生岔路</text>
        <text class="mode-desc">从当前年龄，探索不同选择</text>
      </view>
      <view class="mode-card mode-history" @click="showHistory = true">
        <text class="mode-icon">📚</text>
        <text class="mode-title">人生回忆录</text>
        <text class="mode-desc">查看你经历过的所有人生</text>
      </view>
    </view>

    <!-- 人生回忆录 -->
    <view class="history-section" v-if="showHistory">
      <view class="history-header">
        <text class="history-title">📚 人生回忆录</text>
        <text class="history-back" @click="showHistory = false">返回</text>
      </view>
      <view class="history-stats-bar">
        <view class="h-stat">
          <text class="h-stat-num">{{lifeHistory.length}}</text>
          <text class="h-stat-label">经历人生</text>
        </view>
        <view class="h-stat">
          <text class="h-stat-num">{{bestScore}}</text>
          <text class="h-stat-label">最高评分</text>
        </view>
        <view class="h-stat">
          <text class="h-stat-num">{{avgAge}}</text>
          <text class="h-stat-label">平均寿命</text>
        </view>
      </view>
      <view class="history-list" v-if="lifeHistory.length > 0">
        <view class="history-card" v-for="(life, index) in lifeHistory" :key="index" @click="viewLifeDetail(life)">
          <view class="history-top">
            <text class="history-emoji">{{life.finalEmoji}}</text>
            <view class="history-info">
              <text class="history-name">{{life.name}}</text>
              <text class="history-summary">享年{{life.age}}岁 · {{life.achievement}}</text>
            </view>
            <text class="history-score">{{life.totalScore}}分</text>
          </view>
          <view class="history-tags">
            <text class="h-tag" v-for="(tag, i) in life.tags" :key="i">{{tag}}</text>
          </view>
        </view>
      </view>
      <view class="empty-history" v-else>
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有人生记录</text>
        <text class="empty-desc">开始你的第一次人生吧</text>
      </view>
    </view>

    <!-- 游戏主界面 -->
    <view class="game-container" v-if="gameStarted">
      <!-- 状态栏 -->
      <view class="status-bar">
        <view class="age-badge">
          <text class="age-num">{{currentAge}}</text>
          <text class="age-label">岁</text>
        </view>
        <view class="year-progress">
          <view class="progress-bar">
            <view class="progress-fill" :style="{width: (currentAge / 100 * 100) + '%'}"></view>
          </view>
          <text class="progress-text">人生进度 {{currentAge}}%</text>
        </view>
      </view>

      <!-- 属性面板 -->
      <view class="stats-panel">
        <view class="stat-row">
          <view class="stat-box" v-for="(stat, key) in stats" :key="key">
            <text class="stat-emoji">{{stat.emoji}}</text>
            <text class="stat-name">{{stat.name}}</text>
            <view class="stat-value-bar">
              <view class="stat-value-fill" :style="{width: stat.value + '%', background: stat.color}"></view>
            </view>
            <text class="stat-value-num">{{stat.value}}</text>
          </view>
        </view>
      </view>

      <!-- 人生事件流 -->
      <view class="events-timeline">
        <view class="event-item" 
          v-for="(event, index) in visibleEvents" 
          :key="index"
          :class="{'event-major': event.type === 'major', 'event-choice': event.type === 'choice', 'event-random': event.type === 'random', 'event-death': event.type === 'death'}">
          <view class="event-age">{{event.age}}岁</view>
          <view class="event-dot"></view>
          <view class="event-content">
            <text class="event-title">{{event.title}}</text>
            <text class="event-desc">{{event.desc}}</text>
            <view class="event-effects" v-if="event.effects">
              <text class="effect-tag" v-for="(effect, i) in event.effects" :key="i" :class="{'effect-positive': effect.value > 0, 'effect-negative': effect.value < 0}">
                {{effect.name}} {{effect.value > 0 ? '+' : ''}}{{effect.value}}
              </text>
            </view>
          </view>
        </view>
      </view>

      <!-- 当前抉择 -->
      <view class="choice-panel" v-if="currentChoice">
        <view class="choice-card">
          <view class="choice-header">
            <text class="choice-icon">🤔</text>
            <text class="choice-title">{{currentChoice.title}}</text>
          </view>
          <text class="choice-desc">{{currentChoice.desc}}</text>
          <view class="choice-options">
            <view class="choice-option" v-for="(option, index) in currentChoice.options" :key="index" @click="makeChoice(option)">
              <text class="option-text">{{option.text}}</text>
              <view class="option-effects">
                <text class="opt-effect" v-for="(eff, i) in option.effects" :key="i">{{eff.name}} {{eff.value > 0 ? '+' : ''}}{{eff.value}}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 继续按钮 -->
      <view class="action-area" v-if="!currentChoice && !isDead">
        <button class="continue-btn" @click="nextYear" :disabled="isAutoPlaying">
          <text class="btn-text">{{isAutoPlaying ? '自动播放中...' : '继续人生'}}</text>
        </button>
        <button class="auto-btn" @click="toggleAutoPlay">
          <text class="btn-text">{{isAutoPlaying ? '停止' : '自动'}}</text>
        </button>
      </view>

      <!-- 死亡界面 -->
      <view class="death-panel" v-if="isDead">
        <view class="death-card">
          <text class="death-emoji">🕯️</text>
          <text class="death-title">人生终章</text>
          <text class="death-age">{{currentAge}}岁</text>
          <text class="death-cause">{{deathCause}}</text>
          
          <view class="life-summary">
            <text class="summary-title">人生总结</text>
            <view class="summary-stats">
              <view class="s-stat" v-for="(stat, key) in stats" :key="key">
                <text class="s-stat-emoji">{{stat.emoji}}</text>
                <text class="s-stat-name">{{stat.name}}</text>
                <text class="s-stat-value">{{stat.value}}</text>
              </view>
            </view>
            <view class="life-achievement">
              <text class="achievement-title">🏆 人生成就</text>
              <text class="achievement-text">{{lifeAchievement}}</text>
            </view>
            <view class="life-tags">
              <text class="l-tag" v-for="(tag, i) in lifeTags" :key="i">{{tag}}</text>
            </view>
          </view>

          <view class="final-score">
            <text class="score-label">人生评分</text>
            <text class="score-num">{{totalScore}}</text>
            <text class="score-rank">{{scoreRank}}</text>
          </view>

          <view class="death-actions">
            <button class="restart-btn" @click="restartLife">重新开始</button>
            <button class="share-btn" @click="shareLife">分享人生</button>
          </view>
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
      gameStarted: false,
      showHistory: false,
      currentAge: 0,
      isDead: false,
      deathCause: '',
      isAutoPlaying: false,
      autoPlayTimer: null,
      currentChoice: null,
      lifeName: '',
      totalScore: 0,
      scoreRank: '',
      lifeAchievement: '',
      lifeTags: [],
      finalEmoji: '',
      stats: {
        health: { name: '健康', emoji: '❤️', value: 100, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: 50, color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: 50, color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: 50, color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: 50, color: '#f6ad55' }
      },
      events: [],
      visibleEvents: [],
      lifeHistory: [],
      birthEvents: [
        { title: '👶 你出生了', desc: '在一个普通的家庭，你来到了这个世界。', type: 'major' },
        { title: '🍼 婴儿时期', desc: '你在父母的呵护下健康成长。', type: 'random' }
      ],
      childhoodEvents: [
        { title: '🎒 开始上学', desc: '你背着小书包，第一次走进校园。', type: 'major', effects: [{name: '智力', value: 5}] },
        { title: '📖 爱上阅读', desc: '你发现了一个神奇的世界——书本。', type: 'random', effects: [{name: '智力', value: 3}] },
        { title: '🏃 运动天赋', desc: '你在体育课上展现出了惊人的运动天赋。', type: 'random', effects: [{name: '健康', value: 5}] },
        { title: '🎨 艺术启蒙', desc: '你第一次拿起画笔，画出了心中的世界。', type: 'random', effects: [{name: '魅力', value: 3}] },
        { title: '👫 交到好友', desc: '你遇到了人生中第一个好朋友。', type: 'random', effects: [{name: '快乐', value: 5}] }
      ],
      teenChoices: [
        {
          age: 12,
          title: '初中分班',
          desc: '你面临初中的选择，这将影响你的未来方向。',
          options: [
            { text: '进入重点班，努力学习', effects: [{name: '智力', value: 10}, {name: '快乐', value: -5}] },
            { text: '普通班，全面发展', effects: [{name: '智力', value: 5}, {name: '魅力', value: 5}, {name: '快乐', value: 5}] },
            { text: '艺术特长班', effects: [{name: '魅力', value: 10}, {name: '智力', value: 3}] }
          ]
        },
        {
          age: 15,
          title: '高中抉择',
          desc: '中考结束，你需要选择未来的方向。',
          options: [
            { text: '重点高中，冲击名校', effects: [{name: '智力', value: 15}, {name: '健康', value: -5}, {name: '快乐', value: -5}] },
            { text: '普通高中，轻松学习', effects: [{name: '智力', value: 5}, {name: '快乐', value: 10}] },
            { text: '职高，学一门技术', effects: [{name: '财富', value: 5}, {name: '快乐', value: 5}] }
          ]
        },
        {
          age: 18,
          title: '人生大考',
          desc: '高考结束了，你的成绩决定了下一步。',
          options: [
            { text: '考上985/211，继续深造', effects: [{name: '智力', value: 20}, {name: '财富', value: -5}] },
            { text: '普通大学，安稳度日', effects: [{name: '智力', value: 10}, {name: '快乐', value: 5}] },
            { text: '直接工作，积累经验', effects: [{name: '财富', value: 10}, {name: '快乐', value: -3}] },
            { text: '出国留学，开阔眼界', effects: [{name: '智力', value: 15}, {name: '魅力', value: 10}, {name: '财富', value: -15}] }
          ]
        }
      ],
      adultChoices: [
        {
          age: 22,
          title: '毕业选择',
          desc: '大学毕业，你站在人生的十字路口。',
          options: [
            { text: '考研深造', effects: [{name: '智力', value: 15}, {name: '财富', value: -10}] },
            { text: '进入大厂工作', effects: [{name: '财富', value: 15}, {name: '健康', value: -5}] },
            { text: '考公务员', effects: [{name: '快乐', value: 10}, {name: '财富', value: 5}] },
            { text: '创业', effects: [{name: '财富', value: -10}, {name: '智力', value: 10}, {name: '快乐', value: 5}] }
          ]
        },
        {
          age: 25,
          title: '感情抉择',
          desc: '你遇到了一个特别的人，你会怎么选择？',
          options: [
            { text: '勇敢表白，追求爱情', effects: [{name: '快乐', value: 15}, {name: '魅力', value: 5}] },
            { text: '专注事业，暂时不谈', effects: [{name: '财富', value: 10}, {name: '快乐', value: -5}] },
            { text: '顺其自然，不主动', effects: [{name: '快乐', value: 5}] }
          ]
        },
        {
          age: 30,
          title: '事业瓶颈',
          desc: '工作遇到了瓶颈，你需要做出改变。',
          options: [
            { text: '跳槽到更好的公司', effects: [{name: '财富', value: 15}, {name: '快乐', value: 5}] },
            { text: '辞职创业', effects: [{name: '财富', value: -15}, {name: '智力', value: 10}, {name: '快乐', value: 10}] },
            { text: '坚守岗位，等待机会', effects: [{name: '财富', value: 5}, {name: '快乐', value: -5}] }
          ]
        },
        {
          age: 35,
          title: '家庭与事业',
          desc: '孩子出生了，你需要平衡家庭和事业。',
          options: [
            { text: '以家庭为重', effects: [{name: '快乐', value: 15}, {name: '财富', value: -5}] },
            { text: '以事业为重', effects: [{name: '财富', value: 15}, {name: '快乐', value: -5}] },
            { text: '努力平衡两者', effects: [{name: '快乐', value: 5}, {name: '财富', value: 5}, {name: '健康', value: -5}] }
          ]
        },
        {
          age: 45,
          title: '中年危机',
          desc: '你开始思考人生的意义。',
          options: [
            { text: '转行做自己喜欢的事', effects: [{name: '快乐', value: 20}, {name: '财富', value: -10}] },
            { text: '继续当前的工作', effects: [{name: '财富', value: 10}, {name: '快乐', value: -5}] },
            { text: '提前退休，享受生活', effects: [{name: '快乐', value: 15}, {name: '健康', value: 10}, {name: '财富', value: -15}] }
          ]
        }
      ],
      randomEvents: [
        { title: '🏥 生病住院', desc: '一场大病让你意识到健康的重要性。', effects: [{name: '健康', value: -10}, {name: '财富', value: -5}] },
        { title: '🎰 彩票中奖', desc: '你买了一张彩票，居然中了大奖！', effects: [{name: '财富', value: 20}, {name: '快乐', value: 10}] },
        { title: '💔 失恋', desc: '一段感情结束了，你很伤心。', effects: [{name: '快乐', value: -15}] },
        { title: '💘 遇到真爱', desc: '你遇到了那个对的人。', effects: [{name: '快乐', value: 20}, {name: '魅力', value: 5}] },
        { title: '📈 投资成功', desc: '你的投资获得了丰厚的回报。', effects: [{name: '财富', value: 15}] },
        { title: '📉 投资失败', desc: '一次失败的投资让你损失惨重。', effects: [{name: '财富', value: -15}, {name: '快乐', value: -5}] },
        { title: '🏆 获得奖项', desc: '你的努力得到了认可。', effects: [{name: '快乐', value: 10}, {name: '魅力', value: 5}] },
        { title: '📚 学习新技能', desc: '你学会了新的技能，感觉很充实。', effects: [{name: '智力', value: 5}, {name: '快乐', value: 5}] },
        { title: '🏋️ 坚持健身', desc: '你养成了健身的好习惯。', effects: [{name: '健康', value: 10}, {name: '魅力', value: 5}] },
        { title: '🎮 沉迷游戏', desc: '你沉迷游戏，荒废了时间。', effects: [{name: '智力', value: -5}, {name: '健康', value: -5}] },
        { title: '✈️ 出国旅行', desc: '一次难忘的旅行经历。', effects: [{name: '快乐', value: 10}, {name: '魅力', value: 5}] },
        { title: '👴 亲人离世', desc: '一位亲人离开了，你很悲痛。', effects: [{name: '快乐', value: -20}] },
        { title: '👶 孩子出生', desc: '新生命的到来让你充满喜悦。', effects: [{name: '快乐', value: 25}] },
        { title: '🏠 买房', desc: '你终于有了自己的房子。', effects: [{name: '财富', value: -10}, {name: '快乐', value: 10}] },
        { title: '🚗 车祸', desc: '一场车祸让你受伤。', effects: [{name: '健康', value: -15}, {name: '财富', value: -5}] }
      ],
      achievements: [
        { condition: (s) => s.intelligence.value >= 90, text: '博学多才的智者', tags: ['学霸', '知识分子'] },
        { condition: (s) => s.wealth.value >= 90, text: '富可敌国的富豪', tags: ['富豪', '成功人士'] },
        { condition: (s) => s.charm.value >= 90, text: '万人迷的魅力之星', tags: ['明星', '魅力'] },
        { condition: (s) => s.happiness.value >= 90, text: '幸福满满的人生赢家', tags: ['幸福', '快乐'] },
        { condition: (s) => s.health.value >= 90, text: '健康长寿的百岁老人', tags: ['健康', '长寿'] },
        { condition: (s) => s.intelligence.value >= 70 && s.wealth.value >= 70, text: '智慧与财富并存的精英', tags: ['精英', '成功人士'] },
        { condition: (s) => s.happiness.value >= 70 && s.wealth.value < 50, text: '知足常乐的快乐人', tags: ['平凡', '快乐'] },
        { condition: (s) => s.wealth.value >= 80 && s.happiness.value < 40, text: '孤独的成功者', tags: ['富豪', '孤独'] },
        { condition: (s) => Object.values(s).every(v => v.value >= 60), text: '全面发展的完美人生', tags: ['完美', '平衡'] },
        { condition: (s) => s.health.value < 30, text: '体弱多病的一生', tags: ['坎坷', '坚强'] },
        { condition: (s) => true, text: '平凡而真实的人生', tags: ['平凡', '真实'] }
      ]
    }
  },
  computed: {
    bestScore() {
      if (this.lifeHistory.length === 0) return 0
      return Math.max(...this.lifeHistory.map(l => l.totalScore))
    },
    avgAge() {
      if (this.lifeHistory.length === 0) return 0
      return Math.round(this.lifeHistory.reduce((sum, l) => sum + l.age, 0) / this.lifeHistory.length)
    }
  },
  onShow() {
    this.loadHistory()
  },
  methods: {
    loadHistory() {
      this.lifeHistory = uni.getStorageSync('lifeHistory') || []
    },
    saveHistory() {
      uni.setStorageSync('lifeHistory', this.lifeHistory)
    },
    startNewLife() {
      this.gameStarted = true
      this.showHistory = false
      this.currentAge = 0
      this.isDead = false
      this.deathCause = ''
      this.currentChoice = null
      this.events = []
      this.visibleEvents = []
      this.isAutoPlaying = false
      if (this.autoPlayTimer) clearInterval(this.autoPlayTimer)
      
      // 重置属性
      this.stats = {
        health: { name: '健康', emoji: '❤️', value: 100, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: this.randomStat(), color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: this.randomStat(30, 70), color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: this.randomStat(), color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: this.randomStat(), color: '#f6ad55' }
      }
      
      // 出生事件
      this.addEvent({
        age: 0,
        title: '👶 你出生了',
        desc: `你出生在一个${this.randomFamily()}家庭。`,
        type: 'major'
      })
      
      this.nextYear()
    },
    showParallelMode() {
      uni.showToast({ title: '功能开发中', icon: 'none' })
    },
    randomStat(min = 40, max = 80) {
      return Math.floor(Math.random() * (max - min) + min)
    },
    randomFamily() {
      const families = ['普通', '知识分子', '商人', '工人', '农民', '公务员', '艺术']
      return families[Math.floor(Math.random() * families.length)]
    },
    addEvent(event) {
      this.events.unshift(event)
      this.visibleEvents = [...this.events]
    },
    nextYear() {
      if (this.isDead) return
      
      this.currentAge++
      
      // 检查是否有抉择点
      const choice = this.findChoice(this.currentAge)
      if (choice) {
        this.currentChoice = choice
        return
      }
      
      // 随机事件
      if (Math.random() < 0.3) {
        this.triggerRandomEvent()
      }
      
      // 年龄相关事件
      this.triggerAgeEvent()
      
      // 自然属性变化
      this.naturalChanges()
      
      // 检查死亡
      this.checkDeath()
      
      // 自动滚动
      this.$nextTick(() => {
        uni.createSelectorQuery().select('.events-timeline').boundingClientRect(rect => {
          if (rect) {
            uni.pageScrollTo({ scrollTop: rect.height, duration: 300 })
          }
        }).exec()
      })
    },
    findChoice(age) {
      const allChoices = [...this.teenChoices, ...this.adultChoices]
      return allChoices.find(c => c.age === age)
    },
    makeChoice(option) {
      // 应用效果
      option.effects.forEach(effect => {
        this.changeStat(effect.name, effect.value)
      })
      
      this.addEvent({
        age: this.currentAge,
        title: `🎯 ${this.currentChoice.title}`,
        desc: `你选择了：${option.text}`,
        type: 'choice',
        effects: option.effects
      })
      
      this.currentChoice = null
      
      // 继续下一年
      setTimeout(() => {
        if (!this.isDead) this.nextYear()
      }, 500)
    },
    triggerRandomEvent() {
      const event = this.randomEvents[Math.floor(Math.random() * this.randomEvents.length)]
      const clone = JSON.parse(JSON.stringify(event))
      clone.age = this.currentAge
      
      if (clone.effects) {
        clone.effects.forEach(effect => {
          this.changeStat(effect.name, effect.value)
        })
      }
      
      this.addEvent(clone)
    },
    triggerAgeEvent() {
      let event = null
      
      if (this.currentAge === 3) {
        event = { title: '🍼 上幼儿园', desc: '你第一次离开父母，开始集体生活。', type: 'major', effects: [{name: '快乐', value: 5}] }
      } else if (this.currentAge === 6) {
        event = { title: '🎒 上小学', desc: '你背着书包，开始了漫长的学习生涯。', type: 'major', effects: [{name: '智力', value: 5}] }
      } else if (this.currentAge === 60) {
        event = { title: '🎉 退休', desc: '你退休了，开始享受晚年生活。', type: 'major', effects: [{name: '快乐', value: 10}, {name: '健康', value: -5}] }
      } else if (this.currentAge === 80) {
        event = { title: '👴 耄耋之年', desc: '你已经80岁了，身体大不如前。', type: 'major', effects: [{name: '健康', value: -15}] }
      }
      
      if (event) {
        event.age = this.currentAge
        if (event.effects) {
          event.effects.forEach(effect => {
            this.changeStat(effect.name, effect.value)
          })
        }
        this.addEvent(event)
      }
    },
    naturalChanges() {
      // 年龄对健康的影响
      if (this.currentAge > 40) {
        this.changeStat('健康', -1)
      }
      if (this.currentAge > 60) {
        this.changeStat('健康', -2)
      }
      if (this.currentAge > 80) {
        this.changeStat('健康', -3)
      }
      
      // 财富自然增长（工作年龄）
      if (this.currentAge >= 22 && this.currentAge < 60) {
        this.changeStat('财富', Math.floor(Math.random() * 3) + 1)
      }
      
      // 老年财富消耗
      if (this.currentAge >= 60) {
        this.changeStat('财富', -Math.floor(Math.random() * 2))
      }
    },
    changeStat(name, value) {
      const key = this.getStatKey(name)
      if (key && this.stats[key]) {
        this.stats[key].value = Math.max(0, Math.min(100, this.stats[key].value + value))
      }
    },
    getStatKey(name) {
      const map = { '健康': 'health', '智力': 'intelligence', '财富': 'wealth', '魅力': 'charm', '快乐': 'happiness' }
      return map[name]
    },
    checkDeath() {
      let dead = false
      let cause = ''
      
      if (this.stats.health.value <= 0) {
        dead = true
        cause = '因病去世'
      } else if (this.currentAge >= 100) {
        dead = true
        cause = '寿终正寝'
      } else if (this.currentAge >= 90 && Math.random() < 0.3) {
        dead = true
        cause = '安详离世'
      } else if (this.currentAge >= 70 && Math.random() < 0.1) {
        dead = true
        cause = '突发疾病'
      }
      
      if (dead) {
        this.isDead = true
        this.deathCause = cause
        this.stopAutoPlay()
        this.calculateResult()
      }
    },
    calculateResult() {
      // 计算总分
      let score = 0
      Object.values(this.stats).forEach(stat => {
        score += stat.value
      })
      score += this.currentAge
      this.totalScore = score
      
      // 评级
      if (score >= 400) this.scoreRank = 'S - 传奇人生'
      else if (score >= 350) this.scoreRank = 'A - 精彩人生'
      else if (score >= 300) this.scoreRank = 'B - 不错的人生'
      else if (score >= 250) this.scoreRank = 'C - 普通人生'
      else if (score >= 200) this.scoreRank = 'D - 坎坷人生'
      else this.scoreRank = 'E - 艰难人生'
      
      // 成就
      for (let ach of this.achievements) {
        if (ach.condition(this.stats)) {
          this.lifeAchievement = ach.text
          this.lifeTags = ach.tags
          break
        }
      }
      
      // 最终表情
      if (this.stats.happiness.value >= 80) this.finalEmoji = '😄'
      else if (this.stats.happiness.value >= 60) this.finalEmoji = '🙂'
      else if (this.stats.happiness.value >= 40) this.finalEmoji = '😐'
      else this.finalEmoji = '😢'
      
      // 保存到历史
      const lifeRecord = {
        name: this.lifeAchievement,
        age: this.currentAge,
        totalScore: score,
        achievement: this.lifeAchievement,
        tags: this.lifeTags,
        finalEmoji: this.finalEmoji,
        stats: JSON.parse(JSON.stringify(this.stats)),
        events: this.events,
        date: new Date().toLocaleDateString()
      }
      this.lifeHistory.unshift(lifeRecord)
      this.saveHistory()
    },
    toggleAutoPlay() {
      if (this.isAutoPlaying) {
        this.stopAutoPlay()
      } else {
        this.isAutoPlaying = true
        this.autoPlayTimer = setInterval(() => {
          if (this.currentChoice) {
            this.stopAutoPlay()
            return
          }
          if (!this.isDead) {
            this.nextYear()
          } else {
            this.stopAutoPlay()
          }
        }, 800)
      }
    },
    stopAutoPlay() {
      this.isAutoPlaying = false
      if (this.autoPlayTimer) {
        clearInterval(this.autoPlayTimer)
        this.autoPlayTimer = null
      }
    },
    restartLife() {
      this.startNewLife()
    },
    shareLife() {
      const shareText = `我在【平行人生】中体验了${this.currentAge}岁的人生，获得了${this.totalScore}分，成为了"${this.lifeAchievement}"！`
      uni.showModal({
        title: '分享人生',
        content: shareText,
        showCancel: false
      })
    },
    viewLifeDetail(life) {
      let statsText = ''
      Object.values(life.stats).forEach(s => {
        statsText += `${s.emoji}${s.name}: ${s.value}\n`
      })
      
      uni.showModal({
        title: `${life.finalEmoji} ${life.name}`,
        content: `享年${life.age}岁\n评分: ${life.totalScore}\n\n${statsText}`,
        showCancel: false
      })
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

/* 模式选择 */
.mode-section {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.mode-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

.mode-card:active {
  transform: scale(0.98);
}

.mode-new {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.mode-parallel {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
}

.mode-history {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
}

.mode-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 16rpx;
}

.mode-title {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.mode-desc {
  font-size: 24rpx;
  opacity: 0.9;
}

/* 游戏界面 */
.game-container {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

/* 状态栏 */
.status-bar {
  background: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  gap: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.age-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16rpx;
  padding: 16rpx 24rpx;
  text-align: center;
  min-width: 100rpx;
}

.age-num {
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
  display: block;
}

.age-label {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.8);
}

.year-progress {
  flex: 1;
}

.progress-bar {
  height: 16rpx;
  background: #edf2f7;
  border-radius: 8rpx;
  overflow: hidden;
  margin-bottom: 8rpx;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 8rpx;
  transition: width 0.5s ease;
}

.progress-text {
  font-size: 22rpx;
  color: #a0aec0;
}

/* 属性面板 */
.stats-panel {
  background: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.stat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.stat-box {
  width: calc(50% - 8rpx);
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 16rpx;
}

.stat-emoji {
  font-size: 32rpx;
  margin-right: 8rpx;
}

.stat-name {
  font-size: 24rpx;
  color: #718096;
}

.stat-value-bar {
  height: 10rpx;
  background: #edf2f7;
  border-radius: 5rpx;
  overflow: hidden;
  margin: 8rpx 0;
}

.stat-value-fill {
  height: 100%;
  border-radius: 5rpx;
  transition: width 0.5s ease;
}

.stat-value-num {
  font-size: 24rpx;
  font-weight: bold;
  color: #2d3748;
}

/* 事件时间线 */
.events-timeline {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.event-item {
  display: flex;
  align-items: flex-start;
  padding: 16rpx 0;
  position: relative;
}

.event-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 55rpx;
  top: 50rpx;
  width: 2rpx;
  height: calc(100% - 20rpx);
  background: #e2e8f0;
}

.event-age {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  width: 60rpx;
  flex-shrink: 0;
}

.event-dot {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background: #e2e8f0;
  margin-right: 16rpx;
  margin-top: 4rpx;
  flex-shrink: 0;
}

.event-major .event-dot {
  background: #667eea;
  width: 24rpx;
  height: 24rpx;
}

.event-choice .event-dot {
  background: #f6ad55;
}

.event-random .event-dot {
  background: #48bb78;
}

.event-death .event-dot {
  background: #e53e3e;
}

.event-content {
  flex: 1;
}

.event-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.event-desc {
  font-size: 24rpx;
  color: #718096;
  display: block;
  margin-bottom: 8rpx;
}

.event-effects {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.effect-tag {
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
  background: #edf2f7;
  color: #718096;
}

.effect-positive {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.effect-negative {
  background: rgba(229, 62, 62, 0.1);
  color: #e53e3e;
}

/* 抉择面板 */
.choice-panel {
  margin-bottom: 20rpx;
}

.choice-card {
  background: linear-gradient(135deg, #f6ad55 0%, #f093fb 100%);
  border-radius: 24rpx;
  padding: 30rpx;
  color: #fff;
}

.choice-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.choice-icon {
  font-size: 40rpx;
  margin-right: 12rpx;
}

.choice-title {
  font-size: 32rpx;
  font-weight: bold;
}

.choice-desc {
  font-size: 26rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 20rpx;
}

.choice-options {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.choice-option {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16rpx;
  padding: 20rpx;
  color: #2d3748;
}

.option-text {
  font-size: 28rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.option-effects {
  display: flex;
  gap: 8rpx;
}

.opt-effect {
  font-size: 20rpx;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

/* 操作区域 */
.action-area {
  display: flex;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.continue-btn {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 30rpx;
  border: none;
}

.auto-btn {
  width: 160rpx;
  background: #f7fafc;
  color: #667eea;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

/* 死亡面板 */
.death-panel {
  margin-bottom: 20rpx;
}

.death-card {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
  color: #fff;
}

.death-emoji {
  font-size: 80rpx;
  display: block;
  margin-bottom: 16rpx;
}

.death-title {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.death-age {
  font-size: 48rpx;
  font-weight: bold;
  color: #f6ad55;
  display: block;
  margin-bottom: 8rpx;
}

.death-cause {
  font-size: 26rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 30rpx;
}

.life-summary {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.summary-title {
  font-size: 28rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 16rpx;
}

.summary-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.s-stat {
  width: calc(50% - 8rpx);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12rpx;
  padding: 16rpx;
}

.s-stat-emoji {
  font-size: 32rpx;
  margin-right: 8rpx;
}

.s-stat-name {
  font-size: 22rpx;
  opacity: 0.8;
}

.s-stat-value {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
  margin-top: 4rpx;
}

.life-achievement {
  margin-bottom: 16rpx;
}

.achievement-title {
  font-size: 24rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 8rpx;
}

.achievement-text {
  font-size: 30rpx;
  font-weight: bold;
  color: #f6ad55;
}

.life-tags {
  display: flex;
  gap: 12rpx;
  justify-content: center;
  flex-wrap: wrap;
}

.l-tag {
  background: rgba(102, 126, 234, 0.3);
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 22rpx;
}

.final-score {
  margin-bottom: 30rpx;
}

.score-label {
  font-size: 26rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 8rpx;
}

.score-num {
  font-size: 64rpx;
  font-weight: bold;
  color: #f6ad55;
  display: block;
}

.score-rank {
  font-size: 28rpx;
  color: #48bb78;
}

.death-actions {
  display: flex;
  gap: 20rpx;
}

.restart-btn {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

.share-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

/* 历史记录 */
.history-section {
  animation: fadeIn 0.5s ease;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.history-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.history-back {
  font-size: 26rpx;
  color: #667eea;
}

.history-stats-bar {
  display: flex;
  gap: 16rpx;
  margin-bottom: 20rpx;
}

.h-stat {
  flex: 1;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  text-align: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.h-stat-num {
  font-size: 36rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
}

.h-stat-label {
  font-size: 22rpx;
  color: #a0aec0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.history-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.history-top {
  display: flex;
  align-items: center;
  margin-bottom: 12rpx;
}

.history-emoji {
  font-size: 48rpx;
  margin-right: 16rpx;
}

.history-info {
  flex: 1;
}

.history-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
}

.history-summary {
  font-size: 22rpx;
  color: #a0aec0;
}

.history-score {
  font-size: 32rpx;
  font-weight: bold;
  color: #f6ad55;
}

.history-tags {
  display: flex;
  gap: 8rpx;
}

.h-tag {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

.empty-history {
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

.bottom-space {
  height: 40rpx;
}
</style>
