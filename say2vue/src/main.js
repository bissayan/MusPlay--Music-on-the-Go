import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'

createApp(App).use(store).use(router).use(bootstrap).mount('#app')
