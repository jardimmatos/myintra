import LogService from '../../../services/agenda/logService';
const api = new LogService()
const state = {
    logs: [],
    loading_logs:false,
    paginate_logs:{}
};
const getters = {
    StateLogsAgenda: state => state.logs,
    StateLogsAgendaLoading: state => state.loading_logs,
    StatePaginateLogsAgenda: state => state.paginate_logs,
};
const mutations = {
    setLogsAgenda(state, value){ state.logs = value },
    setLogsAgendaLoading(state, value){ state.loading_logs = value },
    setPaginateLogsAgenda(state, value){ state.paginate_logs = value },
};
const actions = {
    async GetLogsAgenda({commit}, params={}) {
        commit('setLogsAgendaLoading', true)
        try{
            let response = await api.get('',{...params, page_size:20})
            const { count, next, previous, results } = response.data
            // console.log('results, log', results)
            commit('setLogsAgenda', results)
            commit('setPaginateLogsAgenda', {count, next, previous})
        }catch(error){
            commit('setLogsAgenda', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setLogsAgendaLoading', false)
    },
};
export default {
  state,
  getters,
  actions,
  mutations
};