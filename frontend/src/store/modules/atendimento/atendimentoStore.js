import AtendimentoService from '../../../services/atendimento/atendimentoService';
const api = new AtendimentoService()
const state = {
    loaders: []
};
const getters = {
    StateAtendimentoLoading: state => state.loaders,
};
const mutations = {
    setAtendimentoLoading(state, value){ state.loaders.push(value) },
    dropAtendimentoLoading(state, value){ state.loaders.pop(value) },
};
const actions = {
    async GetUnidadesAtendimento({commit}, params={}) {
        commit('setAtendimentoLoading', 'list-unidades')
        var results = []
        try{
            const response = await api.genericGetRequest('/atendimento/api/v1/atendimento/list_unidades_atendimento/', { ...params, page_size: 25 }, false)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', 'list-unidades')
        return results
    },
    async GetLocaisAtendimento({commit}, data={}) {
        commit('setAtendimentoLoading', 'list-locais')
        var results = []
        try{
            const response = await api.post('list_locais/', data)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', 'list-locais')
        return results
    },
    async GetUnidadeAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `get-unidade-${data.pk}`)
        var results = []
        try{
            const response = await api.get(`${data.pk}/get_unidade_atendimento/`)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `get-unidade-${data.pk}`)
        return results
    },
    async GetServicosAtendimento({commit}, data={}) {
        commit('setAtendimentoLoading', 'list-servicos')
        var results = []
        try{
            const response = await api.post(`list_servicos/?serial=${data?.serial||'simple'}`, data)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', 'list-servicos')
        return results
    },
    async GetPrioridadesAtendimento({commit}, data={}) {
        commit('setAtendimentoLoading', 'list-prioridades')
        var results = []
        try{
            const response = await api.post('list_prioridades/', data)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', 'list-prioridades')
        return results
    },
    async GetAtendenteLogado({commit}) {
        commit('setAtendimentoLoading', `get-atendente-logado`)
        var results = {}
        try{
            const response = await api.get(`get_atendente_logado/`)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `get-atendente-logado`)
        return results
    },
    async GetPainelAtualAtendente({commit}) {
        commit('setAtendimentoLoading', `get-painel-atual-atendente`)
        var results = {}
        try{
            const response = await api.get(`get_painel_atual_atendente/`)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `get-painel-atual-atendente`)
        return results
    },
    async IniciarAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `iniciar-atendimento`)
        var results = {}
        try{
            const response = await api.post(`${data.id}/iniciar_atendimento/`)
            results = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `iniciar-atendimento`)
        return results
    },
    async EncerrarAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `encerrar-atendimento`)
        var results = false
        try{
            await api.post(`${data.id}/encerrar_atendimento/`, data)
            results = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `encerrar-atendimento`)
        return results
    },
    async RedirecionarAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `redirecionar-atendimento`)
        var redirecionado = false
        try{
            await api.post(`${data.id}/redirecionar_atendimento/`, data)
            redirecionado = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `redirecionar-atendimento`)
        return redirecionado
    },
    async NaoCompareceuAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `nao-compareceu-atendimento`)
        var finalizado = false
        try{
            await api.post(`${data.id}/nao_compareceu_atendimento/`, data)
            finalizado = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `nao-compareceu-atendimento`)
        return finalizado
    },
    async AlterarAtendente({commit}, data) {
        commit('setAtendimentoLoading', `altera-atendente`)
        var updated = false
        try{
            await api.post(`alterar_atendente/`, data)
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `altera-atendente`)
        return updated
    },
    async ChamarProximaSenha({commit}, data) {
        commit('setAtendimentoLoading', `chamar-proxima-senha`)
        var painel = {}
        try{
            const response = await api.post(`proxima_senha/`, data)
            painel = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `chamar-proxima-senha`)
        return painel
    },
    async ChamarSenhaNovamente({commit}, data) {
        commit('setAtendimentoLoading', `chamar-senha-novamente`)
        try{
            await api.post(`${data.id}/chamar_senha_novamente/`)
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `chamar-senha-novamente`)
    },
    async TriagemSenhaAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `triagem-senha-atendimento`)
        var atendimento = {}
        try{
            const response = await api.post(`triagem_senha/`, data)
            atendimento = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `triagem-senha-atendimento`)
        return atendimento
    },
    async AdicionarComentarioAtendimento({commit}, data) {
        commit('setAtendimentoLoading', `adicionar-comentario-atendimento-${data.atendimento}`)
        var added = false
        try{
            await api.post(`${data.atendimento}/adicionar_comentario/`, data)
            added = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `adicionar-comentario-atendimento-${data.atendimento}`)
        return added
    },
    async ListarComentarioAtendimento({commit}, atendimento_id) {
        commit('setAtendimentoLoading', `listar-comentario-atendimento-${atendimento_id}`)
        var comentarios = []
        try{
            const response = await api.get(`${atendimento_id}/listar_comentarios/`)
            comentarios = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('dropAtendimentoLoading', `listar-comentario-atendimento-${atendimento_id}`)
        return comentarios
    },
};
export default {
    state,
    getters,
    actions,
    mutations
};