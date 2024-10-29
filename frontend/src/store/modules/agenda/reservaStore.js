import ReservaService from '../../../services/agenda/reservaService';
const api = new ReservaService()
const state = {
    selected_reserva:{},
    reservas: [],
    reserva_loading:false,
    reserva_create_loading:false,
    loading_selected_reserva:false,
    // manageResultRequestReserva:{}
};
const getters = {
    StateReservas: state => state.reservas,
    StateSelectedReserva: state => state.selected_reserva,
    StateCalendarReservas: state => state.reservas.map(event => ({
            start: new Date(`${event.date}T${event.start}`),
            end: new Date(`${event.date}T${event.end}`),
            // start: new Date(`${event.date}T${event.start}`),
            // end: new Date(`${event.date}T${event.end}`),
            title: event.titulo,
            event
        })
    ),
    StateReservaLoading: state => state.reserva_loading,
    StateReservaCreateLoading: state => state.reserva_create_loading,
    StateSelectedReservaLoading: state => state.loading_selected_reserva,
    // StateManageResultsRequestReserva: state => state.manageResultRequestReserva,
};
const mutations = {
    setReservas(state, value){ state.reservas = value },
    setSelectedReserva(state, value){ state.selected_reserva = value },
    setReservaLoading(state, value){ state.reserva_loading = value },
    setReservaCreateLoading(state, value){ state.reserva_create_loading = value },
    setSelectedReservaLoading(state, value){ state.loading_selected_reserva = value },
    // setManageResultsRequestReserva(state, value){ state.manageResultRequestReserva = value },
};
const actions = {
    async GetReportAgendaLabsReservas({ commit, dispatch}, params={}) {
        var reservas = []
        try{
            let response = await api.get('', params)
            var { count, next, previous, results } = response.data
            var data = { count, next, previous, results }
            reservas.push(results)
            
            while (data.next !== null) {
                data = await dispatch('PaginateRequest', data)
                let page = data.results
                reservas = [...reservas, ...page]
            }
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        return results
    },
    async GetAgendaLabsReservas({ commit, dispatch, getters}, params={}) {
        commit('setReservaLoading', true)
        commit('setReservas', [])
        try{
            let response = await api.get('',{...params, page_size: 50})
            var { count, next, previous, results } = response.data
            var data = { count, next, previous, results }
            commit('setReservas', data.results)
            while (data.next !== null) {
                data = await dispatch('PaginateRequest', data)
                let page = data.results
                commit('setReservas', [...getters.StateReservas, ...page])
            }
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setReservaLoading', false)
    },
    async GetReservaDetalhe({ commit, dispatch}, id) {
        commit('setSelectedReservaLoading', true)
        commit('setSelectedReserva', {})
        // await dispatch('verifyToken')
        dispatch
        // console.log('requesting reserva detalhe', id)
        try{
            let response = await api.get(`${id}/details`)
            // console.log('requesting reserva detalhe response on ReservaStore -> GetReservaDetalhe', response)
            commit('setSelectedReserva', response.data)
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setSelectedReservaLoading', false)
    },
    // async UpdateReserva({ commit, dispatch}, data) {
    //     commit('setReservaLoading', true)
    //     // await dispatch('verifyToken')
    //     var updated = false
    //     try{
    //         await api.patch(`${data.id}/`, data)
    //         dispatch('GetAgendaLabsReservas')
    //         updated = true
    //     }catch(error){
    //         commit("setAlerts", [ error.toast_message ])
    //     }
    //     commit('setReservaLoading', false)
    //     return updated
    // },
    async CreateReserva({ commit, dispatch}, data) {
        dispatch
        commit('setReservaCreateLoading', true)
        var created = false
        try{
            await api.post('',data)
            // dispatch('GetAgendaLabsReservas')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Novo Evento',
                    message:`Reserva registrado com sucesso!`
                }
            ])
            created = true
        }catch(error){
            console.log('lancando error em CreateReserva Store', error)
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setReservaCreateLoading', false)
        return created
    },
    async RevogarReserva({ commit, dispatch}, data) {
        dispatch
        commit('setReservaLoading', true)
        // await dispatch('verifyToken')
        var revoked = false
        try{
            await api.post(`${data.id}/set_cancelled/`, {status_descricao:data.status_descricao})
            // dispatch('GetAgendaLabsReservas')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Cancelamento de reserva',
                    message:`Reserva do espaço ${data.espaco.descricao} em ${data.date_start_end} cancelada com sucesso!`
                }
            ])
            revoked = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setReservaLoading', false)
        return revoked
    },
    async AprovarReserva({ commit, dispatch}, data) {
        dispatch
        commit('setReservaLoading', true)
        // await dispatch('verifyToken')
        var approved = false
        try{
            await api.post(`${data.id}/set_opened/`)
            // dispatch('GetAgendaLabsReservas')
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Aprovação de reserva',
                    message:`Reserva do espaço ${data.espaco.descricao} em ${data.date_start_end} aprovada com sucesso!`
                }
            ])
            approved = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setReservaLoading', false)
        return approved
    },
    async PaginateRequest({ commit } , data) {
        try{
            let response = await api.genericGetRequest(data.next)
            const { count, next, previous, results } = response.data
            return { count, next, previous, results }
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
            return null
        }
    },
    // async GetAgendaLabsReservasPaginate({ commit, getters}) {
    //     try{
    //         let response = await api.genericGetRequest(getters.StateManageResultsRequestReserva.next)
    //         const {count, next, previous, results} = response.data
    //         let reservas = getters.StateReservas
    //         reservas.push(...results)
    //         commit('setReservas', reservas)
    //         commit('setManageResultsRequestReserva', {count, next, previous})
    //     }catch(error){
    //         commit("setAlerts", [ error.toast_message ])
    //     }
    // },
};
export default {
    state,
    getters,
    actions,
    mutations
};