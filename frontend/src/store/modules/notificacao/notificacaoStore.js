import NotificacaoService from '../../../services/notificacao/notificacaoService';
const api = new NotificacaoService()
const state = {
    notificacao: [],
    notificacao_loading:false,
};
const getters = {
    StateNotificacao: state => state.notificacao,
    StateNotificacaoLoading: state => state.notificacao_loading,
};
const mutations = {
    setNotificacao(state, value){ state.notificacao = value },
    setNotificacaoLoading(state, value){ state.notificacao_loading = value },
};
const actions = {
    async GetNotificacao({commit}, params={}) {
        commit('setNotificacaoLoading', true)
        try{
            const response = await api.get('',{...params, page_size: 100})
            // Limpa e reconstroi, limpar bug de atualizacao
            commit('setNotificacao', [])
            commit('setNotificacao', response.data.results)
        }catch(error){
            commit('setNotificacao', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setNotificacaoLoading', false)
    },
    async UpdateNotificacao({commit, dispatch}, data) {
        dispatch
        commit('setNotificacaoLoading', true)
        var updated = false
        try{
            await api.patch(`${data.id}/`, data)
            //alerts via $on e $emits
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setNotificacaoLoading', false)
        return updated
    },
    async CreateNotificacao({commit, dispatch}, data) {
        dispatch
        commit('setNotificacaoLoading', true)
        var created = false
        try{
            await api.post('',data)
            created = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setNotificacaoLoading', false)
        return created
    },
    async DeleteNotificacao({commit, dispatch}, data) {
        commit('setNotificacaoLoading', true)
        var deleted = false
        try{
            await api.delete(`${data.id}/`)
            dispatch('GetNotificacao')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Registro de Notificação',
                    message:`A Notificação <b>${data.titulo}</b> foi removida com sucesso!`
                }
            ])
            deleted = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setNotificacaoLoading', false)
        return deleted
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};