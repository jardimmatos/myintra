<template>
    <div>
        <v-row>
            <v-col cols="12" sm="5" v-if="$verify.has_perm('add_equipamento', false) || $verify.has_perm('change_equipamento', false)">
                <v-text-field ref="formEquipamento"
                    v-model="selected.descricao" label="Descrição" 
                    :loading="StateRecursosLoading == `update-equipamentos-${selected.id}` || StateRecursosLoading=='create-equipamentos'"
                    @keydown.enter="saveItem(selected)"></v-text-field>
                <span v-if="!!selected.id">
                    <v-btn-small v-if="$verify.has_perm('change_equipamento', false)"
                        @click="saveItem(selected)">Alterar
                    </v-btn-small>
                </span>
                <span v-else>
                    <v-btn-small v-if="$verify.has_perm('add_equipamento', false)"
                        @click="saveItem(selected)">
                        Adicionar Novo
                    </v-btn-small>
                </span>
            </v-col>
            <v-col cols="12" sm="6">
                <v-text-field v-model="search" label="Pesquisar..." hide-details></v-text-field>
                <v-data-table
                    :search="search"
                    :loading="StateRecursosLoading == 'get-equipamentos'"
                    :items="StateRecursosEquipamentos"
                    multi-sort
                    item-value="id"
                    :headers="[
                            { title: 'Equipamento', align: 'start', sortable: false, value: 'descricao', width:'auto'},
                            { title: 'Opções', align: 'start', sortable: false, value: 'opcoes', width:'auto' },
                        ]"
                    >
                    <template v-slot:loading>
                        <v-skeleton-loader type="table-row@3"></v-skeleton-loader>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.opcoes="{ item }">
                        <td>
                            <v-icon color="info" v-if="$verify.has_perm('change_equipamento', false)" @click="onSelectItem(item)">mdi-pencil</v-icon>
                        </td>
                    </template>
                    
                </v-data-table>
            </v-col>

        </v-row>
    
    </div>    
</template>
<script>
import InfraEquipamentoValidate from '@/validations/infraestrutura/formEquipamento'
const formValidation = new InfraEquipamentoValidate()
import { mapGetters, mapActions } from 'vuex';
export default {
    name: 'EquipamentosComponent',
    data: ()=>({
        selected: {},
        search: null
    }),
    methods: {
        ...mapActions(['GetRecursosEquipamentos','CreateRecursosEquipamentos','UpdateRecursosEquipamentos']),
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
                    const updated = await this.UpdateRecursosEquipamentos(item)
                    if(updated){
                        this.resetSelected()
                        this.GetRecursosEquipamentos()
                    }
                }else{
                    const created = await this.CreateRecursosEquipamentos(item)
                    if(created){
                        this.resetSelected()
                        this.GetRecursosEquipamentos()
                    }
                }
                this.$refs.formEquipamento.focus()
            }
        },
        validateForm(item){
            if(!item) return false
            const validate = formValidation.validate(item)
            return validate
        }
    },
    computed: {
        ...mapGetters(['StateRecursosEquipamentos','StateRecursosLoading'])
    },
    mounted(){
        this.GetRecursosEquipamentos()
    }
    
}
</script>