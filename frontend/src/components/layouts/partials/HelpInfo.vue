<template>
    <v-tooltip :location="position">
        <template v-slot:activator="{ props: activatorProps }">
            <v-icon
                v-bind="activatorProps"
                :color="iconColor">{{icon}}</v-icon>
        </template>
        <span v-html="text"></span>
    </v-tooltip>
</template>
<script>
export default {
    props:{
        text:{
            default:'?',
            required: true
        },
        position:{
            default:'right',
        },
        icon:{
            default:'mdi-information',
        },
        iconColor:{
            default:'surface-variant',
        }
    },
}
</script>