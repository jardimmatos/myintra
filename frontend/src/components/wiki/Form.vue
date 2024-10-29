<template>
    <div>
        <loading-jr :propObject="StateWikiLoading"/>

        <modal-jr 
            :code="modal_code"
            dialog-width="100%"
            :fullscreen="true" toolbar-title="Documentação"
            @on-toggle="onToggle" :ref="modal_code">
            <template v-slot:activate-slot>
                <span></span>
            </template>
            <template v-slot:body>
                <v-row>
                    <v-col cols="12" sm="12">
                        <v-text-field v-model="current.titulo"
                            label="Título da documentação"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-select v-model="current.sistema" :rules="required"
                            :items="StateWikiCategorias"
                            item-title="nome" item-value="id"
                            label="Categoria" :loading="StateWikiCategoriaLoading"/>
                    </v-col>
                    <v-col cols="12">
                        <v-autocomplete v-model="current.membros" multiple :rules="required"
                            :items="membros"
                            :item-title="v => v.id ? `${v.first_name}-${v.last_name} (${v.email})` : 'TODOS'"
                            item-value="id"
                            label="Membros" />
                    </v-col>
                    <v-col cols="12" sm="3">
                        <v-checkbox dense v-model="current.ativo" label="Publicar" hide-details ></v-checkbox>
                    </v-col>
                    <v-col cols="12" sm="12">
                        <div>
                            <quill-editor v-model:content="current.corpo"
                                content-type="html"
                                :toolbar="[
                                    [{ 'font': [] }], 
                                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],   // Headers
                                    ['bold', 'italic', 'underline', 'strike'],   // Inline styles
                                    ['blockquote', 'code-block'],                // Blockquote, Code block
                                    [{ 'color': [] }, { 'background': [] }],     // Text color and background color
                                    [{ 'script': 'sub'}, { 'script': 'super' }], // Subscript/Superscript
                                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],// Lists
                                    [{ 'indent': '-1'}, { 'indent': '+1' }],     // Indent/Outdent
                                    [{ 'align': [] }],                           // Text align
                                    [{ 'direction': 'rtl' }],                    // Text direction (Right to Left)
                                    //['clean'],  
                                    ['link', 'image', 'video'],                  // Insert links, images, videos
                                ]"
                                >
                            </quill-editor>
                        </div>
                    </v-col>
                </v-row>
            </template>
            <template #actions>
                <v-spacer></v-spacer>
                <confirm-jr v-if="$verify.has_perm('delete_wiki') && !!current.id"
                    :message="`Tem certeza que você deseja apagar o wiki <strong>${current.titulo}</strong>`"
                    header="Confirmar Exclusão"
                    @confirm="onConfirmDelete($event, current)"
                    >
                    <template v-slot:buttonaction>
                        <v-btn variant="flat" :disabled="StateWikiLoading" color="error">
                            <v-icon class="mr-1">mdi-delete</v-icon>Remover
                        </v-btn>
                    </template>
                </confirm-jr>
                <!-- CRIAR WIKI -->
                <v-btn v-if="!current.id" variant="flat" @click="saveNewWiki(current)">
                    <v-icon class="mr-1">mdi-content-save</v-icon>Salvar</v-btn>
                <!-- ALTERAR WIKI -->
                <v-btn v-if="!!current.id" variant="flat" @click="saveOnChange(current)">
                    <v-icon class="mr-1">mdi-content-save</v-icon>Alterar</v-btn>
            </template>
        </modal-jr>

        <v-btn v-if="$verify.has_perm('add_wiki')" v-show="item && !item.id"
            @click.stop="wikiForm" elevation="0"
            title="Nova documentação">
            <v-icon>mdi-plus</v-icon> Novo Wiki
        </v-btn>
        <v-btn v-if="($verify.has_perm('change_wiki') || item.created_by == StateAuthenticatedUser.id)"
            v-show="item && item.id" class="ml-1"
            @click.stop="wikiForm" text elevation="0"
            title="Alterar Documentação" color="info">
            <v-icon>mdi-pencil</v-icon> Alterar
        </v-btn>
    </div>
</template>
<script>
// import { bus } from '@/main'
import { mapActions, mapGetters } from 'vuex'
import WikiFormValidation from '@/validations/forms/formWiki'
const formValidation = new WikiFormValidation()
export default {
    name: 'WikiFormComponent',
    components:{
    },
    props:{
        item:{
            required:false,
            type: Object,
        },
    },
    data: () => ({
        modal_code: 'wiki-form',
        loading:false,
        required:[ v => !!v||'Campo Obrigatório' ],
        current:{},
        membros: []
    }),
    mounted(){
        this.init()
    },
    methods:{
        ...mapActions([
            'CreateWiki','UpdateWiki','DeleteWiki', 'GetWikiCategorias', 
            'GetSimpleUsers'
        ]),
        init(){
            this.GetWikiCategorias()
            this.get_membros()
        },
        onConfirmDelete(confirmed, item){
            if(confirmed){
                this.deleteWiki(item)
            }

        },
        async get_membros(){
            try{
                const membros = await this.GetSimpleUsers()
                this.membros=membros
            }catch (err) {
                console.error(err)
                alert('Erro ao carregar membros')
            }
            // this.membros = response.data.results
        },
        wikiForm(){
            const current_object = this.item
            // atribuir a prop item a uma variável data
            this.current = current_object
            // abrir modal-jr
            this.$refs[this.modal_code].dialog = true
            // originalmente, o atributo "mensagem" é do tipo instancia Quill, para o Front será carregado apenas o html em "mensagem" e tratado no serializer
            this.current.corpo = current_object.html
        },
        
        validateForm(item){
            item
            if(!item) return false
            return formValidation.validate(item)
        },
        async create(item){
            item
            let created = await this.CreateWiki(item)
            if (created){
                this.$emit('on-create-wiki', created)
                this.$refs[this.modal_code].dialog = false
            }
        },
        async update(item){
            item
            let updated = await this.UpdateWiki(item)
            if (updated){
                this.$emit('on-update-wiki', updated)
                this.$refs[this.modal_code].dialog = false
            }
        },
        async saveOnChange(item){
            item
            if(this.validateForm(item) && item.id) await this.update(item)
        },
        async saveNewWiki(item){
            item
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        async deleteWiki(item){
            // enviando "false" para data dialog, modal-jr irá fechar o dialog
            // utilizando um nova instancia do Vue (bus), eu posso fechar o dialog do componente modal-jr
            // 'close=-modal' nomeei para capturar no componente modal-jr
            let deleted = await this.DeleteWiki(item)
            if (deleted){
                // fechando via refs ou vis bus (abaixo)
                // this.$refs[this.modal_code].dialog = false
                // bus
                // bus.$emit(`close-modal-${this.modal_code}`, !deleted);
                this.$emit('on-delete-wiki', deleted)
            }
        },
        clear(){
            this.current = {}
        },
        onToggle(value){
            if (!value){
                // ao fechar modal-jr
                this.clear()
            }
        },
    },
    computed:{
        ...mapGetters(['StateWikiLoading', 'StateWikiCategorias', 'StateWikiCategoriaLoading', 'StateAuthenticatedUser']),
        computedItem(){
            return this.item//this.details || this.item
        }
    },
}
</script>