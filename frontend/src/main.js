import { createApp } from 'vue';
import App from '@/App';
import store from '@/store/store';
import router from '@/router';
import globals from '@/pugins/globals';
import VueTheMask from 'vue-the-mask';

const app = createApp(App);

app.use(VueTheMask);

// wire-frame
import WireFrame from '@/components/WireFrame';
app.component('wire-frame-jr', WireFrame);

// clock
import ClockJr from '@/components/layouts/partials/Clock';
app.component('clock-jr', ClockJr);

// footer
import FooterJr from '@/components/layouts/partials/FooterGdb';
app.component('footer-jr', FooterJr);

// drawer
import DrawerJr from '@/components/layouts/partials/Drawer';
app.component('drawer-jr', DrawerJr);

// navbar
import NavbarJr from '@/components/layouts/partials/Navbar';
app.component('navbar-jr', NavbarJr);

// confirm
import ConfirmJr from '@/components/layouts/partials/Confirm.vue';
app.component('confirm-jr', ConfirmJr);

// cardItem
import CardItem from '@/components/layouts/partials/CardItem';
app.component('card-item', CardItem);

// modal
import ModalJr from '@/components/layouts/partials/Modal';
app.component('modal-jr', ModalJr);

// ícone de ajuda
import HelpInfo from '@/components/layouts/partials/HelpInfo';
app.component('helper-jr', HelpInfo);

// websocket
import WebSocket from '@/components/layouts/partials/WebSocket';
app.component('ws-jr', WebSocket);

// loading
import Loading from '@/components/layouts/partials/Loading';
app.component('loading-jr', Loading);

import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import '@/assets/quilleditor.css';

const quillOptions = {
  debug: 'info',
  modules: {
    toolbar: 'full'
  },
  placeholder: 'Conteúdo aqui...',
  readOnly: false,
  theme: 'snow',
}
// set default globalOptions prop
QuillEditor.props.globalOptions.default = () => quillOptions
app.component('quill-editor', QuillEditor)

// App.css
import '@/assets/app.css'
import '@/assets/toast.css'

// Primevue
import 'primeicons/primeicons.css'
import PrimeVue from 'primevue/config';
import primevueOptions from '@/pugins/primevueOptions'
import Button from "primevue/button"
app.component('p-btn', Button)

import ToastService from 'primevue/toastservice';
import Tooltip from 'primevue/tooltip';
import Toast from 'primevue/toast';
app.component('toast-jr', Toast)
app.directive('tooltip', Tooltip);

// Vuetify
import 'vuetify/styles'
import vuetifyOptions from '@/pugins/vuetify';
    
//Calendar Vue-Cal
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
app.component('vue-cal',VueCal) /** Biblioteca de Calendário */


app.use(ToastService) /** Service de notificações toast */
app.use(router) /** Router */
app.use(vuetifyOptions) /** Biblioteca de Frontend UI */
app.use(PrimeVue, primevueOptions) /** Biblioteca de Frontend UI */
app.use(store) /** Biblioteca para gerenciamento de estados */
app.use(globals) /** Variáveis globais */

app.mount('#app')
