import ConfigService from '../index'
class NotificacaoService extends ConfigService {
    constructor(){
        super('notificacao/api/v1/notificacao/')
    }
}
export default NotificacaoService
