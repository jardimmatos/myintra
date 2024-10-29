import store from '../../store/store'
import FormValidation from '.'
class EspacoFormValidation extends FormValidation{
    validate(form={}){
        let messages = []
        //Valida Tipo de Espaço
        if(Object.prototype.hasOwnProperty.call(form, 'tipo_espaco') && !form.tipo_espaco) messages.push('Tipo de espaço é obrigatório')
        //Valida Gestores
        if(Object.prototype.hasOwnProperty.call(form, 'gestores') && form.gestores.length == 0) messages.push('Necessário vincular gestor(es) ao espaço')
        //Valida duração máxima
        if(Object.prototype.hasOwnProperty.call(form, 'max_duracao') && [null, undefined, ''].includes(form.max_duracao)) messages.push('Necessário informar a duração máxima')
        //Valida duração minima
        if(Object.prototype.hasOwnProperty.call(form, 'min_duracao') && [null, undefined, ''].includes(form.min_duracao)) messages.push('Necessário informar a duração mínima')
        //Valida carencia criacao
        if(Object.prototype.hasOwnProperty.call(form, 'min_criacao') && [null, undefined, ''].includes(form.min_criacao)) messages.push('Necessário informar a carência de abertura')
        //Valida limitacao por usuário
        if(Object.prototype.hasOwnProperty.call(form, 'limitar_abertura_qtde')){
            if(Object.prototype.hasOwnProperty.call(form, 'limitar_abertura')){
                if (form.limitar_abertura){
                    if( [null, undefined, '', 0].includes(form.limitar_abertura_qtde)){
                        messages.push('Necessário parametrizar o limite por usuário')
                    }
                }else{
                    if(![null, undefined, '', 0].includes(form.limitar_abertura_qtde)){
                        messages.push('Limitar Abertura deve estár habilitada quando a quantidade for parametrizada')
                    }
                }
            }
        }
        let alerts = this.getAlerts(messages)
        store.commit('setAlerts', alerts)
        return messages.length == 0
    }
}
export default EspacoFormValidation