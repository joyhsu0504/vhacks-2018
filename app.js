var express = require('express');
var session = require('express-session');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');

var socket = require('./config/sock');

var app = express();

// references to users db in firebase
var ref = socket.ref;

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
var sessionMiddleware = session({
  secret: 'ssshhhhh',
  resave: false,
  saveUninitialized: true
});
app.use(sessionMiddleware);
app.use(express.static(path.join(__dirname, 'public')));
app.use('/', index);

// init socket for dialog-flow chat
socket.conn();
socket.fromClient();
socket.io.use(function(sock, next) {
	// add session data to socket.io
    sessionMiddleware(sock.request, sock.request.res, next);
});

// Display form for new user
app.get('/register', (req, res) => {
  	res.render('index', { title: 'Register', page: 'register', user: req.session.user });
});

// Handle submitted form for new users
app.post('/register', (req, res) => {
	const user = req.body.username;
	const pass = req.body.password;
	const passwordConfirmation = req.body.passwordConfirmation;

	if (user.length === 0) {
		console.log('Bad name');
	} else if (user.length > 50) {
		console.log('Bad name');
	} else if (pass !== passwordConfirmation) {
		console.log('Passwords don\'t match');
	} else if (pass.length === 0) {
		console.log('Bad password');
	} else if (pass.length > 50) {
		console.log('Bad password');
	} else {
		ref.push({
	  		username: user,
	  		password: pass
		});

		req.session.user = user;
		res.redirect('/');
	}
	res.redirect('/');
});

// Display login form
app.get('/login', (req, res) => {
  	res.render('index', { title: 'Login', page: 'login', user: req.session.user });
});

app.post('/login', (req, res) => {
  	const user = req.body.username;
  	const pw = req.body.password;

	ref.orderByChild("username").equalTo(user).once("value", function(snapshot) {
		var k = "";
		for (var key in snapshot.val()) {
		    k = key;
		}

	    if (k != "" && snapshot.val()[k].password == pw) {
			req.session.user = user;

  			res.redirect('/');
		} else {
			console.log("user doesn't exist");
			res.redirect('/');
		}
	}, function (errorObject) {
	  	console.log("The read failed: " + errorObject.code);
	});
  
});

// Log a user out
app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
