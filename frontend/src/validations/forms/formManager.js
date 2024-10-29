import store from '../../store/store'
import FormValidation from '.'
class ManagerFormValidation extends FormValidation{
    validateEmail(email) {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }
    validate(form={}){
        let messages = []
        //Valida Gestor
        if(Object.prototype.hasOwnProperty.call(form, 'name') && !form.name) messages.push('Nome não informado!')
        if(Object.prototype.hasOwnProperty.call(form, 'email')){
            if(!this.validateEmail(form.email)) {
                messages.push('E-mail informado é inválido!')
            }
            else if(!form.email) {
                messages.push('E-mail não informado!')
            }
        }
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default ManagerFormValidation