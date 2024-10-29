<template>

    <div>
        <modal-jr toolbar-title="Relatório de Reservas" dialog-width="90%" height="80%">
            <template v-slot:activate-slot>
                <v-btn icon :tile="false" size="x-small" color="primary">
                    <v-icon title="Acessar">mdi-chart-box</v-icon>
                </v-btn>
            </template>
            <template v-slot:body>
                <!-- FILTROS e BOTOES -->
                <v-row>
                    <!-- ESPACOS -->
                    <v-col cols="12" sm="12">
                        <v-autocomplete multiple chips
                            :error-messages="params.espaco_id.length > 3 ? 'A seleção de vários espaços pode ocasionar lentidão' : ''"
                            clearable
                            density="default"
                            :loading="$store.getters.StateEspacoLoading"
                            v-model="params.espaco_id"
                            label="Espaços"
                            item-title="descricao"
                            item-value="id"
                            :items="$store.getters.StateEspacos"
                            :no-data-text="$store.getters.StateEspacoLoading ? 'Carregando Espaços...' : 'Nenhum Espaço encontrado'"></v-autocomplete>
                    </v-col>
                    <!-- DATA INICIO -->
                    <v-col cols="12" sm="6" md="3">
                        <v-text-field hide-details v-model="params.date_start" type="date" label="Data Início"></v-text-field>
                    </v-col>
                    <!-- DATA FIM -->
                    <v-col cols="12" sm="6" md="3">
                        <v-text-field hide-details v-model="params.date_end" type="date" label="Data"></v-text-field>
                    </v-col>
                    <!-- GROUP BY -->
                    <v-col cols="12" sm="6" md="6" v-if="false">
                        <v-select 
                            clearable
                            multiple chips
                            label="Agrupar por"
                            :items="[
                                { value: { key: 'espaco_object.descricao', order: 'asc' }, title: 'Espaço' },
                                { value: { key: 'finalidade_object.descricao', order: 'asc' }, title: 'Finalidade' },
                                { value: { key: 'status_reserva', order: 'asc' }, title: 'Status' },
                                { value: { key: 'responsavel', order: 'asc' }, title: 'Responsável' },
                            ]"
                            v-model="group_by"
                            hide-details
                        >
                        </v-select>
                    </v-col>
                    <v-col cols="12" sm="6" md="6">
                        <v-select 
                            clearable
                            multiple chips
                            label="Status de Reserva"
                            :items="[
                                { value: 'OPENED', title: 'Aberto/Concluído' },
                                { value: 'PENDING', title: 'Pendente' },
                                { value: 'CANCELLED', title: 'Cancelado' },
                            ]"
                            v-model="params.status_reserva"
                            hide-details
                        >
                        </v-select>
                    </v-col>
                    <!-- BOTOES -->
                    <v-col cols="12" sm="12">
                        <v-btn @click="getReport" class="my-1"
                            :disabled="!params.espaco_id.length || !params.date_start || !params.date_end || loading"
                        >Pesquisar</v-btn>
                        <v-btn
                            @click.prevent="export_xls()"
                            color="success darken-2" small
                            :disabled="reservas.length == 0 || loading">
                            <v-icon small>mdi-file-excel</v-icon>
                            Excel
                        </v-btn>
                        <v-btn @click.prevent="export_pdf()"
                            color="error darken-2" small
                            :disabled="reservas.length == 0 || loading">
                            <v-icon small>mdi-file-pdf-box</v-icon>
                            PDF
                        </v-btn>
                    </v-col>
                </v-row>

                <!-- TABELA -->
                <v-row>
                    <v-col cols="12">
                        <v-data-table
                            :loading="loading"
                            :items-per-page="1000"
                            :items="reservas"
                            :group-by="group_by"
                            :sort-by="[
                                { key: 'date', order: 'asc' },
                            ]"
                            :headers="[
                                    { title: 'Data', align: 'center', sortable: false, value: 'date', width:'135px'},
                                    { title: 'Título', align: 'start', sortable: false, value: 'titulo', width:'auto' },
                                    { title: 'Espaço', align: 'start', sortable: false, value: 'espaco_object.descricao', width:'auto' },
                                    { title: 'Responsável', align: 'start', sortable: false, value: 'responsavel', width:'10px' },
                                    { title: 'Finalid.', align: 'end', sortable: false, value: 'finalidade_object.descricao', width:'10px' },
                                    { title: ' ', align: 'start', sortable: false, value: 'opcoes', width:'120px' },
                                ]"
                        >
                            <template v-slot:group-header="{ item, columns, toggleGroup, isGroupOpen }">
                                <tr>
                                    <td :colspan="columns.length">
                                        <v-btn
                                            :icon="isGroupOpen(item) ? '$expand' : '$next'"
                                            variant="text"
                                            @click="toggleGroup(item)"
                                        >
                                        </v-btn>
                                        {{item.value}} - ({{item.items.length}})
                                    </td>
                                </tr>
                            </template>
                            <!-- eslint-disable-next-line -->
                            <template #item.date="{ item }">
                                <div class="text-subtitle-2">
                                    {{item.date_start_end.substring(0,10)}}
                                    <br>
                                    {{item.start.substring(0,5)}} - {{item.end.substring(0,5)}}
                                </div>
                            </template>
                            <!-- eslint-disable-next-line -->
                            <template #item.responsavel="{ item }">
                                <div :title="item.responsavel">
                                    {{$verify.truncate(item.responsavel, 12)}}
                                </div>
                            </template>
                            <!-- eslint-disable-next-line -->
                            <template #bottom>
                                <span></span>
                            </template>
                            <!-- eslint-disable-next-line -->
                            <template #item.opcoes="{ item }">
                                <td>
                                    <v-row no-gutters>
                                        <v-col>
                                            <helper-jr
                                                :icon-color="statusAndamentoColor(item.status_andamento)"
                                                icon="mdi-circle" position="bottom"
                                                :text="item.status_andamento"></helper-jr>
                                            <!-- {{item.status_andamento}} -->
                                        </v-col>
                                        <v-col>
                                            <helper-jr
                                                :icon-color="get_status_reserva_color(item.status_reserva)"
                                                icon="mdi-circle" position="bottom"
                                                :text="get_status_reserva_label(item.status_reserva)"></helper-jr>
                                            <!-- {{get_status_reserva_label(item.status_reserva)}} -->
                                        </v-col>
                                        <v-col>
                                            <helper-jr
                                                v-if="item.observacao"
                                                icon="mdi-chat" position="bottom"
                                                :text="item.observacao"></helper-jr>
                                        </v-col>
                                    </v-row>
                                </td>
                            </template>
                            
                        </v-data-table>
                    </v-col>
                </v-row>
                
                <v-row>
                    <!-- IMPRESSAO PDF -->
                    <div id="imprimir-pdf" v-show="false">
                        <div v-for="reserv, i in reservas" :key="i" class="item-tabela">
                            <table>
                                <thead>
                                    <tr style="background: #eee">
                                        <th colspan="7" style="text-align:left">
                                            <div style="padding: 3px 0">
                                                <b style="font-size:14px">{{reserv.titulo}}</b>
                                            </div>
                                        </th>
                                    </tr>
                                    <tr style="background: #eee">
                                        <th style="text-align:left">Data/Hora</th>
                                        <th style="text-align:left">Espaço</th>
                                        <th style="text-align:left">Finalidade</th>
                                        <th style="text-align:left">Responsável</th>
                                        <th style="text-align:left">Status</th>
                                        <th style="text-align:left">Cancelamento</th>
                                        <th style="text-align:left">Obs</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr style="padding: 5px ">
                                        <td style="vertical-align: top; width: 12%; font-size: 12px;">
                                            <div style="align-text:center">
                                                {{reserv.date_start_end.substring(0,10)}}
                                            </div>
                                            <div style="align-text:center">
                                                {{reserv.start.substring(0,5)}} - {{reserv.end.substring(0,5)}}
                                            </div>
                                        </td>
                                        <td style="vertical-align: top; width: 12%; font-size: 12px;">
                                            {{reserv.espaco_object.descricao}}
                                        </td>
                                        <td style="vertical-align: top; width: 10%; font-size: 12px;">
                                            {{reserv.finalidade_object.descricao}}
                                        </td>
                                        <td style="vertical-align: top; width: 18%; font-size: 12px;">
                                            {{reserv.responsavel}}
                                        </td>
                                        <td style="vertical-align: top; width: 14%; font-size: 12px; font-weight: bold;">
                                            {{get_status_reserva_label(reserv.status_reserva)}}
                                        </td>
                                        <td style="vertical-align: top; width: 17%; font-size: 12px;">
                                            {{reserv.status_descricao || '-'}}
                                        </td>
                                        <td style="vertical-align: top; max-width: 17%;">
                                            {{reserv.observacao || '-'}}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-if="estatisticas.length > 0">
                            <h6 style="margin-bottom:2px; padding-bottom:2px">Qtde de Reservas por Espaço</h6>
                            <div v-for="stts, i in estatisticas" :key="i">
                                <div>{{stts.descricao}}: {{stts.qtde}}</div>
                            </div>
                        </div>
                    </div>
                    <!-- IMPRESSAO EXCEL -->
                    <div id="imprimir-excel" v-show="false">
                        <div>
                            <table>
                                <thead>
                                    <tr style="background: #eee">
                                        <th style="text-align:left">Responsável</th>
                                        <th style="text-align:left">Data</th>
                                        <th style="text-align:left">Horário</th>
                                        <th style="text-align:left">Espaço</th>
                                        <th style="text-align:left">Finalidade</th>
                                        <th style="text-align:left">Status</th>
                                        <th style="text-align:left">Título</th>
                                        <th style="text-align:left">Cancelamento</th>
                                        <th style="text-align:left">Obs</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="reserv, i in reservas" :key="i">
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.responsavel}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.date}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.start.substring(0,5)}} - {{reserv.end.substring(0,5)}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.espaco_object.descricao}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.finalidade_object.descricao}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px; font-weight: bold;">
                                            {{get_status_reserva_label(reserv.status_reserva)}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.titulo || '-'}}
                                        </td>
                                        <td style="vertical-align: top; font-size: 12px;">
                                            {{reserv.status_descricao || '-'}}
                                        </td>
                                        <td style="vertical-align: top;">
                                            {{reserv.observacao || '-'}}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </v-row>
            </template>
        </modal-jr>
    </div>
</template>
    
<script>
import { useDate } from 'vuetify';
import { mapGetters } from 'vuex';
import FrontendService  from '@/services/frontendService';
const frontendService = new FrontendService();
export default {
    data: () => ({
        params:{
            date_start: null,
            date_end: null,
            espaco_id: [],
            status_reserva: ['OPENED'],
            page_size: 1000
        },
        loading: false,
        reservas:[],
        group_by: []
    }),
    mounted(){
        const adapter = useDate()
        this.params.date_start = adapter.startOfDay(adapter.startOfMonth(new Date())).format('YYYY-MM-DD')
        this.params.date_end = adapter.endOfDay(adapter.endOfMonth(new Date())).format('YYYY-MM-DD')
    },
    methods: {
        async getReport(){
            this.loading = true
            try{
                const results = await this.$store.dispatch('GetReportAgendaLabsReservas', this.params)
                this.reservas = results
            }catch (err){
                console.log(err)
            }
            this.loading = false
        },
        statusAndamentoColor(status){
            switch(status){
                case 'Finalizado': return 'grey';
                case 'Em andamento': return 'success';
                case 'Em breve': return 'info';
                default: return 'primary';
            }
        },
        get_status_reserva_color(value){
            return frontendService.status_reserva_color(value)
        },
        get_status_reserva_label(value){
            return frontendService.status_reserva_label(value)
        },
        export_xls(){
            // var data_type = 'data:application/vnd.ms-excel';
            var table_div = document.getElementById('imprimir-excel')
            table_div = table_div.children[0].children[0]
            var blobData = new Blob(['\ufeff'+table_div.outerHTML], { type: 'application/vnd.ms-excel' });
            var url = window.URL.createObjectURL(blobData);
            var a = document.createElement('a');
            a.href = url;
            let emitido_em = new Date().toLocaleDateString()
            a.download = emitido_em + '_export_agendalabs.xls';
            a.click();
        },
        sendPrint(html){
            const win = window.open('', '_blank');
            win.document.write(html);
            win.focus();
        },
        export_pdf(){
            var page = ''
            var body = ''
            var title_div = document.createElement('h3')
            title_div.innerHTML = 'Reservas de Espaço - Agendamentos'
            title_div.style.width = '840px'
            title_div.style.marginTop = '20px'
            title_div.style.paddingBottom = '20px'
            title_div.style.textAlign = 'center'
            body = document.getElementById('imprimir-pdf')
            body = body.innerHTML
            let emitido_em = new Date().toLocaleDateString()
            page += `
                <html>
                    <head>
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&family=Poppins:wght@300&display=swap" rel="stylesheet">
                        <style>
                            @media print {
                                table{
                                    width: 100%;
                                    margin-bottom: 10px;
                                    page-break-inside: avoid;
                                }
                                .pagebreak {
                                    page-break-after: always;
                                }
                                *{
                                    font-family: 'Poppins', sans-serif;
                                    font-size: 11px;
                                }
                                h3{
                                    font-family: 'Poppins', sans-serif;
                                    font-size: 16px;
                                }
                                td, th {
                                    /*border-bottom-style: solid;
                                    border-bottom-width: 1px;
                                    border-color: #aaa;*/
                                }
                                .item-tabela {
                                    border-bottom-style: solid;
                                    border-bottom-width: 1px;
                                    border-color: #aaa;
                                    margin-bottom: 10px;
                                }
                            }
                        </style>
                    </head>
                    <body>
                        <div style="display: inline-flex;margin-bottom:50px;width:100%">
                            <img src="favicon.png" width="80px" style="object-fit: contain;" />
                            <div style="width:100%; text-align:center">
                                <h3>Agendamentos - MyIntranet</h3>
                            </div>
                            <div style="width:200px; text-align:right">
                                <div>
                                    <small> Emitido em: ${emitido_em}</small>
                                </div>
                                <div>
                                    <small> por: ${this.StateAuthenticatedUser.username}</small>
                                </div>
                            </div>
                        </div>
                        ${body}
                    </body>
                </html>
            `;
            this.sendPrint(page)
        },
    },
    computed: {
        ...mapGetters(['StateAuthenticatedUser']),
        estatisticas(){
            try{
                const reservas = Object.assign([],this.reservas)
                const espacos_id = Array.from(new Set(reservas.map(m => m.espaco_object.id ) ))
                const espacos_obj = Array.from(new Set(reservas.map(m => ({ id: m.espaco_object.id, descricao: m.espaco_object.descricao}) ) ))
                var espacos = espacos_id.map(m => ({id: m, descricao: espacos_obj.filter(f => f.id == m)[0].descricao}))
                espacos = espacos.map(m => ({...m, qtde: reservas.filter(r => r.espaco_object.id == m.id).length}))
                const sort_by_ordem = (a,b) => b.qtde-a.qtde
                let q = (espacos||[]).sort(sort_by_ordem)
                return q
            }catch{
                return []
            }
        }
    }
    
}
</script>
<style scoped>
.custom-header-style .v-data-table__td {
    font-size: 10px;
}
</style>