import axios from 'axios'

const state = {
  risks: []
}

const mutations = {
  'SET_RISKS' (state, risks) {
    state.risks = risks
  },
  'ADD_RISK' (state, risk) {
    state.risks.push(risk)
  },
  'REMOVE_RISK' (state, id) {
    state.risks = state.risks.filter(r => r.id !== id)
  }
}

const actions = {
  initRisks: ({ commit }) => {
    axios.get('risks/')
      .then(resp => {
        commit('SET_RISKS', resp.data)
      })
  },
  createRisk: ({ commit }, { name, abstract_risk, fields }) => {
    return new Promise((resolve, reject) => {
      axios.post('risks/', { name, abstract_risk, fields })
        .then(resp => {
          commit('ADD_RISK', resp.data)
          resolve(resp)
        })
        .catch(e => reject(e))
    })
  },
  deleteRisk: ({ commit }, id) => {
    return new Promise((resolve, reject) => {
      axios.delete(`risks/${id}`)
        .then(resp => {
          commit('REMOVE_RISK', id)
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        })
    })
  }
}

const getters = {
  risks: state => {
    return state.risks
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
