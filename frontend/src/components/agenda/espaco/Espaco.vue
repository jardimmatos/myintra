<template>
    <div>
        <v-row>
            <v-col cols="12">
                <v-btn class="mr-1"
                    @click="onClickAdd"
                    v-show="!current">
                    <v-icon>mdi-plus</v-icon> &nbsp;
                    Novo Espaço
                </v-btn>
                <v-btn dark @click="clear"
                    v-show="current && current.descricao">Voltar</v-btn>

                <v-btn :to="{name: 'agendalabs'}">
                    <v-icon>mdi-calendar</v-icon> &nbsp;
                    Reservas
                </v-btn>
            </v-col>
            <v-col cols="12">
                <EspacoForm
                    :item="current" v-if="current"
                    @on-update-room="onUpdateRoom"
                    @on-delete-room="onDeleteRoom"
                    @on-create-room="onCreateRoom" />
                <EspacoList
                    @on-select-item="onSelectItem"
                    v-show="!current"/> 
            </v-col>
        </v-row>
    </div>
</template>
<script>
import { mapGetters } from 'vuex';
import EspacoList from './EspacoList'
import EspacoForm from './EspacoForm'

export default {
    name: 'AgendaEspaco',
    components:{
        EspacoList, 
        EspacoForm
    },
    data () {
      return {
          selected:{},
          form:{
                descricao:'Nome do Espaço',
                color:'#ccc',
                ativo:true,
                tipo_espaco:null,
                filiais:[],
                admins:[],
                gestores:[],
                regras:[],
                max_duracao: 60,
                min_duracao: 20,
                min_criacao: 24,
                permite_criar_sabados: false,
                permite_reservar_sabado: false,
                permite_criar_domingos: false,
                permite_reservar_domingo: false,
                instrucoes_espaco: null,
                requer_aprovacao: false,
                limitar_abertura: false,
                limitar_abertura_qtde:0
          },
          current:null
      }
    },
    methods:{
        onSelectItem(item){
            this.current = Object.assign({},item)
        },
        onClickAdd(){
            this.current = Object.assign({},this.form)
        },
        onDeleteRoom(deleted){
            if(deleted)
                this.clear()
        },
        onUpdateRoom(){
            //this.clear()
        },
        onCreateRoom(created){
            if(created)
                this.clear()
        },
        clear(){
            this.current = null
        },
    },
    mounted(){
    },
    computed:{
        ...mapGetters([])
    }
}
</script>