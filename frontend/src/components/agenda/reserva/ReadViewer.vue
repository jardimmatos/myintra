<template>
    <div>
        <div class="text-6 mb-2">{{object.titulo}}</div>
        <v-divider class="my-2"></v-divider>
        <div>
            <div class="text-subtitle-2">Resp.: {{object.responsavel}}</div>
            <div class="my-2">
                <div>Espaço: {{object.espaco.descricao}}</div>
                <div class="text-disabled text-subtitle-2">Finalidade: {{object.finalidade.descricao}}</div>
            </div>
            <div>
                <v-icon>mdi-calendar</v-icon>
                <span class="text-subtitle-2 ml-1">{{object.date_start_end}}</span>
            </div>
            <div v-if="object.observacao" class="my-3 text-disabled">Obs: {{object.observacao}}</div>
            <div v-if="object.participantes">Participantes: {{object.participantes}}</div>
            <div v-if="object.status_descricao">Ressalva: {{object.status_descricao}}</div>
            <v-divider class="my-2"></v-divider>
            <div>
                <div class="text-caption">Criado por: {{object.created_by.username}} - {{object.created_by.first_name}}</div>
                <div class="text-caption">Criado em: {{$verify.formatarData(object.created_at)}}</div>
                <div class="text-caption text-disabled">
                    Última atualização em: {{$verify.formatarData(object.updated_at)}}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import { mapGetters } from 'vuex'
export default {
    props: {
        object: {
            required: true
        }
    },
    computed: {
        // ...mapGetters(['StateSelectedReserva'])
    }
}
</script>
