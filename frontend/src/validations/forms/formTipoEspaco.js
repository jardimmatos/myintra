import store from '../../store/store'
import FormValidation from '.'
class TipoEspacoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Tipo de Salas
        if(Object.prototype.hasOwnProperty.call(form, 'description') && !form.description) messages.push('Informe o nome do tipo de sala')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default TipoEspacoFormValidation