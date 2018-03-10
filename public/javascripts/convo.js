var botui = new BotUI('api-bot');

var socket = io.connect();
// read the BotUI docs : https://docs.botui.org/

botui.message.add({
  content: 'Hi! I\'m Leif, your personal advisor for helping you reintegrate into society post-incarceration!',
  delay: 1500,
}).then(function () {

  socket.emit('fromClient', { client : "begin" }); // sends start to server

}).then(function () {

  socket.on('fromServer', function (data) { // recieveing a reply from server.

    botui.message.add({
      content: data.server,
      delay: 100,
    }).then(function () {
      botui.action.text({
        action: {
          placeholder: '', }
      }).then(function (res) {
        socket.emit('fromClient', { client : res.value }); // sends the message typed to server
        console.log(res.value); // will print whatever was typed in the field.
      })
    });

  })
});
