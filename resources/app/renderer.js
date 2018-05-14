// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
console.log("works?");
var PythonShell = require('python-shell');


PythonShell.run('/resources/app/test.py', function (err) {
    if (err) throw err;
    console.log('finished');
});
