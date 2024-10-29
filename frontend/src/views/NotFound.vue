<template>
  <v-app>
    <v-main class="pt-6 mt-6">
      <v-row justify="center">
        <h1 class="text-h1">404</h1>
      </v-row>
      <v-row justify="center" class="pa-6">
        Página não encontrada
      </v-row>
      <v-row justify="center">
        <v-btn class="tesxt-white font-weight-medium" to="/">Voltar para início
        </v-btn>
      </v-row>
    </v-main>
  </v-app>
</template>
<script>
export default {
  name: 'ErrorView404'
}
</script>