"use strict";

import Vue from 'vue';
import axios from 'axios';
import store from '../store/store'

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8'

let config = {
  baseURL: process.env.VUE_APP_API_HOST || "http://localhost:8000/",
  headers: {
    common: {
      'Content-Type': 'application/json; charset=utf-8'
    }
  }
};

const _axios = axios.create(config);

_axios.interceptors.request.use(
  function(config) {
    store.commit('LOADING')
    return config;
  },
  function(error) {
    store.commit('LOADED')
    return Promise.reject(error);
  }
);

_axios.interceptors.response.use(
  function(response) {
    store.commit('LOADED')
    return response;
  },
  function(error) {
    store.commit('LOADED')
    return Promise.reject(error);
  }
);

Plugin.install = function(Vue, options) {
  Vue.axios = _axios;
  window.axios = _axios;
  Object.defineProperties(Vue.prototype, {
    axios: {
      get() {
        return _axios;
      }
    },
    $axios: {
      get() {
        return _axios;
      }
    },
  });
};

Vue.use(Plugin)

export default Plugin;
