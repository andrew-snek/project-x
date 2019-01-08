'use strict'

import Vue from 'vue'
import axios from 'axios'
import store from '../store/store'

axios.defaults.baseURL = process.env.VUE_APP_API_HOST || 'http://localhost:8000/api/v1/'
axios.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8'

axios.interceptors.request.use(
  function (config) {
    store.commit('LOADING')
    return config
  },
  function (error) {
    store.commit('LOADED')
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  function (response) {
    store.commit('LOADED')
    return response
  },
  function (error) {
    store.commit('LOADED')
    return Promise.reject(error)
  }
)

Plugin.install = function (Vue, options) {
  Vue.axios = axios
  window.axios = axios
  Object.defineProperties(Vue.prototype, {
    axios: {
      get () {
        return axios
      }
    },
    $axios: {
      get () {
        return axios
      }
    }
  })
}

Vue.use(Plugin)

export default Plugin
