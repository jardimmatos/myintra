import axios from 'axios'
import CustomRequestException from '@/exceptions/CustomRequestException'
import FrontendService from '@/services/frontendService'
const fes = new FrontendService()
class ConfigService {
    constructor(apiurl){
        this.apiurl = apiurl;
        this.ax = axios.create({
            baseURL: process.env.NODE_ENV === 'production' ?
            process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV,
        })
        this.headers = {}
    }
    async post(url, objeto){
        await this.verify_or_refreshing()
        try{
            const requestUrl = `${this.apiurl}${url}`
            return await this.ax.post(requestUrl, objeto, { headers: this.headers })
        }catch(error){
            throw new CustomRequestException(error)
        }
    }
    async patch(url, objeto){
        await this.verify_or_refreshing()
        try{
            const requestUrl = `${this.apiurl}${url}`
            return await this.ax.patch(requestUrl, objeto, { headers: this.headers })
        }catch(error){
            throw await new CustomRequestException(error)
        }
    }
    async put(url, objeto){
        await this.verify_or_refreshing()
        try{
            const requestUrl = `${this.apiurl}${url}`
            return await this.ax.put(requestUrl, objeto, {headers: this.headers})
        }catch(error){
            throw await new CustomRequestException(error)
        }
    }
    async delete(url, params){
        await this.verify_or_refreshing()
        try{
            const requestUrl = `${this.apiurl}${url}`
            return await this.ax.delete(requestUrl, {params, headers: this.headers})
        }catch(error){
            throw await new CustomRequestException(error)
        }
    }
    async get(url, params){
        await this.verify_or_refreshing()
        try{
            const requestUrl = `${this.apiurl}${url}`
            return await this.ax.get(requestUrl, {params, headers: this.headers})
        }catch(error){
            throw await new CustomRequestException(error)
        }
    }
    async authenticated_user(){
        let base_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
        const requestUrl = `${base_url}/user/api/v1/global/authenticated_user/`
        try{
            const r = await this.ax.get(requestUrl, {headers: this.headers})
            return r
        } catch (ex) {
            console.error('catch error authenticated_user',ex)
            return null
        }
    }
    async verify_or_refreshing(refresh_user=false){
        // método para atualização de token e refresh token
        // base url da api para ambientes homologação e produção
        let base_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
        // Recupera o token atual
        let token = localStorage.getItem(fes.SESSION_TOKEN)
        // se não houver token, passar token vazio "-"
        if(!token) token ='-'
        // monta o header para requisitar a url de verificação
        this.headers = {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        //prepara a requisição  de verificação
        let response_verify = async () => await axios.post(base_url+'/auth/api/v1/token/verify/', {token:token})
        try{
            await response_verify()
            let has_session_username = localStorage.getItem(fes.SESSION_USERNAME)
            let has_user_authenticated = localStorage.getItem(fes.SESSION_USER_AUTHENTICATED)

            /* obter usuário autenticado somente se não houver localStorage  */
            if (!has_session_username || !has_user_authenticated || refresh_user){
                try{
                    const authed = await this.authenticated_user()

                    localStorage.setItem(fes.SESSION_USERNAME, authed.data.username);
                    localStorage.setItem(fes.SESSION_USER_AUTHENTICATED, JSON.stringify(authed.data))
                } catch (e){
                    console.log('exception', e)
                }
            }
        }catch /*(error_resp_verify)*/{

            try {
                const r = await this.refreshToken()
                localStorage.setItem(fes.SESSION_TOKEN, r.data.access)
                localStorage.setItem(fes.SESSION_REFRESH_TOKEN, r.data.refresh)
                token = localStorage.getItem(fes.SESSION_TOKEN)
                // Atualiza o header para novas requisições
                this.headers = {
                    'Authorization': `Bearer ${token}`,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }

                if (refresh_user){
                    const authed = await this.authenticated_user()
                    // console.log('authed on refresh', authed)
                    localStorage.setItem(fes.SESSION_USERNAME, authed.data.username);
                    localStorage.setItem(fes.SESSION_USER_AUTHENTICATED, JSON.stringify(authed.data))
                }
            } catch /*(e)*/ {
                // console.log('catch on refreshing token', e)
                
                // Em caso de erro com o refresh token, remover todo localStorage
                localStorage.removeItem(fes.SESSION_TOKEN)
                localStorage.removeItem(fes.SESSION_REFRESH_TOKEN)
                localStorage.removeItem(fes.SESSION_USER_AUTHENTICATED)
                localStorage.removeItem(fes.SESSION_USERNAME)
                // Em seguida redirecionar para login
                window.location.href = '/'
            }
        }
        return
    }

    // used to get paginate urls
    async genericGetRequest(url, params, with_auth=true){
        if (with_auth){
            await this.verify_or_refreshing()
        }
        try{
            return await this.ax.get(url,{ params, headers: this.headers})
        }catch(error){
            throw new CustomRequestException(error)
        }
    }

    async genericPostRequest(url, data){
        // Not Auth routes POST
        try{
            return await this.ax.post(url, data, {headers: this.headers})
        }catch(error){
            throw new CustomRequestException(error)
        }
    }
    async verifyToken(){
        let base_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
        let token = localStorage.getItem(fes.SESSION_TOKEN)
        return await axios.post(base_url+'/auth/api/v1/token/verify/', {token:token})
    }
    async refreshToken(){
        let base_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
        let token = localStorage.getItem(fes.SESSION_REFRESH_TOKEN)
        return await axios.post(base_url+'/auth/api/v1/token/refresh/', {refresh:token})
    }
}
export default ConfigService