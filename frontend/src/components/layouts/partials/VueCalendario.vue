<template>
    <span>
        <v-row class="my-0" v-if="false">
            <v-tooltip text="Criar nova reserva">
                <template #activator="{ props }">
                    <v-btn-small v-bind="props" @click="customEventCreation"
                        color="success" class="mx-1">
                        <v-icon>mdi-plus</v-icon> RESERVAR...
                    </v-btn-small>
                </template>
            </v-tooltip>
            <v-spacer></v-spacer>
            <v-tooltip text="Atualizar calendário">
                <template #activator="{ props }">
                    <v-btn v-bind="props" icon @click="logEvents('refresh', $event)" color="info" elevation="0" class="mx-1" size="x-small">
                        <v-icon>mdi-refresh</v-icon>
                    </v-btn>
                </template>
            </v-tooltip>
        </v-row>
        <vue-cal
            ref="ref_vuecal"
            class="vuecal--rounded-theme vuecal--custom-theme"
            style="height: 350px;"
            locale="pt-br"
            :active-view="activeView /** tipo de Visualização padrão ao iniciar */"
            :hide-view-selector="false /** oculta os seletor de tipos de visualização no topo do calendario */"
            :xsmall="$vuetify.display.lgAndDown"
            :time="true /** Exibe o horário na view-date */"
            :click-to-navigate="true /** ir para view-date ao clicar uma só vez*/"
            :min-date="minDate"
            :disable-views="disabledViews /** oculta tipos de visualizacao no topo do calendario */"
            :time-from="6 * 60 /** horário da view day inicia as 06h am da view-date*/"
            :time-to="24 * 60 /** horário da view day encerra as 22h pm da view-date*/"
            :time-step="60 /** step a cada x minutos da view-date*/"
            :hide-weekends="false /** oculta fins de semana da view-week*/"
            :show-time-in-cells="false /** exbe a hora nas células de cada dia da view-date. bug no calendário */"
            :disable-days="[
                //new Date().addDays(2).format() /** Dias que ficam bloqueados */
            ]"
            :drag-to-create-event="false"
            :show-week-numbers="false"
            :hide-weekdays="[] /** ocultar os dias da semana 0,1,2,3,4,5,6  */"
            today-button
            :selected-date="selectedDate"
            :events="eventos"
            :on-event-click="onEventClick"
            :min-event-width="0"
            :events-count-on-year-view="false/** contador de eventos na visão de ano */"
            :editable-events="{ title: false, drag: false, resize: false, delete: false, create: false }"
            :weekDays="['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']"
            @ready="logEvents('ready', $event)"
            @view-change="logEvents('view-change', $event)"
            @cell-click="logEvents('cell-click', $event)"
            @cell-dblclick="logEvents('cell-dblclick', $event)"
            @cell-contextmenu="logEvents('cell-contextmenu', $event)"
            @cell-focus="logEvents('cell-focus', $event)"
            @event-focus="logEvents('event-focus', $event)"
            @event-mouse-enter="logEvents('event-mouse-enter', $event)"
            @event-mouse-leave="logEvents('event-mouse-leave', $event)"
            @event-title-change="logEvents('event-title-change', $event)"
            @event-content-change="logEvents('event-content-change', $event)"
            @event-duration-change="logEvents('event-duration-change', $event)"
            @event-drop="logEvents('event-drop', $event)"
            @event-create="logEvents('event-create', $event)"
            @event-drag-create="logEvents('event-drag-create', $event)"
            @event-delete="logEvents('event-delete', $event)"
            >
            <!-- Custom title -->
            <template #title="{ /*title,*/ view }">
                <span v-if="view.id === 'years'">Anos</span>
                <!-- Using Vue Cal injected Date prototypes -->
                <span v-else-if="view.id === 'year'">{{ view.startDate.format('YYYY') }}</span>
                <span v-else-if="view.id === 'month'">{{ view.startDate.format('MMM YYYY') }}</span>
                <span v-else-if="view.id === 'week'">Sem {{ view.startDate.getWeek() }} ({{ view.startDate.format('MMM YYYY') }})</span>
                <span v-else-if="view.id === 'day'">{{ view.startDate.format('ddd D MMM (YYYY)') }}</span>
            </template>
            <!-- Custom cells-->
            <template #cell-content="{ cell, view,  goNarrower }">
                <span :class="view.id" v-if="view.id === 'week'" @click="goNarrower">
                    <span style="font-size: 10px">{{ cell.startDate.format('ddd') }}</span>
                </span>
            </template>
            <!-- Exibição customizada -->
            <template #event="{ event }">
                <slot name="viewer-event" :viewer="event">
                    <div class="vuecal__event-title text-left pa-2">
                        <v-icon :title="event.title" color="primary">mdi-circle</v-icon>
                        &nbsp;<span v-text="event.title" />
                        <div class="text-caption">
                            {{event.start}} - {{event.end}}
                        </div>
                    </div>
                </slot>
                <!-- Or if your events are editable: -->
                <!-- <div class="vuecal__event-title vuecal__event-title--edit"
                    :contenteditable="false"
                    @blur="event.title = $event.target.innerHTML"
                    v-html="event.title" /> -->
            </template>
            <template #today-button>
                <v-tooltip text="Ir para Hoje">
                    <template #activator="{ props }">
                        <v-btn-small v-bind="props" class="mx-1 mb-1"
                            @click="activeView = 'day'">
                            <v-icon>mdi-calendar</v-icon> HOJE
                        </v-btn-small>
                    </template>
                </v-tooltip>
            </template>
            <template  #arrow-prev>
                <v-btn-small icon class="mx-1 mb-1">
                    <v-icon class="cal-nav-icons pi pi-arrow-left"></v-icon>
                </v-btn-small>
            </template>
            <template  #arrow-next>
                <v-btn-small icon class="mx-1 mb-1">
                    <v-icon class="cal-nav-icons pi pi-arrow-right"></v-icon>
                </v-btn-small>
            </template>
        </vue-cal>
    </span>
</template>
<script setup>
    import { ref, defineEmits, computed, onMounted, defineProps } from 'vue';
    const ref_vuecal = ref(null)
    const props = defineProps({
        eventos: {
            default: [],
            required: true
        },
        disabledViews: {
            default: ['years', 'week'],
        },
    });
    props
    /** Atualiza variável que guarda a data selecionada */
    const selectedDate = ref(new Date())
    /** Atualiza variável que guarda o evento selecionada */
    const selectedEvent= ref({})
    /** Inicializa a view do calendário */
    const activeView = ref('month')
    /** Controle de dialog */

    const emits = defineEmits(['log-events']);
    const logEvents = (e, v) => {
        /** Emite geral que envia um objeto com chave e valor do emit */
        emits('log-events', { event: e, value: v });
    };
    const minDate = computed(() => new Date().subtractDays(0));
    const onEventClick = (event, e) => {
        selectedEvent.value = event;
        selectedDate.value = event.start
        /** disparar um emit para controle for deste componente,por ser um componente genérico */
        emits('log-events', { event: 'event-click', value: event });
        // Prevent navigating to narrower view (default vue-cal behavior).
        e.stopPropagation()
    }
    onMounted(() => {
      // Realize ações quando o componente for montado, por exemplo, buscar dados, iniciar animações, etc.
    //   console.log('props on mounted in VueCalendario', props)
    });
    // const customEventCreation = () => {
    //     const dateTime = prompt('Create event on (YYYY-MM-DD HH:mm)', '2024-03-28 13:15')
    //     // Check if date format is correct before creating event.
    //     if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(dateTime)) {
    //     ref_vuecal.value.createEvent(
    //         // Formatted start date and time or JavaScript Date object.
    //         dateTime,
    //         // Event duration in minutes (Integer).
    //         120,
    //         // Custom event props (optional).
    //         { title: 'New Event', teste:'olá', content: 'yay! 🎉', class: 'blue-event' }
    //     )
    //     } else if (dateTime) alert('Wrong date format.')
    // }
</script>

