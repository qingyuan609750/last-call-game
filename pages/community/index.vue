<template>
  <view class="container">
    <!-- 社区头部 -->
    <view class="community-header">
      <view class="header-bg">
        <text class="header-title">🌈 时光社区</text>
        <text class="header-desc">匿名分享，温暖彼此</text>
        <view class="header-stats">
          <view class="stat-item">
            <text class="stat-num">{{onlineUsers}}</text>
            <text class="stat-label">在线</text>
          </view>
          <view class="stat-item">
            <text class="stat-num">{{totalPosts}}</text>
            <text class="stat-label">帖子</text>
          </view>
          <view class="stat-item">
            <text class="stat-num">{{todayPosts}}</text>
            <text class="stat-label">今日</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 话题标签 -->
    <view class="topic-section">
      <scroll-view class="topic-scroll" scroll-x>
        <view 
          class="topic-tag" 
          v-for="(topic, index) in topics" 
          :key="index"
          :class="{'topic-active': currentTopic === topic}"
          @click="selectTopic(topic)"
        >
          {{topic}}
        </view>
      </scroll-view>
    </view>

    <!-- 发布框 -->
    <view class="post-input-section">
      <view class="input-card" @click="showPostForm = true">
        <text class="input-placeholder">💭 分享你的心情、故事或愿望...</text>
        <text class="input-btn">发布</text>
      </view>
    </view>

    <!-- 帖子列表 -->
    <view class="posts-section">
      <view class="post-card" v-for="(post, index) in filteredPosts" :key="post.id">
        <!-- 帖子头部 -->
        <view class="post-header">
          <view class="user-info">
            <view class="avatar" :style="{background: post.avatarColor}">
              <text class="avatar-text">{{post.nickname[0]}}</text>
            </view>
            <view class="user-meta">
              <text class="nickname">{{post.nickname}}</text>
              <text class="post-time">{{timeAgo(post.time)}}</text>
            </view>
          </view>
          <view class="post-topic">{{post.topic}}</view>
        </view>

        <!-- 帖子内容 -->
        <view class="post-content" @click="goToDetail(post)">
          <text class="post-text">{{post.content}}</text>
          <view class="post-images" v-if="post.images.length > 0">
            <image 
              v-for="(img, i) in post.images" 
              :key="i"
              :src="img" 
              mode="aspectFill" 
              class="post-image"
              @click.stop="previewImage(post.images, i)"
            />
          </view>
        </view>

        <!-- 帖子底部 -->
        <view class="post-footer">
          <view class="action-btn" :class="{'active': post.isLiked}" @click="toggleLike(post)">
            <text class="action-icon">{{post.isLiked ? '❤️' : '🤍'}}</text>
            <text class="action-num">{{post.likes}}</text>
          </view>
          <view class="action-btn" @click="goToDetail(post)">
            <text class="action-icon">💬</text>
            <text class="action-num">{{post.comments.length}}</text>
          </view>
          <view class="action-btn" @click="sharePost(post)">
            <text class="action-icon">🔗</text>
            <text class="action-text">分享</text>
          </view>
        </view>

        <!-- 热门评论预览 -->
        <view class="comments-preview" v-if="post.comments.length > 0">
          <view class="comment-item" v-for="(comment, i) in post.comments.slice(0, 2)" :key="i">
            <text class="comment-name">{{comment.nickname}}：</text>
            <text class="comment-text">{{comment.content}}</text>
          </view>
          <text class="more-comments" v-if="post.comments.length > 2" @click="goToDetail(post)">
            查看全部{{post.comments.length}}条评论
          </text>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view class="empty-state" v-if="filteredPosts.length === 0">
      <text class="empty-icon">📝</text>
      <text class="empty-text">还没有帖子</text>
      <text class="empty-desc">成为第一个分享的人吧</text>
    </view>

    <!-- 发布弹窗 -->
    <view class="modal" v-if="showPostForm">
      <view class="modal-mask" @click="showPostForm = false"></view>
      <view class="modal-content">
        <view class="modal-header">
          <text class="modal-title">发布帖子</text>
          <text class="modal-close" @click="showPostForm = false">✕</text>
        </view>
        
        <!-- 话题选择 -->
        <scroll-view class="modal-topics" scroll-x>
          <view 
            class="modal-topic" 
            v-for="(topic, index) in topics.filter(t => t !== '全部')" 
            :key="index"
            :class="{'modal-topic-active': postTopic === topic}"
            @click="postTopic = topic"
          >
            {{topic}}
          </view>
        </scroll-view>

        <!-- 输入框 -->
        <textarea 
          class="post-textarea" 
          v-model="postContent"
          placeholder="分享你的想法..."
          maxlength="500"
        />
        <text class="word-count">{{postContent.length}}/500</text>

        <!-- 图片 -->
        <view class="image-section">
          <view class="image-list">
            <view class="image-item" v-for="(img, index) in postImages" :key="index">
              <image :src="img" mode="aspectFill" class="selected-image" />
              <view class="image-delete" @click="removeImage(index)">×</view>
            </view>
            <view class="image-add" @click="chooseImage" v-if="postImages.length < 3">
              <text class="add-icon">+</text>
            </view>
          </view>
        </view>

        <!-- 匿名设置 -->
        <view class="anonymous-setting">
          <text class="setting-label">匿名发布</text>
          <switch :checked="isAnonymous" @change="isAnonymous = !isAnonymous" color="#667eea" />
        </view>

        <button class="submit-btn" @click="submitPost">发布</button>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      onlineUsers: 128,
      totalPosts: 0,
      todayPosts: 0,
      currentTopic: '全部',
      topics: ['全部', '心情日记', '时光信', '挑战打卡', '愿望清单', '情感树洞', '生活感悟', '求助问答'],
      showPostForm: false,
      postContent: '',
      postImages: [],
      postTopic: '心情日记',
      isAnonymous: true,
      posts: []
    }
  },
  computed: {
    filteredPosts() {
      if (this.currentTopic === '全部') {
        return this.posts.sort((a, b) => b.time - a.time)
      }
      return this.posts.filter(p => p.topic === this.currentTopic).sort((a, b) => b.time - a.time)
    }
  },
  onShow() {
    this.loadPosts()
    this.updateStats()
  },
  methods: {
    loadPosts() {
      // 从本地存储加载，实际项目中应该从服务器获取
      let posts = uni.getStorageSync('communityPosts')
      if (!posts || posts.length === 0) {
        // 初始化一些示例数据
        posts = this.getDemoPosts()
        uni.setStorageSync('communityPosts', posts)
      }
      this.posts = posts
      this.updateStats()
    },
    getDemoPosts() {
      const nicknames = ['时光旅人', '追梦者', '星空下的猫', '向日葵', '海风', '山间的风', '小确幸', '夜行者']
      const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#ff9a9e', '#30cfd0', '#f6ad55']
      return [
        {
          id: 1,
          nickname: '时光旅人',
          avatarColor: '#667eea',
          topic: '心情日记',
          content: '今天写了一封给一年后自己的信，希望到时候打开会有惊喜。生活中的小确幸，就是给未来的自己留一份期待。',
          images: [],
          likes: 23,
          isLiked: false,
          comments: [
            { nickname: '追梦者', content: '我也写过，打开的时候真的很有感触' },
            { nickname: '向日葵', content: '加油，未来一定会更好的' }
          ],
          time: Date.now() - 3600000
        },
        {
          id: 2,
          nickname: '星空下的猫',
          avatarColor: '#f093fb',
          topic: '挑战打卡',
          content: '七日挑战第5天！每天坚持运动30分钟，感觉精神状态好了很多。有人一起打卡吗？',
          images: [],
          likes: 45,
          isLiked: false,
          comments: [
            { nickname: '海风', content: '我也在坚持，一起加油！' },
            { nickname: '山间的风', content: '第3天，有点累但会坚持的' }
          ],
          time: Date.now() - 7200000
        },
        {
          id: 3,
          nickname: '小确幸',
          avatarColor: '#43e97b',
          topic: '愿望清单',
          content: '在未来商店兑换了"旅行基金"，目标存够1000积分去云南！有推荐的地方吗？',
          images: [],
          likes: 18,
          isLiked: false,
          comments: [
            { nickname: '夜行者', content: '大理和丽江都很棒，推荐！' }
          ],
          time: Date.now() - 10800000
        },
        {
          id: 4,
          nickname: '海风',
          avatarColor: '#4facfe',
          topic: '情感树洞',
          content: '最近有点迷茫，工作不顺心，感情也不顺利。但是每天记录心情后，发现其实生活还是有很多美好的瞬间。',
          images: [],
          likes: 56,
          isLiked: false,
          comments: [
            { nickname: '时光旅人', content: '抱抱，一切都会好起来的' },
            { nickname: '向日葵', content: '相信自己，你是最棒的' },
            { nickname: '追梦者', content: '迷茫是暂时的，坚持记录会有收获的' }
          ],
          time: Date.now() - 14400000
        }
      ]
    },
    updateStats() {
      this.totalPosts = this.posts.length
      const today = new Date().setHours(0, 0, 0, 0)
      this.todayPosts = this.posts.filter(p => p.time >= today).length
    },
    selectTopic(topic) {
      this.currentTopic = topic
    },
    chooseImage() {
      uni.chooseImage({
        count: 3 - this.postImages.length,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.postImages = [...this.postImages, ...res.tempFilePaths]
        }
      })
    },
    removeImage(index) {
      this.postImages.splice(index, 1)
    },
    submitPost() {
      if (!this.postContent.trim()) {
        uni.showToast({ title: '请输入内容', icon: 'none' })
        return
      }

      const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#ff9a9e', '#30cfd0', '#f6ad55']
      const randomNicknames = ['时光旅人', '追梦者', '星空下的猫', '向日葵', '海风', '山间的风', '小确幸', '夜行者']
      
      const post = {
        id: Date.now(),
        nickname: this.isAnonymous ? randomNicknames[Math.floor(Math.random() * randomNicknames.length)] : '我',
        avatarColor: colors[Math.floor(Math.random() * colors.length)],
        topic: this.postTopic,
        content: this.postContent,
        images: this.postImages,
        likes: 0,
        isLiked: false,
        comments: [],
        time: Date.now()
      }

      this.posts.unshift(post)
      uni.setStorageSync('communityPosts', this.posts)

      // 重置表单
      this.postContent = ''
      this.postImages = []
      this.showPostForm = false
      this.updateStats()

      uni.showToast({ title: '发布成功', icon: 'success' })
    },
    toggleLike(post) {
      post.isLiked = !post.isLiked
      post.likes += post.isLiked ? 1 : -1
      uni.setStorageSync('communityPosts', this.posts)
    },
    goToDetail(post) {
      uni.navigateTo({
        url: `/pages/community/detail?id=${post.id}`
      })
    },
    sharePost(post) {
      uni.showShareMenu({
        withShareTicket: true,
        menus: ['shareAppMessage', 'shareTimeline']
      })
    },
    previewImage(images, current) {
      uni.previewImage({
        urls: images,
        current: images[current]
      })
    },
    timeAgo(timestamp) {
      const diff = Date.now() - timestamp
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)

      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      if (days < 30) return `${days}天前`
      return '很久以前'
    }
  }
}
</script>

<style scoped>
.container {
  background: linear-gradient(180deg, #f8f9fc 0%, #eef2f7 100%);
  min-height: 100vh;
}

/* 头部 */
.community-header {
  padding: 30rpx 30rpx 20rpx;
}

.header-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
  color: #fff;
}

.header-title {
  font-size: 40rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 8rpx;
}

.header-desc {
  font-size: 26rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 24rpx;
}

.header-stats {
  display: flex;
  justify-content: center;
  gap: 40rpx;
}

.stat-item {
  text-align: center;
}

.stat-num {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
}

.stat-label {
  font-size: 22rpx;
  opacity: 0.8;
}

/* 话题标签 */
.topic-section {
  padding: 0 30rpx 20rpx;
}

.topic-scroll {
  white-space: nowrap;
}

.topic-tag {
  display: inline-block;
  padding: 12rpx 24rpx;
  background: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
  color: #718096;
  margin-right: 16rpx;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.06);
}

.topic-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

/* 发布框 */
.post-input-section {
  padding: 0 30rpx 20rpx;
}

.input-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.06);
}

.input-placeholder {
  font-size: 28rpx;
  color: #a0aec0;
}

.input-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 26rpx;
  padding: 12rpx 24rpx;
  border-radius: 24rpx;
}

/* 帖子列表 */
.posts-section {
  padding: 0 30rpx;
}

.post-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-text {
  font-size: 28rpx;
  color: #fff;
  font-weight: bold;
}

.user-meta {
  flex: 1;
}

.nickname {
  font-size: 28rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
}

.post-time {
  font-size: 22rpx;
  color: #a0aec0;
}

.post-topic {
  font-size: 22rpx;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
}

.post-content {
  margin-bottom: 16rpx;
}

.post-text {
  font-size: 28rpx;
  color: #4a5568;
  line-height: 1.6;
  display: block;
  margin-bottom: 12rpx;
}

.post-images {
  display: flex;
  gap: 12rpx;
  flex-wrap: wrap;
}

.post-image {
  width: 200rpx;
  height: 200rpx;
  border-radius: 12rpx;
}

.post-footer {
  display: flex;
  gap: 30rpx;
  padding-top: 16rpx;
  border-top: 1rpx solid #f0f0f0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.action-btn.active .action-num {
  color: #e53e3e;
}

.action-icon {
  font-size: 32rpx;
}

.action-num {
  font-size: 24rpx;
  color: #718096;
}

.action-text {
  font-size: 24rpx;
  color: #718096;
}

/* 评论预览 */
.comments-preview {
  background: #f7fafc;
  border-radius: 12rpx;
  padding: 16rpx;
  margin-top: 16rpx;
}

.comment-item {
  margin-bottom: 8rpx;
}

.comment-name {
  font-size: 24rpx;
  color: #667eea;
  font-weight: bold;
}

.comment-text {
  font-size: 24rpx;
  color: #4a5568;
}

.more-comments {
  font-size: 24rpx;
  color: #a0aec0;
  display: block;
  margin-top: 8rpx;
}

/* 空状态 */
.empty-state {
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

/* 弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: flex-end;
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
  border-radius: 24rpx 24rpx 0 0;
  padding: 30rpx;
  width: 100%;
  position: relative;
  z-index: 1001;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
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

.modal-topics {
  white-space: nowrap;
  margin-bottom: 20rpx;
}

.modal-topic {
  display: inline-block;
  padding: 10rpx 20rpx;
  background: #f7fafc;
  border-radius: 20rpx;
  font-size: 24rpx;
  color: #718096;
  margin-right: 12rpx;
}

.modal-topic-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.post-textarea {
  width: 100%;
  min-height: 200rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: #2d3748;
  margin-bottom: 10rpx;
}

.word-count {
  font-size: 22rpx;
  color: #a0aec0;
  text-align: right;
  display: block;
  margin-bottom: 16rpx;
}

.image-section {
  margin-bottom: 20rpx;
}

.image-list {
  display: flex;
  gap: 16rpx;
}

.image-item {
  position: relative;
  width: 160rpx;
  height: 160rpx;
}

.selected-image {
  width: 100%;
  height: 100%;
  border-radius: 12rpx;
}

.image-delete {
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

.image-add {
  width: 160rpx;
  height: 160rpx;
  background: #f7fafc;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2rpx dashed #cbd5e0;
}

.anonymous-setting {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.setting-label {
  font-size: 28rpx;
  color: #2d3748;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 30rpx;
  border: none;
}
</style>
