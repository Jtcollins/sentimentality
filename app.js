/*eslint-env node*/

//------------------------------------------------------------------------------
// node.js starter application for Bluemix
//------------------------------------------------------------------------------

// This application uses express as its web server

/*globals res */
var express = require('express');

// cfenv provides access to your Cloud Foundry environment
// for more info, see: https://www.npmjs.com/package/cfenv
var cfenv = require('cfenv');

// create a new express server
var app = express();

// serve the files out of ./public as our main files
app.use(express.static(__dirname + '/public'));

// get the app environment from Cloud Foundry
var appEnv = cfenv.getAppEnv();
var path = require('path');

app.get('/', function(req, res){
	console.log("Entering get");
	res.sendFile(path.join(__dirname + '/public/index.html'));
});

// start server on the specified port and binding host
app.listen(appEnv.port, '0.0.0.0', function() {

	// print a message when the server starts listening
  console.log("server starting on " + appEnv.url);
 
//var ibmdb = require("ibm_db")
    //, cn = "DATABASE=SQLDB;HOSTNAME=75.126.155.153;PORT=50000;PROTOCOL=TCPIP;UID=user11343;PWD=OxVfEyZxD9Ms;"
   // ;




//app.get('/getData', function( req, res){

var ibmdb = require("ibm_db")
    , cn = "DATABASE=SQLDB;HOSTNAME=75.126.155.153;PORT=50000;PROTOCOL=TCPIP;UID=user11343;PWD=OxVfEyZxD9Ms;"
    ;



app.get('/getData', function(req, res) {


ibmdb.open(cn, function (err, conn) {
    if (err) {
        return console.log(err);
    }

    //we now have an open connection to the database
    //so lets get some data


 	conn.query("select country, AVG(SENT_VAL) FROM tweets GROUP BY country", function (err, rows, moreResultSets) {
        
        if (err) {
            console.log(err);
            //res.sendStatus(500);
        } else {
      
        	res.send(rows);
        	console.log("Row 1");
        	console.log(JSON.stringify(rows[1]));
          console.log(rows);
        }

        //if moreResultSets is truthy, then this callback function will be called
        //again with the next set of rows.
    });//end of query
});//End of ibmd.open
});});//End of app.get
