#!/usr/local/bin/node


// some comment
// another comment added from bitbicket


var c = {
  Reset: "\x1b[0m",
  Bright: "\x1b[1m",
  Dim: "\x1b[2m",
  Underscore: "\x1b[4m",
  Blink: "\x1b[5m",
  Reverse: "\x1b[7m",
  Hidden: "\x1b[8m",
  FgBlack: "\x1b[30m",
  FgRed: "\x1b[31m",
  FgGreen: "\x1b[32m",
  FgYellow: "\x1b[33m",
  FgBlue: "\x1b[34m",
  FgMagenta: "\x1b[35m",
  FgCyan: "\x1b[36m",
  FgWhite: "\x1b[37m",

  CRITICAL: "\x1b[30m\x1b[41m",
  ERROR: "\x1b[30m\x1b[41m",
  WARNING: "\x1b[30m\x1b[43m",
  INFO: "\x1b[30m\x1b[46m",
  DEBUG: "\x1b[37m\x1b[44m",
  NOTSET: "\x1b[37m\x1b[44m",

  BgBlack: "\x1b[40m",
  BgRed: "\x1b[41m",
  BgGreen: "\x1b[42m",
  BgYellow: "\x1b[43m",
  BgBlue: "\x1b[44m",
  BgMagenta: "\x1b[45m",
  BgCyan: "\x1b[46m",
  BgWhite: "\x1b[47m"
};
var created1 = 0;

/**
 * 
 */
String.prototype.toHHMMSS = function () {
  var sec_num = parseInt(this, 10); // don't forget the second param

  if (sec_num < 60) return this.substring(0, 6) + " sec."

  var hours = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours < 10) { hours = "0" + hours; }
  if (minutes < 10) { minutes = "0" + minutes; }
  if (seconds < 10) { seconds = "0" + seconds; }

  return hours + 'h ' + minutes + 'm ' + seconds + 's';
}

/**
 * 
 * @param {*} l 
 */
function parse_line(l) {

  // escaping for windows
  l = l.replace(/\\/g,'\\\\');

  try {
    ob = JSON.parse(l);
    var cc = parseFloat(ob.created) - parseFloat(created1);
    created1 = ob.created
    var sep = c.BgBlack + c.FgWhite + "\n--- " + c[ob.levelname] + " " + ob.levelname + " " + c.BgBlack +
      c.FgWhite + " -------- " + (cc > 3 ? (cc > 60 ? c.BgRed + c.FgBlack : c.FgRed) : c.FgGreen) +
      cc.toString().toHHMMSS() + c.BgBlack + c.FgWhite +
      " -------------------------------------------------------------------------------------------------------"
    console.log(sep.substring(0, 160));
    var metd = c.FgYellow +
      "Time: " + c.FgCyan + ob.asctime + c.FgYellow +
      " - Script: " + c.FgCyan + ob.filename + c.FgYellow +
      " - Function: " + c.FgCyan + ob.funcName + "() " + c.FgYellow +
      " - Line#: " + c.FgCyan + ob.lineno + c.FgYellow +
      "\n"
    console.log(metd);
    console.log(
      c.FgWhite + ob.message //.substring(0, 100)
    );
  } catch (eee) {
    console.log(eee);
  }
}

/* ---------------------------- Streaming --------------------------------- */

var encoding = 'utf-8';
function processData() {
  data.split(/\r\n|\n/).map(l => parse_line(l));;
}
if (process.stdin.isTTY) {
  data = new Buffer(process.argv[2] || '', encoding);
  processData();
} else {
  data = '';
  process.stdin.setEncoding(encoding);
  process.stdin.on('readable', function () {
    var chunk;
    while (chunk = process.stdin.read()) {
      data += chunk;
    }
  });
  process.stdin.on('end', function () {
    data = data.replace(/\n$/, '');
    processData();
  });
}
