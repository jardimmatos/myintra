import ConfigService from '../index'
class InfraService extends ConfigService {
    constructor(){
        super('infraestrutura/api/v1/')
    }
}
export default InfraService
