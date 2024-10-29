import WikiService from '../../../services/wiki/wikiService';
const api = new WikiService()
const state = {
    wikis: [],
    wiki_loading:false,
    categorias: [],
    categoria_loading:false,
};
const getters = {
    StateWikis: state => state.wikis,
    StateWikiLoading: state => state.wiki_loading,
    StateWikiCategorias: state => state.categorias,
    StateWikiCategoriaLoading: state => state.categoria_loading,
};
const mutations = {
    setWikis(state, value){ state.wikis = value },
    setWikiLoading(state, value){ state.wiki_loading = value },
    setWikiCategorias(state, value){ state.categorias = value },
    setWikiCategoriaLoading(state, value){ state.categoria_loading = value },
};
const actions = {
    async GetWikis({commit}, params={}) {
        commit('setWikiLoading', true)
        try{
            const response = await api.get('wiki/',{...params, page_size:1000})
            const wikis = response.data.results
            commit('setWikis', Object.assign([],wikis))
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiLoading', false)
    },
    async GetWiki({commit}, id) {
        commit('setWikiLoading', true)
        try{
            let response = await api.get(`wiki/${id}/`)
            commit('setWikiLoading', false)
            return response
        }catch(error){
            commit('setWikiLoading', false)
            return error
            // commit("setAlerts", [ error.toast_message ])
        }
    },
    async UpdateWiki({commit, dispatch, getters}, data) {
        dispatch
        getters
        commit('setWikiLoading', true)
        var updated = false
        try{
            let response = await api.patch(`wiki/${data.id}/`, data)
            response
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiLoading', false)
        return updated
    },
    async CreateWiki({commit}, data) {
        commit('setWikiLoading', true)
        var created = false
        try{
            let response = await api.post('wiki/',data)
            response
            // console.log('CreateWiki', response)
            created = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Inclusão de nova documentação',
                message:`Documentação criada com sucesso!`
                }
            ])
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiLoading', false)
        return created
    },
    async DeleteWiki({commit}, data) {
        commit('setWikiLoading', true)
        var deleted = false
        try{
            await api.delete(`wiki/${data.id}/`)
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Exclusão de Documentação',
                    message:`A documentação foi removida com sucesso!`
                }
            ])
            deleted = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiLoading', false)
        return deleted
    },
    async GetWikiCategorias({commit}, params={}) {
        commit('setWikiCategoriaLoading', true)
        try{
            let response = await api.get('categoria-sistema/',{...params, page_size:200})
            commit('setWikiCategorias', response.data.results)
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiCategoriaLoading', false)
    },
    async UpdateWikiCategoria({ commit }, data) {
        commit('setWikiCategoriaLoading', true)
        var updated = false
        try{
            let response = await api.patch(`categoria-sistema/${data.id}/`, data)
            response
            updated = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiCategoriaLoading', false)
        return updated
    },
    async CreateWikiCategoria({commit}, data) {
        commit('setWikiCategoriaLoading', true)
        var created = false
        try{
            let response = await api.post('categoria-sistema/',data)
            response
            created = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Inclusão de nova categoria',
                message:`Categoria criada com sucesso!`
                }
            ])
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiCategoriaLoading', false)
        return created
    },
    async DeleteWikiCategoria({commit}, data) {
        commit('setWikiCategoriaLoading', true)
        var deleted = false
        try{
            await api.delete(`categoria-sistema/${data.id}/`)
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Exclusão de categoria',
                    message:`A categoria foi removida com sucesso!`
                }
            ])
            deleted = true
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setWikiCategoriaLoading', false)
        return deleted
    },
    // async GetAgendaLabsWikisPaginate({commit, getters}) {
    //     try{
    //         let response = await api.genericGetRequest(getters.StateManageResultsRequestRoom.next)
    //         const {count, next, previous, results} = response.data
    //         let wikis = getters.StateWikis
    //         wikis.push(...results)
    //         commit('setWikis', wikis)
    //         commit('setManageResultsRequestRoom', {count, next, previous})
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