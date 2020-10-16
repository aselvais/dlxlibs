#!/usr/local/bin/node
var stdin = process.openStdin();
var data = "";
var c = {
  Reset : "\x1b[0m",
  Bright : "\x1b[1m",
  Dim : "\x1b[2m",
  Underscore : "\x1b[4m",
  Blink : "\x1b[5m",
  Reverse : "\x1b[7m",
  Hidden : "\x1b[8m",
  FgBlack : "\x1b[30m",
  FgRed : "\x1b[31m",
  FgGreen : "\x1b[32m",
  FgYellow : "\x1b[33m",
  FgBlue : "\x1b[34m",
  FgMagenta : "\x1b[35m",
  FgCyan : "\x1b[36m",
  FgWhite : "\x1b[37m",
  CRITICAL: "\x1b[31m",
  ERROR: "\x1b[31m",
  WARNING: "\x1b[33m",
  INFO: "\x1b[36m",
  DEBUG: "\x1b[36m",
  NOTSET: "\x1b[36m",
  BgBlack : "\x1b[40m",
  BgRed : "\x1b[41m",
  BgGreen : "\x1b[42m",
  BgYellow : "\x1b[43m",
  BgBlue : "\x1b[44m",
  BgMagenta : "\x1b[45m",
  BgCyan : "\x1b[46m",
  BgWhite : "\x1b[47m"
};
var created1 = 0;

function process_line(chunk) {
  data += chunk;
  chunk.toString('utf8').split("\n").map( l => {
      try {
        ob = JSON.parse(l);
        var cc = parseFloat(ob.created)-parseFloat(created1);
        created1 = ob.created
        var sep = c.FgWhite + "\n--- " + c.BgBlue + c[ob.levelname] + ob.levelname  + c.BgBlack +
                  c.FgWhite + " -------- " + ( cc > 3 ? c.FgRed : c.FgGreen ) + 
                  cc + " sec." + c[ob.levelname] + c.FgWhite + 
                  " -------------------------------------------------------------------------------------------------------"
        console.log(sep.substring(0, 150));
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
      } catch(eee) {}
  })
}

stdin.on('data', process_line);
