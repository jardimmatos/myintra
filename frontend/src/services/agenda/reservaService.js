import ConfigService from '../index'
class ReservaService extends ConfigService {
    constructor(){
        super('agendalabs/api/v1/reservas/')
    }
}
export default ReservaService
