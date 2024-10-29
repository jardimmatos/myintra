import AuthService from '../../../services/auth/authService';
import FrontendService from '../../../services/frontendService';

const fes = new FrontendService()
const api = new AuthService()

const state = {
    user: localStorage.getItem(fes.SESSION_USERNAME),
    authenticated_user: JSON.parse(localStorage.getItem(fes.SESSION_USER_AUTHENTICATED)),
    authLoading: null
};

const getters = {
    isAuthenticated: () => !!JSON.parse(localStorage.getItem(fes.SESSION_USER_AUTHENTICATED)) && 
                            !!localStorage.getItem(fes.SESSION_USERNAME),
    StateUser: () => localStorage.getItem(fes.SESSION_USERNAME),
    StateAuthenticatedUser: () => JSON.parse(localStorage.getItem(fes.SESSION_USER_AUTHENTICATED)),
    StateAuthLoading: state => state.authLoading,
};

const mutations = {
    setAuthLoading(state, value){ state.authLoading = value },
};

const actions = {
    async LogIn({commit, dispatch }, user) {
        dispatch
        try{
            commit('setAuthLoading', 'login')
            const response = await api.authenticate({...user});

            fes.set_token_local(response, user)

            commit('setAuthLoading', null)
            return response

        } catch(error){
            commit("setAlerts", [error.toast_message])
            commit('setAuthLoading', null)
            return null
        }
    },
    async LogOut({ commit }, alert=null) {
        commit('setAuthLoading', 'logout')
        let logout = {
            tag: 'warn',
            title: 'Logout',
            message:`Desconectando...`
        }
        setTimeout(()=>{
            location.reload()
        }, 1000)
        fes.remove_token_local()
        if (!alert){
            commit("setAlerts", [ logout ])
        }else{
            commit("setAlerts", [ alert ])
        }
        commit('setAuthLoading', null)
    },
};
export default {
  state,
  getters,
  actions,
  mutations
};