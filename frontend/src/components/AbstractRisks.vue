<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm6 offset-sm3 class="text-xs-center">
        <h1 class="display-3 font-weight-black">Abstract Risks</h1>
        <h2 class="body-2">(templates for concrete risks)</h2>
        <v-btn color="amber" @click="openCreateDialog()">New</v-btn>
      </v-flex>
    </v-layout>

    <v-layout row justify-center>
      <v-dialog v-model="deleteErrorDialog" persistent max-width="290">
        <v-card>
          <v-card-title class="headline red white--text">
            <v-icon class="mr-2">error</v-icon>
            <span>
              Deletion error
            </span>
          </v-card-title>
          <v-card-text class="body-2" v-for="err in deleteErrors" :key="err">
            {{ err }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="primary black--text" flat @click="deleteErrorDialog = false">OK</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>

    <v-layout row justify-center>
      <v-dialog v-model="createDialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">Create Abstract Risk</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form">
                <v-layout row v-for="err in nonFieldFormErrors" :key="err">
                  <v-flex xs12>
                    <v-alert :value="formAlert" type="error">
                      {{ err }}
                    </v-alert>
                  </v-flex>
                </v-layout>
                <v-layout row>
                  <v-flex xs12>
                    <v-text-field
                      name="name"
                      label="Name"
                      id="name"
                      v-model="newAbstractRisk.name"
                      :counter="30"
                      :error-messages="fieldFormErrors.name"
                      :error-count="fieldFormErrors.name.length"
                      required>
                    </v-text-field>
                  </v-flex>
                </v-layout>
              <v-layout row class="text-xs-center">
                <v-flex xs12>
                  <v-btn class="primary black--text" flat @click="addField">Add field</v-btn>
                </v-flex>
              </v-layout>

              <v-layout row v-for="(af, i) in newAbstractRisk.abstract_fields" :key="i">
                <v-flex xs6>
                  <v-text-field
                  class="pr-1"
                  label="Label"
                  v-model="newAbstractRisk.abstract_fields[i].label"
                  :error-messages="fieldFormErrors.abstract_fields[i].label"
                  :error-count="fieldFormErrors.abstract_fields[i].length"
                  required>
                  </v-text-field>
                </v-flex>
                <v-flex xs6>
                  <v-select
                  class="pl-1"
                  label="Field Type"
                  v-model="newAbstractRisk.abstract_fields[i].field_type"
                  :items="fieldTypes"
                  item-text="name"
                  item-value="id"
                  :error-messages="fieldFormErrors.abstract_fields[i].field_type"
                  :error-count="fieldFormErrors.abstract_fields[i].field_type.length"
                  required>
                  </v-select>
                </v-flex>
              </v-layout>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="primary black--text" flat @click="closeDialog()">Close</v-btn>
            <v-btn class="primary black--text" flat @click="createAbstractRisk(newAbstractRisk)">Create</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>

    <v-layout row>
      <v-flex xs12 sm6 offset-sm3>
        <div
        v-if="$store.getters.loading && !abstractRisks.length"
        class="text-xs-center display-2">
          ...
        </div>
        <div
        v-else-if="!$store.getters.loading && !abstractRisks.length"
        class="mt-3 text-xs-center body-2 font-weight-light">
          Nothing here yet.
        </div>
        <v-list dense v-else>
          <v-list-group v-for="abstractRisk in abstractRisks" :key="abstractRisk.id" no-action>
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title class="title ml-2">{{ abstractRisk.name }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-container>
              <v-layout
              v-for="af in abstractRisk.abstract_fields" :key="af.label"
              :class="{'ml-2': $vuetify.breakpoint.smAndDown}"
              >
                <v-flex xs4>
                  <span class="body-2">{{ af.label }}</span>
                </v-flex>
                <v-flex xs8>
                  <span class="body-1">{{ fieldTypes.find(ft => ft.id === af.field_type).name }}</span>
                </v-flex>
              </v-layout>
            </v-container>
            <v-list-tile-action class="text-xs-center">
              <v-btn class="error my-2" @click="deleteAbstractRisk(abstractRisk.id)">DELETE</v-btn>
            </v-list-tile-action>
          </v-list-group>
        </v-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data () {
    return {
      'newAbstractRisk': {
        'name': '',
        'abstract_fields': []
      },
      'deleteErrorDialog': false,
      'deleteErrors': [],
      'labelRules': [],
      'createDialog': false,
      'formAlert': false,
      'nonFieldFormErrors': '',
      'fieldFormErrors': {
        'name': [],
        'abstract_fields': []
      }
    }
  },
  computed: {
    abstractRisks () {
      return this.$store.getters.abstractRisks
    },
    fieldTypes () {
      return this.$store.getters.fieldTypes
    }
  },
  mounted: function () {
    this.$store.dispatch('initAbstractRisks')
    this.$store.dispatch('initFieldTypes')
  },
  methods: {
    deleteAbstractRisk (abstractRiskID) {
      this.$store.dispatch('deleteAbstractRisk', abstractRiskID)
        .catch(e => {
          this.deleteErrorDialog = true
          if (e.response) {
            if (typeof e.response.data === 'object') {
              this.deleteErrors = Object.values(e.response.data)
            } else {
              this.deleteErrors = [e.response.data]
            }
          } else {
            this.deleteErrors = [e.message]
          }
        })
    },
    createAbstractRisk (newAbstractRisk) {
      if (this.$refs.form.validate()) {
        this.formAlert = false
        this.nonFieldFormErrors = ''
        this.fieldFormErrors.name = []
        this.fieldFormErrors.abstract_fields.forEach((el, i, arr) => {
          arr[i] = { 'label': [], 'field_type': [] }
        })

        this.$store.dispatch('createAbstractRisk', newAbstractRisk)
          .then(() => {
            this.closeDialog()
          })
          .catch(e => {
            if (e.response) {
              if (e.response.data.name) {
                this.fieldFormErrors.name = e.response.data.name
              }
              e.response.data.abstract_fields.forEach((el, i) => {
                if (el.label) {
                  this.$set(this.fieldFormErrors.abstract_fields[i], 'label', el.label)
                }
                if (el.field_type) {
                  this.$set(this.fieldFormErrors.abstract_fields[i], 'field_type', el.field_type)
                }
                this.fieldFormErrors = Object.assign({}, this.fieldFormErrors)
              })
            } else {
              this.formAlert = true
              this.nonFieldFormErrors = [e.message]
            }
          })
      }
    },
    addField () {
      this.newAbstractRisk.abstract_fields.push({
        'label': '',
        'field_type': ''
      })
      this.fieldFormErrors.abstract_fields.push({ 'label': [], 'field_type': [] })
    },
    closeDialog () {
      this.createDialog = false
    },
    openCreateDialog () {
      this.createDialog = true
      this.formAlert = false
      this.nonFieldFormErrors = ''
      this.$refs.form.reset()
      this.newAbstractRisk.abstract_fields = []
      this.fieldFormErrors.name = []
      this.fieldFormErrors.abstract_fields = []
      this.addField()
    }
  }
}
</script>

<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.list-complete-item {
  transition: all 1s;
  margin-right: 10px;
}
.list-complete-enter, .list-complete-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.list-complete-leave-active {
  position: absolute;
}
</style>
