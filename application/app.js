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
var http = require('http');

var routes = require('./routes/index');
var users = require('./routes/users');
var app = express();
var db = new neo4j("http://neo4j:neo4j_pass@213.32.74.108:7475");

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

var User = require('./models/user');

//app.use('/', index);
//app.use('/users', users);

app.get('/', function (req, res) {
  res.render('home', {logged: false});
});

app.get('/songs/:name', function(req, res) {
  var name = req.params.name;
  db.cypherQuery(
    'MATCH (u:Utilisateur {nomUtilisateur:"'+name+'"}) MATCH (t:Titre) WHERE NOT (u)-[:AIME]->(t) RETURN t LIMIT 10',
    function(err, result) {
        if(err) res.render('error', {error:err});
        else {
          res.render('songs', {songs:result.data, user:name});
        }
      }
    );
});

app.get('/refresh/:name', function(req, res) {
  var options = { host:'127.0.0.1', port:'5000', path: '/compute_recommendation/'+req.params.name};
  //var options = { host:'google.fr', path: '/'};
  var req_get = http.get(options, function(res) {
        console.log(res.statusCode);
        /*if (res.statusCode != 200) {
          var options = {host: '149.202.161.163:5000', path: '/compute_recommandation/'+req.params.name}
          var req_get2 = http.get(options, function(res) {
            console.log(res.statusCode);
          });
        }*/
  });
  var name = req.params.name;
  db.cypherQuery(
    'MATCH (u:Utilisateur {nomUtilisateur:"'+name+'"}) MATCH (t:Titre) WHERE (u)-[:RECO]->(t) RETURN t LIMIT 10',
    function(err, result) {
        if(err) {
                res.render('error', {error:err});
                console.log(err);}
        else {
          res.render('recommandations', {songs:result.data, user:name});
        }
     });
});

app.get('/recommandations/:name', function(req, res) {
  var name = req.params.name;
  db.cypherQuery(
    'MATCH (u:Utilisateur {nomUtilisateur:"'+name+'"}) MATCH (t:Titre) WHERE (u)-[:RECO]->(t) RETURN t LIMIT 10',
    function(err, result) {
        if(err) {
		res.render('error', {error:err});
		console.log(err);}
        else {
          res.render('recommandations', {songs:result.data, user:name});
        }
      }
    );
});

app.post('/like', function(req, res) {
  addLike(req.query.id, req.query.user, res);
});

app.post('/dislike', function(req, res) {
  addDislike(req.query.id, req.query.user, res);
});

app.post('/unreco', function(req, res) {
  User.addUserRelationship('unreco', req.query.user, req.query.id, function(err){
    if (err) res.sendStatus(500);
    else res.sendStatus(200);
  });
});

function addLike(id, name, res) {
 User.addUserRelationship('like', name, id, function(err) {
   if (err) res.sendStatus(500);
   else res.sendStatus(200);
 });
}

function addDislike(id, name, res) {
  User.addUserRelationship('dislike', name, id, function(err) {
    if (err) res.sendStatus(500);
    else res.sendStatus(200);
  });
}

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
