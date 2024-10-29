import store from '../../store/store'
import FormValidation from '.'
class RoleFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Role
        if(Object.prototype.hasOwnProperty.call(form, 'week_day') && form.week_day == null) messages.push('Dia da semana não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'start_time') && !form.start_time) messages.push('Horário inicial não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'end_time') && !form.end_time) messages.push('Horário final não informado')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default RoleFormValidation