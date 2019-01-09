import axios from 'axios'

const state = {
  fieldtypes: []
}

const mutations = {
  'SET_FIELDTYPES' (state, fieldtypes) {
    state.fieldtypes = fieldtypes
  },
  'ADD_FIELDTYPE' (state, fieldtype) {
    state.fieldtypes.push(fieldtype)
  },
  'REMOVE_FIELDTYPE' (state, id) {
    state.fieldtypes = state.fieldtypes.filter(ft => ft.id !== id)
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
  fieldtypes: state => {
    return state.fieldtypes
  }
}

export default {
  state,
  mutations,
  actions,
  getters
}
