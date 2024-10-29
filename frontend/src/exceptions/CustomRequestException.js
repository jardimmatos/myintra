class CustomRequestException extends Error {
    constructor(message) {
        super(message)
        this.name = 'CUSTOM_EXCEPTION'
        this.error = message
        var toast_message = {
            tag:'error',
            title:'Error',
            message: this.error.message,
            timeout: "7000"
        }
        // DEBUG
        if(process.env.NODE_ENV !== 'production'){
            // console.log('LOGGED USER (DEBUG)', JSON.parse(localStorage.getItem(fes.SESSION_USER_AUTHENTICATED)))
        }
        
        if(this.error.code == 'ERR_BAD_REQUEST'){
            // console.log('error', this.error)
            if(this.error.response && this.error.response.data){
                const data = this.error.response.data
                var first_error = '...'
                if (typeof(data) == 'string'){
                    if (this.error.response.status == 404){
                        first_error =  'Nada encontrado!'
                    }else{
                        first_error =  data
                    }
                }
                if (typeof(data) == 'object'){
                    // {} e [] são do tipo 'object',
                    // abaixo, em try catch é testado quem tem .length
                    if (data.length === undefined){
                        //se undefined,  então é json, caso contrario é array
                        let first_key = Object.keys(data)
                        // obtem o primeiro erro
                        first_error = data[first_key[0]] + (first_key != 'non_field_errors' ?`#(${first_key})`: '')
                        // traduzir mensagem original do backend
                        if (first_error === "No active account found with the given credentials(detail)"){
                            first_error = 'Usuário e/ou senha inválido(s)!'
                        }
                    }else{
                        try{
                            // Tratamento quando o response data retorna formato JSON com aspas simples
                            // E o js não reconhece quando utilizamos o JSON.parse, por isso a necessidade de replace
                            // Posteriormente, é feito o parse
                            let dt = data[0]
                            dt = dt.replaceAll("'", '"')
                            dt = JSON.parse(dt)
                            let first_key = Object.keys( dt )
                            // obtem o primeiro erro
                            first_error = dt[first_key[0]]
                        }catch{
                            first_error = data[0]
                        }
                        // first_error = data[0]
                    }
                }
                toast_message.title = "Atenção"
                toast_message.message = first_error
            }
        }
        if(this.error.code == 'ERR_BAD_RESPONSE'){
            // ERROR 500 CASES
            if(this.error.response && this.error.response.status == 500){
                toast_message.title = "500"
                toast_message.message = 'Erro no servidor'
                console.error(JSON.stringify(this.error.response.data).substring(0,600))
            }else{
                toast_message.title = this.error.response.status+ '- ERR_BAD_RESPONSE'
                toast_message.message = this.error.response.statusText
            }
        }
        // Conexão com a internet
        if (this.error.code === "ERR_NETWORK"){
            if (this.error.message == 'Network Error'){
                toast_message.title = "Falha de conexão"
                toast_message.message = "Não foi possível conectar com o Servidor! Possivelmente, o servidor pode estar for do ar ou em manutenção"+this.error.message
            }else{
                toast_message.title = this.error.message
                toast_message.message = "Status da resposta "+ this.error.response.status
            }
        }
        // Usuário não identificado
        if (this.error.response && this.error.response.data && this.error.response.data.code === "user_not_found"){
            // Usuário não encontrado
            toast_message.title = "Usuário"
            toast_message.message = "Usuário não identificado!"
        }
        this.error = {...this.error, toast_message}
        return this.error
    }
}
export default CustomRequestException