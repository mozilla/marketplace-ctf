var system = require('system');
var fs = require('fs');
var page = require('webpage').create();

var check_url = function(url) {
  page.open(url, function(status) {
  });
};

// Example: phantomjs reviewer.js http://localhost:5000
page.open(system.args[1] + '/review?key=' + fs.read('secret.json'), function(status) {
  var hrefs = page.evaluate(function() {
    return document.getElementsByTagName('a');
  });

  for (var k = 0; k < hrefs.length; k++) {
    page.sendEvent('click', hrefs[k].offsetLeft, hrefs[k].offsetTop);
  }

  phantom.exit();
});

