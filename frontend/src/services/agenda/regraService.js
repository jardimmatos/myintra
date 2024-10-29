import ConfigService from '../index'
class RegraService extends ConfigService {
    constructor(){
        super('agendalabs/api/v1/regras/')
    }
}
export default RegraService
