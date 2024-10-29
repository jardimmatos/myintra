<template>
  <div class="about">
    <span v-show="false">
      Param: {{$route.params.slug}} - {{slug}}
    </span>
    <v-row v-if="false">
        <v-spacer></v-spacer>
        <v-col cols="12" sm="8" md="6" lg="4" align-self="center" style="margin-top:5vw">
            <v-card elevation="20" :height="$vuetify.display.smAndUp ? '300' : '370'">
                <v-card-text style="padding: 60px">
                    <p>Desenvolvido por:</p>
                    <div>
                      <v-icon color="secondary">mdi-account</v-icon> {{ $verify.configs.brandName }}
                    </div>
                    <div>
                      <a class="links" target="_blank" href="mailto:jr.jardimmatos@gmail.com">
                        <v-icon color="error">mdi-gmail</v-icon> jr.jardimmatos@gmail.com
                      </a>
                    </div>
                    <div>
                      <a class="links" target="_blank" href="tel:+5598988861514">
                        <img src="@/assets/images/flag-br.png" height="13" alt="br" style="margin-left:3px">
                        +55 (98) 98886-1514
                        <a class="links" target="_blank" href="https://wa.me/5598988861514?text=Ol%C3%A1,%20Augustus">
                          <v-icon small color="success">mdi-whatsapp</v-icon>
                        </a>
                      </a>
                    </div>
                </v-card-text>
            </v-card>
        </v-col>
        <v-spacer></v-spacer>
    </v-row>
  </div>
</template>
<script>
export default {
  name: 'About',
  components: {
  },
  props:{
    slug:{
      type: String,
      required:false
    }
  },
}
</script>
<style scoped>
  .links{
    text-decoration: none;
  }
</style>