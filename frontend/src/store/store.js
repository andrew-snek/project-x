import Vue from 'vue'
import Vuex from 'vuex'

import user from './modules/user'
import fieldtypes from './modules/fieldtypes'
import abstractrisks from './modules/abstractrisks'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {

  },
  mutations: {

  },
  actions: {

  },
  getters: {

  },
  modules: {
    user,
    fieldtypes,
    abstractrisks
  }
})
