import axios from 'axios'

const state = {
  fieldTypes: []
}

const mutations = {
  'SET_FIELDTYPES' (state, fieldTypes) {
    state.fieldTypes = fieldTypes
  },
  'ADD_FIELDTYPE' (state, fieldtype) {
    state.fieldTypes.push(fieldtype)
  },
  'REMOVE_FIELDTYPE' (state, id) {
    state.fieldTypes = state.fieldTypes.filter(ft => ft.id !== id)
  }
}

const actions = {
  initFieldtypes: ({ commit }) => {
    axios.get('fieldtypes/')
      .then(resp => {
        commit('SET_FIELDTYPES', resp.data)
      })
  },
  createFieldType: ({ commit }, { name, widget_type, regex }) => {
    return new Promise((resolve, reject) => {
      axios.post('fieldtypes/', {
        name,
        widget_type,
        regex
      })
        .then(resp => {
          commit('ADD_FIELDTYPE', resp.data)
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        })
    })
  },
  deleteFieldType: ({ commit }, id) => {
    return new Promise((resolve, reject) => {
      axios.delete(`fieldtypes/${id}`)
        .then(resp => {
          commit('REMOVE_FIELDTYPE', id)
          resolve(resp)
        })
        .catch(e => {
          reject(e)
        })
    })
  }
}

const getters = {
  fieldTypes: state => {
    return state.fieldTypes
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
