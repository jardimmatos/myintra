<template>
    <div>
        <v-row>
            <v-col cols="12" sm="12" md="5" lg="4" xl="3" 
                v-if="$verify.has_perm('change_statusdispositivo', false) || $verify.has_perm('add_statusdispositivo', false)">
                <v-row>
                    <v-col cols="12">
                        <v-text-field v-model="selected.descricao"
                            ref="formStatusDispositivo"
                            hide-details
                            label="Descrição"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <v-autocomplete chip
                            hide-details
                            :items="$verify.lista_cores_hex"
                            item-value="hexa"
                            item-title="name"
                            label="Cor"
                            v-model="selected.color"
                            >   
                            <template #chip="{ item }">
                                <v-chip-small variant="flat" tile :color="item.raw.hexa">
                                    {{item.raw.name}}
                                </v-chip-small>
                            </template>
                            <template v-slot:item="{item, props}">
                                <template v-if="!(typeof(item.raw) == 'object')">
                                </template>
                                <template v-else>
                                    <v-list-item v-bind="props" :style="'background:'+item.raw.hexa">
                                        <v-list-item-subtitle>
                                            <div>
                                                <b class="text-">                                    
                                                    {{item.raw.hexa}} 
                                                </b>
                                            </div>
                                        </v-list-item-subtitle>
                                    </v-list-item>
                                </template>
                            </template>

                        </v-autocomplete>
                    </v-col>
                    <v-col cols="12">
                        <!-- eslint-disable-next-line -->
                        <v-checkbox v-model="selected.permite_circular"
                            hide-details
                            :true-value="true"
                            :false-value="false"
                            label="Permite Circular"></v-checkbox>
                    </v-col>
                    <v-col cols="12" sm="5">
                        <span v-if="!!selected.id">
                            <v-btn-small v-if="$verify.has_perm('change_statusdispositivo', false)"
                                @click="saveItem(selected)">
                                Alterar
                            </v-btn-small>
                        </span>
                        <span>
                            <v-btn-small v-if="$verify.has_perm('add_statusdispositivo', false)"
                                @click="saveItem(selected)">
                                Adicionar Novo
                            </v-btn-small>
                        </span>
                    </v-col>
                </v-row>
            </v-col>
            <v-col cols="12" sm="12" md="6" lg="5" xl="4">
                <v-data-table
                    :headers="[
                        { title: 'Descrição', align: 'start', sortable: false, value: 'descricao', width:'auto'},
                        { title: 'Opções', align: 'end', sortable: false, value: 'opcoes', width:'1' },
                    ]"
                    :items="StateRecursosStatusDispositivos"
                    item-value="id"
                    item-title="descricao"
                    >
                    <!-- eslint-disable-next-line -->
                    <template #item.descricao="{ item }">
                        <v-chip-small variant="flat" tile :color="item.color">
                            {{item.descricao}}
                        </v-chip-small>
                        <span class="mx-2">
                            <helper-jr 
                                :text="item.permite_circular ? 'Pode circular': 'Não pode circular'"
                                :icon="item.permite_circular ? 'mdi-check' : 'mdi-cancel'"
                                :iconColor="item.permite_circular ? 'success' : 'error'"
                            ></helper-jr>
                        </span>
                    </template>
                    <!-- eslint-disable-next-line -->
                    <template #item.opcoes="{ item }">
                        <td>
                            <v-icon color="info" v-if="$verify.has_perm('change_statusdispositivo', false)" @click="onSelectItem(item)">mdi-pencil</v-icon>
                        </td>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </div>    
</template>

<script>
import InfraStatusDispositivoValidate from '@/validations/infraestrutura/formStatusDispositivo'
const formValidation = new InfraStatusDispositivoValidate()
import { mapGetters, mapActions } from 'vuex';
export default {
    data: ()=>({
        selected: {
            descricao: null,
            color: null,
            permite_circular: true
        },
        search: null,
    }),
    methods: {
        ...mapActions([
            'GetRecursosStatusDispositivos',
            'CreateRecursosStatusDispositivos',
            'UpdateRecursosStatusDispositivos',
        ]),
        async saveItem(item){   
            if(this.validateForm(item)){
                if(item.id){
                    const updated = await this.UpdateRecursosStatusDispositivos(item)
                    if(updated){
                        this.GetRecursosStatusDispositivos()
                    }
                }else{
                    const created = await this.CreateRecursosStatusDispositivos(item)
                    if(created){
                        this.GetRecursosStatusDispositivos()
                    }
                }
            }
        },
        onSelectItem(item){
            const selected = Object.assign({}, item)
            this.selected = selected
            this.$refs.formStatusDispositivo.focus()
        },
        validateForm(item){
            if(!item) return false
            const validate = formValidation.validate(item)
            return validate
        },
        async init(){
            await this.GetRecursosStatusDispositivos()
        }
    },
    computed: {
        ...mapGetters([
            'StateRecursosLoading',
            'StateRecursosStatusDispositivos'
        ])
    },
    mounted(){
        this.init()
    }
    
}
</script>