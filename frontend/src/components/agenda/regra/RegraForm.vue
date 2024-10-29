<template>
    <div class="">
        <card-item :loading="StateRegraLoading">
            <template v-slot:title>
                <!-- dia da semana -->
                <v-select  hide-details class="mt-2"
                    label="Dia da semana"
                    :items="StateRegraEnums.weekday_enums"
                    v-model="item.week_day"
                    item-value="weekday_index"
                    item-title="weekday_name"
                    @update:modelValue="saveOnChange({id:item.id, week_day:item.week_day})"
                    >
                </v-select>
            </template>
            <template v-slot:text>
                <v-text-field
                    v-model="item.start_time"
                    label="Início"
                    type="time"
                    >
                </v-text-field>
                <v-text-field
                    v-model="item.end_time"
                    label="Fim"
                    type="time"
                    >
                </v-text-field>
            </template>
            <template v-slot:actions>
                <!-- BOTAO APAGAR  -->
                <modal-jr :code="modal_code" v-if="!!item.id" :with-cancel-btn="true"
                    :toolbar-title="'Excluir '+ getDayOfWeek(item.week_day)"
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
                                Tem certeza que você deseja apagar a restrição <strong>{{getDayOfWeek(item.week_day)}} de {{item.start_time}} às {{item.end_time}}</strong>?
                            </v-col>
                        </v-row>
                    </template>
                    <template v-slot:actions>
                        <v-btn :loading="StateRegraLoading" small color="error" @click="deleteRegra(item)">Remover</v-btn>
                    </template>
                </modal-jr>
                <v-spacer></v-spacer>
                <!-- CRIAR NOVO TIPO DE SALA -->
                <v-btn v-if="!item.id" small color="primary" @click="saveNewRegra(item)" :loading="StateRegraLoading">Salvar</v-btn>
            </template>
        </card-item>
    </div>
</template>
<script>
// import { bus } from './../../../main'
import { mapActions, mapGetters } from 'vuex'
import RegraFormValidation from '../../../validations/forms/formRole'
const formValidation = new RegraFormValidation()
export default {
    name: 'AgendaRegraForm',
    components:{
    },
    props:{
        propObject:{
            required:true,
            },
    },
    data: () => ({
        loading:false,
        required:[ v => !!v||'Campo Obrigatório' ],
        modal_code: 'role-form-delete',
        stime_picker:false,
        etime_picker:false,
        item: {}
    }),
    methods:{
        ...mapActions(['UpdateRegra','CreateRegra', 'DeleteRegra']),
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            let created = await this.CreateRegra(item)
            this.$emit('on-create', created)
        },
        async update(item){
            let updated = await this.UpdateRegra(item)
            this.$emit('on-update', updated)
        },
        async saveOnChange(item){
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewRegra(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async deleteRegra(item){
            // enviando "false" para data dialog, modal-jr irá fechar o dialog
            // utilizando um nova instancia do Vue (bus), eu posso fechar o dialog do componente modal-jr
            // 'close=-modal' nomeei para capturar no componente modal-jr
            let deleted = await this.DeleteRegra(item)
            // let keepOpenedDialog = !deleted
            // bus.$emit(`close-modal-${this.modal_code}`, keepOpenedDialog);
            this.$emit('on-delete', deleted)
        },
        getDayOfWeek(index){
            // Recuperar o nome do dia da semana com base no enum via api
            let enums = this.StateRegraEnums
            if(enums && enums.weekday_enums && enums.weekday_enums.length > 0){
                return enums.weekday_enums[index].weekday_name
            }
            return '-'
        },
        onSetStartTime(value){
            this.stime_picker = false
            this.saveOnChange({id:value.id, start_time:value.start_time})
        },
        onSetEndTime(value){
            this.etime_picker = false
            this.saveOnChange({id:value.id, end_time:value.end_time})
        }
    },
    computed:{
        ...mapGetters(['StateRegraLoading','StateRegraEnums']),
        computedItem(){
            return this.item//this.details || this.item
        }
    },
    watch: {
        propObject:{
            handler(value){
                const prop = value
                this.item = prop
            }, deep: true
        }
    }
};
</script>