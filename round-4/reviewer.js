var system = require('system');
var fs = require('fs');
var page = require('webpage').create();

// Example: phantomjs reviewer.js http://localhost:5000
page.open(system.args[1] + '/login?key=' + fs.read('secret.json'), function(status) {
  window.setTimeout(function () {
    phantom.exit();
  }, 1500);
});
