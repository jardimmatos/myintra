<template>
    <div>
        <loading-jr :propObject="StateUserBisLoading" text="Carregando links"/>
        
        <div>
            <div dense class="text-center" v-if="!StateUserBis.length">
                Nenhum dashboard disponível
            </div>
            <div v-else>
                <CategoriaComponent
                    v-for="categoria in StateUserBis.filter(r => r.pai == null)"
                    :key="categoria.id" 
                    :node="categoria"
                    @on-select-categoria="selectedCategId = $event"
                    >
                </CategoriaComponent>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import CategoriaComponent from './CategoriaComponent.vue';

export default {
    components:{
        CategoriaComponent
    },
    data:()=>({
        selectedCategId: null
    }),
    methods:{
        ...mapActions(['GetUserBis']),
        onLoadIframe(){
            // alert('loaded')
        },
        biFromCategory(){
            try{
                return this.StateUserBis.find(i => i.id == this.selectedCategId).repos
            }catch{
                return []
            }
        }
    },
    computed:{
        ...mapGetters(['StateUserBis','StateUserBisLoading', 'StateDark', 'StateAuthenticatedUser'])
    },
    mounted(){
        this.GetUserBis()
    }
}
</script>
<style scoped>
.iframes{
    border: none;
}
</style>