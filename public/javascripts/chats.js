var botui = new BotUI('api-bot');

var socket = io.connect();
// read the BotUI docs : https://docs.botui.org/

botui.message.add({
  content: 'Hi, Leif here! This is someone who has had a similar experience with incarceration to you, and who we think you might connect well with. Feel free to introduce yourself!',
  delay: 1500,
}).then(function () {

  socket.on('fromConnection', function (data) { // recieveing a reply from server.
    botui.message.add({
      content: data.server,
      delay: 100,
    }).then(function () {
      botui.action.text({
        action: {
          placeholder: '', }
      }).then(function (res) {
        socket.emit('fromMe', { client : res.value }); // sends the message typed to server
        console.log(res.value); // will print whatever was typed in the field.
      })
    });
  });

  botui.action.text({
    action: {
      placeholder: 'Hi, my name is...', }
  }).then(function (res) {
    socket.emit('fromMe', { client : res.value });
  })
  
});
