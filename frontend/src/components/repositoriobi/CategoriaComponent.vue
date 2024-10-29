<template>
  <span>
      <v-expansion-panels density="compact" class="my-1" v-if="node.repos.length || node.filhos.length && (node.filhos.filter(f => f.filhos.length).length || node.filhos.filter(f => f.repos.length).length)">
        <v-expansion-panel elevation="0">
          <v-expansion-panel-title>
            <template v-slot:default="{ expanded }">
              <v-row no-gutters>
                <v-col class="d-flex justify-start" cols="6">
                  <v-icon-small class="mr-2">
                    {{ expanded ? 'mdi-minus' : 'mdi-plus' }}
                  </v-icon-small>
                  <span :class="expanded ? 'font-weight-bold' : ''">
                    {{node.nome}}
                  </span>
                </v-col>
                <v-col class="text-grey" cols="6">
                  <v-fade-transition leave-absolute>
                    <span v-if="expanded">
                      {{node.descricao}}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <div>
              <!-- Component recursivo -->
              <!-- eslint-disable-next-line -->
              <categoria-component v-for="filho in node.filhos.sort(ordenarCategoria)"
                :key="filho.id"
                :node="filho">
              </categoria-component>
            </div>
            <!-- eslint-disable-next-line -->
            <div v-for="bi in node.repos.filter( f => meuRepo(f.membros).length).sort(ordenarRepo)" :key="bi.id">
              <modal-jr :code="'modal_code_'+bi.id"
                  :with-cancel-btn="true"
                  :fullscreen="true"
                  dialog-width="100%"
                  :persistent="false"
                  :toolbar-title="bi.descricao"
                  cancel-btn-label="Fechar"
                  toolbar-color="primary"
                  btn-icon="mdi-delete">
                  <template v-slot:activate-slot>
                      <v-btn-small class="my-1" color="colored-font"
                          variant="text" title="Clique para abrir...">
                          <v-icon>mdi-open-in-new</v-icon> &nbsp;{{bi.categoria.nome}} - {{bi.descricao}}
                      </v-btn-small>
                  </template>
                  <template v-slot:body>
                      <v-icon v-if="StateAuthenticatedUser.is_superuser"
                      color="info" :title="`Visível a: ${bi.membros.map(u => u.username+' - '+u.first_name).join(', ')}`">mdi-account-group</v-icon>
                      <iframe :src="bi.link_bi" style="width: 100%; height: 75vh" class="iframes"
                          allowfullscreen></iframe>
                  </template>
                  <template v-slot:actions>
                  </template>
              </modal-jr>
            </div>
          </v-expansion-panel-text>

        </v-expansion-panel>
      </v-expansion-panels>
  </span>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: 'CategoriaComponent',
  props: {
    node: {
      type: Object,
      required: true
    },
    isRoot: {
      default: false,
    }
  },
  computed:{
    ...mapGetters(['StateAuthenticatedUser']),
    isPai(){
      return !this.node.pai
    }
  },
  methods: {
    meuRepo(membros){
      return membros.filter(m=> {
            const eh_meu = m.id === this.$store.getters.StateAuthenticatedUser.id;
            return eh_meu
      })
    },
    ordenarCategoria(a, b){
        if (a.nome < b.nome) {
            return -1;
        }
        if (a.nome > b.nome) {
            return 1;
        }
        return 0;
    },
    ordenarRepo(a, b){
        if (a.descricao < b.descricao) {
            return -1;
        }
        if (a.descricao > b.descricao) {
            return 1;
        }
        return 0;
    }
  }
}
</script>
<style scoped>
button.v-expansion-panel-title {
  border-left: rgb(var(--v-theme-primary)) 5px solid !important;
}
.v-expansion-panel-title {
    padding: 10px 10px;    
}
.v-expansion-panel-text__wrapper {
    padding: 2px 24px 2px;
}
.v-expansion-panel--active > .v-expansion-panel-title:not(.v-expansion-panel-title--static) {
    min-height: 48px;
}
</style>