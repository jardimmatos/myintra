<template>
    <wire-frame-jr>
        <template v-slot:top-main>
            <v-btn v-if="hasAtenderPerm.value" :to="{name: 'atendimentos-atende'}">Atender</v-btn>
            <v-btn v-if="hasTriagemPerm.value" :to="{name: 'atendimentos-triagem'}">Triagem</v-btn>
            <v-btn :href="painel_to" target="_blank">Painel</v-btn>
            <v-divider class="my-2"></v-divider>
        </template>
    </wire-frame-jr>
</template>
<script setup>
import { ref, computed } from 'vue';
import  { useRouter } from 'vue-router';
const hasTriagemPerm = ref(false)
const hasAtenderPerm = ref(false)
const router = useRouter();

const painel_endpoint = '/atendimento/painel/'
const painel_url = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV
const painel_to =ref(painel_url + painel_endpoint)
hasTriagemPerm.value = computed(() => router.resolve({name: 'atendimentos-triagem'}).meta.has_perm())
hasAtenderPerm.value = computed(() => router.resolve({name: 'atendimentos-atende'}).meta.has_perm())
</script>