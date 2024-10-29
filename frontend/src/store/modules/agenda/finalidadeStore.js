import FinalidadeService from '../../../services/agenda/finalidadeService';
const api = new FinalidadeService()
const state = {
    finalidades: [],
    finalidades_loading:false,
};
const getters = {
    StateFinalidades: state => state.finalidades,
    StateFinalidadesLoading: state => state.finalidades_loading,
};
const mutations = {
    setFinalidades(state, value){ state.finalidades = value },
    setFinalidadesLoading(state, value){ state.finalidades_loading = value },
};
const actions = {
    async GetAgendaLabsFinalidades({commit}, params={}) {
        commit('setFinalidadesLoading', true)
        try{
            let response = await api.get('',params)
            // const {count, next, previous, results} = response.data
            commit('setFinalidades', response.data.results)
        }catch(error){
            commit('setFinalidades', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setFinalidadesLoading', false)
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};