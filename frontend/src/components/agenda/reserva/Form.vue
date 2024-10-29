<template>
    <div>
        <div v-if="object">
            <v-row>
                <v-col cols="12">
                    <!-- Responsavel -->
                    
                    <div class="mb-2 pl-1 text-subtitle-2">Titular/Solicitante</div>
                    <!-- RESPONSAVEL -->
                    <!-- eslint-disable-next-line -->
                    <v-text-field  v-model="object.responsavel"
                        clearable label="Responsável"
                        messages="Se você está reservando para terceiros, informe aqui o nome do responsável. Caso contrário, basta clicar no botão 'SOU O TITULAR'">
                    </v-text-field>
                    <div class="mt-1">
                        <v-btn-small @click.stop="onClickSouResponsavel"
                            v-show="!object.responsavel">
                            Sou o titular
                        </v-btn-small>
                    </div>
                </v-col>
                <v-divider class="my-2 "></v-divider>
            </v-row>
            <!-- Reserva -->
            <div class="mb-2 pl-2 text-subtitle-2">Reserva</div>
            <v-row >
                <!-- TITULO -->
                <v-col cols="12" sm="12">
                    <!-- eslint-disable-next-line -->
                    <v-text-field  v-model="object.titulo"
                        clearable label="Título"
                        messages="Informe uma descrição para melhor identificação desta reserva">
                    </v-text-field>
                </v-col>
                <!-- ESPACO -->
                <v-col cols="12" sm="7">
                    <!-- eslint-disable-next-line -->
                    <v-autocomplete v-model="object.espaco"
                        label="Espaço"
                        :disabled="StateReservaCreateLoading"
                        :items="StateEspacos.filter(obj => obj.ativo)"
                        :loading="StateEspacoLoading"
                        item-value="id"
                        item-title="descricao"
                        no-data-text="Nenhum Espaço"
                        loading-text="Carregando Espaços..."
                        messages="Espaço a ser utilizado"
                        >
                        <template v-slot:selection="data">
                            <!-- Item quando selecionado -->
                            <span>{{data.item.title}}</span>
                        </template>
                        <template v-slot:item="data">
                            <template v-if="!(typeof(data.item.raw) == 'object')">
                                <v-list-item-title>{{data.item.raw}}</v-list-item-title>
                                {{data.item.raw}}
                            </template>
                            <template v-else>
                                <v-hover v-slot="{ isHovering, props }">
                                    <v-list-item v-bind="{...data.props, ...props }" color="primary">
                                        <v-list-item-title>
                                            <div class="text-caption text-disabled font-weight-medium">
                                                {{data.item.raw.tipo_espaco_object.descricao}}
                                                <span class="pa-3" v-show="!!data.item.raw.instrucoes_espaco && isHovering">
                                                    <helper-jr :text="data.item.raw.instrucoes_espaco" iconColor="warning" />
                                                </span>
                                            </div>
                                        </v-list-item-title>
                                    </v-list-item>
                                </v-hover>
                            </template>
                        </template>
                    </v-autocomplete>
                </v-col>
                <!-- FINALIDADE -->
                <v-col cols="12" sm="5">
                    <!-- eslint-disable-next-line -->
                    <v-autocomplete v-model="object.finalidade"
                        :disabled="StateReservaCreateLoading"
                        label="Finalidade"
                        :items="StateFinalidades"
                        item-value="id"
                        item-title="descricao"
                        :loading="StateFinalidadesLoading"
                        no-data-text="Nenhuma Finalidade"
                        messages="Finalidade da reserva">
                    </v-autocomplete>
                </v-col>
            </v-row>
            <!-- DATA -->
            <div class="my-2 pl-2 text-subtitle-2">Data/Hora</div>
            <v-row>
                <v-col cols="12" sm="4">
                    <!-- eslint-disable-next-line -->
                    <v-text-field v-model="object.date"
                        type="date" hide-details class="input-date"
                        :disabled="StateReservaCreateLoading"
                        label="Data"></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                    <!-- eslint-disable-next-line -->
                    <v-text-field v-model="object.start"
                        type="time" hide-details
                        :disabled="StateReservaCreateLoading"
                        label="Hora início"></v-text-field>
                </v-col>
                <v-col cols="12" sm="4">
                    <!-- eslint-disable-next-line -->
                    <v-text-field v-model="object.end"
                        type="time" hide-details
                        :disabled="StateReservaCreateLoading"
                        label="Hora fim"></v-text-field>
                </v-col>
                <v-col cols="12">
                    <v-row>
                        <v-col cols="12" sm="12" align="center">
                            <!-- eslint-disable-next-line -->
                            <v-chip-small variant="flat" tile color="primary" @click="()=> { object.start = '08:00'; object.end = '12:00'; }"
                                class="mx-1"
                                title="8h - 12h">
                                Manhã
                            </v-chip-small>
                            <!-- eslint-disable-next-line -->
                            <v-chip-small variant="flat" tile color="primary" @click="()=> { object.start = '14:00'; object.end = '18:00'; }"
                                class="mx-1"
                                title="14h - 18h">
                                Tarde
                            </v-chip-small>
                            <!-- eslint-disable-next-line -->
                            <v-chip-small variant="flat" tile color="primary" @click="()=> { object.start = '19:00'; object.end = '22:00'; }"
                                class="mx-1"
                                title="19h - 22h">
                                Noite
                            </v-chip-small>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            <div class="my-2 pl-2 text-subtitle-2">Adicionais</div>
            <v-row>
                <v-col cols="12" sm="12">
                    <!-- eslint-disable-next-line -->
                    <v-textarea  v-model="object.observacao"
                        :loading="StateReservaCreateLoading" hide-details
                        label="Observações" rows="2"></v-textarea>
                    <div>
                        <!-- Observações predefinidas -->
                        <v-chip-group v-model="obs_tags" multiple column>
                            <v-chip-small color="info" :tile="true" link variant="flat"
                                v-for="tag in tags" :key="tag" :text="tag" :value="tag">
                            </v-chip-small>
                        </v-chip-group>
                    </div>
                </v-col>
            </v-row>
            <br>
            <!-- OBS -->
            <!-- <v-text-field type="number"  v-model="object.participants" label="Participantes"></v-text-field>
            <v-file-input v-show="false"
                show-size
                :multiple="false"
                accept="application/pdf, image/png, image/jpeg, image/bmp"
                color="primary"
                 label="Anexos">
                <template v-slot:selection="{ text }">
                    <v-chip small label color="primary">
                        {{ text }}
                        <v-icon small>mdi-file</v-icon>
                    </v-chip>
                </template>
            </v-file-input> -->
        </div>
        <!-- Actions -->
        <v-row class="px-2">
            <v-btn 
                color="warning" elevation="0"
                :loading="StateReservaCreateLoading"
                @click="createAndAddOther(object)"
                title="Salva e reutiliza o preenchimento de todos os campos">
                Salvar e adicionar outro
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn 
                :loading="StateReservaCreateLoading"
                @click="saveNewEvent(object)"
                color="success"
                title="Salva e finaliza o formulário">
                Salvar
            </v-btn>
        </v-row>
    </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import ReservaFormValidation from '../../../validations/forms/formReserva'
// import { bus } from '@/main'
const formValidation = new ReservaFormValidation()
export default {
    name: 'AgendaReservaForm',
    props:{
        object:{
            required: true
        },
    },
    data:()=>({
        sou_resp:false,
        obs_tags: [],
        tags: [
            "Sugestão frequente I", 
            "Sugestão frequente II", 
            "Sugestão frequente III", 
            "Sugestão frequente IV", 
            "Sugestão frequente V",
        ]
    }),
    methods:{
        ...mapActions(['GetAgendaLabsEspacos',
                        'GetAgendaLabsFinalidades',
                        'CreateReserva',
                        // 'UpdateReserva'
                    ]),
        ...mapMutations([]),
        validateForm(item){
            if(!item) return false
            return formValidation.validate(item)
        },
        async createAndAddOther(item){
            if(this.validateForm(item) && !item.id){
                let created = await this.CreateReserva(item)
                if (created){
                    // bus.$emit(`on-reserva-created`, created);
                }
                    // this.$emit('on-create', created)
            }
        },
        async create(item){
            let created = await this.CreateReserva(item)
            if(created){
                // bus.$emit(`on-reserva-created`, created);
                this.$emit('on-create', created)
            }
        },
        async saveNewEvent(item){
            if(this.validateForm(item) && !item.id) await this.create(item)
        },
        onClickSouResponsavel(){
            const own_user = this.StateAuthenticatedUser
            const name = (own_user.first_name + ' ' + own_user.last_name).trim()
            // eslint-disable-next-line
            this.object.responsavel = name
        },
        init(){
            this.GetAgendaLabsFinalidades({page_size:100})
        },
    },
    computed:{
        ...mapGetters([
            'StateEspacos',
            'StateFinalidades',
            'StateAuthenticatedUser',
            'StateEspacoLoading',
            'StateReservaCreateLoading',
            'StateFinalidadesLoading']),
    },
    mounted(){
        this.init()
    },
    watch: {
        obs_tags(value){
            // eslint-disable-next-line
            this.object.observacao = value.join(", ")
        }
        
    }
}
</script>
