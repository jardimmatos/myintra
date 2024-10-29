export default class FrontendService {
    constructor(){
        this.SESSION_TOKEN = '_token';
        this.SESSION_REFRESH_TOKEN = '_refresh_token';
        this.SESSION_USERNAME = '_username';
        this.SESSION_USER_AUTHENTICATED = '_authenticated_user';
    }

    isSuper(){
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        return authenticated && authenticated.id && authenticated.is_superuser
    }
    
    isStaff(){
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        return authenticated && authenticated.id && authenticated.is_staff
    }

    has_group(group_name){
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        if(authenticated && authenticated.id){
            return authenticated.get_groups.includes(group_name) || authenticated.is_superuser
        }
        return false
    }

    has_perm(code_permission, considerar_superusuario=true){
        /** Parâmetro valida */
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        if(authenticated && authenticated.id){
            const tem_permissao = authenticated.get_perms.includes(code_permission);
            const eh_superuser = considerar_superusuario ? authenticated.is_superuser : false;
            return tem_permissao || eh_superuser
        }
        return false
    }

    has_bis(){
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        if(authenticated && authenticated.id){
            return authenticated.user_count_bis
        }
        return false
    }

    is_atendente(){
        const authenticated = JSON.parse(localStorage.getItem(this.SESSION_USER_AUTHENTICATED))
        if(authenticated && authenticated.id){
            return authenticated.is_atendente
        }
        return false
    }

    set_token_local(response, user){
        localStorage.setItem(this.SESSION_TOKEN, response.data.access);
        localStorage.setItem(this.SESSION_REFRESH_TOKEN, response.data.refresh);
        localStorage.setItem(this.SESSION_USERNAME, user.username);
        localStorage.setItem(this.SESSION_USER_AUTHENTICATED, JSON.stringify(response.data.auth))
    }

    remove_token_local(){
        localStorage.removeItem(this.SESSION_TOKEN)
        localStorage.removeItem(this.SESSION_REFRESH_TOKEN)
        localStorage.removeItem(this.SESSION_USERNAME)
        localStorage.removeItem(this.SESSION_USER_AUTHENTICATED)
    }

    getOptionsToastr = (options ={}) => {
        return {
            ...options
        }
    }

    actual_state_color(value){
        switch(value){
            case 'Em breve': return 'info'
            case 'Finalizado': return 'grey'
            case 'Em andamento': return 'success'
            default: return 'secondary'
        }
    }

    status_reserva_label(value){
        switch(value){
            case 'PENDING': return 'PENDENTE'
            case 'OPENED': return 'ABERTO'
            case 'CANCELLED': return 'CANCELADO'
            default: return '-'
        }
    }

    status_reserva_color(value){
        switch(value){
            case 'PENDING': return 'warning'
            case 'OPENED': return 'success'
            case 'CANCELLED': return 'error'
            default: return 'secondary'
        }
    }
}
