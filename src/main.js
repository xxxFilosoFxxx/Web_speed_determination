import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

createApp(App).use(Quasar, quasarUserOptions).use(store).use(router).use(BootstrapVue, IconsPlugin).mount('#app')
