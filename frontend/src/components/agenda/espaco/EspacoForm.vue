<template>
    <div>
        <loading-jr :propObject="StateTipoEspacoLoading || 
                                StateRegraLoading" />

        <v-row class="between-rows">
            <v-spacer></v-spacer>
            
            <!-- BOTAO APAGAR  -->
            <modal-jr :fullscreen="false"
                :code="modal_code_delete"
                :ref="modal_code_delete"
                v-if="!!item.id" :with-cancel-btn="true"
                :toolbar-title="'Excluir '+item.descricao"
                :disabled="!$verify.has_perm('delete_room')"
                toolbar-color="error"
                btn-icon="mdi-delete">
                <template v-slot:activate-slot>
                    <v-btn color="error">
                        <span><v-icon>mdi-delete</v-icon> &nbsp;
                        </span>Remover Espaço
                    </v-btn>
                </template>
                <template v-slot:body>
                    <v-row>
                        <v-col cols="12" sm="12">
                            Tem certeza que você deseja apagar o Espaço <strong>{{item.descricao}}</strong>?
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:actions>
                    <v-btn :loading="StateEspacoLoading"
                        color="error"
                        @click="removeRoom(item)">Remover</v-btn>
                </template>
            </modal-jr>
        </v-row>

        <!-- Nome cor e ativo -->
        <v-row class="between-rows">
            <v-col cols="12" sm="6">
                <div>
                    <!-- eslint-disable-next-line -->
                    <v-text-field v-model="item.descricao"
                        @blur="saveOnChange({id:item.id, descricao:item.descricao})"
                        hide-details class="mt-3"
                        label="Nome do Espaço..." :rules="required" ></v-text-field>
                </div>
                <div class="mt-6">
                    <!-- eslint-disable-next-line -->
                    <v-switch v-model="item.ativo"
                        @update:modelValue="saveOnChange({id:item.id, ativo: item.ativo})"
                        :label="'Espaço ' + (computedItem.ativo ? 'Ativo' : 'Inativo')"
                        color="success" inset
                        density="compact" >
                    </v-switch>
                </div>
            </v-col>
            <v-col cols="12" sm="6">
                <!-- eslint-disable-next-line -->
                <v-color-picker v-model="item.color"
                    mode="hex"
                    dot-size="25"
                    elevation="0"
                    hide-canvas
                    swatches-max-height="100"
                    @update:modelValue="saveOnChange({id:item.id, color:item.color})"
                    ></v-color-picker>
            </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <!-- Tipo e Filiais do Espaco -->
        <v-row class="between-rows">
            <v-col cols="12" sm="6" class="my-2">
                <div>
                    <span class="font-weight-medium">Tipo de Espaco: </span>
                    <v-btn-small icon :tile="false"
                        @click="onChangeTipoEspaco"
                        :loading="StateTipoEspacoLoading">
                        <v-icon title="Recarregar tipos de espaços">mdi-refresh</v-icon>
                    </v-btn-small>
                </div>
                <div>
                    <!-- eslint-disable-next-line -->
                    <v-chip-group v-model="item.tipo_espaco"
                        color="primary"
                        column
                        @update:modelValue="saveOnChange({id:item.id, tipo_espaco:item.tipo_espaco})">
                        <v-chip filter label v-for="tipo_espaco in StateTipoEspaco"
                            :key="tipo_espaco.id" :value="tipo_espaco.id">
                            {{ tipo_espaco.descricao }}
                            <span v-if="tipo_espaco.required_approve" title="Requer aprovação" >
                                &nbsp; <v-icon>mdi-information-outline</v-icon>
                            </span>
                        </v-chip>
                    </v-chip-group>
                    <TipoEspaco>
                        <template v-slot:modal-activate>
                            <v-chip label link>
                                <span title="Adicionar Tipo de Espaço">
                                    <v-icon >mdi-plus</v-icon> Adicionar tipo de espaço
                                </span>
                            </v-chip>
                        </template>
                    </TipoEspaco>
                </div>
            </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <!-- Gestores e Supers -->
        <v-row class="between-rows">
            <v-col cols="12" sm="6" class="my-2">
                <div>
                    <span class="font-weight-medium">Gestores:</span>
                    <!-- eslint-disable-next-line -->
                    <v-autocomplete v-model="item.gestores"
                        class="mt-3"
                        item-color="primary"
                        chips deletable-chips small-chips
                        :loading="StateEspacoLoading"
                        no-data-text="Nenhum Gestor"
                        label="Selecionar Gestores"
                        :items="StateGestores"
                        item-value="id"
                        item-title="email"
                        multiple
                        messages="Gestores receberão notificações de reservas"
                        @update:modelValue="saveOnChange({id:item.id, gestores:item.gestores})"
                    >
                    </v-autocomplete>
                </div>
            </v-col>
            <v-col cols="12" sm="6" class="my-2">
                <div>
                    <span class="font-weight-medium">Super usuários:</span>
                    <!-- eslint-disable-next-line -->
                    <v-autocomplete v-model="item.admins"
                        class="mt-3"
                        item-color="primary"
                        chips deletable-chips small-chips
                        :loading="StateEspacoLoading"
                        no-data-text="Nenhum usuário"
                        label="Selecionar admins"
                        :items="StateAdmins"
                        item-value="id"
                        item-title="email"
                        multiple
                        messages="Usuários com privilégios sobre restrições"
                        @update:modelValue="saveOnChange({id:item.id, admins:item.admins})"
                    >
                    </v-autocomplete>
                </div>
            </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <!-- Parametrizacoes Gerais -->
        <v-row class="between-rows">
            <v-col cols="12">
                <span class="font-weight-medium">Parametrizações gerais:</span>
            </v-col>
            <v-col cols="12">
                <v-row>
                    <v-col cols="12" sm="6">
                        <div class="my-3"></div>
                        <v-row>
                            <v-col cols="12" sm="12" >
                                <!-- DURAÇÃO MÁXIMA (MIN) -->
                                <div class="mr-12 my-4">
                                    <!-- eslint-disable-next-line -->
                                    <v-text-field v-model="item.max_duracao"
                                        @blur="saveOnChange({id:item.id, max_duracao:item.max_duracao})"
                                        :loading="StateEspacoLoading"
                                        type="number"
                                        label="Duração máxima"
                                        messages="Duração máxima (em minutos) que uma reserva pode ocupar"
                                    >
                                        <template v-slot:append>minutos</template>
                                    </v-text-field>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- DURAÇÃO MINIMA (MIN) -->
                                <div class="mr-12 my-4">
                                    <!-- eslint-disable-next-line -->
                                    <v-text-field v-model="item.min_duracao"
                                        @blur="saveOnChange({id:item.id, min_duracao:item.min_duracao})"
                                        :loading="StateEspacoLoading"
                                        type="number"
                                        label="Duração mínima"
                                        messages="Duração mínima (em minutos) necessária para abertura de reservas"
                                    >
                                        <template v-slot:append>minutos</template>
                                    </v-text-field>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- CARÊNCIA DE ABERTURA (HORAS) -->
                                <div class="mr-12 my-4">
                                    <!-- eslint-disable-next-line -->
                                    <v-text-field v-model="item.min_criacao"
                                        @blur="saveOnChange({id:item.id, min_criacao:item.min_criacao})"
                                        :loading="StateEspacoLoading"
                                        type="number"
                                        label="Carência mínima"
                                        messages="Prazo mínimo (em horas) necessário até a data da reserva"
                                    >
                                        <template v-slot:append>hora(s)</template>
                                    </v-text-field>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-text-field v-model="item.limitar_abertura_qtde"
                                    @blur="saveOnChange({id:item.id, limitar_abertura_qtde:item.limitar_abertura_qtde})"
                                    :loading="StateEspacoLoading"
                                    type="number" min="1"
                                    label="Qtde reservas por usuário"
                                    messages="Limitar a quantidade máxima de reservas em ABERTO ou PENDENTE por usuário"
                                >
                                    <template v-slot:append>
                                        <!-- eslint-disable-next-line -->
                                        <v-switch v-model="item.limitar_abertura" class="ma-0 pa-0"
                                            :loading="StateEspacoLoading"
                                            @update:modelValue="saveOnChange({
                                                id:item.id, limitar_abertura:item.limitar_abertura,
                                                limitar_abertura_qtde:item.limitar_abertura_qtde
                                                })"
                                            color="success"
                                            inset dense
                                            :messages="item.limitar_abertura ? 'Limitado a '+ item.limitar_abertura_qtde+ ' reserva(s)':'Desabilitado'"
                                            >
                                        </v-switch>
                                    </template>
                                </v-text-field>
                            </v-col>
                        </v-row>

                    </v-col>
                    <v-col cols="12" sm="6" >
                        <v-row>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.enviar_notificacao"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, enviar_notificacao:item.enviar_notificacao})"
                                    :label="computedItem.enviar_notificacao ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Habilita o envio de notificações por e-mail"
                                    >
                                </v-switch>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.permite_criar_sabados"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, permite_criar_sabados:item.permite_criar_sabados})"
                                    :label="computedItem.permite_criar_sabados ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Permitir registrar eventos aos sábados"
                                    >
                                </v-switch>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.permite_reservar_sabado"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, permite_reservar_sabado:item.permite_reservar_sabado})"
                                    :label="computedItem.permite_reservar_sabado ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Permitir registrar para um sábado"
                                    >
                                </v-switch>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.permite_criar_domingos"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, permite_criar_domingos:item.permite_criar_domingos})"
                                    :label="computedItem.permite_criar_domingos ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Permitir registrar eventos aos domingos"
                                    >
                                </v-switch>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.permite_reservar_domingo"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, permite_reservar_domingo:item.permite_reservar_domingo})"
                                    :label="computedItem.permite_reservar_domingo ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Permitir registrar para um domingo"
                                    >
                                </v-switch>
                            </v-col>
                            <v-col cols="12" sm="12" >
                                <!-- eslint-disable-next-line -->
                                <v-switch v-model="item.requer_aprovacao"
                                    :loading="StateEspacoLoading"
                                    @update:modelValue="saveOnChange({id:item.id, requer_aprovacao:item.requer_aprovacao})"
                                    :label="computedItem.requer_aprovacao ? 'Sim' : 'Não'"
                                    color="success"
                                    inset dense
                                    messages="Espaço requer aprovação? Reservas ficam pendente até aprovação"
                                    >
                                </v-switch>
                            </v-col>
                            <!-- LIMITAR ABERTURA RESERVAS -->
                            <v-col cols="12">
                                
                            </v-col>
                        </v-row>

                    </v-col>
                </v-row>
            </v-col>
        </v-row>

        <v-divider class="my-2"></v-divider>

        <!-- Regras -->
        <v-row class="between-rows">
            <v-col cols="12">
                <strong class="font-weight-medium">Restrições: </strong>
                <v-btn-small :tile="false" icon
                    @click="GetAgendaLabsRegras"
                    :loading="StateRegraLoading">
                    <v-icon title="Recarregar restrições">mdi-refresh</v-icon>
                </v-btn-small>
                <div class="pl-4">
                    <div><small>Períodos em que a sala está bloqueada para agendamento</small></div>
                    <!-- eslint-disable-next-line -->
                    <v-chip-group v-model="item.regras"
                        column multiple
                        color="primary"
                        @update:modelValue="saveOnChange({id:item.id, regras:item.regras})"
                        >
                        <v-chip filter label v-for="role in StateRegras" :key="role.id" :value="role.id">
                            {{ role.week_day_name }} {{role.start_time}} - {{role.end_time}}
                        </v-chip>
                    </v-chip-group>
                    <Regra>
                        <template v-slot:modal-activate>
                            <v-chip label link>
                                <span title="Adicionar Restrição">
                                    <v-icon small>mdi-plus</v-icon> Adicionar Restrição
                                </span>
                            </v-chip>
                        </template>
                    </Regra>
                </div>
            </v-col>
        </v-row>

        <!-- Instruções -->
        <v-row class="between-rows">
            <v-col cols="12" sm="12">
                <span class="font-weight-medium">Orientações:</span>
                <div>
                    <!-- eslint-disable-next-line -->
                    <quill-editor v-model:content="item.instrucoes_espaco"
                        @blur="saveOnChange({id:item.id, instrucoes_espaco:item.instrucoes_espaco})"
                        content-type="html"
                        toolbar="full">
                    </quill-editor>
                </div>
                <!-- <tiptap-vuetify
                    :loading="StateEspacoLoading"
                    :toolbar-attributes="{ color: 'primary', dark:true }"
                    :card-props="{ outlined:true }"
                    v-model="item.instrucoes_espaco"
                    :extensions="extensions"
                    @blur="saveOnChange({id:item.id, instrucoes_espaco:item.instrucoes_espaco})"
                /> -->
            </v-col>
        </v-row>
       

            
        <!-- SALVAR NOVA SALA -->
        <v-btn v-if="!item.id" color="primary"
            @click="saveNewRoom(item)"
            :disabled="StateEspacoLoading">Salvar</v-btn>
    </div>
</template>
<script>
// import { bus } from './../../../main'
import { mapActions, mapGetters } from 'vuex'
import EspacoFormValidation from '../../../validations/forms/formEspaco'
import TipoEspaco from '../tipo_espaco/TipoEspaco.vue'
import Regra from '../regra/Regra.vue'
import FrontendService from '@/services/frontendService';
// import the component and the necessary extensions
// import {
//     TiptapVuetify,
//     Heading, Bold, Italic, Strike, Underline,
//     Code, Paragraph, BulletList, OrderedList,
//     ListItem, Link, Blockquote, HardBreak,
//     HorizontalRule, History } from 'tiptap-vuetify'
const fs = new FrontendService()
const formValidation = new EspacoFormValidation()
export default {
    name: 'AgendaEspacoForm',
    components:{
        TipoEspaco, Regra,
        // TiptapVuetify
    },
    props:{
        item:{
            required:true,
        },
    },
    data: () => ({
        extensions: [
            // History,
            // Blockquote,
            // Link,
            // Bold,
            // Italic,
            // Underline,
            // Strike,
            // ListItem,
            // BulletList,
            // OrderedList,
            // [Heading, {
            //     options: {
            //     levels: [1, 2, 3]
            //     }
            // }],
            // Code,
            // HorizontalRule,
            // Paragraph,
            // HardBreak
        ],
        search_gestor:'',
        loading:false,
        required:[ v => !!v||'Campo Obrigatório' ],
        modal_code_delete: 'room-form-delete',
    }),
    methods:{
        ...mapActions(['GetGestores',
                        'GetAgendaLabsEspacos',
                        'CarregarMaisGestores',
                        'ListCorporations',
                        'GetAgendaLabsTipoEspacos',
                        'GetAgendaLabsRegras',
                        'GetAdmins',
                        'UpdateRoom',
                        'CreateRoom',
                        'DeleteRoom'
        ]),
        HasPerm(code){
            return fs.has_perm(code)
        },
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            let created = await this.CreateRoom(item)
            this.$emit('on-create-room', created)
        },
        async update(item){
            let updated = await this.UpdateRoom(item)
            this.$emit('on-update-room', updated)
        },
        async delete(item){
            let deleted = await this.DeleteRoom(item)
            this.$emit('on-delete-room', deleted)
        },
        async saveOnChange(item){
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewRoom(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async removeRoom(item){
            if(item.id) await this.delete(item)
        },
        onChangeTipoEspaco(){
            this.GetAgendaLabsTipoEspacos()
        }
    },
    computed:{
        ...mapGetters(['StateTipoEspaco','StateGestores','StateRegras', ]),
        ...mapGetters(['StateAdmins']),
        ...mapGetters(['StateTipoEspacoLoading','StateGestoresLoading','StateRegraLoading']),
        ...mapGetters(['StateEspacoLoading']),
        ...mapGetters(['StatePaginateGestores']),
        computedItem(){
            return this.item // this.details || this.item
        }
    },
    mounted(){
        this.ListCorporations()
        this.GetGestores({page_size: 500})
        this.GetAdmins({page_size: 500})
        this.GetAgendaLabsRegras()
        this.GetAgendaLabsTipoEspacos()
    },
}
</script>

<style scoped>
.between-rows{
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>