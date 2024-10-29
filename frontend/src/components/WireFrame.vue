<template>
  <v-app :theme="themeClass">
    <!-- TOAST DE NOTIFICAÇÕES -->
    <toast-jr group="tc" position="bottom-right"/>
    
    <loading-jr :propObject="['login'].includes($store.state.auth.authLoading)" text="Acessando..." />

    <span>
      <slot name="navbar">
        <navbar-jr v-if="isAuthenticated" />
      </slot>

      <slot name="drawer">
          <drawer-jr v-if="isAuthenticated"/>
      </slot>

      <slot name="footer">
        <footer-jr/>
      </slot>

      <slot name="main">
        <v-main v-if="isAuthenticated">
            <v-container fluid>
              <v-row>
                <!-- Exibição dinâmica de titulos de páginas -->
                <h3>{{ titlePage }}</h3>
                <v-spacer></v-spacer>
                <h4>{{ subtitlePage }}</h4>
              </v-row>
              <v-divider class="my-2"></v-divider>

              <!-- DIV para permissão habilitada baseada nas permissões de rotas -->
              <div v-show="$route.meta.has_perm()">

                <div class="mb-2">
                  <slot name="top-main-legend">
                    <!-- Legenda que fica acima do top main -->
                    <div class="text-disabled text-caption">
                      selecione uma opção...
                    </div>
                  </slot>
                  <!-- Seção para incluir botões/menus globais -->
                  <slot name="top-main"></slot>
                </div>

                <div style="min-height: 68vh !important">
                  <!-- Seção de rotas -->
                  <router-view v-slot="{ Component }">
                    <transition name="fade">
                      <component :is="Component"/>
                    </transition>
                  </router-view>

                </div>

              </div>
              <!-- DIV para permissão desabilitada -->
              <div v-show="!$route.meta.has_perm()">
                <NoPermissionRoute />
              </div>
            </v-container>
        </v-main>
      </slot>

      <slot name="userws">
        <!-- Websocket do Usuário  -->
        <ws-jr v-if="StateAuthenticatedUser && StateAuthenticatedUser.id"
            :ws_channel="'channel_session_user_'+StateAuthenticatedUser.id"
            app="Usuário"
            :debug="false"
            @on-message="onMessageWebSocketSessionUser"
            @on-ready="onReadyWebSocketSessionUser"/>
      </slot>
      
      <slot name="notificationsws">
        <!-- ws de Notificações -->
        <ws-jr v-if="StateAuthenticatedUser && StateAuthenticatedUser.id"
            :ws_channel="'channel_notifications'"
            app="Notificações"
            :debug="false"
            @on-message="onMessageWebSocketNotificacoes"
            @on-ready="onReadyWebSocketNotificacoes"/>

      </slot>
    </span>
  </v-app>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
import FrontendService from '@/services/frontendService';
import ConfigService from '@/services/index';
import NoPermissionRoute from './layouts/partials/NoPermissionRoute.vue';

const fes = new FrontendService()
const svc = new ConfigService()

export default {
  name: 'LayoutWireFrame',
  components: { NoPermissionRoute },
  data: () => ({
    cards: ['Today', 'Yesterday'],
    drawer: null,
    newTask: true,
  }),
  methods:{
    ...mapActions(['GetNotificacao']),
    ...mapMutations(['setAlerts']),
      onReadyWebSocketSessionUser(){
        //
      },
      async onMessageWebSocketSessionUser(value){
          const evento = value["event"];
          if (evento == 'USER-REFRESH'){
              // atualizar localStorage do usuário
              await svc.verify_or_refreshing(true)
              location.reload()
          }
      },
      onReadyWebSocketNotificacoes(){
      },
      onMessageWebSocketNotificacoes(value){
          // const message = value['message'];
          const evento = value["event"];
          const notificar = value["notify"];
          const message = value["message"];
          switch (evento) {
            case "NOTIFICATION-CREATED":
                if(notificar){
                    this.setAlerts([ {
                        tag:'info',
                        title:'Nova notificação',
                        message: message
                        }
                    ])
                }
                this.GetNotificacao()
                break;
            case "NOTIFICATION-CHANGED":
                // APENAS ATUALIZAR
                if(notificar){
                    this.setAlerts([ {
                        tag:'info',
                            title:'Atualização de Notificação',
                            message: message //+ ' <a href="#/" >Visualizar</a>'
                        }
                    ])
                }
                this.GetNotificacao()
                break;
            case "NOTIFICATION-DELETED":
                if(notificar){
                    this.setAlerts([ {
                        tag:'info',
                            title:'Remoção de Notificação',
                            message: message //+ ' <a href="#/" >Visualizar</a>'
                        }
                    ])
                }
                this.GetNotificacao()
                break;
            default:
              console.info("No event" + evento)
        }
      }
  },
  computed:{
    ...mapGetters(['isAuthenticated', 'StateAuthenticatedUser']),
    computedMessageAlerts(){
      const alerts = this.$store.getters.StateAlerts
      return alerts
    },
    themeClass(){
      return this.$store.state.base.dark ? 'dark' : 'light'
    },
    titlePage(){
      let group_title = [
          this.$route.meta.groupName,
          this.$route.meta.title
        ].filter(i => ![null, undefined, ''].includes(i)).join(" - ")
      return group_title
    },
    subtitlePage(){
      let subtitle = this.$route.meta.subtitle
      return subtitle
    }
  },
  watch: {
    computedMessageAlerts:{
        handler(value){
            if (value == {0: undefined}) return
            try{
              for(let message of value){
                
                const options = {
                  severity: message.tag, // "error" | "success" | "secondary" | "info" | "contrast" | "warn"
                  summary: typeof(message.message) == 'string' ? message.message: message.message[0],
                  detail: message.title,
                  closable: (message.closable || true),
                  group: 'tc',
                  life: (message.timeout || 5000)
                }
                const fes_options = fes.getOptionsToastr(options)
                this.$toast.add(fes_options);
              }
            } catch(ex) {
              console.error('Falha ao lançar mensagem de alerta', value, ex)
            }
        },deep: true
      }
  },
  mounted(){
      /** Teste Toast */
      // this.$store.commit('setAlerts',[
      //       {
      //         tag: 'warn',
      //         title: 'teste',
      //         message:`Testando...`
      //       },
      //       {
      //         "tag": "error",
      //         "title": "Atenção",
      //         "message": [
      //           "Validação de Horários para o espaço Nome do Espaço Teste 2 (Sala de Aula). Conflito no horário: 11:00:00 - 12:00:00"
      //         ],
      //         "timeout": "70000"
      //       }
      // ])
  },
  
}
</script>
<style>
.fade-enter-active, .fade-leave-active {
  transition-property: opacity;
  transition-duration: 0.25s;
}
.fade-enter-active {
  transition-delay: 0.25s;
}
.fade-enter, .fade-leave-active {
  opacity: 0;
}
</style>