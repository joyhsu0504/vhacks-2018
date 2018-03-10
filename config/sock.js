var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var api = require('./api');

// firebase for users db
var admin = require("firebase-admin");

// Fetch the service account key JSON file contents
var serviceAccount = require("./leif-fcc81-firebase-adminsdk-cc45z-0a7cc95a1a.json");

// Initialize the app with a service account, granting admin privileges
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://leif-fcc81.firebaseio.com"
});

// As an admin, the app has access to read and write all data, regardless of Security Rules
var db = admin.database();
var ref = db.ref("users");


var conn = function() {
  
  app.get('/', function (req, res) {
    res.sendfile(__dirname + '/index.html');
  });
};

var fromClient = function() {

  io.on('connection', function (socket) {
    // get user info from express session
    var sessionUser = socket.request.session.user;

    // From Leif
    socket.on('fromClient', function (data) {
      console.log(data.client);

      var hasNum = /([0123456789])/g.exec(data.client);
      if (hasNum != null) {

        // find key of username
        ref.orderByChild("username").equalTo(sessionUser).once("value", function(snapshot) {
          var yrsIncarceratedSet = false;
          var k = "";
          for (var key in snapshot.val()) {
              k = key;
              if (k != "" && "years_incarcerated" in snapshot.val()[k]) {
                yrsIncarceratedSet = true;
              }
          }
          if (yrsIncarceratedSet) {
            ref.child(k).update({
              years_released: data.client
            });
          } else {
            ref.child(k).update({
              years_incarcerated: data.client
            });
          }
        });

      }

      api.getRes(data.client, sessionUser).then(function(res){
        socket.emit('fromServer', { server: res });
      });
    });

    // From connection
    socket.on('fromMe', function (data) {
      socket.broadcast.emit('fromConnection', { server : data.client });
    });

  });
}

module.exports = {conn, fromClient, io, ref}
