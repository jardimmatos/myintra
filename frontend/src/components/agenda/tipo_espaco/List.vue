<template>
    <div>
        <v-row class="">
            <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-filter-variant"
                color="primary"
                label="Filtrar Tipo de espaço"></v-text-field>
        </v-row>
        <v-row class="px-1 py-1">
            {{StateTipoEspaco.length}} Tipos de espaços cadastrados
            <v-spacer></v-spacer>
            <v-btn text title="atualizar" @click="getTipoEspacos" :loading="StateTipoEspacoLoading">
                Atualizar <v-icon>mdi-refresh</v-icon>
            </v-btn>
        </v-row>
        <v-skeleton-loader v-if="StateTipoEspacoLoading"
            type="list-item-two-line,list-item-two-line, list-item-two-line, list-item-two-line">
        </v-skeleton-loader>
        <v-virtual-scroll
            v-show="!StateTipoEspacoLoading"
            :items="StateTipoEspaco.filter(i => i.descricao.toLowerCase().indexOf(search.toLowerCase()) !== -1)"
            :item-height="55"
            height="360"
            style="border-style: solid;border-width: 1px;border-color: #ccc;border-radius: 15px 0 0 15px;">
            <template v-slot:default="{ item }">
                <v-list-item dense class="active ml-4 my-2" link @click="onSelectItem(item)">
                    <v-list-item-title> 
                        <v-menu top left rounded="bl-xl tl-xl tr-sm br-sm" offset-y
                            transition="slide-x-transition">
                            <template v-slot:activator="{ props: activatorProps }">
                                <v-row>
                                    {{item.descricao}}
                                    <v-spacer></v-spacer>
                                    <v-btn-small color="grey" dark v-bind="activatorProps" icon>
                                        <v-icon>mdi-dots-vertical</v-icon>
                                    </v-btn-small>
                                </v-row>
                            </template>
                            <v-list dense>
                                <v-list-item @click="onCopyItem(item)" >
                                        <v-avatar size="32">
                                            <v-icon small color="grey">mdi-content-copy</v-icon>
                                        </v-avatar>
                                    <v-list-item-title>Criar uma cópia</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                    </v-list-item-title>
                </v-list-item>
                <v-divider class="mx-5"></v-divider>
            </template>
        </v-virtual-scroll>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: 'AgendaTipoEspacoList',
    components:{
    },
    data: () => ({
        search:'',
        filter:{
            active:null,
            order:null
        }
    }),
    methods:{
        ...mapActions(['GetAgendaLabsTipoEspacos']),
        async getTipoEspacos(){
            await this.GetAgendaLabsTipoEspacos()
        },
        //async getTipoEspacos(){
        //    await this.GetAgendaLabsTipoEspacos()
        //},
        //async getCorporations(){
        //    await this.ListCorporations()
        //},
        //async getManagers(){
        //    await this.ListManagers()
        //},
        //async getRoles(){
        //    await this.ListRoles()
        //},
        init(){
            this.getTipoEspacos()
        },
        onSelectItem(item){
            this.$emit('on-select-item',item)
        },
        onCopyItem(item){
            //click já está em um list-item com @click enviando para o Form
            //apenas deletear o id
            delete item.id
            this.$emit('on-select-item',item)
            //item.descricao = `${item.descricao} COPY`
        }
    },
    computed:{
        ...mapGetters(['StateTipoEspacoLoading','StateTipoEspaco']),
    },
    mounted(){
        this.init()
    },
}
</script>