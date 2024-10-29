import ConfigService from '../index'
// import CustomRequestException from '../../exceptions/CustomRequestException'
// import FrontendService from '../frontendService'
// import axios from 'axios'
// const fes = new FrontendService()
class AuthService extends ConfigService {
    constructor(){
        super('repositoriobi/api/v1/')
    }
    async user_bis(){
        // return await this.get('bi/user/')
        return await this.get('categoria/categorias_pais_filhos/')
    }
}
export default AuthService
