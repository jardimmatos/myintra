<template>
    <div class="">
        <card-item :loading="StateTipoEspacoLoading">
            <template v-slot:title>
                <v-spacer></v-spacer>
            </template>
            <template v-slot:text>
                <!-- NOME TIPO ESPACO -->
                <!-- eslint-disable-next-line -->
                <v-text-field hide-details class="mt-2" v-model="item.descricao" label="Tipo de espaço" :rules="required" ></v-text-field>
            </template>
            <template v-slot:actions>
                <!-- BOTAO APAGAR  -->
                <modal-jr :code="modal_code" v-if="!!item.id" :with-cancel-btn="true"
                    :toolbar-title="'Excluir '+item.descricao"
                    btn-label="Apagar"
                    btn-color="error"
                    toolbar-color="error"
                    btn-icon="mdi-delete">
                    <template v-slot:activate-slot>
                        <v-btn color="error" small dark >
                            <span><v-icon small>mdi-delete</v-icon> &nbsp; </span>Remover
                        </v-btn>
                    </template>
                    <template v-slot:body>
                        <v-row class="">
                            <v-col cols="12" sm="12">
                                Tem certeza que você deseja apagar o tipo de espaço <strong>{{item.descricao}}</strong>?
                            </v-col>
                        </v-row>
                    </template>
                    <template v-slot:actions>
                        <v-btn-small :loading="StateTipoEspacoLoading" color="error" @click="deleteTipoEspaco(item)">Remover</v-btn-small>
                    </template>
                </modal-jr>
                <v-spacer></v-spacer>
                <!-- CRIAR NOVO TIPO DE ESPACO -->
                <v-btn-small v-if="!item.id" color="primary" @click="saveNewTipoEspaco(item)" :loading="StateTipoEspacoLoading"><v-icon>mdi-content-save</v-icon>Salvar</v-btn-small>
                <v-btn-small v-else color="primary" @click="saveOnChange({id:item.id, descricao:item.descricao})" :loading="StateTipoEspacoLoading"><v-icon>mdi-content-save</v-icon>Salvar</v-btn-small>
            </template>
        </card-item>
    </div>
</template>
<script>
// import { bus } from './../../../main'
import { mapActions, mapGetters } from 'vuex'
import TipoEspacoFormValidation from '../../../validations/forms/formTipoEspaco'
const formValidation = new TipoEspacoFormValidation()
export default {
    name: 'AgendaTipoEspacoForm',
    props:{
        item: {
            required:true,
        },
    },
    data: () => ({
        loading:false,
        required:[ v => !!v||'Campo Obrigatório' ],
        modal_code: 'room-type-form-delete',
    }),
    methods:{
        ...mapActions(['UpdateTipoEspaco','CreateTipoEspaco', 'DeleteTipoEspaco']),
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            let created = await this.CreateTipoEspaco(item)
            this.$emit('on-create', created)
        },
        async update(item){
            let updated = await this.UpdateTipoEspaco(item)
            this.$emit('on-update', updated)
        },
        async saveOnChange(item){
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewTipoEspaco(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async deleteTipoEspaco(item){
            // enviando "false" para data dialog, modal-jr irá fechar o dialog
            // utilizando um nova instancia do Vue (bus), eu posso fechar o dialog do componente modal-jr
            // 'close=-modal' nomeei para capturar no componente modal-jr
            let deleted = await this.DeleteTipoEspaco(item)
            // let keepOpenedDialog = !deleted
            // bus.$emit(`close-modal-${this.modal_code}`, keepOpenedDialog);
            this.$emit('on-delete', deleted)
        }
    },
    computed:{
        // ...mapGetters(['StateTipoEspaco',]),
        ...mapGetters(['StateTipoEspacoLoading']),
        computedItem(){
            return this.item//this.details || this.item
        }
    },
    // watch: {
    //     propObject:{
    //         handler(value){
    //             const prop = value
    //             this.item = prop
    //         }, deep: true
    //     }
    // }
};
</script>