<template>
    <div>
        <loading-jr :propObject="StateAtendimentoLoading.includes('list-servicos')" :text="'Carregando Serviços'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('get-atendente-logado')" :text="'Caregando atendente...'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('get-painel-atual-atendente')" :text="'Carregando Atendimento do Atendente'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('encerrar-atendimento')" :text="'Encerrando Atendimento'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('redirecionar-atendimento')" :text="'Redirecionando Atendimento'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('nao-compareceu-atendimento')" :text="'Cliente não compareceu'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('altera-atendente')" :text="'Atualizando Atendente'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('chamar-proxima-senha')" :text="'Chamando próxima senha'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('chamar-senha-novamente')" :text="'Chamando a senha novamente'" />
        <loading-jr :propObject="StateAtendimentoLoading.includes('triagem-senha-atendimento')" :text="'Triando nova senha'" />

        <div v-if="atendente?.perfil_object?.pode_atender">
            <v-row>
                <!-- CARDS BOTOES -->
                <v-col cols="4" sm="3" class="pl-0">
                    <!-- CARD CHAMAR PRÓXIMO -->
                    <v-card
                        v-if="!painel.id"
                        :disabled="!!StateAtendimentoLoading.length"
                        :loading="StateAtendimentoLoading.includes('chamar-proxima-senha')"
                        height="80"
                        class="align-content-center"
                        color="warning"
                        @click="chamar_proximo()">
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-bullhorn</v-icon>
                            </div>
                            <div>Chamar</div>
                        </v-card-text>
                    </v-card>
                    <!-- CARD CHAMAR NOVAMENTE -->
                    <v-card v-if="painel.id && painel?.atendimento_object?.status_atendimento == 'chamado'"
                        height="80"
                        :loading="StateAtendimentoLoading.includes('chamar-senha-novamente')"
                        class="align-content-center"
                        color="grey"
                        @click="chamar_novamente"
                        >
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-bullhorn</v-icon>
                            </div>
                            <div>Chamar novamente</div>
                        </v-card-text>
                    </v-card>
                    <!-- CARD INICIAR ATENDIMENTO -->
                    <v-card 
                        v-if="painel?.atendimento_object?.status_atendimento === 'chamado'"
                        height="80"
                        :loading="StateAtendimentoLoading.includes('iniciar-atendimento')"
                        class="align-content-center"
                        color="success"
                        @click="iniciar_atendimento"
                        >
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-play</v-icon>
                            </div>
                            <div>Iniciar atendimento</div>
                        </v-card-text>
                    </v-card>
                    <!-- CARD ENCERRAR ATENDIMENTO -->
                    <v-card v-if="painel?.atendimento_object?.status_atendimento === 'iniciado'"
                        height="80"
                        :loading="StateAtendimentoLoading.includes('encerrar-atendimento')"
                        class="align-content-center"
                        color="info"
                        @click="confirmar_encerrar_atendimento"
                        >
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-stop</v-icon>
                            </div>
                            <div>Encerrar</div>
                        </v-card-text>
                    </v-card>
                    <!-- CARD REDIRECIONAMENTO -->
                    <v-card v-if="['chamado', 'iniciado'].includes(painel?.atendimento_object?.status_atendimento)"
                        height="80"
                        :loading="StateAtendimentoLoading.includes('redirecionar-atendimento')"
                        class="align-content-center"
                        color="#555"
                        @click="confirmar_redirecionar_atendimento">
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-swap-horizontal</v-icon>
                            </div>
                            <div>Redirecionar</div>
                        </v-card-text>
                    </v-card>
                    <!-- CARD NAO COMPARECEU -->
                    <v-card v-if="painel?.atendimento_object?.status_atendimento === 'chamado'"
                        height="80"
                        :loading="StateAtendimentoLoading.includes('nao-compareceu-atendimento')"
                        class="align-content-center"
                        color="error"
                        @click="nao_compareceu(painel?.id)">
                        <v-card-text class="text-center">
                            <div>
                                <v-icon size="large">mdi-account-off</v-icon>
                            </div>
                            <div>Não compareceu</div>
                        </v-card-text>
                    </v-card>
                    <!-- COMENTÁRIOS DO ATENDIMENTO -->
                    <!-- MODAL DE COMENTÁRIOS -->
                    <modal-jr code="modal_comentarios"
                        :no-actions="false"
                        :persistent="false"
                        ref="modal_comentarios"
                        toolbar-title="Observações do Atendimento"
                        v-if="['chamado', 'iniciado'].includes(painel?.atendimento_object?.status_atendimento)">
                        <template v-slot:activate-slot>
                            <v-card v-if="['chamado', 'iniciado'].includes(painel?.atendimento_object?.status_atendimento)"
                                height="80" link
                                :loading="StateAtendimentoLoading.includes('nao-compareceu-atendimento')"
                                class="align-content-center"
                                color="success">
                                <v-card-text class="text-center">
                                    <div>
                                        <v-icon size="large">mdi-chat</v-icon>
                                    </div>
                                    <div>Observações</div>
                                </v-card-text>
                            </v-card>
                        </template>
                        <template v-slot:body>
                            <v-row class="nmp">
                                <v-col cols="12" sm="12" v-if="painel?.atendimento_object?.id">
                                    <div>
                                        <AdicionarComentarioAtendimento :atendimento="painel.atendimento_object.id"/>
                                    </div>
                                </v-col>
                            </v-row>
                        </template>
                    </modal-jr>
                    <!-- CARD REFLEXO DE CHAMADA SENHA PAINEL -->
                    <v-card
                        v-if="painel?.atendimento_object?.sigla_senha"
                        height="100"
                        class="align-content-center"
                        :class="{'text-error':painel?.atendimento_object?.prioridade_object?.nome == 'Prioridade'}"
                        :color="isBlinking ? 'white':'black'">
                        <v-card-text class="text-center">
                            <div><b>{{painel?.atendimento_object?.sigla_senha}}</b></div>
                            <small>Preview Painel</small>
                        </v-card-text>
                    </v-card>
                </v-col>

                <!-- CARDS DE INFORMACOES DE ATENDIMENTO -->
                <v-col cols="8" sm="9">
                    <!-- DADOS ATENDENTE -->
                    <div v-if="atendente.usuario_object" class="mb-1">
                        <v-row class="mb-2">
                            <div class="text-grey">{{atendente?.unidade_object?.nome}}</div>
                            <v-spacer></v-spacer>
                            <div class="text-grey">
                                {{atendente?.usuario_object?.first_name}} {{atendente?.usuario_object?.last_name}}
                                <modal-jr code="modal_servicos_atendente"
                                    :no-actions="true" :persistent="false"
                                    ref="modal_servicos_atendente"
                                    toolbar-title="Serviços do Atendente"
                                    dialog-width="60%">
                                    <template v-slot:activate-slot>
                                        <v-icon-small>mdi-cog</v-icon-small>
                                    </template>
                                    <template v-slot:body>
                                        <v-row>
                                            <v-col cols="12" sm="6">
                                                <label class="text-grey">Serviços do Atendente </label>
                                                <small v-for="s in servicos_atendimento.filter(o => atendente.servicos.includes(o.id))" :key="s.id">
                                                    <li>{{s.nome}}</li>
                                                </small>
                                            </v-col>
                                            <v-col cols="12" sm="6">
                                                <label class="text-grey">Local do atendente</label>
                                                <div>
                                                    <label for="atendente_local_id">Local</label>
                                                    <v-autocomplete style="min-width: 100px" id="atendente_local_id"
                                                        :disabled="StateAtendimentoLoading.includes('altera-atendente')"
                                                        v-model="atendente.local" 
                                                        @update:modelValue="updateAtendente({local: $event})"
                                                        @blur="edit_local=false"
                                                        item-value="id"
                                                        item-title="nome"
                                                        :items="locais_atendimento"
                                                    ></v-autocomplete>
                                                </div>
                                                <div>
                                                    <label for="atendente_numero_id">Número do local</label>
                                                    <v-select style="min-width: 100px"
                                                        :disabled="StateAtendimentoLoading.includes('altera-atendente')"
                                                        v-model="atendente.numero_local" 
                                                        @update:modelValue="updateAtendente({numero_local: $event})"
                                                        @blur="edit_num_local=false"
                                                        :items="[1,2,3,4,5,6,7,8,9,10]"
                                                    ></v-select>
                                                </div>

                                            </v-col>
                                        </v-row>
                                    </template>
                                </modal-jr>
                            </div>
                        </v-row>
                    </div>

                    <!-- MSG USUARIO NAO É ATENDENTE -->
                    <div v-else class="mb-1">
                        <v-alert border="start" border-color="error" color="error" elevation="2">
                            <v-card
                                class="align-content-center"
                                color="error">
                                <v-card-text class="text-center">
                                    <div>Usuário não é atendente</div>
                                </v-card-text>
                            </v-card>
                        </v-alert>
                    </div>

                    <!-- DADOS CLIENTE -->
                    <div v-if="painel?.atendimento_object?.cliente_object?.id" class="mb-1">
                        <v-alert border="start" border-color="warning" color="white" elevation="2">
                            <label class="label-cards text-grey">CLIENTE </label>
                            <v-divider class="mb-2"></v-divider>
                            <v-row class="nmp">
                                <v-col cols="12" sm="7">
                                    <div class="text-caption">NOME:
                                        <span class="text-subtitle-2" style="display: inline-block;">
                                            {{painel?.atendimento_object?.cliente_object?.nome}}
                                        </span>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="5">
                                    <div class="text-caption">MATRÍCULA:
                                        <span class="text-subtitle-2">
                                            {{painel?.atendimento_object?.cliente_object?.matricula}}
                                        </span>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="7">
                                    <div class="text-caption">E-MAIL:
                                        <span class="text-subtitle-2" style="display: inline-block;">
                                            {{painel?.atendimento_object?.cliente_object?.email}}
                                        </span>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="7">
                                    <div class="text-caption">CONTATO:
                                        <span class="text-subtitle-2">
                                            {{painel?.atendimento_object?.cliente_object?.celular}}
                                        </span>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-alert>
                    </div>

                    <!-- DADOS DO ATENDIMENTO -->
                    <div v-if="painel?.atendimento_object?.id">
                        <v-alert border="start" border-color="warning" color="white" elevation="2">
                            <v-row class="mb-1">
                                <label class="label-cards text-grey">ATENDIMENTO </label>
                                <v-spacer></v-spacer>
                                <label class="label-cards text-grey">
                                    {{painel?.atendimento_object?.servico_object?.departamento_object?.nome}}
                                </label>
                            </v-row>
                            <v-divider class="mb-2"></v-divider>
                            <v-row class="nmp">
                                <v-col cols="12" sm="8">
                                    <div>
                                        <span :title="'Reimprimir #'+painel?.atendimento_object?.id" class="mr-2">
                                            <v-icon size="large" @click="imprimir(painel.atendimento_object)">mdi-qrcode</v-icon>
                                        </span>
                                        <span class="text-subtitle-2">{{painel?.atendimento_object?.servico_object?.nome}}</span>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="4" align="end">
                                    <div class="text-caption">
                                        <v-chip
                                            :color="painel?.atendimento_object?.prioridade_object?.nome =='Prioridade' ? '#ffff00': 'success'"
                                            :class="painel?.atendimento_object?.prioridade_object?.nome =='Prioridade' ? 'text-error': 'text-white'"
                                            size="small" :tile="false" label>
                                            <span class="ml-2" 
                                                :title="'Departamento: ' + painel?.atendimento_object?.servico_object?.departamento_object?.nome">
                                                <b>{{painel?.atendimento_object?.prioridade_object?.nome}}</b>
                                            </span>
                                        </v-chip>
                                    </div>
                                </v-col>
                                <v-col cols="12" sm="12" v-if="painel?.atendimento_object?.obs">
                                    <div class="text-caption">OBS:</div>
                                    <div class="text-subtitle-2">
                                        <u>{{painel?.atendimento_object?.obs}}</u>
                                    </div>
                                </v-col>
                                <v-col cols="12">
                                    <v-row>
                                        <v-col cols="12" sm="3">
                                            <v-card
                                                height="70"
                                                class="align-content-center"
                                                color="green-lighten-5">
                                                <v-card-text class="text-center pa-1">
                                                    <div class="text-caption">CHEGADA</div>
                                                    <div class="text-subtitle-2">
                                                        {{to_moment(painel?.atendimento_object?.data_chegada,'LTS')}}
                                                    </div>
                                                </v-card-text>
                                            </v-card>
                                        </v-col>
                                        <v-col cols="12" sm="3">
                                            <v-card
                                                height="70"
                                                class="align-content-center"
                                                color="green-lighten-5">
                                                <v-card-text class="text-center pa-1">
                                                    <div class="text-caption">CHAMADA</div>
                                                    <div class="text-subtitle-2">
                                                        {{to_moment(painel?.atendimento_object?.data_chamada,'LTS')}}
                                                    </div>
                                                </v-card-text>
                                            </v-card>
                                        </v-col>
                                        <v-col cols="12" sm="3">
                                            <v-card
                                                height="70"
                                                class="align-content-center"
                                                color="green-lighten-5">
                                                <v-card-text class="text-center pa-1">
                                                    <div class="text-caption">ESPERA</div>
                                                    <div class="text-subtitle-2">
                                                        {{calcula_tempo_espera(painel?.atendimento_object?.tempo_espera,'LTS')}}
                                                    </div>
                                                </v-card-text>
                                            </v-card>
                                        </v-col>
                                        <v-col cols="12" sm="3">
                                            <v-card
                                                height="70"
                                                class="align-content-center"
                                                color="green-lighten-5">
                                                <v-card-text class="text-center pa-1">
                                                    <div class="text-caption" title="Deslocamento">DESLOCAM.</div>
                                                    <div class="text-subtitle-2" v-if="painel?.atendimento_object?.tempo_deslocamento">
                                                        {{calcula_tempo_espera(painel?.atendimento_object?.tempo_deslocamento,'LTS')}}
                                                    </div>
                                                </v-card-text>
                                            </v-card>
                                        </v-col>
                                    </v-row>
                                </v-col>
                                <v-col cols="12" sm="3" v-if="false">
                                    <div class="text-caption">Status:</div>
                                    <div class="text-subtitle-2">
                                        <v-chip color="success">{{painel?.atendimento_object?.status_atendimento}}</v-chip>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-alert>
                        <v-divider class="my-1"></v-divider>
                    </div>
                </v-col>
            </v-row>

            <!-- MODAL DE ENCERRAMENTO -->
            <modal-jr code="modal_encerrar_atendimento"
                :no-actions="false"
                :persistent="false"
                ref="modal_encerrar_atendimento"
                toolbar-title="Encerrar Atendimento">
                <template v-slot:activate-slot>
                    <span></span>
                </template>
                <template v-slot:body>
                    <v-row class="nmp">
                        <v-col cols="12" sm="12">
                            <h3>Solução</h3>
                        </v-col>
                        <v-col cols="12" sm="7">
                            <!-- Solução -->
                            <v-autocomplete density="comfortable"
                                clearable
                                label="Resolução"
                                :items="[{value:'resolvido', title:'Resolvido'},{value:'pendente', title:'Pendente'}]"
                                item-value="value"
                                item-title="title"
                                v-model="encerrar_atendimento_obj.resolucao">
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="12" sm="7" v-if="false">
                            <!-- Obs -->
                            <v-textarea density="comfortable"
                                clearable
                                label="Obs"
                                v-model="encerrar_atendimento_obj.obs">
                            </v-textarea>
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:actions>
                    <v-spacer></v-spacer>
                    <v-col cols="12" sm="7">
                        <v-btn @click="encerrar_atendimento" variant="flat">Encerrar</v-btn>
                    </v-col>
                </template>
            </modal-jr>

            <!-- MODAL DE REDIRECIONAMENTO -->
            <modal-jr code="modal_redirecionar_atendimento"
                :no-actions="false"
                :persistent="false"
                ref="modal_redirecionar_atendimento"
                toolbar-title="Redirecionar Atendimento"
                >
                <template v-slot:activate-slot>
                    <span></span>
                </template>
                <template v-slot:body>
                    <v-row class="nmp">
                        <v-col cols="12" sm="12">
                            <h3>Redirecionar para Serviço</h3>
                        </v-col>
                        <v-col cols="12" sm="7">
                            <!-- Serviços -->
                            <v-autocomplete density="comfortable"
                                clearable
                                label="Selecione Serviço"
                                :items="servicos_atendimento.filter(obj=> !atendente.servicos.includes(obj.id))"
                                item-value="id"
                                item-title="nome"
                                v-model="redirecionar_atendimento_obj.servico"
                                :messages="servicos_atendimento.filter(obj=> !atendente.servicos.includes(obj.id)).length ? '': 'Nenhum outro Serviço ativo que este usuário não esteja vinculado foi encontrado!'">
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="12" sm="7" v-if="false">
                            <!-- Observação -->
                            <v-textarea label="Observação" v-model="redirecionar_atendimento_obj.obs"></v-textarea>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-divider></v-divider>
                        <v-col cols="12" sm="7">
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="redirecionar_atendimento" color="warning" variant="flat">Redirecionar</v-btn>
                </template>
            </modal-jr>

            <FilaSenha :atendente="atendente" 
                        @action-menu="onSelectedMenuItem"
                        @on-called-ws="onMessageWebSocket"
                        :habilita-menu="!atendente_em_atendimento" />
        </div>
        <div v-else>
            <v-row class="pa-8" v-if="atendente.id">
                <v-col class="align-content-center text-center">
                    Atendente sem permissão a atendimentos
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
import moment from 'moment'
import { mapActions, mapGetters } from 'vuex';
import AdicionarComentarioAtendimento from '@/components/atendimento/components/AdicionarComentarioAtendimento.vue';
import FilaSenha from '@/components/atendimento/components/FilaSenha.vue';
export default {
    name: 'AtenderComponent',
    components: {
        AdicionarComentarioAtendimento, FilaSenha
    },
    data: ()=>({
        atendente: {},
        edit_local: false,
        // edit_prioridade: false,
        edit_num_local: false,
        painel: {},
        isBlinking: false,
        // minhas_senhas: true,
        encerrar_atendimento_obj: {},
        redirecionar_atendimento_obj: {},
        locais_atendimento: [],
        servicos_atendimento: [],
        prioridades_atendimento: [],
        fila_senhas: []
    }),
    methods: {
        ...mapActions([
            'GetAtendenteLogado', 
            'GetPainelAtualAtendente',
            'GetLocaisAtendimento',
            'GetServicosAtendimento',
            'GetPrioridadesAtendimento',
            'AlterarAtendente',
            'ChamarProximaSenha',
            'ChamarSenhaNovamente',
            'IniciarAtendimento',
            'EncerrarAtendimento',
            'NaoCompareceuAtendimento',
            'RedirecionarAtendimento'
        ]),
        onMessageWebSocket(value){
            if(value?.event === 'CALL-TICKET' && value?.obj?.id==this.painel?.atendimento){
                // pisca somente quando for a respectiva senha chamada em relacao ao mesmo atendimento
                this.blinkCard()
            }
        },
        onSelectedMenuItem(value){
            if(value.value === 'chamar'){
                // Chamar senha manualmente
                this.chamar_proximo(value.atendimento.id)
            }
        },
        async imprimir(atendimento){
            // var body = document.getElementById('imprimir-ticket').innerHTML
            const url_host = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV;
            const text = `${url_host}/atendimento/acompanhamento/${atendimento?.id}/${atendimento?.sigla_senha}/`
            const qrcode = `https://quickchart.io/qr?text=${text}&size=128`
            var page = `
                <!DOCTYPE html>
                <html lang="pt-BR">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Imprimir Ticket</title>
                        <style>
                            body {
                                font-family: "Courier New", Courier, monospace;
                                text-align: center;
                            }
                        </style>
                    </head>
                    <body>
                        <div style="padding: 20px;1width: 300px;margin: 0 auto;width: 280px;">
                            <div style="font-size: 18px;font-weight: bold;text-wrap: wrap;max-width: 260px;text-align: center;">${atendimento?.unidade_object?.nome}</div>
                            <div style="font-size: 16px;margin: 10px auto;">${atendimento?.prioridade_object?.nome}</div>
                            <div style="font-size: 36px;font-weight: bold;margin: 10px 0;" id="ticket-number">${atendimento?.sigla_senha}</div>
                            <div><img src="${qrcode}" alt=""></div>
                            <div style="font-size: 16px;margin: 10px auto;">${atendimento?.servico_object?.nome}</div>
                            <div style="font-size: 12px;">${new Date(atendimento?.data_chegada).toLocaleString()}</div>
                            <div style="margin-top: 10px;font-size: 14px;">Os melhores se formam aqui</div>
                        </div>
                    </body>
                </html>`;
            
            const newWindow = window.open();
            newWindow.document.write(page);
            newWindow.document.close();
            newWindow.onload = function(){
                newWindow.focus()
                newWindow.print()
                newWindow.close()
            }
        },
        blinkCard() {
            let blinkCount = 0;
            const maxBlinks = 3;
            const blinkInterval = setInterval(() => {
                this.isBlinking = !this.isBlinking;
                blinkCount++;
                
                // Para após 3 blinks (6 alterações de estado)
                if (blinkCount >= maxBlinks * 2) {
                    clearInterval(blinkInterval);
                    this.isBlinking = false;
                }
            }, 500);
        },
        to_moment(data, formato){
            return moment(data).format(formato)
        },
        calcula_tempo_espera(t){
            const tempo = new Date(t*1000).toUTCString().substring(17,25)
            return tempo
        },
        async init(){
            await this.atendenteLogado()
            await this.painelAtual()
        },
        async updateAtendente(value){
            await this.AlterarAtendente(value)
            this.edit_num_local = false
            this.edit_local = false
            // this.edit_prioridade = false
            await this.atendenteLogado()
        },
        async listaLocais(unidade_id){
            const locais = await this.GetLocaisAtendimento({unidade: unidade_id})
            this.locais_atendimento = Object.assign([], locais)
        },
        async listaServicos(unidade_id){
            const servicos = await this.GetServicosAtendimento({unidade: unidade_id, serial: 'simple'})
            this.servicos_atendimento = Object.assign([], servicos)
        },
        async listaPrioridades(unidade_id){
            const prioridades = await this.GetPrioridadesAtendimento({unidade: unidade_id})
            this.prioridades_atendimento = Object.assign([], prioridades)
        },
        async atendenteLogado(){
            const atendente = await this.GetAtendenteLogado()
            this.atendente = atendente
            this.listaLocais(atendente.unidade)
            this.listaPrioridades(atendente.unidade)
            this.listaServicos(atendente.unidade)
        },
        async painelAtual(){
            const painel = await this.GetPainelAtualAtendente()
            this.painel = painel
        },
        async chamar_proximo(atendimento_id=null){
            const data = {
                atendimento_id: atendimento_id
            }
            const painel = await this.ChamarProximaSenha(data)
            this.painel = painel
            // await this.painelAtual()
        },
        async chamar_novamente(){
            if(!this.validaPainel()) return
            await this.ChamarSenhaNovamente({id: this.painel.id})
            
        },
        async iniciar_atendimento(){
            if(!this.validaPainel()) return
            const painel = await this.IniciarAtendimento({id: this.painel.id})
            this.painel = painel
        },
        confirmar_encerrar_atendimento(){
            this.$refs.modal_encerrar_atendimento.dialog=true
            this.encerrar_atendimento_obj.obs = this.painel?.atendimento_object?.obs
        },
        confirmar_redirecionar_atendimento(){
            this.$refs.modal_redirecionar_atendimento.dialog=true
        },
        async encerrar_atendimento(){
            if(!this.validaPainel()) return
            if(!this.encerrar_atendimento_obj.resolucao){
                alert('Resolução não informada!')
                return
            }
            let args = {...this.encerrar_atendimento_obj, id: this.painel.id}
            const encerrado = await this.EncerrarAtendimento(args)
            if (encerrado){
                this.$refs.modal_encerrar_atendimento.dialog=false
                this.encerrar_atendimento_obj = Object.assign({}, {})
                this.painel = Object.assign({},{})
            }

        },
        async redirecionar_atendimento(){
            if(!this.validaPainel()) return
            if(!this.redirecionar_atendimento_obj.servico){
                alert('Serviço não informado!')
                return
            }
            let args = {...this.redirecionar_atendimento_obj, id: this.painel.id}
            const redirecionado = await this.RedirecionarAtendimento(args)
            if (redirecionado){
                this.$refs.modal_redirecionar_atendimento.dialog=false
                this.redirecionar_atendimento_obj = Object.assign({}, {})
                this.painel = Object.assign({},{})
            }
        },
        async nao_compareceu(painel_id){
            if(!this.validaPainel()) return

            const confirma = confirm('Confirmar o não comparecimento?')
            if (!confirma) return

            const finalizado = await this.NaoCompareceuAtendimento({id: painel_id})
            if(finalizado){
                this.painel = Object.assign({},{})
            }
        },
        validaPainel(){
            if(!this.painel.id){
                alert('Painel/Senha não obtido para chamar senha novamente!')
                return false
            }
            return true
        }
    },
    mounted(){
        this.init()
    },
    computed: {
        ...mapGetters(['StateAtendimentoLoading']),
        atendente_em_atendimento(){
            // verifica se o usuário está atendendo no momento,
            // esta validação é necessária para bloquear a chamada manual quano o atendente estiver um atendimento corrente
            return !!this.painel.atendimento
        }
    }
}
</script>
<style scoped>
.label-cards{
    font-size: 12px;
    font-weight: 500;
}
</style>