<template>
    <v-row class="px-2">
        <v-col cols="12" sm="12">
            <span v-if="computedNotificacoes.length == 0" class="title"> Nenhuma notificação</span>
            <span v-else class="title">Notificações</span>
            <v-divider class="my-1"></v-divider>
        </v-col>
        <v-col cols="12" sm="12">
            <v-spacer></v-spacer>
            <!-- Formulário de criação -->
            <Form :item="Object.assign({}, {...model})"
                @on-create-notification="onCreateNotification"/>
        </v-col>
        <v-col cols="12" sm="12" v-if="computedNotificacoes.length > 0">
            <v-hover>
                <template v-slot:default="{ isHovering, props }">
                    <v-carousel v-bind="props"
                        style="height:auto;min-height:100vh; padding-bottom:50px"
                        :show-arrows="isHovering && computedNotificacoes.length > 1"
                        :interval="1000"
                        :cycle="!isHovering"
                        >
                        <v-carousel-item v-for="(item,i) in computedNotificacoes" :key="i">
                            <v-sheet tile>
                                <div class="pa-2 px-4">
                                    <v-card elevation="0" block class="pa-2" >
                                        <v-row>
                                            <div>{{item.titulo}}</div>
                                            <v-spacer></v-spacer>
                                            <!-- Formulário de alteração e exclusão -->
                                            <Form :item="Object.assign({}, item)" v-show="isHovering"
                                                @on-update-notification="onUpdateNotification"
                                                @on-delete-notification="onDeleteNotification"/>
                                        </v-row>
                                        <v-divider class="my-3"></v-divider>
                                        <div class="quill-custom-content">
                                            <div v-html="item.html"></div>
                                        </div>
                                        <div v-if="item.fim" class="text-error" v-show="false">
                                            <v-icon color="grey" :title="$verify.formatarData(item.fim)">mdi-information</v-icon>
                                        </div>
                                    </v-card>
                                </div>
                            </v-sheet>
                        </v-carousel-item>
                    </v-carousel>
                </template>
            </v-hover>
            
        </v-col>
    </v-row>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
// import { bus } from '@/main'
import Form from '@/components/notifications/Form.vue'
export default {
    name: 'NotificationComponent',
    components:{
        Form,
    },
    data: () => ({
        model:{
            titulo:'...',
            mensagem:'...',
            inicio: null,
            fim: null,
        }
    }),
    mounted () {
        this.GetNotificacao()
    },
    created(){
        // bus.$on('refresh-notifications', (value) => {
        //     console.log('bus on notifications refreshing', value)
        // })
    },
    methods: {
        ...mapActions(['GetNotificacao']),
        onUpdateNotification(){
            // Emitir que uma notificação foi alterada
            // bus.$emit(`on-notification-changed`, true);
        },
        onDeleteNotification(){
            // Emitir que uma notificação foi removida
            // bus.$emit(`on-notification-deleted`, true);
        },
        onCreateNotification(){
            // Emitir que uma notificação foi criada
            // bus.$emit(`on-notification-created`, true);
        }
    },
    computed: {
        ...mapGetters(['StateNotificacao', 'StateDark', 'StateNotificacaoLoading', 'StateAuthenticatedUser']),
        computedNotificacoes(){
            return this.StateNotificacao
        }
    },
    unmounted(){
        // bus.$off('refresh-notifications');
    }
  }
</script>
<style >
/* .quill-custom-content img{
    height: 70vh !important;
} */

</style>


