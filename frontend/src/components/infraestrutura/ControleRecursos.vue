<template>
    <div>
        <span v-for="m, i in menus" :key="i">
            <v-btn-small variant="outlined"  color="secondary"  v-if="m.perm"  :to="m.to">{{m.label}}</v-btn-small>
        </span>
        <v-divider class="my-2"></v-divider>
        <router-view></router-view>
    </div>
</template>
<script>
export default {
    computed: {
        hasLocalPerm(){
            return this.$router.resolve({name: 'recursos-locais'}).meta.has_perm()
        },
        hasStatusDispositivoPerm(){
            return this.$router.resolve({name: 'recursos-status-dispositivos'}).meta.has_perm()
        },
        hasDispositivoPerm(){
            return this.$router.resolve({name: 'recursos-dispositivos'}).meta.has_perm()
        },
        hasEquipamentoPerm(){
            return this.$router.resolve({name: 'recursos-equipamentos'}).meta.has_perm()
        },
        hasCirculacaoPerm(){
            return this.$router.resolve({name: 'recursos-circulacao'}).meta.has_perm()
        },
        menus(){
            return [
               { label: 'Locais', to: { name: 'recursos-locais' }, perm: this.hasLocalPerm },
               { label: 'Equipamentos', to: { name: 'recursos-equipamentos' }, perm: this.hasEquipamentoPerm },
               { label: 'Status Dispositivos', to: { name: 'recursos-status-dispositivos' }, perm: this.hasStatusDispositivoPerm },
               { label: 'Dispositivos', to: { name: 'recursos-dispositivos' }, perm: this.hasDispositivoPerm },
               { label: 'Circulação', to: { name: 'recursos-circulacao' }, perm: this.hasCirculacaoPerm }
           ]

        }
    }
}
</script>
