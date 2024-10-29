<template>
    <div>
        <v-combobox
            clearable
            :ref="refName"
            :items="pessoas"
            item-value="NOME"
            item-title="NOME"
            hide-details
            @keyup.enter="pesquisarPessoas"
            return-object
            v-model:search="search"
            @update:modelValue="onSelectPessoa"
            :label="label"
            :placeholder="placeholder"
            >
            <template #append>
                <div>
                    <v-btn :disabled="!minCharsSearch"
                        @click="pesquisarPessoas"
                        :loading="loading">
                        <v-icon>mdi-magnify</v-icon>
                        <span v-if="$vuetify.display.mdAndUp">Pessoa</span>
                    </v-btn>
                </div>
            </template>
        </v-combobox>
    </div>
</template>

<script>

import { mapActions } from 'vuex'

export default {
    props: {
        label: {
            required: false,
            default: 'Nome da pessoa'
        },
        placeholder: {
            required: false,
            default: 'Pesquisar'
        },
        refName: {
            required: false,
        },
        loading: {
            required: false,
            default: false
        },
    },
    data: ()=>({
        pessoas:[],
        search:'',
        objeto_pessoa: {
            NOME: '',
            EMAIL: ''
        }
    }),
    methods: {
        ...mapActions([
            'PesquisarPessoasRecursosCirculacao'
        ]),
        async pesquisarPessoas(){
            if(!this.minCharsSearch) return
            const payload = {
                q: this.search
            }
            this.pessoas = await this.PesquisarPessoasRecursosCirculacao(payload)
            try{
                this.$refs[this.refName].focus()
            }catch{
                //
            }
        },
        onSelectPessoa(p){
            if(typeof(p) == 'string'){
                this.objeto_pessoa.NOME = p
            }
            if(typeof(p) == 'object'){
                try{
                    const { NOME, EMAIL} = p
                    this.objeto_pessoa= { NOME, EMAIL}
                }catch{
                    // destruct quando p é null
                }
            }
            this.$emit('select-pessoa', this.objeto_pessoa)
        }
    },
    computed: {
        minCharsSearch(){
            return (this.search||'').length >= 4
        }
    }
}
</script>