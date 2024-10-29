<template>
    <div>
        <v-card variant="outlined" class="mb-1">
            <v-card-subtitle>
                <v-row>
                    <span class="text-subtitle-1 mt-2">
                        {{item.dispositivo_object.identificador}} - {{item.dispositivo_object.equipamento_object.descricao}}
                    </span>
                    <v-spacer></v-spacer>
                    <v-menu top left v-if="itemCirculacaoOptions(item).length"
                        rounded="bl-xl tl-xl tr-sm br-sm" offset-y transition="slide-x-transition">
                        <template v-slot:activator="{ props: activatorProps }">
                            <v-btn-small variant="plain" v-if="itemCirculacaoOptions(item).length"
                                v-bind="activatorProps" icon>
                                <v-icon>mdi-dots-vertical</v-icon>
                            </v-btn-small>
                        </template>
                        <v-list dense>
                            <v-list-item v-for="m, mi in itemCirculacaoOptions(item)" :key="mi"
                                @click="m.do()">
                                <v-list-item-title>
                                    <v-icon-small color="grey">{{m.icon}}</v-icon-small>
                                    {{m.label}}
                                </v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-row>
                <!-- <div class="text-disabled text-subtitle-2">{{item.id}}</div> -->
            </v-card-subtitle>
            <v-card-text>
                <v-row>
                    <v-chip-small variant="flat" tile
                        :color="item.situacao_object.color">
                        {{item.situacao_object.value}}
                    </v-chip-small>
                    <v-col cols="12" sm="12">
                        <div v-show="!!item.devolvido_em">Em: {{ $verify.formatarData(item.devolvido_em) }}</div>
                        <div v-show="!!item.recebido_por">por: {{ item.recebedor }}</div>
                    </v-col>
                    <v-col cols="12" sm="12" v-show="!!item.obs">
                        <div>Obs: <span class="font-italic">{{item.obs}}</span></div>
                    </v-col>
                    <v-divider></v-divider>
                    <v-col cols="12" class="pa-0">
                        <small class="font-italic">Saída: {{ $verify.formatarData(item.created_at) }}</small>
                    </v-col>
                    <v-col cols="12" class="pa-0">
                        <small class="font-italic">Incluído por: {{ (item.created_by||{}).first_name }} {{ (item.created_by||{}).last_name }}</small>
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>

        <!-- MODAL DE BAIXA -->
        <modal-jr dialogWidth="50%" :no-actions="true" ref="receberCirculacaoItem"
            toolbar-title="Baixar Circulação">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="receberCirculacaoItem.devolvido_em"
                            label="Data devolução">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="receberCirculacaoItem.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setReceber(receberCirculacaoItem)">Baixar</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- MODAL DE ESTORNO -->
        <modal-jr dialogWidth="50%" :no-actions="true" ref="estornarCirculacaoItem"
            toolbar-title="Estornar Circulação">
            <template v-slot:activate-slot><span></span></template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="estornarCirculacaoItem.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setEstornar(estornarCirculacaoItem)">Estornar</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- MODAL DE AVARIA -->
        <modal-jr dialogWidth="50%" :no-actions="true" ref="avariarCirculacaoItem"
            toolbar-title="Avaria Circulação">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="avariarCirculacaoItem.devolvido_em"
                            label="Data devolução">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="avariarCirculacaoItem.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setAvariar(avariarCirculacaoItem)">Registrar Avaria</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- MODAL DE CANCELAR -->
        <modal-jr dialogWidth="50%" :no-actions="true" ref="cancelarCirculacaoItem"
            toolbar-title="Cancelar Circulação">
            <template v-slot:activate-slot><span></span></template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="cancelarCirculacaoItem.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setCancelar(cancelarCirculacaoItem)">Cancelar Item</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- MODAL DE EXTRAVIO -->
        <modal-jr dialogWidth="50%" :no-actions="true" ref="extraviarCirculacaoItem"
            toolbar-title="Extravio Circulação">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="extraviarCirculacaoItem.devolvido_em"
                            label="Data devolução">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="extraviarCirculacaoItem.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setExtraviar(extraviarCirculacaoItem)">Registrar Extravio</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        
    </div>    
</template>
<script>
import InfraCirculacaoItemValidate from '@/validations/infraestrutura/formCirculacaoItem'
const formValidation = new InfraCirculacaoItemValidate()
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'CirculacaoItemComponent',
    data: ()=>({
        selected: {},
        search: null,
        expanded: null,
        receberCirculacaoItem:{},
        estornarCirculacaoItem:{},
        avariarCirculacaoItem:{},
        cancelarCirculacaoItem:{},
        extraviarCirculacaoItem:{},
    }),
    props:{
        item: {
            required: true
        }
    },
    methods: {
        ...mapActions([
            'ReceberRecursosCirculacaoItem',
            'EstornarRecursosCirculacaoItem',
            'AvariarRecursosCirculacaoItem',
            'CancelarRecursosCirculacaoItem',
            'ExtraviarRecursosCirculacaoItem',
        ]),
        
        /** BAIXA NORMAL */
        async openReceberModal(item){
            this.$refs.receberCirculacaoItem.dialog = true
            this.receberCirculacaoItem = Object.assign({}, item)
            this.receberCirculacaoItem.devolvido_em = new Date().format('YYYY-MM-DD HH:mm')
            this.receberCirculacaoItem.obs = '' // limpar obs ao receber normal
        },
        async setReceber(item){
            const payload = {
                ids: [item.id],
                obs: item.obs,
                devolvido_em: item.devolvido_em
            } 
            if(formValidation.validate_receber(payload)){
                const enabled = await this.ReceberRecursosCirculacaoItem(payload)
                if (enabled){
                    this.$emit('change-item', true)
                    this.$refs.receberCirculacaoItem.dialog = false
                }
            }
        },

        /** ESTORNO */
        async openEstornarModal(item){
            this.$refs.estornarCirculacaoItem.dialog = true
            this.estornarCirculacaoItem = Object.assign({}, item)
        },
        async setEstornar(item){
            if(formValidation.validate_estornar(item)){
                const payload = {
                    ids: [item.id],
                    obs: item.obs
                } 
                const enabled = await this.EstornarRecursosCirculacaoItem(payload)
                if (enabled){
                    this.$emit('change-item', true)
                    this.$refs.estornarCirculacaoItem.dialog = false
                }
            }
        },

        /** AVARIA */
        async openAvariarModal(item){
            this.$refs.avariarCirculacaoItem.dialog = true
            this.avariarCirculacaoItem = Object.assign({}, item)
            this.avariarCirculacaoItem.devolvido_em = new Date().format('YYYY-MM-DD HH:mm')
        },
        async setAvariar(item){
            if(formValidation.validate_avariar(item)){
                const payload = {
                    ids: [item.id],
                    obs: item.obs,
                    devolvido_em: item.devolvido_em
                } 
                const enabled = await this.AvariarRecursosCirculacaoItem(payload)
                if (enabled){
                    this.$emit('change-item', true)
                    this.$refs.avariarCirculacaoItem.dialog = false
                }
            }
        },

        /** CANCELAR */
        async openCancelarModal(item){
            this.$refs.cancelarCirculacaoItem.dialog = true
            this.cancelarCirculacaoItem = Object.assign({}, item)
        },
        async setCancelar(item){
            if(formValidation.validate_cancelar(item)){
                const payload = {
                    ids: [item.id],
                    obs: item.obs
                } 
                const enabled = await this.CancelarRecursosCirculacaoItem(payload)
                if (enabled){
                    this.$emit('change-item', true)
                    this.$refs.cancelarCirculacaoItem.dialog = false
                }
            }
        },

        /** EXTRAVIAR */
        async openExtraviarModal(item){
            this.$refs.extraviarCirculacaoItem.dialog = true
            this.extraviarCirculacaoItem = Object.assign({}, item)
            this.extraviarCirculacaoItem.devolvido_em = new Date().format('YYYY-MM-DD HH:mm')
        },
        async setExtraviar(item){
            if(formValidation.validate_extraviar(item)){
                const payload = {
                    ids: [item.id],
                    obs: item.obs,
                    devolvido_em: item.devolvido_em
                } 
                const enabled = await this.ExtraviarRecursosCirculacaoItem(payload)
                if (enabled){
                    this.$emit('change-item', true)
                    this.$refs.extraviarCirculacaoItem.dialog = false
                }
            }
        },

        itemCirculacaoOptions(i){
            const menus = [
                {
                    if: ['EM_CIRCULACAO'].includes(i.situacao),
                    do: () => this.openReceberModal(i),
                    icon: 'mdi-check',
                    label: 'Baixar Normal'
                },
                {
                    if: ['BAIXADO_NORMAL','CIRCULACAO_CANCELADA'].includes(i.situacao),
                    do: () => this.openEstornarModal(i),
                    icon: 'mdi-refresh',
                    label: 'Estornar'
                },
                {
                    if: ['EM_CIRCULACAO'].includes(i.situacao),
                    do: () => this.openAvariarModal(i),
                    icon: 'mdi-trophy-broken',
                    label: 'Avariado'
                },
                {
                    if: ['EM_CIRCULACAO'].includes(i.situacao),
                    do: () => this.openExtraviarModal(i),
                    icon: 'mdi-progress-close',
                    label: 'Extraviado'
                },
                {
                    if: ['EM_CIRCULACAO'].includes(i.situacao),
                    do: () => this.openCancelarModal(i),
                    icon: 'mdi-close',
                    label: 'Cancelar'
                }
            ]
            return menus.filter(m => m.if)
        }
    },
    computed: {
        ...mapGetters([
                    'StateRecursosLoading'
                    ])
    },
    mounted(){
    }
    
}
</script>