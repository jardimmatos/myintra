<template>
	<!-- DIALOG LOADING -->
	<v-dialog v-model="dialog" :hide-overlay="false" persistent width="300">
		<v-card color="primary">
			<v-card-text>
				{{text}}
				<v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
			</v-card-text>
		</v-card>
	</v-dialog>
</template>
<script>
export default {
	name: 'LoadingComponent',
	props:{
		propObject:{
			default:false
		},
		text: {
			default: 'Aguarde, carregando...'
		}
	},
	data:()=>({
		dialog: false
	}),
	watch: {
        propObject:{
            handler(value){
                const prop = value
                this.dialog = prop
            }, deep: true
        }
    }
}
</script>
