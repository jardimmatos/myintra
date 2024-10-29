<template>
    <wire-frame-jr>
        <template v-slot:top-main>
            <v-btn v-if="hasMonitorPerm.value" :to="{name: 'monitors'}">Monitor</v-btn>
            <v-btn v-if="hasRecursosPerm.value" :to="{name: 'recursos'}">Controle de Recursos</v-btn>
            <v-divider class="my-2"></v-divider>
        </template>
    </wire-frame-jr>
</template>
<script setup>
import { ref, computed } from 'vue';
import  { useRouter } from 'vue-router';
const hasMonitorPerm = ref(false)
const hasRecursosPerm = ref(false)
const router = useRouter();
hasMonitorPerm.value = computed(() => router.resolve({name: 'monitors'}).meta.has_perm())
hasRecursosPerm.value = computed(() => router.resolve({name: 'recursos'}).meta.has_perm())
</script>