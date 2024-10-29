<template>
    <div>
        <v-container style="max-width: 1200px;">
            <div class="pa-2"><strong>Histórico</strong></div>
            <v-divider class="my-2" :dark="StateDark"></v-divider>
            <v-timeline align-center dense :dark="StateDark" >
                <v-timeline-item small style="padding-bottom:10px"
                    :color="log.reserva_object ? log.reserva_object.status_color_classname: 'cyan'"
                    v-for="log, i in StateLogsAgenda.slice(0,10)" :key="log.id">
                    <v-card class="elevation-2">
                        <v-card-text class="pa-0">
                            <v-alert color="cyan"
                                class="mb-0"
                                elevation="0"
                                colored-border
                                style="font-size:1.0em"
                                icon="mdi-calendar">
                                <span :style="'color:'+(i >= 5 ? '#777' : '')">
                                    <strong>{{$verify.formatarData(log.log_at)}}</strong> - {{log.log}}
                                </span>
                            </v-alert>
                        </v-card-text>
                    </v-card>
                </v-timeline-item>
            </v-timeline>
        </v-container>
    </div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
// import { bus } from '@/main'
export default {
    created(){
        // bus.$on('refresh-reservas-logs', (value) => {
        //     value
        //     // console.log('bus on reserva logs refreshing', value)
        //     this.GetLogsAgenda()
        // })
    },
    methods:{
        ...mapActions(['GetLogsAgenda'])
    },
    computed:{
        ...mapGetters(['StateLogsAgenda', 'StateDark'])
    },
    mounted(){
        this.GetLogsAgenda()
    },
    unmounted(){
        // bus.$off('refresh-reservas-logs');
    }
}
</script>