import ConfigService from '../index'
class LogAgendaService extends ConfigService {
    constructor(){
        super('agendalabs/api/v1/logs/')
    }
}
export default LogAgendaService
