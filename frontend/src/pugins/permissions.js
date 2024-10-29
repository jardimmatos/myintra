import FrontendService from '@/services/frontendService';

const fes = new FrontendService()

const acesso_livre = () => true;
const formatarData = (val)=> new Date(val).toLocaleString();
const formatarDataShort = (val)=> {
    const data = val.split('-')
    const y = `${data[0]}`.padStart(4, '0')
    const m = `${data[1]}`.padStart(2, '0')
    const d = `${data[2]}`.padStart(2, '0')
    return `${d}/${m}/${y}`
};
const truncate = (value, size)=> {
    if (!value) return '';

    value = value.toString();
    if (value.length <= size) 
        return value;

    // retornar o texto truncado de acordo com o size especificado
    const truncated_text = value.substr(0, size) + '...';
    return truncated_text;
};
// flags de usuário do padrão model Django --------------
// Valida se usuário é superusuário
const is_superuser = ()=> fes.isSuper();

// Valida se usuário é membro (Django admin)
const is_staff = ()=> fes.isStaff();

// Valida se usuário tem uma permissão específica no DJango
const has_perm = (code, considerar_superusuario=true) =>
    fes.has_perm(code, considerar_superusuario);

// Valida se usuário tem um grupo de perfil específico no DJango
const has_group = (code) => fes.has_group(code);

// Verifica se usuário tem atendente vinculado no App Atendimento
const is_atendente = () => fes.is_atendente();

// Verifica se o usuário de repositório de dados vinculado
const has_bis = () => fes.has_bis();

// AgendaLABS ------------------------------------------
// Permissão específica de acesso ao app de Agendamento
const pode_acessar_agendalabs = (validate=false) =>
    fes.has_perm('can_acessar_agendalabs') || validate ;

// Permissão específica de gerenciamento apenas à gestão dos espaços
const pode_gerenciar_espacos = (validate=false) =>
    fes.has_perm('can_gerenciar_espaco') || validate ;

// Permissão específica de cancelamento apenas à gestão dos espaços
const pode_cancelar_reservas = (validate=false) =>
    fes.has_perm('can_cancelar_reserva') || validate ;

// Permissão específica quanto à aprovação de reservas dos espaços
const pode_aprovar_reservas = (validate=false) =>
    fes.has_perm('can_aprovar_reserva') || validate ;

const functions = {
    // Formata Data no Padrão LocaleString
    formatarData,

    // Formatar
    formatarDataShort,

    // Quebrar o texto conforme o tamanho do texto especificado
    truncate,

    // permissão de acesso livre (que não dependa de uma permissão)
    acesso_livre,

    // usuário é superuser
    is_superuser,

    // usuário é membro
    is_staff,

    // verificação de permissão
    has_perm,

    // verificação de grupo vinculado ao usuário
    has_group,

    // verifica se usuário tem repositorio vinculdo
    has_bis,

    // verifica se usuário é atendente no app Atendimento
    is_atendente,

    // Funções de validação no app Agendamento
    pode_acessar_agendalabs,
    pode_gerenciar_espacos,
    pode_cancelar_reservas,
    pode_aprovar_reservas,

    // MENUS para o Drawer
    menu_options: [
            {
                route_name:'index',
                icon:'mdi-home',
                title:'Página inicial',
                subtitle:'Início',
                perm: () => acesso_livre()
            },
            {
                route_name:'agendalabs',
                icon:'mdi-calendar',
                title:'Agendamentos',
                subtitle:'Agendamento de espaços',
                perm: () => pode_acessar_agendalabs()
            },
            {
                route_name:'atendimentos',
                icon:'mdi-face-agent',
                title:'Atendimento',
                subtitle:'Gerenciamento de Senhas',
                perm: () => is_atendente()
            },
            {
                route_name:'infraestrutura',
                icon:'mdi-application-cog-outline',
                title:'Infraestrutura',
                subtitle:'Recursos Operacionais',
                perm: () => fes.has_perm('view_monitorservico')
            },
                {
                route_name:'bi-repositorio',
                icon:'mdi-puzzle-outline',
                title:'Repositório Dados',
                subtitle:'Repositório de fonte de dados externas',
                perm: () => has_bis()
            },
            {
                route_name:'wiki',
                icon:'mdi-book-search',
                title:'Wiki',
                subtitle:'Base de conhecimento',
                perm: () => fes.has_perm('view_wiki')
            },
    ],
    // função para cálculo de luminescência entre cor de fonte e cor de fundo
    calcula_luminescencia: (hexColor)=>{
        // Auxílio em GPT para calcular Luminescência
        // Remove o símbolo # se estiver presente (quando o hexadecimal é passado com o #)
        if (hexColor.startsWith('#')) {
            hexColor = hexColor.slice(1);
        }
    
        // Converte o valor hexadecimal para valores RGB
        let r = parseInt(hexColor.substr(0, 2), 16);
        let g = parseInt(hexColor.substr(2, 2), 16);
        let b = parseInt(hexColor.substr(4, 2), 16);
    
        // Normaliza os valores RGB
        r /= 255;
        g /= 255;
        b /= 255;
    
        // Calcula a luminância relativa
        let luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    
        // Define a cor do texto com base na luminância
        return luminance > 0.5 ? 'black' : 'white';
    },
    // TODO: Model de Links em banco de dados
    links_uteis: [
        {
            label: 'Link A',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 1'
        },
        {
            label: 'Link B',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 1'
        },
        {
            label: 'Link C',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 1'
        },
        {
            label: 'Link A',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 2'
        },
        {
            label: 'Link B',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 2'
        },
        {
            label: 'Link C',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 2'
        },
        {
            label: 'Link A',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 3'
        },
        {
            label: 'Link B',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 3'
        },
        {
            label: 'Link C',
            link: 'https://meuservidor',
            categoria: 'LinGrupo Links 3'
        },
    ],
    lista_cores_hex:[
        { name: 'Black', hexa: '#000000' },
        { name: 'grey11', hexa: '#1C1C1C' },
        { name: 'grey21', hexa: '#363636' },
        { name: 'grey31', hexa: '#4F4F4F' },
        { name: 'DimGray', hexa: '#696969' },
        { name: 'Gray', hexa: '#808080' },
        { name: 'DarkGray', hexa: '#A9A9A9' },
        { name: 'Silver', hexa: '#C0C0C0' },
        { name: 'LightGrey', hexa: '#D3D3D3' },
        { name: 'Gainsboro', hexa: '#DCDCDC' },
        { name: 'SlateBlue', hexa: '#6A5ACD' },
        { name: 'SlateBlue1', hexa: '#836FFF' },
        { name: 'SlateBlue3', hexa: '#6959CD' },
        { name: 'DarkSlateBlue', hexa: '#483D8B' },
        { name: 'MidnightBlue', hexa: '#191970' },
        { name: 'Navy', hexa: '#000080' },
        { name: 'DarkBlue', hexa: '#00008B' },
        { name: 'MediumBlue', hexa: '#0000CD' },
        { name: 'Blue', hexa: '#0000FF' },
        { name: 'CornflowerBlue', hexa: '#6495ED' },
        { name: 'RoyalBlue', hexa: '#4169E1' },
        { name: 'DodgerBlue', hexa: '#1E90FF' },
        { name: 'DeepSkyBlue', hexa: '#00BFFF' },
        { name: 'LightSkyBlue', hexa: '#87CEFA' },
        { name: 'SkyBlue', hexa: '#87CEEB' },
        { name: 'LightBlue', hexa: '#ADD8E6' },
        { name: 'SteelBlue', hexa: '#4682B4' },
        { name: 'LightSteelBlue', hexa: '#B0C4DE' },
        { name: 'SlateGray', hexa: '#708090' },
        { name: 'LightSlateGray', hexa: '#778899' },
        { name: 'Aqua', hexa: '#00FFFF' },
        { name: 'DarkTurquoise', hexa: '#00CED1' },
        { name: 'Turquoise', hexa: '#40E0D0' },
        { name: 'MediumTurquoise', hexa: '#48D1CC' },
        { name: 'LightSeaGreen', hexa: '#20B2AA' },
        { name: 'DarkCyan', hexa: '#008B8B' },
        { name: 'Teal', hexa: '#008080' },
        { name: 'Aquamarine', hexa: '#7FFFD4' },
        { name: 'MediumAquamarine', hexa: '#66CDAA' },
        { name: 'CadetBlue', hexa: '#5F9EA0' },
        { name: 'DarkSlateGray', hexa: '#2F4F4F' },
        { name: 'MediumSpringGreen', hexa: '#00FA9A' },
        { name: 'SpringGreen', hexa: '#00FF7F' },
        { name: 'PaleGreen', hexa: '#98FB98' },
        { name: 'LightGreen', hexa: '#90EE90' },
        { name: 'DarkSeaGreen', hexa: '#8FBC8F' },
        { name: 'MediumSeaGreen', hexa: '#3CB371' },
        { name: 'SeaGreen', hexa: '#2E8B57' },
        { name: 'DarkGreen', hexa: '#006400' },
        { name: 'Green', hexa: '#008000' },
        { name: 'ForestGreen', hexa: '#228B22' },
        { name: 'LimeGreen', hexa: '#32CD32' },
        { name: 'Lime', hexa: '#00FF00' },
        { name: 'LawnGreen', hexa: '#7CFC00' },
        { name: 'Chartreuse', hexa: '#7FFF00' },
        { name: 'GreenYellow', hexa: '#ADFF2F' },
        { name: 'YellowGreen', hexa: '#9ACD32' },
        { name: 'OliveDrab', hexa: '#6B8E23' },
        { name: 'DarkOliveGreen', hexa: '#556B2F' },
        { name: 'Olive', hexa: '#808000' },
        { name: 'DarkKhaki', hexa: '#BDB76B' },
        { name: 'Goldenrod', hexa: '#DAA520' },
        { name: 'DarkGoldenrod', hexa: '#B8860B' },
        { name: 'SaddleBrown', hexa: '#8B4513' },
        { name: 'Sienna', hexa: '#A0522D' },
        { name: 'RosyBrown', hexa: '#BC8F8F' },
        { name: 'Peru', hexa: '#CD853F' },
        { name: 'Chocolate', hexa: '#D2691E' },
        { name: 'SandyBrown', hexa: '#F4A460' },
        { name: 'NavajoWhite', hexa: '#FFDEAD' },
        { name: 'Wheat', hexa: '#F5DEB3' },
        { name: 'BurlyWood', hexa: '#DEB887' },
        { name: 'Tan', hexa: '#D2B48C' },
        { name: 'MediumSlateBlue', hexa: '#7B68EE' },
        { name: 'MediumPurple', hexa: '#9370DB' },
        { name: 'BlueViolet', hexa: '#8A2BE2' },
        { name: 'Indigo', hexa: '#4B0082' },
        { name: 'DarkViolet', hexa: '#9400D3' },
        { name: 'DarkOrchid', hexa: '#9932CC' },
        { name: 'MediumOrchid', hexa: '#BA55D3' },
        { name: 'Purple', hexa: '#A020F0' },
        { name: 'DarkMagenta', hexa: '#8B008B' },
        { name: 'Fuchsia', hexa: '#FF00FF' },
        { name: 'Violet', hexa: '#EE82EE' },
        { name: 'Orchid', hexa: '#DA70D6' },
        { name: 'Plum', hexa: '#DDA0DD' },
        { name: 'MediumVioletRed', hexa: '#C71585' },
        { name: 'DeepPink', hexa: '#FF1493' },
        { name: 'HotPink', hexa: '#FF69B4' },
        { name: 'PaleVioletRed', hexa: '#DB7093' },
        { name: 'LightPink', hexa: '#FFB6C1' },
        { name: 'Pink', hexa: '#FFC0CB' },
        { name: 'LightCoral', hexa: '#F08080' },
        { name: 'IndianRed', hexa: '#CD5C5C' },
        { name: 'Crimson', hexa: '#DC143C' },
        { name: 'Maroon', hexa: '#800000' },
        { name: 'DarkRed', hexa: '#8B0000' },
        { name: 'FireBrick', hexa: '#B22222' },
        { name: 'Brown', hexa: '#A52A2A' },
        { name: 'Salmon', hexa: '#FA8072' },
        { name: 'DarkSalmon', hexa: '#E9967A' },
        { name: 'LightSalmon', hexa: '#FFA07A' },
        { name: 'Coral', hexa: '#FF7F50' },
        { name: 'Tomato', hexa: '#FF6347' },
        { name: 'Red', hexa: '#FF0000' },
        { name: 'OrangeRed', hexa: '#FF4500' },
        { name: 'DarkOrange', hexa: '#FF8C00' },
        { name: 'Orange', hexa: '#FFA500' },
        { name: 'Gold', hexa: '#FFD700' },
        { name: 'Yellow', hexa: '#FFFF00' },
        { name: 'Khaki', hexa: '#F0E68C' },
        { name: 'AliceBlue', hexa: '#F0F8FF' },
        { name: 'GhostWhite', hexa: '#F8F8FF' },
        { name: 'Snow', hexa: '#FFFAFA' },
        { name: 'Seashell', hexa: '#FFF5EE' },
        { name: 'FloralWhite', hexa: '#FFFAF0' },
        { name: 'WhiteSmoke', hexa: '#F5F5F5' },
        { name: 'Beige', hexa: '#F5F5DC' },
        { name: 'OldLace', hexa: '#FDF5E6' },
        { name: 'Ivory', hexa: '#FFFFF0' },
        { name: 'Linen', hexa: '#FAF0E6' },
        { name: 'Cornsilk', hexa: '#FFF8DC' },
        { name: 'AntiqueWhite', hexa: '#FAEBD7' },
        { name: 'BlanchedAlmond', hexa: '#FFEBCD' },
        { name: 'Bisque', hexa: '#FFE4C4' },
        { name: 'LightYellow', hexa: '#FFFFE0' },
        { name: 'LemonChiffon', hexa: '#FFFACD' },
        { name: 'LightGoldenrodYellow', hexa: '#FAFAD2' },
        { name: 'PapayaWhip', hexa: '#FFEFD5' },
        { name: 'PeachPuff', hexa: '#FFDAB9' },
        { name: 'Moccasin', hexa: '#FFE4B5' },
        { name: 'PaleGoldenrod', hexa: '#EEE8AA' },
        { name: 'MistyRose', hexa: '#FFE4E1' },
        { name: 'LavenderBlush', hexa: '#FFF0F5' },
        { name: 'Lavender', hexa: '#E6E6FA' },
        { name: 'Thistle', hexa: '#D8BFD8' },
        { name: 'Azure', hexa: '#F0FFFF' },
        { name: 'LightCyan', hexa: '#E0FFFF' },
        { name: 'PowderBlue', hexa: '#B0E0E6' },
        { name: 'PaleTurquoise', hexa: '#E0FFFF' },
        { name: 'Honeydew', hexa: '#F0FFF0' },
        { name: 'MintCream', hexa: '#F5FFFA' },
    ],
    configs: {
        appName: 'MyIntranet',
        brandName: 'Augustus Dev',
        address: 'Av. 01, 53A. CEP: 12345-67 - São Luís - MA - Brasil',
        phone: '+55 98 x9999-9999',
    }
};

export default functions