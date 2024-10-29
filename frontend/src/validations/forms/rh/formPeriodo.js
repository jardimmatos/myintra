import store from '@/store/store'
import FormValidation from './../index'
class PeriodoFormValidation extends FormValidation {
    validate(form={}){
        let messages = []
        if(Object.prototype.hasOwnProperty.call(form, 'descricao') && !form.descricao) messages.push('Descrição não informada!')
        if(Object.prototype.hasOwnProperty.call(form, 'inicio') && !form.inicio) messages.push('Data Início não informada!')
        if(Object.prototype.hasOwnProperty.call(form, 'fim') && !form.fim) messages.push('Data Fim não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default PeriodoFormValidation