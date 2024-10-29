import UserService from '@/services/user/userService';

const api = new UserService()

const state = {
  setores: [],
  setores_loading: false,
};

const getters = {};

const mutations = {
  SetSetores(state, value){state.setores = value},
  SetSetoresLoading(state, value){state.setores_loading = value},
};

const actions = {
  async GetAllLocais({commit}, params) {
    try {
      commit('SetSetoresLoading', true)
      const response = await api.get('local/all/', {...params, page_size: 1000 })
      commit('SetSetoresLoading', false)
      return response
    } catch (error) {
      commit('SetSetoresLoading', false)
      return error
    }
  },
  async GetLocais({commit}, params) {
    commit('SetSetoresLoading', true)
    try {
      const response = await api.get('local/', {...params, page_size: 1000 })
      commit('SetSetores', response.data.results)
    } catch (error) {
      commit('SetSetores', [])
      commit("setAlerts", [ error.toast_message ])
    }
    commit('SetSetoresLoading', false)
  },
  async GetSimpleUsers({commit}, params) {
    commit
    const response = await api.get('users/simpleusers/', {...params, page_size: 1000 })
    return response.data.results.map(u => {
      const { id, username, first_name, last_name, email } = u
      return { id, username, first_name, last_name, email }
    })
  },
  async RefreshAuthenticatedUser({ commit }) {
    console.log('no refresh needed')
    commit
    return
  }

};
export default {
  state,
  getters,
  actions,
  mutations
};