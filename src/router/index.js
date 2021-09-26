import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
  },
  {
    path: '/load_video',
    name: 'LoadVideo',
    component: LoadVideo
>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
  }
]

const router = createRouter({
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

>>>>>>> c7d71ff (v2.0.1)
>>>>>>> 5dc33da (v2.0.1)
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
