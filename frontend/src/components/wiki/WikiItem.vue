<template>
  <div class="pa-4">
    <v-row>
        <v-btn :to="{ name:'wiki-base'}">Voltar </v-btn>
        <!-- Vincular outra condição para alteração(?) -->
        <FormWiki :item="Object.assign({}, wiki)"
          @on-update-wiki="onUpdateWiki"
          @on-delete-wiki="onDeleteWiki"
          />
    </v-row>
    <v-divider class="my-4"></v-divider>
    <v-card>
      <v-card-text class="wiki-content">
        <div v-if="wiki && wiki.id">
            <div>{{wiki.titulo}}</div>
            <br>
            <div>{{wiki.sistema_object.nome}}</div>
            <small><samp>criado em: {{$verify.formatarData(wiki.created_at)}} </samp></small>
            <br>
            <small><samp>criado por: {{wiki.criado_por}} </samp></small>
            <br><br>
            <span class="quill-custom-content" v-html="wiki.html"></span>
        </div>
        <v-divider class="mt-8"></v-divider>
        <v-row>
          <v-col cols="12">
            <small> Compartilhado com: {{(wiki.membros_objects||[]).length === 0 ? 'Todos' : `${(wiki.membros_objects||[]).length} membros`}} ({{wiki.ativo ? 'Publicado' : 'Privado' }})</small>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <loading-jr :dialog="StateWikiLoading"/>
  </div>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'
import FormWiki from './Form.vue'
export default {
  components:{
    FormWiki
  },
  props:{
    idWiki:{
      required:true
    }
  },
  data:()=>({
    wiki:{}
  }),
  methods:{
    ...mapActions(['GetWiki']),
    async loadWiki(){
        let response = await this.GetWiki(this.idWiki)
        if (response.status == 200){
            this.wiki = response.data
        }else{
            this.wiki = {}
            alert('Documentação não encontrada.')
            this.$router.push({name:'wiki'})
        }
    },
    onUpdateWiki(){
        // Recarregar o wiki após alterar
        this.loadWiki()
    },
    onDeleteWiki(deleted){
        // redirecionar para lista de wikis
        if (deleted)
          this.$router.push({name:'wiki'})
    },
  },
  computed:{
    ...mapGetters(['StateWikiLoading','StateAuthenticatedUser'])
  },
  mounted(){
    this.loadWiki()
  }
}
</script>
<style>
.wiki-content img{
    width: 100%;
    height: auto;
    max-width: 600px;
    max-height: 600px;
    text-align: center !important;
}
</style>