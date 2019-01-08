import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import colors from 'vuetify/es5/util/colors'

Vue.use(Vuetify, {
  theme: {
    primary: colors.amber.base,
    secondary: '#424242',
    accent: colors.amber.base,
    error: '#FF5252',
    info: colors.amber.base,
    success: '#4CAF50',
    warning: '#FFC107'
  },
  iconfont: 'md',
})
