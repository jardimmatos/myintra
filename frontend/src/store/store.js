import { createStore } from 'vuex';
//import createPersistedState from "vuex-persistedstate";
import user from "./modules/user/userStore";
import auth from "./modules/auth/authStore";
import base from "./modules/base/baseStore";
import atendimento from "./modules/atendimento/atendimentoStore";
import agendaEspaco from "./modules/agenda/espacoStore";
import agendaTipoEspaco from "../store/modules/agenda/tipoEspacoStore";
import agendaFinalidade from "../store/modules/agenda/finalidadeStore";
import agendaGestor from "../store/modules/agenda/gestorStore";
import agendaAdmins from "../store/modules/agenda/adminStore";
import agendaRegra from './modules/agenda/RegraStore'
import agendaReserva from '../store/modules/agenda/reservaStore'
import agendaLogs from '../store/modules/agenda/logStore'
import repobi from "../store/modules/repobi/repobiStore";
import notificacao from "../store/modules/notificacao/notificacaoStore";
import wiki from "../store/modules/wiki/wikiStore"
import infraestrutura from "../store/modules/infraestrutura/infraStore"
// Create store
export default createStore({
  modules: {
    // App Users
    user,
    auth,
    // Atendimento
    atendimento,
    // App Base
    base,
    // App Agendalabs
    agendaEspaco,
    agendaTipoEspaco,
    agendaFinalidade,
    agendaGestor,
    agendaAdmins,
    agendaRegra,
    agendaReserva,
    agendaLogs,
    // App Repositorio BI
    repobi,
    //Notificacoes
    notificacao,
    // Wiki
    wiki,
    // Infraestrutura
    infraestrutura,

  },
  //plugins: [createPersistedState()],
});