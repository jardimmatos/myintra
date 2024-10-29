<template>
    <div v-if="object && object.id">
        <v-row>
            <v-spacer></v-spacer>
            <v-chip :color="get_actual_state_color(object.status_andamento)" :disabled="object.status_andamento === 'Finalizado'"
                title="Andamento" v-show="object.status_reserva != 'CANCELLED'">
                {{ object.status_andamento }}
            </v-chip>
            <v-chip title="Status"
                :color="get_status_reserva_color(object.status_reserva)">
                {{get_status_reserva_label(object.status_reserva)}}
            </v-chip>
            
            <v-menu v-if="object && object.id && menu(object).length"
                transition="slide-y-transition" location="bottom">
                <template v-slot:activator="{ props }">
                    <v-chip color="primary" title="Detalhes" v-bind="props" v-show="!StateSelectedReservaLoading">
                        Opções <v-icon>mdi-dots-vertical</v-icon>
                    </v-chip>
                </template>
                <v-list dense>
                    <span v-for="m, index in menu(object)" :key="index">
                        <v-list-item  @click="m.click()">
                            <v-list-item-title>{{m.label}}</v-list-item-title>
                        </v-list-item>
                    </span>
                </v-list>
            </v-menu>

        </v-row>
        <v-divider class="my-2"></v-divider>
        
        <v-skeleton-loader v-show="StateSelectedReservaLoading" type="article, article"></v-skeleton-loader>

        <ReadViewer :object="object" />
    </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
// import { bus } from '@/main'
import FrontendService  from '../../../services/frontendService'
import ReadViewer from './ReadViewer.vue'

const frontendService = new FrontendService()
export default {
    name: 'AgendaReservaRead',
    components: {
        ReadViewer
    },
    props:{
        object:{
            required: true
        }
    },
    date:()=>({
    }),
    methods:{
        ...mapActions(['RevogarReserva', 'AprovarReserva']),
        get_actual_state_color(value){
            return frontendService.actual_state_color(value)
        },
        get_status_reserva_label(value){
            return frontendService.status_reserva_label(value)
        },
        get_status_reserva_color(value){
            return frontendService.status_reserva_color(value)
        },
        async changeStatus(obj, to_status){
            if (to_status === 'CANCELLED'){
                let ressalva = prompt('Informe o motivo do cancelamento!')
                if (ressalva){
                    obj.status_descricao = ressalva
                    let revoked = await this.RevogarReserva(obj)
                    if (revoked){
                        // bus.$emit(`on-reserva-cancelled`, obj);
                        this.onClose()
                    }
                }
            }
            if (to_status === 'OPENED'){
                let approved = await this.AprovarReserva(obj)
                if (approved){
                    // bus.$emit(`on-reserva-approved`, obj);
                    this.onClose()
                }
            }
        },
        menu(object){
            if (object && object.created_by && object.created_by.username){
                var items = [
                    {
                        label: 'Cancelar reserva',
                        click: () => this.changeStatus(object, 'CANCELLED'),
                        if: ['OPENED', 'PENDING'].includes(object.status_reserva),
                        can: () => this.$verify.pode_cancelar_reservas((object.created_by.username||'').toLowerCase() === (this.StateUser || '').toLowerCase()) // default para $is_cit
                    },
                    {
                        label: 'Aprovar reserva',
                        click: ()=> this.changeStatus(object, 'OPENED'),
                        if: ['PENDING'].includes(object.status_reserva),
                        can: () => this.$verify.pode_aprovar_reservas()
                    },
                ]
                // Exibir somente itens de Menu com permissão e seu fluxo de status
                items = items.filter(o => o.can() && o.if)
                return items
            }else{
                return []
            }
        },
        onClose(){
            this.$emit('on-close', true)
        },
    },
    computed:{
        ...mapGetters(['StateSelectedReservaLoading', 'StateUser'])
    }
}
</script>