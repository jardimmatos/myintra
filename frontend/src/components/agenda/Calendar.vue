<template>
    <v-row>
        <!-- <loading-jr :propObject="StateReservaLoading" /> -->
        <v-col cols="12" sm="6" md="5" lg="5">
            
            <!-- CALENDARIO -->
            <v-row>
                <!-- ADICIONAR RESERVA -->
                <v-col>
                    <modal-jr :code="modal_event_form"
                        :no-actions="true"
                        :ref="modal_event_form"
                        toolbar-title="Reserva"
                        >
                        <template v-slot:activate-slot>
                            <v-btn block color="success"
                                @click="onClickNewEvent">
                                <v-icon>mdi-plus</v-icon>
                                <span class="pl-2">Nova Reserva</span>
                            </v-btn>
                        </template>
                        <template v-slot:body>
                            <ReservaForm
                                :object="newEvent"
                                @on-create="onCreatedEvent"
                                @on-update="onUpdatedEvent"
                                />
                        </template>
                    </modal-jr>
                </v-col>
                <!-- ESPACOS -->
                <v-col v-if="hasEspacosPerm">
                    <v-btn block v-if="hasEspacosPerm" :to="{ name: 'agenda-espacos' }">Espaços</v-btn>
                </v-col>
                <!-- CALENDARIO -->
                <v-col cols="12" sm="12">
                    <VueCalendario :eventos="computedReservas" @log-events="onVueCalEvents">
                        <template #viewer-event="{viewer}">
                            <div class="vuecal__event-title text-left pa-2">
                                <v-icon
                                    :title="viewer.event.status_reserva" 
                                    :color="viewer.event.status_color_classname">
                                    mdi-circle
                                </v-icon>
                                &nbsp;
                                <span v-text="viewer.event.espaco_object.descricao" />
                                <div class="text-caption">
                                    {{(viewer.event.start||'').substring(0,5)}} -
                                    {{(viewer.event.end||'').substring(0,5)}}
                                </div>
                            </div>
                        </template>
                    </VueCalendario>
                </v-col>
            </v-row>

            <!-- Hide/Show ABERTOS/PENDENTES/CANCELADOS -->
            <v-row>
                <v-col cols="6"
                    v-for="hs, hs_index in hideShow()" :key="hs_index">
                    <v-card class="pa-2" v-show="hs.show" @click="hs.click()">
                        <v-row>
                            <v-icon size="x-small" :color="hs.color">{{hs.icon1}}</v-icon>
                            &nbsp; 
                            <small class="mx-1">{{hs.count}}</small>
                            &nbsp; 
                            <small v-text="hs.title" class="font-weight-medium"></small>
                            <v-spacer></v-spacer>
                            <v-icon size="small" :title="hs.label" v-show="!!hs.icon2">{{hs.icon2}}</v-icon>
                            <!-- <v-btn icon :tile="false" size="x-small" :color="hs.vmodel ? 'error': 'success'">
                            </v-btn> -->
                        </v-row>
                    </v-card>
                </v-col>
                <v-col cols="12" sm="12" md="12" clas="ma-1">
                    <v-card class="pa-2">
                        <v-row>
                            <v-icon color="primary">mdi-circle</v-icon>
                            &nbsp; 
                            <span v-text="'Relatórios'" class="font-weight-medium"></span>
                            <v-spacer></v-spacer>
                            
                            <RelatorioReservas/>
                        </v-row>
                    </v-card>

                </v-col>
            </v-row>
        </v-col>
        <v-col cols="12" sm="6" md="7" lg="7">
            <v-row>
                <!-- Filtro de Espaços -->
                <v-col cols="12">
                    <ReservaFiltro :reservas="computedReservas"
                        @filtered-espaco="filter_espacos = $event" />
                </v-col>
                
                <!-- Lista agrupada por espacos -->
                <v-col cols="12">
                    <v-list density="compact" nav>
                        <v-list-item @click="getEvents"
                            v-show="params.date_start"
                            title="Atualizar Reservas">
                            <template v-slot:prepend>
                                <v-icon v-show="!StateReservaLoading">mdi-refresh</v-icon>
                                <v-progress-circular indeterminate v-show="StateReservaLoading"/>
                            </template>

                        </v-list-item>
                        
                        <v-list-group class="lista-filtro-espacos"
                            :value="group_espaco_id"
                            :key="group_espaco_id"
                            v-for="group_espaco_id in Array.from(new Set(computedReservas.map(i => i.event.espaco_object.id)))">
                            <template v-slot:activator="{ props, isOpen }">
                                <v-list-item :style="isOpen ? 'background: rgb(var(--v-theme-primary)) !important;color: rgb(var(--v-theme-on-primary)) !important' : ''" v-bind="props" >{{computedReservas.filter(i => i.event.espaco_object.id === group_espaco_id)[0].event.espaco_object.descricao}}</v-list-item>
                            </template>

                            <v-list-item class="px-2"
                                lines="three"
                                :key="espaco_index"
                                @click="showEvent(r_espaco)"
                                v-for="r_espaco, espaco_index in computedReservas
                                            .filter(i => i.event.espaco_object.id === group_espaco_id)"
                                :subtitle="`${r_espaco.event.date_start_end}`"
                                :title="r_espaco.event.titulo">

                                <template v-slot:prepend>
                                    <helper-jr
                                        :icon-color="statusAndamentoColor(r_espaco.event.status_andamento)"
                                        icon="mdi-circle" position="left"
                                        :text="r_espaco.event.status_andamento"></helper-jr>
                                </template>
                                <template v-slot:subtitle="{ subtitle }">
                                    <div v-html="subtitle"></div>
                                </template>
                                <template v-slot:title="{ title }">
                                    <div v-html="title"></div>
                                </template>
                                <div class="text-caption">
                                    {{r_espaco.event.responsavel}}
                                    <helper-jr v-if="!!r_espaco.event.observacao"
                                        icon="mdi-text-box-plus-outline" position="top left"
                                        :text="r_espaco.event.observacao">
                                    </helper-jr>    
                                </div>
                            </v-list-item>
                        </v-list-group>
                    </v-list>
                    <loading-jr :propObject="StateSelectedReservaLoading" text="Carregando detalhes de reserva..." />
                    <modal-jr :code="modal_event_read"
                        :ref="modal_event_read"
                        :withCancelBtn="true"
                        dialogWidth="40%"
                        cancelBtnLabel="Fechar"
                        toolbar-title="Detalhes">
                        <template v-slot:activate-slot>
                            <span></span>
                        </template>
                        <template v-slot:body>
                            <ReservaDetalhe
                                :object="StateSelectedReserva"
                                @on-close="onCloseReservaDetalhe($event)"/>
                        </template>

                    </modal-jr>
                </v-col>
            </v-row>
        </v-col>
        
        <ws-jr v-if="StateAuthenticatedUser && StateAuthenticatedUser.id"
            :ws_channel="'channel_reservas'"
            app="Agenda Labs"
            @on-message="onMessageWebSocketAgendaLabs"
            @on-ready="onReadyWebSocketAgendaLabs"/>
    </v-row>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from 'vuex';
import VueCalendario from '@/components/layouts/partials/VueCalendario.vue';
import ReservaForm from './reserva/Form.vue';
import RelatorioReservas from './reserva/RelatorioReservas.vue';
import ReservaDetalhe from './reserva/Read.vue';
import ReservaFiltro from './reserva/Filtro.vue';

import FrontendService  from '../../services/frontendService';
const frontendService = new FrontendService();

export default {
    name: 'AgendaCalendar',
    components:{
        VueCalendario,
        ReservaForm, 
        ReservaDetalhe,
        ReservaFiltro,
        RelatorioReservas
    },
    data: () => ({
        view: null,
        calendar_start: null,
        calendar_end: null,
        params:{
            date_start: new Date().format('YYYY-MM-DD'),
            date_end: new Date().format('YYYY-MM-DD'),
        },
        model:{
            responsavel:null,
            titulo: null,
            espaco:null,
            finalidade:null,
            date: new Date().toLocaleDateString("en-CA"),
            start: '11:00',
            end: '12:00',
            participantes: 0,
            arquivos:[],
            observacao: null
        },
        newEvent:{},
        modal_event_form:'modal-event-form',
        modal_event_read :'modal-event-read',
        
        selectedElement: null,
        selectedOpen: false,
        ocultarAbertos: false,
        ocultarPendentes: false,
        ocultarCancelados: true,
        
        filter_espacos:[]
    }),
    mounted () {
        this.getEspacosPorContextosUsuario()
    },
    methods: {
        ...mapActions(['GetAgendaLabsReservas','GetReservaDetalhe','GetAgendaLabsEspacos']),
        ...mapMutations(['setAlerts']),
        getEspacosPorContextosUsuario(){
            this.GetAgendaLabsEspacos()
        },
        closeModalFormReserva(){
            this.$refs[this.modal_event_form].dialog = false
        },
        statusAndamentoColor(status){
            switch(status){
                case 'Finalizado': return 'grey';
                case 'Em andamento': return 'success';
                case 'Em breve': return 'info';
                default: return 'primary';
            }
        },
        onClickNewEvent(){
            this.newEvent = Object.assign({}, this.model)
        },        
        showEvent (event) {
            const open = async () => {
                await this.GetReservaDetalhe(event.event.id)
                this.selectedEvent = event.event
                this.$refs[this.modal_event_read].dialog = true
            }
            open()
        },
        async getEvents(){
            const params = this.params
            await this.GetAgendaLabsReservas(params)
        },
        onCreatedEvent(){
            this.closeModalFormReserva()
        },
        onUpdatedEvent(){
            //
        },
        onCloseReservaDetalhe(value){
            this.selectedOpen = !value //retorna true que foi fechado, mas recebe false para a variavel v-model
            this.$refs[this.modal_event_read].dialog = false;
        },
        get_status_reserva_color(value){
            return frontendService.status_reserva_color(value)
        },
        hideShow(){
            var items = [
                {
                    show: true,
                    title: 'Abertos',
                    color: this.get_status_reserva_color('OPENED'),
                    count: this.StateCalendarReservas.filter(obj => obj.event.status_reserva == 'OPENED').length,
                    label: 'Ocultar Abertos',
                    click: () => this.ocultarAbertos = !this.ocultarAbertos,
                    icon1: 'mdi-brightness-1',
                    icon2: this.ocultarAbertos ? 'mdi-eye-off-outline' : 'mdi-eye-outline',
                    vmodel: this.ocultarAbertos,
                    show_loading: false
                },
                {
                    show: true,
                    title: "Pendentes",
                    color: this.get_status_reserva_color('PENDING'),
                    count: this.StateCalendarReservas.filter(obj => obj.event.status_reserva == 'PENDING').length,
                    label: 'Ocultar Pendentes',
                    click: () => this.ocultarPendentes = !this.ocultarPendentes,
                    icon1: 'mdi-brightness-1',
                    icon2: this.ocultarPendentes ? 'mdi-eye-off-outline' : 'mdi-eye-outline',
                    vmodel: this.ocultarPendentes,
                    show_loading: false
                },
                {
                    show: true,
                    title: "Cancelados",
                    color: this.get_status_reserva_color('CANCELLED'),
                    count: this.StateCalendarReservas.filter(obj => obj.event.status_reserva == 'CANCELLED').length,
                    label: 'Ocultar Cancelados',
                    click: ()=> this.ocultarCancelados = !this.ocultarCancelados ,
                    icon1: 'mdi-brightness-1',
                    icon2: this.ocultarCancelados ? 'mdi-eye-off-outline' : 'mdi-eye-outline',
                    vmodel: this.ocultarCancelados,
                    show_loading: false
                },
                {
                    show: true,
                    title: "Reservas",
                    color: '',
                    count: this.StateCalendarReservas.length,
                    label: 'Atualizar',
                    click: ()=> this.getEvents() ,
                    icon1: 'mdi-calendar',
                    icon2: 'mdi-refresh',
                    vmodel: this.StateReservaLoading,
                    show_loading: this.StateReservaLoading
                },
            ]
            return items
        },
        onMessageWebSocketAgendaLabs(value){
            const evento = value["event"];
            const notificar = value["notify"];
            const message = value["message"];
            switch (evento) {
              case "RESERVA-CREATED":
                    if(notificar){
                        this.setAlerts([ {
                                tag:'info',
                                title:'Nova reserva',
                                message: message
                            }
                        ])
                    }
                    this.getEvents()
                    break;
              case "RESERVA-APPROVED":
                    if(notificar){
                        this.setAlerts([ {
                                tag:'info',
                                title:'Aprovação de Reserva',
                                message: message
                            }
                        ])
                    }
                    this.getEvents()
                    break;
              case "RESERVA-CANCELLED":
                    if(notificar){
                        this.setAlerts([ {
                                tag:'info',
                                title:'Cancelamento de Reserva',
                                message: message
                            }
                        ])
                    }
                    this.getEvents()
                    break;
                default:
                    console.info("No event" + evento)
            }
        },
        onReadyWebSocketAgendaLabs(){
        },
        async onVueCalEvents(e){
            /** evento de alteração de view */
            if(e.event === 'ready'){
                /** INICIALIZAR CALENDARIO */
                this.params.date_start = new Date().format('YYYY-MM-DD')
                this.params.date_end = new Date().format('YYYY-MM-DD')
                this.getEvents()
            }
            if(e.event === 'event-click'){
                /** Evento ao clicar em um event no calendário */
                this.showEvent(e.value)
            }
            if(e.event === 'view-change'){
                /** view for day */
                if(e.value.view === 'day'){
                    this.params.date_start = e.value.startDate.format('YYYY-MM-DD')
                    this.params.date_end = e.value.endDate.format('YYYY-MM-DD')
                    await this.getEvents()
                }
            }
        }
    },
    computed: {
        ...mapGetters(['StateCalendarReservas',
                        'StateSelectedReserva',
                        'StateSelectedReservaLoading',
                        'StateReservaLoading',
                        'StateAuthenticatedUser',
                        ]),
        computedReservas(){
            let filtereds = this.StateCalendarReservas
            // ocultar os de status cancelados
            if (this.ocultarCancelados){
                filtereds = filtereds.filter(obj => obj.event.status_reserva != 'CANCELLED')
            }
            // ocultar os de status pendentes
            if (this.ocultarPendentes){
                filtereds = filtereds.filter(obj => obj.event.status_reserva != 'PENDING')
            }
            // ocultar os de status abertos
            if (this.ocultarAbertos){
                filtereds = filtereds.filter(obj => obj.event.status_reserva != 'OPENED')
            }
            // filtrar somente os espacos no select
            if (this.filter_espacos.length > 0){
                filtereds = filtereds.filter(obj => this.filter_espacos.includes(obj.event.espaco_object.id))
            }
            const ordenarPorDescricao = (a, b) => {
                if (a.event.espaco_object.descricao < b.event.espaco_object.descricao) {
                    return -1;
                }
                if (a.event.espaco_object.descricao > b.event.espaco_object.descricao) {
                    return 1;
                }
                return 0;
            };

            // Ordenar pela descricao da sala
            filtereds.sort(ordenarPorDescricao)
            
            const ordenarPorHorarioInicial = (a, b) => {
                if (a.start < b.start) {
                    return -1;
                }
                if (a.start > b.start) {
                    return 1;
                }
                return 0;
            };
            ordenarPorHorarioInicial
            // Ordenar pelo horário Inicial
            filtereds.sort(ordenarPorHorarioInicial)
            return filtereds
        },
        hasEspacosPerm(){
            return this.$router.resolve({name: 'agenda-espacos'}).meta.has_perm()
        } 
    },
    unmounted(){
    }
  }
</script>
