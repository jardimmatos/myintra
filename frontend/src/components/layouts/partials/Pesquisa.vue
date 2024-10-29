<template>
    <span>
        <v-autocomplete
            hide-details
            density="compact"
            variant="solo-filled"
            prepend-inner-icon="mdi-magnify"
            clearable
            flat
            :items="computedSearchables"
            label="Pesquisar..."
            item-title="label"
            return-object
            @update:modelValue="onChangeItem"
            no-data-text="Nenhuma página a encontrar"></v-autocomplete>
    </span>
</template>
<script>
export default {
    name: 'PesquisaMenuComponent',
    methods: {
        onChangeItem(value){
            if(value){
                this.$router.push({ name: value.route_name })
            }
        },
    },
    computed: {
        computedSearchables(){
            const ordenar = (a, b) => {
                if (a.label < b.label) {
                    return -1;
                }
                if (a.label > b.label) {
                    return 1;
                }
                return 0;
            };
            const routes = this.$router.getRoutes()
            const menus = routes.filter(r => {
                    try{ 
                        return r.meta.has_perm() 
                    } catch { 
                        console.error('Rota sem meta.has_perm definido')
                        return false 
                    }
                })
                .filter(f => !f.redirect ) /** rotas que não tenham redirect */
                .filter(f => (f.name !== 'page-not-found')) /** rota diferente de not found */
                .filter(f => (f.children||[]).length === 0) /** rotas que não tenham children */
                .filter(f => f.props.default === false) /** rotas que não tenham props */
                .map(m => ({
                    route_name: m.name, 
                    label: `${m.meta.groupName} - ${m.meta.title||''}`
                }) /* Padronizar lista de opções */
            )
            /** ordenar pelo label */
            menus.sort(ordenar)
            return menus
        }
    },
}
</script>