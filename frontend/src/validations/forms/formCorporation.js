import store from '../../store/store'
import FormValidation from '.'
class CorporationFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Tipo de Salas
        if(Object.prototype.hasOwnProperty.call(form, 'fantasy_name') && !form.fantasy_name) messages.push('Nome fantasia não informado!')
        if(Object.prototype.hasOwnProperty.call(form, 'registered_name') && !form.registered_name) messages.push('Razão social não informada!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default CorporationFormValidation