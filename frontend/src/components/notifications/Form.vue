<template>
    <div>
        <modal-jr :code="modal_code"
            dialog-width="60%"
            height="600"
            toolbar-title="Notificação"
            @on-toggle="onToggle" :ref="modal_code">
            <template v-slot:activate-slot>
                <slot name="modal-activate">
                    <span></span>
                </slot>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="12">
                        <!-- eslint-disable-next-line -->
                        <v-text-field v-model="current.titulo"
                            label="Título da notificação"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- eslint-disable-next-line -->
                        <v-text-field v-model="current.inicio"
                            type="datetime-local"
                            label="Início"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <!-- eslint-disable-next-line -->
                        <v-text-field v-model="current.fim"
                            type="datetime-local"
                            label="Fim"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <quill-editor v-model:content="current.mensagem"
                            content-type="html"
                            toolbar="full">
                        </quill-editor>
                    </v-col>
                </v-row>
                <v-row>
                </v-row>
            </template>

            <template #actions>
                <modal-jr
                    v-if="!!current.id" :with-cancel-btn="true"
                    :code="modal_code"
                    :toolbar-title="'Excluir '+current.titulo"
                    btn-label="Apagar"
                    toolbar-color="error"
                    btn-icon="mdi-delete">
                    <template v-slot:activate-slot>
                        <v-btn-small color="error" v-if="$verify.has_perm('delete_notificacao')">
                            <v-icon>mdi-delete</v-icon> &nbsp;Remover
                        </v-btn-small>
                    </template>
                    <template v-slot:body>
                        <v-row>
                            <v-col cols="12" sm="12">
                                Tem certeza que você deseja apagar a notificação <strong>{{current.titulo}}</strong>?
                            </v-col>
                        </v-row>
                    </template>
                    <template v-slot:actions>
                        <span>
                            <v-btn-small color="error"
                                :disabled="StateNotificacaoLoading"
                                @click="deleteNotification(current)">Remover</v-btn-small>
                        </span>
                    </template>
                </modal-jr>
                <v-spacer></v-spacer>
                <v-btn-small v-if="!current.id" 
                    @click="saveNewNotification(current)"
                    :loading="StateNotificacaoLoading">Salvar</v-btn-small>
                <v-btn-small v-if="!!current.id" 
                    @click="saveOnChange(current)"
                    :loading="StateNotificacaoLoading">Alterar</v-btn-small>
            </template>
        </modal-jr>
        <!-- Criar componente que substitui o modal-jr -->
        <v-btn-small v-if="$verify.has_perm('add_notificacao')" v-show="item && !item.id"
            @click.stop="notificationForm"
            title="Nova notificação">
            <v-icon>mdi-plus</v-icon> Nova Notificação
        </v-btn-small>
        <v-btn-small v-if="$verify.has_perm('change_notificacao')" v-show="item && item.id"
            @click.stop="notificationForm"
            icon title="Alterar">
            <v-icon>mdi-pencil</v-icon>
        </v-btn-small>
    </div>
</template>
<script>
// import { bus } from '@/main'
import { mapActions, mapGetters } from 'vuex'
import NotificacaoFormValidation from '../../validations/forms/formNotificacao'
const formValidation = new NotificacaoFormValidation()
export default {
    name: 'NotificationForm',
    props:{
        item:{
            required: true,
        },
    },
    data: () => ({
        modal_code: 'notification-form',
        loading:false,
        current: {},
        required:[ v => !!v||'Campo Obrigatório' ],
    }),
    mounted(){
    },
    methods:{
        ...mapActions(['CreateNotificacao','UpdateNotificacao','DeleteNotificacao']),
        notificationForm(){
            var now = new Date()
            // inicializar data HOJE quando não houver DATA
            var dataInicio = now.setHours(now.getHours() - 4)
            dataInicio = new Date(dataInicio).toISOString().substring(0,16)
            // inicializar data AMANHÃ quando não houver data
            var dataFim = now.setDate(now.getDate() + 1)
            dataFim = new Date(dataFim).toISOString().substring(0,16)
            const current_object = this.item
            // atribuir a prop item a uma variável data
            this.current = current_object
            // ativar modal-jr
            this.$refs[this.modal_code].dialog = true
            // originalmente, o atributo "mensagem" é do tipo instancia Quill, para o Front será carregado apenas o html em "mensagem" e tratado no serializer
            this.current.mensagem = current_object.html
            // remover o sufixo de datetime (-03:00) para inicio e fim
            this.current.inicio = current_object && !!current_object.inicio ? current_object.inicio.substr(0,16): dataInicio
            this.current.fim = current_object && !!current_object.fim ? current_object.fim.substr(0,16): dataFim
        },
        onEditorBlur(quill) {
            quill
        },
        onEditorFocus(quill) {
            quill
        },
        onEditorReady(quill) {
            quill
        },
        onEditorChange(data) {
            data
        },
        onInputEditor(event){
            event
        },
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            let created = await this.CreateNotificacao(item)
            if (created){
                this.$emit('on-create-notification', created)
                this.$refs[this.modal_code].dialog = false
            }
        },
        async update(item){
            item
            let updated = await this.UpdateNotificacao(item)
            if (updated){
                // this.$emit('on-update-notification', updated)
                this.$refs[this.modal_code].dialog = false
            }
        },
        async saveOnChange(item){
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewNotification(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async deleteNotification(item){
            item
            // enviando "false" para data dialog, modal-jr irá fechar o dialog
            // utilizando um nova instancia do Vue (bus), eu posso fechar o dialog do componente modal-jr
            // 'close=-modal' nomeei para capturar no componente modal-jr
            let deleted = await this.DeleteNotificacao(item)
            // let keepOpenedDialog = !deleted
            // bus.$emit(`close-modal-${this.modal_code}`, keepOpenedDialog);
            this.$emit('on-delete-notification', deleted)
        },
        clear(){
            this.current = {}
        },
        onToggle(value){
            if (!value){
                // ao fechar modal-jr
                this.clear()
            }
        },
    },
    computed:{
        ...mapGetters(['StateNotificacaoLoading']),
        computedItem(){
            return this.item//this.details || this.item
        }
    },
    watch: {
        // propObject:{
        //     handler(value){
        //         console.log('watch for notification', value)
        //         const prop = value
        //         this.item = prop
        //     }, deep: true
        // }
    }
}
</script>