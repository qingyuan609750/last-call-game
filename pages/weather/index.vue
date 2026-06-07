<template>
  <view class="container">
    <view class="weather-header">
      <text class="weather-title">🌤️ 情绪气象站</text>
      <text class="weather-desc">记录心情，看内心的天气</text>
    </view>

    <!-- 今日天气选择 -->
    <view class="today-weather" v-if="!todayRecorded">
      <text class="today-title">今天的心情天气是？</text>
      <view class="weather-options">
        <view 
          class="weather-option" 
          v-for="(weather, index) in weathers" 
          :key="index"
          :class="{'weather-selected': selectedWeather === weather}"
          @click="selectWeather(weather)"
        >
          <text class="weather-emoji">{{weather.emoji}}</text>
          <text class="weather-name">{{weather.name}}</text>
          <text class="weather-temp">{{weather.temp}}</text>
        </view>
      </view>
      
      <textarea 
        class="weather-note" 
        v-model="weatherNote"
        placeholder="记录一下今天的心情..."
        maxlength="200"
      />
      
      <button class="record-btn" @click="recordWeather">记录今日天气</button>
    </view>

    <!-- 已记录展示 -->
    <view class="today-recorded" v-else>
      <view class="recorded-card">
        <text class="recorded-emoji">{{todayRecord.emoji}}</text>
        <text class="recorded-name">{{todayRecord.name}}</text>
        <text class="recorded-note">{{todayRecord.note}}</text>
        <text class="recorded-date">{{todayRecord.date}}</text>
      </view>
      <button class="rerecord-btn" @click="reRecord">重新记录</button>
    </view>

    <!-- 本周天气图 -->
    <view class="week-section" v-if="weekRecords.length > 0">
      <text class="section-title">本周心情天气</text>
      <view class="week-chart">
        <view class="day-item" v-for="(day, index) in weekRecords" :key="index">
          <text class="day-emoji">{{day.emoji}}</text>
          <view class="day-bar" :style="{height: day.height + 'rpx', background: day.color}"></view>
          <text class="day-label">{{day.label}}</text>
        </view>
      </view>
    </view>

    <!-- 月度天气统计 -->
    <view class="month-section" v-if="monthStats.length > 0">
      <text class="section-title">本月天气统计</text>
      <view class="month-grid">
        <view class="month-item" v-for="(item, index) in monthStats" :key="index">
          <text class="month-emoji">{{item.emoji}}</text>
          <text class="month-name">{{item.name}}</text>
          <text class="month-count">{{item.count}}天</text>
          <view class="month-bar">
            <view class="month-fill" :style="{width: item.percentage + '%', background: item.color}"></view>
          </view>
        </view>
      </view>
    </view>

    <!-- 心情语录 -->
    <view class="quote-section">
      <view class="quote-card">
        <text class="quote-text">"{{currentQuote}}"</text>
        <text class="quote-refresh" @click="refreshQuote">换一句</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      selectedWeather: null,
      weatherNote: '',
      todayRecorded: false,
      todayRecord: {},
      weekRecords: [],
      monthStats: [],
      weathers: [
        { emoji: '☀️', name: '晴天', temp: '25°C', value: 5, color: '#f6ad55', desc: '阳光明媚，心情大好' },
        { emoji: '⛅', name: '多云', temp: '20°C', value: 4, color: '#f6e05e', desc: '平静安稳，一切顺利' },
        { emoji: '🌧️', name: '雨天', temp: '15°C', value: 2, color: '#63b3ed', desc: '有点低落，需要安慰' },
        { emoji: '⛈️', name: '雷雨', temp: '12°C', value: 1, color: '#4a5568', desc: '心情烦躁，需要释放' },
        { emoji: '🌈', name: '彩虹', temp: '22°C', value: 5, color: '#9f7aea', desc: '雨过天晴，充满希望' },
        { emoji: '❄️', name: '下雪', temp: '0°C', value: 3, color: '#a0aec0', desc: '安静清冷，适合思考' },
        { emoji: '🌤️', name: '微风', temp: '18°C', value: 4, color: '#68d391', desc: '清爽舒适，心情愉悦' },
        { emoji: '🌪️', name: '大风', temp: '16°C', value: 2, color: '#ed8936', desc: '情绪波动，需要平静' }
      ],
      quotes: [
        '心情就像天气，有晴有雨才是人生',
        '即使下雨，也要记得带伞前行',
        '彩虹总在风雨后',
        '今天的阴霾，是明天阳光的前奏',
        '每一种天气，都是生活的馈赠',
        '心情是自己的，天气是暂时的'
      ],
      currentQuote: ''
    }
  },
  onShow() {
    this.loadTodayRecord()
    this.loadWeekRecords()
    this.loadMonthStats()
    this.refreshQuote()
  },
  methods: {
    selectWeather(weather) {
      this.selectedWeather = weather
    },
    recordWeather() {
      if (!this.selectedWeather) {
        uni.showToast({ title: '请选择天气', icon: 'none' })
        return
      }
      
      const record = {
        ...this.selectedWeather,
        note: this.weatherNote,
        date: new Date().toLocaleDateString(),
        timestamp: Date.now()
      }
      
      let records = uni.getStorageSync('weatherRecords') || []
      records = records.filter(r => r.date !== record.date)
      records.push(record)
      uni.setStorageSync('weatherRecords', records)
      
      this.todayRecorded = true
      this.todayRecord = record
      this.loadWeekRecords()
      this.loadMonthStats()
      uni.showToast({ title: '记录成功', icon: 'success' })
    },
    reRecord() {
      this.todayRecorded = false
      this.selectedWeather = null
      this.weatherNote = ''
    },
    loadTodayRecord() {
      const today = new Date().toLocaleDateString()
      const records = uni.getStorageSync('weatherRecords') || []
      const todayRecord = records.find(r => r.date === today)
      if (todayRecord) {
        this.todayRecorded = true
        this.todayRecord = todayRecord
      }
    },
    loadWeekRecords() {
      const records = uni.getStorageSync('weatherRecords') || []
      const weekDays = ['日', '一', '二', '三', '四', '五', '六']
      const today = new Date()
      const weekData = []
      
      for (let i = 6; i >= 0; i--) {
        const date = new Date(today)
        date.setDate(date.getDate() - i)
        const dateStr = date.toLocaleDateString()
        const record = records.find(r => r.date === dateStr)
        
        weekData.push({
          emoji: record ? record.emoji : '➖',
          label: weekDays[date.getDay()],
          height: record ? record.value * 40 + 40 : 40,
          color: record ? record.color : '#e2e8f0'
        })
      }
      
      this.weekRecords = weekData
    },
    loadMonthStats() {
      const records = uni.getStorageSync('weatherRecords') || []
      const stats = {}
      
      records.forEach(r => {
        if (!stats[r.name]) {
          stats[r.name] = { name: r.name, emoji: r.emoji, count: 0, color: r.color }
        }
        stats[r.name].count++
      })
      
      const total = records.length
      this.monthStats = Object.values(stats).map(s => ({
        ...s,
        percentage: total > 0 ? (s.count / total * 100) : 0
      })).sort((a, b) => b.count - a.count)
    },
    refreshQuote() {
      this.currentQuote = this.quotes[Math.floor(Math.random() * this.quotes.length)]
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

.weather-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.weather-title {
  font-size: 40rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10rpx;
}

.weather-desc {
  font-size: 26rpx;
  color: #a0aec0;
}

/* 今日天气选择 */
.today-weather {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.today-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 24rpx;
  text-align: center;
}

.weather-options {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.weather-option {
  width: calc(25% - 12rpx);
  text-align: center;
  padding: 20rpx 10rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  border: 2rpx solid transparent;
  transition: all 0.3s;
}

.weather-selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.weather-emoji {
  font-size: 40rpx;
  display: block;
  margin-bottom: 6rpx;
}

.weather-name {
  font-size: 24rpx;
  color: #2d3748;
  display: block;
  margin-bottom: 2rpx;
}

.weather-temp {
  font-size: 20rpx;
  color: #a0aec0;
}

.weather-note {
  width: 100%;
  min-height: 120rpx;
  background: #f7fafc;
  border-radius: 16rpx;
  padding: 20rpx;
  font-size: 26rpx;
  color: #2d3748;
  margin-bottom: 20rpx;
}

.record-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 40rpx;
  padding: 24rpx;
  font-size: 30rpx;
  border: none;
}

/* 已记录 */
.today-recorded {
  text-align: center;
  margin-bottom: 30rpx;
}

.recorded-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24rpx;
  padding: 50rpx;
  margin-bottom: 20rpx;
  color: #fff;
}

.recorded-emoji {
  font-size: 80rpx;
  display: block;
  margin-bottom: 16rpx;
}

.recorded-name {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 12rpx;
}

.recorded-note {
  font-size: 26rpx;
  opacity: 0.9;
  display: block;
  margin-bottom: 12rpx;
}

.recorded-date {
  font-size: 22rpx;
  opacity: 0.7;
}

.rerecord-btn {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 40rpx;
  padding: 20rpx 60rpx;
  font-size: 26rpx;
  border: 2rpx solid #667eea;
}

/* 本周天气 */
.week-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #2d3748;
  margin-bottom: 24rpx;
  display: block;
}

.week-chart {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  height: 200rpx;
  padding: 0 10rpx;
}

.day-item {
  text-align: center;
  flex: 1;
}

.day-emoji {
  font-size: 32rpx;
  display: block;
  margin-bottom: 8rpx;
}

.day-bar {
  width: 40rpx;
  border-radius: 8rpx;
  margin: 0 auto 8rpx;
  transition: all 0.5s ease;
}

.day-label {
  font-size: 22rpx;
  color: #a0aec0;
}

/* 月度统计 */
.month-section {
  background: #fff;
  border-radius: 24rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);
}

.month-grid {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.month-item {
  display: flex;
  align-items: center;
  padding: 16rpx 0;
}

.month-emoji {
  font-size: 36rpx;
  margin-right: 16rpx;
}

.month-name {
  font-size: 26rpx;
  color: #2d3748;
  width: 100rpx;
}

.month-count {
  font-size: 24rpx;
  color: #a0aec0;
  width: 80rpx;
  text-align: right;
  margin-right: 16rpx;
}

.month-bar {
  flex: 1;
  height: 12rpx;
  background: #edf2f7;
  border-radius: 6rpx;
  overflow: hidden;
}

.month-fill {
  height: 100%;
  border-radius: 6rpx;
  transition: width 0.5s ease;
}

/* 语录 */
.quote-section {
  margin-bottom: 30rpx;
}

.quote-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 24rpx;
  padding: 40rpx;
  text-align: center;
  position: relative;
}

.quote-text {
  font-size: 28rpx;
  color: #fff;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
  font-style: italic;
}

.quote-refresh {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: underline;
}
</style>
