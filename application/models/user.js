// user.js
// User model logic.

//var env = require('node-env-file');
//env('./.env');
var nodeneo4j = require('node-neo4j');
var dbnode = new nodeneo4j("http://neo4j:neo4j_pass@149.202.170.185:7474");
//var bcrypt   = require('bcrypt-nodejs');

// private constructor:
var User = module.exports = function User(_node) {
	// all we'll really store is the node; the rest of our properties will be
	// derivable or just pass-through properties (see below).
	this._node = _node;
}


User.addUserRelationship = function(relation, userName, titreId, callback) {
	switch (relation) {
		case 'like':
			var query = 'MATCH (user:Utilisateur),(titre:Titre) WHERE user.nomUtilisateur = "'+userName+'" AND titre.idTitre = "'+titreId+
					'" MERGE (user)-[rel:AIME]->(titre) RETURN rel';
		break;
		case 'dislike':
    var query = 'MATCH (user:Utilisateur),(titre:Titre) WHERE user.nomUtilisateur = "'+userName+'" AND titre.idTitre = "'+titreId+
        '" MERGE (user)-[rel:DISLIKE]->(titre) RETURN rel';
		break;
    case 'unreco':
    var query = 'MATCH (user:Utilisateur),(titre:Titre) WHERE user.nomUtilisateur = "'+userName+'" AND titre.idTitre = '+titreId+
        '" MERGE (user)-[rel:RECO]->(titre) DELETE rel';
		break;

	}
	console.log(query);
	dbnode.cypherQuery(query, function (err, result) {
		console.log(err);
		//console.log(result);
		callback(err);
	});
}
