<template>
    <v-app-bar color="navbar" >
        <v-icon @click="$store.commit('setDrawer', !$store.state.base.drawer)">
            {{$store.state.base.drawer ? 'mdi-menu-open' : 'mdi-menu' }}
        </v-icon>
        <span v-show="$vuetify.display.smAndUp">
            <strong>
                {{$verify.configs.appName}}
                <span v-if="$vuetify.display.mdAndUp">{{$verify.configs.brandName}}</span>
            </strong>
        </span>
        <v-spacer></v-spacer>
        <v-chip title='Administração e Configurações'
            @click.stop="admin_url" target="_blank"
            v-show="StateAuthenticatedUser && StateAuthenticatedUser.is_staff">
            <v-icon color="">mdi-cog</v-icon>
        </v-chip>
        <v-chip @click.stop="SetDark" title='Tema claro/escuro'>
            <v-icon>{{StateDarkIcon}}</v-icon>
        </v-chip>
        <v-chip @click.stop="LogOut()" title="Desconectar">
            <v-icon>mdi-exit-to-app</v-icon>
        </v-chip>
    </v-app-bar>
</template>

<script>
import { mapMutations } from 'vuex';
import { mapActions, mapGetters } from 'vuex';
export default {
    name: 'NavbarComponent',
    props: {
      value: {
        default: false,
      },
    },
    data: () => ({
        drawer: null,
    }),
    methods:{
        ...mapActions(['SetDark','LogOut','StateDrawer']),
        ...mapMutations({ setDrawer: 'setDrawer' }),
        admin_url(){
            const token = this.StateAuthenticatedUser.token
            const endpoint = '/auth/api/v1/auth-sso-admin/?'
            const base_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
            const to = base_url + endpoint + 'token='+ token
            // Abre a URL em uma nova guia
            window.open(to, '_blank');
        }
    },
    computed:{
        ...mapGetters(['isAuthenticated','StateAuthenticatedUser','StateBaseURL','StateDarkIcon','StateDark',]),
    },
}
</script>
<style scoped>
.v-app-bar--fixed {
    margin-left: 10px;
    margin-right: 10px;
    border-radius: 0px 0px 5px 5px !important;
}
</style>