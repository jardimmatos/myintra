<template>
    <div>
        <small v-if="false" class="text-disabled">{{selected.id}}</small>
        <v-row v-if="$verify.has_perm('change_statusdispositivo', false) || $verify.has_perm('add_statusdispositivo', false)">
            <v-col cols="12" sm="4">
                <v-text-field hide-details class="mb-1"
                    v-model="selected.identificador"
                    ref="formDispositivo" 
                    label="Identificador">
                </v-text-field>
            </v-col>
            <v-col cols="12" sm="5">
                <v-autocomplete hide-details class="mb-1"
                    v-model="selected.equipamento"
                    :items="StateRecursosEquipamentos"
                    item-value="id"
                    placeholder="Equipamento"
                    item-title="descricao">
                </v-autocomplete>
            </v-col>
            <v-col cols="12" sm="4">
                <v-text-field hide-details class="mb-1"
                    v-model="selected.serie"
                    label="Nº Série">
                </v-text-field>
            </v-col>
            <v-col cols="12" sm="5">
                <v-select hide-details class="mb-1"
                    v-model="selected.status_inventario"
                    :items="StateRecursosStatusDispositivos"
                    placeholder="Status Inventário"
                    item-value="id"
                    item-title="descricao">
                    <template #chip="{ item }">
                        <v-chip-small variant="flat" tile :color="item.raw.color">
                            {{item.raw.descricao}}
                            <v-icon>{{item.raw.permite_circular ? 'mdi-check': 'mdi-cancel'}}</v-icon>
                        </v-chip-small>
                    </template>
                </v-select>
            </v-col>
            <v-col cols="12" sm="9">
                <v-textarea hide-details class="mb-1"
                    v-model="selected.obs"
                    label="Informações adicionais"
                    rows="3">
                </v-textarea>
            </v-col>
            <v-col cols="12" sm="9">
                <v-textarea hide-details class="mb-1"
                    v-model="selected.obs_inventario"
                    label="Observações de Inventário"
                    rows="3">
                </v-textarea>
            </v-col>
            <v-col cols="12" sm="9">
                <span v-if="!!selected.id">
                    <v-btn-small v-if="$verify.has_perm('change_dispositivo', false)"
                        @click="saveItem(selected)">
                        Alterar
                    </v-btn-small>
                </span>
                <span v-else>
                    <v-btn-small v-if="$verify.has_perm('add_dispositivo', false)"
                        @click="saveItem(selected)">
                        Adicionar Novo
                    </v-btn-small>
                </span>
            </v-col>
        </v-row>

        <!-- TABELA -->
        <v-row>
            <v-col cols="12" sm="12">
                <v-text-field v-model="search" label="Pesquisar..." hide-details></v-text-field>
                <!-- eslint-disable-next-line -->
                <v-data-table v-model:expanded="expanded" show-expand
                    :search="search"
                    :loading="StateRecursosLoading == 'get-equipamentos'"
                    :items="StateRecursosDispositivos"
                    multi-sort
                    item-value="id"
                    :sort-by="[
                        { key: 'descricao', order: 'asc' },
                    ]"
                    :headers="[
                            { title: 'Identificador', align: 'start', sortable: false, value: 'identificador', width:'1'},
                            { title: 'Série', align: 'start', sortable: false, value: 'serie', width:'1'},
                            { title: 'Equipamento', align: 'start', sortable: false, value: 'equipamento_object.descricao', width:'100px'},
                            { title: 'Status Invent.', align: 'center', sortable: false, value: 'status_inventario', width:'150px'},
                            { title: 'Situação', align: 'center', sortable: false, value: 'situacao', width:'150px'},
                            { title: ' ', align: 'end', sortable: false, value: 'opcoes', width:'1' },
                        ]"
                    >
                    <template v-slot:loading>
                        <v-skeleton-loader type="table-row@3"></v-skeleton-loader>
                    </template>
                    <template v-slot:expanded-row="{ columns, item }">
                        <tr>
                            <td :colspan="columns.length" class="pa-2">
                                <div class="text-disabled">
                                    # {{item.id}}
                                </div>
                                <div class="my-2">
                                    Obs: {{item.obs}}
                                </div>
                                <div class="my-2">
                                    Obs Inventário: {{item.obs_inventario}}
                                </div>
                                <v-divider class="my-2"></v-divider>
                                <div v-for="i in item.item_objects||[]" :key="i.id">
                                </div>
                            </td>
                        </tr>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.opcoes="{ item }">
                        <v-menu top left v-if="itemMenuOptions(item).length"
                            location="start"
                            transition="slide-x-transition">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-btn-small v-bind="activatorProps" icon v-if="itemMenuOptions(item).length">
                                    <v-icon>mdi-dots-vertical</v-icon>
                                </v-btn-small>
                            </template>
                            <v-list density="compact">
                                <v-list-item @click="m.do()" v-for="m, index in itemMenuOptions(item)" :key="index">
                                    <v-list-item-title>
                                        <v-icon-small color="grey">{{m.icon}}</v-icon-small>
                                        {{m.label}}
                                    </v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                        <loading-jr :propObject="StateRecursosLoading == `get-log-dispositivo-${item.id}`"
                            text="Carregando logs de dispositivo" />
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.status_inventario="{ item }">
                        <td>
                            <v-chip-small variant="flat" tile :color="(item.status_inventario_object||{}).color||'grey'">
                                {{(item.status_inventario_object||{}).descricao||'Nenhum'}}
                            </v-chip-small>
                            <span class="mx-2">
                                <helper-jr 
                                    :text="(item.status_inventario_object||{}).permite_circular ? 'Pode circular': 'Não pode circular'"
                                    :icon="(item.status_inventario_object||{}).permite_circular ? 'mdi-check' : 'mdi-cancel'"
                                    :iconColor="(item.status_inventario_object||{}).permite_circular ? 'success' : 'error'"
                                ></helper-jr>
                            </span>
                        </td>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.situacao="{ item }">
                        <v-chip-small variant="flat" tile
                            :loading="[`enable-dispositivos-${item.id}`,`manutencao-dispositivos-${item.id}`].includes(StateRecursosLoading)"
                            :color="item.situacao_object.color">
                            {{item.situacao_object.value}}
                        </v-chip-small>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.identificador="{ item }">
                        <span class="text-subtitle-2">
                            {{item.identificador}}
                        </span>
                    </template>
                    
                </v-data-table>
            </v-col>

        </v-row>

        <!-- LOG DISPOSITIVO -->
        <modal-jr ref="modalLogDispositivo" fullscreen dialogWidth="100%">
            <template #activate-slot>
                <span></span>
            </template>
            <template #body>
                <ListaPaginada :dataResults="logsDispositivo">
                    <template #body="{ listaitem }">
                        
                        <v-row>
                            <v-col cols="12" sm="4">
                                {{((listaitem.circulacao_object||{}).local_object||{}).descricao}}
                            </v-col>
                            <v-col cols="12" sm="4">
                                {{$verify.formatarData(listaitem.created_at) }}
                            </v-col>
                            <v-col cols="12" sm="4" align="right">
                                <v-chip-small variant="flat" tile
                                    :color="listaitem.situacao_object.color">
                                    {{listaitem.situacao_object.value}}
                                </v-chip-small>
                            </v-col>
                            <v-col cols="12">
                                <div class="text-disabled">
                                    Incluído por: {{ listaitem.created_by.first_name }} {{ listaitem.created_by.last_name }}
                                </div>
                            </v-col>
                            <v-col cols="12">
                                <div class="text-subtitle-2 text-disabled">
                                    Obs: {{ listaitem.obs }}
                                </div>
                            </v-col>
                        </v-row>
                    </template>
                </ListaPaginada>
            </template>
        </modal-jr>
    
    </div>    
</template>
<script>
import InfraDispositivoValidate from '@/validations/infraestrutura/formDispositivo'
const formValidation = new InfraDispositivoValidate()
import { mapGetters, mapActions } from 'vuex';
import ListaPaginada from '@/components/layouts/partials/ListaPaginada.vue';
export default {
    name: 'DispositivosComponent',
    components: {
        ListaPaginada
    },
    data: ()=>({
        selected: {},
        search: null,
        expanded: null,
        logsDispositivo: {},
        logs_page_size: 50
    }),
    methods: {
        ...mapActions([
            'GetRecursosEquipamentos',
            'GetRecursosStatusDispositivos',
            'GetRecursosDispositivos',
            'CreateRecursosDispositivos',
            'UpdateRecursosDispositivos',
            'GetRecursosEnumsDispositivos',
            'DisponibilizarRecursosDispositivos',
            'ManutencaoRecursosDispositivos',
            'AvariaRecursosDispositivos',
            'ExtravioRecursosDispositivos',
            'GetRecursosLogDispositivo',
            'DeleteRecursosLogDispositivo'
        ]),
        async openLogDispositivosModal(item){
            this.logsDispositivo = await this.GetRecursosLogDispositivo({
                                                                        dispositivo: item.id,
                                                                        page_size: this.logs_page_size
                                                                    })
            if(!(this.logsDispositivo.results||[]).length){
                alert('Nenhum log registrado para este dispositivo!')
                return
            }
            this.$refs.modalLogDispositivo.dialog = true
            
        },
        async setDisponivel(item){
            const enabled = await this.DisponibilizarRecursosDispositivos(item)
            if (enabled){
                this.GetRecursosDispositivos()
            }
        },
        async setManutencao(item){
            const obs = prompt('Necessário informar uma observação')
            if (!obs) return
            item.obs = obs
            const enabled = await this.ManutencaoRecursosDispositivos(item)
            if (enabled){
                this.GetRecursosDispositivos()
            }
        },
        async setAvaria(item){
            const obs = prompt('Necessário informar uma observação')
            if (!obs) return
            item.obs = obs
            const enabled = await this.AvariaRecursosDispositivos(item)
            if (enabled){
                this.GetRecursosDispositivos()
            }
        },
        async setExtravio(item){
            const obs = prompt('Necessário informar uma observação')
            if (!obs) return
            item.obs = obs
            const enabled = await this.ExtravioRecursosDispositivos(item)
            if (enabled){
                this.GetRecursosDispositivos()
            }
        },
        onSelectItem(item){
            const selected = Object.assign({}, item)
            this.selected = selected
            this.$refs.formDispositivo.focus()
        },
        resetSelected(){
            const selected = Object.assign({}, {})
            this.selected = selected
        },
        async saveItem(item){   
            if(this.validateForm(item)){
                if(item.id){
                    const updated = await this.UpdateRecursosDispositivos(item)
                    if(updated){
                        this.resetSelected()
                        this.GetRecursosDispositivos()
                    }
                }else{
                    const created = await this.CreateRecursosDispositivos(item)
                    if(created){
                        this.resetSelected()
                        this.GetRecursosDispositivos()
                    }
                }
                this.$refs.formDispositivo.focus()
            }
        },
        validateForm(item){
            if(!item) return false
            const validate = formValidation.validate(item)
            return validate
        },
        async init(){
            await this.GetRecursosEquipamentos()
            await this.GetRecursosEnumsDispositivos()
            await this.GetRecursosStatusDispositivos()
            await this.GetRecursosDispositivos()
        },
        async removerLogs(item){
            await this.DeleteRecursosLogDispositivo({dispositivo: item.id})
        },
        itemMenuOptions(item){
            const menus = [
                { 
                    if: this.$verify.has_perm('change_dispositivo', false),
                    do: () => this.onSelectItem(item),
                    icon: 'mdi-pencil',
                    label: 'Editar'
                },
                {
                    if: ['MANUTENCAO', 'EXTRAVIO', 'AVARIADO'].includes(item.situacao) &&
                        this.$verify.has_perm('change_dispositivo', false),
                    do: () => this.setDisponivel(item),
                    icon: 'mdi-check',
                    label: 'Atualizar para Disponível'
                },
                {
                    if: ['DISPONIVEL','EXTRAVIO', 'AVARIADO'].includes(item.situacao) &&
                        this.$verify.has_perm('change_dispositivo', false),
                    do: () => this.setManutencao(item),
                    icon: 'mdi-wrench',
                    label: 'Em Manutenção'
                },
                {
                    if: ['DISPONIVEL','EXTRAVIO',].includes(item.situacao) &&
                        this.$verify.has_perm('change_dispositivo', false),
                    do: () => this.setAvaria(item),
                    icon: 'mdi-trophy',
                    label: 'Avariado'
                },
                {
                    if: ['DISPONIVEL', 'AVARIADO'].includes(item.situacao) &&
                        this.$verify.has_perm('change_dispositivo', false),
                    do: () => this.setExtravio(item),
                    icon: 'mdi-close-outline',
                    label: 'Extraviado'
                },
                { 
                    if: this.$verify.has_perm('view_logdispositivo', false),
                    do: () => this.openLogDispositivosModal(item),
                    icon: 'mdi-refresh',
                    label: 'Logs do Dispositivo'
                },
                { 
                    if: this.$verify.has_perm('delete_logdispositivo', false),
                    do: () => this.removerLogs(item),
                    icon: 'mdi-close',
                    label: 'Remoção de Logs'
                }
            ]
            return menus.filter(f=> f.if)

        }
    },
    computed: {
        ...mapGetters([
                    'StateRecursosEquipamentos',
                    'StateRecursosDispositivos',
                    'StateRecursosStatusDispositivos',
                    'StateRecursosEnumsDispositivos',
                    'StateRecursosLoading'
                    ])
    },
    mounted(){
        this.init()
    }
    
}
</script>