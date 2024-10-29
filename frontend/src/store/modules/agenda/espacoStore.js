import RoomService from '../../../services/agenda/espacoService';
const api = new RoomService()
const state = {
    espacos: [],
    espaco_loading:false,
};
const getters = {
    StateEspacos: state => state.espacos,
    StateEspacoLoading: state => state.espaco_loading,
};
const mutations = {
    setEspacos(state, value){ state.espacos = value },
    setEspacoLoading(state, value){ state.espaco_loading = value },
};
const actions = {
    async GetAgendaLabsEspacos({commit}, params={}) {
        commit('setEspacoLoading', true)
        try{
            let response = await api.get('',{...params, page_size:300})
            // console.log('espacos', response.data.results, params)
            commit('setEspacos', response.data.results)
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setEspacoLoading', false)
    },
    async UpdateRoom({commit, dispatch, getters}, data) {
        dispatch
        getters
        commit('setEspacoLoading', true)
        var updated = false
        try{
            let response = await api.patch(`${data.id}/`, data)
            response
            // console.log('response updateRoom', data, response)
            let contexts = getters.StateUserFiliais
            // console.log('contexts', contexts)
            dispatch('GetAgendaLabsEspacos', {contexts})
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setEspacoLoading', false)
        return updated
    },
    async CreateRoom({commit, dispatch, getters}, data) {
        commit('setEspacoLoading', true)
        var created = false
        try{
            await api.post('',data)
            created = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cadastro de Espaço',
                message:`Espaço ${data.descricao} criado com sucesso!`
                }
            ])
            // Recarregar Espaços com os parametros de contexto do usuario
            let contexts = getters.StateUserFiliais
            dispatch('GetAgendaLabsEspacos', {contexts})
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setEspacoLoading', false)
        return created
    },
    async DeleteRoom({commit, getters, dispatch}, data) {
        commit('setEspacoLoading', true)
        var deleted = false
        try{
            await api.delete(`${data.id}/`)
            deleted = true
            let contexts = getters.StateUserFiliais
            dispatch('GetAgendaLabsEspacos', {contexts})
            const alerta = {
                tag:'success',
                title:'Registro de Espaço',
                message:`A espaço ${data.descricao} foi removido com sucesso!`
            }
            commit("setAlerts", [ alerta ])
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setEspacoLoading', false)
        return deleted
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};