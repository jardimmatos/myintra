<template>
        <v-dialog scrollable
            v-model="dialog"
            :fullscreen="fullscreen || $vuetify.display.smAndDown"
            :hide-overlay="hideOverlay"
            :transition="transition"
            :width="fullscreen || $vuetify.display.smAndDown ? '100%' : dialogWidth"
            :persistent="persistent"
            :height="fullscreen || $vuetify.display.smAndDown ? '' : height"
            >
            <template v-slot:activator="{ props: activatorProps }">
                <span v-bind="activatorProps">
                    <slot name="activate-slot">
                        Open
                    </slot>
                </span>
            </template>
            <v-card color="background">
                <v-card-title style="padding:0 !important">
                    <v-toolbar dark :color="toolbarColor">
                        <v-toolbar-title><span v-html="toolbarTitle"></span></v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-toolbar-items>
                            <v-btn v-show="!$vuetify.display.smAndDown && dialogWidth!='100%'"
                                @click="fullscreen = !fullscreen" title="Maximizar/Redimensionar">
                                <v-icon>{{fullscreen? 'mdi-fullscreen-exit':'mdi-fullscreen'}}</v-icon>
                            </v-btn>
                            <v-btn @click="dialog = false" title="Fechar">
                                <v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-toolbar-items>
                    </v-toolbar>
                </v-card-title>
                <v-card-text :class="$vuetify.display.smAndUp ? 'pa-2' : 'pa-0'">
                    <div class="px-2 py-3">
                        <slot name="body"></slot>
                    </div>
                </v-card-text>
                <v-card-actions class="px-3" v-if="!noActions">
                    <v-btn v-if="withCancelBtn"
                        color="secondary"
                        @click="dialog = false">
                        {{cancelBtnLabel}}
                    </v-btn>
                    <v-spacer v-if="withCancelBtn"></v-spacer>
                    <slot name="actions"></slot>
                </v-card-actions>
            </v-card>
        </v-dialog>
</template>
<script>
// import { bus } from './../../main'
import { mapGetters } from 'vuex';
export default {
    name: 'ModalComponent',
    props:{
        persistent:{
            default:true
        },
        hideOverlay:{
            default:false
        },
        transition:{
            default:'dialog-bottom-transition'
        },
        toolbarColor:{
            default:'primary'
        },
        toolbarTitle:{
            default:''
        },
        dialogWidth:{
            default: '60%'
        },
        withCancelBtn:{
            default:false
        },
        cancelBtnLabel:{
            default:'Cancelar'
        },
        height:{
            default:''
        },
        // utilizado para mapear o bus do dialog, dessa forma é possível isolar e
        // fechar uma modal referenciada, caso contrário, todas as Modal seriam fechadas
        code:{
            required:false
        },
        noActions:{
            default: false
        }
    },
    data () {
      return {
        dialog: false,
        fullscreen: false
      }
    },
    computed:{
        ...mapGetters(['StateDark'])
    },
    watch:{
        dialog(value){
            this.$emit('on-toggle', value)
        }
    },
    created(){
        // bus.$on(`close-modal-${this.code}`, (value) => {
        //     this.dialog = value
        // })
    },
    unmounted(){
        // bus.$off(`close-modal-${this.code}`);
    }
}
</script>