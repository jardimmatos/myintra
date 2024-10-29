<template>
    <div>
        <!-- Campo Pesquisa -->
        <v-row>
            <v-text-field v-model="search"
                color="primary"
                label="Pesquisa Espaço..."></v-text-field>
        </v-row>

        <v-row>
            <div class="text-caption text-disabled">
                {{StateEspacos.length}} Espaços
            </div>
            <v-spacer></v-spacer>
            <v-chip color="primary" class="my-1"
                :disabled="StateEspacoLoading"
                @click="getEspacos">
                <span v-show="$vuetify.display.mdAndUp">Atualizar</span>
                <v-icon>mdi-refresh</v-icon>
            </v-chip>
        </v-row>
        <v-skeleton-loader v-if="StateEspacoLoading"
            type="list-item-two-line,list-item-two-line, list-item-two-line, list-item-two-line">
        </v-skeleton-loader>

        <v-card class="my-1" variant="outlined"
            v-for="item, espaco_index in computedEspacos"
            :key="espaco_index"
            v-show="!StateEspacoLoading">
            <v-card-text>
                <v-row>
                    <div class="text-subtitle-1 font-weight-medium my-1">
                        <v-icon class="mr-2" :color="item.color">mdi-circle</v-icon>{{item.descricao}}
                        <helper-jr :text="item.instrucoes_espaco"
                            v-if="!!item.instrucoes_espaco"
                            icon-color="warning"/>
                    </div>
                </v-row>
                <v-row>
                    <v-spacer></v-spacer>
                    <v-chip label :color="item.ativo?'success':'error'" class="mx-1">
                        {{ item.ativo ? 'Ativo' : 'Inativo' }}
                    </v-chip>
                    <v-chip label color="grey" class="mx-1" @click="onCopyItem(item)"
                        title="Criar uma cópia do espaço">
                        <v-icon>mdi-content-copy</v-icon>
                    </v-chip>
                    <v-chip label color="info" class="mx-1" @click="onSelectItem(item)"
                        title="Alterar Espaço">
                        <v-icon>mdi-pencil</v-icon>
                    </v-chip>
                </v-row>
            </v-card-text>
        </v-card>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: 'AgendaEspacoList',
    data: () => ({
        search:'',
        filter:{
            active:null,
            order:null
        }
    }),
    methods:{
        ...mapActions(['GetAgendaLabsEspacos','GetAgendaLabsTipoEspacos']),
        async getEspacos(){
            await this.GetAgendaLabsEspacos()
        },
        async getTipoEspaco(){
            await this.GetAgendaLabsTipoEspacos()
        },
        async init(){
            await this.getEspacos()
        },
        onSelectItem(item){
            this.$emit('on-select-item',item)
        },
        onCopyItem(espaco){
            const item = espaco
            delete item.id
            delete item.teams
            this.$emit('on-select-item',item)
        },
    },
    computed:{
        ...mapGetters(['StateEspacoLoading','StateEspacos', 'StateUserFiliais', 'StateDark']),
        computedEspacos(){
            let filtereds = this.StateEspacos
            if (this.search){
                filtereds = filtereds.filter(i => (i.descricao||'').toLowerCase().indexOf((this.search||'').toLowerCase()) !== -1)
            }
            if (this.StateUserFiliais.length > 0){
                filtereds = filtereds.filter(i => (i.filiais_objects.filter(o=> this.StateUserFiliais.includes(o.codtipocurso)).length > 0))
            }
            return filtereds
        }
    },
    mounted(){
        this.init()
    },
}
</script>