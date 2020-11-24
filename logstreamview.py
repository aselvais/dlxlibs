#!/usr/bin/python3
import math, json, sys

c = {
  "Reset": "\x1b[0m",
  "Bright": "\x1b[1m",
  "Dim": "\x1b[2m",
  "Underscore": "\x1b[4m",
  "Blink": "\x1b[5m",
  "Reverse": "\x1b[7m",
  "Hidden": "\x1b[8m",
  "FgBlack": "\x1b[30m",
  "FgRed": "\x1b[31m",
  "FgGreen": "\x1b[32m",
  "FgYellow": "\x1b[33m",
  "FgBlue": "\x1b[34m",
  "FgMagenta": "\x1b[35m",
  "FgCyan": "\x1b[36m",
  "FgWhite": "\x1b[37m",

  "CRITICAL": "\x1b[30m\x1b[41m",
  "ERROR": "\x1b[30m\x1b[41m",
  "WARNING": "\x1b[30m\x1b[43m",
  "INFO": "\x1b[30m\x1b[46m",
  "DEBUG": "\x1b[37m\x1b[44m",
  "NOTSET": "\x1b[37m\x1b[44m",

  "BgBlack": "\x1b[40m",
  "BgRed": "\x1b[41m",
  "BgGreen": "\x1b[42m",
  "BgYellow": "\x1b[43m",
  "BgBlue": "\x1b[44m",
  "BgMagenta": "\x1b[45m",
  "BgCyan": "\x1b[46m",
  "BgWhite": "\x1b[47m"
}
created1 = 0


def console_log(v):
    """[summary]

    Args:
        v ([type]): [description]
    """
    print(v)


def toHHMMSS(v):
    """[summary]

    Args:
        v ([type]): [description]

    Returns:
        [type]: [description]
    """
    sec_num = v
    if sec_num < 60:
        return f"{v} sec."
    hours = math.floor(sec_num / 3600)
    minutes = math.floor((sec_num - (hours * 3600)) / 60)
    seconds = sec_num - (hours * 3600) - (minutes * 60)
    if hours < 10:
        hours = "0" + hours
    if minutes < 10:
        minutes = f"0{minutes}"
    if seconds < 10:
        seconds = f"0{seconds}"
    return f"{hours} h {minutes} m {seconds} s"


def parse_line(l):
    """[summary]

    Args:
        l ([type]): [description]
    """
    global created1, c
    # escaping for windows
    # l = l.replace(/\\/g,'\\\\');
    try:
        ob = json.loads(l);
        cc = float(ob["created"]) - float(created1)
        created1 = ob["created"]
        if cc > 60:
            ddd = c["BgRed"] + c["FgBlack"]
        elif cc > 3:
            ddd = c["FgRed"] + c["FgBlack"]
        else:
            ddd = c["FgGreen"] + c["BgBlack"]
        
        ccdd = toHHMMSS(cc)
        sep = f'''{c["BgBlack"]}{c["FgWhite"]} --- {c[ob["levelname"]]} {ob["levelname"]} {c["BgBlack"]}{c["FgWhite"]} -------- {ddd}{ccdd}{c["BgBlack"]}{c["FgWhite"]} -------------------------------------------------------------------------------------------------------'''
        str01 = sep[0:160]
        str02 = f'''{c["FgYellow"]}Time: {c["FgCyan"]}{ob["asctime"]}{c["FgYellow"]} - Script: {c["FgCyan"]}{ob["filename"]}{c["FgYellow"]} - Function: {c["FgCyan"]}{ob["funcName"]}() {c["FgYellow"]} - Line#: {c["FgCyan"]}{ob["lineno"]}{c["FgYellow"]}'''
        str03 = f'''{c["FgWhite"]}{ob["message"]}'''
        return f'''{str01}\n{str02}\n\n{str03}\n\n'''
    except Exception as e:
        return e



if __name__ == '__main__':
    for line in sys.stdin:
        print(parse_line(line))
