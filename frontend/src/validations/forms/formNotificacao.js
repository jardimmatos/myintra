import store from '../../store/store'
import FormValidation from '.'
class NotificacaoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Título
        if(Object.prototype.hasOwnProperty.call(form, 'titulo') && !form.titulo) messages.push('Título de notificação é obrigatório')
        //Valida data inicio
        if(Object.prototype.hasOwnProperty.call(form, 'inicio') && !form.inicio) messages.push('A data de início da notificação é obrigatória')
        //Valida data fim
        if(Object.prototype.hasOwnProperty.call(form, 'fim') && !form.fim) messages.push('A data fim da notificação é obrigatória')
        //Valida corpo
        if(Object.prototype.hasOwnProperty.call(form, 'mensagem') && !form.mensagem) messages.push('O conteúdo da notificação não foi informado')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default NotificacaoFormValidation