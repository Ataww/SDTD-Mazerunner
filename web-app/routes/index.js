var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'SDTD-Mazerunner' });
});

/* GET spark page. */
router.get('/spark', function(req, res, next) {
    res.render('spark', { title: 'SDTD-Mazerunner' });
});

module.exports = router;
