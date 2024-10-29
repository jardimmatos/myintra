import { createWebHashHistory, createRouter } from 'vue-router';
import LayoutDefault from '@/components/layouts/LayoutDefault';
import AppView from '@/App';
import IndexView from '@/views/Index';

// Atendimento
import LayoutAtendimento from '@/components/layouts/LayoutAtendimento';
import TriagemView from '@/components/atendimento/Triagem';
import AtenderView from '@/components/atendimento/Atender';
// import PainelView from '@/components/atendimento/Painel';

// Repositorio BI
import LayoutRepositorio from '@/components/layouts/LayoutRepositorio';
import RepoBiView from '@/components/repositoriobi/RepoBI';

// Infraestrutura
import LayoutInfra from '@/components/layouts/LayoutInfra';
import MonitorView from '@/components/infraestrutura/Monitor';
import RecursosView from '@/components/infraestrutura/ControleRecursos';
import RecursosLocalUsoView from '@/components/infraestrutura/recursos/LocalUso';
import RecursosEquipamentosView from '@/components/infraestrutura/recursos/Equipamentos';
import RecursosDispositivosView from '@/components/infraestrutura/recursos/Dispositivos';
import RecursosStatusDispositivosView from '@/components/infraestrutura/recursos/StatusDispositivo';
import RecursosCirculacaoView from '@/components/infraestrutura/recursos/Circulacao';

// AgendaLabs
import LayoutAgendaLabs from '@/components/layouts/LayoutAgendaLabs';
import AgendaLabsCalendar from '@/components/agenda/Calendar';
import AgendaEspacosView from '@/components/agenda/espaco/Espaco';

// Wiki
import LayoutWiki from '@/components/layouts/LayoutWiki';
import WikiBase from '@/components/wiki/Wikis';
import WikiItem from '@/components/wiki/WikiItem';

// Else Views
import LoginView from '@/views/Login';
import NotFoundView from '@/views/NotFound';
import store from '@/store/store';
import perm from '@/pugins/permissions';

const transitionEffect = 'fade';

const homePages = {
  path: '/',
  component: LayoutDefault,
  name: 'index',
  redirect: '/home',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    has_perm: () => perm.acesso_livre()
  },

  children: [
    {
      path: 'home',
      name: 'inicio',
      component: IndexView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: perm.configs.appName,
        title:'Página Inicial',
        subtitle: perm.configs.brandName,
        has_perm: () => perm.acesso_livre()
      }
    },
  ]
}

const infraestruturaPages = {
  path: '/infraestrutura/',
  component: LayoutInfra,
  name: 'infraestrutura',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    groupName: 'Infraestrutura',
    title:'Início',
    subtitle: 'Recursos técnicos',
    has_perm: () => perm.has_perm('view_monitorservico') ||
                    perm.has_perm('can_gerenciar_containers')
  },
  children: [
    {
      path: 'monitor',
      name: 'monitors',
      component: MonitorView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Infraestrutura',
        title: 'Monitor',
        subtitle: 'Monitor de serviços',
        has_perm: () => perm.has_perm('view_monitorservico')
      },
    },
    {
      path: 'recursos',
      name: 'recursos',
      component: RecursosView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Infraestrutura',
        title: 'Recursos',
        subtitle: 'Controle de uso de dispositivos',
        has_perm: () => perm.has_perm('view_circulacao', false) ||
                        perm.has_perm('view_dispositivo', false) ||
                        perm.has_perm('view_equipamento', false) ||
                        perm.has_perm('view_localuso', false) ||
                        perm.has_perm('view_statusdispositivo', false)
      },
      children: [
        {
          path: 'locais',
          name: 'recursos-locais',
          component: RecursosLocalUsoView,
          meta: {
            transition: transitionEffect,
            requiredAuth: true,
            groupName: 'Infraestrutura',
            title: 'Locais',
            subtitle: 'Locais de uso de dispositivos',
            has_perm: () => perm.has_perm('view_localuso', false)
          },
        },    
        {
          path: 'equipamentos',
          name: 'recursos-equipamentos',
          component: RecursosEquipamentosView,
          meta: {
            transition: transitionEffect,
            requiredAuth: true,
            groupName: 'Infraestrutura',
            title: 'Equipamentos',
            subtitle: 'Equipamentos de uso',
            has_perm: () => perm.has_perm('view_equipamento', false)
          },
        },    
        {
          path: 'dispositivos',
          name: 'recursos-dispositivos',
          component: RecursosDispositivosView,
          meta: {
            transition: transitionEffect,
            requiredAuth: true,
            groupName: 'Infraestrutura',
            title: 'Dispositivos',
            subtitle: 'Identificação de dispositivos',
            has_perm: () => perm.has_perm('view_dispositivo', false)
          },
        },    
        {
          path: 'status-dispositivos',
          name: 'recursos-status-dispositivos',
          component: RecursosStatusDispositivosView,
          meta: {
            transition: transitionEffect,
            requiredAuth: true,
            groupName: 'Infraestrutura',
            title: 'Status Dispositivos',
            subtitle: 'Status de dispositivos no inventário',
            has_perm: () => perm.has_perm('view_statusdispositivo', false)
          },
        },    
        {
          path: 'circulacao',
          name: 'recursos-circulacao',
          component: RecursosCirculacaoView,
          meta: {
            transition: transitionEffect,
            requiredAuth: true,
            groupName: 'Infraestrutura',
            title: 'Circulação',
            subtitle: 'Dispositivos em circulação',
            has_perm: () => perm.has_perm('view_circulacao', false)
          },
        },    
      ]
    },
  ]
}
const agendaLabsPages = {
  path: '/agendalabs/',
  component: LayoutAgendaLabs,
  name: 'agendalabs',
  redirect: '/agendalabs/reservas/',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    groupName: 'Agenda Labs',
    has_perm: () => true
  },
  children: [
    {
      path: 'reservas/',
      name: 'agenda-reservas',
      component: AgendaLabsCalendar,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Agenda Labs',
        title: 'Agendamentos',
        subtitle: 'Sistema de Reserva de Espaços',
        has_perm: () => perm.pode_acessar_agendalabs()
      }
    },
    {
      path: 'espacos/',
      name: 'agenda-espacos',
      component: AgendaEspacosView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Agenda Labs',
        title: 'Espaços',
        subtitle: 'Gestão de Espaços',
        has_perm: () => perm.pode_gerenciar_espacos()
      }
    },
  ]
}
const atendimentoPages = {
  path: '/atendimentos/',
  component: LayoutAtendimento,
  name: 'atendimentos',
  redirect: '/atendimentos/atende/',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    groupName: 'Atendimento',
    has_perm: () => true
  },
  children: [
    {
      path: 'atende/',
      name: 'atendimentos-atende',
      component: AtenderView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Atendimento',
        title: 'Atender',
        subtitle: 'Área de Atendimento',
        has_perm: () => perm.is_atendente()
      }
    },
    {
      path: 'triagem/',
      name: 'atendimentos-triagem',
      component: TriagemView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Atendimento',
        title: 'Triagem',
        subtitle: 'Triagem de Senhas de atendimento',
        has_perm: () => perm.is_atendente()
      }
    },
  ]
}
const repositorioBIPages = {
  path: '/bi/',
  component: LayoutRepositorio,
  name: 'bi',
  redirect: '/bi/repositorio/',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    groupName: 'Fonte de dados',
    title:'Repositório',
    subtitle: 'Repositório de dados',
    has_perm: () => perm.has_bis()
  },
  children: [
    {
      path: 'repositorio/',
      name: 'bi-repositorio',
      component: RepoBiView,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Fonte de dados',
        title: 'Repositório',
        subtitle: 'Repositório de dados',
        has_perm: () => perm.has_bis()
      }
    },
  ]
}
const wikiPages = {
  path: '/wiki/',
  component: LayoutWiki,
  name: 'wiki',
  meta: {
    transition: transitionEffect,
    requiredAuth: true,
    groupName: 'Wiki',
    title:'Documentação',
    subtitle: 'Knowledge Base',
    has_perm: () => perm.has_perm('view_wiki')
  },
  children: [
    {
      path: 'base/',
      name: 'wiki-base',
      component: WikiBase,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Wiki',
        title:'Documentação',
        subtitle: 'Knowledge Base',
        has_perm: () => perm.has_perm('view_wiki')
      }
    },
    {
      path: ':idWiki',
      name: 'wiki-item',
      props: true,
      component: WikiItem,
      meta: {
        transition: transitionEffect,
        requiredAuth: true,
        groupName: 'Wiki',
        title:'Documento',
        subtitle: 'Knowledge Base',
        has_perm: () => perm.has_perm('view_wiki')
      }
    },
  ]
}
const elsePages = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      transition: transitionEffect,
      requiredAuth: false,
      groupName: 'Acesso',
      title: 'Login',
      subtitle: 'Acesso ao Sistema',
      has_perm: () => false
    }
  },
  {
    path: "/not-found",
    name: "page-not-found",
    component: NotFoundView,
    meta: {
      transition: transitionEffect,
      requiredAuth: false,
      groupName: 'Error',
      title: 'Página não encontrada',
      subtitle: 'Página não encontrada',
      has_perm: () => perm.acesso_livre()
    }
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: '/not-found',
    meta: {
      requiredAuth: false,
      has_perm: () => perm.acesso_livre()
    }

  }
]
const routes = [
  {
    path: '/',
    name: 'app',
    component: AppView,
    redirect: '/home/', // Definir Página Inicial
    meta:{
      transition: transitionEffect,
      requiredAuth: true,
      title: 'Início',
      has_perm: () => perm.acesso_livre()
    },
    children: [
      homePages,
      atendimentoPages,
      infraestruturaPages,
      agendaLabsPages,
      repositorioBIPages,
      wikiPages,
    ]
  },
  ...elsePages
]
const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = !!store.getters.isAuthenticated

  // se a rota de "to" requer autenticação
  if (to.meta.requiredAuth){
    // se usuário não está autenticado
    if (!isAuthenticated) {
      next({ name: 'login' })
      return
    }
  }
  
  // Se usuário tiver autenticado e tentar acessar a rota de login, redirecionar para home
  if (isAuthenticated && to.name === 'login'){
    next({name:'index'})
    return
  }
  next()
})

export default router