import store from '@/store/store'
import FormValidation from './../index'
class PeriodoQuestFormValidation extends FormValidation {
    validate(form={}){
        let messages = []
        if(Object.prototype.hasOwnProperty.call(form, 'periodo') && !form.periodo) messages.push('Período não informado!')
        if(Object.prototype.hasOwnProperty.call(form, 'questionario') && !form.questionario) messages.push('Questionário não informado!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default PeriodoQuestFormValidation