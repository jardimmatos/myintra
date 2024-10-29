<template>
    <div>
        <!-- Form Create -->
        <v-row v-if="$verify.has_perm('change_circulacao', false) || $verify.has_perm('add_circulacao', false)">
            <v-col cols="12" sm="6" md="7" lg="6" xl="4" xxl="3">
                <v-row no-gutters>
                    <v-col cols="12">
                        <v-text-field hide-details class="mb-1"
                            v-model="selected.responsavel"
                            label="Nome/Responsável">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-text-field hide-details class="mb-1"
                            v-model="selected.email"
                            label="E-mail">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6" v-if="!selected.id">
                        <v-autocomplete hide-details class="mb-1"
                            :items="StateRecursosLocais"
                            v-model="selected.local"
                            item-value="id"
                            item-title="descricao"
                            :loading="StateRecursosLoading == 'get-dispositivos'"
                            label="Local">
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="selected.previsao_devolucao"
                            label="Previsão de Devolução">
                        </v-text-field>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="6" md="5" lg="6" xl="4" xxl="3">
                <v-row>
                    <v-col cols="12" sm="12" v-if="!selected.id">
                        <v-autocomplete density="default" hide-details class="mb-1"
                            :loading="StateRecursosLoading == 'get-dispositivos-enums'"
                            chips
                            :items="computedDispositivosDisponiveis"
                            v-model="selected.itens_dispositivos"
                            multiple
                            item-value="id"
                            :item-title="i => !!i.identificador ? `${i.identificador} - ${i.equipamento_object.descricao}`: ''"
                            label="Dispositivos">
                            <template #append-inner>
                                <v-chip color="primary">
                                    {{computedDispositivosSelecionadosOnCreate}} itens
                                </v-chip>
                            </template>
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="12" v-if="!selected.id">
                        <v-textarea v-model="selected.obs" placeholder="Obs" hide-details rows="2"></v-textarea>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="12"  align="center" xl="8" xxl="6">
                <span v-if="!!selected.id">
                    <v-btn color="success"
                        v-if="$verify.has_perm('change_circulacao', false)"
                        :loading="StateRecursosLoading === `update-circulacao-${selected.id}`"
                        @click="saveItem(selected)">Alterar</v-btn>
                </span>
                <span v-else>
                    <v-btn color="success" v-if="$verify.has_perm('add_circulacao', false)"
                        :loading="StateRecursosLoading === 'create-circulacao'"
                        @click="saveItem(selected)">Adicionar Novo</v-btn>
                </span>
                <span>
                    <v-btn color="warning" v-if="!!selected.id" @click="resetSelected"
                        >Limpar</v-btn>
                </span>
            </v-col>
        </v-row>

        <v-divider class="my-4 mx-1"></v-divider>

        <!-- Filtros e Agrupamentos -->
        <v-row>
            <v-col cols="12">
                <v-sheet>
                    <v-row>
                        <v-col cols="12" sm="6" md="6" xl="6" xxl="3">
                            <v-text-field
                                v-model="search"
                                label="Pesquisar..."
                                placeholder="Identificador, Nº Série, Local, Equipamento..."
                                clearable
                                hide-details>
                            </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="3" md="3" xl="3" xxl="3">
                            <v-text-field class="mb-1" clearable
                                type="date"
                                v-model="filtros.data_inicio"
                                label="Início"
                                >
                            </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="3" md="3" xl="3" xxl="3">
                            <v-text-field class="mb-1" clearable
                                type="date"
                                v-model="filtros.data_fim"
                                label="Fim"
                                >
                            </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4" xl="3" xxl="3">
                            <v-autocomplete
                                clearable
                                multiple chips
                                label="Agrupar por"
                                :items="[
                                    { id: { key: 'local_object.descricao', order: 'asc' }, label: 'Local' },
                                    { id: { key: 'situacao_object.value', order: 'asc' }, label: 'Situação' },
                                    { id: { key: 'responsavel', order: 'asc' }, label: 'Responsável' },
                                ]"
                                item-value="id"
                                item-title="label"
                                v-model="agrupar_por_local">
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="12" sm="6" md="4" xl="3" xxl="3">
                            <v-autocomplete 
                                clearable
                                multiple chips
                                hide-details
                                label="Filtrar por local"
                                :items="StateRecursosLocais"
                                item-value="id"
                                item-title="descricao"
                                v-model="filtros.local"
                                @blur="getCirculacao"
                                >
                                <template #chip="{ item }">
                                    <v-chip-small variant="flat" tile color="primary">
                                        {{item.raw.descricao}}
                                    </v-chip-small>
                                </template>
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="12" sm="6" md="4" xl="3" xxl="3">
                            <v-autocomplete
                                clearable
                                multiple chips
                                hide-details
                                :loading="StateRecursosLoading == 'get-circulacao-enums'"
                                label="Filtrar por situação"
                                :items="StateRecursosEnumsCirculacao.filter(f=> f.key !== 'TRANSFERIDO')"
                                item-value="key"
                                item-title="value"
                                v-model="filtros.situacao"
                                @blur="getCirculacao"
                                >
                                <template #chip="{ item }">
                                    <v-chip-small variant="flat" tile
                                        :color="item.raw.color">
                                        {{item.raw.value}}
                                    </v-chip-small>

                                </template>
                            </v-autocomplete>
                        </v-col>
                        <v-col cols="12" sm="12" align="center">
                            <v-btn @click="getCirculacao">Filtrar</v-btn>
                        </v-col>
                    </v-row>
                </v-sheet>
            </v-col>
        </v-row>

        <!-- Tabela --> 
        <v-row>
            <v-col cols="12" sm="12">
                <!-- eslint-disable-next-line -->
                <v-data-table v-model:expanded="expanded"
                    :custom-filter="filtroCirculacao"
                    :group-by="agrupar_por_local"
                    show-expand
                    :search="search"
                    :loading="StateRecursosLoading == 'get-circulacao'"
                    :items="StateRecursosCirculacao"
                    item-value="id"
                    :sort-by="[
                        { key: 'descricao', order: 'asc' },
                    ]"
                    :headers="headers"
                    >
                    <template v-slot:loading>
                        <v-skeleton-loader type="table-row@1"></v-skeleton-loader>
                    </template>
                    <template v-slot:expanded-row="{ columns, item }">
                        <tr>
                            <td :colspan="columns.length" class="pa-2">
                                <!-- <div class="text-disabled">
                                    # {{item.id}}
                                </div> -->
                                <div class="text-disabled">
                                    Prev. Devolução {{$verify.formatarData(item.previsao_devolucao)}}
                                </div>
                                <div>Obs: {{item.obs}}</div>
                                <div>
                                    <small class="font-italic">
                                        Liberado por: {{ (item.created_by||{}).first_name }} {{ (item.created_by||{}).last_name }}
                                    </small>
                                </div>
                                <div>
                                    <small class="font-italic">
                                        Baixado por: {{ (item.baixado_por||{}).first_name }} {{ (item.baixado_por||{}).last_name }}
                                    </small>
                                </div>
                                <v-divider class="my-2"></v-divider>
                                <v-alert v-if="$verify.has_perm('add_itemcirculacao', false)"
                                    variant="outlined" color="default"
                                    class="my-1"
                                    icon="mdi-plus" title="Incluir dispositivos"
                                    density="compact">
                                    <div>Adicionar mais dispositivos a esta circulação</div>
                                    <v-row>
                                        <v-col cols="12" sm="12">
                                            <v-autocomplete density="compact"
                                                variant="outlined"
                                                hide-details class="my-1"
                                                chips
                                                :items="computedDispositivosDisponiveis"
                                                v-model="item.incluir"
                                                multiple
                                                item-value="id"
                                                :item-title="i => !!i.identificador ? `${i.identificador} - ${i.equipamento_object.descricao}`: ''"
                                                label="Dispositivos"
                                                placeholder="Selecione para adicionar"
                                                >
                                                <template #append-inner>
                                                    <v-chip color="primary">
                                                        {{(item.incluir||[]).length}} itens
                                                    </v-chip>
                                                </template>
                                                <template #append>
                                                    <v-btn @click="addCirculacaoItem({circulacao: item.id, dispositivos: item.incluir})">
                                                        Incluir
                                                    </v-btn>
                                                </template>
                                            </v-autocomplete>
                                        </v-col>
                                    </v-row>
                                </v-alert>
                                <div v-for="i in item.item_objects" :key="i.id">
                                    <CirculacaoItem @change-item="init" :item="i"/>
                                </div>
                            </td>
                        </tr>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.opcoes="{ item }">
                        <v-chip>
                            <span class="text-subtitle-2">{{item.item_objects.length}}</span>
                        </v-chip>
                        <v-menu top left v-if="itemMenuOptions(item).length"
                            rounded="bl-xl tl-xl tr-sm br-sm" offset-y
                            transition="slide-x-transition">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-chip color="primary" 
                                    v-bind="activatorProps" class="pr-1"
                                    v-if="itemMenuOptions(item).length">
                                    <span v-if="$vuetify.display.mdAndUp">
                                        Opções
                                    </span>
                                    <v-divider vertical class="ml-1"></v-divider>
                                    <v-icon>mdi-menu-down</v-icon>
                                    <loading-jr :propObject="[
                                                                `receber-circulacao-${item.id}`,
                                                                `update-circulacao-${item.id}`,
                                                                `cancelar-circulacao-${item.id}`,
                                                                `transferir-circulacao-${item.id}`
                                                                ].includes(StateRecursosLoading)"
                                        text="Processando Circulação..."
                                    ></loading-jr>
                                </v-chip>
                            </template>
                            <v-list density="compact">
                                <v-list-item v-for="m, mi in itemMenuOptions(item)" :key="mi"
                                    @click="m.do()" >
                                    <v-list-item-title>
                                        <v-icon-small color="grey">{{m.icon}}</v-icon-small>
                                        {{m.label}}
                                    </v-list-item-title>
                                </v-list-item>
                            </v-list>
                            <loading-jr :propObject="StateRecursosLoading == `get-log-circulacao-${item.id}`"
                                text="Carregando Logs de Circulação"/>
                        </v-menu>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.created_at="{ item }">
                        {{$verify.formatarData(item.created_at)}}
                        <v-icon color="error" :title="'Previsão de devolução em atraso desde ' + $verify.formatarData(item.previsao_devolucao)"
                            v-if="new Date(item.previsao_devolucao) < new Date() && item.situacao !== 'FINALIZADO'">mdi-bell-badge</v-icon>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.data_baixa="{ item }">
                        <span v-if="!!item.data_baixa">
                            {{$verify.formatarData(item.data_baixa)}}
                        </span>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.situacao="{ item }">
                        <v-chip-small variant="flat" tile
                            :loading="[
                                        `enable-dispositivos-${item.id}`,
                                        `manutencao-dispositivos-${item.id}`
                                    ].includes(StateRecursosLoading)"
                            :color="item.situacao_object.color">
                            {{item.situacao_object.value}}
                        </v-chip-small>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.identificador="{ item }">
                        <span class="text-overline">
                            {{item.identificador}}
                        </span>
                    </template>
                    
                </v-data-table>
            </v-col>

        </v-row>

        <!-- MODAL DE BAIXA -->
        <modal-jr dialogWidth="50%" :no-actions="true"
            ref="receberCirculacao" toolbar-title="Baixar Circulação">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="receberCirculacao.data_baixa"
                            label="Data da baixa">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="8">
                        <v-textarea v-model="receberCirculacao.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setReceber(receberCirculacao)">Baixar</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- MODAL DE TRANSFERENCIA -->
        <modal-jr dialogWidth="50%" :no-actions="true"
            ref="transferirCirculacao" toolbar-title="Transferir Circulação">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="12">
                        <div>
                            <ComboBoxPessoa
                                class="mb-1"
                                label="Novo Professor/Responsável"
                                ref="formTransferencia"
                                ref-name="formTransferencia"
                                @select-pessoa="onSelectPessoaTransferencia" />
                        </div>
                    </v-col>
                    <v-col cols="12" sm="6" v-if="false">
                        <v-text-field hide-details class="mb-1"
                            v-model="transferirCirculacao.email"
                            label="E-mail">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field hide-details class="mb-1"
                            type="datetime-local"
                            v-model="transferirCirculacao.previsao_devolucao"
                            label="Nova Previsão de Devolução">
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" v-if="false">
                        <v-autocomplete hide-details class="mb-1"
                            :items="StateRecursosLocais"
                            v-model="transferirCirculacao.local"
                            item-value="id"
                            item-title="descricao"
                            label="Local">
                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-textarea v-model="transferirCirculacao.obs" placeholder="Obs" hide-details rows="3" label="Observações"></v-textarea>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <v-btn @click="setTransferir(transferirCirculacao)">Transferir</v-btn>
                    </v-col>
                </v-row>
            </template>
        </modal-jr>

        <!-- LOG CIRCULACAO -->
        <modal-jr ref="modalLogCirculacao" fullscreen dialogWidth="100%">
            <template #activate-slot>
                <!-- <v-btn @click="getLogs(item)" :loading="StateRecursosLoading==`get-log-circulacao-${item.id}`">Logs da circulação</v-btn> -->
                <span></span>
            </template>
            <template #body>
                <ListaPaginada :dataResults="logsCirculacao">
                    <template #body="{ listaitem }">
                        <v-row>
                            <v-col cols="12">
                                {{$verify.formatarData(listaitem.created_at) }}
                                <v-chip-small variant="flat" tile
                                    :color="listaitem.situacao_object.color">
                                    {{listaitem.situacao_object.value}}
                                </v-chip-small>
                                por {{ listaitem.created_by.first_name }} {{ listaitem.created_by.last_name }}
                            </v-col>
                            <v-col cols="12">
                                <div class="font-italic">
                                    Obs: {{listaitem.obs}}
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
import InfraCirculacaoValidate from '@/validations/infraestrutura/formCirculacao'
const formValidation = new InfraCirculacaoValidate()
import { mapGetters, mapActions } from 'vuex';
import CirculacaoItem from './CirculacaoItem.vue';
import ComboBoxPessoa from '../../layouts/partials/ComboBoxPessoa.vue';
import ListaPaginada from '../../layouts/partials/ListaPaginada.vue';
export default {
    components: {
        CirculacaoItem,
        ComboBoxPessoa,
        ListaPaginada
    },
    name: 'CirculacaoComponent',
    data: ()=>({
        headers: [
            { title: 'Situação', align: 'center', sortable: false, value: 'situacao', width:'1' },
            { title: 'Saída', align: 'center', sortable: false, value: 'created_at', width:'100px' },
            { title: 'Local', align: 'start', sortable: false, value: 'local_object.descricao', width:'100px' },
            { title: 'Responsável', align: 'start', sortable: false, value: 'responsavel', width:'auto' },
            { title: 'Baixa', align: 'center', sortable: false, value: 'data_baixa', width:'100px' },
            { title: ' ', align: 'end', sortable: false, value: 'opcoes', width:'auto' },
        ],
        selected: {},
        search: null,
        expanded: null,
        receberCirculacao:{},
        transferirCirculacao:{},
        agrupar_por_local: [],
        filtros: {
            local: [], //filtro circulacao
            situacao: ['ABERTO'], //filtro circulacao
            pesquisa: '',
        },
        logsCirculacao: {}
    }),
    methods: {
        ...mapActions([
            'GetRecursosLocais',
            'GetRecursosDispositivos',
            'GetRecursosCirculacao',
            'GetRecursosEnumsCirculacao',
            'AddRecursosCirculacaoItem',
            'CreateRecursosCirculacao',
            'UpdateRecursosCirculacao',
            'ReceberRecursosCirculacao',
            'CancelarRecursosCirculacao',
            'TransferirRecursosCirculacao',
            'GetRecursosLogCirculacao',
            'DeleteRecursosLogCirculacao'
        ]),
        async removerLogs(item){
            await this.DeleteRecursosLogCirculacao({circulacao: item.id})
        },
        onSelectPessoaTransferencia(p){
            this.transferirCirculacao.responsavel = p.NOME
            this.transferirCirculacao.email = p.EMAIL
        },
        async addCirculacaoItem(item){
            for (let i of item.dispositivos){
                const added = await this.AddRecursosCirculacaoItem({circulacao: item.circulacao, dispositivo: i})
                if(added){
                    this.init()
                }
            }
        },
        async openLogCirculacaoModal(item){
            this.logsCirculacao =await this.GetRecursosLogCirculacao({circulacao: item.id, page_size: 10})
            if(!(this.logsCirculacao.results||[]).length){
                alert('Nenhum log registrado para esta Circulação!')
                return
            }
            this.$refs.modalLogCirculacao.dialog = true
            
        },
        async openReceberModal(item){
            this.$refs.receberCirculacao.dialog = true
            this.receberCirculacao = Object.assign({}, item)
            this.receberCirculacao.data_baixa = new Date().format('YYYY-MM-DD HH:mm')
            this.receberCirculacao.obs = ''
        },
        async openTransferirModal(item){
            this.$refs.transferirCirculacao.dialog = true
            this.transferirCirculacao = Object.assign({}, item)
            this.transferirCirculacao.responsavel = null
            this.transferirCirculacao.previsao_devolucao = new Date().format('YYYY-MM-DD 23:00')
        },
        async setReceber(item){
            if(formValidation.validate_receber(item)){
                const enabled = await this.ReceberRecursosCirculacao(item)
                if (enabled){
                    this.$refs.receberCirculacao.dialog = false
                    this.init()
                }
            }
        },
        async setTransferir(item){
            if(formValidation.validate_transferir(item)){
                const enabled = await this.TransferirRecursosCirculacao(item)
                if (enabled){
                    this.init()
                    this.$refs.transferirCirculacao.dialog = false
                }
            }
        },
        async setCancelar(item){
            const motivo_cancelamento = prompt('Necessário informar uma motivo de cancelamento')
            item.motivo_cancelamento = motivo_cancelamento
            if(formValidation.validate_cancelar(item)){
                const enabled = await this.CancelarRecursosCirculacao(item)
                if (enabled){
                    this.init()
                }
            }
        },
        setEditar(item){
            const selected = Object.assign({}, item)
            selected.previsao_devolucao = new Date(selected.previsao_devolucao).format('YYYY-MM-DD HH:mm')
            this.selected = selected
            // alimentar o combobox em sua estrutura de variavel
            this.$refs.formCirculacao.$refs.formCirculacao.focus()
        },
        resetSelected(){
            const responsavel_dados = Object.assign({}, this.selected)
            const selected = Object.assign({}, {})
            this.selected = selected
            this.selected.previsao_devolucao = new Date().format('YYYY-MM-DD 23:00')
            this.selected.responsavel = responsavel_dados.responsavel
            this.selected.email = responsavel_dados.email
        },
        async saveItem(item){   
            if(this.validateForm(item)){
                if(item.id){
                    const updated = await this.UpdateRecursosCirculacao(item)
                    if(updated){
                        this.init()
                    }
                }else{
                    const created = await this.CreateRecursosCirculacao(item)
                    if(created){
                        this.init()
                    }
                }
            }
        },
        validateForm(item){
            if(!item) return false
            const validate = formValidation.validate(item)
            return validate
        },
        async getCirculacao(){
            this.filtros.pesquisa = this.search
            await this.GetRecursosCirculacao(this.filtros)
        },
        async init(){
            this.resetSelected()
            await this.GetRecursosEnumsCirculacao()
            await this.GetRecursosLocais()
            await this.GetRecursosDispositivos()
            await this.getCirculacao()
        },
        itemMenuOptions(item){
            const menus = [
                { 
                    if: ['ABERTO'].includes(item.situacao) && this.$verify.has_perm('change_circulacao', false),
                    do: () => this.setEditar(item),
                    icon: 'mdi-pencil',
                    label: 'Editar'
                },
                { 
                    if: ['ABERTO'].includes(item.situacao) && this.$verify.has_perm('change_circulacao', false),
                    do: () => this.openReceberModal(item),
                    icon: 'mdi-check',
                    label: 'Baixar Circulação'
                },
                { 
                    if: ['ABERTO'].includes(item.situacao) && this.$verify.has_perm('change_circulacao', false),
                    do: () => this.setCancelar(item),
                    icon: 'mdi-wrench',
                    label: 'Cancelar Circulação'
                },
                { 
                    if: ['ABERTO'].includes(item.situacao) && this.$verify.has_perm('change_circulacao', false),
                    do: () => this.openTransferirModal(item),
                    icon: 'mdi-progress-close',
                    label: 'Transferir Circulação'
                },
                { 
                    if: true,
                    do: () => this.getCirculacao(),
                    icon: 'mdi-refresh',
                    label: 'Atualizar'
                },
                { 
                    if:  this.$verify.has_perm('view_logcirculacao', false),
                    do: () => this.openLogCirculacaoModal(item),
                    icon: 'mdi-refresh',
                    label: 'Logs'
                },
                { 
                    if: this.$verify.has_perm('delete_logcirculacao', false),
                    do: () => this.removerLogs(item),
                    icon: 'mdi-close',
                    label: 'Remoção de Logs'
                }
            ]
            return menus.filter(f=> f.if)
        },
        filtroCirculacao(item, queryText, itemText){
            item // titulo do item ()
            queryText // texto digitado
            itemText // item obj da lista 
            const searchText = (queryText||'').toLowerCase()
            const local = (itemText.raw.local_object.descricao ||'').toLowerCase().indexOf(searchText) !== -1
            const responsavel = (itemText.raw.responsavel||'').toLowerCase().indexOf(searchText) !== -1 
            const item_props = itemText.raw.item_objects.filter(f => {
                const a = f.dispositivo_object.identificador.toLowerCase().indexOf(searchText) !== -1
                const b = f.dispositivo_object.equipamento_object.descricao.toLowerCase().indexOf(searchText) !== -1
                const c = (f.dispositivo_object.serie||'').toLowerCase().indexOf(searchText) !== -1
                return a || b || c
            }).length > 0
            return local || responsavel || item_props
        },
    },
    computed: {
        ...mapGetters([
            'StateRecursosLocais',
            'StateRecursosCirculacao',
            'StateRecursosDispositivos',
            'StateRecursosEnumsCirculacao',
            'StateRecursosLoading'
        ]),
        computedDispositivosSelecionadosOnCreate(){
            return (this.selected.itens_dispositivos || []).length
        },
        computedDispositivosDisponiveis(){
            return this.StateRecursosDispositivos.filter(f => {
                // liberar para AVARIADO e DISPONIVEL
                const disponivel = ['DISPONIVEL', 'AVARIADO'].includes(f.situacao)
                // Liberar apenas com status no inventário e flag marcada com pode_circular
                const permitido_no_inventario = f.status_inventario_object.permite_circular
                return disponivel && permitido_no_inventario

            })
        }
    },
    mounted(){
        this.init()
        this.filtros.data_inicio = new Date().format('YYYY-MM-DD')
        this.filtros.data_fim = new Date().format('YYYY-MM-DD')
    },
}
</script>
<style >
.custom-header-style tbody td {
    font-size: 12px !important;
}
</style>