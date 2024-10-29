<template>
    <div v-if="atendimento">
        <div>
            Adicionar Comentário
        </div>
        <v-divider class="my-2"></v-divider>
        <v-list-item>
            <v-row dense class="pa-1">
                <v-col cols="12" sm="12">
                    <span>
                        <v-text-field 
                            hide-details class="my-1" 
                            v-model="comentario"
                            @keyup.enter="post_comentario({atendimento, comentario})"
                            label="Adicionar comentário">
                            <template v-slot:append>
                                <v-btn icon fab color="primary" :tile="false"
                                    :loading="StateAtendimentoLoading.includes(`adicionar-comentario-atendimento-${atendimento}`)"
                                    :disabled="!comentario"
                                    @click.stop="post_comentario({atendimento, comentario})">
                                    <v-icon small dark>mdi-send</v-icon>
                                </v-btn>
                            </template>
                        </v-text-field>
                    </span>
                </v-col>
            </v-row>
        </v-list-item>

        <div v-if="StateAtendimentoLoading.includes(`listar-comentario-atendimento-${atendimento}`)" class="text-center">
            <v-progress-linear indeterminate height="1" color="primary"></v-progress-linear>
        </div>
        <v-virtual-scroll :height="300" :items="comentarios">
            <template v-slot:default="{ item }">
                <v-list-item class="mb-3">
                    <v-list-item-title>
                        <v-row dense class="pa-1 header-comment">
                            <b class="text-grey">
                                {{item.created_by_object.first_name}} {{item.created_by_object.last_name}}
                            </b>
                            <v-spacer></v-spacer>
                            <span class="text-grey">
                                {{item.get_created_at}}
                            </span>
                        </v-row>
                    </v-list-item-title>
                    <v-list-item-subtitle class="body-comment">
                        {{item.comentario}}
                    </v-list-item-subtitle>
                    <template v-slot:prepend>
                        <v-avatar size="36" color="primary">
                            <span class="">
                                {{(item.created_by_object.first_name || 'DB').slice(0,2).toUpperCase()}}
                            </span>
                        </v-avatar>
                    </template>
                </v-list-item>
            </template>
        </v-virtual-scroll>

    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    props: {
        atendimento: { required: true }
    },
    data: ()=>({
        comentario: null,
        comentarios: []
    }),
    methods: {
        ...mapActions([
            'AdicionarComentarioAtendimento',
            'ListarComentarioAtendimento'
        ]),
        async post_comentario(data){
            if (!data.comentario){
                alert("Por favor, informe um comentário")
                return
            }

            const adicionado = await this.AdicionarComentarioAtendimento(data)
            if (adicionado){
                this.loadComentarios()
                this.comentario = null
            }
        },
        async loadComentarios(){
            if(!this.atendimento) return
            const comentarios = await this.ListarComentarioAtendimento(this.atendimento)
            this.comentarios = comentarios
            return comentarios
        }
    },
    mounted(){
        this.loadComentarios()
    },
    computed: {
        ...mapGetters(['StateAtendimentoLoading'])
    },
    watch: {
        atendimento(){
            this.loadComentarios()
        }
    }
}
</script>
<style scoped>
.v-list-item__prepend{
    align-self: start;
}
.header-comment *{
    font-size: 12px;
}
.body-comment{
    white-space: unset !important;
    font-size: 13px;
    padding: 2px 5px;
    line-height: 1.5;
}
</style>