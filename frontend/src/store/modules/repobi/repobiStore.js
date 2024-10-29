import RepoBIService from '../../../services/repobi/repobiService';
const api = new RepoBIService()
const state = {
  user_bis: [],
  user_bis_loading:false
};
const getters = {
  StateUserBis: state => state.user_bis,
  StateUserBisLoading: state => state.user_bis_loading,
};
const mutations = {
  SetUserBis(state, value){state.user_bis = value},
  SetUserBisLoading(state, value){state.user_bis_loading = value},
};
const actions = {
  async GetUserBis({commit, dispatch, getters}) {
    commit('SetUserBisLoading', true)
    dispatch
    getters
    try{
        let response = await api.user_bis()
        commit('SetUserBis', response.data)
    }catch(error){
        commit("setAlerts", [ error.toast_message ])
    }
    commit('SetUserBisLoading', false)
  },
};
export default {
  state,
  getters,
  actions,
  mutations
};