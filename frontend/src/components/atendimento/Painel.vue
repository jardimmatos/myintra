<template>
    <div>
        <v-row class="nmp">
            <v-col cols="12" sm="9" class="nmp">
                <v-row class="nmp">
                    <v-col sm="12" class="nmp">
                        <v-card flat :class="`text-center align-content-center `"
                            style="height:82vh"
                            :style="'color:'+(chamada.prioridade == 'Prioridade' ? config.pageFontColorPriority : config.pageFontColorNormal)"
                            :color="chamada.prioridade == 'Prioridade' ? config.pageBgColorPriority : config.pageBgColorNormal">
                            <div v-if="!config.unidade">
                                <v-chip color="yellow" class="text-error text-subtitle-1">
                                    UNIDADE DE ATENDIMENTO NÃO PARAMETRIZADA
                                </v-chip>
                            </div>
                            <div class="senha-painel prioridade-label">{{chamada.prioridade}}</div>
                            <div class="senha-painel senha-label" :class="{ blink: isBlinking }">{{chamada.sigla_senha}}</div>
                            <div class="senha-painel local-label mb-6">{{chamada.local}}</div>
                            <div class="senha-painel atendente-label mb-3">{{chamada.atendente}}</div>
                            <div class="senha-painel em-label">chamada em {{chamada.em}}</div>
                        </v-card>
                    </v-col>
                    <v-col cols="12" class="nmp">
                        <v-card flat class="align-content-center footer-label px-6"
                            style="height:20vh"
                            :color="config.footerBgColor">
                            <v-row class="nmp">
                                <v-img v-if="config.img" max-height="300px" max-width="300px" min-width="300px" :src="config.img"></v-img>
                                <span class="px-2" :style="'align-self:center;white-space:pre-wrap;font-size:25px;color:'+config.footerFontColor">
                                    {{config.footerLabel}}
                                </span>
                                <v-spacer></v-spacer>
                            </v-row>
                        </v-card>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="3" class="pl-3" :style="'color:'+config.sidebarFontColor+';background:'+config.sidebarBgColor">
                <div style="height:85vh">
                    <v-row class="ma-0 pa-0">
                        <v-col cols="12" sm="12" class="my-4 pa-0 text-center historico-label">
                            HISTÓRICO
                            <v-btn-small @click="limparHistorico"
                                title="Limpar Histórico"
                                color="background"
                                :tile="false"
                                icon
                                variant="tonal">
                                <v-icon>mdi-close</v-icon>
                            </v-btn-small>
                        </v-col>
                        <v-divider class="mb-4"></v-divider>
                        <v-col v-for="i in chamada.historico||[]" sm="12" class="mb-4" :key="i">
                            <div class="item-historico-senha">{{i.sigla_senha}}</div>
                            <v-row class="nmp">
                                <span class="item-historico-local">{{i.local}}</span>
                                <v-spacer></v-spacer>
                                <!-- <span class="item-historico-prioridade">{{i.prioridade}}</span> -->
                                <v-chip-small :tile="false" label variant="flat"
                                    :color="i.prioridade == 'Prioridade' ? config.pageBgColorPriority : config.pageBgColorNormal">
                                    <span :style="'color:'+(i.prioridade == 'Prioridade' ? config.pageFontColorPriority : config.pageFontColorNormal)">
                                        <b>{{i.prioridade}}</b>
                                    </span>
                                </v-chip-small>
                            </v-row>
                        </v-col>
                    </v-row>
                </div>
                <v-row class="ma-0 pa-0">
                    <v-col cols="12" sm="12" class="ma-0 pa-0 text-center">
                        <clock-jr class="text-center" fontColor="#ccc"/>
                    </v-col>
                </v-row>

            </v-col>
        </v-row>
        <v-hover v-slot="{ isHovering, props }">
            <v-btn @click="openConfig"
                color="background"
                :tile="false"
                v-bind="props"
                icon
                :class="'fab '+ (isHovering ? 'fab-hovering':'')"
                variant="tonal">
                <v-icon>mdi-cog</v-icon>
            </v-btn>
        </v-hover>

        <modal-jr code="config_painel"
            :no-actions="true"
            :persistent="false"
            ref="config_painel"
            toolbar-title="Configurações de Painel"
            >
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Unidade</h3>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-autocomplete density="comfortable"
                            clearable :loading="StateAtendimentoLoading.includes('list-unidades')"
                            :rules="[v=> !!v || 'Campo obrigatório']"
                            label="Unidade de Atendimento"
                            :items="unidades"
                            v-model="config.unidade"
                            item-value="id"
                            item-title="nome">
                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Som</h3>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Som -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Selecione o Som..."
                            :items="alertsAvailable"
                            v-model="config.alert"
                            item-value="value"
                            item-title="name"
                            no-data-text="Nenhum Som carregado">
                            <template v-slot:append>
                                <v-btn :disabled="!config.alert" icon @click="notificarSom">
                                    <v-icon>mdi-play</v-icon>
                                </v-btn>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Senha Normal</h3>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- fundo -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="cor de fundo"
                            :items="cores"
                            v-model="config.pageBgColorNormal"
                            item-value="hexa"
                            item-title="name">
                            <template v-slot:append>
                                <v-chip :color="config.pageBgColorNormal || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.pageBgColorNormal || '#000000')">{{(config.pageBgColorNormal || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- fonte -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Cor de fonte"
                            :items="cores"
                            v-model="config.pageFontColorNormal"
                            item-value="hexa"
                            item-title="name">
                            <template v-slot:append>
                                <v-chip :color="config.pageFontColorNormal || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.pageFontColorNormal || '#000000')">{{(config.pageFontColorNormal || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Senha Prioridade</h3>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Prioridade Fundo -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fundo Chamada Senha Prioridade"
                            :items="cores"
                            v-model="config.pageBgColorPriority"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.pageBgColorPriority || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.pageBgColorPriority || '#000000')">
                                        {{(config.pageBgColorPriority || '#000000')}}
                                    </span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Prioridade Fonte -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fonte Chamada Senha Prioridade"
                            :items="cores"
                            v-model="config.pageFontColorPriority"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.pageFontColorPriority || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.pageFontColorPriority || '#000000')">
                                        {{(config.pageFontColorPriority || '#000000')}}
                                    </span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Histórico Lateral</h3>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Sidebar Fundo -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fundo Barra Lateral"
                            :items="cores"
                            v-model="config.sidebarBgColor"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.sidebarBgColor || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.sidebarBgColor || '#000000')">{{(config.sidebarBgColor || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Sidebar Fonte -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fonte Barra Lateral"
                            :items="cores"
                            v-model="config.sidebarFontColor"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.sidebarFontColor || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.sidebarFontColor || '#000000')">{{(config.sidebarFontColor || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Rodapé</h3>
                    </v-col>
                
                    <v-col cols="12" sm="6">
                        <!-- Footer Fundo -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fundo Rodapé"
                            :items="cores"
                            v-model="config.footerBgColor"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.footerBgColor || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.footerBgColor || '#000000')">{{(config.footerBgColor || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Footer Fonte -->
                        <v-autocomplete density="comfortable" 
                            clearable
                            label="Fonte Rodapé"
                            :items="cores"
                            v-model="config.footerFontColor"
                            item-value="hexa"
                            item-title="name"
                            no-data-text="Nenhum período carregado">
                            <template v-slot:append>
                                <v-chip :color="config.footerFontColor || '#ffffff'" variant="flat">
                                    <span :class="'text-'+$verify.calcula_luminescencia(config.footerFontColor || '#000000')">{{(config.footerFontColor || '#000000')}}</span>
                                </v-chip>
                            </template>

                            <template v-slot:selection="data">
                                <b>{{data.item.title}}</b>
                            </template>

                            <template v-slot:item="data">
                                <template v-if="!(typeof(data.item.raw) == 'object')">
                                    <v-list-item-title>-- {{data.item.raw}}</v-list-item-title>
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="{...data.props }" :key="data.item.value" :title="''">
                                        <v-list-item-title>
                                            <div v-html="data.item.raw.hexa"></div>
                                            <v-chip label :color="data.item.value">{{data.item.title}}</v-chip>
                                        </v-list-item-title>
                                    </v-list-item>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-text-field v-model="config.img" label="Caminho de logo">
                        </v-text-field>
                    </v-col>
                </v-row>
                <v-row class="nmp">
                    <v-col cols="12" sm="12">
                        <h3>Texto Rodapé</h3>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- Som -->
                        <v-textarea density="comfortable" 
                            clearable
                            label="Rodapé"
                            v-model="config.footerLabel">
                        </v-textarea>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <ws-jr :ws_channel="`channel_painel_atendimento_${unidade_selecionada}`"
            app="Painel de atendimento"
            @on-message="onMessageWebSocket"
            />
    </div>
</template>

<script>
import moment from 'moment';
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'PainelComponent',
    data:()=>({
        channel_painel_atendimento: 'channel',
        isBlinking: false,
        config:{},
        chamada:{},
        //atendente: {},
        alertsAvailable: [
            { name: 'Default', value: 'ekiga-vm.wav'},
            { name: 'Airport Bingbong', value: 'airport-bingbong.wav'},
            { name: 'Ding dong', value: 'ding-dong.wav'},
            { name: 'Doorbell Bingbong', value: 'doorbell-bingbong.wav'},
            { name: 'Info bleep', value: 'infobleep.wav'},
            { name: 'Quito Mariscal sucre', value: 'quito-mariscal-sucre.wav'},
            // { name: 'Toy doorbell', value: 'toydoorbell.wav'}
        ],
        unidades: [],
    }),
    methods: {
        ...mapActions(['GetUnidadesAtendimento']),
        async init(){
            //await this.atendenteLogado()
            this.load()
            await this.listar_unidades()
        },
        limparHistorico(){
            localStorage.removeItem('chamada')
            window.location.reload()
        },
        async listar_unidades(){
            const unidades = await this.GetUnidadesAtendimento()
            this.unidades = unidades
        },
        blinkText() {
            let blinkCount = 0;
            const maxBlinks = 3;
            this.notificarSom()
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
        notificarSom(){
            return new Promise((resolve, reject) => {
                var filename = this.config.alert || 'ekiga-vm.wav'

                const audio = new Audio()
                audio.src = `/audio/${filename}`
                audio.onended = resolve
                audio.onerror = reject
                audio.play()
            })
        },
        onMessageWebSocket(value){
            if(value?.event === 'CALL-TICKET'){
                this.chamada = value.obj
                this.chamada.em = moment().format('LTS');
                // console.log(this.chamada)
                this.blinkText()
            }
        },
        async load () {
            // console.log(JSON.parse(localStorage.getItem('chamada')))
            this.chamada = JSON.parse(localStorage.getItem('chamada')) || {}
            this.chamada.prioridade = this.chamada.prioridade || 'Normal';

            this.config = JSON.parse(localStorage.getItem('config')) || {}
            // defaults
            this.config.alert = this.config.alert || this.alertsAvailable[0].value

            this.config.footerLabel = this.config.footerLabel || 'Os melhores se formam aqui'
            this.config.img = this.config.img || ''
            this.config.unidade = this.config.unidade || 0
            this.config.pageBgColorNormal = this.config.pageBgColorNormal || '#B22222'
            this.config.pageFontColorNormal = this.config.pageFontColorNormal || '#F5F5F5'
            this.config.pageBgColorPriority = this.config.pageBgColorPriority || '#FFFF00'
            this.config.pageFontColorPriority = this.config.pageFontColorPriority || '#FF0000'
            this.config.sidebarBgColor = this.config.sidebarBgColor || '#8B0000'
            this.config.sidebarFontColor = this.config.sidebarFontColor || '#F5F5F5'
            this.config.footerBgColor = this.config.footerBgColor || '#8B0000'
            this.config.footerFontColor = this.config.footerFontColor || '#F5F5F5'
            this.config.clockBgColor = this.config.clockBgColor || '#BBBBBB'
            this.config.clockFontColor = this.config.clockFontColor || '#000000'

        },
        openConfig(){
            this.$refs.config_painel.dialog = true
        }
    },
    mounted(){
        this.init()
    },
    computed: {
        ...mapGetters(['StateAtendimentoLoading']),
        cores(){
            const hexadecimais = this.$verify.lista_cores_hex
            return hexadecimais
        },
        unidade_selecionada(){
            const uni = this.config.unidade
            return uni
        }
    },
    watch: {
        config: {
            handler(value){
                localStorage.setItem('config',JSON.stringify(value))
            }, deep: true
        },
        chamada: {
            handler(value){
                localStorage.setItem('chamada',JSON.stringify(value))
            }, deep: true
        },
        
    }
}
</script>
<style scoped>
.senha-painel{
    line-height: 1;
    font-size: 72px;
    font-family: Arial, Helvetica, sans-serif;
}
.historico-label{
    font-size: 20px;
    font-weight: bold;
}
.prioridade-label{
    font-size: 70px;
    font-weight: bold;
}
.senha-label{
    font-size: 150px;
    margin: 8vh 0;
    font-weight: bold;
}
.local-label{
    font-size: 40px;
    font-weight: bold;
}
.atendente-label{
    font-size: 40px;
    font-weight: bold;
}
.em-label{
    font-size: 20px;
}
.footer-label{
    font-size: 30px;
    font-weight: bold;
}
.item-historico-senha{
    font-size: 50px;
    font-weight: bold;
    line-height: 1;
}
.item-historico-local{
    font-size: 25px;
    font-weight: bold; 
}
.fab{
    position: fixed;
    top: 10px;
    left: 10px;
    filter: opacity(.05);
}
.fab-hovering{
    filter: opacity(1);
}
.nmp{
    margin: 0 !important;
    padding: 0 !important;
}
.blink {
  visibility: hidden;
}
</style>