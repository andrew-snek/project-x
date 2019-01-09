import Vue from 'vue'
import Router from 'vue-router'
import store from './store/store'

Vue.use(Router)

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next()
  } else {
    next('/login')
  }
}

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./components/Welcome.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./components/Login.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: (to, from, next) => {
        store.dispatch('authLogout').then(() => { next('/login') })
      }
    },
    {
      path: '/fieldtypes',
      name: 'fieldtypes',
      component: () => import('./components/FieldTypes.vue'),
      beforeEnter: ifAuthenticated
    },
    {
      path: '/abstractrisks',
      name: 'abstractrisks',
      component: () => import('./components/AbstractRisks.vue'),
      beforeEnter: ifAuthenticated
    }
  ]
})
