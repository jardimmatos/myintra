import { VCalendar } from 'vuetify/labs/VCalendar';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { VBtn } from 'vuetify/components/VBtn';
import { VIcon } from 'vuetify/components/VIcon';
import { VChip } from 'vuetify/components/VChip';

export default createVuetify({
    aliases: {
        VBtnSmall: VBtn,
        VIconSmall: VIcon,
        VChipSmall: VChip,
    },
    defaults: {
        global: {
            ripple: true,
        },
        VAlert: {
            tile: true
        },
        VAppBar: {
            color: 'primary',
            class: "px-3",
            flat: true,
            height: "62",
            VIcon: {
                class: 'mx-1',
            },
            VChip: {
                class:"mx-1",
                variant: 'default'
            }
        },
        VAutocomplete: {
            variant: 'solo',
            density: 'compact',
            color: 'primary',
            tile: true,
            loadingText: "Carregando...",
            noDataText:'Nenhum registro',
            noResultsText: 'Nenhum registro encontrado',
        },
        VBtn: {
            elevation: 0,
            color: 'primary',
            style: 'text-transform: none;',
            tile: true,
        },
        VBtnSmall: {
            elevation: 0,
            color: 'primary',
            style: 'text-transform: none;',
            tile: true,
            size: 'small'
        },
        VCard: {
            tile: true,
        },
        VCombobox: {
            variant: 'solo',
            density: 'compact',
            color: 'primary',
            tile: true,
            loadingText: "Carregando...",
            noDataText:'Nenhum registro',
            noResultsText: 'Nenhum registro encontrado',
        },
        VChip: {
            tile: true,
            variant: 'flat'
        },
        VChipSmall: {
            variant: 'default',
            size: 'small'
        },
        VDataTable: {
            multiSort: true,
            itemsPerPage: 10,
            locale:"pt-br",
            loadingText: "Carregando...",
            noDataText:'Nenhum registro',
            noResultsText: 'Nenhum registro encontrado',
            class: "custom-header-style",
            itemsPerPageText:"Itens por página"
        },
        VIconSmall: {
            size: 'small'
        },
        VFooter: {
            color: "primary",
            app: true
        },
        VNavigationDrawer: {
            floating: false,
            VSheet: {
                class: "pa-2 text-center",
                color: "grey-lighten-4",
                height: "40",
                width: "100%",
                style: "border-radius: 5px",
            },
            VAvatar: {
                class: "ms-2",
                color: "surface-variant",
                variant: "flat",
                rounded: true
            },
            VList: {
                nav: true,
                density: "compact"
            }
        },
        VRow: {
            dense: true,
            class: "px-1",
        },
        VSelect: {
            variant: 'solo',
            density: 'compact',
            color: 'primary',
            tile: true,
            loadingText: "Carregando...",
            noDataText:'Nenhum registro',
            noResultsText: 'Nenhum registro encontrado',
        },
        VTextField: {
            variant: 'solo',
            density: 'compact',
            color: 'primary',
            tile: true,
        },
        VTextarea: {
            variant: 'solo',
            density: 'compact',
            color: 'primary',
            tile: true
        },
    },
    directives,
    components: {
        VCalendar,
        ...components
    },
    theme: {
        // defaultTheme: 'GdbDarkTheme',
        themes: {
            dark: {
                dark: true,
                colors: {
                    "background": "#151515",
                    "surface": "#252525", // Tom menos escuro(mais claro que o background do dark)
                    "primary": '#008097',
                    "surface-bright": "#F3FAFF", // color de parte de elementos (por exemplo, a bolinha de um v-switch)
                    "surface-light": "#ccc", // identificado nas bordas do elemento v-timeline, por exemplo
                    "surface-variant": "#333", // cinza default de elementos sem cores aplicadas
                    "on-surface-variant": "#ddd", // cor da fonte da surface-variant
                    "primary-darken-1": "#007287",
                    "secondary": '#9DB9B9',
                    "secondary-darken-1": "#758E8E",
                    "success": '#66B774',
                    "info": '#2C8279',
                    "warning": '#C56F03',
                    "error": '#C3324A',
                    'footer': '#424242',
                    'navbar': '#424242',
                    'drawer': '#252525',
                    'card': '#252525',
                    'colored-font': '#fff', // utilizado para alternar cores do dark/light para os links de repositorios (somente fonte - sem fundo)
                },
                variables: {
                },
            },
            light: {
                dark: false,
                colors: {
                    "background": "#FFFFFF",
                    "surface": "#f4f4f4",
                    "surface-bright": "#F3FAFF", // color de parte de elementos (por exemplo, a bolinha de um v-switch)
                    "surface-light": "#ccc", // identificado nas bordas do elemento v-timeline, por exemplo
                    "surface-variant": "#ddd", // cinza default de elementos sem cores aplicadas
                    "on-surface-variant": "#555", // cor da fonte da surface-variant
                    'primary-darken-1': '#1F5592',
                    "primary": '#396082',
                    'primary-lighten-1': '#C3CFD9',
                    "secondary": '#46759E',
                    'secondary-darken-1': '#018786',
                    "success": '#66B774',
                    "info": '#14a8af',
                    "warning": '#C56F03',
                    "error": '#C3324A',
                    'footer': '#396082',
                    'navbar': '#396082',
                    'drawer': '#D6D6D6',
                    'card': '#f9f9f9',
                    'colored-font': '#008097', // utilizado para alternar cores do dark/light para os links de repositorios (somente fonte - sem fundo)
                },
                variables: {}
            },
        }
    },
    display: {
      mobileBreakpoint: 'md', /* quando o comportamento do Drawer é exibido sem overlay*/
      thresholds: {
        // xs: 600,
        // sm: 600,
        // md: 900,
        // lg: 1200,
        // xl: 1920,
      },
    },
})
