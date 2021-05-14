/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import LoadVideo from '@/components/LoadVideo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LoadVideo',
      component: LoadVideo
    }
  ]
})
