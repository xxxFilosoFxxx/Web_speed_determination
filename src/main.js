<<<<<<< HEAD
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
=======
<<<<<<< HEAD
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
=======
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'
<<<<<<< HEAD
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

createApp(App).use(Quasar, quasarUserOptions).use(store).use(router).use(BootstrapVue, IconsPlugin).mount('#app')
=======
<<<<<<< HEAD
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

createApp(App).use(Quasar, quasarUserOptions).use(store).use(router).use(BootstrapVue, IconsPlugin).mount('#app')
=======

createApp(App).use(Quasar, quasarUserOptions)
    .use(store)
    .use(router)
    .mount('#app')
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
