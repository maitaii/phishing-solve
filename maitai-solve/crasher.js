const express = require('express')
const crasher = express()
crasher.set('view engine', 'ejs');
var port = 3000
var username = ""

crasher.get('/username', (req, res) => {
    username=req.query.username
    return;
})

crasher.get('/moderator/logs', (req, res) => {
    res.render("../public/stage-3.ejs",{"username":username})
})

crasher.get('/bye', (req, res) => {
    console.log("Stage 3 Started, killing this process")
    process.exit(1)
})

crasher.listen(port, () => {
    console.log(`Crasher app listening on port ${port}`)
})