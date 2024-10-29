import ConfigService from '../index'
class GestorService extends ConfigService {
    constructor(){
        super('agendalabs/api/v1/gestores/')
    }
}
export default GestorService
