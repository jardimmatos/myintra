import router from '@/router'
import BaseService from '@/services/base/baseService';
const api = new BaseService()
const state = {
    user_filiais: [],
    dark: localStorage.getItem('dark') == 'true',
    drawer: true,
    alerts: [],
    monitors: [],
    monitors_loading: false,
};
const getters = {
    StateMonitors: state => state.monitors,
    StateMonitorsLoading: state => state.monitors_loading,
    StateDrawer: state => state.drawer,
    StateAlerts: state => state.alerts,
    StateBaseURL: ()=> process.env.NODE_ENV === 'production' ? process.env.VUE_APP_BACKEND_PROD : process.env.VUE_APP_BACKEND_DEV,
    StateDark: () => state => state.dark,
    StateDarkIcon: state => state.dark ? 'mdi-weather-night' : 'mdi-weather-sunny',
    StateUserFiliais: state => state.user_filiais
};
const mutations = {
    setDark(state){
        state.dark = state.dark  ? false : true;
        localStorage.setItem('dark', state.dark)
    },
    setDrawer(state, value){
        state.drawer = value
    },
    setAlerts(state, value){
        state.alerts = value
    },
    setMonitors(state, value){
        state.monitors = value
    },
    setMonitorsLoading(state, value){
        state.monitors_loading = value
    },
    setUserFiliais(state, value){
        state.user_filiais = value
    },
};
const actions = {
    // eslint-disable-next-line
    gotoRoute({}, route) {
        if(router.currentRoute.name != route.name){
            console.log('goto', route)
            router.push(route)
        }
    },
    SetDark({commit}){
        commit('setDark')
    },
    async GetMonitors({commit},) {
        commit('setMonitorsLoading', true)
        try{
            let response = await api.get_monitor_status()
            commit('setMonitors', response.data)
          }catch(error){
            commit('setMonitors', [])
            commit("setAlerts", [ error.toast_message ])
        }
        commit('setMonitorsLoading', false)
    },
};
export default {
  state,
  getters,
  actions,
  mutations
};