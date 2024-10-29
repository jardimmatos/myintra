<template>
    <div>
        <modal-jr code="room-type-form" dialog-width="550px"
            toolbar-title="Gestão de Tipos de Espaço" @on-toggle="onToggle">
            <template v-slot:activate-slot>
                <slot name="modal-activate">
                    <v-btn >
                        <span><v-icon small>mdi-door</v-icon> &nbsp; </span>Tipos de Espaço
                    </v-btn>
                </slot>
            </template>
            <template v-slot:body>
                <v-row class="">
                    <v-col cols="12" sm="12">
                        <v-row>
                            <v-col cols="12">
                                <v-btn  class="mr-1" @click="onClickAdd" v-show="!current">Adicionar</v-btn>
                                <v-btn  dark @click="clear" v-show="current && current.descricao">Voltar</v-btn>
                                <v-divider class="my-2"></v-divider>
                            </v-col>
                            <v-col cols="12">
                                <Form
                                    :item="current" v-if="current"
                                    @on-update="onUpdate"
                                    @on-delete="onDelete"
                                    @on-create="onCreate" />
                                <List
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
import List from './List'
import Form from './Form'
export default {
    components:{
      List, Form
    },
    data () {
        return {
            selected:{},
            form:{
                descricao:'Novo Tipo...'
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