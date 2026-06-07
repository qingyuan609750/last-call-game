<template>
  <view class="container">
    <!-- 帖子详情 -->
    <view class="post-detail" v-if="post">
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
      <view class="post-content">
        <text class="post-text">{{post.content}}</text>
        <view class="post-images" v-if="post.images.length > 0">
          <image 
            v-for="(img, i) in post.images" 
            :key="i"
            :src="img" 
            mode="aspectFill" 
            class="post-image"
            @click="previewImage(post.images, i)"
          />
        </view>
      </view>

      <!-- 帖子操作 -->
      <view class="post-actions">
        <view class="action-btn" :class="{'active': post.isLiked}" @click="toggleLike">
          <text class="action-icon">{{post.isLiked ? '❤️' : '🤍'}}</text>
          <text class="action-num">{{post.likes}}</text>
        </view>
        <view class="action-btn">
          <text class="action-icon">💬</text>
          <text class="action-num">{{post.comments.length}}</text>
        </view>
        <view class="action-btn" @click="sharePost">
          <text class="action-icon">🔗</text>
          <text class="action-text">分享</text>
        </view>
      </view>
    </view>

    <!-- 评论区域 -->
    <view class="comments-section" v-if="post">
      <text class="section-title">评论 ({{post.comments.length}})</text>
      
      <view class="comment-list">
        <view class="comment-card" v-for="(comment, index) in post.comments" :key="index">
          <view class="comment-avatar" :style="{background: comment.avatarColor || '#667eea'}">
            <text class="comment-avatar-text">{{comment.nickname[0]}}</text>
          </view>
          <view class="comment-body">
            <view class="comment-header">
              <text class="comment-name">{{comment.nickname}}</text>
              <text class="comment-time">{{timeAgo(comment.time)}}</text>
            </view>
            <text class="comment-content">{{comment.content}}</text>
          </view>
        </view>
      </view>

      <!-- 空评论 -->
      <view class="empty-comments" v-if="post.comments.length === 0">
        <text class="empty-icon">💬</text>
        <text class="empty-text">还没有评论</text>
        <text class="empty-desc">来说点什么吧</text>
      </view>
    </view>

    <!-- 底部评论输入 -->
    <view class="comment-input-bar">
      <input 
        class="comment-input" 
        v-model="commentContent"
        placeholder="写下你的评论..."
        confirm-type="send"
        @confirm="submitComment"
      />
      <button class="send-btn" @click="submitComment">发送</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      post: null,
      postId: '',
      commentContent: ''
    }
  },
  onLoad(options) {
    this.postId = options.id
    this.loadPost()
  },
  methods: {
    loadPost() {
      const posts = uni.getStorageSync('communityPosts') || []
      this.post = posts.find(p => p.id == this.postId)
    },
    toggleLike() {
      if (!this.post) return
      this.post.isLiked = !this.post.isLiked
      this.post.likes += this.post.isLiked ? 1 : -1
      this.savePosts()
    },
    submitComment() {
      if (!this.commentContent.trim()) {
        uni.showToast({ title: '请输入评论', icon: 'none' })
        return
      }

      const colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#ff9a9e']
      const randomNames = ['时光旅人', '追梦者', '星空下的猫', '向日葵', '海风', '山间的风']

      const comment = {
        nickname: randomNames[Math.floor(Math.random() * randomNames.length)],
        avatarColor: colors[Math.floor(Math.random() * colors.length)],
        content: this.commentContent,
        time: Date.now()
      }

      this.post.comments.push(comment)
      this.savePosts()
      this.commentContent = ''
      uni.showToast({ title: '评论成功', icon: 'success' })
    },
    savePosts() {
      const posts = uni.getStorageSync('communityPosts') || []
      const index = posts.findIndex(p => p.id == this.postId)
      if (index > -1) {
        posts[index] = this.post
        uni.setStorageSync('communityPosts', posts)
      }
    },
    sharePost() {
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
  padding-bottom: 120rpx;
}

/* 帖子详情 */
.post-detail {
  background: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-text {
  font-size: 32rpx;
  color: #fff;
  font-weight: bold;
}

.user-meta {
  flex: 1;
}

.nickname {
  font-size: 30rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
}

.post-time {
  font-size: 24rpx;
  color: #a0aec0;
}

.post-topic {
  font-size: 24rpx;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
}

.post-content {
  margin-bottom: 24rpx;
}

.post-text {
  font-size: 30rpx;
  color: #4a5568;
  line-height: 1.8;
  display: block;
  margin-bottom: 16rpx;
}

.post-images {
  display: flex;
  gap: 12rpx;
  flex-wrap: wrap;
}

.post-image {
  width: 220rpx;
  height: 220rpx;
  border-radius: 12rpx;
}

.post-actions {
  display: flex;
  gap: 40rpx;
  padding-top: 20rpx;
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
  font-size: 36rpx;
}

.action-num {
  font-size: 26rpx;
  color: #718096;
}

.action-text {
  font-size: 26rpx;
  color: #718096;
}

/* 评论区域 */
.comments-section {
  background: #fff;
  padding: 30rpx;
  min-height: 400rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 24rpx;
  display: block;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.comment-card {
  display: flex;
  gap: 16rpx;
}

.comment-avatar {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.comment-avatar-text {
  font-size: 24rpx;
  color: #fff;
  font-weight: bold;
}

.comment-body {
  flex: 1;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 16rpx;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8rpx;
}

.comment-name {
  font-size: 26rpx;
  font-weight: bold;
  color: #667eea;
}

.comment-time {
  font-size: 22rpx;
  color: #a0aec0;
}

.comment-content {
  font-size: 28rpx;
  color: #4a5568;
  line-height: 1.6;
}

/* 空评论 */
.empty-comments {
  text-align: center;
  padding: 60rpx 40rpx;
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

/* 底部输入 */
.comment-input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 20rpx 30rpx;
  display: flex;
  gap: 16rpx;
  align-items: center;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.comment-input {
  flex: 1;
  height: 72rpx;
  background: #f7fafc;
  border-radius: 36rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
  color: #2d3748;
}

.send-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 36rpx;
  padding: 16rpx 40rpx;
  font-size: 28rpx;
  border: none;
}
</style>
