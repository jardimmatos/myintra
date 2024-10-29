<template>
    <div>
        <!-- Campo Pesquisa -->
        <v-row>
            <v-text-field v-model="search"
                color="primary"
                label="Pesquisar restrições..."></v-text-field>
        </v-row>

        <v-row class="px-1">
            <div class="text-caption text-disabled">
                {{StateRegras.length}} Restrições
            </div>
            <v-spacer></v-spacer>

            <v-chip color="primary" class="my-1"
                :disabled="StateRegraLoading"
                @click="getRoles">
                <span v-show="$vuetify.display.mdAndUp">Atualizar</span>
                <v-icon>mdi-refresh</v-icon>
            </v-chip>
        </v-row>

        <v-skeleton-loader v-if="StateRegraLoading"
            type="list-item-two-line,list-item-two-line, list-item-two-line, list-item-two-line">
        </v-skeleton-loader>
        <v-card class="my-1" elevation="0" variant="outlined"
            v-for="item, role_index in StateRegras.filter(i => i.start_time.indexOf(search) !== -1 || getDayOfWeek(i.week_day).toLowerCase().indexOf(search.toLowerCase()) !== -1 || i.end_time.indexOf(search) !== -1)"
            :key="role_index"
            v-show="!StateRegraLoading">
            <v-card-text>
                <v-row>
                    <div class="text-subtitle-1 font-weight-medium">
                        {{getDayOfWeek(item.week_day)}}
                    </div>
                </v-row>
                <v-row>
                    <div class="text-caption">
                        {{item.start_time}} - {{item.end_time}}
                    </div>
                </v-row>
                <v-row>
                    <v-chip label color="info" class="mx-1" @click="onSelectItem(item)"
                        title="Alterar Restrição">
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
    name: 'AgendaRegraList',
    components:{
    },
    data: () => ({
        search:'',
    }),
    methods:{
        ...mapActions(['GetAgendaLabsRegras']),
        async getRoles(){
            await this.GetAgendaLabsRegras()
        },
        async init(){
            await this.getRoles()
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
        },
        getDayOfWeek(index){
            // Recuperar o nome do dia da semana com base no enum via api
            let enums = this.StateRegraEnums
            if(enums && enums.weekday_enums && enums.weekday_enums.length > 0){
                return enums.weekday_enums[index].weekday_name
            }
            return '-'
        },
    },
    computed:{
        ...mapGetters(['StateRegraLoading','StateRegras','StateRegraEnums']),
    },
    mounted(){
        this.init()
    },
}
</script>