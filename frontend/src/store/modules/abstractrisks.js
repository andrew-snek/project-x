import axios from 'axios'

const state = {
  abstractRisks: []
}

const mutations = {
  'SET_ABSTRACT_RISKS' (state, abstractRisks) {
    state.abstractRisks = abstractRisks
  },
  'ADD_ABSTRACT_RISK' (state, abstractRisk) {
    state.abstractRisks.push(abstractRisk)
  },
  'REMOVE_ABSTRACT_RISK' (state, id) {
    state.abstractRisks = state.abstractRisks.filter(ar => ar.id !== id)
  }
}

const actions = {
  initAbstractRisks: ({ commit }) => {
    axios.get('abstractrisks/')
      .then(resp => {
        commit('SET_ABSTRACT_RISKS', resp.data)
      })
  },
  createAbstractRisk: ({ commit }, { name, abstract_fields }) => {
    return new Promise((resolve, reject) => {
      axios.post('abstractrisks/', { name, abstract_fields })
        .then(resp => {
          commit('ADD_ABSTRACT_RISK', resp.data)
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        })
    })
  },
  deleteAbstractRisk: ({ commit }, id) => {
    return new Promise((resolve, reject) => {
      axios.delete(`abstractrisks/${id}`)
        .then(resp => {
          commit('REMOVE_ABSTRACT_RISK', id)
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        })
    })
  }
}

const getters = {
  abstractRisks: state => {
    return state.abstractRisks
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
