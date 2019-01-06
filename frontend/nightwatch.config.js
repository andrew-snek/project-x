const deepmerge = require('deepmerge')
const userOptions = JSON.parse(process.env.VUE_NIGHTWATCH_USER_OPTIONS || '{}')

module.exports = deepmerge({
  src_folders: ['tests/e2e/specs'],
  output_folder: 'tests/e2e/reports',
  custom_assertions_path: 'tests/e2e/custom-assertions',

  selenium: {
    start_process: false,
    server_path: require('selenium-server').path,
    host: 'selenium',
    port: 4444,
    cli_args: {
      'webdriver.chrome.driver': require('chromedriver').path
    }
  },

  test_settings: {
    default: {
      selenium_host: 'selenium',
      silent: true,
      desiredCapabilities: {
        browserName: 'chrome',
        javascriptEnabled: true,
        acceptSslCerts: true
      }
    },

    headlessChrome: {
      desiredCapabilities: {
        chromeOptions: {
          args: ['no-sandbox', 'headless']
        }
      }
    }
  }
}, userOptions)