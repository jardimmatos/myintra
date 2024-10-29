import ConfigService from '@/services'
class UserService extends ConfigService {
    constructor(){
        super('user/api/v1/')
    }
    
}
export default UserService
