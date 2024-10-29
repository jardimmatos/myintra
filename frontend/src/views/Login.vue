<template>
    <wire-frame-jr>
        <template #navbar><span></span></template>
        <template #drawer><span></span></template>
        <template #footer><span></span></template>
        <template #main>
        <v-app>
            <!-- <Toast position="top-center" group="tc" /> -->
            <v-row justify="center" class="ma-0">
                <v-col cols="12" sm="6" md="6" lg="8" v-show="$vuetify.display.smAndUp" class="pa-0">
                    <v-card elevation="20" :loading="StateAuthLoading !== null"  style="border-radius: 5px 0px 0px 5px;"
                        class="align-center transparent bg-card-login"
                        height="100vh">
                        <v-card-text style="padding: 15px 15% 15px 15%" >
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="6" lg="4" class="pa-0">
                    <v-form ref="form" v-model="valid" style="height:93vh; padding:20vh 15% 20px 15% !important"
                        lazy-validation @submit.prevent="submit" class="form-login glass pa-8">
                        <v-row>
                            <v-img src="#" alt="logo" width="60" />
                        </v-row>
                        <v-row justify="center" class="mt-9 text--secondary">
                            <span class="title mb-4"> INTRANET
                                <span class="app-legend">by Augustus</span>
                            </span>
                        </v-row>
                        <v-row class="my-2">
                            <v-text-field variant="outlined"
                                v-model="login.username"
                                :rules="rules.required"
                                autocomplete="username"
                                label="Usuário"
                                :disabled="StateAuthLoading !== null"
                                required hide-details>
                                <template v-slot:prepend-inner>
                                    <v-icon class="mr-3">mdi-account</v-icon>
                                </template>
                            </v-text-field>
                        </v-row>
                        <v-row class="my-4">
                            <v-text-field variant="outlined"
                                v-model="login.password"
                                autocomplete="current-password"
                                type="password"
                                :rules="rules.required"
                                label="Senha"
                                :disabled="StateAuthLoading !== null"
                                required hide-details>
                                <template v-slot:prepend-inner>
                                    <v-icon class="mr-3">mdi-lock</v-icon>
                                </template>
                            </v-text-field>
                        </v-row>
                        <v-row>
                            <v-spacer></v-spacer>
                            <v-col cols="12" sm="6" class="text-right" dense>
                                <v-btn type="submit" elevation="0" :disabled="!valid" :small="$vuetify.display.smAndDown"
                                    color="primary" :loading="StateAuthLoading">
                                    Entrar
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-form>
                </v-col>
            </v-row>
        </v-app>
        </template>
        <template v-slot:userws>{{''}}</template>
        <template v-slot:notificationsws>{{''}}</template>
    </wire-frame-jr>
</template>
<script>

import { mapActions, mapGetters, mapMutations } from "vuex";
export default {
    name: 'LoginView',
    components: {
    },
    data(){
        return {
            login:{
                username:'',
                password:''
            },
            valid: true,
            rules:{
                required: [ v => !!v || 'Campo obrigatório' ]
            },
            loading:false
        }
    },
    methods:{
        ...mapActions(["LogIn"]),
        ...mapMutations([]),
        async entrar() {
            const log = await this.LogIn(this.login)
            if (log?.status === 200){
                location.reload()
            }
        },
        submit () {
            if(this.$refs.form.validate()){
                this.entrar()
            }
        },
    },
    computed:{
        ...mapGetters(['StateAuthLoading','StateAuthenticatedUser'])
    },
    mounted(){
    }
}
</script>
<style>
.glass {
    border-radius: 0px 5px 5px 0;
}
.form-login .text-error, .form-login .v-messages{
    font-weight: bold !important;
    color: darkred !important;
}
.app-legend{
    font-size: 0.5em;
    display: flex;
    line-height: 0;
    justify-content: right;
    position: relative;
    top: 0px;
    left: 40px;
    font-style: italic;
}
.bg-card-login{
    background-image:url('https://i.imgur.com/Nu1IOQc.jpg') !important;
    background-size: cover !important;
}
</style>