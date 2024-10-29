import GestorService from '../../../services/agenda/gestorService';
const api = new GestorService()
const state = {
    gestores: [],
    loading_gestores:false,
    paginate_gestores:{}
};
const getters = {
    StateGestores: state => state.gestores,
    StateGestoresLoading: state => state.loading_gestores,
    StatePaginateGestores: state => state.paginate_gestores,
};
const mutations = {
    setGestores(state, value){ state.gestores = value },
    setGestoresLoading(state, value){ state.loading_gestores = value },
    setPaginateGestores(state, value){ state.paginate_gestores = value },
};
const actions = {
    async GetGestores({commit}, params={}) {
        commit('setGestoresLoading', true)
        try{
            let response = await api.get('',params)
            // console.log(params, response)
            const { count, next, previous, results } = response.data
            commit('setGestores', results)
            commit('setPaginateGestores', {count, next, previous})
            // commit('setManageResultsRequestManager', {count, next, previous})
            // while (getters.StateManageResultsRequestManager.next){
                //     await dispatch('GetGestoresPaginate')
                // }
            }catch(error){
                commit('setGestores', [])
                commit("setAlerts", [ error.toast_message ])
        }
        commit('setGestoresLoading', false)
    },
    async CarregarMaisGestores({commit, getters}, params={}) {
        commit('setGestoresLoading', true)
        try{
            let response = await api.genericGetRequest(getters.StatePaginateGestores.next, params)
            // console.log(params, response)
            let gestores = []
            gestores = gestores.concat(getters.StateGestores)
            const {count, next, previous, results } = response.data
            gestores = gestores.concat(results)
            commit('setPaginateGestores', {count, next, previous})
            commit('setGestores', gestores)
            }catch(error){
                // commit('setGestores', [])
                commit("setAlerts", [ error.toast_message ])
        }
        commit('setGestoresLoading', false)
    },
};
export default {
  state,
  getters,
  actions,
  mutations
};