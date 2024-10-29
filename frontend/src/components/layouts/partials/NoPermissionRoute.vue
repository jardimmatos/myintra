<template>
    <div class="text-center">
        <p class="my-4">
            Você não tem permissão para acessar {{$route.meta.title || 'este Módulo'}}
        </p>
        <v-btn @click="$router.push({ name:'inicio' })">Página Inicial</v-btn>
    </div>
    
</template>

<script>
export default {
    
}
</script>