<template>
    <span></span>
</template>
<script>
// import { bus } from '@/main'
import { mapActions, mapMutations } from 'vuex';
export default {
    props:{
        app: {
            required:true,
        },
        ws_channel:{
            required:true,
        },
        debug:{
            default: process.env.NODE_ENV !== 'production'
        },
    },
    data: () => ({
        ws_socket: null
    }),
    mounted(){
        // Considerando a conexão do websocket no watch, quando é alterado novamente
        // para um valor diferente de "channel"
        this.ws_connect()
    },
    created(){
    },
    methods:{
        ...mapMutations([]),
        ...mapActions([]),
        onCreatedEmit(value){
            // se o bus receber um emit de created, disparar para o ws do app um evento CREATED
            if (this.debug) console.log(`on created ${this.app} ws`)
            let data = {
                "event": "CREATED",
                "message": value
            }
            this.ws_socket.send(JSON.stringify(data))
        },
        onChangedEmit(value){
            // se o bus receber um emit de changed, disparar para o ws do app um evento CHANGED
            if (this.debug) console.log(`on changed ${this.app} ws`)
            let data = {
                "event": "CHANGED",
                "message": value
            }
            this.ws_socket.send(JSON.stringify(data))
        },
        onDeletedEmit(value){
            // se o bus receber um emit de deleted, disparar para o ws do app um evento DELETED
            if (this.debug) console.log(`on deleted ${this.app} ws`)
            let data = {
                "event": "DELETED",
                "message": value,
                "notify":false // não notificar
            }
            this.ws_socket.send(JSON.stringify(data))
        },
        initialize_ws(){
            let url_ws = ''
            if (process.env.NODE_ENV === 'production'){
                url_ws = process.env.VUE_APP_BACKEND_PROD.replace('https://', '')
            }else{
                url_ws = process.env.VUE_APP_BACKEND_DEV.replace('http://', '')
                // url_ws = 'localhost:8000'
            }
            var connectionString = (window.location.protocol == 'https:' ? 'wss://' : 'ws://')+ url_ws + '/ws/global/' + this.ws_channel + '/';
            if (this.ws_socket){
                this.ws_socket.close()
            }
            this.ws_socket = new WebSocket(connectionString);
        },
        ws_connect(){
            this.initialize_ws()
            this.ws_socket.onopen = ()=> {
                if (this.debug) console.log(`Socket ${this.app} aberto: ${this.ws_channel}`)
                this.$emit("on-ready", true)
            };
            this.ws_socket.onclose = (e)=> {
                if (this.debug) console.info(`Socket ${this.app} fechado: ${this.ws_channel}`, e)
                switch(e.code){
                    case 1000: {
                            // (brekado pelo front) "Normal closure, meaning that the purpose for which the connection was established has been fulfilled.";
                            // quando, por exemplo,usuário sai de um componente para outro
                            if (this.debug) console.info(`Frontend restarted`)
                            break;
                        }
                    case 1001: break;// "An endpoint is \"going away\", such as a server going down or a browser having navigated away from a page.";
                    case 1002: break;// "An endpoint is terminating the connection due to a protocol error";
                    case 1003: break;// "An endpoint is terminating the connection because it has received a type of data it cannot accept (e.g., an endpoint that understands only text data MAY send this if it receives a binary message).";
                    case 1004: break;// "Reserved. The specific meaning might be defined in the future.";
                    case 1005: break;// "No status code was actually present.";
                    case 1006: {
                            // (brekado pelo backend)"The connection was closed abnormally, e.g., without sending or receiving a Close control frame";
                            //0 - CONNECTING, 1 - OPEN, 2 - CLOSING, 3 - CLOSED
                            setTimeout(()=>{
                                this.ws_connect()
                            }, 5000)
                            // this.ws_connect();
                            if (this.debug) console.info(`Backend stopped`)
                            break;
                        }
                    case 1007: break;// "An endpoint is terminating the connection because it has received data within a message that was not consistent with the type of the message (e.g., non-UTF-8 [https://www.rfc-editor.org/rfc/rfc3629] data within a text message).";
                    case 1008: break;// "An endpoint is terminating the connection because it has received a message that \"violates its policy\". This reason is given either if there is no other sutible reason, or if there is a need to hide specific details about the policy.";
                    case 1009: break;// "An endpoint is terminating the connection because it has received a message that is too big for it to process.";
                    case 1010: break;// "An endpoint (client) is terminating the connection because it has expected the server to negotiate one or more extension, but the server didn't return them in the response message of the WebSocket handshake. <br /> Specifically, the extensions that are needed are: " + event.reason;
                    case 1011: break;// "A server is terminating the connection because it encountered an unexpected condition that prevented it from fulfilling the request.";
                    case 1015: break;// "The connection was closed due to a failure to perform a TLS handshake (e.g., the server certificate can't be verified).";
                    default: return  // "Unknown reason";
                }
            };
            this.ws_socket.onerror = (e) => {
                if (this.debug) console.info(`Socket ${this.app} with Error. `, e)
            }
            // Sending the info about the room
            this.ws_socket.onmessage = (e) => {
                if (e === undefined) return
                // recuperando mensagem do servidor
                // retornar a mensagem recebida para a saída do componente WS
                let data = JSON.parse(e.data);
                data = data["payload"];
                // retornar do componente WS todo o payload e tratar fora deste conforme as regras de negócio
                this.$emit("on-message", data);
            }
            if (this.ws_socket.readyState == WebSocket.OPEN) {
                this.ws_socket.onopen();
            }
        },
    },
    watch: {
        ws_channel(v){
            if(v !== 'channel'){
                setTimeout(()=>{
                    this.ws_connect()
                }, 1500)
            }
        }
    },
    unmounted(){
        if (this.debug) console.log('on destroy WS', this.app)
        
        if (this.ws_socket && this.ws_socket.readyState === WebSocket.OPEN) {
            this.ws_socket.close();
        }
    },
}
</script>