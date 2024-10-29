<template>
    <div>
        <v-list-item link>
            <v-list-item-avatar>
                <slot name="avatar"></slot>
            </v-list-item-avatar>
            <v-list-item-content>
                <v-list-item-title>
                    <slot name="title"></slot>
                </v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
                <slot name="actions"></slot>
            </v-list-item-action>
        </v-list-item>
    </div>
</template>
<script>
export default {
    props:{
        click:{
            default:()=>{}
        }
    }
}
</script>