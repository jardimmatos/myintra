import InfraService from '@/services/infraestrutura/infraService';
const api = new InfraService()
const state = {
    locais: [],
    equipamentos: [],
    enums_dispositivos: [],
    status_dispositivos: [],
    dispositivos: [],
    enums_circulacao: [],
    circulacao: [],
    log_circulacao: {},
    log_dispositivo: {},
    enums_item_circulacao: [],
    loading_id: null
};
const getters = {
    StateRecursosLocais: state => state.locais,
    StateRecursosEquipamentos: state => state.equipamentos,
    StateRecursosStatusDispositivos: state => state.status_dispositivos,
    StateRecursosLogDispositivo: state => state.log_dispositivo,
    StateRecursosDispositivos: state => state.dispositivos,
    StateRecursosLogCirculacao: state => state.log_circulacao,
    StateRecursosCirculacao: state => state.circulacao,
    StateRecursosEnumsDispositivos: state => state.enums_dispositivos,
    StateRecursosEnumsCirculacao: state => state.enums_circulacao,
    StateRecursosEnumsItemCirculacao: state => state.enums_item_circulacao,
    StateRecursosLoading: state => state.loading_id,
};
const mutations = {
    setRecursosLoading(state, value){
        state.loading_id = value
    },
    setRecursosLocais(state, value){
        state.locais = value
    },
    setRecursosEquipamentos(state, value){
        state.equipamentos = value
    },
    setRecursosDispositivos(state, value){
        state.dispositivos = value
    },
    setRecursosLogDispositivo(state, value){
        state.log_dispositivo = value
    },
    setRecursosStatusDispositivos(state, value){
        state.status_dispositivos = value
    },
    setRecursosLogCirculacao(state, value){
        state.log_circulacao = value
    },
    setRecursosCirculacao(state, value){
        state.circulacao = value.map(m => m.dict_read_only)
    },
    setRecursosEnumsDispositivos(state, value){
        state.enums_dispositivos = value
    },
    setRecursosEnumsCirculacao(state, value){
        state.enums_circulacao = value
    },
    setRecursosEnumsItemCirculacao(state, value){
        state.enums_item_circulacao = value
    }
};

const actions = {
    // Locais
    async GetRecursosLocais({commit}, params) {
        commit('setRecursosLoading', 'get-locais')
        try{
            let response = await api.get('local-uso/', {...params, page_size:500 })
            commit('setRecursosLocais', response.data.results)
          }catch(error){
            commit('setRecursosLocais', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async CreateRecursosLocais({commit}, data) {
        var create = false
        commit('setRecursosLoading', 'create-locais')
        try{
            await api.post('local-uso/', data)
            create = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cadastro de Local',
                message:`Local ${data.descricao} cadastrado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return create
    },
    async UpdateRecursosLocais({commit}, data) {
        var update = false
        commit('setRecursosLoading', `update-locais-${data.id}`)
        try{
            await api.patch(`local-uso/${data.id}/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cadastro de Local',
                message:`Local ${data.descricao} atualizado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    
    // Equipamentos
    async GetRecursosEquipamentos({commit}, params) {
        commit('setRecursosLoading', 'get-equipamentos')
        try{
            let response = await api.get('equipamentos/', { ...params, page_size: 500 })
            commit('setRecursosEquipamentos', response.data.results)
        }catch(error){
            commit('setRecursosEquipamentos', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async CreateRecursosEquipamentos({commit}, data) {
        var create = false
        commit('setRecursosLoading', 'create-equipamentos')
        try{
            await api.post('equipamentos/', data)
            create = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cadastro de Equipamentos',
                message:`Equipamento ${data.descricao} cadastrado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return create
    },
    async UpdateRecursosEquipamentos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `update-equipamentos-${data.id}`)
        try{
            await api.patch(`equipamentos/${data.id}/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Alteração de Equipamentos',
                message:`Equipamento ${data.descricao} atualizado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    
    // Status Dispositivos
    async GetRecursosStatusDispositivos({commit}, params) {
        commit('setRecursosLoading', 'get-status-dispositivos')
        try{
            let response = await api.get('status-dispositivos/', {...params, page_size:500 })
            commit('setRecursosStatusDispositivos', response.data.results)
        }catch(error){
            commit('setRecursosStatusDispositivos', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async CreateRecursosStatusDispositivos({commit}, data) {
        var create = false
        commit('setRecursosLoading', 'create-status-dispositivos')
        try{
            await api.post('status-dispositivos/', data)
            create = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Status de Dispositivo',
                message:`Status ${data.descricao} criado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return create
    },
    async UpdateRecursosStatusDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `update-status-dispositivos-${data.id}`)
        try{
            await api.patch(`status-dispositivos/${data.id}/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Status de Dispositivo',
                message:`Status ${data.descricao} atualizado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },

    // Dispositivos
    async GetRecursosDispositivos({commit}, params) {
        commit('setRecursosLoading', 'get-dispositivos')
        try{
            let response = await api.get('dispositivos/', {...params, page_size:500 })
            commit('setRecursosDispositivos', response.data.results)
        }catch(error){
            commit('setRecursosDispositivos', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async GetRecursosLogDispositivo({commit}, params) {
        var results = {}
        commit('setRecursosLoading', `get-log-dispositivo-${params.dispositivo}`)
        try{
            let response = await api.get(`log-dispositivos/`, {...params})
            results = response.data
          }catch(error){
            results = {}
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return results
    },
    async DeleteRecursosLogDispositivo({commit}, params) {
        commit('setRecursosLoading', `delete-log-dispositivo-${params.dispositivo}`)
        try{
            await api.delete(`log-dispositivos/delete_logs/`, {...params})
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Limpeza de Logs',
                    message:`Logs removidos com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async GetRecursosEnumsDispositivos({commit}, params) {
        commit('setRecursosLoading', 'get-dispositivos-enums')
        try{
            let response = await api.get('dispositivos/get_enum_situacao/', {...params })
            commit('setRecursosEnumsDispositivos', response.data)
        }catch(error){
            commit('setRecursosEnumsDispositivos', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async CreateRecursosDispositivos({commit}, data) {
        var create = false
        commit('setRecursosLoading', 'create-dispositivos')
        try{
            await api.post('dispositivos/', data)
            create = true
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Cadastro de Dispositivos',
                    message:`Dispositivo ${data.identificador} cadastrado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return create
    },
    async UpdateRecursosDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `update-dispositivos-${data.id}`)
        try{
            await api.patch(`dispositivos/${data.id}/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cadastro de Dispositivos',
                message:`Dispositivo ${data.identificador} atualizado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async DisponibilizarRecursosDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `enable-dispositivos-${data.id}`)
        try{
            const response = await api.post(`dispositivos/${data.id}/set_disponivel/`)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Disponibilizar dispositivo',
                message:`Dispositivo ${response.data.identificador} ${response.data.equipamento_object.descricao} habilitado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async ManutencaoRecursosDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `manutencao-dispositivos-${data.id}`)
        try{
            const response = await api.post(`dispositivos/${data.id}/set_manutencao/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Dispositivo em manutenção',
                message:`Dispositivo ${response.data.identificador} ${response.data.equipamento_object.descricao} remanejado para manutenção!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async ExtravioRecursosDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `extravio-dispositivos-${data.id}`)
        try{
            const response = await api.post(`dispositivos/${data.id}/set_extravio/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Extravio de Dispositivo',
                message:`Dispositivo ${response.data.identificador} ${response.data.equipamento_object.descricao} registrado como extravio!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async AvariaRecursosDispositivos({commit}, data) {
        var update = false
        commit('setRecursosLoading', `avaria-dispositivos-${data.id}`)
        try{
            const response = await api.post(`dispositivos/${data.id}/set_avaria/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Avaria de Dispositivo',
                message:`Dispositivo ${response.data.identificador} ${response.data.equipamento_object.descricao} registrado com avaria!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    
    //Circulacao
    async GetRecursosCirculacao({commit}, params) {
        commit('setRecursosLoading', 'get-circulacao')
        try{
            let response = await api.get('circulacao/', {...params})
            commit('setRecursosCirculacao', response.data)
          }catch(error){
            commit('setRecursosCirculacao', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async GetRecursosLogCirculacao({commit}, params) {
        var results = {}
        commit('setRecursosLoading', `get-log-circulacao-${params.circulacao}`)
        try{
            let response = await api.get(`log-circulacao/`, {...params})
            results = response.data
            // commit('setRecursosLogCirculacao', response.data)
          }catch(error){
            results = {}
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return results
    },
    async DeleteRecursosLogCirculacao({commit}, params) {
        commit('setRecursosLoading', `delete-log-circulacao-${params.circulacao}`)
        try{
            await api.delete(`log-circulacao/delete_logs/`, {...params})
            commit("setAlerts", [ {
                    tag:'success',
                    title:'Limpeza de Logs',
                    message:`Logs removidos com sucesso!`
                }
            ])
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async GetRecursosEnumsCirculacao({commit}, params) {
        commit('setRecursosLoading', 'get-circulacao-enums')
        try{
            let response = await api.get('circulacao/get_enum_situacao/', params)
            commit('setRecursosEnumsCirculacao', response.data)
          }catch(error){
            commit('setRecursosEnumsCirculacao', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
    },
    async CreateRecursosCirculacao({commit}, data) {
        var create = false
        commit('setRecursosLoading', 'create-circulacao')
        try{
            await api.post('circulacao/', data)
            create = true
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return create
    },
    async UpdateRecursosCirculacao({commit}, data) {
        var update = false
        commit('setRecursosLoading', `update-circulacao-${data.id}`)
        try{
            const response = await api.patch(`circulacao/${data.id}/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Circulação',
                message:`Circulação no local ${response.data.local_object.descricao} atualizado com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async ReceberRecursosCirculacao({commit}, data) {
        var update = false
        commit('setRecursosLoading', `receber-circulacao-${data.id}`)
        try{
            await api.post(`circulacao/${data.id}/set_receber/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Baixa de Circulação',
                message:`Circulação baixada com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async CancelarRecursosCirculacao({commit}, data) {
        var update = false
        commit('setRecursosLoading', `cancelar-circulacao-${data.id}`)
        try{
            await api.post(`circulacao/${data.id}/set_cancelar/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cancelamento de Circulação',
                message:`Circulação cancelada com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async TransferirRecursosCirculacao({commit}, data) {
        var update = false
        commit('setRecursosLoading', `transferir-circulacao-${data.id}`)
        try{
            await api.post(`circulacao/${data.id}/set_transferir/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Transferência de Circulação',
                message:`Circulação transferida com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async PesquisarPessoasRecursosCirculacao({commit}, params) {
        var result = []
        commit('setRecursosLoading', `pesquisar-pessoas-circulacao`)
        try{
            const response = await api.get(`circulacao/pesquisar_pessoas/`, params)
            result = response.data
        }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return result
    },
    
    // CirculacaoItem
    async ReceberRecursosCirculacaoItem({commit}, data) {
        var update = false
        commit('setRecursosLoading', `receber-circulacao-item`)
        try{
            const response = await api.post(`item-circulacao/set_receber/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Baixa de Item de Circulação',
                message:`${response.data.length } Baixa(s) realizada(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async EstornarRecursosCirculacaoItem({commit}, data) {
        var update = false
        commit('setRecursosLoading', `estornar-circulacao-item`)
        try{
            const response = await api.post(`item-circulacao/set_estornar/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Estorno de Item de Circulação',
                message:`${response.data.length } Estorno(s) realizado(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async AvariarRecursosCirculacaoItem({commit}, data) {
        var update = false
        commit('setRecursosLoading', `avariar-circulacao-item`)
        try{
            const response = await api.post(`item-circulacao/set_avaria/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Avaria de Item de Circulação',
                message:`${response.data.length } Avaria(s) registradas(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async CancelarRecursosCirculacaoItem({commit}, data) {
        var update = false
        commit('setRecursosLoading', `cancelar-circulacao-item`)
        try{
            const response = await api.post(`item-circulacao/set_cancelar/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Cancelamento de Item de Circulação',
                message:`${response.data.length } Item(ns) cancelado(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async ExtraviarRecursosCirculacaoItem({commit}, data) {
        var update = false
        commit('setRecursosLoading', `extravio-circulacao-item`)
        try{
            const response = await api.post(`item-circulacao/set_extravio/`, data)
            update = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Extravio de Item de Circulação',
                message:`${response.data.length } extravio(s) realizado(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return update
    },
    async AddRecursosCirculacaoItem({commit}, data) {
        var added = false
        commit('setRecursosLoading', `add-circulacao-item`)
        try{
            await api.post(`item-circulacao/`, data)
            added = true
            commit("setAlerts", [ {
                tag:'success',
                title:'Inclusão de Itens à Circulação',
                message:`Item(ns) adicionado(s) com sucesso!`
                }
            ])
          }catch(error){
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setRecursosLoading', null)
        return added
    },
    

};
export default {
  state,
  getters,
  actions,
  mutations
};