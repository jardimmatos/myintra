<template>
    <div>
        <b-button @click="openModal" squared :variant="`${btnColor}`">{{btnLabel}}</b-button>
        <b-modal v-model="modal" hide-header-close>
            <template #modal-footer>
                <b-button class="m-1" squared @click="confirm(true)">Sim</b-button>
                <b-button class="m-1" squared @click="confirm(false)">Não</b-button>
            </template>
            <template #modal-title>
                <span v-html="title"></span>
            </template>
            <div class="d-block text-center">
                <span v-html="text"></span>
            </div>
        </b-modal>
    </div>
</template>
<script>
export default {
    name:'ModalConfirm',
    props:{
        text:{
            default:'Deseja confirmar?'
        },
        title:{
            default:'Confirmar'
        },
        btnLabel:{
            default:'confirmar'
        },
        btnColor:{
            default:''
        }
    },
    data:()=>{
        return {
            modal:false
        }
    },
    methods:{
        openModal(){
            this.modal = true
        },
        closeModal(){
            this.modal = false
        },
        confirm(value){
            this.$emit('confirm',value)
            this.closeModal()
        }
    }
}
</script>