var express = require('express');
var router = express.Router();

var socket = require('../config/sock');

var similarity = require('compute-cosine-similarity');

/* GET home page. */
router.get('/', function(req, res, next) {
	console.log(req.session);
	res.render('index', { title: 'Leif', page: 'leif', user: req.session.user });
	console.log(res.value);
});

/* GET groups page. */
router.get('/connections', function(req, res, next) {
	if (req.session.user != null) {

		// Get # years in prison + # years since release
        socket.ref.orderByChild("username").equalTo(req.session.user).once("value", function(snapshot) {
          	var k = "";
          	for (var key in snapshot.val()) {
              	k = key;
          	}

          	// If they have a connection, reconnect with them
          	if ("connection" in snapshot.val()[k]) {
          		req.session.connection = snapshot.val()[k].connection;

				console.log(req.session.connection);
		        res.render('index', { title: 'Connections', page: 'connections', user: req.session.user, connection: req.session.connection });
				console.log(res.value);
          	} else {
          		var years1 = parseInt(snapshot.val()[k].years_incarcerated)
	          	var years2 = parseInt(snapshot.val()[k].years_released)
	          	var p1 = [years1, years2]

	          	// Loop through everyone else's 
	          	socket.ref.once("value", function(snapshot) {
	          		var k2 = "";
	          		var maxSim = 0;
		          	for (var key in snapshot.val()) {
		          		var years3, years4 = 0;
		          		if ("years_incarcerated" in snapshot.val()[key]) {
		          			years3 = parseInt(snapshot.val()[key].years_incarcerated)
		          		}
		          		if ("years_released" in snapshot.val()[key]) {
		          			years4 = parseInt(snapshot.val()[key].years_released)
		          		}
			          	var p2 = [years3, years4]
			          	var sim = similarity(p1, p2);
			          	if (sim > maxSim) {
			          		k2 = key
			          	}
		          	}

		          	// Update both firebase DBs
		          	socket.ref.child(k).update({
		              connection: snapshot.val()[key].username
		            });
		            socket.ref.child(k2).update({
		              connection: snapshot.val()[k].username
		            });

					req.session.connection = snapshot.val()[key].username;

					console.log(req.session.connection);
		          	res.render('index', { title: 'Connections', page: 'connections', user: req.session.user, connection: req.session.connection });
					console.log(res.value);
				});
          	}
          	
        });
	} else {
		res.redirect('/');
	}
});

/* GET jobs page. */
router.get('/jobs', function(req, res, next) {
	if (req.session.user != null) {
		res.render('index', { title: 'Your Jobs', page: 'jobs', user: req.session.user });
		console.log(res.value);
	} else {
		res.redirect('/');
	}
});

module.exports = router;
