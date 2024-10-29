<template>
    <div>
        <v-row class="py-2">
            <v-text-field hide-details
                v-model="search"
                prepend-inner-icon="mdi-filter"
                color="primary"
                label="Pesquisar Usuário" @keyup.enter="getUsuarios"></v-text-field>
        </v-row>
        <v-row>
            <v-autocomplete multiple
                label="Selecione os usuários"
                item-title="first_name"
                item-value="id"
                @update:modelValue="selectUsuarios"
                v-model="selecteds"
                :loading="StateAdminsLoading"
                :items="StateAdmins.filter(i => i.first_name.toLowerCase().indexOf(search.toLowerCase()) !== -1 || i.email.toLowerCase().indexOf(search.toLowerCase()) !== -1)"
                >
                <template v-slot:item="data">
                    <v-list-item-content class="text-left">
                        <v-list-item-title>
                            {{data.item.first_name}} {{data.item.last_name}}
                        </v-list-item-title>
                        <v-list-item-subtitle>
                            {{data.item.email}}
                        </v-list-item-subtitle>
                    </v-list-item-content>
                </template>
            </v-autocomplete>
        </v-row>
    </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    components:{
    },
    data: () => ({
        selecteds:[],
        search:'',
        paginate_usuarios:100,
    }),
    methods:{
        ...mapActions(['GetAdmins']),
        async init(){
            await this.getUsuarios()
        },
        selectUsuarios(){
            this.$emit('on-selected-items',this.selecteds)
        },
        async getUsuarios(){
            await this.GetAdmins({page_size:this.paginate_usuarios, q:this.search})
        },
        // onCopyItem(item){
        //     //click já está em um list-item com @click enviando para o Form
        //     //apenas deletear o id
        //     delete item.id
        //     this.$emit('on-select-item',item)
        //     //item.description = `${item.description} COPY`
        // }
    },
    computed:{
        ...mapGetters(['StateAdminsLoading','StateAdmins']),
    },
    mounted(){
        this.init()
    },
}
</script>