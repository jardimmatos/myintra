<template>
    <span>
        <v-autocomplete
            label="Filtrar por Espaços"
            multiple chips clearable
            density="comfortable"
            :items="uniqueEspacos"
            item-value="event.espaco_object.id"
            item-title="event.espaco_object.descricao"
            v-model="filter_espacos"
            @update:modelValue="onChangeFilterEspacos"
            messages="Somente as reservas dos Espaços selecionados serão exibidas"
            no-data-text="Sem reservas para filtrar Espaço"       
        >

        </v-autocomplete>
    </span>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'AgendaReservaFiltro',
    props: {
        reservas:{
            default:[],
            required:true
        }
    },
    data: () => ({
        filter_espacos:[]
    }),
    mounted () {
    },
    methods: {
        onChangeFilterEspacos(value){
            this.$emit('filtered-espaco', value)
        },
    },
    computed: {
        ...mapGetters(['StateCalendarReservas']),
        uniqueEspacos(){
            // const espaco_ids = Array.from(new Set(this.reservas.map(i => i.event.espaco_object.id)))
            // const espacos = this.reservas.filter( i => i.event.espaco_object.id)
            // Atributo que será usado para identificar os objetos duplicados
            const atributoComparacao = 'id';

            // Cria um novo conjunto (Set) contendo os valores únicos do atributo de comparação
            const valoresUnicos = new Set(this.StateCalendarReservas.map(obj => obj.event.espaco_object[atributoComparacao]));

            // Filtra a lista de objetos, mantendo apenas os que têm valores únicos para o atributo de comparação
            const uniqueEspacos = this.StateCalendarReservas.filter(i =>
                valoresUnicos.has(i.event.espaco_object[atributoComparacao]) &&
                valoresUnicos.delete(i.event.espaco_object[atributoComparacao])
            )
            return uniqueEspacos

        }
    },
  }
</script>