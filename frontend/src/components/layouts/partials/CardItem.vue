<template>
<div>
    <v-hover v-slot="{ hover }" open-delay="10" close-delay="100">
        <v-card :elevation="hover ? 4 : 2" :class="{ 'on-hover': hover }" :loading="loading" :disabled="disabled">
            <template #progress>
                <slot name="loading">
                    <v-progress-linear color="primary" height="1" indeterminate></v-progress-linear>
                </slot>
            </template>
            <v-card-title>
                <slot name="title"></slot>
            </v-card-title>
            <v-card-text>
                <slot name="text"></slot>
            </v-card-text>
            <v-card-actions>
                <slot name="actions"></slot>
            </v-card-actions>
        </v-card>
    </v-hover>
</div>
</template>
<script>
export default {
    props:{
        loading:{
            default:false,
        },
        disabled:{
            default:false,
        }
    }
}
</script>