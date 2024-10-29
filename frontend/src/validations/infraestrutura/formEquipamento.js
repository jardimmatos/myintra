import store from './../../store/store'
import FormValidation from '../forms/index'

class InfraEquipamentoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        if(!('descricao' in form) || !form.descricao) messages.push('Descrição não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default InfraEquipamentoFormValidation