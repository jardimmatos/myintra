<template>
    <div>
        <v-row class="py-2">
            <v-text-field hide-details
                v-model="search"
                prepend-inner-icon="mdi-filter"
                color="primary"
                label="Pesquisar Gestor" @keyup.enter="getGestores"></v-text-field>
        </v-row>
        <v-row>
            <v-autocomplete multiple
                label="Selecione os gestores"
                item-title="first_name"
                item-value="id"
                @update:modelValue="selectGestores"
                v-model="selecteds"
                :loading="StateGestoresLoading"
                :items="StateGestores.filter(i => i.first_name.toLowerCase().indexOf(search.toLowerCase()) !== -1 || i.email.toLowerCase().indexOf(search.toLowerCase()) !== -1)"
                >
                <template v-slot:item="data">
                    <v-list-item-title>
                        {{data.item.first_name}} {{data.item.last_name}}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                        {{data.item.email}}
                    </v-list-item-subtitle>
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
        paginate_gestores:100,
    }),
    methods:{
        ...mapActions(['GetGestores']),
        async init(){
            await this.getGestores()
        },
        selectGestores(){
            this.$emit('on-selected-items',this.selecteds)
        },
        async getGestores(){
            await this.GetGestores({page_size:this.paginate_gestores, q:this.search})
        },
        // saveOnChange(value){
        //     console.log(value)
        // }
        // onCopyItem(item){
        //     //click já está em um list-item com @click enviando para o Form
        //     //apenas deletear o id
        //     delete item.id
        //     this.$emit('on-select-item',item)
        //     //item.description = `${item.description} COPY`
        // }
    },
    computed:{
        ...mapGetters(['StateGestoresLoading','StateGestores', 'StatePaginateGestores']),
    },
    mounted(){
        this.init()
    },
}
</script>