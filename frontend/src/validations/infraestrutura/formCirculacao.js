import store from './../../store/store'
import FormValidation from '../forms/index'

class InfraCirculacaoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        if(!('responsavel' in form) || !form.responsavel) messages.push('Responsável não informado!')
        if(!('local' in form) || !form.local) messages.push('Local de uso não informado!')
        if(!('previsao_devolucao' in form) || !form.previsao_devolucao) messages.push('Previsão de devolução não informada!')
        if(!form.id){
            // validar na criação
            if(!('itens_dispositivos' in form) || (form.itens_dispositivos||[]).length == 0) messages.push('Dispositivos não informados')
        }
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_receber(form={}){
        let messages = []
        if(!('data_baixa' in form) || !form.data_baixa) messages.push('Data de baixa não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_transferir(form={}){
        let messages = []
        if(!('responsavel' in form) || !form.responsavel) messages.push('Responsável não informado!')
        if(!('previsao_devolucao' in form) || !form.previsao_devolucao) messages.push('Previsão de devolução não informada!')
        if(!('local' in form) || !form.local) messages.push('Local não informado!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_cancelar(form={}){
        let messages = []
        if(!('motivo_cancelamento' in form) || !form.motivo_cancelamento) messages.push('Motivo de cancelamento não informado!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default InfraCirculacaoFormValidation