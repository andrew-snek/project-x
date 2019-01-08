import axios from 'axios'
import router from '../../router'

const state = {
  accessToken: '',
  refreshToken: '',
  loading: false
}

const mutations = {
  'LOADING': (state) => {
    state.loading = true
  },
  'LOADED': (state) => {
    state.loading = false
  },
  'AUTH_SUCCESS': (state, { access, refresh }) => {
    state.accessToken = access
    state.refreshToken = refresh
  },
  'AUTH_REFRESH': (state, accessToken) => {
    state.accessToken = accessToken
  },
  'AUTH_LOGOUT': (state) => {
    state.accessToken = ''
    state.refreshToken = ''
  }
}

const actions = {
  setRefreshTokenTimeout: ({ dispatch, state }) => {
    let accessTokenPayload = JSON.parse(atob(state.accessToken.split('.')[1]))
    let secsToExpire = accessTokenPayload.exp * 1000 - new Date().getTime()

    setTimeout(() => {
      dispatch('authRefreshToken')
    }, secsToExpire - 1000) // refresh 1 second before token expiration
  },
  authRequest: ({ commit, dispatch }, { username, password }) => {
    return new Promise((resolve, reject) => {
      axios.post('obtain-token/', {
        username, password
      })
        .then(resp => {
          let { access, refresh } = resp.data

          localStorage.setItem('access-token', access)
          localStorage.setItem('refresh-token', refresh)
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + access
          commit('AUTH_SUCCESS', { access, refresh })
          dispatch('setRefreshTokenTimeout')

          resolve(resp)
        })
        .catch(err => {
          dispatch('authLogout')
          reject(err)
        })
    })
  },
  authLogout: ({ commit }) => {
    return new Promise((resolve) => {
      commit('AUTH_LOGOUT')
      localStorage.removeItem('access-token')
      localStorage.removeItem('refresh-token')
      delete axios.defaults.headers.common['Authorization']
      resolve()
    })
  },
  authRefreshToken: ({ commit, state, dispatch }) => {
    axios.post('refresh-token/', {
      refresh: state.refreshToken
    })
      .then(resp => {
        let { access } = resp.data

        localStorage.setItem('access-token', access)
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access
        commit('AUTH_REFRESH', access)

        dispatch('setRefreshTokenTimeout')
      })
      .catch(() => {
        dispatch('authLogout').then(() => { router.push('/login') })
      })
  },
  autoLogin: ({ commit, dispatch }) => {
    const access = localStorage.getItem('access-token')
    if (!access) {
      return
    }
    const refresh = localStorage.getItem('refresh-token')

    axios.defaults.headers.common['Authorization'] = 'Bearer ' + access
    commit('AUTH_SUCCESS', { access, refresh })
    dispatch('setRefreshTokenTimeout')
  }
}

const getters = {
  isAuthenticated: state => !!state.accessToken,
  loading: state => state.loading
}

export default {
  state,
  mutations,
  actions,
  getters
}
