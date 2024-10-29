<template>
    <div>
        <div v-if="atendente?.perfil_object?.pode_atender">
            <!-- CARDS DE FILA DE SENHA -->
            <v-card flat>
                <v-card-text>
                    <v-row>
                        <v-checkbox hide-details v-model="minhas_senhas" label="Monitorar somente minhas senhas"></v-checkbox>
                        <v-spacer></v-spacer>
                        <div class="text-caption">
                            <div><v-icon-small color="error">mdi-circle</v-icon-small>Acima de 30m</div>
                            <div><v-icon-small color="warning">mdi-circle</v-icon-small>Acima de 20m</div>
                            <div><v-icon-small color="success">mdi-circle</v-icon-small>Até 20m</div>
                        </div>
                    </v-row>
                    <v-row>
                        <v-col v-for="senha in senhas_do_usuario" :key="senha">
                            <v-card flat color="transparent">
                                <v-card-text class="text-center align-content-center pa-2">
                                    <div>
                                        <v-chip :tile="false" label
                                            link
                                            :color="senha.prioridade_object.nome==='Prioridade'? 'yellow':'info'"
                                            :key="senha.id"
                                            :title="`${senha?.id} | ${senha?.sigla_senha}: ${senha?.servico_object?.nome}`"
                                            >
                                            <span :class="senha.prioridade_object.nome==='Prioridade'? 'text-error':'text-white'">
                                                <v-icon-small :color="calculaExpectativaAtendimento(senha).color" title="Expectativa de Senha">mdi-circle</v-icon-small>
                                                <v-icon-small v-if="senha.redirecionado_por" title="Senha redirecionada">mdi-swap-horizontal</v-icon-small> {{senha.sigla_senha}}
                                            </span>
                                            <v-menu activator="parent" v-if="habilitaMenu">
                                                <v-list>
                                                    <v-list-item
                                                        v-for="item in [
                                                            { value: 'chamar', atendimento: senha, title: 'Antecipar Atendimento' },
                                                        ]"
                                                        :key="item.atendimento.id"
                                                        :value="item.value"
                                                        @click.stop="onSelectMenuItem(item)"
                                                    >
                                                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                                                    </v-list-item>
                                                </v-list>
                                            </v-menu>
                                        </v-chip>
                                    </div>
                                    <div>
                                        <small>{{tempoEspera(senha)}}</small>
                                    </div>
                                    <div>
                                        <small>{{senha.prioridade_object.nome}}</small>
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>

            <ws-jr :ws_channel="`channel_painel_atendimento_${atendente?.unidade}`"
                app="Painel do Atendente"
                @on-message="onMessageWebSocket"
                />
        </div>
    </div>
</template>

<script>
export default {
    name: 'FilaSenhasComponent',
    props: {
        atendente: {
            required: true
        },
        habilitaMenu: {
            default: false
        },
    },
    data: ()=>({
        painel: {},
        minhas_senhas: true,
        fila_senhas: []
    }),
    methods: {
        notificarAlerta(){
            Notification.requestPermission().then(function (permission) {
                // Se o usuário conceder a permissão, exibe uma notificação
                if (permission === "granted") {
                    // Verifica se o navegador suporta notificações
                    if ('Notification' in window) {
                        // Função para exibir a notificação
                        const opcoes = {
                            body: 'Nova Senha Emitida',
                            icon: 'favicon.png' // Opcional: ícone da notificação
                        };

                        new Notification('Atendimento - Intranet!', opcoes);
                        // const notificacao = new Notification('Notificação!', opcoes);

                        // Ação após o usuário clicar na notificação
                        // notificacao.onclick = function () {
                        //     window.open('https://example.com'); // Redireciona para o site, por exemplo
                        // };

                    } else {
                        console.log('Notificações não suportadas pelo navegador.');
                    }
                }
            });
        },
        onMessageWebSocket(value){
            this.$emit('on-called-ws', value)
            if(value?.event === 'LIST-TICKET'){
                // Atualiza a lista de fila de senhas
                this.fila_senhas = value.obj
            }
            if(value?.event === 'PRINTED-TICKET' && value?.notify){
                const servico_id = value?.obj?.servico_id
                if( (this.atendente?.servicos||[]).includes(servico_id)){
                    this.notificarSom()
                    this.notificarAlerta()
                }
            }
        },
        onSelectMenuItem(item){
            this.$emit('actionMenu', item)
        },
        notificarSom(){
            return new Promise((resolve, reject) => {
                var filename = 'ding.mp3'

                const audio = new Audio()
                audio.src = `/audio/${filename}`
                audio.onended = resolve
                audio.onerror = reject
                audio.play().catch((error) => {
                    console.error('Falha ao tentar reproduzir o áudio:', error);

                    // Aqui você pode tratar a falha de reprodução. Por exemplo, exibir uma mensagem
                    // ou retornar um erro customizado.
                    // reject(new Error('Reprodução de áudio falhou: interação do usuário necessária.'));
                });
            })
        },
        converteSegundos(data){
            // Defina uma data arbitrária (por exemplo, 1 de outubro de 2024, 12:00)
            let date = new Date(data);

            // Obtenha a data e hora atuais
            let now = new Date();

            // Calcule a diferença em milissegundos
            let diffInMs = now - date; // resultado em milissegundos

            // Converta a diferença em horas, minutos e segundos
            let diffInSeconds = Math.floor(diffInMs / 1000);
            let diffInMinutes = Math.floor(diffInSeconds / 60);
            let diffInHours = Math.floor(diffInMinutes / 60);

            // Resto para minutos e segundos
            let hours = diffInHours;
            let minutes = diffInMinutes % 60;
            let seconds = diffInSeconds % 60;

            return {hours, minutes, seconds}
        },
        tempoEspera(item){
            const tempo = this.converteSegundos(item.data_chegada)

            return `${String(tempo.hours).padStart(2, '0')}:${String(tempo.minutes).padStart(2, '0')}:${String(tempo.seconds).padStart(2, '0')}`
        },
        calculaExpectativaAtendimento(item){
            const tempo = this.converteSegundos(item.data_chegada)
            const alta = (tempo.hours == 0 && tempo.minutes > 30) || tempo.hours > 0;
            const media = tempo.hours == 0 && tempo.minutes > 20
            if(alta) return { color: 'error' }
            else if (media) return {color: 'warning'}
            else return { color: 'success' }
        }
    },
    computed: {
        senhas_do_usuario(){
            if(!this.minhas_senhas){
                return this.fila_senhas
            }
            const senhas = this.fila_senhas.filter(o => this.atendente.servicos.includes(o.servico_object.id))
            return senhas
        }
    }
}
</script>