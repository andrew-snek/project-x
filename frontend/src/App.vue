<template>
  <v-app id="britecore">
    <v-navigation-drawer
      v-model="drawer"
      fixed
      clipped
      disable-resize-watcher
      class="grey lighten-4"
      app
    >
      <v-list
        dense
        class="grey lighten-4"
      >
        <template v-for="(item, i) in items">
          <v-list-tile
            :key="i"
            :to="item.link"
          >
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar color="amber" app absolute clipped-left>
      <v-toolbar-side-icon @click="isAuthenticated ? drawer = !drawer : $router.push('/login')"></v-toolbar-side-icon>
      <router-link to="/">
        <span class="title black--text mx-3">Britecore&nbsp;<span class="font-weight-light">Insurance</span></span>
      </router-link>

      <span class="custom-loader" v-show="loading">
        <v-icon light>cached</v-icon>
      </span>
      <v-spacer></v-spacer>

      <router-link to="/login" v-if="!isAuthenticated">
        <v-btn color="amber">
          <v-icon>account_box</v-icon>
          <span class="pl-1">LOGIN</span>
        </v-btn>
      </router-link>
      <router-link to="/logout" v-else>
        <v-btn color="amber">
          <v-icon>account_box</v-icon>
          <span class="pl-1">LOGOUT</span>
        </v-btn>
      </router-link>
    </v-toolbar>

    <v-container fluid fill-height class="grey lighten-4">
          <transition name="slide-y-transition" mode="out-in">
            <router-view  class="mt-5"/>
          </transition>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    drawer: false,
    items: [
      { icon: 'subject', text: 'Field Types', link: '/fieldtypes' },
      { icon: 'tab_unselected', text: 'Abstract Risks', link: '/abstractrisks' },
      { icon: 'tab', text: 'Risks', link: '/risks' }
    ]
  }),
  computed: {
    isAuthenticated () {
      return this.$store.getters.isAuthenticated
    },
    loading () {
      return this.$store.getters.loading
    }
  }
}
</script>

<style lang="scss">
  #britecore main .container {
    height: 660px;
  }

  .navigation-drawer__border {
    display: none;
  }

  .text {
    font-weight: 400;
  }

  a {
    text-decoration: none;
    color: black !important;
  }

  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }

  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
