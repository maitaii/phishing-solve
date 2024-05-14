const express = require('express')
const fs = require('fs')
const path = require('path')

/*
 * We need a couple of server running.
 * The one listening on 9999 is for starting the exploit. 
 * The one listening on 3000 is for performing some DNS Rebinding magic.
 */

const starter = express()
var port = 9999

starter.get('/', (req, res) => {
    let filePath = path.join(__dirname, 'public/stage-1.html');
    fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            res.end();
        } else {
            console.log(err);
        }
    });
})

starter.get('/stage-two', (req, res) => {
    let filePath = path.join(__dirname, 'public/stage-2.html');
    fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
        if (!err) {
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            res.end();
        } else {
            console.log(err);
        }
    });
})

starter.listen(port, () => {
  console.log(`Starter listening on port ${port}`)
})