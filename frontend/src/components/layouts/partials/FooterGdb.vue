<template>
    <!-- <v-footer></v-footer> -->
    <v-footer absolute class="text-center d-flex flex-column" color="footer">
        <div style="width:95%">

            <div class="endereco text-caption text-right">
                <div>{{$verify.configs.address}}</div>
                <div>{{$verify.configs.phone}}</div>
            </div>

            <v-divider class="my-4"></v-divider>

            <div class="links-institucionais">
                <v-row>
                    <v-col cols="12" sm="4" md="4"
                        v-for="categoria, ci in Array.from(new Set(computedLinks.map(i => i.categoria)))" :key="'links-categoria-'+ci">
                        <div class="text-left text-h6">
                            {{categoria}}
                            <v-divider class="mr-12"></v-divider>
                        </div>
                        <div v-for="link, index in computedLinks.filter(i => i.categoria==categoria)"
                            :key="'col-link-'+index">
                            <v-list-item two-line :href="link.link" class="text-left mx-0 px-0"
                                target="_blank" elevation="0" density="compact">
                                <v-list-item-title class="text-caption">
                                    <v-icon-small class="mb-1">mdi-web</v-icon-small>
                                    {{link.label}}
                                </v-list-item-title>
                            </v-list-item>
                        </div>
                    </v-col>
                </v-row>
            </div> 

            <v-divider class="my-2"></v-divider>
            <div class="logos pa-2">
                <v-row>
                    <v-col cols="12" offset-sm="1" sm="10" >
                        <div class="text-center">
                            <div class="logo-footer">
                                <v-img src="favicon.png"
                                    width="80">
                                </v-img>
                            </div>
                            <div>
                                <v-btn-small v-for="l in socials" :key="l.link" :href="l.link" icon color="transparent">
                                    <v-icon>{{l.icon}}</v-icon>
                                </v-btn-small>
                            </div>
                        </div>
                    </v-col>
                </v-row>
            </div>
            <v-divider class="my-4"></v-divider>
            <div>
                <small>{{ new Date().getFullYear() }} — 
                    <strong>{{$verify.configs.appName}} - {{$verify.configs.brandName}}</strong>
                </small>
            </div>
        </div>
    </v-footer>
</template>
<script>
export default {
    data: () => ({
        socials: [
            { icon: 'mdi-web', link: 'https://myintra.dev.br' },
            { icon: 'mdi-linkedin', link: 'https://myintra.dev.br' },
            { icon: 'mdi-instagram', link: 'https://myintra.dev.br' },
        ],
    }),
    computed:{
        computedLinks(){
            return this.$verify.links_uteis
        }
    },
}
</script>
<style scoped>
.logo-footer {
    background-color: transparent;
    padding: 10px 10px;
    border-radius: 5px;
    text-align: -webkit-center;
}
</style>