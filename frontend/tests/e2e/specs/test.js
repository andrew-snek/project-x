// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage

module.exports = {
  'default e2e tests': browser => {
    browser
      .url('http://spa:8080/')
      .waitForElementVisible('#britecore', 5000)
      .assert.containsText('div', 'Welcome')
      .end()
  }
}
