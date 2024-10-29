
class FormValidation{
    getAlerts(messages=[]){
        let alerts = []
        for (let msg of messages){
            alerts.push({ tag: 'warn', title:'Validação de Formulário', message: msg})
        }
        return alerts
    }
}
export default FormValidation