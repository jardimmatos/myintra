import store from './../../store/store'
import FormValidation from '../forms/index'

class InfraItemCirculacaoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        if(!('responsavel' in form) || !form.responsavel) messages.push('Responsável não informado!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_receber(form={}){
        let messages = []
        if(!('devolvido_em' in form) || !form.devolvido_em) messages.push('Data não informada!')
            let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_estornar(form={}){
        let messages = []
        if(!('obs' in form) || !form.obs) messages.push('Observação de estorno não informada!')
            let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_avariar(form={}){
        let messages = []
        if(!('devolvido_em' in form) || !form.devolvido_em) messages.push('Data não informada!')
            let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_cancelar(form={}){
        let messages = []
        if(!('obs' in form) || !form.obs) messages.push('Observação de cancelamento não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
    validate_extraviar(form={}){
        let messages = []
        if(!('devolvido_em' in form) || !form.devolvido_em) messages.push('Data não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default InfraItemCirculacaoFormValidation