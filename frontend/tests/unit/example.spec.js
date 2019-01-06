import Vue from 'vue'
import Vuetify from 'vuetify'
import { shallowMount } from '@vue/test-utils'
import Welcome from '@/components/Welcome.vue'

Vue.use(Vuetify)
// we're not using createLocalVue here due to a bug https://github.com/vuetifyjs/vuetify/issues/4068

describe('Welcome.vue', () => {
  it('renders welcome', () => {
    const wrapper = shallowMount(Welcome)
    expect(wrapper.html()).toContain('Welcome')
  })
})
