import store from '../../store/store'
import FormValidation from '.'
class WikiFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Título
        if(Object.prototype.hasOwnProperty.call(form, 'titulo') && !form.titulo) messages.push('Título é obrigatório')
        //Valida Sistema Categoria
        if(Object.prototype.hasOwnProperty.call(form, 'sistema') && !form.sistema) messages.push('Categoria de Sistema obrigatória')
        //Valida Corpo
        if(Object.prototype.hasOwnProperty.call(form, 'corpo') && !form.corpo) messages.push('Corpo não pode ser vazio')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default WikiFormValidation