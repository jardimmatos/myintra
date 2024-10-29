import store from './../../store/store'
import FormValidation from '../forms/index'

class InfraDispositivoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        if(!('identificador' in form) || !form.identificador) messages.push('Identificador não informado!')
        if(!('equipamento' in form) || !form.equipamento) messages.push('Equipamento não informado!')
        // if(!('serie' in form) || !form.serie) messages.push('Nº de série não informado!')
        if(!('status_inventario' in form) || !form.status_inventario) messages.push('Status no inventário não informado!')
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default InfraDispositivoFormValidation