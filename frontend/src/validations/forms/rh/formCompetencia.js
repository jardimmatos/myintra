import store from '@/store/store'
import FormValidation from './../index'
class CompetenciaFormValidation extends FormValidation {
    validate(form={}){
        let messages = []
        if(Object.prototype.hasOwnProperty.call(form, 'nome') && !form.nome) messages.push('Nome não informado!')
        // if(Object.prototype.hasOwnProperty.call(form, 'descricao') && !form.descricao) messages.push('Descrição não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default CompetenciaFormValidation