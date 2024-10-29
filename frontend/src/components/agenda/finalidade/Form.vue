<template>
    <div class="">
        <card-item :loading="StateLoadingRoomType">
            <template v-slot:title>
                <!-- NOME TIPO SALA -->
                <v-edit-dialog :return-value.sync="item.description" persistent large
                    save-text="Salvar" cancel-text="Cancelar" @save="saveOnChange({id:item.id, description:item.description})">
                    # {{ item.description }}
                    <template v-slot:input>
                        <v-text-field  hide-details class="mt-2" v-model="item.description" label="Tipo de sala" :rules="required" ></v-text-field>
                    </template>
                </v-edit-dialog>
                <v-spacer></v-spacer>
            </template>
            <template v-slot:text>
                <v-switch v-model="item.ignore_roles" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_roles:item.ignore_roles})"
                    label="Ignora restrições"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_holidays" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_holidays:item.ignore_holidays})"
                    label="Ignora feriados"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_saturdays" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_saturdays:item.ignore_saturdays})"
                    label="Ignora Sábados"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_sundays" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_sundays:item.ignore_sundays})"
                    label="Ignora Domingos"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_workdays" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_workdays:item.ignore_workdays})"
                    label="Ignora dias úteis"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_durations" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_durations:item.ignore_durations})"
                    label="Ignora limites de duração"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.ignore_time_conflicts" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, ignore_time_conflicts:item.ignore_time_conflicts})"
                    label="Ignora choques de horários"
                    inset dense
                    ></v-switch>
                <v-switch v-model="item.required_approve" hide-details
                    @update:modelValue="saveOnChange({ id:item.id, required_approve:item.required_approve})"
                    label="Evento para a sala requer aprovação"
                    inset dense
                    ></v-switch>
            </template>
            <template v-slot:actions>
                <!-- BOTAO APAGAR  -->
                <modal-jr :code="modal_code" v-if="!!item.id" :with-cancel-btn="true"
                    :toolbar-title="'Excluir '+item.description"
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
                                Tem certeza que você deseja apagar o tipo de sala <strong>{{item.description}}</strong>?
                            </v-col>
                        </v-row>
                    </template>
                    <template v-slot:actions>
                        <v-btn :loading="StateLoadingRoomType" small color="error" @click="deleteRoomType(item)">Remover</v-btn>
                    </template>
                </modal-jr>
                <v-spacer></v-spacer>
                <!-- CRIAR NOVO TIPO DE SALA -->
                <v-btn v-if="!item.id" small color="primary" @click="saveNewRoomType(item)" :loading="StateLoadingRoomType">Salvar</v-btn>
            </template>
        </card-item>
    </div>
</template>
<script>
import { bus } from './../../../main'
import { mapActions, mapGetters } from 'vuex'
import RoomTypeFormValidation from '../../../validations/forms/formRoomType'
const formValidation = new RoomTypeFormValidation()
export default {
    components:{
    },
    props:{
        item:{
            required:true,
            type: Object,
        },
    },
    data: () => ({
        loading:false,
        required:[ v => !!v||'Campo Obrigatório' ],
        modal_code: 'room-type-form-delete',
    }),
    methods:{
        ...mapActions(['ListRoomTypes']),
        ...mapActions(['UpdateRoomType','CreateRoomType', 'DeleteRoomType']),
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            let created = await this.CreateRoomType(item)
            this.$emit('on-create', created)
        },
        async update(item){
            let updated = await this.UpdateRoomType(item)
            this.$emit('on-update', updated)
        },
        async saveOnChange(item){
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewRoomType(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async deleteRoomType(item){
            // enviando "false" para data dialog, modal-jr irá fechar o dialog
            // utilizando um nova instancia do Vue (bus), eu posso fechar o dialog do componente modal-jr
            // 'close=-modal' nomeei para capturar no componente modal-jr
            let deleted = await this.DeleteRoomType(item)
            let keepOpenedDialog = !deleted
            bus.$emit(`close-modal-${this.modal_code}`, keepOpenedDialog);
            this.$emit('on-delete', deleted)
        }
    },
    computed:{
        ...mapGetters(['StateRoomTypes',]),
        ...mapGetters(['StateLoadingRoomType']),
        computedItem(){
            return this.item//this.details || this.item
        }
    },
};
</script>