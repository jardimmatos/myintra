<template>
    <div>
      <router-view></router-view>
    </div>
</template>
<script>
import FrontendService from '@/services/frontendService'
import { mapGetters, mapMutations } from 'vuex'
const fes = new FrontendService()

export default {
    name: 'AppView',
    computed:{
        ...mapGetters(['StateAuthenticatedUser', 'StateUser', 'isAuthenticated']),
    },
    methods:{
        // ...mapMutations(['setUserFiliais']),
        ...mapMutations([]),
    },
    mounted(){
        // remover localstorage quando usuário alterar chaves do storage
        fes
        // window.addEventListener('storage', (event) => {
        //     if ([
        //           fes.SESSION_USERNAME, 
        //           fes.SESSION_USER_AUTHENTICATED,
        //           fes.SESSION_TOKEN,
        //           fes.SESSION_REFRESH_TOKEN].includes(event.key)) {
        //         localStorage.removeItem(fes.SESSION_TOKEN)
        //         localStorage.removeItem(fes.SESSION_REFRESH_TOKEN)
        //         localStorage.removeItem(fes.SESSION_USER_AUTHENTICATED)
        //         localStorage.removeItem(fes.SESSION_USERNAME)
        //         window.location.href = '/'
        //     }
        // });
        // Modo escuro de acordo com o ambiente client
        localStorage.setItem('dark',window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
        // utilizado principalmente em Login, para carregamento de contextos do usuário
        // this.setUserFiliais(this.$verify.user_filiais(this.StateAuthenticatedUser))
    }
};
</script>
<style>
/* width */
::-webkit-scrollbar {
  width: 6px;
}
/* Track */
::-webkit-scrollbar-track {
  background: #9c9c9c;
    border-radius: 5px;
}
/* Handle */
::-webkit-scrollbar-thumb {
  background: #3d3d3d;
  border-radius: 0px;
}
/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #2f2442;
}
.v-field--variant-solo{
  box-shadow: none !important;
}
</style>