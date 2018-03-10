var apiai = require('apiai');

// read the api.ai docs : https://api.ai/docs/

//Enter your API Key
var app = apiai("715f5fb1ea0c4851a9d568e4d7ad5d82");

// Function which returns speech from api.ai
var getRes = function(query, sessionUser) {
	var request = app.textRequest(query, {
		sessionId: sessionUser
	});

	const responseFromAPI = new Promise(
        function (resolve, reject) {
			request.on('error', function(error) {
    			reject(error);
			});
			request.on('response', function(response) {
  				resolve(response.result.fulfillment.speech);
			});
		});
	request.end();
	return responseFromAPI;
};

// test the command :
//getRes('hello').then(function(res){console.log(res)});

module.exports = {getRes}
