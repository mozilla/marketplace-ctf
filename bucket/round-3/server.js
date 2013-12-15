var http = require('http');

var server = http.createServer(function (request, response) {
  response.writeHead(200, {"Content-Type": "application/json"});
  response.end(JSON.stringify({'valid': false}));
});

server.listen(9999);
