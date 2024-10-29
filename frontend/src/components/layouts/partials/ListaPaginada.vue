<template>
    <span>
        <loading-jr :propObject="loading" text="Carregando registros..." />

        <slot name="top"></slot>
        <v-row>
            <div>
                <v-btn-small color="secondary" elevation="0"
                    @click.prevent="carregarMais(settingResults.next)"
                    v-if="settingResults && settingResults.next">
                    <v-icon small>mdi-arrow-left</v-icon>
                    &nbsp;
                    {{previousLabel}}
                </v-btn-small>
            </div>
            <v-spacer></v-spacer>
            <div>
                <v-btn-small color="secondary" elevation="0"
                    @click.prevent="carregarMais(settingResults.previous)"
                    v-if="settingResults && settingResults.previous">
                    {{nextLabel}}
                    &nbsp;
                    <v-icon small>mdi-arrow-right</v-icon>
                </v-btn-small>
            </div>
        </v-row>
        <v-card v-for="l, li in (settingResults.results||[])" :key="li" class="my-1">
            <v-card-text>
                <div>
                    <slot name="body" :listaitem="l">
                        {{l}}
                    </slot>
                </div>
            </v-card-text>
        </v-card>    
        <v-row v-if="(settingResults.results||[]).length > 4">
            <div>
                <v-btn-small color="secondary" elevation="0"
                    @click.prevent="carregarMais(settingResults.next)"
                    v-if="settingResults && settingResults.next">
                    <v-icon small>mdi-arrow-left</v-icon>
                    &nbsp;
                    {{previousLabel}}
                </v-btn-small>
            </div>
            <v-spacer></v-spacer>
            <div>
                <v-btn-small color="secondary" elevation="0"
                    @click.prevent="carregarMais(settingResults.previous)"
                    v-if="settingResults && settingResults.previous">
                    {{nextLabel}}
                    &nbsp;
                    <v-icon small>mdi-arrow-right</v-icon>
                </v-btn-small>
            </div>
        </v-row>
    </span>
</template>

<script>
import ConfigService from '@/services/index'
const configService = new ConfigService()
export default {
    props: {
        dataResults: {
            default: {}
        },
        previousLabel: {
            default: 'Registros mais antigos'
        },
        nextLabel: {
            default: 'Registros mais recentes'
        },
    },
    data:()=>({
        results: {},
        loading: false,
    }),
    methods: {
        async carregarMais(url){
            this.loading = true
            const response = await configService.genericGetRequest(url)
            this.results = response.data
            this.loading = false
        },
    },
    computed: {
        settingResults(){
            if(this.results && (this.results.results||[]).length){
                // Não alterar objeto
            }else{
                // atualizar results
                if(this.dataResults && (this.dataResults.results||[]).length){
                    // eslint-disable-next-line
                    this.results = Object.assign({}, this.dataResults)
                }
            }
            return this.results
        },
    },
}
</script>