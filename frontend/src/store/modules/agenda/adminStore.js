import GestorService from '../../../services/agenda/gestorService';
const api = new GestorService()
const state = {
    admins: [],
    loading_admins:false,
    paginate_admins:{}
};
const getters = {
    StateAdmins: state => state.admins,
    StateAdminsLoading: state => state.loading_admins,
    StatePaginateAdmins: state => state.paginate_admins,
};
const mutations = {
    setAdmins(state, value){ state.admins = value },
    setAdminsLoading(state, value){ state.loading_admins = value },
    setPaginateAdmins(state, value){ state.paginate_admins = value },
};
const actions = {
    async GetAdmins({commit}, params={}) {
        commit('setAdminsLoading', true)
        try{
            let response = await api.get('',params)
            // console.log(params, response)
            const { count, next, previous, results } = response.data
            commit('setAdmins', results)
            commit('setPaginateAdmins', {count, next, previous})
        }catch(error){
            commit('setAdmins', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setAdminsLoading', false)
    },
};
export default {
  state,
  getters,
  actions,
  mutations
};