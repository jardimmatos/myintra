import RegraService from '../../../services/agenda/regraService';
const api = new RegraService()
const week_day_names = [
    'Segunda-feira', //0
    'Terça-feira',  //1
    'Quarta-feira', //2
    'Quinta-feira', //3
    'Sexta-feira',  //4
    'Sábado',       //5
    'Domingo'       //6
]
const state = {
    regras: [],
    regra_enums: [],
    regra_loading:false,
    manage_results_regra:{}
};
const getters = {
    StateRegras: state => state.regras,
    StateRegraEnums: state => state.regra_enums,
    StateRegraLoading: state => state.regra_loading,
    StateManageResultsRegra: state => state.manage_results_regra,
};
const mutations = {
    setRegras(state, value){ state.regras = value },
    setRegraEnums(state, value){ state.regra_enums = value },
    setRegraLoading(state, value){ state.regra_loading = value },
    setManageResultsRegra(state, value){ state.manage_results_regra = value },
};
const actions = {
    async GetAgendaLabsRegras({commit, dispatch}, params={}) {
        commit('setRegraLoading', true)
        try{
            await dispatch('GetRegraEnumsAgendaLabs')
            let response = await api.get('',{...params, page_size:100})
            const {count, next, previous, results} = response.data
            commit('setRegras', results)
            commit('setManageResultsRegra', {count, next, previous})
            // while (getters.StateManageResultsRegra.next){
            //     await dispatch('GetAgendaLabsRegrasPaginate')
            // }
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRegraLoading', false)
    },
    async GetRegraEnumsAgendaLabs({commit, dispatch}, params={}) {
        // await dispatch('verifyToken')
        dispatch
        try{
            let response = await api.get('weekdays',params)
            const results = response.data
            commit('setRegraEnums', results)
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
    },
    async UpdateRegra({commit, dispatch}, data) {
        commit('setRegraLoading', true)
        // await dispatch('verifyToken')
        var updated = false
        try{
            await api.patch(`${data.id}/`, data)
            dispatch('GetAgendaLabsRegras')
            // console.log('updateRegras',data)
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRegraLoading', false)
        return updated
    },
    async CreateRegra({commit, dispatch}, data) {
        commit('setRegraLoading', true)
        // await dispatch('verifyToken')
        var created = false
        try{
            await api.post('',data)
            dispatch('GetAgendaLabsRegras')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Cadastro de Restrições',
                    message:`Restrição ${week_day_names[data.week_day]} - ${data.start_time} a ${data.end_time} criada com sucesso!`
                }
            ])
            created = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRegraLoading', false)
        return created
    },
    async DeleteRegra({commit, dispatch}, data) {
        commit('setRegraLoading', true)
        // await dispatch('verifyToken')
        var deleted = false
        try{
            await api.delete(`${data.id}/`)
            dispatch('GetAgendaLabsRegras')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Registro de restrição',
                    message:`Restrição ${week_day_names[data.week_day]} - ${data.start_time} a ${data.end_time} removido com sucesso!`
                }
            ])
            deleted = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRegraLoading', false)
        return deleted
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};