<template>
  <view class="container">
    <!-- 顶部 -->
    <view class="header">
      <text class="header-title">🦋 蝴蝶效应推演</text>
      <text class="header-desc">基于知识推理，推演事件的各种可能</text>
    </view>

    <!-- 输入区域 -->
    <view class="input-section" v-if="!showingResult">
      <view class="input-card">
        <text class="input-label">📖 描述你的情况</text>
        <textarea 
          class="input-textarea" 
          v-model="userEvent"
          placeholder="详细描述一件正在发生或即将发生的事情...&#10;例如：我在互联网公司做产品经理3年了，最近直属领导离职，公司让我接替他带团队，但我没有管理经验，不确定要不要接受"
          maxlength="300"
        />
        <text class="input-hint">描述越详细，推理越精准（建议包含背景、人物、时间、你的顾虑）</text>
      </view>

      <view class="input-card">
        <text class="input-label">🎯 你倾向的选择（可选）</text>
        <input 
          class="input-field" 
          v-model="userChoice"
          placeholder="例如：我想接受但担心做不好"
        />
      </view>

      <view class="input-card">
        <text class="input-label">📊 推演深度</text>
        <view class="depth-selector">
          <view 
            class="depth-option" 
            v-for="(d, index) in depthOptions" 
            :key="index"
            :class="{'depth-active': depth === d.value}"
            @click="depth = d.value"
          >
            <text class="depth-name">{{d.name}}</text>
            <text class="depth-desc">{{d.desc}}</text>
          </view>
        </view>
      </view>

      <button class="predict-btn" @click="startPrediction" :disabled="!userEvent.trim() || isPredicting">
        <text class="btn-text">{{isPredicting ? '🔮 正在推演...' : '🔮 开始推演'}}</text>
      </button>

      <!-- 历史记录 -->
      <view class="history-entry" @click="showHistory = true">
        <text class="history-icon">📚</text>
        <text class="history-text">推演历史 ({{predictionHistory.length}})</text>
      </view>
    </view>

    <!-- 推演结果 -->
    <view class="result-section" v-if="showingResult">
      <!-- 原始事件 -->
      <view class="original-event">
        <text class="original-label">📖 原始事件</text>
        <text class="original-text">{{userEvent}}</text>
        <text class="original-choice" v-if="userChoice">你的倾向：{{userChoice}}</text>
      </view>

      <!-- 推理过程 -->
      <view class="reasoning-process" v-if="reasoningSteps.length > 0">
        <text class="process-title">🧠 推理过程</text>
        <view class="process-steps">
          <view class="process-step" v-for="(step, index) in reasoningSteps" :key="index">
            <view class="step-num">{{index + 1}}</view>
            <view class="step-content">
              <text class="step-title">{{step.title}}</text>
              <text class="step-desc">{{step.desc}}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 维度分析 -->
      <view class="dimension-analysis" v-if="dimensions.length > 0">
        <text class="dim-title">📊 多维度分析</text>
        <view class="dim-list">
          <view class="dim-item" v-for="(dim, index) in dimensions" :key="index">
            <view class="dim-header">
              <text class="dim-emoji">{{dim.emoji}}</text>
              <text class="dim-name">{{dim.name}}</text>
              <view class="dim-score" :class="{'dim-high': dim.score >= 7, 'dim-mid': dim.score >= 4 && dim.score < 7, 'dim-low': dim.score < 4}">
                <text class="ds-num">{{dim.score}}</text>
                <text class="ds-total">/10</text>
              </view>
            </view>
            <text class="dim-analysis">{{dim.analysis}}</text>
          </view>
        </view>
      </view>

      <!-- 分支树 -->
      <view class="branch-tree">
        <text class="tree-title">🌳 推演结果</text>
        <text class="tree-subtitle">点击分支查看后续推演</text>
        
        <view class="branch-level" v-for="(level, levelIndex) in branchTree" :key="levelIndex">
          <text class="level-label">{{levelNames[levelIndex] || ('第' + (levelIndex + 1) + '层')}}</text>
          <view class="level-branches">
            <view 
              class="branch-node" 
              v-for="(branch, branchIndex) in level" 
              :key="branchIndex"
              :class="{'branch-selected': branch.selected, 'branch-faded': branch.faded}"
              @click="selectBranch(branch, levelIndex, branchIndex)"
            >
              <view class="node-header">
                <text class="node-probability" :class="{'p-high': branch.probability >= 40, 'p-mid': branch.probability >= 20, 'p-low': branch.probability < 20}">{{branch.probability}}%</text>
                <text class="node-emoji">{{branch.emoji}}</text>
              </view>
              <text class="node-title">{{branch.title}}</text>
              <text class="node-desc">{{branch.desc}}</text>
              <view class="node-reasoning" v-if="branch.reasoning">
                <text class="nr-label">推理依据：</text>
                <text class="nr-text">{{branch.reasoning}}</text>
              </view>
              <view class="node-effects" v-if="branch.effects">
                <text class="ne-tag" v-for="(eff, i) in branch.effects" :key="i" :class="{'ne-positive': eff.value > 0, 'ne-negative': eff.value < 0}">
                  {{eff.emoji}} {{eff.name}} {{eff.value > 0 ? '+' : ''}}{{eff.value}}
                </text>
              </view>
              <view class="node-continue" v-if="branch.canContinue && !branch.faded">
                <text class="continue-text">点击深入推演 →</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 推演路径 -->
      <view class="timeline-view" v-if="selectedPath.length > 0">
        <text class="timeline-title">⏱️ 你的推演路径</text>
        <view class="timeline-path">
          <view class="path-item" v-for="(item, index) in selectedPath" :key="index">
            <view class="path-dot">{{index + 1}}</view>
            <view class="path-content">
              <text class="path-title">{{item.title}}</text>
              <text class="path-desc">{{item.desc}}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 总结 -->
      <view class="summary-card" v-if="finalSummary">
        <text class="summary-title">📋 推演总结</text>
        <text class="summary-text">{{finalSummary}}</text>
        <view class="summary-advice" v-if="finalAdvice">
          <text class="advice-label">💡 建议</text>
          <text class="advice-text">{{finalAdvice}}</text>
        </view>
      </view>

      <!-- 操作 -->
      <view class="result-actions">
        <button class="action-btn btn-continue" @click="continuePrediction" v-if="canContinue">
          <text class="btn-text">继续推演</text>
        </button>
        <button class="action-btn btn-restart" @click="resetPrediction">
          <text class="btn-text">重新推演</text>
        </button>
        <button class="action-btn btn-share" @click="shareResult">
          <text class="btn-text">分享</text>
        </button>
      </view>
    </view>

    <!-- 历史 -->
    <view class="history-section" v-if="showHistory">
      <view class="history-header">
        <text class="history-title">📚 推演历史</text>
        <text class="history-back" @click="showHistory = false">返回</text>
      </view>
      <view class="history-list" v-if="predictionHistory.length > 0">
        <view class="history-card" v-for="(item, index) in predictionHistory" :key="index" @click="loadHistory(item)">
          <text class="history-event">{{item.event}}</text>
          <text class="history-date">{{item.date}}</text>
          <view class="history-branches-preview">
            <text class="hb-tag" v-for="(b, i) in item.branches.slice(0, 3)" :key="i">{{b.title}}</text>
          </view>
        </view>
      </view>
      <view class="empty-history" v-else>
        <text class="empty-icon">📝</text>
        <text class="empty-text">还没有推演记录</text>
      </view>
    </view>

    <view class="bottom-space"></view>
  </view>
</template>

<script>
// ============================================
// 专业知识推理引擎
// ============================================
class ReasoningEngine {
  constructor() {
    this.knowledgeBase = this.buildKnowledgeBase()
  }

  // 构建知识库
  buildKnowledgeBase() {
    return {
      // 职场领域
      career: {
        keywords: ['工作', '上班', '公司', '老板', '同事', '职场', '加班', '辞职', '面试', '薪资', '升职', '领导', '团队', '管理', '项目', '业绩', 'KPI', '裁员', '跳槽', '离职'],
        dimensions: ['职业发展', '能力提升', '收入影响', '工作强度', '人际关系', '行业趋势'],
        
        // 调岗场景
        transfer: {
          trigger: ['调岗', '调动', '转岗', '换部门', '岗位调整', '转去'],
          reasoning: (input) => {
            const steps = []
            
            // 分析公司意图
            if (input.includes('领导') || input.includes('老板')) {
              steps.push({
                title: '分析公司意图',
                desc: '直属领导主动提出调岗，通常意味着：1）新岗位确实需要人 2）公司认可你的能力 3）可能是培养你的信号。但也要注意是否是"明升暗降"。'
              })
            }
            
            // 分析个人匹配度
            if (input.includes('没有经验') || input.includes('没做过') || input.includes('不懂')) {
              steps.push({
                title: '评估能力匹配度',
                desc: '没有直接经验不等于不能胜任。关键看：1） transferable skills（可迁移技能）如沟通、逻辑 2）学习能力 3）公司是否提供培训。很多管理者都是"先上岗后学习"。'
              })
            }
            
            // 行业规律
            steps.push({
              title: '参考行业规律',
              desc: '在互联网行业，3年产品经理转管理是常见路径。带团队经验对长期职业发展至关重要，但前6个月通常会很痛苦（管理成本>产出）。'
            })
            
            return steps
          },
          
          dimensions: (input) => {
            const dims = []
            
            // 职业发展
            dims.push({
              emoji: '📈', name: '职业发展', score: 8,
              analysis: '管理岗是产品职业路径的重要分支。带过团队后，未来可走的路更宽（总监/VP/创业）。不带团队，天花板通常是高级产品经理。'
            })
            
            // 能力提升
            const hasExp = !input.includes('没有经验') && !input.includes('没做过')
            dims.push({
              emoji: '📚', name: '能力提升', score: hasExp ? 7 : 5,
              analysis: hasExp 
                ? '管理能力（沟通、协调、决策）是核心软实力，比专业技能更难被替代。'
                : '前3-6个月会很痛苦，需要快速学习管理技能（OKR制定、1on1沟通、冲突解决）。'
            })
            
            // 收入影响
            dims.push({
              emoji: '💰', name: '收入影响', score: 7,
              analysis: '管理岗通常有更高base + 团队奖金。但管理岗的绩效与团队绑定，收入波动可能更大。'
            })
            
            // 工作强度
            dims.push({
              emoji: '⚡', name: '工作强度', score: 4,
              analysis: '管理岗工作时间更长（会议多、突发多），但时间自主权更大。前6个月加班是常态。'
            })
            
            // 人际关系
            dims.push({
              emoji: '🤝', name: '人际关系', score: 5,
              analysis: '从"平级"变"上级"，原有同事关系会改变。需要重新建立信任，可能面临老同事的抵触。'
            })
            
            // 行业趋势
            dims.push({
              emoji: '📊', name: '行业趋势', score: 6,
              analysis: '当前互联网行业"去中层化"趋势明显，但基层管理者（5-15人团队）仍然稀缺。纯执行岗反而更容易被优化。'
            })
            
            return dims
          },
          
          branches: (input) => {
            const branches = []
            
            branches.push({
              emoji: '📈', title: '接受并快速适应', 
              desc: '你接受了挑战，前3个月很痛苦，但半年后渐入佳境。一年后你成为了合格的管理者。',
              probability: 30,
              reasoning: '根据行业数据，约30%的技术转管理者能在1年内适应。关键是前3个月能否撑过"管理黑洞期"。',
              effects: [{emoji: '📈', name: '职业', value: 25}, {emoji: '💰', name: '收入', value: 20}, {emoji: '😰', name: '压力', value: 15}]
            })
            
            branches.push({
              emoji: '😰', title: '接受但难以适应',
              desc: '你接受了，但管理工作让你身心俱疲。1年后你申请转回执行岗，但发现回不去了。',
              probability: 25,
              reasoning: '约25%的人不适合管理岗（缺乏同理心/不喜欢冲突/享受独处工作）。强行做管理会导致职业倦怠。',
              effects: [{emoji: '📉', name: '职业', value: -10}, {emoji: '😰', name: '压力', value: 25}, {emoji: '💔', name: '自信', value: -15}]
            })
            
            branches.push({
              emoji: '🤝', title: '接受+找导师',
              desc: '你接受了，但主动找了公司内一位资深管理者做导师。在指导下你少走了很多弯路。',
              probability: 20,
              reasoning: '有导师指导的新管理者，适应速度提升50%（哈佛商业评论数据）。这是最优策略之一。',
              effects: [{emoji: '📈', name: '职业', value: 30}, {emoji: '🤝', name: '人脉', value: 20}, {emoji: '📚', name: '能力', value: 25}]
            })
            
            branches.push({
              emoji: '🚪', title: '拒绝并跳槽',
              desc: '你拒绝了调岗，觉得不适合管理。半年后你跳槽到另一家公司做高级产品经理，薪资涨了30%。',
              probability: 15,
              reasoning: '如果明确知道自己不适合管理，及时拒绝是理性的。但需确保市场上有更好的执行岗机会。',
              effects: [{emoji: '💰', name: '收入', value: 15}, {emoji: '📈', name: '职业', value: 10}, {emoji: '😊', name: '心情', value: 10}]
            })
            
            branches.push({
              emoji: '💡', title: '谈判条件后接受',
              desc: '你提出需要管理培训+过渡期+薪资调整，公司同意了。这为你后续成功奠定了基础。',
              probability: 10,
              reasoning: '谈判是成熟职场人的标志。要求培训+薪资调整+明确KPI，能将成功率提升到60%以上。',
              effects: [{emoji: '📈', name: '职业', value: 35}, {emoji: '💰', name: '收入', value: 25}, {emoji: '📚', name: '能力', value: 20}]
            })
            
            return branches
          }
        },
        
        // 辞职场景
        resign: {
          trigger: ['辞职', '离职', '跳槽', '不干', '走人', '想换工作'],
          reasoning: (input) => {
            const steps = []
            
            steps.push({
              title: '分析离职原因',
              desc: '离职原因通常分几类：1）钱不到位 2）心受委屈（管理/文化）3）没成长 4）外部机会更好。不同原因对应不同策略。'
            })
            
            if (input.includes('薪资') || input.includes('工资') || input.includes('钱')) {
              steps.push({
                title: '薪资问题的替代方案',
                desc: '如果是薪资问题，建议先尝试内部调薪或跳槽谈判。单纯裸辞在当前的就业环境下风险较高（2024年互联网行业HC收紧约30%）。'
              })
            }
            
            steps.push({
              title: '评估就业市场',
              desc: '当前就业市场：互联网大厂HC收紧，但AI/新能源/出海领域仍有需求。建议先拿到offer再离职，避免"空窗期焦虑"。'
            })
            
            return steps
          },
          
          dimensions: () => [
            { emoji: '💰', name: '经济安全', score: 4, analysis: '裸辞后平均求职周期2-4个月（2024年数据）。需确保有6个月生活费储备。' },
            { emoji: '📈', name: '职业连续性', score: 5, analysis: '空窗期超过3个月，面试时会被质疑。建议骑驴找马。' },
            { emoji: '😊', name: '心理状态', score: 6, analysis: '如果当前工作已严重影响身心健康，离职是合理的。但需区分"暂时疲惫"和"长期消耗"。' },
            { emoji: '🎯', name: '目标清晰度', score: 5, analysis: '离职前需明确：下一份工作要什么？如果只是为了"逃离"，很可能跳入另一个坑。' }
          ],
          
          branches: () => [
            { emoji: '🎉', title: '骑驴找马成功', desc: '在职期间拿到更好offer，无缝衔接。', probability: 25, reasoning: '最优策略，但需要投入大量时间面试。适合有明确目标的人。', effects: [{emoji: '💰', name: '收入', value: 20}, {emoji: '📈', name: '职业', value: 15}] },
            { emoji: '😰', title: '裸辞后长期失业', desc: '辞职后2个月还没找到合适工作，开始焦虑。', probability: 20, reasoning: '2024年就业市场严峻，裸辞风险高。焦虑状态下容易降低标准。', effects: [{emoji: '💰', name: '收入', value: -30}, {emoji: '😰', name: '焦虑', value: 25}] },
            { emoji: '💻', title: '转自由职业', desc: '你开始做自由职业/咨询，收入不稳定但时间自由。', probability: 15, reasoning: '适合有核心技能+人脉资源的人。前6个月收入通常只有上班的30-50%。', effects: [{emoji: '😊', name: '自由', value: 25}, {emoji: '💰', name: '收入', value: -15}] },
            { emoji: '📚', title: 'gap year学习', desc: '你决定休息一段时间，学习新技能。', probability: 15, reasoning: '适合有明确学习目标的人。但gap year在HR眼中可能是减分项。', effects: [{emoji: '📚', name: '能力', value: 20}, {emoji: '💰', name: '收入', value: -25}] },
            { emoji: '🔄', title: '回原公司', desc: '找不到更好的，又联系了原公司，降薪回去了。', probability: 10, reasoning: '发生概率约10%。回原公司通常意味着谈判地位下降。', effects: [{emoji: '📉', name: '自尊', value: -15}, {emoji: '💰', name: '收入', value: -10}] },
            { emoji: '🚀', title: '创业', desc: '你和前同事一起创业了。', probability: 15, reasoning: '创业成功率约10%，但失败后获得的认知远超打工。适合有积累+能承受风险的人。', effects: [{emoji: '📈', name: '上限', value: 50}, {emoji: '💰', name: '风险', value: -30}] }
          ]
        },
        
        // 面试场景
        interview: {
          trigger: ['面试', '应聘', '求职', '找工作', 'offer'],
          reasoning: () => [
            { title: '评估面试准备度', desc: '面试成功率与准备度强相关。建议：1）研究公司业务和产品 2）准备STAR法则案例 3）准备3-5个反问问题。' },
            { title: '分析岗位匹配度', desc: '不要只看JD，要看团队阶段。初创团队需要全能型，大厂需要专精型。错配会导致很快离职。' }
          ],
          dimensions: () => [
            { emoji: '🎯', name: '匹配度', score: 6, analysis: '技能匹配度占面试成功的40%，文化匹配度占35%，薪资匹配度占25%。' },
            { emoji: '📚', name: '准备度', score: 5, analysis: '充分准备的候选人，通过率提升2-3倍。包括公司研究、案例准备、模拟面试。' },
            { emoji: '💰', name: '薪资谈判空间', score: 5, analysis: '通常有10-20%的谈判空间。但超出预算30%以上，即使通过也可能被放弃。' }
          ],
          branches: () => [
            { emoji: '🎉', title: '拿到满意offer', desc: '面试表现出色，拿到期望薪资的offer。', probability: 20, reasoning: '充分准备+岗位匹配的候选人，拿到满意offer的概率约20%。', effects: [{emoji: '📈', name: '职业', value: 20}, {emoji: '💰', name: '收入', value: 20}] },
            { emoji: '📈', title: '拿到但需谈判', desc: 'offer给了但薪资低于预期，进入谈判阶段。', probability: 25, reasoning: '约25%的offer需要谈判。谈判技巧：用其他offer做杠杆>单纯要求加薪。', effects: [{emoji: '💰', name: '收入', value: 10}, {emoji: '😰', name: '焦虑', value: 5}] },
            { emoji: '😐', title: '进入下一轮', desc: '初面通过，进入复试/HR面。', probability: 30, reasoning: '大厂通常3-5轮面试。每轮通过率约50%。', effects: [{emoji: '😊', name: '希望', value: 10}] },
            { emoji: '😰', title: '面试失败', desc: '面试未通过，收到拒信。', probability: 20, reasoning: '面试失败很正常。建议复盘：是技能不匹配？还是表达问题？还是薪资超预期？', effects: [{emoji: '😰', name: '自信', value: -10}, {emoji: '📚', name: '经验', value: 5}] },
            { emoji: '💡', title: '被推荐其他岗位', desc: '面试官觉得你适合另一个岗位。', probability: 5, reasoning: '发生概率约5%，通常说明你给人留下了好印象但技能错配。', effects: [{emoji: '🤝', name: '人脉', value: 15}, {emoji: '📈', name: '机会', value: 10}] }
          ]
        }
      },
      
      // 感情领域
      relationship: {
        keywords: ['感情', '恋爱', '分手', '表白', '相亲', '结婚', '离婚', '对象', '男朋友', '女朋友', '喜欢', '爱', '追'],
        dimensions: ['情感匹配', '长期潜力', '现实条件', '个人成长', '家庭因素'],
        
        confession: {
          trigger: ['表白', '喜欢', '告白', '暗恋', '追', '心动'],
          reasoning: (input) => {
            const steps = []
            
            steps.push({
              title: '评估关系阶段',
              desc: '表白成功率与双方关系阶段强相关。暧昧期表白成功率最高（约50%），刚认识就表白成功率最低（<10%）。'
            })
            
            if (input.includes('很久') || input.includes('多年') || input.includes('一直')) {
              steps.push({
                title: '警惕"沉没成本"',
                desc: '暗恋时间越长，表白时心理压力越大。但对方是否喜欢你，通常在相处1-2个月内就能感知到。长期暗恋而不表白，往往是害怕面对答案。'
              })
            }
            
            steps.push({
              title: '分析信号',
              desc: '积极信号：主动找你聊天、愿意单独见面、分享私密话题、身体距离近。消极信号：回复慢/敷衍、拒绝邀约、不谈感情话题。'
            })
            
            return steps
          },
          
          dimensions: (input) => {
            const dims = []
            
            dims.push({
              emoji: '💕', name: '情感匹配', score: 5,
              analysis: '单方面的喜欢不等于匹配。需要评估：价值观、生活方式、未来规划是否一致。'
            })
            
            dims.push({
              emoji: '📈', name: '表白时机', score: input.includes('暧昧') || input.includes('经常聊天') ? 7 : 4,
              analysis: '有明确暧昧信号时表白成功率最高。如果没有信号就表白，容易被当"朋友"。'
            })
            
            dims.push({
              emoji: '😊', name: '心理承受力', score: 6,
              analysis: '被拒绝是大概率事件（即使互相喜欢，时机不对也可能被拒）。需要评估自己能否承受。'
            })
            
            dims.push({
              emoji: '🎯', name: '长期潜力', score: 5,
              analysis: '即使表白成功，也需要考虑：异地、家庭背景、人生阶段是否匹配。'
            })
            
            return dims
          },
          
          branches: (input) => {
            const hasSignal = input.includes('暧昧') || input.includes('经常') || input.includes('主动')
            
            return [
              { emoji: '💕', title: '双向奔赴', desc: '对方也喜欢你，你们在一起了。', probability: hasSignal ? 35 : 15, reasoning: hasSignal ? '有暧昧信号时，双向喜欢的概率约35%。' : '没有明确信号就表白，成功率通常<20%。', effects: [{emoji: '😊', name: '幸福', value: 30}, {emoji: '💕', name: '感情', value: 25}] },
              { emoji: '🤔', title: '需要想想', desc: '对方说需要时间考虑。', probability: 20, reasoning: '约20%的表白会得到"考虑"的答复。这通常意味着：1）对你有好感但不强烈 2）有顾虑（异地/时机）3）不想直接拒绝伤感情。', effects: [{emoji: '😰', name: '焦虑', value: 10}, {emoji: '⏱️', name: '等待', value: 15}] },
              { emoji: '💔', title: '婉拒但做朋友', desc: '对方说更适合做朋友。', probability: 30, reasoning: '约30%的表白会被婉拒。但如果处理得当，仍可能保持友好关系。', effects: [{emoji: '😢', name: '伤心', value: 15}, {emoji: '🤝', name: '人脉', value: 5}] },
              { emoji: '🚪', title: '直接拒绝', desc: '对方明确拒绝，关系变尴尬。', probability: 10, reasoning: '直接拒绝约占10%。通常发生在：1）完全没感觉 2）已有对象 3）觉得被冒犯。', effects: [{emoji: '💔', name: '伤心', value: 20}, {emoji: '😰', name: '自信', value: -10}] },
              { emoji: '💡', title: '表白后更亲近', desc: '虽然没立刻答应，但你们的关系反而更近了。', probability: 5, reasoning: '约5%的概率。对方被你的勇气打动，开始认真考虑你们的关系。', effects: [{emoji: '💕', name: '感情', value: 15}, {emoji: '😊', name: '希望', value: 10}] }
            ]
          }
        },
        
        breakup: {
          trigger: ['分手', '离婚', '失恋', '劈腿', '出轨'],
          reasoning: () => [
            { title: '评估分手类型', desc: '冲动型分手（可挽回）vs 积累型分手（难挽回）vs 原则性分手（不可挽回）。不同类型策略完全不同。' },
            { title: '分析挽回可能性', desc: '真性分手的信号：删除联系方式、向亲友宣布、开始新生活。假性分手的信号：仍回复消息、社交动态伤感、向共同朋友打听你。' }
          ],
          dimensions: () => [
            { emoji: '💔', name: '情感恢复', score: 4, analysis: '分手后的痛苦期通常持续3-6个月。前1个月最痛苦，3个月后开始好转。' },
            { emoji: '📈', name: '个人成长', score: 6, analysis: '70%的人表示分手让自己更清楚想要什么。关键是从关系中学习，而不是重复同样模式。' },
            { emoji: '🎯', name: '未来机会', score: 7, analysis: '结束错误的关系，才能遇到对的人。统计显示，第二段婚姻/恋爱的满意度通常高于第一段。' }
          ],
          branches: () => [
            { emoji: '😢', title: '痛苦期后成长', desc: '前3个月很痛苦，但你逐渐走出来，变得更成熟。', probability: 40, reasoning: '约40%的人能从分手中获得成长。关键是不要急于进入下一段关系。', effects: [{emoji: '📚', name: '成长', value: 20}, {emoji: '😢', name: '痛苦', value: -15}] },
            { emoji: '🔄', title: '复合成功', desc: '冷静一段时间后，你们复合了。', probability: 15, reasoning: '复合成功率约15%。但复合后再次分手的概率高达80%，除非解决了根本问题。', effects: [{emoji: '💕', name: '感情', value: 15}, {emoji: '😰', name: '风险', value: 10}] },
            { emoji: '👀', title: '遇到更好的人', desc: '半年后你遇到了更适合的人。', probability: 25, reasoning: '约25%的人在分手1年内遇到更合适的对象。前提是：1）彻底放下前任 2）明确自己的需求。', effects: [{emoji: '💕', name: '感情', value: 25}, {emoji: '😊', name: '幸福', value: 20}] },
            { emoji: '😰', title: '长期走不出', desc: '1年后你还在怀念前任，影响新恋情。', probability: 15, reasoning: '约15%的人会长期沉浸在失恋中。这通常与自尊受损有关，建议寻求心理咨询。', effects: [{emoji: '😰', name: '抑郁', value: 15}, {emoji: '💔', name: '孤独', value: 10}] },
            { emoji: '💡', title: '专注自我', desc: '你把精力投入到事业/兴趣中，意外获得成功。', probability: 5, reasoning: '约5%的人将失恋能量转化为动力，在事业/学业上取得突破。', effects: [{emoji: '📈', name: '事业', value: 30}, {emoji: '😊', name: '自信', value: 20}] }
          ]
        }
      },
      
      // 投资领域
      investment: {
        keywords: ['投资', '股票', '基金', '买房', '理财', '赚钱', '存款', '负债', '贷款'],
        dimensions: ['风险承受', '收益预期', '流动性', '知识储备', '市场环境'],
        
        stock: {
          trigger: ['股票', '炒股', '股市', 'A股', '港股', '美股'],
          reasoning: () => [
            { title: '评估投资知识', desc: '散户在股市中亏损的概率约70%。如果没有系统的投资知识（财务报表分析、估值模型、宏观判断），炒股等同于赌博。' },
            { title: '分析市场环境', desc: '2024年A股波动率较高，结构性行情明显。没有选股能力的散户，建议通过指数基金参与市场。' },
            { title: '风险承受评估', desc: '投资股票的钱必须是"3年内不用的闲钱"。如果这笔钱是买房首付/结婚费用，绝对不要投入股市。' }
          ],
          dimensions: () => [
            { emoji: '⚠️', name: '风险等级', score: 3, analysis: '个股投资属于高风险。散户在信息、工具、心理上均处于劣势。' },
            { emoji: '📚', name: '知识储备', score: 4, analysis: '需要掌握：基本面分析、技术分析、仓位管理、止损纪律。缺少任何一项都可能导致亏损。' },
            { emoji: '📊', name: '市场环境', score: 5, analysis: '当前市场处于震荡期，板块轮动快。对选股能力要求极高。' },
            { emoji: '💰', name: '资金性质', score: 4, analysis: '如果是闲钱（3年以上不用），风险可控。如果是短期资金，风险极高。' }
          ],
          branches: () => [
            { emoji: '📈', title: '短期获利', desc: '你运气好，买的股票涨了20%。', probability: 15, reasoning: '短期获利约15%概率。但运气赚的钱，通常会凭实力亏回去。', effects: [{emoji: '💰', name: '财富', value: 15}, {emoji: '😊', name: '自信', value: 10}] },
            { emoji: '📉', title: '被套牢', desc: '买入后下跌30%，你舍不得割肉，越套越深。', probability: 35, reasoning: '散户被套牢的概率约35%。核心原因：没有止损纪律+补仓摊低成本的心理陷阱。', effects: [{emoji: '💰', name: '财富', value: -25}, {emoji: '😰', name: '焦虑', value: 20}] },
            { emoji: '📊', title: '不赚不赔', desc: '股票涨跌波动，你频繁操作，最后发现没赚钱还交了手续费。', probability: 25, reasoning: '约25%的散户处于"盈亏平衡"状态。但算上时间成本和手续费，实际是亏损的。', effects: [{emoji: '⏱️', name: '时间', value: -15}, {emoji: '😰', name: '精力', value: -10}] },
            { emoji: '💡', title: '转为价值投资', desc: '经历几次亏损后，你开始学习价值投资，转向指数基金。', probability: 15, reasoning: '约15%的散户会"进化"为价值投资者。这是从亏损走向稳定盈利的关键转变。', effects: [{emoji: '📚', name: '认知', value: 25}, {emoji: '📈', name: '长期', value: 15}] },
            { emoji: '🚪', title: '退出股市', desc: '亏损后你决定不再炒股，把钱存银行或买房。', probability: 10, reasoning: '约10%的人会选择彻底退出。这未必是坏事——承认不适合也是一种智慧。', effects: [{emoji: '😊', name: '安心', value: 10}, {emoji: '💰', name: '保值', value: 3}] }
          ]
        },
        
        house: {
          trigger: ['买房', '房子', '房产', '楼盘', '首付', '房贷'],
          reasoning: (input) => {
            const steps = []
            
            steps.push({
              title: '评估购房目的',
              desc: '自住 vs 投资，决策逻辑完全不同。自住看需求和承受力，投资看租售比和升值潜力。'
            })
            
            if (input.includes('一线') || input.includes('北京') || input.includes('上海') || input.includes('深圳')) {
              steps.push({
                title: '一线城市分析',
                desc: '一线城市房价收入比约30-40倍，远超国际合理水平（6-8倍）。但核心地段仍有保值属性。需警惕：远郊新区、老破小（无学区）。'
              })
            }
            
            steps.push({
              title: '计算真实成本',
              desc: '买房不只是首付。需计算：1）贷款利息（30年利息≈本金）2）物业费 3）维修基金 4）机会成本（首付若投资其他）。真实年化成本约4-6%。'
            })
            
            return steps
          },
          
          dimensions: (input) => {
            const isFirst = input.includes('第一套') || input.includes('首套')
            const isInvestment = input.includes('投资') || input.includes('升值')
            
            return [
              { emoji: '💰', name: '财务压力', score: isFirst ? 4 : 5, analysis: '首套房首付20-30%，但月供通常占收入30-50%。需确保有6个月应急储备。' },
              { emoji: '📈', name: '升值潜力', score: isInvestment ? 5 : 6, analysis: '非核心城市房产升值空间有限。2024年除一线核心地段外，多数城市房价持平或微跌。' },
              { emoji: '🏠', name: '居住价值', score: isFirst ? 8 : 4, analysis: '自住房的核心价值是"稳定感"和"归属感"。对刚需来说，这是无法用金钱衡量的。' },
              { emoji: '⚡', name: '流动性', score: 4, analysis: '房产流动性差，急售通常需降价10-20%。确保3-5年内不会急用钱。' }
            ]
          },
          
          branches: (input) => {
            const isFirst = input.includes('第一套') || input.includes('首套')
            
            return [
              { emoji: '📈', title: '房价微涨', desc: '买了之后房价每年涨3-5%，跑赢通胀。', probability: 25, reasoning: '核心城市核心地段，长期看有保值属性。但非核心地段可能横盘。', effects: [{emoji: '💰', name: '资产', value: 15}, {emoji: '😊', name: '安心', value: 10}] },
              { emoji: '🏠', title: '安居乐业', desc: '房价没涨没跌，但你有了稳定的家。', probability: 35, reasoning: isFirst ? '对刚需来说，"住"的价值远大于"涨"。35%的概率是横盘，但这不影响居住价值。' : '投资的话，横盘意味着亏损（算上利息和机会成本）。', effects: [{emoji: '😊', name: '幸福', value: 15}, {emoji: '💰', name: '资产', value: isFirst ? 0 : -5}] },
              { emoji: '📉', title: '房价下跌', desc: '买了之后房价跌了15%，首付亏没了。', probability: 25, reasoning: '2024年部分城市已出现15-20%的跌幅。特别是远郊新区、无学区老破小。', effects: [{emoji: '💰', name: '资产', value: -20}, {emoji: '😰', name: '焦虑', value: 15}] },
              { emoji: '⚡', title: '急需用钱', desc: '买房后遇到突发情况，需要卖房但卖不掉。', probability: 10, reasoning: '约10%的家庭会在买房3年内遇到急需用钱的情况。房产流动性差，急售需大幅降价。', effects: [{emoji: '💰', name: '资产', value: -15}, {emoji: '😰', name: '压力', value: 20}] },
              { emoji: '💡', title: '租房更划算', desc: '仔细计算后发现，租房+理财比买房更划算。', probability: 5, reasoning: '在房价收入比>30的城市，租房+定投指数基金可能是更理性的选择。但大多数人过不了心理关。', effects: [{emoji: '💰', name: '灵活', value: 15}, {emoji: '😰', name: '不安', value: 5}] }
            ]
          }
        }
      },
      
      // 学业领域
      education: {
        keywords: ['考试', '高考', '考研', '考公', '考编', '考证', '成绩', '学习', '学校', '大学', '研究生', '留学'],
        dimensions: ['投入产出', '时间成本', '竞争强度', '个人适配', '长期价值'],
        
        gaokao: {
          trigger: ['高考', '中考', '期末'],
          reasoning: () => [
            { title: '评估当前水平', desc: '模考成绩与目标院校的差距是多少？10分以内可以通过心态调整弥补，30分以上需要策略性放弃部分难题。' },
            { title: '分析发挥规律', desc: '回顾历次大考：你是"稳定型"（波动<20分）还是"起伏型"？稳定型保持节奏即可，起伏型需要调整作息和心态。' }
          ],
          dimensions: () => [
            { emoji: '📚', name: '知识掌握', score: 5, analysis: '最后阶段，知识框架已基本定型。重点是查漏补缺，而不是全面复习。' },
            { emoji: '😊', name: '心态状态', score: 6, analysis: '高考发挥失常约30%是因为心态。适度紧张有利，过度紧张有害。' },
            { emoji: '⏱️', name: '时间分配', score: 5, analysis: '最后阶段，时间分配比学习时间更重要。建议：70%时间给弱科，30%维持强科。' }
          ],
          branches: () => [
            { emoji: '🎉', title: '超常发挥', desc: '比模考高30-50分，考上理想学校。', probability: 10, reasoning: '超常发挥约10%概率。通常发生在：心态好+题目恰好对口+身体状态佳。', effects: [{emoji: '📈', name: '学历', value: 25}, {emoji: '😊', name: '自信', value: 20}] },
            { emoji: '📚', title: '正常发挥', desc: '成绩和模考差不多，进入预期学校。', probability: 50, reasoning: '约50%的人正常发挥。这是最可能的结果，也是制定志愿的基础。', effects: [{emoji: '📈', name: '学历', value: 15}, {emoji: '😊', name: '满意', value: 10}] },
            { emoji: '😰', title: '发挥失常', desc: '比模考低20-40分，需要调整志愿。', probability: 30, reasoning: '约30%的人发挥失常。原因：紧张、身体问题、题目风格不适应。', effects: [{emoji: '📉', name: '学历', value: -10}, {emoji: '😰', name: '失落', value: 15}] },
            { emoji: '🔄', title: '选择复读', desc: '成绩不理想，决定再来一年。', probability: 10, reasoning: '复读成功率约60%（提分），但心理压力极大。适合：有明显失误+心理承受力强的人。', effects: [{emoji: '📚', name: '机会', value: 20}, {emoji: '😰', name: '压力', value: 25}] }
          ]
        },
        
        postgraduate: {
          trigger: ['考研', '研究生', '考博', '读研'],
          reasoning: () => [
            { title: '评估考研动机', desc: '逃避就业（错误动机）vs 学术兴趣（正确动机）vs 提升学历（中性动机）。动机决定你能坚持多久。' },
            { title: '计算机会成本', desc: '考研1年+读研3年=4年时间。如果直接工作，4年后可能已是资深员工（年薪20-30万）。读研的回报是否大于这4年的收入？' }
          ],
          dimensions: () => [
            { emoji: '📈', name: '长期收益', score: 6, analysis: '研究生起薪通常比本科高20-30%，但3年工作经验可能带来更高涨幅。适合：研究型岗位/体制内/转行。' },
            { emoji: '⏱️', name: '时间成本', score: 4, analysis: '3年时间+学费+生活费。对家境一般的学生，时间成本很高。' },
            { emoji: '😊', name: '心理承受', score: 5, analysis: '考研成功率约25%。失败后的挫败感+同龄人已工作的对比压力，需要强心理素质。' }
          ],
          branches: () => [
            { emoji: '🎉', title: '一战上岸', desc: '成功考上理想学校和专业。', probability: 20, reasoning: '一战成功率约20%（名校更低）。需要：充分准备+合理目标+稳定心态。', effects: [{emoji: '📈', name: '学历', value: 25}, {emoji: '😊', name: '成就', value: 20}] },
            { emoji: '📚', title: '调剂录取', desc: '没考上目标学校，调剂到其他学校/专业。', probability: 15, reasoning: '约15%的人通过调剂上岸。但调剂学校/专业通常不如预期，需权衡是否值得读。', effects: [{emoji: '📈', name: '学历', value: 15}, {emoji: '😰', name: '遗憾', value: 5}] },
            { emoji: '😰', title: '考研失败', desc: '没考上，需要重新规划。', probability: 35, reasoning: '约35%的人考研失败。失败后的选择：二战（风险高）/工作（更务实）/出国（成本高）。', effects: [{emoji: '😰', name: '失落', value: 15}, {emoji: '⏱️', name: '时间', value: -20}] },
            { emoji: '💼', title: '先工作后考研', desc: '工作几年后再考研，目标更明确。', probability: 15, reasoning: '工作后考研的人，目标通常更明确（MBA/转行），成功率反而更高。但时间成本更大。', effects: [{emoji: '💰', name: '收入', value: 15}, {emoji: '📈', name: '学历', value: 20}] },
            { emoji: '✈️', title: '出国读研', desc: '转而出国读1-2年硕士。', probability: 15, reasoning: '出国读研时间短（1-2年），但成本高（30-80万）。适合：家境允许+想转行+想体验海外生活的人。', effects: [{emoji: '📈', name: '学历', value: 20}, {emoji: '💰', name: '花费', value: -30}] }
          ]
        }
      },
      
      // 健康领域
      health: {
        keywords: ['健康', '体检', '生病', '医院', '病', '身体', '减肥', '健身', '熬夜', '失眠'],
        dimensions: ['严重程度', '恢复难度', '生活习惯', '医疗成本', '长期影响'],
        
        checkup: {
          trigger: ['体检', '检查', '报告'],
          reasoning: () => [
            { title: '解读体检指标', desc: '体检异常分三级：1）箭头指标（轻微异常，调整生活方式即可）2）建议复查（需进一步检查确认）3）立即就医（严重异常）。' },
            { title: '避免过度焦虑', desc: '体检发现异常≠生病。很多指标受近期作息、饮食影响。建议：1）复查确认 2）找专科医生解读 3）不要百度自我诊断。' }
          ],
          dimensions: () => [
            { emoji: '⚠️', name: '异常程度', score: 5, analysis: '大多数体检异常是轻度（如脂肪肝、尿酸偏高），通过生活方式调整可逆。' },
            { emoji: '⏱️', name: '干预时机', score: 7, analysis: '体检的意义在于"早发现早干预"。很多疾病在早期完全可逆，拖到晚期则代价巨大。' },
            { emoji: '💰', name: '医疗成本', score: 6, analysis: '早期干预成本（几百元+生活方式调整）远低于晚期治疗（几万元+手术）。' }
          ],
          branches: () => [
            { emoji: '💪', title: '虚惊一场', desc: '复查后确认没事，是假阳性。', probability: 40, reasoning: '约40%的体检异常在复查后确认没事。特别是肿瘤标志物、心电图等项目假阳性率高。', effects: [{emoji: '😊', name: '安心', value: 15}, {emoji: '💰', name: '花费', value: -3}] },
            { emoji: '🥗', title: '调整生活方式', desc: '确实有问题，但通过饮食+运动改善了。', probability: 35, reasoning: '约35%的体检异常（脂肪肝、高血脂、尿酸高）可通过3-6个月生活方式调整逆转。', effects: [{emoji: '💪', name: '健康', value: 20}, {emoji: '😊', name: '习惯', value: 15}] },
            { emoji: '💊', title: '需要药物治疗', desc: '指标较高，需要药物干预。', probability: 15, reasoning: '约15%需要药物治疗（如高血压、糖尿病前期）。遵医嘱服药+生活方式调整，通常可控。', effects: [{emoji: '💊', name: '治疗', value: 15}, {emoji: '💰', name: '花费', value: -5}] },
            { emoji: '🏥', title: '需要手术/住院', desc: '发现较严重问题，需要进一步治疗。', probability: 8, reasoning: '约8%需要手术或住院治疗。但体检发现的问题，通常比出现症状才发现要早，预后更好。', effects: [{emoji: '🏥', name: '治疗', value: 25}, {emoji: '💰', name: '花费', value: -20}, {emoji: '😰', name: '压力', value: 15}] },
            { emoji: '😰', title: '忽视不管', desc: '你觉得没事，没复查也没调整，问题恶化。', probability: 2, reasoning: '约2%的人忽视体检异常，导致小问题变大问题。这是体检最大的浪费。', effects: [{emoji: '📉', name: '健康', value: -25}, {emoji: '💰', name: '花费', value: -30}] }
          ]
        }
      }
    }
  }

  // 智能分析输入
  analyze(input) {
    const text = input.toLowerCase()
    let bestMatch = null
    let maxScore = 0
    
    // 遍历所有领域和场景
    for (const [domain, domainData] of Object.entries(this.knowledgeBase)) {
      // 检查领域关键词
      let domainScore = 0
      for (const kw of domainData.keywords) {
        if (text.includes(kw)) domainScore += 2
      }
      
      // 检查具体场景
      for (const [scenario, scenarioData] of Object.entries(domainData)) {
        if (scenario === 'keywords' || scenario === 'dimensions') continue
        
        let scenarioScore = domainScore
        for (const trigger of scenarioData.trigger) {
          if (text.includes(trigger)) scenarioScore += 5
        }
        
        if (scenarioScore > maxScore) {
          maxScore = scenarioScore
          bestMatch = { domain, scenario, data: scenarioData }
        }
      }
    }
    
    // 如果没有匹配，使用通用分析
    if (!bestMatch || maxScore < 3) {
      return this.genericAnalyze(input)
    }
    
    // 执行匹配场景的推理
    return {
      matched: true,
      domain: bestMatch.domain,
      scenario: bestMatch.scenario,
      reasoning: bestMatch.data.reasoning ? bestMatch.data.reasoning(input) : [],
      dimensions: bestMatch.data.dimensions ? bestMatch.data.dimensions(input) : [],
      branches: bestMatch.data.branches ? bestMatch.data.branches(input) : []
    }
  }
  
  // 通用分析（未匹配到具体场景时）
  genericAnalyze(input) {
    return {
      matched: false,
      reasoning: [
        { title: '分析事件性质', desc: '这是一个生活决策类事件。根据经验，大多数生活决策可以从以下几个维度分析：短期影响、长期影响、可逆性、机会成本。' },
        { title: '评估信息完整度', desc: '你提供的信息有限。为了更精准地推演，建议补充：1）你的背景/现状 2）你的顾虑/目标 3）时间约束 4）资源约束。' },
        { title: '给出通用建议', desc: '面对不确定的决策，建议采用"最小后悔原则"：想象10年后的自己，哪个选择会让你更后悔？通常答案会变得清晰。' }
      ],
      dimensions: [
        { emoji: '🎯', name: '信息完整度', score: 4, analysis: '信息越完整，推演越精准。建议补充更多背景。' },
        { emoji: '⏱️', name: '时间压力', score: 5, analysis: '如果决策时间充裕，建议收集更多信息。如果必须马上决定，跟随直觉往往比过度分析更好。' },
        { emoji: '😊', name: '心理承受', score: 5, analysis: '任何决策都有风险。关键是：这个风险你是否能承受？最坏结果你是否能接受？' }
      ],
      branches: [
        { emoji: '📈', title: '事情向好发展', desc: '基于现有信息，这件事有不错的结果。', probability: 25, reasoning: '约25%的生活事件会超预期发展。通常发生在：准备充分+心态积极+有一定运气。', effects: [{emoji: '😊', name: '心情', value: 15}] },
        { emoji: '😐', title: '平淡收场', desc: '事情没有大的波澜，结果中规中矩。', probability: 30, reasoning: '约30%的事件会平淡收场。这其实是好事——说明风险可控。', effects: [{emoji: '😊', name: '心情', value: 0}] },
        { emoji: '⚠️', title: '遇到挑战', desc: '过程中会遇到一些困难，但最终能解决。', probability: 25, reasoning: '约25%的事件会遇到挑战。这些挑战往往是成长的机会。', effects: [{emoji: '📚', name: '成长', value: 15}, {emoji: '😰', name: '压力', value: 10}] },
        { emoji: '😰', title: '结果不理想', desc: '事情的发展不如预期，需要调整策略。', probability: 15, reasoning: '约15%的事件结果不理想。关键是：能否及时止损？能否从中学到东西？', effects: [{emoji: '😰', name: '失落', value: 15}] },
        { emoji: '💡', title: '意外转机', desc: '会出现意想不到的转机或新机会。', probability: 5, reasoning: '约5%的概率出现意外转机。保持开放心态，往往能在危机中发现机会。', effects: [{emoji: '💡', name: '机遇', value: 20}] }
      ]
    }
  }
  
  // 生成下一层分支
  generateNextBranches(selectedBranch, currentLevel) {
    // 根据当前分支生成后续
    const nextMap = {
      '接受并快速适应': [
        { emoji: '🏆', title: '成为优秀管理者', desc: '2年后你成为了公司最年轻的管理者，年薪翻倍。', probability: 30 },
        { emoji: '✈️', title: '被挖角', desc: '你的管理能力被认可，收到多家公司邀请。', probability: 25 },
        { emoji: '😤', title: '团队危机', desc: '团队核心成员离职，你面临重建团队的挑战。', probability: 25 },
        { emoji: '💼', title: '平稳发展', desc: '管理工作渐入佳境，但也没有大的突破。', probability: 20 }
      ],
      '接受但难以适应': [
        { emoji: '🔄', title: '转回执行岗', desc: '1年后你申请转回产品经理岗。', probability: 35 },
        { emoji: '😰', title: '被优化', desc: '管理绩效不佳，被公司优化。', probability: 25 },
        { emoji: '📚', title: '艰难适应', desc: '虽然很痛苦，但你咬牙坚持下来了。', probability: 25 },
        { emoji: '🚪', title: '离职', desc: '你选择了离职，重新找工作。', probability: 15 }
      ],
      '接受+找导师': [
        { emoji: '🚀', title: '快速晋升', desc: '在导师指导下，你1年就达到了别人3年的水平。', probability: 40 },
        { emoji: '🤝', title: '建立人脉', desc: '通过导师认识了更多行业大佬。', probability: 30 },
        { emoji: '💡', title: '创业机会', desc: '导师邀请你一起创业。', probability: 20 },
        { emoji: '📈', title: '稳步成长', desc: '按部就班地成长，成为合格管理者。', probability: 10 }
      ],
      '拒绝并跳槽': [
        { emoji: '🎉', title: '新工作更好', desc: '你找到了更适合的工作，薪资涨30%。', probability: 35 },
        { emoji: '😐', title: '平级跳槽', desc: '新工作差不多，没有本质变化。', probability: 30 },
        { emoji: '😰', title: '后悔', desc: '新工作也不如意，你开始后悔当初的选择。', probability: 20 },
        { emoji: '💡', title: '发现新方向', desc: '新工作让你发现了自己真正的兴趣。', probability: 15 }
      ],
      '谈判条件后接受': [
        { emoji: '🏆', title: '双赢', desc: '你成功带领团队，获得了公司和团队的双重认可。', probability: 45 },
        { emoji: '📈', title: '稳步发展', desc: '条件改善了，你逐渐适应并成长。', probability: 35 },
        { emoji: '😰', title: '期望过高', desc: '公司答应了条件但后续支持不到位。', probability: 20 }
      ],
      '双向奔赴': [
        { emoji: '💑', title: '甜蜜恋爱', desc: '你们开始了幸福的恋爱生活。', probability: 40 },
        { emoji: '💍', title: '走向婚姻', desc: '1-2年后你们决定结婚。', probability: 20 },
        { emoji: '😤', title: '发现不合', desc: '深入了解后发现价值观差异很大。', probability: 25 },
        { emoji: '🌍', title: '异地恋', desc: '一方需要去外地，开始异地恋。', probability: 15 }
      ],
      '短期获利': [
        { emoji: '📈', title: '继续加仓', desc: '你觉得还会涨，继续买入。', probability: 30 },
        { emoji: '💰', title: '获利了结', desc: '你明智地卖出了，落袋为安。', probability: 25 },
        { emoji: '📉', title: '利润回吐', desc: '没卖，股价跌回成本价。', probability: 30 },
        { emoji: '😰', title: '被套牢', desc: '加仓后股价暴跌，深度套牢。', probability: 15 }
      ],
      '被套牢': [
        { emoji: '📉', title: '越套越深', desc: '不断补仓，但股价持续下跌。', probability: 35 },
        { emoji: '💔', title: '割肉离场', desc: '承受不住亏损，认赔卖出。', probability: 30 },
        { emoji: '⏱️', title: '长期持有', desc: '你决定装死，等股价回升。', probability: 25 },
        { emoji: '📚', title: '学习反思', desc: '这次亏损让你开始系统学习投资知识。', probability: 10 }
      ]
    }
    
    if (nextMap[selectedBranch.title]) {
      return nextMap[selectedBranch.title]
    }
    
    // 通用后续
    return [
      { emoji: '📈', title: '持续影响', desc: '这件事继续产生后续影响。', probability: 30 },
      { emoji: '🔄', title: '新的变化', desc: '情况出现新的变化。', probability: 25 },
      { emoji: '🎯', title: '尘埃落定', desc: '事情基本有了定论。', probability: 25 },
      { emoji: '💡', title: '意外发展', desc: '出现意想不到的新情况。', probability: 20 }
    ]
  }
}

export default {
  data() {
    return {
      userEvent: '',
      userChoice: '',
      depth: 2,
      depthOptions: [
        { name: '浅层', desc: '推演1层', value: 1 },
        { name: '中等', desc: '推演2层', value: 2 },
        { name: '深层', desc: '推演3层', value: 3 }
      ],
      isPredicting: false,
      showingResult: false,
      showHistory: false,
      branchTree: [],
      selectedPath: [],
      finalSummary: '',
      finalAdvice: '',
      reasoningSteps: [],
      dimensions: [],
      canContinue: false,
      currentBranch: null,
      engine: null,
      predictionHistory: [],
      levelNames: ['可能的结果', '后续发展', '长期影响']
    }
  },
  onShow() {
    this.loadHistory()
    this.engine = new ReasoningEngine()
  },
  methods: {
    loadHistory() {
      this.predictionHistory = uni.getStorageSync('predictionHistory') || []
    },
    saveHistory() {
      uni.setStorageSync('predictionHistory', this.predictionHistory)
    },

    async startPrediction() {
      if (!this.userEvent.trim()) return
      
      this.isPredicting = true
      this.branchTree = []
      this.selectedPath = []
      this.finalSummary = ''
      this.finalAdvice = ''
      this.reasoningSteps = []
      this.dimensions = []
      
      await this.delay(600)
      
      // 使用推理引擎分析
      const result = this.engine.analyze(this.userEvent)
      
      this.reasoningSteps = result.reasoning
      this.dimensions = result.dimensions
      
      // 生成第一层分支
      const level1 = result.branches.map(b => ({
        ...b,
        selected: false,
        faded: false,
        canContinue: true,
        level: 0
      }))
      
      this.branchTree.push(level1)
      
      // 预生成后续层
      for (let i = 1; i < this.depth; i++) {
        await this.delay(300)
        const prevLevel = this.branchTree[i - 1]
        const nextLevel = []
        
        for (const branch of prevLevel) {
          const nextBranches = this.engine.generateNextBranches(branch, i)
          nextBranches.forEach(b => {
            nextLevel.push({
              ...b,
              selected: false,
              faded: false,
              canContinue: i < 2,
              level: i,
              parent: branch.title
            })
          })
        }
        
        if (nextLevel.length > 0) {
          this.branchTree.push(nextLevel)
        }
      }
      
      this.isPredicting = false
      this.showingResult = true
      this.canContinue = true
      
      this.saveToHistory()
    },

    selectBranch(branch, levelIndex, branchIndex) {
      this.branchTree[levelIndex].forEach((b, i) => {
        b.selected = i === branchIndex
        b.faded = i !== branchIndex
      })
      
      // 更新路径
      this.selectedPath = []
      for (let i = 0; i <= levelIndex; i++) {
        const selected = this.branchTree[i].find(b => b.selected)
        if (selected) {
          this.selectedPath.push(selected)
        }
      }
      
      this.generateSummary()
      this.currentBranch = branch
    },

    continuePrediction() {
      if (!this.currentBranch) {
        uni.showToast({ title: '请先选择一个分支', icon: 'none' })
        return
      }
      
      const currentLevel = this.currentBranch.level
      
      if (currentLevel + 1 < this.branchTree.length) {
        this.branchTree[currentLevel + 1].forEach(b => {
          b.faded = false
        })
      } else {
        const nextBranches = this.engine.generateNextBranches(this.currentBranch, currentLevel + 1)
        const newLevel = nextBranches.map(b => ({
          ...b,
          selected: false,
          faded: false,
          canContinue: currentLevel < 2,
          level: currentLevel + 1,
          parent: this.currentBranch.title
        }))
        
        this.branchTree.push(newLevel)
      }
      
      this.canContinue = currentLevel < 2
    },

    generateSummary() {
      if (this.selectedPath.length === 0) return
      
      const lastBranch = this.selectedPath[this.selectedPath.length - 1]
      const pathNames = this.selectedPath.map(p => p.title).join(' → ')
      
      let summary = `你选择了「${pathNames}」这条路径。`
      
      if (lastBranch.probability >= 35) {
        summary += '这是比较可能发生的方向。'
      } else if (lastBranch.probability >= 20) {
        summary += '这是有一定可能性的方向。'
      } else {
        summary += '这是小概率事件，但也不是不可能。'
      }
      
      // 生成建议
      let advice = ''
      if (lastBranch.title.includes('适应') || lastBranch.title.includes('困难')) {
        advice = '建议：寻求外部支持（导师/培训/书籍），不要独自硬撑。前3个月是最难的，撑过去就会好转。'
      } else if (lastBranch.title.includes('成功') || lastBranch.title.includes('好')) {
        advice = '建议：保持谦逊，持续学习。成功时最容易犯错，不要被胜利冲昏头脑。'
      } else if (lastBranch.title.includes('失败') || lastBranch.title.includes('不理想')) {
        advice = '建议：及时止损，复盘原因。失败本身不可怕，可怕的是重复同样的错误。'
      } else {
        advice = '建议：保持开放心态，准备好Plan B。生活充满不确定性，灵活性是最好的策略。'
      }
      
      this.finalSummary = summary
      this.finalAdvice = advice
    },

    resetPrediction() {
      this.showingResult = false
      this.userEvent = ''
      this.userChoice = ''
      this.branchTree = []
      this.selectedPath = []
      this.finalSummary = ''
      this.finalAdvice = ''
      this.reasoningSteps = []
      this.dimensions = []
      this.currentBranch = null
    },

    shareResult() {
      if (this.selectedPath.length === 0) {
        uni.showToast({ title: '请先选择一条路径', icon: 'none' })
        return
      }
      
      const pathText = this.selectedPath.map(p => p.title).join(' → ')
      const shareText = `我在【蝴蝶效应推演】中分析了一件事：\n\n「${this.userEvent}」\n\n推演路径：${pathText}\n\n${this.finalSummary}\n\n💡 ${this.finalAdvice}`
      
      uni.showModal({
        title: '分享推演结果',
        content: shareText,
        showCancel: false
      })
    },

    saveToHistory() {
      const record = {
        event: this.userEvent,
        choice: this.userChoice,
        date: new Date().toLocaleDateString(),
        branches: this.branchTree[0] || [],
        depth: this.depth
      }
      this.predictionHistory.unshift(record)
      if (this.predictionHistory.length > 50) {
        this.predictionHistory = this.predictionHistory.slice(0, 50)
      }
      this.saveHistory()
    },

    loadHistory(item) {
      this.userEvent = item.event
      this.userChoice = item.choice || ''
      this.depth = item.depth || 2
      this.showHistory = false
    },

    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
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

.header {
  text-align: center;
  margin-bottom: 40rpx;
}

.header-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.header-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 输入区域 */
.input-section {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.input-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.input-label {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 16rpx;
}

.input-textarea {
  width: 100%;
  min-height: 200rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
  margin-bottom: 10rpx;
}

.input-field {
  width: 100%;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
}

.input-hint {
  font-size: 22rpx;
  color: #a0aec0;
}

.depth-selector {
  display: flex;
  gap: 12rpx;
}

.depth-option {
  flex: 1;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  text-align: center;
  transition: all 0.3s;
}

.depth-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.depth-name {
  font-size: 28rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 4rpx;
}

.depth-desc {
  font-size: 22rpx;
  opacity: 0.8;
}

.predict-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 30rpx;
  font-size: 32rpx;
  border: none;
  margin-top: 10rpx;
}

.predict-btn[disabled] {
  opacity: 0.6;
}

.history-entry {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  padding: 20rpx;
  background: #fff;
  border-radius: 16rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.history-icon {
  font-size: 32rpx;
}

.history-text {
  font-size: 26rpx;
  color: #667eea;
}

/* 结果区域 */
.result-section {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.original-event {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  color: #fff;
}

.original-label {
  font-size: 24rpx;
  opacity: 0.8;
  display: block;
  margin-bottom: 8rpx;
}

.original-text {
  font-size: 30rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
  line-height: 1.5;
}

.original-choice {
  font-size: 26rpx;
  opacity: 0.9;
}

/* 推理过程 */
.reasoning-process {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.process-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.process-steps {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.process-step {
  display: flex;
  gap: 16rpx;
}

.step-num {
  width: 44rpx;
  height: 44rpx;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 44rpx;
  font-size: 24rpx;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.step-desc {
  font-size: 26rpx;
  color: #718096;
  line-height: 1.5;
}

/* 维度分析 */
.dimension-analysis {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.dim-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.dim-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.dim-item {
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
}

.dim-header {
  display: flex;
  align-items: center;
  margin-bottom: 8rpx;
}

.dim-emoji {
  font-size: 32rpx;
  margin-right: 8rpx;
}

.dim-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  flex: 1;
}

.dim-score {
  display: flex;
  align-items: baseline;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  background: #edf2f7;
}

.ds-num {
  font-size: 32rpx;
  font-weight: bold;
}

.ds-total {
  font-size: 22rpx;
  color: #a0aec0;
}

.dim-high .ds-num { color: #48bb78; }
.dim-mid .ds-num { color: #f6ad55; }
.dim-low .ds-num { color: #e53e3e; }

.dim-analysis {
  font-size: 26rpx;
  color: #718096;
  line-height: 1.5;
}

/* 分支树 */
.branch-tree {
  margin-bottom: 20rpx;
}

.tree-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
}

.tree-subtitle {
  font-size: 24rpx;
  color: #a0aec0;
  display: block;
  margin-bottom: 20rpx;
}

.branch-level {
  margin-bottom: 24rpx;
}

.level-label {
  font-size: 26rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
  margin-bottom: 12rpx;
}

.level-branches {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.branch-node {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
  border: 2rpx solid transparent;
}

.branch-node:active {
  transform: scale(0.98);
}

.branch-selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.branch-faded {
  opacity: 0.4;
}

.node-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8rpx;
}

.node-probability {
  font-size: 22rpx;
  font-weight: bold;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

.p-high {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.p-mid {
  background: rgba(246, 173, 85, 0.1);
  color: #f6ad55;
}

.p-low {
  background: rgba(229, 62, 62, 0.1);
  color: #e53e3e;
}

.node-emoji {
  font-size: 36rpx;
}

.node-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 6rpx;
}

.node-desc {
  font-size: 26rpx;
  color: #718096;
  display: block;
  margin-bottom: 10rpx;
}

.node-reasoning {
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 12rpx 16rpx;
  margin-bottom: 10rpx;
}

.nr-label {
  font-size: 22rpx;
  color: #667eea;
  font-weight: bold;
}

.nr-text {
  font-size: 24rpx;
  color: #4a5568;
  line-height: 1.5;
}

.node-effects {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.ne-tag {
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
  background: #edf2f7;
  color: #718096;
}

.ne-positive {
  background: rgba(72, 187, 120, 0.1);
  color: #48bb78;
}

.ne-negative {
  background: rgba(229, 62, 62, 0.1);
  color: #e53e3e;
}

.node-continue {
  margin-top: 10rpx;
  text-align: right;
}

.continue-text {
  font-size: 22rpx;
  color: #667eea;
}

/* 时间线 */
.timeline-view {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.timeline-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.timeline-path {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.path-item {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-bottom: 20rpx;
}

.path-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 20rpx;
  top: 48rpx;
  width: 2rpx;
  height: calc(100% - 20rpx);
  background: #e2e8f0;
}

.path-dot {
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  text-align: center;
  line-height: 44rpx;
  font-size: 24rpx;
  font-weight: bold;
  margin-right: 16rpx;
  flex-shrink: 0;
}

.path-content {
  flex: 1;
}

.path-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.path-desc {
  font-size: 24rpx;
  color: #718096;
}

/* 总结 */
.summary-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.summary-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 16rpx;
}

.summary-text {
  font-size: 28rpx;
  color: #4a5568;
  line-height: 1.6;
  display: block;
  margin-bottom: 20rpx;
}

.summary-advice {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 16rpx;
  padding: 20rpx;
  border-left: 4rpx solid #667eea;
}

.advice-label {
  font-size: 26rpx;
  font-weight: bold;
  color: #667eea;
  display: block;
  margin-bottom: 8rpx;
}

.advice-text {
  font-size: 26rpx;
  color: #4a5568;
  line-height: 1.5;
}

/* 操作按钮 */
.result-actions {
  display: flex;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.action-btn {
  flex: 1;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 28rpx;
  border: none;
}

.btn-continue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-restart {
  background: #f7fafc;
  color: #667eea;
}

.btn-share {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
}

/* 历史 */
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

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.history-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.04);
}

.history-event {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 8rpx;
}

.history-date {
  font-size: 22rpx;
  color: #a0aec0;
  display: block;
  margin-bottom: 10rpx;
}

.history-branches-preview {
  display: flex;
  gap: 8rpx;
  flex-wrap: wrap;
}

.hb-tag {
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

.bottom-space {
  height: 40rpx;
}
</style>
