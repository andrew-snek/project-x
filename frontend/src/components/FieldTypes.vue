<template>
  <v-container>
    <v-layout row>
      <v-flex xs12 sm6 offset-sm3 class="text-xs-center">
        <h1 class="display-3 font-weight-black">Field types</h1>
        <h2 class="body-2">(basic building blocks of the system)</h2>
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
            <span class="headline">Create Field Type</span>
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
                      v-model="newFieldType.name"
                      :counter="30"
                      :error-messages="fieldFormErrors.name"
                      :error-count="fieldFormErrors.name.length"
                      >
                    </v-text-field>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs12>
                  <v-select
                  name="widget_type"
                  label="Widget type"
                  id="widget_type"
                  v-model="newFieldType.widget_type"
                  :items="widgetTypes"
                  item-text="text"
                  item-value="value"
                  :error-messages="fieldFormErrors.widget_type"
                  :error-count="fieldFormErrors.widget_type.length"
                  >
                  </v-select>
                </v-flex>
              </v-layout>
              <v-layout row>
                <v-flex xs12>
                  <v-textarea
                    name="regex"
                    label="Regular expression"
                    id="regex"
                    :counter="3000"
                    v-model="newFieldType.regex"
                    :error-messages="fieldFormErrors.regex"
                    :error-count="fieldFormErrors.regex.length"
                    >
                  </v-textarea>
                </v-flex>
              </v-layout>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn class="primary black--text" flat @click="closeDialog()">Close</v-btn>
            <v-btn class="primary black--text" flat @click="createFieldType(newFieldType)">Create</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>

    <v-layout row>
      <v-flex xs12 sm6 offset-sm3>
        <div
        v-if="$store.getters.loading && !fieldTypes.length"
        class="text-xs-center display-2">
          ...
        </div>
        <div
        v-else-if="!$store.getters.loading && !fieldTypes.length"
        class="mt-3 text-xs-center body-2 font-weight-light">
          Nothing here yet.
        </div>
        <v-list dense v-else>
          <v-list-group v-for="fieldType in fieldTypes" :key="fieldType.name" no-action>
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title class="title">{{ fieldType.name }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-container>
              <v-layout>
                <v-flex xs3>
                  <span class="body-2">Widget type</span>
                </v-flex>
                <v-flex xs9>
                  <span class="body-1">
                    {{ widgetTypes.find(wt => wt.value === fieldType.widget_type).text }}
                  </span>
                </v-flex>
              </v-layout>
              <v-layout>
                <v-flex xs3>
                  <span class="body-2">Regular expression</span>
                </v-flex>
                <v-flex xs9>
                  <span class="body-1">{{ fieldType.regex }}</span>
                </v-flex>
              </v-layout>
            </v-container>
            <v-list-tile-action class="text-xs-center">
              <v-btn class="error my-2" @click="deleteFieldType(fieldType.id)">DELETE</v-btn>
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
      'newFieldType': {
        'name': '',
        'widget_type': '',
        'regex': ''
      },
      'deleteErrorDialog': false,
      'deleteErrors': [],
      'createDialog': false,
      'formAlert': false,
      'nonFieldFormErrors': '',
      'fieldFormErrors': {
        'name': [],
        'widget_type': [],
        'regex': []
      },
      'widgetTypes': [
        {
          'text': 'One line input',
          'value': 0
        },
        {
          'text': 'Multiline input',
          'value': 1
        },
        {
          'text': 'Date picker',
          'value': 2
        },
        {
          'text': 'Options selector',
          'value': 3
        }
      ]
    }
  },
  computed: {
    fieldTypes () {
      return this.$store.getters.fieldTypes
    }
  },
  mounted: function () {
    this.$store.dispatch('initFieldtypes')
  },
  methods: {
    deleteFieldType (fieldTypeID) {
      this.$store.dispatch('deleteFieldType', fieldTypeID)
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
    createFieldType (newFieldType) {
      if (this.$refs.form.validate()) {
        this.formAlert = false
        this.nonFieldFormErrors = ''
        for (const field of Object.keys(this.fieldFormErrors)) {
          this.fieldFormErrors[field] = []
        }

        this.$store.dispatch('createFieldType', newFieldType)
          .then(() => {
            this.closeDialog()
          })
          .catch(e => {
            this.formAlert = true
            if (e.response) {
              for (const field of Object.keys(e.response.data)) {
                this.fieldFormErrors[field] = e.response.data[field]
              }
            } else {
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
      this.nonFieldFormErrors = ''
      this.$refs.form.reset()
      for (const field of Object.keys(this.fieldFormErrors)) {
        this.fieldFormErrors[field] = []
      }
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
