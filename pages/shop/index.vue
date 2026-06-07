<template>
  <view class="container">
    <view class="shop-header">
      <view class="user-points">
        <text class="points-icon">💎</text>
        <text class="points-value">{{userPoints}}</text>
        <text class="points-label">积分</text>
      </view>
      <text class="shop-title">🛒 未来商店</text>
      <text class="shop-desc">完成挑战赚取积分，兑换未来愿望</text>
    </view>

    <!-- 愿望清单 -->
    <view class="wish-section">
      <view class="section-header">
        <text class="section-title">我的愿望清单</text>
        <text class="add-wish" @click="showAddWish">+ 添加愿望</text>
      </view>
      
      <view class="wish-list" v-if="wishes.length > 0">
        <view 
          class="wish-card" 
          v-for="(wish, index) in wishes" 
          :key="wish.id"
          :class="{'wish-completed': wish.completed}"
        >
          <view class="wish-info">
            <text class="wish-emoji">{{wish.emoji}}</text>
            <view class="wish-detail">
              <text class="wish-name">{{wish.name}}</text>
              <text class="wish-desc">{{wish.desc}}</text>
            </view>
          </view>
          <view class="wish-action">
            <text class="wish-cost">{{wish.cost}}积分</text>
            <button 
              class="exchange-btn" 
              :class="{'can-exchange': userPoints >= wish.cost && !wish.completed}"
              @click="exchangeWish(wish)"
              :disabled="userPoints < wish.cost || wish.completed"
            >
              {{wish.completed ? '已兑换' : '兑换'}}
            </button>
          </view>
        </view>
      </view>
      
      <view class="empty-wish" v-else>
        <text class="empty-icon">🌟</text>
        <text class="empty-text">还没有愿望</text>
        <text class="empty-desc">添加你的第一个愿望吧</text>
      </view>
    </view>

    <!-- 积分获取方式 -->
    <view class="earn-section">
      <text class="section-title">赚取积分</text>
      <view class="earn-list">
        <view class="earn-item" v-for="(task, index) in earnTasks" :key="index">
          <view class="earn-icon">{{task.emoji}}</view>
          <view class="earn-info">
            <text class="earn-name">{{task.name}}</text>
            <text class="earn-desc">{{task.desc}}</text>
          </view>
          <text class="earn-reward">+{{task.points}}</text>
        </view>
      </view>
    </view>

    <!-- 添加愿望弹窗 -->
    <view class="modal" v-if="showModal">
      <view class="modal-mask" @click="hideModal"></view>
      <view class="modal-content">
        <text class="modal-title">添加新愿望</text>
        <input class="modal-input" v-model="newWish.name" placeholder="愿望名称" />
        <input class="modal-input" v-model="newWish.desc" placeholder="愿望描述" />
        <input class="modal-input" v-model="newWish.cost" type="number" placeholder="所需积分" />
        <view class="emoji-select">
          <text 
            class="emoji-option" 
            v-for="(emoji, index) in emojis" 
            :key="index"
            :class="{'emoji-selected': newWish.emoji === emoji}"
            @click="newWish.emoji = emoji"
          >{{emoji}}</text>
        </view>
        <button class="modal-btn" @click="addWish">确认添加</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      userPoints: 100,
      showModal: false,
      wishes: [
        { id: 1, emoji: '📱', name: '换新手机', desc: '努力攒钱换一部新手机', cost: 500, completed: false },
        { id: 2, emoji: '✈️', name: '旅行基金', desc: '去一个想去的地方旅行', cost: 1000, completed: false },
        { id: 3, emoji: '📚', name: '买书基金', desc: '买10本喜欢的书', cost: 200, completed: false },
        { id: 4, emoji: '🎮', name: '游戏时间', desc: '奖励自己2小时游戏时间', cost: 50, completed: false }
      ],
      earnTasks: [
        { emoji: '🎯', name: '完成七日挑战', desc: '完成一个7天挑战', points: 100 },
        { emoji: '📝', name: '写日记', desc: '连续写日记7天', points: 50 },
        { emoji: '📸', name: '记忆快照', desc: '记录今日心情', points: 10 },
        { emoji: '🎰', name: '命运转盘', desc: '完成转盘挑战', points: 20 },
        { emoji: '📮', name: '时光信笺', desc: '写一封给未来的信', points: 30 }
      ],
      newWish: {
        emoji: '🌟',
        name: '',
        desc: '',
        cost: 100
      },
      emojis: ['🌟', '🎁', '🎯', '✈️', '📱', '📚', '🎮', '🏠', '🚗', '💼', '🎨', '🎵']
    }
  },
  onShow() {
    this.loadPoints()
    this.loadWishes()
  },
  methods: {
    loadPoints() {
      const points = uni.getStorageSync('userPoints')
      if (points !== undefined) {
        this.userPoints = points
      }
    },
    loadWishes() {
      const wishes = uni.getStorageSync('wishes')
      if (wishes) {
        this.wishes = wishes
      }
    },
    showAddWish() {
      this.showModal = true
      this.newWish = { emoji: '🌟', name: '', desc: '', cost: 100 }
    },
    hideModal() {
      this.showModal = false
    },
    addWish() {
      if (!this.newWish.name || !this.newWish.cost) {
        uni.showToast({ title: '请填写完整信息', icon: 'none' })
        return
      }
      
      const wish = {
        id: Date.now(),
        ...this.newWish,
        completed: false
      }
      
      this.wishes.push(wish)
      uni.setStorageSync('wishes', this.wishes)
      this.hideModal()
      uni.showToast({ title: '添加成功', icon: 'success' })
    },
    exchangeWish(wish) {
      if (this.userPoints < wish.cost) {
        uni.showToast({ title: '积分不足', icon: 'none' })
        return
      }
      
      uni.showModal({
        title: '确认兑换',
        content: `确定花费 ${wish.cost} 积分兑换"${wish.name}"吗？`,
        success: (res) => {
          if (res.confirm) {
            this.userPoints -= wish.cost
            wish.completed = true
            uni.setStorageSync('userPoints', this.userPoints)
            uni.setStorageSync('wishes', this.wishes)
            uni.showToast({ title: '兑换成功', icon: 'success' })
          }
        }
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

.shop-header {
  text-align: center;
  margin-bottom: 30rpx;
}

.user-points {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50rpx;
  padding: 16rpx 40rpx;
  margin-bottom: 20rpx;
}

.points-icon {
  font-size: 36rpx;
  margin-right: 12rpx;
}

.points-value {
  font-size: 40rpx;
  font-weight: bold;
  color: #fff;
  margin-right: 8rpx;
}

.points-label {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
}

.shop-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.shop-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 愿望清单 */
.wish-section {
  margin-bottom: 30rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
}

.add-wish {
  font-size: 26rpx;
  color: #667eea;
}

.wish-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.wish-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

.wish-completed {
  opacity: 0.6;
  background: #f7fafc;
}

.wish-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.wish-emoji {
  font-size: 48rpx;
  margin-right: 20rpx;
}

.wish-detail {
  flex: 1;
}

.wish-name {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.wish-desc {
  font-size: 24rpx;
  color: #a0aec0;
}

.wish-action {
  text-align: center;
}

.wish-cost {
  font-size: 24rpx;
  color: #667eea;
  display: block;
  margin-bottom: 8rpx;
}

.exchange-btn {
  background: #e2e8f0;
  color: #a0aec0;
  border-radius: 30rpx;
  padding: 12rpx 30rpx;
  font-size: 24rpx;
  border: none;
  min-width: 100rpx;
}

.can-exchange {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.empty-wish {
  text-align: center;
  padding: 60rpx;
  background: #fff;
  border-radius: 20rpx;
}

.empty-icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 16rpx;
}

.empty-text {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 8rpx;
}

.empty-desc {
  font-size: 24rpx;
  color: #a0aec0;
}

/* 赚取积分 */
.earn-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.earn-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.earn-item {
  display: flex;
  align-items: center;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f0f0f0;
}

.earn-item:last-child {
  border-bottom: none;
}

.earn-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.earn-info {
  flex: 1;
}

.earn-name {
  font-size: 28rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 4rpx;
}

.earn-desc {
  font-size: 22rpx;
  color: #a0aec0;
}

.earn-reward {
  font-size: 28rpx;
  font-weight: bold;
  color: #48bb78;
}

/* 弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
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
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx;
  width: 80%;
  position: relative;
  z-index: 1001;
}

.modal-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  text-align: center;
  margin-bottom: 30rpx;
}

.modal-input {
  width: 100%;
  height: 80rpx;
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  color: #2d3748;
  margin-bottom: 16rpx;
}

.emoji-select {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 24rpx;
  justify-content: center;
}

.emoji-option {
  font-size: 40rpx;
  padding: 10rpx;
  border-radius: 12rpx;
  background: #f7fafc;
}

.emoji-selected {
  background: rgba(102, 126, 234, 0.2);
}

.modal-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 30rpx;
  border: none;
}
</style>
