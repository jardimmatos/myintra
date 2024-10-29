import perms from '@/pugins/permissions'
export default {
    install(app){
        app.config.globalProperties.$verify = perms
    }
}