<template>
    <div>
        <loading-jr
            :propObject="StateAtendimentoLoading.includes('triagem-senha-atendimento')"
            text="Gerando nova senha..."
        ></loading-jr>
        <div v-if="atendente?.perfil_object?.acessa_triagem">
            <div>
                <v-row class="nmp">
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details label="Documento"
                            v-model="cliente.matricula">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details label="Nome" v-model="cliente.nome"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details label="E-mail" v-model="cliente.email"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details label="Contato" v-model="cliente.celular"></v-text-field>
                    </v-col>
                </v-row>
                <div v-if="ultima_senha?.id">
                    <v-divider class="my-2"></v-divider>
                    <v-row>
                        <v-col cols="12" sm="4">
                            <v-btn-small :tile="false" @click="imprimir(ultima_senha)">
                                <v-icon>mdi-printer</v-icon> Última Senha {{ultima_senha.sigla_senha}}
                            </v-btn-small>
                        </v-col>
                    </v-row>
                </div>
                <v-divider class="my-2"></v-divider>
                <v-row class="nmp">
                    <v-col cols="12" sm="6" v-for="s in servicos" :key="'servico_'+s.id">
                        <v-card outlined flat>
                            <v-card-text>
                                <v-row>
                                    <div>
                                        <div class="text-subtitle-2 text-primary">{{s.nome}}</div>
                                        <small>{{s.departamento_object.nome}}</small>
                                    </div>
                                    <v-spacer></v-spacer>
                                    <div class="align-content-center">
                                        <v-btn-small 
                                            :disabled="!atendente.id"
                                            :tile="false"
                                            class="mr-1 pa-1"
                                            v-for="p in prioridades"
                                            :color="p.nome === 'Prioridade'? 'error': 'success'"
                                            :key="'prioridade_'+p.id"
                                            @click="triagemSenha({
                                                                    prioridade: p.id,
                                                                    unidade: atendente.unidade,
                                                                    servico: s.id,
                                                                    atendente_tri: atendente.id
                                                                })">
                                            {{p.nome.toUpperCase()}}
                                        </v-btn-small>
                                    </div>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </div>
        </div>
        <div v-else>
            <v-row class="pa-8" v-if="atendente.id">
                <v-col class="align-content-center text-center">
                    Atendente sem permissão a triagem
                </v-col>
            </v-row>
        </div>

    </div>
</template>

<script>

import { mapGetters, mapActions, mapMutations } from 'vuex';

export default {
    name: 'TriagemComponent',
    data: ()=>({
        atendimento: {},
        cliente: {},
        atendente: {},
        unidades: [],
        servicos: [],
        prioridades: [],
        ultima_senha: {}
    }),
    mounted(){
        this.init()
    },
    methods: {
        ...mapActions([
            'GetAtendenteLogado',
            'TriagemSenhaAtendimento', 
            'GetServicosAtendimento',
            'GetPrioridadesAtendimento',
            'GetInfoAluno'
            ]),
        ...mapMutations([
            'SetInfoAluno'
        ]),
        init(){
            this.atendenteLogado()
        },
        async getInfoAluno(params){
            await this.GetInfoAluno(params)
            if(this.StateInfoAluno?.aluno?.RA){
                this.cliente.matricula = this.StateInfoAluno?.aluno?.RA
                this.cliente.nome = this.StateInfoAluno?.aluno?.NOME
                this.cliente.email = this.StateInfoAluno?.aluno?.EMAIL
                var contatos = []
                if (this.StateInfoAluno?.aluno?.TELEFONE1){
                    contatos.push(this.StateInfoAluno?.aluno?.TELEFONE1)
                }
                if (this.StateInfoAluno?.aluno?.TELEFONE2){
                    contatos.push(this.StateInfoAluno?.aluno?.TELEFONE2)
                }
                this.cliente.celular = contatos.join(' / ')
            }

        },
        async atendenteLogado(){
            const atendente = await this.GetAtendenteLogado()
            this.atendente = atendente
            this.onSelectUnidade(this.atendente.unidade)
        },
        async listarPrioridades(unidade_id){
            const prioridades = await this.GetPrioridadesAtendimento({unidade: unidade_id})
            this.prioridades = prioridades
        },
        async listarServicos(unidade_id){
            const servicos = await this.GetServicosAtendimento({unidade: unidade_id, serial: 'full'})
            this.servicos = servicos
        },
        async triagemSenha(params){
            this.SetInfoAluno({})
            if(this.cliente.matricula || this.cliente.nome){
                params['cliente'] = this.cliente
            }
            const atendimento = await this.TriagemSenhaAtendimento(params)
            if(!atendimento.id){
                alert('Atendimento não foi gerado!')
                return
            }
            this.ultima_senha = atendimento
            this.imprimir(atendimento)
            this.cliente = Object.assign({}, {})
        },
        async onSelectUnidade(value){
            await this.listarServicos(value)
            await this.listarPrioridades(value)
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
                    </html>
            `;
            var newWindow = window.open();
            newWindow.document.write(page);
            newWindow.document.close();
            newWindow.onload = function(){
                newWindow.focus()
                newWindow.print()
                newWindow.close()
            }
        }
    },
    computed: {
        ...mapGetters(['StateAtendimentoLoading',
            'StateInfoAluno',
            'StateInfoAlunoLoading'
            ]),
    }
}
</script>
