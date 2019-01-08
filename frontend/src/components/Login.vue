<template>
  <v-container>
    <v-layout row v-if="formAlert">
      <v-flex xs12 sm6 offset-sm3 v-for="err in nonFieldFormErrors">
        <v-alert :value="formAlert" type="error">
          {{ err }}
        </v-alert>
      </v-flex>
    </v-layout>
    <v-layout row>
      <v-flex xs12 sm6 offset-sm3>
        <v-card>
          <v-card-text>
            <v-container>
              <form @submit.prevent="login">
                <v-layout row>
                  <v-flex xs12>
                    <v-text-field
                      name="username"
                      label="Username"
                      id="username"
                      v-model="username"
                      type="input"
                      required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12>
                    <v-text-field
                      name="password"
                      label="Password"
                      id="password"
                      v-model="password"
                      type="password"
                      required></v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12>
                    <v-btn class="primary black--text" type="submit">
                      Login
                    </v-btn>
                  </v-flex>
                </v-layout>
              </form>
            </v-container>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
      nonFieldFormErrors: '',
      formAlert: false
    }
  },
  methods: {
    login: function () {
      const { username, password } = this

      this.$store.dispatch('authRequest', { username, password })
        .then(() => {
          this.$router.push('/')
        })
        .catch(e => {
          this.formAlert = true
          if (e.response && e.response.data.non_field_errors) {
            this.nonFieldFormErrors = e.response.data.non_field_errors
          } else {
            this.nonFieldFormErrors = [e.message]
          }
          console.log(e)
        })
    }
  },
  watch: {
    formAlert: function (newVal, oldVal) {
      if (!newVal) {
        this.nonFieldFormErrors = ''
      }
    }
  }
}
</script>
