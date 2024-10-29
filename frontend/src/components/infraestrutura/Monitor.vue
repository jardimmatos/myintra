<template>
    <div>
      <v-row>

        <helper-jr text="Serviços que estão fora do ar ou apresentando algum nível de lentidão. <br>Os serviços fora do ar aparecerão no topo, acima dos indicadores em verde, destacados de vermelho."/>
        <span class="ml-2 text-grey" style="font-size:9px">{{ws_temp_messages}}</span>

        <v-spacer></v-spacer>

        <v-btn-small icon title="Atualizar" @click.prevent="GetMonitors" :loading="StateMonitorsLoading">
          <v-icon>mdi-refresh</v-icon>
        </v-btn-small>

      </v-row>

      <div>
        <!-- SERVICOS INSTAVEIS -->
        <v-row class="instaveis">
          <v-col v-for="monitor in StateMonitors.filter(o=> o.online == false)"
            :key="monitor.id" cols="12" sm="6" md="6">
            <v-alert tile :type="mapColorStatus(monitor.online)">
              <v-row>
                <v-col cols="12" sm="12" >
                  <div><span v-text="monitor.servico"></span> {{monitor.referencia}}</div>
                  <div><span class="text-caption" v-text="monitor.url"></span></div>
                </v-col>
                <v-col cols="12" sm="12" md="7" align="left">
                  <v-chip class="mx-1 pa-2" :title="monitor.mensagem" :color="mapColorStatus(monitor.online)">
                  </v-chip>
                  <v-chip variant="outlined" class="mx-1 pa-2" title="Acessar" :href="monitor.url" target="_blank">
                    <v-icon>{{mapIconStatus(monitor.online)}}</v-icon>
                    Acessar
                  </v-chip>
                </v-col>
              </v-row>
              <div>
              </div>
            </v-alert>
          </v-col>
        </v-row>

        <!-- SERVICOS NORMAIS -->
        <v-row class="normais">
          <v-col v-for="monitor in StateMonitors.filter(o=> o.online == true)" :key="monitor.id"
            cols="12" sm="3" lg="2">
            <v-alert tile text elevation="8" color="success" class="my-1 ">
              <div class="text-center" :title="monitor.servico">
                <v-icon>mdi-information</v-icon>
                {{monitor.servico}}
              </div>
              <v-row>
                <v-col cols="12" sm="12" align="center" class="py-3">
                  <v-chip variant="outlined" :title="monitor.referencia" :href="monitor.url">
                    Acessar
                  </v-chip>
                </v-col>
              </v-row>
            </v-alert>
          </v-col>
        </v-row>
      </div>
      <ws-jr
        :ws_channel="'channel_monitor_'+StateAuthenticatedUser.id"
        app="monitor"
        @on-message="onMessageWebSocket"
        @on-ready="onReadyWebSocket"/>
    </div>
</template>
<script>
import {mapActions,mapGetters} from 'vuex';
export default {
    name: 'MonitorComponent',
    data: () => ({
      interval:null,
      ws_temp_messages:''
    }),
    methods:{
        ...mapActions(['GetMonitors']),
        mapColorStatus(status){
          switch(status){
            case true: return 'success';
            case false: return 'error';
            case null: return 'secondary';
            default: ''
          }
        },
        mapIconStatus(status){
          switch(status){
            case true: return 'mdi-check-bold';
            case false: return 'mdi-close';
            case null: return 'mdi-help-circle-outline';
            default: ''
          }
        },
        onReadyWebSocket(){
          this.GetMonitors()
        },
        onMessageWebSocket(value){
          const message = value['message'];
          const evento = value["event"];
          if(['MONITOR-LOADING'].includes(evento)){
            this.ws_temp_messages = message
          }
          if (evento == 'MONITOR-LOADED'){
            this.ws_temp_messages = message
            setTimeout(()=>{
              this.ws_temp_messages = null
            },5000)
          }
        }
    },
    computed:{
      ...mapGetters(['StateAuthenticatedUser','StateDark', 'StateMonitors','StateMonitorsLoading']),
    },
    mounted(){
      // O carregamento inicial será disparado quando a conexão websocket estiver pronta (no metodo onReadyWebSocket())
      // por isso this.GetMonitors() foi removido do mounted
      // manter recarregando periodicamente
      this.interval = setInterval(this.GetMonitors, 90000)
    },
    unmounted(){
      // Limpar para, ao sair do componente não ficar recarregando os serviços
      clearInterval(this.interval)
    }
  }
</script>