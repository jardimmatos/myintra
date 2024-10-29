<template>
    <v-navigation-drawer v-model="$store.state.base.drawer" color="drawer">
        <div class="d-flex px-0 my-2">
            <v-avatar>
                <span>
                    {{((StateAuthenticatedUser||{}).username||'A').substr(0,1).toUpperCase()}}
                </span>
            </v-avatar>
            <v-sheet color="transparent">
                {{ $verify.truncate((StateAuthenticatedUser||{}).first_name||'', 16) }}
            </v-sheet>
        </div>
        <div class="px-2 my-2">
            <Pesquisa v-show="$vuetify.display.smAndUp"/>
            <v-divider class="my-2"></v-divider>
            <!-- MORE MENU -->
        </div>
        <v-list nav density="compact" >
            <v-list-item v-for="link, index in computed_apps" :key="index"
                :to="{name: link.route_name}"
                @click="selectedItem = index"
                exact-active-class="warning white--text"
                :exact="true"
                :style="'justify-content:center'"
                >
                <template v-slot:prepend>
                    <v-icon>{{link.icon}}</v-icon>
                </template>
                <template v-slot:default>
                    <v-list-item-title
                            :title="link.subtitle">{{link.title}}</v-list-item-title>
                </template>
            </v-list-item>
        </v-list>
        <template v-slot:append>
            <v-list >
                <v-list-item @click="LogOut()">
                    <template v-slot:default>
                        <v-list-item-title :title="'Sair do Sistema'">Desconectar</v-list-item-title>
                    </template>
                    <template #prepend>
                        <v-icon>mdi-exit-to-app</v-icon>
                    </template>
                </v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';
import Pesquisa from './Pesquisa.vue'
export default {
    name: 'SidebarComponent',
    components: {
        Pesquisa
    },
    data: () => ({
      selectedItem:'home'
    }),
    methods:{
        ...mapActions(['LogOut']),
    },
    computed:{
        ...mapGetters(['StateAuthenticatedUser']),
        computed_apps(){
            return this.$verify.menu_options.filter(o => o.perm() == true)
        },
    },
    mounted(){
    }
  }
</script>
<style scoped>
.v-navigation-drawer.v-navigation-drawer--fixed{
    top:10px !important;
    left:10px !important;
    border-radius: 10px;
    height: 97vh !important;
}
.v-list-item__icon:first-child {
    margin-right: 5px !important;
}
</style>