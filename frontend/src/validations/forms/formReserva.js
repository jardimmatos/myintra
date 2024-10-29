import store from '../../store/store'
import FormValidation from '.'
class ReservaFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Reserva
        if(Object.prototype.hasOwnProperty.call(form, 'responsavel') && !form.responsavel) messages.push('Responsável não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'titulo') && !form.titulo) messages.push('Título não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'espaco') && !form.espaco) messages.push('Espaço não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'finalidade') && !form.finalidade) messages.push('Finalidade não informada')
        if(Object.prototype.hasOwnProperty.call(form, 'date') && !form.date) messages.push('Data não informada')
        if(Object.prototype.hasOwnProperty.call(form, 'start') && !form.start) messages.push('Horário início não informado')
        if(Object.prototype.hasOwnProperty.call(form, 'end') && !form.end) messages.push('Horário final não informado')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default ReservaFormValidation