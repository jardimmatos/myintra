import TipoEspacoService from '../../../services/agenda/tipoEspacoService';
const api = new TipoEspacoService()
const state = {
    tipo_espaco: [],
    tipo_espaco_loading:false,
};
const getters = {
    StateTipoEspaco: state => state.tipo_espaco,
    StateTipoEspacoLoading: state => state.tipo_espaco_loading,
};
const mutations = {
    setTipoEspacos(state, value){ state.tipo_espaco = value },
    setTipoEspacosLoading(state, value){ state.tipo_espaco_loading = value },
};
const actions = {
    async GetAgendaLabsTipoEspacos({commit}, params={}) {
        commit('setTipoEspacosLoading', true)
        try{
            let response = await api.get('',{...params, page_size:100})
            commit('setTipoEspacos', response.data.results)
        }catch(error){
            commit('setTipoEspacos', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setTipoEspacosLoading', false)
    },
    async UpdateTipoEspaco({commit, dispatch}, data) {
        commit('setTipoEspacosLoading', true)
        var updated = false
        try{
            await api.patch(`${data.id}/`, data)
            dispatch('GetAgendaLabsTipoEspacos')
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setTipoEspacosLoading', false)
        return updated
    },
    async CreateTipoEspaco({commit, dispatch}, data) {
        commit('setTipoEspacosLoading', true)
        var created = false
        try{
            await api.post('',data)
            dispatch('GetAgendaLabsTipoEspacos')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Cadastro de Tipo de Espaço',
                    message:`Tipo de Espaço ${data.descricao} criado com sucesso!`
                }
            ])
            created = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setTipoEspacosLoading', false)
        return created
    },
    async DeleteTipoEspaco({commit, dispatch}, data) {
        commit('setTipoEspacosLoading', true)
        var deleted = false
        try{
            await api.delete(`${data.id}/`)
            dispatch('GetAgendaLabsTipoEspacos')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Registro de Tipo de Espaço',
                    message:`O tipo de espaço ${data.descricao} foi removido com sucesso!`
                }
            ])
            deleted = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setTipoEspacosLoading', false)
        return deleted
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};