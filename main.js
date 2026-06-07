import Vue from 'vue'
import App from './App'
import CustomTabbar from './components/custom-tabbar/custom-tabbar.vue'

Vue.config.productionTip = false

Vue.component('custom-tabbar', CustomTabbar)

App.mpType = 'app'

const app = new Vue({
  ...App
})
app.$mount()
