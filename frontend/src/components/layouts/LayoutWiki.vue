<template>
    <wire-frame-jr>
        <template v-slot:top-main>
            <v-btn v-if="hasBasePerm.value" :to="{ name: 'wiki-base' }" tile>Base</v-btn>
            <v-divider class="my-2"></v-divider>
        </template>
    </wire-frame-jr>
</template>
<script setup>
import { ref, computed } from 'vue';
import  { useRouter } from 'vue-router';
const hasBasePerm = ref(false)
const router = useRouter();
hasBasePerm.value = computed(() => router.resolve({name: 'wiki-base'}).meta.has_perm())
</script>