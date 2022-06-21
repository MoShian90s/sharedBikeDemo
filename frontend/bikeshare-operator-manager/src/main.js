import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// load the global css style
import './assets/css/global.css'
import axios from 'axios'
import * as VueGoogleMaps from 'vue2-google-maps'
import VueSession from 'vue-session'

// yif's configurations
import database from './components/Manager/Database.vue'
import "vue-easytable/libs/theme-default/index.css"
import VueEasytable from "vue-easytable"
import * as echarts from 'echarts'
import * as GmapVue from 'gmap-vue'

Vue.use(VueSession)
// root path for request
axios.default.baseURI = ''
axios.interceptors.request.use(config => {
	console.log(config)
	config.headers.Authorization = window.sessionStorage.getItem('token')
	return config
})
Vue.prototype.$axios = axios
Vue.prototype.$baseURL = "api"
// yifan
Vue.prototype.$echarts = echarts
Vue.use(VueEasytable);
Vue.config.productionTip = false
// Jinni's map
Vue.use(VueGoogleMaps, {
	load: {
		key: 'AIzaSyA3ixh5N1ll313O3_MTSooGrdL2vnesQME',
		libraries: 'places', // This is required if you use the Autocomplete plugin
		language: 'en',
		sensor: 'false'
	}
})
// yifan's map
Vue.use(GmapVue, {
	load: {
		key: 'AIzaSyA3ixh5N1ll313O3_MTSooGrdL2vnesQME',
		libraries: ['places', 'visualization'], // This is required if you use the Autocomplete plugin
		language: 'en',
		sensor: 'false',
	},
	installComponents: true
})
// mount the vue root instance
new Vue({
	router,
	render: h => h(App)
}).$mount('#app')
