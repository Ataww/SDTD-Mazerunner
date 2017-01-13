//var env = require('node-env-file');
//env('./.env');

var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
//Require the Neo4J module
var neo4j = require('node-neo4j');
var exphbs  = require('express-handlebars');
var flash = require('connect-flash');
var session = require('cookie-session');
var helmet = require('helmet');

var routes = require('./routes/index');
var users = require('./routes/users');
var app = express();
var db = new neo4j();

var hbs = exphbs.create({
    // Specify helpers which are only registered on this instance.
    defaultLayout: 'main'
});

// view engine setup
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(flash());
app.use(helmet());
app.disable('x-powered-by');

app.set('trust proxy', 1) // trust first proxy

//var expiryDate = new Date( Date.now() + 60 * 60 * 1000 ); // 1 hour
app.use(session({
    secret: 'M4zE-RuNnEr',
    cookie: { maxAge: 6000000 } // 1 minute : this isn't working.
}));

//app.use('/', index);
//app.use('/users', users);

app.get('/', function (req, res) {
  res.render('home', {logged: false});
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
