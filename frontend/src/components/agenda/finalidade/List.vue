<template>
    <div>
        <v-row class="">
            <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-filter-variant"
                color="primary"
                label="Filtrar Tipo de Sala"></v-text-field>
        </v-row>
        <v-row class="px-1 py-1">
            {{StateRoomTypes.length}} Tipos de salas cadastradas
            <v-spacer></v-spacer>
            <v-btn text title="atualizar" @click="getRoomTypes" :loading="StateLoadingRoomType">
                Atualizar <v-icon>mdi-refresh</v-icon>
            </v-btn>
        </v-row>
        <v-skeleton-loader v-if="StateLoadingRoomType"
            type="list-item-two-line,list-item-two-line, list-item-two-line, list-item-two-line">
        </v-skeleton-loader>
        <v-virtual-scroll
            v-show="!StateLoadingRoomType"
            :items="StateRoomTypes.filter(i => i.description.toLowerCase().indexOf(search.toLowerCase()) !== -1)"
            :item-height="55"
            height="360"
            style="border-style: solid;border-width: 1px;border-color: #ccc;border-radius: 15px 0 0 15px;">
            <template v-slot:default="{ item }">
                <v-list-item dense class="active" link @click="onSelectItem(item)">
                    <v-list-item-content>
                        <v-list-item-title> {{item.description}} </v-list-item-title>
                        <v-list-item-subtitle>
                            <v-chip class="mr-1"
                                :color="item.ignore_roles ? 'success' : 'error'"
                                title="Ignora Restrições" style="padding:5px"
                                >
                                <span>R</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_holidays ? 'success' : 'error'"
                                title="Ignora Feriados" style="padding:5px"
                                >
                                <span>F</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_saturdays ? 'success' : 'error'"
                                title="Ignora regras de bloqueio no sábado" style="padding:5px"
                                >
                                <span>S</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_sundays ? 'success' : 'error'"
                                title="Ignora regras de bloqueio no sábado" style="padding:5px"
                                >
                                <span>D</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_workdays ? 'success' : 'error'"
                                title="Ignora regras de dias úteis" style="padding:5px"
                                >
                                <span>U</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_durations ? 'success' : 'error'"
                                title="Ignora regras de duração mínima e máxima" style="padding:5px"
                                >
                                <span>T</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.ignore_time_conflicts ? 'success' : 'error'"
                                title="Ignora choques de horários" style="padding:5px"
                                >
                                <span>X</span>
                            </v-chip>
                            <v-chip class="mr-1"
                                :color="item.required_approve ? 'success' : 'error'"
                                title="Requer Aprovação" style="padding:5px"
                                >
                                <span>A</span>
                            </v-chip>
                        </v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action style="align-self: center;" class="mr-2">
                        <v-row style="align-items:center">
                            <v-menu top left
                                rounded="bl-xl tl-xl tr-sm br-sm"
                                offset-y
                                transition="slide-x-transition">
                                <template v-slot:activator="{ props: activatorProps }">
                                    <v-btn dark v-bind="activatorProps" icon>
                                        <v-icon>mdi-dots-vertical</v-icon>
                                    </v-btn>
                                </template>
                                <v-list dense>
                                    <v-list-item @click="onCopyItem(item)" >
                                        <v-list-item-avatar>
                                            <v-avatar size="32">
                                                <v-icon small color="grey">mdi-content-copy</v-icon>
                                            </v-avatar>
                                        </v-list-item-avatar>
                                        <v-list-item-title>Criar uma cópia</v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-menu>
                        </v-row>
                        <v-divider></v-divider>
                    </v-list-item-action>
                </v-list-item>
                <v-divider class="mx-5"></v-divider>
            </template>
        </v-virtual-scroll>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
export default {
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
        ...mapActions(['ListRoomTypes']),
        ...mapActions(['verifyToken']),
        async getRoomTypes(){
            await this.ListRoomTypes()
        },
        //async getRoomTypes(){
        //    await this.ListRoomTypes()
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
        async init(){
            let verified = await this.verifyToken()
            if (verified){
                await this.getRoomTypes()
            }
        },
        onSelectItem(item){
            this.$emit('on-select-item',item)
        },
        onCopyItem(item){
            //click já está em um list-item com @click enviando para o Form
            //apenas deletear o id
            delete item.id
            this.$emit('on-select-item',item)
            //item.description = `${item.description} COPY`
        }
    },
    computed:{
        ...mapGetters(['StateLoadingRoomType','StateRoomTypes']),
    },
    mounted(){
        this.init()
    },
}
</script>