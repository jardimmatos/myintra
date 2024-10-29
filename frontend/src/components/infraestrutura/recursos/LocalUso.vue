<template>
    <div>
        <v-row>
            <v-col cols="12" sm="5" v-if="$verify.has_perm('add_localuso', false) || $verify.has_perm('change_localuso', false)">
                <small class="text-disabled">{{selected.id}}</small>
                <v-text-field ref="formlocal"
                    v-model="selected.descricao" label="Descrição" 
                    :loading="StateRecursosLoading == `update-locais-${selected.id}` || StateRecursosLoading=='create-locais'"
                    @keydown.enter="saveItem(selected)"></v-text-field>
                <span v-if="!!selected.id">
                    <v-btn-small v-if="$verify.has_perm('change_localuso', false)"
                        @click="saveItem(selected)">Alterar
                    </v-btn-small>
                </span>
                <span v-else>
                    <v-btn-small v-if="$verify.has_perm('add_localuso', false)"
                        @click="saveItem(selected)">
                        Adicionar Novo
                    </v-btn-small>
                </span>
            </v-col>
            <v-col cols="12" sm="6">
                <v-text-field v-model="search" label="Pesquisar..." hide-details></v-text-field>
                <v-data-table
                    :search="search"
                    :loading="StateRecursosLoading == 'get-locais'"
                    :items="StateRecursosLocais"
                    multi-sort
                    item-value="id"
                    items-per-page-text="Itens por página"
                    :headers="[
                        { title: 'Local', align: 'start', sortable: false, value: 'descricao', width:'auto'},
                        { title: 'Opções', align: 'start', sortable: false, value: 'opcoes', width:'auto' },
                    ]"
                    >
                    <template v-slot:loading>
                        <v-skeleton-loader type="table-row@3"></v-skeleton-loader>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.opcoes="{ item }">
                        <td>
                            <v-icon color="info" v-if="$verify.has_perm('change_localuso', false)" @click="onSelectItem(item)">mdi-pencil</v-icon>
                        </td>
                    </template>
                    
                </v-data-table>
            </v-col>

        </v-row>
    
    </div>    
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import InfraLocalValidate from '@/validations/infraestrutura/formLocal'
const formValidation = new InfraLocalValidate()
export default {
    data: ()=>({
        selected: {},
        search: null
    }),
    methods: {
        ...mapActions(['GetRecursosLocais','CreateRecursosLocais','UpdateRecursosLocais']),
        onSelectItem(item){
            const selected = Object.assign({}, item)
            this.selected = selected
        },
        resetSelected(){
            const selected = Object.assign({}, {})
            this.selected = selected
        },
        async saveItem(item){   
            if(this.validateForm(item)){
                if(item.id){
                    const updated = await this.UpdateRecursosLocais(item)
                    if(updated){
                        this.resetSelected()
                        this.GetRecursosLocais()
                    }
                }else{
                    const created = await this.CreateRecursosLocais(item)
                    if(created){
                        this.resetSelected()
                        this.GetRecursosLocais()
                    }
                }
                this.$refs.formlocal.focus()
            }
        },
        validateForm(item){
            if(!item) return false
            const validate = formValidation.validate(item)
            return validate
        }
    },
    computed: {
        ...mapGetters(['StateRecursosLocais','StateRecursosLoading'])
    },
    mounted(){
        this.GetRecursosLocais()
    }
    
}
</script>