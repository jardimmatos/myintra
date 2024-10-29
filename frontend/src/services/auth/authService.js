import CustomRequestException from '../../exceptions/CustomRequestException'
import axios from 'axios'
class AuthService {
    constructor(){
        this.axios = axios.create({
            baseURL: process.env.NODE_ENV === 'production' ?
            process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV,
        })
    }
    async authenticate(data){
        try{
            return await this.axios.post('auth/api/v1/token/', data)
        }catch(error){
            throw new CustomRequestException(error)
        }
    }
}
export default AuthService
