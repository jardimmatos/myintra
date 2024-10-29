<template>
    <div class="text-center">
        <v-dialog v-model="dialog" width="500">
            <template v-slot:activator="{ props: activatorProps }">
                <span v-bind="activatorProps">
                    <slot name="buttonaction">
                        <v-btn color="success">
                            Dialog
                        </v-btn>
                    </slot>
                </span>
            </template>
            <v-card>
                <v-card-title class="text-h5">
                    {{header}}
                </v-card-title>
                <v-card-text class="py-8">
                    <div v-html="message"></div>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                <v-btn color="error" text @click="confirm(false)">
                    {{btnCancelLabel}}
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn color="success" text @click="confirm(true)">
                    {{btnConfirmLabel}}
                </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
export default {
    name: 'ConfirmComponent',
    props:{
        header:{
            default:'Confirmar'
        },
        dark:{
            default:false
        },
        message:{
            default: 'Deseja prosseguir com esta ação?'
        },
        btnConfirmLabel:{
            default:'Sim'
        },
        btnCancelLabel:{
            default:'Não'
        },
    },
    data:()=>({
        dialog: false,
    }),
    methods:{
        openModal(){
            this.dialog = true
        },
        closeModal(){
            this.dialog = false
        },
        confirm(value){
            this.$emit('confirm',value)
            this.closeModal()
        }
    }
}
</script>