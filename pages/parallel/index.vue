<template>
  <view class="container">
    <!-- 顶部 -->
    <view class="header">
      <text class="header-title">🦋 蝴蝶效应</text>
      <text class="header-desc">输入一件事，推演未来的无限可能</text>
    </view>

    <!-- 输入区域 -->
    <view class="input-section" v-if="!showingResult">
      <view class="input-card">
        <text class="input-label">📖 发生了什么？</text>
        <textarea 
          class="input-textarea" 
          v-model="userEvent"
          placeholder="描述一件你正在经历或即将发生的事情...&#10;例如：今天老板找我谈话，说要给我调岗到另一个部门"
          maxlength="200"
        />
        <text class="input-hint">越详细，推演越精准</text>
      </view>

      <view class="input-card">
        <text class="input-label">🎯 你的选择（可选）</text>
        <input 
          class="input-field" 
          v-model="userChoice"
          placeholder="你打算怎么做？例如：接受调岗"
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
        <text class="btn-text">{{isPredicting ? '推演中...' : '🔮 开始推演'}}</text>
      </button>

      <!-- 历史记录入口 -->
      <view class="history-entry" @click="showHistory = true">
        <text class="history-icon">📚</text>
        <text class="history-text">查看推演历史 ({{predictionHistory.length}})</text>
      </view>
    </view>

    <!-- 推演结果 -->
    <view class="result-section" v-if="showingResult">
      <!-- 原始事件 -->
      <view class="original-event">
        <text class="original-label">原始事件</text>
        <text class="original-text">{{userEvent}}</text>
        <text class="original-choice" v-if="userChoice">你的选择：{{userChoice}}</text>
      </view>

      <!-- 分支树 -->
      <view class="branch-tree">
        <text class="tree-title">🌳 推演结果</text>
        
        <view class="branch-level" v-for="(level, levelIndex) in branchTree" :key="levelIndex">
          <text class="level-label">第{{levelIndex + 1}}层</text>
          <view class="level-branches">
            <view 
              class="branch-node" 
              v-for="(branch, branchIndex) in level" 
              :key="branchIndex"
              :class="{'branch-selected': branch.selected, 'branch-faded': branch.faded}"
              @click="selectBranch(branch, levelIndex, branchIndex)"
            >
              <view class="node-header">
                <text class="node-probability">{{branch.probability}}%</text>
                <text class="node-emoji">{{branch.emoji}}</text>
              </view>
              <text class="node-title">{{branch.title}}</text>
              <text class="node-desc">{{branch.desc}}</text>
              <view class="node-effects" v-if="branch.effects">
                <text class="ne-tag" v-for="(eff, i) in branch.effects" :key="i" :class="{'ne-positive': eff.value > 0, 'ne-negative': eff.value < 0}">
                  {{eff.name}} {{eff.value > 0 ? '+' : ''}}{{eff.value}}
                </text>
              </view>
              <view class="node-continue" v-if="branch.canContinue">
                <text class="continue-text">点击继续推演 →</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 时间线视图 -->
      <view class="timeline-view" v-if="selectedPath.length > 0">
        <text class="timeline-title">⏱️ 你的推演路径</text>
        <view class="timeline-path">
          <view class="path-item" v-for="(item, index) in selectedPath" :key="index">
            <view class="path-dot"></view>
            <view class="path-content">
              <text class="path-title">{{item.title}}</text>
              <text class="path-desc">{{item.desc}}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 总结卡片 -->
      <view class="summary-card" v-if="finalSummary">
        <text class="summary-title">📋 推演总结</text>
        <text class="summary-text">{{finalSummary}}</text>
        <view class="summary-stats" v-if="pathStats">
          <view class="ps-item" v-for="(stat, key) in pathStats" :key="key">
            <text class="ps-emoji">{{stat.emoji}}</text>
            <text class="ps-name">{{stat.name}}</text>
            <text class="ps-value" :class="{'ps-up': stat.change > 0, 'ps-down': stat.change < 0}">
              {{stat.change > 0 ? '+' : ''}}{{stat.change}}
            </text>
          </view>
        </view>
      </view>

      <!-- 操作按钮 -->
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

    <!-- 推演历史 -->
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
// 推演引擎 - 根据用户输入生成推理分支
class PredictionEngine {
  constructor() {
    this.scenarios = this.buildScenarioDatabase()
  }

  buildScenarioDatabase() {
    return {
      // 工作相关
      '工作': {
        '调岗': {
          branches: [
            { emoji: '📈', title: '新岗位很适合', desc: '你在新岗位发挥出色，获得领导赏识', probability: 35, effects: [{name: '事业', value: 20}, {name: '收入', value: 15}] },
            { emoji: '😰', title: '难以适应', desc: '新岗位要求很高，你感到压力很大', probability: 25, effects: [{name: '事业', value: -10}, {name: '心情', value: -15}] },
            { emoji: '🤝', title: '遇到贵人', desc: '新部门有位前辈很欣赏你，愿意带你', probability: 20, effects: [{name: '人脉', value: 20}, {name: '事业', value: 10}] },
            { emoji: '🚪', title: '选择离职', desc: '你决定不接受调岗，选择离开公司', probability: 15, effects: [{name: '事业', value: -5}, {name: '自由', value: 15}] },
            { emoji: '💰', title: '薪资谈判', desc: '你借机要求加薪，公司同意了', probability: 5, effects: [{name: '收入', value: 25}, {name: '事业', value: 5}] }
          ],
          next: {
            '新岗位很适合': [
              { emoji: '🏆', title: '升职加薪', desc: '半年后你获得晋升，成为团队负责人', probability: 40 },
              { emoji: '✈️', title: '外派机会', desc: '公司派你去海外分部工作', probability: 20 },
              { emoji: '😤', title: '同事嫉妒', desc: '你的优秀引起同事排挤', probability: 25 },
              { emoji: '💼', title: '跳槽邀请', desc: '竞争对手挖你过去', probability: 15 }
            ],
            '难以适应': [
              { emoji: '📚', title: '努力学习', desc: '你加班学习，逐渐跟上节奏', probability: 35 },
              { emoji: '🏥', title: '身体报警', desc: '长期压力导致健康问题', probability: 25 },
              { emoji: '👨‍👩‍👧', title: '家庭矛盾', desc: '工作不顺影响家庭关系', probability: 20 },
              { emoji: '🔄', title: '调回原岗', desc: '领导同意你调回原来岗位', probability: 20 }
            ],
            '遇到贵人': [
              { emoji: '🚀', title: '快速成长', desc: '在贵人指导下，你能力突飞猛进', probability: 45 },
              { emoji: '🤝', title: '合伙创业', desc: '贵人邀请你一起创业', probability: 20 },
              { emoji: '💔', title: '贵人离职', desc: '贵人跳槽了，你失去依靠', probability: 20 },
              { emoji: '📖', title: '学到真传', desc: '你学到了核心技术，成为专家', probability: 15 }
            ],
            '选择离职': [
              { emoji: '🎉', title: '找到更好', desc: '你很快找到更满意的工作', probability: 30 },
              { emoji: '😰', title: '求职困难', desc: '市场环境不好，找工作很难', probability: 30 },
              { emoji: '💻', title: '自由职业', desc: '你决定做自由职业者', probability: 20 },
              { emoji: '📚', title: '考研深造', desc: '你决定回学校继续学习', probability: 20 }
            ]
          }
        },
        '辞职': {
          branches: [
            { emoji: '🎉', title: '找到更好工作', desc: '你很快入职一家更好的公司', probability: 30, effects: [{name: '收入', value: 20}, {name: '心情', value: 15}] },
            { emoji: '😰', title: '求职困难', desc: '市场环境不好，长期找不到工作', probability: 25, effects: [{name: '收入', value: -30}, {name: '心情', value: -20}] },
            { emoji: '💻', title: '自由职业', desc: '你开始做自由职业，收入不稳定', probability: 20, effects: [{name: '自由', value: 25}, {name: '收入', value: -10}] },
            { emoji: '📚', title: '考研/留学', desc: '你决定继续深造', probability: 15, effects: [{name: '学历', value: 20}, {name: '收入', value: -20}] },
            { emoji: '🏠', title: '回家创业', desc: '你回老家创业', probability: 10, effects: [{name: '事业', value: -5}, {name: '家庭', value: 15}] }
          ],
          next: {}
        },
        '面试': {
          branches: [
            { emoji: '🎉', title: '面试通过', desc: '你成功拿到offer', probability: 40, effects: [{name: '事业', value: 15}, {name: '心情', value: 20}] },
            { emoji: '📈', title: '薪资谈判', desc: '面试通过，进入薪资谈判', probability: 20, effects: [{name: '收入', value: 10}] },
            { emoji: '😰', title: '面试失败', desc: '你没有通过面试', probability: 25, effects: [{name: '心情', value: -10}] },
            { emoji: '🤔', title: '考虑其他', desc: '面试后觉得不适合，放弃', probability: 15, effects: [{name: '心情', value: -5}] }
          ],
          next: {}
        },
        '加班': {
          branches: [
            { emoji: '🏆', title: '获得认可', desc: '加班被领导看到，获得表扬', probability: 25, effects: [{name: '事业', value: 10}, {name: '健康', value: -10}] },
            { emoji: '🏥', title: '身体透支', desc: '长期加班导致健康问题', probability: 30, effects: [{name: '健康', value: -20}, {name: '心情', value: -10}] },
            { emoji: '💔', title: '家庭不满', desc: '家人抱怨你只顾工作', probability: 25, effects: [{name: '家庭', value: -15}] },
            { emoji: '📚', title: '能力提升', desc: '加班让你快速成长', probability: 20, effects: [{name: '能力', value: 15}, {name: '健康', value: -5}] }
          ],
          next: {}
        }
      },
      // 感情相关
      '感情': {
        '表白': {
          branches: [
            { emoji: '💕', title: '表白成功', desc: '对方接受了你的心意', probability: 30, effects: [{name: '心情', value: 30}, {name: '感情', value: 25}] },
            { emoji: '💔', title: '被拒绝', desc: '对方婉拒了你', probability: 35, effects: [{name: '心情', value: -20}, {name: '自信', value: -10}] },
            { emoji: '🤔', title: '需要考虑', desc: '对方说需要时间考虑', probability: 20, effects: [{name: '心情', value: -5}] },
            { emoji: '👫', title: '成为朋友', desc: '对方不想恋爱但愿意做朋友', probability: 15, effects: [{name: '人脉', value: 10}, {name: '心情', value: -5}] }
          ],
          next: {
            '表白成功': [
              { emoji: '💑', title: '甜蜜恋爱', desc: '你们开始了幸福的恋爱', probability: 40 },
              { emoji: '💍', title: '很快结婚', desc: '交往不久就决定结婚', probability: 15 },
              { emoji: '😤', title: '发现缺点', desc: '深入了解后发现不合适', probability: 25 },
              { emoji: '🌍', title: '异地恋', desc: '一方需要去外地工作', probability: 20 }
            ],
            '被拒绝': [
              { emoji: '📈', title: '化悲愤为力量', desc: '你专注事业，获得成功', probability: 30 },
              { emoji: '😢', title: '长期低落', desc: '你很久走不出来', probability: 25 },
              { emoji: '👀', title: '遇到更好', desc: '后来遇到更合适的人', probability: 30 },
              { emoji: '🤝', title: '保持联系', desc: '你们还是朋友', probability: 15 }
            ]
          }
        },
        '分手': {
          branches: [
            { emoji: '😢', title: '痛苦期', desc: '你经历了一段痛苦的时期', probability: 40, effects: [{name: '心情', value: -25}] },
            { emoji: '🎉', title: '如释重负', desc: '分手后反而轻松了', probability: 25, effects: [{name: '心情', value: 10}, {name: '自由', value: 15}] },
            { emoji: '🤝', title: '和平分手', desc: '你们友好分手，保持联系', probability: 20, effects: [{name: '人脉', value: 5}] },
            { emoji: '💔', title: '撕破脸', desc: '分手很不愉快', probability: 15, effects: [{name: '心情', value: -15}, {name: '人脉', value: -10}] }
          ],
          next: {}
        },
        '相亲': {
          branches: [
            { emoji: '💕', title: '一见钟情', desc: '你们彼此都很满意', probability: 15, effects: [{name: '感情', value: 20}] },
            { emoji: '🤝', title: '可以接触', desc: '感觉还行，先接触看看', probability: 35, effects: [{name: '感情', value: 5}] },
            { emoji: '😰', title: '不太合适', desc: '聊不来，没有共同话题', probability: 35, effects: [{name: '心情', value: -5}] },
            { emoji: '👋', title: '奇葩经历', desc: '遇到很奇葩的相亲对象', probability: 15, effects: [{name: '心情', value: -10}] }
          ],
          next: {}
        }
      },
      // 学业相关
      '考试': {
        '高考': {
          branches: [
            { emoji: '🎉', title: '超常发挥', desc: '你考出了比平时好的成绩', probability: 15, effects: [{name: '学历', value: 20}, {name: '心情', value: 20}] },
            { emoji: '📚', title: '正常发挥', desc: '成绩和预期差不多', probability: 40, effects: [{name: '学历', value: 10}, {name: '心情', value: 5}] },
            { emoji: '😰', title: '发挥失常', desc: '考试紧张，成绩不理想', probability: 30, effects: [{name: '学历', value: -5}, {name: '心情', value: -15}] },
            { emoji: '📉', title: '严重失误', desc: '出现重大失误，成绩很差', probability: 15, effects: [{name: '学历', value: -15}, {name: '心情', value: -25}] }
          ],
          next: {}
        },
        '考研': {
          branches: [
            { emoji: '🎉', title: '成功上岸', desc: '你考上了理想的学校', probability: 25, effects: [{name: '学历', value: 25}, {name: '心情', value: 20}] },
            { emoji: '📚', title: '调剂录取', desc: '被调剂到其他学校/专业', probability: 25, effects: [{name: '学历', value: 15}, {name: '心情', value: 0}] },
            { emoji: '😰', title: '差几分', desc: '分数不够，未能录取', probability: 30, effects: [{name: '心情', value: -15}] },
            { emoji: '🚪', title: '放弃考研', desc: '考试前决定放弃', probability: 20, effects: [{name: '自由', value: 10}, {name: '学历', value: -5}] }
          ],
          next: {}
        }
      },
      // 投资/财务
      '投资': {
        '股票': {
          branches: [
            { emoji: '📈', title: '大涨', desc: '股票大涨，赚了不少', probability: 15, effects: [{name: '财富', value: 30}, {name: '心情', value: 20}] },
            { emoji: '📊', title: '小涨', desc: '略有盈利', probability: 25, effects: [{name: '财富', value: 10}, {name: '心情', value: 5}] },
            { emoji: '😐', title: '持平', desc: '不赚不赔', probability: 20, effects: [{name: '心情', value: -2}] },
            { emoji: '📉', title: '亏损', desc: '股票下跌，亏了钱', probability: 30, effects: [{name: '财富', value: -15}, {name: '心情', value: -10}] },
            { emoji: '💸', title: '暴跌套牢', desc: '股票暴跌，深度套牢', probability: 10, effects: [{name: '财富', value: -35}, {name: '心情', value: -25}] }
          ],
          next: {}
        },
        '买房': {
          branches: [
            { emoji: '📈', title: '房价大涨', desc: '买完房价就涨了', probability: 25, effects: [{name: '财富', value: 25}, {name: '心情', value: 15}] },
            { emoji: '🏠', title: '安居乐业', desc: '有了自己的家，很踏实', probability: 35, effects: [{name: '心情', value: 10}, {name: '家庭', value: 10}] },
            { emoji: '😰', title: '房贷压力', desc: '每月还贷压力很大', probability: 25, effects: [{name: '财富', value: -15}, {name: '心情', value: -10}] },
            { emoji: '📉', title: '房价下跌', desc: '买完房价跌了', probability: 15, effects: [{name: '财富', value: -20}, {name: '心情', value: -15}] }
          ],
          next: {}
        }
      },
      // 健康
      '健康': {
        '体检': {
          branches: [
            { emoji: '💪', title: '一切正常', desc: '体检结果很好', probability: 40, effects: [{name: '心情', value: 10}, {name: '健康', value: 5}] },
            { emoji: '⚠️', title: '小问题', desc: '发现一些小问题，需要注意', probability: 30, effects: [{name: '心情', value: -5}, {name: '健康', value: -2}] },
            { emoji: '🏥', title: '需要治疗', desc: '发现需要治疗的疾病', probability: 20, effects: [{name: '健康', value: -15}, {name: '财富', value: -10}] },
            { emoji: '😰', title: '严重疾病', desc: '发现严重健康问题', probability: 10, effects: [{name: '健康', value: -30}, {name: '心情', value: -25}] }
          ],
          next: {}
        },
        '生病': {
          branches: [
            { emoji: '💊', title: '很快康复', desc: '休息几天就好了', probability: 45, effects: [{name: '健康', value: 5}] },
            { emoji: '🏥', title: '需要住院', desc: '病情较重，需要住院治疗', probability: 30, effects: [{name: '健康', value: -10}, {name: '财富', value: -10}] },
            { emoji: '😰', title: '转为慢性', desc: '病情转为慢性病，长期影响', probability: 15, effects: [{name: '健康', value: -20}, {name: '心情', value: -10}] },
            { emoji: '💡', title: '改变生活方式', desc: '生病让你开始重视健康', probability: 10, effects: [{name: '健康', value: 15}, {name: '心情', value: 5}] }
          ],
          next: {}
        }
      },
      // 人际关系
      '人际': {
        '吵架': {
          branches: [
            { emoji: '🤝', title: '和解', desc: '双方冷静下来，和好如初', probability: 35, effects: [{name: '人脉', value: 5}, {name: '心情', value: 5}] },
            { emoji: '😤', title: '冷战', desc: '互不搭理，关系降温', probability: 30, effects: [{name: '人脉', value: -10}, {name: '心情', value: -10}] },
            { emoji: '💔', title: '绝交', desc: '关系彻底破裂', probability: 20, effects: [{name: '人脉', value: -20}, {name: '心情', value: -15}] },
            { emoji: '💡', title: '关系升华', desc: '吵完反而更了解彼此', probability: 15, effects: [{name: '人脉', value: 15}, {name: '心情', value: 10}] }
          ],
          next: {}
        },
        '借钱': {
          branches: [
            { emoji: '💰', title: '按时归还', desc: '朋友按时还了钱', probability: 40, effects: [{name: '财富', value: 0}, {name: '人脉', value: 5}] },
            { emoji: '😰', title: '拖延不还', desc: '朋友一直拖着不还', probability: 30, effects: [{name: '财富', value: -10}, {name: '人脉', value: -10}] },
            { emoji: '💔', title: '赖账', desc: '朋友不还钱，关系破裂', probability: 15, effects: [{name: '财富', value: -15}, {name: '人脉', value: -20}] },
            { emoji: '🤝', title: '帮助度过难关', desc: '朋友感激你，关系更好', probability: 15, effects: [{name: '人脉', value: 15}, {name: '心情', value: 5}] }
          ],
          next: {}
        }
      },
      // 意外事件
      '意外': {
        '车祸': {
          branches: [
            { emoji: '🙏', title: '轻微擦伤', desc: '人没事，只是车辆损坏', probability: 40, effects: [{name: '健康', value: -2}, {name: '财富', value: -10}] },
            { emoji: '🏥', title: '受伤住院', desc: '需要住院治疗', probability: 30, effects: [{name: '健康', value: -20}, {name: '财富', value: -15}] },
            { emoji: '⚖️', title: '对方全责', desc: '对方全责，获得赔偿', probability: 15, effects: [{name: '财富', value: 10}] },
            { emoji: '😰', title: '自己责任', desc: '你负主要责任', probability: 15, effects: [{name: '财富', value: -25}, {name: '心情', value: -15}] }
          ],
          next: {}
        },
        '中奖': {
          branches: [
            { emoji: '💰', title: '小额奖金', desc: '中了小奖，开心一下', probability: 50, effects: [{name: '财富', value: 5}, {name: '心情', value: 10}] },
            { emoji: '🎉', title: '大额奖金', desc: '中了大奖，改变生活', probability: 10, effects: [{name: '财富', value: 50}, {name: '心情', value: 30}] },
            { emoji: '📉', title: '投资失败', desc: '奖金投资亏了', probability: 20, effects: [{name: '财富', value: -5}, {name: '心情', value: -5}] },
            { emoji: '👨‍👩‍👧', title: '家庭矛盾', desc: '奖金引发家庭纷争', probability: 20, effects: [{name: '家庭', value: -15}, {name: '心情', value: -10}] }
          ],
          next: {}
        }
      }
    }
  }

  // 智能匹配场景
  matchScenario(input) {
    const text = input.toLowerCase()
    let matchedCategory = null
    let matchedSubCategory = null
    let maxScore = 0

    // 遍历所有场景找最佳匹配
    for (const [category, subs] of Object.entries(this.scenarios)) {
      for (const [sub, data] of Object.entries(subs)) {
        let score = 0
        if (text.includes(category)) score += 3
        if (text.includes(sub)) score += 5
        
        // 关键词匹配
        const keywords = this.getKeywords(category, sub)
        for (const kw of keywords) {
          if (text.includes(kw)) score += 2
        }

        if (score > maxScore) {
          maxScore = score
          matchedCategory = category
          matchedSubCategory = sub
        }
      }
    }

    // 如果没有匹配到，使用通用推演
    if (maxScore === 0) {
      return this.generateGenericBranches(input)
    }

    return this.scenarios[matchedCategory][matchedSubCategory]
  }

  getKeywords(category, sub) {
    const keywordMap = {
      '工作': ['工作', '上班', '公司', '老板', '同事', '职场', '加班', '辞职', '面试', '薪资', '升职'],
      '调岗': ['调岗', '调动', '转岗', '换部门', '岗位调整'],
      '辞职': ['辞职', '离职', '跳槽', '不干', '走人'],
      '面试': ['面试', '应聘', '求职', '找工作'],
      '加班': ['加班', '熬夜', '通宵'],
      '感情': ['感情', '恋爱', '分手', '表白', '相亲', '结婚', '离婚', '对象', '男朋友', '女朋友'],
      '表白': ['表白', '喜欢', '告白', '暗恋'],
      '分手': ['分手', '离婚', '失恋', '劈腿'],
      '相亲': ['相亲', '介绍对象', '媒人'],
      '考试': ['考试', '高考', '考研', '考公', '考编', '考证', '成绩'],
      '高考': ['高考', '中考', '期末考'],
      '考研': ['考研', '研究生', '考博'],
      '投资': ['投资', '股票', '基金', '买房', '理财', '赚钱'],
      '股票': ['股票', '炒股', '股市'],
      '买房': ['买房', '房子', '房产', '楼盘'],
      '健康': ['健康', '体检', '生病', '医院', '病', '身体'],
      '体检': ['体检', '检查'],
      '生病': ['生病', '感冒', '发烧', '住院'],
      '人际': ['人际', '吵架', '矛盾', '朋友', '借钱', '关系'],
      '吵架': ['吵架', '争吵', '冲突', '矛盾'],
      '借钱': ['借钱', '借给', '欠款'],
      '意外': ['意外', '车祸', '中奖', '倒霉', '幸运']
    }
    return keywordMap[sub] || keywordMap[category] || []
  }

  // 通用推演（当没有匹配到具体场景时）
  generateGenericBranches(input) {
    return {
      branches: [
        { emoji: '📈', title: '事情向好发展', desc: '这件事会有一个不错的结果', probability: 30, effects: [{name: '心情', value: 15}] },
        { emoji: '😐', title: '平淡收场', desc: '事情没有大的波澜，平平常常', probability: 25, effects: [{name: '心情', value: 0}] },
        { emoji: '⚠️', title: '遇到挑战', desc: '过程中会遇到一些困难', probability: 25, effects: [{name: '心情', value: -5}, {name: '能力', value: 10}] },
        { emoji: '😰', title: '结果不理想', desc: '事情的发展不如预期', probability: 15, effects: [{name: '心情', value: -15}] },
        { emoji: '💡', title: '意外转机', desc: '会出现意想不到的转机', probability: 5, effects: [{name: '心情', value: 10}, {name: '机遇', value: 15}] }
      ],
      next: {
        '事情向好发展': [
          { emoji: '🎉', title: '超出预期', desc: '结果比想象的还要好', probability: 35 },
          { emoji: '📈', title: '持续向好', desc: '这件事带来连锁的好影响', probability: 35 },
          { emoji: '🤝', title: '获得帮助', desc: '有人在这个过程中帮助你', probability: 30 }
        ],
        '遇到挑战': [
          { emoji: '💪', title: '克服困难', desc: '你成功克服了困难', probability: 40 },
          { emoji: '📚', title: '学到经验', desc: '虽然艰难，但学到了很多', probability: 30 },
          { emoji: '😰', title: '需要放弃', desc: '困难太大，不得不放弃', probability: 30 }
        ],
        '结果不理想': [
          { emoji: '🔄', title: '重新来过', desc: '你决定再试一次', probability: 35 },
          { emoji: '💡', title: '找到替代', desc: '你发现了一条新的路', probability: 35 },
          { emoji: '😔', title: '暂时搁置', desc: '先放下，以后再说', probability: 30 }
        ]
      }
    }
  }

  // 生成下一层分支
  generateNextBranches(selectedBranch, currentLevel) {
    if (selectedBranch.next && selectedBranch.next.length > 0) {
      return selectedBranch.next
    }
    
    // 如果没有预定义的下层，生成通用后续
    const genericNext = [
      { emoji: '📈', title: '持续影响', desc: '这件事继续产生后续影响', probability: 30 },
      { emoji: '🔄', title: '新的变化', desc: '情况出现新的变化', probability: 25 },
      { emoji: '🎯', title: '尘埃落定', desc: '事情基本有了定论', probability: 25 },
      { emoji: '💡', title: '意外发展', desc: '出现意想不到的新情况', probability: 20 }
    ]
    
    return genericNext
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
        { name: '深层', desc: '推演3层', value: 3 },
        { name: '完整', desc: '推演4层', value: 4 }
      ],
      isPredicting: false,
      showingResult: false,
      showHistory: false,
      branchTree: [],
      selectedPath: [],
      finalSummary: '',
      pathStats: null,
      canContinue: false,
      currentBranch: null,
      engine: null,
      predictionHistory: []
    }
  },
  onShow() {
    this.loadHistory()
    this.engine = new PredictionEngine()
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
      this.pathStats = null
      
      // 模拟推演延迟
      await this.delay(800)
      
      // 匹配场景
      const scenario = this.engine.matchScenario(this.userEvent)
      
      // 生成第一层
      const level1 = scenario.branches.map(b => ({
        ...b,
        selected: false,
        faded: false,
        canContinue: true,
        level: 0
      }))
      
      this.branchTree.push(level1)
      
      // 根据深度预生成后续层
      for (let i = 1; i < this.depth; i++) {
        await this.delay(400)
        const prevLevel = this.branchTree[i - 1]
        const nextLevel = []
        
        for (const branch of prevLevel) {
          const nextBranches = this.engine.generateNextBranches(branch, i)
          nextBranches.forEach(b => {
            nextLevel.push({
              ...b,
              selected: false,
              faded: false,
              canContinue: i < 3,
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
      
      // 保存到历史
      this.saveToHistory()
    },

    selectBranch(branch, levelIndex, branchIndex) {
      // 标记选中状态
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
      
      // 计算路径统计
      this.calculatePathStats()
      
      // 生成总结
      this.generateSummary()
      
      this.currentBranch = branch
    },

    continuePrediction() {
      if (!this.currentBranch) {
        uni.showToast({ title: '请先选择一个分支', icon: 'none' })
        return
      }
      
      const currentLevel = this.currentBranch.level
      
      // 如果已经有下一层，显示出来
      if (currentLevel + 1 < this.branchTree.length) {
        // 取消下层的选择状态
        this.branchTree[currentLevel + 1].forEach(b => {
          b.faded = false
        })
      } else {
        // 生成新的一层
        const nextBranches = this.engine.generateNextBranches(this.currentBranch, currentLevel + 1)
        const newLevel = nextBranches.map(b => ({
          ...b,
          selected: false,
          faded: false,
          canContinue: currentLevel < 3,
          level: currentLevel + 1,
          parent: this.currentBranch.title
        }))
        
        this.branchTree.push(newLevel)
      }
      
      this.canContinue = currentLevel < 3
    },

    calculatePathStats() {
      const stats = {
        心情: { emoji: '😊', name: '心情', change: 0 },
        财富: { emoji: '💰', name: '财富', change: 0 },
        健康: { emoji: '❤️', name: '健康', change: 0 },
        人脉: { emoji: '🤝', name: '人脉', change: 0 },
        事业: { emoji: '💼', name: '事业', change: 0 }
      }
      
      this.selectedPath.forEach(branch => {
        if (branch.effects) {
          branch.effects.forEach(effect => {
            if (stats[effect.name]) {
              stats[effect.name].change += effect.value
            }
          })
        }
      })
      
      // 只显示有变化的
      this.pathStats = {}
      Object.entries(stats).forEach(([key, val]) => {
        if (val.change !== 0) {
          this.pathStats[key] = val
        }
      })
    },

    generateSummary() {
      if (this.selectedPath.length === 0) return
      
      const lastBranch = this.selectedPath[this.selectedPath.length - 1]
      const pathNames = this.selectedPath.map(p => p.title).join(' → ')
      
      let summary = `你选择了「${pathNames}」这条路径。`
      
      // 根据最终分支生成总结
      if (lastBranch.probability >= 35) {
        summary += '这是比较可能发生的方向。'
      } else if (lastBranch.probability >= 20) {
        summary += '这是有一定可能性的方向。'
      } else {
        summary += '这是小概率事件，但也不是不可能。'
      }
      
      // 根据属性变化给出建议
      const hasNegative = Object.values(this.pathStats).some(s => s.change < 0)
      const hasPositive = Object.values(this.pathStats).some(s => s.change > 0)
      
      if (hasNegative && !hasPositive) {
        summary += '这条路径整体偏负面，建议谨慎考虑或寻找替代方案。'
      } else if (hasPositive && !hasNegative) {
        summary += '这条路径整体偏正面，值得尝试。'
      } else if (hasPositive && hasNegative) {
        summary += '这条路径有利有弊，需要权衡取舍。'
      }
      
      this.finalSummary = summary
    },

    resetPrediction() {
      this.showingResult = false
      this.userEvent = ''
      this.userChoice = ''
      this.branchTree = []
      this.selectedPath = []
      this.finalSummary = ''
      this.pathStats = null
      this.currentBranch = null
    },

    shareResult() {
      if (this.selectedPath.length === 0) {
        uni.showToast({ title: '请先选择一条路径', icon: 'none' })
        return
      }
      
      const pathText = this.selectedPath.map(p => p.title).join(' → ')
      const shareText = `我在【蝴蝶效应】推演了一件生活事件：\n\n「${this.userEvent}」\n\n推演路径：${pathText}\n\n${this.finalSummary}`
      
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
  min-height: 160rpx;
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

/* 分支树 */
.branch-tree {
  margin-bottom: 20rpx;
}

.tree-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 20rpx;
}

.branch-level {
  margin-bottom: 24rpx;
}

.level-label {
  font-size: 24rpx;
  color: #a0aec0;
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
  color: #667eea;
  font-weight: bold;
  background: rgba(102, 126, 234, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
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

/* 时间线视图 */
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
  left: 15rpx;
  top: 40rpx;
  width: 2rpx;
  height: calc(100% - 20rpx);
  background: #e2e8f0;
}

.path-dot {
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin-right: 16rpx;
  flex-shrink: 0;
  margin-top: 4rpx;
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

/* 总结卡片 */
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

.summary-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.ps-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  background: #f7fafc;
  padding: 12rpx 20rpx;
  border-radius: 12rpx;
}

.ps-emoji {
  font-size: 28rpx;
}

.ps-name {
  font-size: 24rpx;
  color: #4a5568;
}

.ps-value {
  font-size: 26rpx;
  font-weight: bold;
}

.ps-up {
  color: #48bb78;
}

.ps-down {
  color: #e53e3e;
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
