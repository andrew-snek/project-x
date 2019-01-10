<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm6 offset-sm3 class="text-xs-center">
        <h1 class="display-3 font-weight-black">Risks</h1>
        <h2 class="body-2">
            ("There are risks and costs to action. But they are far less than the long range risks of comfortable inaction." - JFK)
        </h2>
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
            <span class="headline">Create Risk</span>
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
                  v-model="newRisk.name"
                  :counter="30"
                  :error-messages="fieldFormErrors.name"
                  :error-count="fieldFormErrors.name.length"
                  required>
                  </v-text-field>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs12>
                  <v-select
                  label="Abstract Risk"
                  v-model="newRisk.abstract_risk"
                  @change="fillWithEmptyFields(abstractRisk.abstract_fields.length)"
                  :items="abstractRisks"
                  item-text="name"
                  item-value="id"
                  :error-messages="fieldFormErrors.abstract_risk"
                  :error-count="fieldFormErrors.abstract_risk.length"
                  required>
                  </v-select>
                </v-flex>
              </v-layout>
              <v-layout row v-for="(af, i) in requiredFields" :key="i">
                <v-flex xs12 :myVar="widgetType = fieldTypes.find(ft => ft.id === af.field_type).widget_type">
                  <v-text-field
                  v-if="widgetType === 0"
                  :label="af.label"
                  v-model="newRisk.fields[i].value"
                  :error-messages="fieldFormErrors.fields[i].value"
                  :error-count="fieldFormErrors.fields[i].length"
                  required>
                  </v-text-field>
                  <v-textarea
                  v-else-if="widgetType === 1"
                  :label="af.label"
                  v-model="newRisk.fields[i].value"
                  :error-messages="fieldFormErrors.fields[i].value"
                  :error-count="fieldFormErrors.fields[i].length"
                  required>
                  </v-textarea>
                  <v-menu
                  v-else-if="widgetType === 2"
                  ref="datePickerMenu"
                  :close-on-content-click="true"
                  v-model="datePickerMenu"
                  :nudge-right="40"
                  :return-value.sync="date"
                  lazy
                  transition="scale-transition"
                  offset-y
                  full-width
                  min-width="290px"
                  >
                    <v-text-field
                    slot="activator"
                    v-model="newRisk.fields[i].value"
                    :label="af.label"
                    prepend-icon="event"
                    readonly
                    :error-messages="fieldFormErrors.fields[i].value"
                    :error-count="fieldFormErrors.fields[i].length"
                    ></v-text-field>
                    <v-date-picker
                    v-model="newRisk.fields[i].value"
                    no-title
                    scrollable>
                    </v-date-picker>
                  </v-menu>
                  <v-select
                  v-else-if="widgetType === 3"
                  :label="af.label"
                  v-model="newRisk.fields[i].value"
                  :items="fieldTypes.find(ft => ft.id === af.field_type).regex.split('$|^').map(e => e.replace(/\$|\^/g, ''))"
                  :error-messages="fieldFormErrors.fields[i].value"
                  :error-count="fieldFormErrors.fields[i].length"
                  required>
                  </v-select>
                </v-flex>
              </v-layout>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="primary black--text" flat @click="closeDialog()">Close</v-btn>
            <v-btn class="primary black--text" flat @click="createRisk(newRisk)">Create</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>

    <v-layout row >
      <v-flex xs12 sm6 offset-sm3>
        <div
        v-if="$store.getters.loading && !risks.length"
        class="text-xs-center display-2">
          ...
        </div>
        <div
        v-else-if="!$store.getters.loading && !risks.length"
        class="mt-3 text-xs-center body-2 font-weight-light"
        >
          Nothing here yet.
        </div>
        <v-list dense v-else>
          <v-list-group v-for="risk in risks" :key="risk.name" no-action>
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title class="title text-xs-left">
                  <div class="ml-2">
                    {{ risk.name }}
                  </div>
                </v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
            <v-container>
              <v-layout>
                <v-flex xs2 class="body-2">
                  Abstract Risk
                </v-flex>
                <v-flex xs10>
                  <span class="body-1 text-xs-left">
                    {{ abstractRisks.find(ar => ar.id === risk.abstract_risk).name }}
                  </span>
                </v-flex>
              </v-layout>
              <hr />
              <v-layout
              row
              v-for="(af, i) in abstractRisks.find(ar => ar.id === risk.abstract_risk).abstract_fields"
              :class="{'ml-2': $vuetify.breakpoint.smAndDown}"
              :key="i"
              >
                <v-flex xs2 class="body-2">
                  {{ af.label }}
                </v-flex>
                <v-flex xs10>
                  <span class="body-1 text-xs-left">{{ risk.fields[i].value }}</span>
                </v-flex>
              </v-layout>
            </v-container>
            <v-list-tile-action class="text-xs-center">
              <v-btn class="error my-2" @click="deleteRisk(risk.id)">DELETE</v-btn>
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
      'date': new Date().toISOString().substr(0, 7),
      'datePickerMenu': false,
      'newRisk': {
        'name': '',
        'abstract_risk': '',
        'fields': []
      },
      'createDialog': false,
      'deleteErrorDialog': false,
      'deleteErrors': [],
      'formAlert': false,
      'nonFieldFormErrors': '',
      'fieldFormErrors': {
        'name': [],
        'abstract_risk': [],
        'fields': []
      }
    }
  },
  computed: {
    risks () {
      return this.$store.getters.risks
    },
    abstractRisks () {
      return this.$store.getters.abstractRisks
    },
    fieldTypes () {
      return this.$store.getters.fieldTypes
    },
    abstractRisk () {
      return this.abstractRisks.find(ar => ar.id === this.newRisk.abstract_risk)
    },
    requiredFields () {
      if (this.abstractRisk) {
        return this.abstractRisk.abstract_fields
      } else {
        return []
      }
    }
  },
  beforeCreate: function () {
    this.$store.dispatch('initRisks')
    this.$store.dispatch('initAbstractRisks')
    this.$store.dispatch('initFieldTypes')
  },
  methods: {
    deleteRisk (riskID) {
      this.$store.dispatch('deleteRisk', riskID)
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
    fillWithEmptyFields (numOfFields) {
      this.newRisk.fields = Array(numOfFields).fill().map(e => ({ 'value': '' }))
      this.fieldFormErrors.fields = Array(numOfFields).fill().map(e => ({ 'value': '' }))
    },
    createRisk (newRisk) {
      if (this.$refs.form.validate()) {
        this.formAlert = false
        this.fieldFormErrors.name = []
        this.fieldFormErrors.abstract_risk = []
        this.fieldFormErrors.fields.forEach((el, i, arr) => {
          arr[i] = { 'value': [] }
        })

        this.$store.dispatch('createRisk', newRisk)
          .then(() => {
            this.closeDialog()
          })
          .catch(e => {
            if (e.response) {
              if (e.response.data.name) {
                this.fieldFormErrors.name = e.response.data.name
              }
              if (e.response.data.abstract_risk) {
                this.fieldFormErrors.abstract_risk = e.response.data.abstract_risk
              }
              for (const field of Object.keys(e.response.data.fields)) {
                this.$set(this.fieldFormErrors.fields, field, e.response.data.fields[field])
              }
            } else {
              this.formAlert = true
              this.nonFieldFormErrors = [e.message]
            }
          })
      }
    },
    closeDialog () {
      this.createDialog = false
    },
    openCreateDialog () {
      this.createDialog = true
      this.formAlert = false
      this.$refs.form.reset()
      this.newRisk.fields = []
      this.fieldFormErrors.name = []
      this.fieldFormErrors.abstract_risk = []
      this.fieldFormErrors.fields = []
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
</style>
