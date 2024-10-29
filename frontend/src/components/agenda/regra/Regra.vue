<template>
    <div>
        <modal-jr code="role-form" dialog-width="550px"
            toolbar-title="Gestão de restrições" @on-toggle="onToggle">
            <template v-slot:activate-slot>
                <slot name="modal-activate">
                    <v-btn dark>
                        <span><v-icon small>mdi-alert-octagon</v-icon> &nbsp; </span>Restrições
                    </v-btn>
                </slot>
            </template>
            <template v-slot:body>
                <v-row class="">
                    <v-col cols="12" sm="12">
                        <v-row>
                            <v-col cols="12">
                                <v-btn  class="mr-1"
                                    @click="onClickAdd" v-show="!current">Nova Regra</v-btn>
                                <v-btn  dark
                                    @click="clear" v-show="current">Voltar</v-btn>
                                <v-divider class="my-2"></v-divider>
                            </v-col>
                            <v-col cols="12">
                                <RegraForm
                                    :item="current" v-if="current"
                                    @on-update="onUpdate"
                                    @on-delete="onDelete"
                                    @on-create="onCreate" />
                                <RegraList
                                    @on-select-item="onSelectItem"
                                    v-show="!current"/>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>
    </div>
</template>
<script>
import RegraList from './RegraList'
import RegraForm from './RegraForm'
export default {
    name: 'AgendaRegra',
    components:{
      RegraList, RegraForm
    },
    data () {
      return {
            selected:{},
            form:{
                    week_day: null,
                    start_time: null,
                    end_time: null,
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
        onDelete(){
            this.clear()
        },
        onUpdate(){
            //this.clear()
        },
        onCreate(created){
            if(created)
                this.clear()
        },
        clear(){
            this.current = null
        },
        onToggle(value){
            if (!value){
                this.clear()
            }
        }
    }
}
</script>