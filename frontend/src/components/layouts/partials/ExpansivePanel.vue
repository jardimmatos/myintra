<template>
    <v-expansion-panels density="compact" class="my-1">
        <v-expansion-panel elevation="0">
            <v-expansion-panel-title>
                <template v-slot:default="{ expanded }">
                    <v-row no-gutters>
                        <v-col class="d-flex justify-start" cols="8">
                            <v-icon-small class="mr-2">
                                {{ expanded ? 'mdi-minus' : 'mdi-plus' }}
                            </v-icon-small>
                            <span :class="expanded ? 'font-weight-bold' : ''">
                                <slot name="titulo" />
                            </span>
                        </v-col>
                        <v-col class="text-grey" cols="4">
                            <v-fade-transition leave-absolute>
                                <span v-if="expanded">
                                    <slot name="descricao" />
                                </span>
                            </v-fade-transition>
                        </v-col>
                    </v-row>
                </template>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
                <slot name="conteudo" />
            </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
export default {
    
}
</script>

<style scoped>
button.v-expansion-panel-title {
  border-left: rgb(var(--v-theme-primary)) 5px solid !important;
}
.v-expansion-panel-title {
    padding: 10px 10px;    
}
.v-expansion-panel-text__wrapper {
    padding: 2px 24px 2px;
}
.v-expansion-panel--active > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
    min-height: 48px;
}
</style>