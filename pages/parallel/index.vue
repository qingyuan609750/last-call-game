<template>
  <view class="container">
    <!-- 顶部标题 -->
    <view class="parallel-header">
      <text class="parallel-title">🌍 平行人生推演器</text>
      <text class="parallel-desc">自定义你的人生，推演无限可能</text>
    </view>

    <!-- 模式选择 -->
    <view class="mode-section" v-if="!gameStarted && !showHistory && !showCustomCreator">
      <view class="mode-card mode-new" @click="startNewLife">
        <text class="mode-icon">🍼</text>
        <text class="mode-title">随机人生</text>
        <text class="mode-desc">快速开始，随机属性</text>
      </view>
      <view class="mode-card mode-custom" @click="openCustomCreator">
        <text class="mode-icon">✏️</text>
        <text class="mode-title">自定义人生</text>
        <text class="mode-desc">设定背景、性格、目标</text>
      </view>
      <view class="mode-card mode-whatif" @click="openWhatIf">
        <text class="mode-icon">❓</text>
        <text class="mode-title">如果当初...</text>
        <text class="mode-desc">改变过去，推演未来</text>
      </view>
      <view class="mode-card mode-history" @click="showHistory = true">
        <text class="mode-icon">📚</text>
        <text class="mode-title">人生档案馆</text>
        <text class="mode-desc">查看所有推演记录</text>
      </view>
    </view>

    <!-- 自定义人生创建器 -->
    <view class="creator-section" v-if="showCustomCreator && !gameStarted">
      <view class="creator-header">
        <text class="creator-title">✏️ 创建你的人生</text>
        <text class="creator-back" @click="showCustomCreator = false">取消</text>
      </view>

      <view class="creator-form">
        <!-- 基础信息 -->
        <view class="form-section">
          <text class="form-title">基础信息</text>
          <view class="form-item">
            <text class="form-label">姓名</text>
            <input class="form-input" v-model="customProfile.name" placeholder="输入你的名字" />
          </view>
          <view class="form-item">
            <text class="form-label">出生年份</text>
            <picker mode="selector" :range="yearOptions" :value="yearIndex" @change="onYearChange">
              <view class="form-picker">{{customProfile.birthYear}}年</view>
            </picker>
          </view>
          <view class="form-item">
            <text class="form-label">出生地</text>
            <input class="form-input" v-model="customProfile.birthPlace" placeholder="例如：北京、上海、农村..." />
          </view>
          <view class="form-item">
            <text class="form-label">家庭背景</text>
            <view class="tag-selector">
              <text 
                class="select-tag" 
                v-for="(tag, index) in familyTags" 
                :key="index"
                :class="{'select-tag-active': customProfile.family === tag}"
                @click="customProfile.family = tag"
              >{{tag}}</text>
            </view>
          </view>
        </view>

        <!-- 性格特质 -->
        <view class="form-section">
          <text class="form-title">性格特质（选择3个）</text>
          <view class="tag-selector">
            <text 
              class="select-tag" 
              v-for="(trait, index) in personalityTraits" 
              :key="index"
              :class="{'select-tag-active': customProfile.traits.includes(trait)}"
              @click="toggleTrait(trait)"
            >{{trait}}</text>
          </view>
        </view>

        <!-- 初始属性分配 -->
        <view class="form-section">
          <text class="form-title">初始属性（共100点）</text>
          <text class="form-subtitle">剩余: {{remainingPoints}}点</text>
          <view class="point-allocation">
            <view class="point-item" v-for="(stat, key) in customStats" :key="key">
              <text class="point-emoji">{{stat.emoji}}</text>
              <text class="point-name">{{stat.name}}</text>
              <view class="point-control">
                <text class="point-btn" @click="adjustPoint(key, -5)">-</text>
                <text class="point-value">{{stat.value}}</text>
                <text class="point-btn" @click="adjustPoint(key, 5)">+</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 人生目标 -->
        <view class="form-section">
          <text class="form-title">人生目标</text>
          <view class="tag-selector">
            <text 
              class="select-tag" 
              v-for="(goal, index) in lifeGoals" 
              :key="index"
              :class="{'select-tag-active': customProfile.goal === goal}"
              @click="customProfile.goal = goal"
            >{{goal}}</text>
          </view>
        </view>

        <!-- 初始事件 -->
        <view class="form-section">
          <text class="form-title">开局事件（可选）</text>
          <textarea 
            class="form-textarea" 
            v-model="customProfile.startEvent"
            placeholder="描述一件影响你人生起点的事件，例如：父母离异、获得奖学金、遭遇车祸..."
            maxlength="200"
          />
        </view>

        <button class="start-custom-btn" @click="startCustomLife">开始推演</button>
      </view>
    </view>

    <!-- 如果当初模式 -->
    <view class="whatif-section" v-if="showWhatIf && !gameStarted">
      <view class="whatif-header">
        <text class="whatif-title">❓ 如果当初...</text>
        <text class="whatif-back" @click="showWhatIf = false">返回</text>
      </view>
      <view class="whatif-desc">选择一个你已经经历过的人生，改变其中一个关键决定，看看会发生什么。</view>
      <view class="whatif-list" v-if="lifeHistory.length > 0">
        <view class="whatif-card" v-for="(life, index) in lifeHistory" :key="index" @click="loadLifeForWhatIf(life)">
          <text class="whatif-emoji">{{life.finalEmoji}}</text>
          <view class="whatif-info">
            <text class="whatif-name">{{life.name || '无名人生'}}</text>
            <text class="whatif-summary">享年{{life.age}}岁 · {{life.achievement || '平凡一生'}}</text>
          </view>
          <text class="whatif-score">{{life.totalScore}}分</text>
        </view>
      </view>
      <view class="empty-whatif" v-else>
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有人生记录</text>
        <text class="empty-desc">先去体验一次人生吧</text>
      </view>
    </view>

    <!-- 改变决定界面 -->
    <view class="change-choice-section" v-if="showChangeChoice">
      <view class="change-header">
        <text class="change-title">🔄 改变决定</text>
        <text class="change-back" @click="showChangeChoice = false">返回</text>
      </view>
      <view class="change-desc">你回到了{{changeAge}}岁，重新做出选择...</view>
      <view class="original-choice">
        <text class="orig-label">原来的选择：</text>
        <text class="orig-text">{{originalChoiceText}}</text>
      </view>
      <view class="new-choices">
        <view class="new-choice-option" v-for="(option, index) in alternativeChoices" :key="index" @click="applyNewChoice(option)">
          <text class="new-choice-text">{{option.text}}</text>
          <view class="new-choice-effects">
            <text class="nce-tag" v-for="(eff, i) in option.effects" :key="i">{{eff.name}} {{eff.value > 0 ? '+' : ''}}{{eff.value}}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 游戏主界面 -->
    <view class="game-container" v-if="gameStarted">
      <!-- 状态栏 -->
      <view class="status-bar">
        <view class="player-info">
          <text class="player-name">{{playerName}}</text>
          <view class="age-badge">
            <text class="age-num">{{currentAge}}</text>
            <text class="age-label">岁</text>
          </view>
        </view>
        <view class="year-progress">
          <view class="progress-bar">
            <view class="progress-fill" :style="{width: Math.min(currentAge, 100) + '%'}"></view>
          </view>
          <text class="progress-text">{{currentYear}}年</text>
        </view>
      </view>

      <!-- 属性面板 -->
      <view class="stats-panel">
        <view class="stat-row">
          <view class="stat-box" v-for="(stat, key) in stats" :key="key" :class="{'stat-box-low': stat.value < 30}">
            <text class="stat-emoji">{{stat.emoji}}</text>
            <text class="stat-name">{{stat.name}}</text>
            <view class="stat-value-bar">
              <view class="stat-value-fill" :style="{width: stat.value + '%', background: stat.color}"></view>
            </view>
            <text class="stat-value-num">{{stat.value}}</text>
          </view>
        </view>
      </view>

      <!-- 关系网络 -->
      <view class="relations-panel" v-if="Object.keys(relations).length > 0">
        <view class="relations-header" @click="showRelations = !showRelations">
          <text class="relations-title">👥 关系网 ({{Object.keys(relations).length}})</text>
          <text class="relations-toggle">{{showRelations ? '收起' : '展开'}}</text>
        </view>
        <view class="relations-list" v-if="showRelations">
          <view class="relation-item" v-for="(rel, name) in relations" :key="name">
            <text class="relation-emoji">{{rel.emoji}}</text>
            <text class="relation-name">{{name}}</text>
            <view class="relation-bar">
              <view class="relation-fill" :style="{width: rel.value + '%'}"></view>
            </view>
            <text class="relation-value">{{rel.value}}</text>
          </view>
        </view>
      </view>

      <!-- 人生事件流 -->
      <view class="events-timeline">
        <view class="timeline-header">
          <text class="timeline-title">📖 人生历程</text>
          <text class="timeline-count">{{events.length}}个事件</text>
        </view>
        <view class="event-item" 
          v-for="(event, index) in visibleEvents" 
          :key="index"
          :class="{'event-major': event.type === 'major', 'event-choice': event.type === 'choice', 'event-random': event.type === 'random', 'event-death': event.type === 'death', 'event-relation': event.type === 'relation'}">
          <view class="event-age">{{event.age}}岁</view>
          <view class="event-dot"></view>
          <view class="event-content">
            <text class="event-title">{{event.title}}</text>
            <text class="event-desc">{{event.desc}}</text>
            <view class="event-effects" v-if="event.effects && event.effects.length > 0">
              <text class="effect-tag" v-for="(effect, i) in event.effects" :key="i" :class="{'effect-positive': effect.value > 0, 'effect-negative': effect.value < 0}">
                {{effect.name}} {{effect.value > 0 ? '+' : ''}}{{effect.value}}
              </text>
            </view>
            <view class="event-relations" v-if="event.relations">
              <text class="rel-change" v-for="(rel, i) in event.relations" :key="i">
                {{rel.emoji}} {{rel.name}} {{rel.value > 0 ? '+' : ''}}{{rel.value}}
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
            <view class="choice-info">
              <text class="choice-title">{{currentChoice.title}}</text>
              <text class="choice-context">{{currentChoice.context}}</text>
            </view>
          </view>
          <text class="choice-desc">{{currentChoice.desc}}</text>
          <view class="choice-options">
            <view class="choice-option" v-for="(option, index) in currentChoice.options" :key="index" @click="makeChoice(option)">
              <text class="option-text">{{option.text}}</text>
              <text class="option-reason">{{option.reason}}</text>
              <view class="option-effects">
                <text class="opt-effect" v-for="(eff, i) in option.effects" :key="i">{{eff.name}} {{eff.value > 0 ? '+' : ''}}{{eff.value}}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 推演预测 -->
      <view class="prediction-panel" v-if="showPrediction && !currentChoice && !isDead">
        <view class="prediction-card">
          <text class="prediction-title">🔮 推演预测</text>
          <text class="prediction-text">{{currentPrediction}}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-area" v-if="!currentChoice && !isDead">
        <button class="continue-btn" @click="nextYear" :disabled="isAutoPlaying">
          <text class="btn-text">{{isAutoPlaying ? '推演中...' : '推进一年'}}</text>
        </button>
        <button class="auto-btn" @click="toggleAutoPlay">
          <text class="btn-text">{{isAutoPlaying ? '停止' : '自动'}}</text>
        </button>
        <button class="predict-btn" @click="generatePrediction">
          <text class="btn-text">预测</text>
        </button>
      </view>

      <!-- 死亡界面 -->
      <view class="death-panel" v-if="isDead">
        <view class="death-card">
          <text class="death-emoji">🕯️</text>
          <text class="death-title">人生终章</text>
          <text class="death-name">{{playerName}}</text>
          <text class="death-years">{{customProfile.birthYear}} - {{currentYear}}</text>
          <text class="death-age">享年{{currentAge}}岁</text>
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
            <view class="life-traits" v-if="lifeTags.length > 0">
              <text class="traits-title">人生标签</text>
              <view class="traits-list">
                <text class="l-tag" v-for="(tag, i) in lifeTags" :key="i">{{tag}}</text>
              </view>
            </view>
            <view class="life-achievement">
              <text class="achievement-title">🏆 最终成就</text>
              <text class="achievement-text">{{lifeAchievement}}</text>
            </view>
            <view class="life-epitaph">
              <text class="epitaph-mark">"</text>
              <text class="epitaph-text">{{generateEpitaph()}}</text>
            </view>
          </view>

          <view class="final-score">
            <text class="score-label">人生评分</text>
            <text class="score-num">{{totalScore}}</text>
            <text class="score-rank">{{scoreRank}}</text>
          </view>

          <view class="death-actions">
            <button class="restart-btn" @click="restartLife">重新开始</button>
            <button class="whatif-btn" @click="startWhatIfFromHere">如果当初...</button>
            <button class="share-btn" @click="shareLife">分享</button>
          </view>
        </view>
      </view>
    </view>

    <!-- 人生档案馆 -->
    <view class="history-section" v-if="showHistory">
      <view class="history-header">
        <text class="history-title">📚 人生档案馆</text>
        <text class="history-back" @click="showHistory = false">返回</text>
      </view>
      <view class="history-stats-bar">
        <view class="h-stat">
          <text class="h-stat-num">{{lifeHistory.length}}</text>
          <text class="h-stat-label">推演次数</text>
        </view>
        <view class="h-stat">
          <text class="h-stat-num">{{bestScore}}</text>
          <text class="h-stat-label">最高评分</text>
        </view>
        <view class="h-stat">
          <text class="h-stat-num">{{avgAge}}</text>
          <text class="h-stat-label">平均寿命</text>
        </view>
        <view class="h-stat">
          <text class="h-stat-num">{{totalChoices}}</text>
          <text class="h-stat-label">总抉择数</text>
        </view>
      </view>
      
      <!-- 筛选 -->
      <view class="history-filter">
        <text class="filter-label">筛选：</text>
        <scroll-view class="filter-scroll" scroll-x>
          <text class="filter-tag" :class="{'filter-active': historyFilter === 'all'}" @click="historyFilter = 'all'">全部</text>
          <text class="filter-tag" :class="{'filter-active': historyFilter === 'high'}" @click="historyFilter = 'high'">高分</text>
          <text class="filter-tag" :class="{'filter-active': historyFilter === 'long'}" @click="historyFilter = 'long'">长寿</text>
          <text class="filter-tag" :class="{'filter-active': historyFilter === 'custom'}" @click="historyFilter = 'custom'">自定义</text>
        </scroll-view>
      </view>

      <view class="history-list" v-if="filteredHistory.length > 0">
        <view class="history-card" v-for="(life, index) in filteredHistory" :key="index" @click="viewLifeDetail(life)">
          <view class="history-top">
            <text class="history-emoji">{{life.finalEmoji || '😐'}}</text>
            <view class="history-info">
              <text class="history-name">{{life.name || '无名人生'}}</text>
              <text class="history-summary">{{life.birthYear}}-{{life.deathYear}} · 享年{{life.age}}岁</text>
            </view>
            <text class="history-score">{{life.totalScore}}分</text>
          </view>
          <view class="history-mid">
            <text class="history-achievement">🏆 {{life.achievement || '平凡一生'}}</text>
          </view>
          <view class="history-tags">
            <text class="h-tag" v-for="(tag, i) in life.tags" :key="i">{{tag}}</text>
            <text class="h-tag h-tag-custom" v-if="life.isCustom">自定义</text>
          </view>
        </view>
      </view>
      <view class="empty-history" v-else>
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有人生记录</text>
        <text class="empty-desc">开始你的第一次推演吧</text>
      </view>
    </view>

    <!-- 人生详情弹窗 -->
    <view class="life-detail-modal" v-if="showLifeDetail">
      <view class="modal-mask" @click="showLifeDetail = false"></view>
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">{{selectedLife.name || '人生详情'}}</text>
          <text class="modal-close" @click="showLifeDetail = false">✕</text>
        </view>
        <scroll-view class="modal-body" scroll-y>
          <view class="detail-section">
            <text class="detail-label">基本信息</text>
            <text class="detail-text">{{selectedLife.birthYear}}年出生在{{selectedLife.birthPlace || '未知地点'}}</text>
            <text class="detail-text">家庭背景：{{selectedLife.family || '普通家庭'}}</text>
            <text class="detail-text">享年{{selectedLife.age}}岁（{{selectedLife.deathYear}}年去世）</text>
          </view>
          <view class="detail-section">
            <text class="detail-label">最终属性</text>
            <view class="detail-stats">
              <view class="d-stat" v-for="(stat, key) in selectedLife.stats" :key="key">
                <text class="d-stat-emoji">{{stat.emoji}}</text>
                <text class="d-stat-name">{{stat.name}}</text>
                <text class="d-stat-value">{{stat.value}}</text>
              </view>
            </view>
          </view>
          <view class="detail-section" v-if="selectedLife.events">
            <text class="detail-label">人生大事记</text>
            <view class="detail-events">
              <view class="d-event" v-for="(event, i) in selectedLife.events.slice(0, 20)" :key="i">
                <text class="d-event-age">{{event.age}}岁</text>
                <text class="d-event-title">{{event.title}}</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <view class="bottom-space"></view>
  </view>
</template>

<script>
// 推演引擎
class LifeEngine {
  constructor(profile, stats) {
    this.profile = profile
    this.stats = stats
    this.age = 0
    this.year = profile.birthYear || 2000
    this.relations = {}
    this.events = []
    this.choices = []
    this.isDead = false
    this.deathCause = ''
  }

  // 根据性格和属性生成个性化事件
  generateEvent(age) {
    const events = []
    const traits = this.profile.traits || []
    const family = this.profile.family || '普通家庭'
    
    // 幼年事件 (0-6)
    if (age === 0) {
      events.push(this.createEvent(age, '👶 出生', `你出生在${this.profile.birthPlace || '一个普通家庭'}，是一个${family}的孩子。`, 'major'))
    }
    if (age === 3 && traits.includes('聪明')) {
      events.push(this.createEvent(age, '📚 早慧', '你展现出了超乎同龄人的学习能力。', 'random', [{name: '智力', value: 5}]))
    }
    if (age === 5 && traits.includes('活泼')) {
      events.push(this.createEvent(age, '🏃 运动天赋', '你在幼儿园的运动会上表现突出。', 'random', [{name: '健康', value: 3}]))
    }

    // 学龄事件 (7-12)
    if (age === 7) {
      events.push(this.createEvent(age, '🎒 上小学', '你背着新书包，第一次走进校园。', 'major', [{name: '智力', value: 2}]))
    }
    if (age === 10 && this.stats.intelligence.value > 60) {
      events.push(this.createEvent(age, '🏆 成绩优异', '你的成绩在班里名列前茅。', 'random', [{name: '智力', value: 3}, {name: '快乐', value: 5}]))
    }

    // 青春期事件 (13-18)
    if (age === 13) {
      events.push(this.createEvent(age, '📖 初中生活', '进入青春期，你开始思考更多问题。', 'major'))
      if (traits.includes('叛逆')) {
        events.push(this.createEvent(age, '😤 叛逆期', '你和父母发生了激烈的争吵。', 'random', [{name: '快乐', value: -5}]))
      }
    }
    if (age === 15 && this.stats.charm.value > 60) {
      events.push(this.createEvent(age, '💕 初恋', '你有了第一次心动的感觉。', 'random', [{name: '快乐', value: 10}, {name: '魅力', value: 2}]))
    }
    if (age === 16 && traits.includes('勤奋')) {
      events.push(this.createEvent(age, '📚 刻苦学习', '你每天学习到深夜，成绩稳步提升。', 'random', [{name: '智力', value: 5}, {name: '健康', value: -3}]))
    }
    if (age === 18) {
      events.push(this.createEvent(age, '🎓 高中毕业', '你完成了基础教育，面临人生的重要选择。', 'major'))
      if (this.stats.intelligence.value > 80) {
        events.push(this.createEvent(age, '🏆 考上名校', '你的努力得到了回报，考上了理想的大学！', 'random', [{name: '快乐', value: 15}, {name: '智力', value: 5}]))
      }
    }

    // 大学/工作事件 (19-30)
    if (age === 19) {
      if (this.stats.intelligence.value > 70) {
        events.push(this.createEvent(age, '🎓 大学生活', '你进入了大学，开始了新的人生阶段。', 'major', [{name: '智力', value: 5}, {name: '魅力', value: 3}]))
      } else {
        events.push(this.createEvent(age, '💼 开始工作', '你选择了直接进入社会。', 'major', [{name: '财富', value: 5}]))
      }
    }
    if (age === 22 && this.stats.intelligence.value > 70) {
      events.push(this.createEvent(age, '🎓 大学毕业', '你完成了学业，拿到了学位证书。', 'major'))
    }
    if (age === 23 && traits.includes('冒险')) {
      events.push(this.createEvent(age, '✈️ 独自旅行', '你决定独自去远方看看。', 'random', [{name: '快乐', value: 10}, {name: '魅力', value: 5}, {name: '财富', value: -5}]))
    }
    if (age === 25) {
      if (this.stats.wealth.value > 60) {
        events.push(this.createEvent(age, '💰 事业起步', '你的工作开始有了起色。', 'random', [{name: '财富', value: 10}]))
      }
      if (traits.includes('浪漫') && this.stats.charm.value > 50) {
        events.push(this.createEvent(age, '💘 遇到真爱', '在一个偶然的场合，你遇到了那个特别的人。', 'relation', [], [{emoji: '💑', name: '伴侣', value: 80}]))
      }
    }
    if (age === 28 && this.stats.wealth.value > 80) {
      events.push(this.createEvent(age, '🏠 买房', '你终于攒够了首付，买了第一套房子。', 'random', [{name: '财富', value: -10}, {name: '快乐', value: 10}]))
    }

    // 中年事件 (31-50)
    if (age === 30) {
      events.push(this.createEvent(age, '🎂 而立之年', '30岁了，你开始认真思考人生的方向。', 'major'))
      if (this.relations['伴侣'] && this.relations['伴侣'].value > 60) {
        events.push(this.createEvent(age, '👶 孩子出生', '你们迎来了新的家庭成员！', 'major', [{name: '快乐', value: 20}], [{emoji: '👶', name: '孩子', value: 100}]))
      }
    }
    if (age === 35 && this.stats.wealth.value < 40) {
      events.push(this.createEvent(age, '😰 经济压力', '生活开销越来越大，你感到压力很大。', 'random', [{name: '快乐', value: -10}]))
    }
    if (age === 40) {
      events.push(this.createEvent(age, '🎂 不惑之年', '40岁了，你对人生有了更深的理解。', 'major', [{name: '智力', value: 5}]))
      if (traits.includes('野心') && this.stats.wealth.value > 70) {
        events.push(this.createEvent(age, '🚀 事业巅峰', '你的事业达到了新的高度。', 'random', [{name: '财富', value: 15}, {name: '快乐', value: 10}]))
      }
    }
    if (age === 45 && this.stats.health.value < 50) {
      events.push(this.createEvent(age, '🏥 健康警告', '体检报告提醒你注意健康。', 'random', [{name: '健康', value: -5}, {name: '快乐', value: -5}]))
    }

    // 老年事件 (51+)
    if (age === 50) {
      events.push(this.createEvent(age, '🎂 知天命', '50岁了，你开始回顾自己的人生。', 'major'))
    }
    if (age === 55) {
      events.push(this.createEvent(age, '🎉 退休', '你退休了，开始享受晚年生活。', 'major', [{name: '快乐', value: 10}, {name: '健康', value: -5}]))
    }
    if (age === 60) {
      if (this.stats.happiness.value > 60) {
        events.push(this.createEvent(age, '👴 含饴弄孙', '孙辈的陪伴让你的晚年充满欢乐。', 'random', [{name: '快乐', value: 15}]))
      }
    }
    if (age === 70) {
      events.push(this.createEvent(age, '🎂 古稀之年', '70岁了，你成为了家族的长辈。', 'major'))
    }
    if (age === 80) {
      events.push(this.createEvent(age, '👴 耄耋之年', '80岁高龄，身体大不如前。', 'major', [{name: '健康', value: -15}]))
    }

    // 随机事件 (每年概率触发)
    if (Math.random() < 0.15) {
      events.push(this.generateRandomEvent(age))
    }

    // 检查死亡
    this.checkDeath(age)

    return events
  }

  createEvent(age, title, desc, type = 'random', effects = [], relations = []) {
    return { age, year: this.year + age, title, desc, type, effects, relations }
  }

  generateRandomEvent(age) {
    const events = [
      { title: '🏥 生病', desc: '一场小病让你卧床休息几天。', effects: [{name: '健康', value: -5}, {name: '财富', value: -2}] },
      { title: '🎰 意外之财', desc: '你获得了一笔意外收入。', effects: [{name: '财富', value: 10}, {name: '快乐', value: 5}] },
      { title: '💔 失恋', desc: '一段感情结束了。', effects: [{name: '快乐', value: -10}] },
      { title: '💘 新恋情', desc: '你遇到了心动的人。', effects: [{name: '快乐', value: 15}, {name: '魅力', value: 3}] },
      { title: '📈 投资成功', desc: '你的投资获得了回报。', effects: [{name: '财富', value: 12}] },
      { title: '📉 投资失败', desc: '一次失败的投资让你损失惨重。', effects: [{name: '财富', value: -12}, {name: '快乐', value: -5}] },
      { title: '🏆 获得荣誉', desc: '你的努力得到了认可。', effects: [{name: '快乐', value: 10}, {name: '魅力', value: 5}] },
      { title: '📚 学习新技能', desc: '你掌握了新的能力。', effects: [{name: '智力', value: 5}, {name: '快乐', value: 3}] },
      { title: '🏋️ 健身习惯', desc: '你养成了运动的好习惯。', effects: [{name: '健康', value: 8}, {name: '魅力', value: 3}] },
      { title: '😰 工作压力', desc: '工作压力让你身心俱疲。', effects: [{name: '健康', value: -5}, {name: '快乐', value: -5}] },
      { title: '✈️ 旅行', desc: '一次难忘的旅行。', effects: [{name: '快乐', value: 10}] },
      { title: '👴 亲友离世', desc: '一位亲近的人离开了。', effects: [{name: '快乐', value: -15}] },
      { title: '🎨 培养爱好', desc: '你发现了新的兴趣。', effects: [{name: '快乐', value: 8}, {name: '魅力', value: 3}] },
      { title: '🤝 贵人相助', desc: '有人在你困难时伸出了援手。', effects: [{name: '财富', value: 5}, {name: '快乐', value: 5}] },
      { title: '😤 人际冲突', desc: '你和朋友发生了矛盾。', effects: [{name: '快乐', value: -8}] }
    ]
    
    const event = events[Math.floor(Math.random() * events.length)]
    return this.createEvent(age, event.title, event.desc, 'random', event.effects)
  }

  checkDeath(age) {
    if (this.stats.health.value <= 0) {
      this.isDead = true
      this.deathCause = '因病去世'
    } else if (age >= 100) {
      this.isDead = true
      this.deathCause = '寿终正寝'
    } else if (age >= 90 && Math.random() < 0.25) {
      this.isDead = true
      this.deathCause = '安详离世'
    } else if (age >= 75 && Math.random() < 0.1) {
      this.isDead = true
      this.deathCause = '突发疾病'
    } else if (age >= 60 && this.stats.health.value < 20 && Math.random() < 0.15) {
      this.isDead = true
      this.deathCause = '重病不治'
    }
  }

  // 生成抉择点
  generateChoice(age) {
    const choices = [
      {
        age: 12,
        title: '初中选择',
        context: '小升初，你需要做出选择',
        desc: '你面临初中的选择，这将影响你的未来方向。',
        options: [
          { text: '进入重点初中', reason: '更好的师资和学习氛围', effects: [{name: '智力', value: 10}, {name: '快乐', value: -5}] },
          { text: '普通初中', reason: '压力小，全面发展', effects: [{name: '智力', value: 5}, {name: '魅力', value: 5}, {name: '快乐', value: 5}] },
          { text: '艺术/体育特长班', reason: '发挥特长优势', effects: [{name: '魅力', value: 10}, {name: '智力', value: 3}] }
        ]
      },
      {
        age: 15,
        title: '高中抉择',
        context: '中考结束，选择未来方向',
        desc: '中考成绩出来了，你需要决定下一步。',
        options: [
          { text: '重点高中', reason: '冲击名牌大学', effects: [{name: '智力', value: 15}, {name: '健康', value: -5}, {name: '快乐', value: -5}] },
          { text: '普通高中', reason: '轻松学习，发展兴趣', effects: [{name: '智力', value: 5}, {name: '快乐', value: 10}] },
          { text: '职业学校', reason: '学一门实用技术', effects: [{name: '财富', value: 5}, {name: '快乐', value: 5}] },
          { text: '出国留学', reason: '开阔国际视野', effects: [{name: '智力', value: 10}, {name: '魅力', value: 10}, {name: '财富', value: -15}] }
        ]
      },
      {
        age: 18,
        title: '人生大考',
        context: '高考结束，成绩揭晓',
        desc: '高考成绩决定了你下一步的方向。',
        options: [
          { text: '985/211大学', reason: '继续深造，提升学历', effects: [{name: '智力', value: 20}, {name: '财富', value: -5}] },
          { text: '普通大学', reason: '安稳度过大学时光', effects: [{name: '智力', value: 10}, {name: '快乐', value: 5}] },
          { text: '直接就业', reason: '早点赚钱积累经验', effects: [{name: '财富', value: 10}, {name: '快乐', value: -3}] },
          { text: '复读一年', reason: '争取更好的成绩', effects: [{name: '智力', value: 15}, {name: '快乐', value: -10}] }
        ]
      },
      {
        age: 22,
        title: '毕业选择',
        context: '大学毕业，站在十字路口',
        desc: '你拿到了毕业证书，接下来该何去何从？',
        options: [
          { text: '考研深造', reason: '提升学历，增加竞争力', effects: [{name: '智力', value: 15}, {name: '财富', value: -10}] },
          { text: '进入大厂', reason: '高薪工作，快速积累', effects: [{name: '财富', value: 15}, {name: '健康', value: -5}] },
          { text: '考公务员', reason: '稳定工作，福利好', effects: [{name: '快乐', value: 10}, {name: '财富', value: 5}] },
          { text: '自主创业', reason: '追逐梦想，自己当老板', effects: [{name: '财富', value: -15}, {name: '智力', value: 10}, {name: '快乐', value: 10}] },
          { text: '出国留学', reason: '继续深造，开阔眼界', effects: [{name: '智力', value: 15}, {name: '魅力', value: 10}, {name: '财富', value: -20}] }
        ]
      },
      {
        age: 25,
        title: '感情抉择',
        context: '遇到了心动的人',
        desc: '你遇到了一个特别的人，你会怎么选择？',
        options: [
          { text: '勇敢追求', reason: '爱情需要勇气', effects: [{name: '快乐', value: 20}, {name: '魅力', value: 5}] },
          { text: '专注事业', reason: '先立业再成家', effects: [{name: '财富', value: 10}, {name: '快乐', value: -5}] },
          { text: '保持暧昧', reason: '享受当下的感觉', effects: [{name: '快乐', value: 5}] },
          { text: '理性拒绝', reason: '觉得不合适', effects: [{name: '快乐', value: -5}, {name: '智力', value: 3}] }
        ]
      },
      {
        age: 28,
        title: '事业转折',
        context: '工作遇到瓶颈',
        desc: '你在工作中遇到了瓶颈，需要做出改变。',
        options: [
          { text: '跳槽加薪', reason: '换个环境，获得更高薪资', effects: [{name: '财富', value: 15}, {name: '快乐', value: 5}] },
          { text: '辞职创业', reason: '自己当老板，追逐梦想', effects: [{name: '财富', value: -20}, {name: '智力', value: 10}, {name: '快乐', value: 15}] },
          { text: '坚守岗位', reason: '等待机会，稳步发展', effects: [{name: '财富', value: 5}, {name: '快乐', value: -5}] },
          { text: '转行发展', reason: '寻找更适合自己的方向', effects: [{name: '快乐', value: 10}, {name: '财富', value: -5}] }
        ]
      },
      {
        age: 30,
        title: '成家立业',
        context: '到了成家的年纪',
        desc: '周围的朋友都结婚了，你需要做出选择。',
        options: [
          { text: '结婚成家', reason: '组建自己的家庭', effects: [{name: '快乐', value: 15}, {name: '财富', value: -10}] },
          { text: '继续单身', reason: '享受自由的生活', effects: [{name: '快乐', value: 5}, {name: '财富', value: 5}] },
          { text: '先买房', reason: '有了房子再结婚', effects: [{name: '财富', value: -20}, {name: '快乐', value: 5}] }
        ]
      },
      {
        age: 35,
        title: '中年危机',
        context: '人生进入下半场',
        desc: '35岁了，你开始思考人生的意义。',
        options: [
          { text: '追求梦想', reason: '做真正想做的事', effects: [{name: '快乐', value: 20}, {name: '财富', value: -15}] },
          { text: '稳扎稳打', reason: '继续当前的生活', effects: [{name: '财富', value: 10}, {name: '快乐', value: -5}] },
          { text: '回归家庭', reason: '多陪伴家人', effects: [{name: '快乐', value: 15}, {name: '财富', value: -5}] }
        ]
      },
      {
        age: 40,
        title: '不惑之年',
        context: '40岁的人生反思',
        desc: '40岁了，你对人生有了更深的理解。',
        options: [
          { text: '继续奋斗', reason: '人生还长，继续拼搏', effects: [{name: '财富', value: 10}, {name: '健康', value: -5}] },
          { text: '享受生活', reason: '工作不是全部', effects: [{name: '快乐', value: 15}, {name: '健康', value: 5}] },
          { text: '回馈社会', reason: '帮助他人，实现价值', effects: [{name: '快乐', value: 20}, {name: '魅力', value: 10}] }
        ]
      },
      {
        age: 50,
        title: '知天命',
        context: '人生过半',
        desc: '50岁了，你开始规划退休生活。',
        options: [
          { text: '提前退休', reason: '享受生活，四处旅行', effects: [{name: '快乐', value: 15}, {name: '健康', value: 5}, {name: '财富', value: -10}] },
          { text: '继续工作', reason: '发挥余热，保持活力', effects: [{name: '财富', value: 10}, {name: '快乐', value: -3}] },
          { text: '培养爱好', reason: '发展兴趣，丰富生活', effects: [{name: '快乐', value: 15}, {name: '魅力', value: 5}] }
        ]
      }
    ]

    return choices.find(c => c.age === age)
  }

  // 生成预测
  generatePrediction() {
    const predictions = []
    const age = this.age
    const stats = this.stats
    const traits = this.profile.traits || []

    if (stats.health.value < 40) {
      predictions.push('健康预警：你的健康状况堪忧，建议加强锻炼和定期体检。')
    }
    if (stats.wealth.value < 30 && age > 30) {
      predictions.push('财务风险：你的财富积累不足，建议制定理财计划。')
    }
    if (stats.intelligence.value > 80 && age < 25) {
      predictions.push('学业前景：你的智力超群，适合继续深造或从事研究工作。')
    }
    if (stats.charm.value > 70 && !this.relations['伴侣']) {
      predictions.push('感情运势：你的魅力出众，近期可能遇到心仪的对象。')
    }
    if (stats.happiness.value < 30) {
      predictions.push('心理预警：你的快乐指数偏低，建议调整心态或寻求改变。')
    }
    if (traits.includes('冒险') && stats.wealth.value > 50) {
      predictions.push('投资建议：你的冒险精神和财富积累适合尝试创业或投资。')
    }
    if (age > 50 && stats.health.value > 70) {
      predictions.push('长寿潜力：你的健康状况良好，有望享受长寿人生。')
    }
    if (predictions.length === 0) {
      predictions.push('人生平稳：你目前的人生轨迹平稳，继续保持当前状态。')
    }

    return predictions.join('\n')
  }

  // 生成墓志铭
  generateEpitaph() {
    const epitaphs = [
      '这里躺着一个人，他/她来过，爱过，奋斗过。',
      '一生平凡，但从未放弃追求幸福。',
      '他/她用自己的方式，书写了独特的人生。',
      '愿来生，依然勇敢，依然热爱。',
      '人生如梦，他/她做了一个好梦。',
      '他/她的一生，是对生命最好的诠释。',
      '来时一无所有，走时满载回忆。'
    ]
    return epitaphs[Math.floor(Math.random() * epitaphs.length)]
  }
}

export default {
  data() {
    return {
      gameStarted: false,
      showHistory: false,
      showCustomCreator: false,
      showWhatIf: false,
      showChangeChoice: false,
      showLifeDetail: false,
      showPrediction: false,
      showRelations: false,
      currentPrediction: '',
      currentAge: 0,
      currentYear: 2000,
      isDead: false,
      deathCause: '',
      isAutoPlaying: false,
      autoPlayTimer: null,
      currentChoice: null,
      playerName: '',
      totalScore: 0,
      scoreRank: '',
      lifeAchievement: '',
      lifeTags: [],
      finalEmoji: '',
      historyFilter: 'all',
      selectedLife: {},
      changeAge: 0,
      originalChoiceText: '',
      alternativeChoices: [],
      yearIndex: 20,
      yearOptions: Array.from({length: 50}, (_, i) => (1975 + i) + '年'),
      
      customProfile: {
        name: '',
        birthYear: 2000,
        birthPlace: '',
        family: '普通家庭',
        traits: [],
        goal: '平衡发展',
        startEvent: ''
      },
      
      familyTags: ['富裕家庭', '知识分子', '商人家庭', '工人家庭', '农村家庭', '单亲家庭', '普通家庭'],
      personalityTraits: ['聪明', '勤奋', '活泼', '内向', '外向', '叛逆', '稳重', '冒险', '浪漫', '理性', '感性', '野心', '佛系', '完美主义', '随和'],
      lifeGoals: ['财富自由', '学术成就', '家庭幸福', '事业成功', '环游世界', '艺术追求', '社会贡献', '平衡发展'],
      
      customStats: {
        health: { name: '健康', emoji: '❤️', value: 50, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: 50, color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: 50, color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: 50, color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: 50, color: '#f6ad55' }
      },
      
      stats: {
        health: { name: '健康', emoji: '❤️', value: 100, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: 50, color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: 50, color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: 50, color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: 50, color: '#f6ad55' }
      },
      relations: {},
      events: [],
      visibleEvents: [],
      lifeHistory: [],
      engine: null,
      isCustom: false
    }
  },
  computed: {
    remainingPoints() {
      const total = Object.values(this.customStats).reduce((sum, s) => sum + s.value, 0)
      return 250 - total
    },
    bestScore() {
      if (this.lifeHistory.length === 0) return 0
      return Math.max(...this.lifeHistory.map(l => l.totalScore))
    },
    avgAge() {
      if (this.lifeHistory.length === 0) return 0
      return Math.round(this.lifeHistory.reduce((sum, l) => sum + l.age, 0) / this.lifeHistory.length)
    },
    totalChoices() {
      return this.lifeHistory.reduce((sum, l) => sum + (l.choiceCount || 0), 0)
    },
    filteredHistory() {
      let list = [...this.lifeHistory]
      if (this.historyFilter === 'high') {
        list = list.filter(l => l.totalScore >= 300)
      } else if (this.historyFilter === 'long') {
        list = list.filter(l => l.age >= 70)
      } else if (this.historyFilter === 'custom') {
        list = list.filter(l => l.isCustom)
      }
      return list
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
    
    // 自定义创建器
    openCustomCreator() {
      this.showCustomCreator = true
      this.customProfile = {
        name: '',
        birthYear: 2000,
        birthPlace: '',
        family: '普通家庭',
        traits: [],
        goal: '平衡发展',
        startEvent: ''
      }
      this.customStats = {
        health: { name: '健康', emoji: '❤️', value: 50, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: 50, color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: 50, color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: 50, color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: 50, color: '#f6ad55' }
      }
    },
    onYearChange(e) {
      this.yearIndex = e.detail.value
      this.customProfile.birthYear = 1975 + parseInt(e.detail.value)
    },
    toggleTrait(trait) {
      const index = this.customProfile.traits.indexOf(trait)
      if (index > -1) {
        this.customProfile.traits.splice(index, 1)
      } else if (this.customProfile.traits.length < 3) {
        this.customProfile.traits.push(trait)
      } else {
        uni.showToast({ title: '最多选择3个', icon: 'none' })
      }
    },
    adjustPoint(key, delta) {
      const newValue = this.customStats[key].value + delta
      if (newValue >= 10 && newValue <= 100 && this.remainingPoints - delta >= 0) {
        this.customStats[key].value = newValue
      }
    },
    startCustomLife() {
      if (!this.customProfile.name) {
        uni.showToast({ title: '请输入姓名', icon: 'none' })
        return
      }
      if (this.customProfile.traits.length === 0) {
        uni.showToast({ title: '请选择至少1个性格特质', icon: 'none' })
        return
      }
      
      this.isCustom = true
      this.showCustomCreator = false
      this.gameStarted = true
      this.currentAge = 0
      this.currentYear = this.customProfile.birthYear
      this.isDead = false
      this.deathCause = ''
      this.currentChoice = null
      this.events = []
      this.visibleEvents = []
      this.relations = {}
      this.isAutoPlaying = false
      this.playerName = this.customProfile.name
      
      // 应用自定义属性
      this.stats = {
        health: { name: '健康', emoji: '❤️', value: this.customStats.health.value, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: this.customStats.intelligence.value, color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: this.customStats.wealth.value, color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: this.customStats.charm.value, color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: this.customStats.happiness.value, color: '#f6ad55' }
      }
      
      // 应用开局事件
      if (this.customProfile.startEvent) {
        this.addEvent({
          age: 0,
          year: this.currentYear,
          title: '📖 开局事件',
          desc: this.customProfile.startEvent,
          type: 'major'
        })
      }
      
      // 创建引擎
      this.engine = new LifeEngine(this.customProfile, this.stats)
      this.engine.year = this.currentYear
      
      this.nextYear()
    },
    
    // 随机人生
    startNewLife() {
      this.isCustom = false
      this.gameStarted = true
      this.showHistory = false
      this.currentAge = 0
      this.currentYear = 2000
      this.isDead = false
      this.deathCause = ''
      this.currentChoice = null
      this.events = []
      this.visibleEvents = []
      this.relations = {}
      this.isAutoPlaying = false
      this.playerName = '无名氏'
      
      const randomName = ['小明', '小红', '阿强', '小丽', '子涵', '梓轩', '浩然', '诗涵'][Math.floor(Math.random() * 8)]
      this.playerName = randomName
      
      this.stats = {
        health: { name: '健康', emoji: '❤️', value: 100, color: '#e53e3e' },
        intelligence: { name: '智力', emoji: '🧠', value: this.randomStat(40, 70), color: '#667eea' },
        wealth: { name: '财富', emoji: '💰', value: this.randomStat(30, 60), color: '#48bb78' },
        charm: { name: '魅力', emoji: '✨', value: this.randomStat(40, 70), color: '#f093fb' },
        happiness: { name: '快乐', emoji: '😊', value: this.randomStat(50, 80), color: '#f6ad55' }
      }
      
      const profile = {
        birthYear: 2000,
        family: '普通家庭',
        traits: [],
        birthPlace: '城市'
      }
      
      this.engine = new LifeEngine(profile, this.stats)
      
      this.addEvent({
        age: 0,
        year: this.currentYear,
        title: '👶 出生',
        desc: `你出生在一个普通家庭。`,
        type: 'major'
      })
      
      this.nextYear()
    },
    
    randomStat(min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },
    
    addEvent(event) {
      this.events.unshift(event)
      this.visibleEvents = [...this.events]
    },
    
    nextYear() {
      if (this.isDead) return
      
      this.currentAge++
      this.currentYear++
      
      if (this.engine) {
        this.engine.age = this.currentAge
        this.engine.year = this.currentYear
      }
      
      // 检查抉择点
      const choice = this.engine ? this.engine.generateChoice(this.currentAge) : null
      if (choice) {
        this.currentChoice = choice
        return
      }
      
      // 生成事件
      if (this.engine) {
        const newEvents = this.engine.generateEvent(this.currentAge)
        newEvents.forEach(event => {
          if (event.effects) {
            event.effects.forEach(effect => this.changeStat(effect.name, effect.value))
          }
          if (event.relations) {
            event.relations.forEach(rel => {
              this.relations[rel.name] = { emoji: rel.emoji, value: rel.value }
            })
          }
          this.addEvent(event)
        })
        
        if (this.engine.isDead) {
          this.isDead = true
          this.deathCause = this.engine.deathCause
          this.stopAutoPlay()
          this.calculateResult()
        }
      }
      
      // 自然变化
      this.naturalChanges()
      
      // 再次检查死亡
      if (!this.isDead) {
        this.checkDeath()
      }
    },
    
    makeChoice(option) {
      option.effects.forEach(effect => {
        this.changeStat(effect.name, effect.value)
      })
      
      this.addEvent({
        age: this.currentAge,
        year: this.currentYear,
        title: `🎯 ${this.currentChoice.title}`,
        desc: `你选择了：${option.text}。${option.reason}`,
        type: 'choice',
        effects: option.effects
      })
      
      this.currentChoice = null
      
      setTimeout(() => {
        if (!this.isDead) this.nextYear()
      }, 500)
    },
    
    naturalChanges() {
      if (this.currentAge > 40) this.changeStat('健康', -1)
      if (this.currentAge > 60) this.changeStat('健康', -2)
      if (this.currentAge > 80) this.changeStat('健康', -3)
      
      if (this.currentAge >= 22 && this.currentAge < 60) {
        this.changeStat('财富', Math.floor(Math.random() * 3) + 1)
      }
      if (this.currentAge >= 60) {
        this.changeStat('财富', -Math.floor(Math.random() * 2))
      }
    },
    
    changeStat(name, value) {
      const map = { '健康': 'health', '智力': 'intelligence', '财富': 'wealth', '魅力': 'charm', '快乐': 'happiness' }
      const key = map[name]
      if (key && this.stats[key]) {
        this.stats[key].value = Math.max(0, Math.min(100, this.stats[key].value + value))
      }
    },
    
    checkDeath() {
      if (this.stats.health.value <= 0) {
        this.isDead = true
        this.deathCause = '因病去世'
      } else if (this.currentAge >= 100) {
        this.isDead = true
        this.deathCause = '寿终正寝'
      } else if (this.currentAge >= 90 && Math.random() < 0.2) {
        this.isDead = true
        this.deathCause = '安详离世'
      } else if (this.currentAge >= 75 && Math.random() < 0.08) {
        this.isDead = true
        this.deathCause = '突发疾病'
      }
      
      if (this.isDead) {
        this.stopAutoPlay()
        this.calculateResult()
      }
    },
    
    generatePrediction() {
      if (this.engine) {
        this.currentPrediction = this.engine.generatePrediction()
        this.showPrediction = true
        setTimeout(() => {
          uni.createSelectorQuery().select('.prediction-panel').boundingClientRect(rect => {
            if (rect) {
              uni.pageScrollTo({ scrollTop: rect.top + 500, duration: 300 })
            }
          }).exec()
        }, 100)
      }
    },
    
    calculateResult() {
      let score = 0
      Object.values(this.stats).forEach(stat => {
        score += stat.value
      })
      score += this.currentAge
      this.totalScore = score
      
      if (score >= 450) this.scoreRank = 'S - 传奇人生'
      else if (score >= 380) this.scoreRank = 'A - 精彩人生'
      else if (score >= 320) this.scoreRank = 'B - 不错的人生'
      else if (score >= 260) this.scoreRank = 'C - 普通人生'
      else if (score >= 200) this.scoreRank = 'D - 坎坷人生'
      else this.scoreRank = 'E - 艰难人生'
      
      // 判定成就
      const achievements = [
        { condition: (s) => s.intelligence.value >= 90, text: '博学多才的智者', tags: ['学霸', '知识分子'] },
        { condition: (s) => s.wealth.value >= 90, text: '富可敌国的富豪', tags: ['富豪', '成功人士'] },
        { condition: (s) => s.charm.value >= 90, text: '万人迷的魅力之星', tags: ['明星', '魅力'] },
        { condition: (s) => s.happiness.value >= 90, text: '幸福满满的人生赢家', tags: ['幸福', '快乐'] },
        { condition: (s) => s.health.value >= 90, text: '健康长寿的百岁老人', tags: ['健康', '长寿'] },
        { condition: (s) => s.intelligence.value >= 70 && s.wealth.value >= 70, text: '智慧与财富并存的精英', tags: ['精英', '成功人士'] },
        { condition: (s) => s.happiness.value >= 70 && s.wealth.value < 50, text: '知足常乐的快乐人', tags: ['平凡', '快乐'] },
        { condition: (s) => s.wealth.value >= 80 && s.happiness.value < 40, text: '孤独的成功者', tags: ['富豪', '孤独'] },
        { condition: (s) => Object.values(s).every(v => v.value >= 60), text: '全面发展的完美人生', tags: ['完美', '平衡'] },
        { condition: (s) => s.health.value < 30, text: '体弱多病但坚强的一生', tags: ['坎坷', '坚强'] },
        { condition: () => true, text: '平凡而真实的人生', tags: ['平凡', '真实'] }
      ]
      
      for (let ach of achievements) {
        if (ach.condition(this.stats)) {
          this.lifeAchievement = ach.text
          this.lifeTags = ach.tags
          break
        }
      }
      
      if (this.stats.happiness.value >= 80) this.finalEmoji = '😄'
      else if (this.stats.happiness.value >= 60) this.finalEmoji = '🙂'
      else if (this.stats.happiness.value >= 40) this.finalEmoji = '😐'
      else this.finalEmoji = '😢'
      
      const choiceCount = this.events.filter(e => e.type === 'choice').length
      
      const lifeRecord = {
        name: this.playerName,
        age: this.currentAge,
        totalScore: score,
        achievement: this.lifeAchievement,
        tags: this.lifeTags,
        finalEmoji: this.finalEmoji,
        stats: JSON.parse(JSON.stringify(this.stats)),
        events: this.events.slice(0, 30),
        date: new Date().toLocaleDateString(),
        birthYear: this.isCustom ? this.customProfile.birthYear : 2000,
        deathYear: this.currentYear,
        birthPlace: this.isCustom ? this.customProfile.birthPlace : '城市',
        family: this.isCustom ? this.customProfile.family : '普通家庭',
        isCustom: this.isCustom,
        choiceCount: choiceCount
      }
      this.lifeHistory.unshift(lifeRecord)
      this.saveHistory()
    },
    
    generateEpitaph() {
      if (this.engine) {
        return this.engine.generateEpitaph()
      }
      return '这里躺着一个人，他/她来过，爱过，奋斗过。'
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
        }, 600)
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
      this.showPrediction = false
      this.gameStarted = false
      this.isDead = false
    },
    
    shareLife() {
      const shareText = `我在【平行人生推演器】中体验了${this.playerName}的${this.currentAge}岁人生，获得了${this.totalScore}分！\n最终成就：${this.lifeAchievement}\n"${this.generateEpitaph()}"`
      uni.showModal({
        title: '分享人生',
        content: shareText,
        showCancel: false
      })
    },
    
    // 如果当初
    openWhatIf() {
      this.showWhatIf = true
    },
    
    loadLifeForWhatIf(life) {
      uni.showToast({ title: '功能开发中', icon: 'none' })
    },
    
    startWhatIfFromHere() {
      uni.showToast({ title: '功能开发中', icon: 'none' })
    },
    
    // 详情
    viewLifeDetail(life) {
      this.selectedLife = life
      this.showLifeDetail = true
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

.mode-custom {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
}

.mode-whatif {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
}

.mode-history {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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

/* 自定义创建器 */
.creator-section {
  animation: fadeIn 0.3s ease;
}

.creator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.creator-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.creator-back {
  font-size: 26rpx;
  color: #667eea;
}

.creator-form {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

.form-section {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.form-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.form-subtitle {
  font-size: 24rpx;
  color: #667eea;
  display: block;
  margin-bottom: 16rpx;
}

.form-item {
  margin-bottom: 20rpx;
}

.form-label {
  font-size: 26rpx;
  color: #4a5568;
  display: block;
  margin-bottom: 10rpx;
}

.form-input {
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
}

.form-picker {
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
}

.form-textarea {
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
  width: 100%;
  min-height: 160rpx;
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.select-tag {
  background: #f7fafc;
  padding: 12rpx 24rpx;
  border-radius: 24rpx;
  font-size: 24rpx;
  color: #718096;
  transition: all 0.3s;
}

.select-tag-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.point-allocation {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.point-item {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
}

.point-emoji {
  font-size: 36rpx;
  margin-right: 12rpx;
}

.point-name {
  font-size: 26rpx;
  color: #2d3748;
  width: 100rpx;
}

.point-control {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-left: auto;
}

.point-btn {
  width: 48rpx;
  height: 48rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 48rpx;
  font-size: 32rpx;
}

.point-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #667eea;
  width: 60rpx;
  text-align: center;
}

.start-custom-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 30rpx;
  font-size: 32rpx;
  border: none;
  margin-top: 20rpx;
}

/* WhatIf */
.whatif-section {
  animation: fadeIn 0.3s ease;
}

.whatif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.whatif-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.whatif-back {
  font-size: 26rpx;
  color: #667eea;
}

.whatif-desc {
  font-size: 26rpx;
  color: #718096;
  margin-bottom: 20rpx;
}

.whatif-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.whatif-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.whatif-emoji {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.whatif-info {
  flex: 1;
}

.whatif-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
}

.whatif-summary {
  font-size: 22rpx;
  color: #a0aec0;
}

.whatif-score {
  font-size: 32rpx;
  font-weight: bold;
  color: #f6ad55;
}

.empty-whatif {
  text-align: center;
  padding: 100rpx 40rpx;
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
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.player-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.player-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.age-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16rpx;
  padding: 12rpx 20rpx;
  text-align: center;
  display: flex;
  align-items: baseline;
}

.age-num {
  font-size: 36rpx;
  font-weight: bold;
  color: #fff;
}

.age-label {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-left: 4rpx;
}

.year-progress {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.progress-bar {
  flex: 1;
  height: 16rpx;
  background: #edf2f7;
  border-radius: 8rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 8rpx;
  transition: width 0.5s ease;
}

.progress-text {
  font-size: 24rpx;
  color: #a0aec0;
  width: 120rpx;
  text-align: right;
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

.stat-box-low {
  background: rgba(229, 62, 62, 0.05);
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

/* 关系面板 */
.relations-panel {
  background: #fff;
  border-radius: 20rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.relations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.relations-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
}

.relations-toggle {
  font-size: 24rpx;
  color: #667eea;
}

.relations-list {
  margin-top: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.relation-item {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 12rpx 16rpx;
}

.relation-emoji {
  font-size: 32rpx;
  margin-right: 12rpx;
}

.relation-name {
  font-size: 26rpx;
  color: #2d3748;
  width: 120rpx;
}

.relation-bar {
  flex: 1;
  height: 8rpx;
  background: #edf2f7;
  border-radius: 4rpx;
  overflow: hidden;
  margin-right: 12rpx;
}

.relation-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4rpx;
}

.relation-value {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
  width: 50rpx;
  text-align: right;
}

/* 事件时间线 */
.events-timeline {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.timeline-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
}

.timeline-count {
  font-size: 24rpx;
  color: #a0aec0;
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

.event-relation .event-dot {
  background: #f093fb;
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

.event-relations {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
  margin-top: 8rpx;
}

.rel-change {
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
  background: rgba(240, 147, 251, 0.1);
  color: #f093fb;
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

.choice-info {
  flex: 1;
}

.choice-title {
  font-size: 32rpx;
  font-weight: bold;
  display: block;
}

.choice-context {
  font-size: 24rpx;
  opacity: 0.9;
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
  margin-bottom: 4rpx;
}

.option-reason {
  font-size: 22rpx;
  color: #718096;
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

/* 预测面板 */
.prediction-panel {
  margin-bottom: 20rpx;
}

.prediction-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 20rpx;
  padding: 30rpx;
  color: #fff;
}

.prediction-title {
  font-size: 28rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 12rpx;
}

.prediction-text {
  font-size: 26rpx;
  line-height: 1.6;
  opacity: 0.95;
}

/* 操作区域 */
.action-area {
  display: flex;
  gap: 12rpx;
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
  width: 140rpx;
  background: #f7fafc;
  color: #667eea;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 26rpx;
  border: none;
}

.predict-btn {
  width: 140rpx;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 26rpx;
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

.death-name {
  font-size: 32rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 4rpx;
}

.death-years {
  font-size: 24rpx;
  opacity: 0.7;
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
  text-align: left;
}

.summary-title {
  font-size: 28rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 16rpx;
  text-align: center;
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
  text-align: center;
}

.s-stat-emoji {
  font-size: 32rpx;
  display: block;
  margin-bottom: 4rpx;
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

.life-traits {
  margin-bottom: 16rpx;
}

.traits-title {
  font-size: 24rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 8rpx;
  text-align: center;
}

.traits-list {
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

.life-achievement {
  margin-bottom: 16rpx;
  text-align: center;
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

.life-epitaph {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12rpx;
  padding: 20rpx;
  text-align: center;
}

.epitaph-mark {
  font-size: 40rpx;
  color: rgba(255, 255, 255, 0.3);
  display: block;
}

.epitaph-text {
  font-size: 26rpx;
  font-style: italic;
  opacity: 0.8;
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
  gap: 16rpx;
}

.restart-btn {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 26rpx;
  border: none;
}

.whatif-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 26rpx;
  border: none;
}

.share-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 26rpx;
  border: none;
}

/* 历史记录 */
.history-section {
  animation: fadeIn 0.3s ease;
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
  gap: 12rpx;
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

.history-filter {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.filter-label {
  font-size: 26rpx;
  color: #718096;
}

.filter-scroll {
  flex: 1;
  white-space: nowrap;
}

.filter-tag {
  display: inline-block;
  padding: 10rpx 24rpx;
  background: #fff;
  border-radius: 24rpx;
  font-size: 24rpx;
  color: #718096;
  margin-right: 12rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.filter-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
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

.history-mid {
  margin-bottom: 12rpx;
}

.history-achievement {
  font-size: 26rpx;
  color: #667eea;
}

.history-tags {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.h-tag {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

.h-tag-custom {
  background: rgba(240, 147, 251, 0.1);
  color: #f093fb;
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

/* 详情弹窗 */
.life-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
}

.modal-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  border-radius: 40rpx 40rpx 0 0;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f0f0f0;
}

.modal-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.modal-close {
  font-size: 32rpx;
  color: #a0aec0;
  padding: 10rpx;
}

.modal-body {
  flex: 1;
  padding: 30rpx;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 30rpx;
}

.detail-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 12rpx;
}

.detail-text {
  font-size: 26rpx;
  color: #4a5568;
  display: block;
  margin-bottom: 8rpx;
}

.detail-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.d-stat {
  width: calc(50% - 8rpx);
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 16rpx;
  text-align: center;
}

.d-stat-emoji {
  font-size: 32rpx;
  display: block;
  margin-bottom: 4rpx;
}

.d-stat-name {
  font-size: 22rpx;
  color: #718096;
}

.d-stat-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
  margin-top: 4rpx;
}

.detail-events {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.d-event {
  display: flex;
  align-items: center;
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 16rpx;
}

.d-event-age {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
  width: 80rpx;
  flex-shrink: 0;
}

.d-event-title {
  font-size: 26rpx;
  color: #4a5568;
}

.bottom-space {
  height: 40rpx;
}
</style>
