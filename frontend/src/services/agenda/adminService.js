import ConfigService from '../index'
class AdminService extends ConfigService {
    constructor(){
        super('agendalabs/api/v1/admins/')
    }
}
export default AdminService
