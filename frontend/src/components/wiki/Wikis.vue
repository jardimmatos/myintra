<template>
    <span>
        <div>
            <v-row justify="center" class="py-6">
                <h3>Documentações/Tutoriais</h3>
            </v-row>
            <v-row>
                <v-col cols="12" sm="4" md="4" lg="4" class="px-0">
                    <v-text-field v-model="param.q"
                        hide-details label="Pesquisar">
                    </v-text-field>
                </v-col>
                <v-col cols="12" sm="4" md="4" lg="2">
                    <v-select v-model="param.categoria"
                        placeholder="Categoria"
                        hide-details
                        :items="[ ...StateWikiCategorias]"
                        item-title="nome"
                        item-value="id"
                        ></v-select>
                </v-col>
            </v-row>
            <v-row>
                <v-btn @click.prevent="get_wikis" elevation="0" color="primary" small :disabled="!param.categoria && !param.q">
                    <v-icon>mdi-magnify</v-icon> Pesquisar
                </v-btn>
                <v-spacer></v-spacer>
                <FormWiki :item="Object.assign({}, {...model})" @on-create-wiki="onCreateWiki"/>
            </v-row>

            <v-row v-if="computedWikis.length > 0">
                <v-col cols="12" sm="12" md="12" lg="12" class="px-0"
                    v-for="wiki, wi in computedWikis" :key="wi">
                    <v-card :to="{ name:'wiki-item',  params:{ idWiki: wiki.id } }">
                        <v-card-text>
                            <v-row class="py-2">
                                <div class="subtitle-2" v-text="wiki.titulo"></div>
                                <v-spacer></v-spacer>
                            </v-row>
                            <v-divider class="mt-2"></v-divider>
                            <v-row>
                                <small class="text-grey text--darken-1">registrado em: {{$verify.formatarData(wiki.created_at)}}</small>
                                <v-spacer></v-spacer>
                                <small class="text-grey text--darken-1"> por: {{wiki.criado_por}}</small>
                            </v-row>
                            <v-row>
                                <v-chip size="small" color="success" label v-if="wiki.membros_objects.length == 0">
                                    <b>Compartilhado com todos</b>
                                </v-chip>
                                <v-chip size="small" color="success" label v-if="wiki.membros_objects.length > 0 && wiki.ativo">
                                    <b>Compartilhado</b>
                                </v-chip>
                                <v-chip size="small" v-if="!wiki.ativo" label color="warning">
                                    <b>Privado</b>
                                </v-chip>
                                <v-chip size="small" label color="" v-else>
                                    <b>Publicado</b>
                                </v-chip>
                                <v-spacer></v-spacer>
                                <v-chip size="small" label color="info">
                                    <b>{{wiki.sistema_object.nome}}</b>
                                </v-chip>
                            </v-row>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row justify="center" v-else>
                Nenhum resultado
            </v-row>
        </div>
        <loading-jr :dialog="StateWikiCategoriaLoading || StateWikiLoading"/>
    </span>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import FormWiki from './Form.vue'
export default {
    name: 'WikisComponent',
    components:{
        FormWiki
    },
    data:()=>({
        param:{
            categoria: null,
            q: null
        },
        model:{
            titulo:'...',
            sistema: null,
            corpo:'...',
            ativo: true,
            membros: []
        }
    }),
    mounted(){
        this.init()
    },
    methods:{
        ...mapActions([
            'GetWikis',
        ]),
        async init(){
            //await this.GetWikis();
        },
        async get_wikis(){
            const params = this.param
            await this.GetWikis({...params})
        },
        onCreateWiki(){
            this.get_wikis()
        }
    },
    computed:{
        ...mapGetters([
            'StateWikis', 'StateWikiLoading',
            'StateWikiCategorias', 'StateWikiCategoriaLoading',
            'StateDark'
        ]),
        computedWikis(){
            const wikis = Object.values(this.StateWikis)
            if((this.param.q||'')){
                return wikis
                    .filter((i) =>
                        i.titulo.toLowerCase().indexOf((this.param.q||'').toLowerCase()) !== -1 ||
                        i.html.toLowerCase().indexOf((this.param.q||'').toLowerCase()) !== -1 ||
                        i.sistema_object.nome.toLowerCase().indexOf((this.param.q||'').toLowerCase()) !== -1)
            }
            return wikis
        }
    }
}
</script>